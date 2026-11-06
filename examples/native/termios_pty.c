/*
 * POSIX serial-port configuration with termios, exercised on a pseudo-terminal
 * pair. No real serial device is opened, so it is safe to run anywhere Linux
 * provides /dev/ptmx.
 *
 * Build: cc -std=c11 -Wall -Wextra -Werror examples/native/termios_pty.c -o /tmp/termios-pty
 * Run:   /tmp/termios-pty
 */
#define _XOPEN_SOURCE 700
#define _DEFAULT_SOURCE

#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <termios.h>
#include <time.h>
#include <unistd.h>

static int fail(const char *what)
{
    fprintf(stderr, "FAIL: %s (%s)\n", what, errno ? strerror(errno) : "no errno");
    return 1;
}

/* Opens a master/slave pseudo-terminal pair. The slave plays the "serial port". */
static int open_pty_pair(int *master, int *slave)
{
    *master = posix_openpt(O_RDWR | O_NOCTTY);
    if (*master < 0)
        return -1;
    if (grantpt(*master) < 0 || unlockpt(*master) < 0) {
        close(*master);
        return -1;
    }
    const char *name = ptsname(*master); /* single-threaded program: static buffer is fine */
    if (!name) {
        close(*master);
        return -1;
    }
    *slave = open(name, O_RDWR | O_NOCTTY);
    if (*slave < 0) {
        close(*master);
        return -1;
    }
    return 0;
}

/* 115200 8N1, no flow control, raw bytes, read returns after 0.5 s without data. */
static int configure_8n1_raw(int fd, speed_t baud)
{
    struct termios tio;
    if (tcgetattr(fd, &tio) < 0)
        return -1;
    cfmakeraw(&tio);                 /* no echo, no CR/LF translation, no signals */
    tio.c_cflag |= (CLOCAL | CREAD); /* ignore modem lines, enable receiver */
    tio.c_cflag &= ~(CSIZE | PARENB | CSTOPB | CRTSCTS);
    tio.c_cflag |= CS8;
    tio.c_cc[VMIN] = 0;              /* VMIN=0, VTIME>0: timed read, 0 bytes = timeout */
    tio.c_cc[VTIME] = 5;             /* tenths of a second */
    if (cfsetispeed(&tio, baud) < 0 || cfsetospeed(&tio, baud) < 0)
        return -1;
    return tcsetattr(fd, TCSAFLUSH, &tio); /* TCSAFLUSH: discard unread input first */
}

/* Reads exactly n bytes; a short read or a 0 return (VTIME expired) is handled explicitly. */
static int read_exact(int fd, unsigned char *buf, size_t n)
{
    size_t got = 0;
    int idle_rounds = 0;
    while (got < n) {
        ssize_t r = read(fd, buf + got, n - got);
        if (r < 0) {
            if (errno == EINTR)
                continue;
            return -1;
        }
        if (r == 0) {
            if (++idle_rounds >= 4) { /* about two seconds of silence */
                errno = ETIMEDOUT;
                return -1;
            }
            continue;
        }
        got += (size_t)r;
    }
    return 0;
}

static double seconds_since(const struct timespec *start)
{
    struct timespec now;
    clock_gettime(CLOCK_MONOTONIC, &now);
    return (double)(now.tv_sec - start->tv_sec) + (double)(now.tv_nsec - start->tv_nsec) / 1e9;
}

int main(void)
{
    int master, slave;
    errno = 0;
    if (open_pty_pair(&master, &slave) < 0)
        return fail("open pty pair");
    if (configure_8n1_raw(slave, B115200) < 0)
        return fail("configure slave");

    /* tcsetattr can report success when only some changes were applied; read back. */
    struct termios check;
    if (tcgetattr(slave, &check) < 0)
        return fail("tcgetattr");
    if ((check.c_cflag & CSIZE) != CS8 || (check.c_cflag & (PARENB | CSTOPB)) != 0)
        return fail("8N1 was not applied");
    if (check.c_lflag & (ECHO | ICANON))
        return fail("raw mode was not applied");

    /* 1. Bytes pass through unchanged: CR must not become LF in raw mode. */
    const unsigned char request[] = {'P', 'I', 'N', 'G', '\r', '\n', 0x00, 0xFF};
    if (write(master, request, sizeof request) != (ssize_t)sizeof request)
        return fail("write request");
    unsigned char got[sizeof request];
    if (read_exact(slave, got, sizeof got) < 0)
        return fail("read request on slave");
    if (memcmp(request, got, sizeof request) != 0)
        return fail("raw bytes were altered");

    /* 2. Reverse direction: the "device" answers. */
    const unsigned char reply[] = {'O', 'K', '\r'};
    if (write(slave, reply, sizeof reply) != (ssize_t)sizeof reply)
        return fail("write reply");
    unsigned char back[sizeof reply];
    if (read_exact(master, back, sizeof back) < 0)
        return fail("read reply on master");
    if (memcmp(reply, back, sizeof reply) != 0)
        return fail("reply was altered");

    /* 3. Silence: with VMIN=0/VTIME=5 read() returns 0 after roughly half a second. */
    struct timespec start;
    clock_gettime(CLOCK_MONOTONIC, &start);
    unsigned char one;
    ssize_t r = read(slave, &one, 1);
    double waited = seconds_since(&start);
    if (r != 0)
        return fail("expected timeout read to return 0");
    if (waited < 0.3 || waited > 2.0) {
        fprintf(stderr, "FAIL: timeout took %.2f s\n", waited);
        return 1;
    }

    close(slave);
    close(master);
    puts("termios pty loopback OK");
    return 0;
}
