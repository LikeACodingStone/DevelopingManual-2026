#include <stdio.h>
#include <stdlib.h>
#include "core_interfaces.h"
static void *worker(void *arg) {
    struct core_thread_counter *c = arg;
    for (int i = 0; i < 10000; ++i) core_thread_counter_add(c, 1);
    return NULL;
}
int main(void) {
    struct core_thread_counter c;
    pthread_t a, b;
    if (core_thread_counter_init(&c) != CORE_OK) return EXIT_FAILURE;
    if (pthread_create(&a, NULL, worker, &c)) return EXIT_FAILURE;
    if (pthread_create(&b, NULL, worker, &c)) {
        pthread_join(a, NULL);
        core_thread_counter_destroy(&c);
        return EXIT_FAILURE;
    }
    if (pthread_join(a, NULL) || pthread_join(b, NULL)) return EXIT_FAILURE;
    int result = core_thread_counter_get(&c);
    core_thread_counter_destroy(&c);
    printf("counter=%d\n", result);
    return result == 20000 ? EXIT_SUCCESS : EXIT_FAILURE;
}
