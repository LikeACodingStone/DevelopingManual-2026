/* Independently written bounded counter with checked pthread operations. */
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
struct counter { pthread_mutex_t lock; unsigned value; };
static void require(int error) {
    if (error) { fprintf(stderr, "pthread error: %d\n", error); exit(EXIT_FAILURE); }
}
static void *increment(void *context) {
    struct counter *counter = context;
    for (unsigned i = 0; i < 10000; ++i) {
        require(pthread_mutex_lock(&counter->lock));
        counter->value++;
        require(pthread_mutex_unlock(&counter->lock));
    }
    return NULL;
}
int main(void) {
    struct counter counter = { .value = 0 };
    pthread_t threads[2];
    require(pthread_mutex_init(&counter.lock, NULL));
    unsigned created = 0;
    int error = 0;
    for (; created < 2; ++created) {
        error = pthread_create(&threads[created], NULL, increment, &counter);
        if (error) break;
    }
    for (unsigned i = 0; i < created; ++i) require(pthread_join(threads[i], NULL));
    require(pthread_mutex_destroy(&counter.lock));
    if (error) { fprintf(stderr, "pthread_create: %d\n", error); return 1; }
    printf("counter=%u\n", counter.value);
    return counter.value == 20000 ? 0 : 1;
}
