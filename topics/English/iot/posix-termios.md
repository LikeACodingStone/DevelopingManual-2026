# POSIX Serial Ports: termios

- Aliases and ecosystem: termios / `tcgetattr` / `tcsetattr` (POSIX; Linux device nodes such as `/dev/ttyUSB0`; not the Qt serial API and not the Windows Win32 serial API)
- Versions and platforms: Linux / POSIX; the example is verified on Linux x86_64 using a pseudo-terminal
- Tags: iot
- Example status: compiled and run (pseudo-terminal loopback; no real serial port is opened); not integrated with a real device
- Code source: written independently for this handbook; all teaching code is in examples/; no historical project source is referenced

## What it is

termios is the POSIX interface that describes how terminals and serial ports behave. `struct termios` holds four groups of mode flags (input, output, control, local), an array of control characters (including `VMIN`/`VTIME`, which decide when a read returns), and the baud rate. Serial devices and pseudo-terminals (pty) are configured through the same interface.

## When to use

When you access a serial device directly from C on Linux, for example to talk to a card reader, a sensor or a debug port, and do not want a framework. When you need to be cross-platform (Windows, macOS), use a wrapper such as the [Qt serial](../../programming/qt-serial.md) page (Chinese only). termios only decides how bytes are sent and received; the device's message format comes from the device's own protocol documentation.

## How to use

1. Open the device with `open(path, O_RDWR | O_NOCTTY)`; save the old settings with `tcgetattr` first and restore them before exit.
2. Configure: `cfmakeraw()` gives "raw" mode (no echo, no line buffering, no CR/LF translation, no signal characters); then set 8N1: `c_cflag |= CS8`, clear `PARENB`, `CSTOPB` and `CRTSCTS`, and add `CLOCAL | CREAD`.
3. Baud rate: `cfsetispeed()` / `cfsetospeed()` with predefined values such as `B9600` or `B115200`.
4. Read timeout: `VMIN`/`VTIME`. `VMIN=0, VTIME=0` returns immediately; `VMIN>0, VTIME=0` blocks until `VMIN` bytes arrive; `VMIN=0, VTIME>0` waits at most `VTIME`×0.1 s and returns 0 on timeout; `VMIN>0, VTIME>0` is an inter-byte timeout.
5. Apply with `tcsetattr(fd, TCSAFLUSH, &tio)` and read back with `tcgetattr` to check, because `tcsetattr` can return success even when only some of the changes were applied.
6. The read/write loop must handle short reads, `EINTR` and the 0-byte return of a timeout; use `tcdrain()` when you must be sure the output has left.
7. A non-standard baud rate on Linux needs `termios2` with `BOTHER` (header `<asm/termbits.h>`, which cannot be included in the same translation unit as `<termios.h>`). This is a Linux-specific extension and has not been verified in this handbook.
8. Permissions: the user normally has to belong to a group such as `dialout` to open the device.

## Minimal example

Run the commands from the handbook root.

[termios_pty.c](../../../examples/native/termios_pty.c) creates a pseudo-terminal pair, configures the slave side as a "serial port" at 115200 8N1 in raw mode, and verifies: reading the settings back, bytes passing through unchanged (`\r` is not turned into `\n`, and `0x00` and `0xFF` are not lost), the reply in the other direction, and that `VMIN=0, VTIME=5` returns 0 after about half a second of silence.

```sh
cc -std=c11 -Wall -Wextra -Werror examples/native/termios_pty.c -o /tmp/termios-pty
/tmp/termios-pty
```

Expected: `termios pty loopback OK`. Run on Linux x86_64 with gcc 13.3. To confirm the check is effective, a mutation test was also done: with `cfmakeraw` removed, the example reports `raw mode was not applied` and exits with failure.

## FAQ

- A pseudo-terminal does not simulate baud rate, parity, flow control or line errors, so this example proves the configuration and read/write logic, not a real-device integration.
- A received `\r` becomes `\n`: `ICRNL` was not cleared; use `cfmakeraw()`.
- Reads block forever: check `VMIN`/`VTIME`, or use `select`/`poll`.
- Opening some USB serial devices pulls DTR low, which restarts boards with auto-reset.
- Several processes opening the same device steal data from each other; use exclusive open (`TIOCEXCL`) or a lock-file convention.
- After a USB serial device is unplugged, reads and writes usually return `EIO`; close and reopen.

## References

- [POSIX termios.h](https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/termios.h.html)
- [Linux termios(3)](https://man7.org/linux/man-pages/man3/termios.3.html)
- [Example verification scope](../../../examples/README_EN.md)
