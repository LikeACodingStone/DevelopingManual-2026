#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <pthread.h>
#include <semaphore.h>
#include <stdio.h>
#include <stdlib.h>
static sem_t ready;
static int value;
static void *producer(void *unused) {
    (void)unused;
    value = 42;
    if (sem_post(&ready)) abort();
    return NULL;
}
int main(void) {
    pthread_t thread;
    if (sem_init(&ready, 0, 0)) return EXIT_FAILURE;
    if (pthread_create(&thread, NULL, producer, NULL)) {
        sem_destroy(&ready); return EXIT_FAILURE;
    }
    int rc;
    do { rc = sem_wait(&ready); } while (rc == -1 && errno == EINTR);
    if (rc || pthread_join(thread, NULL)) return EXIT_FAILURE;
    printf("value=%d\n", value);
    if (sem_destroy(&ready)) return EXIT_FAILURE;
    return value == 42 ? EXIT_SUCCESS : EXIT_FAILURE;
}
