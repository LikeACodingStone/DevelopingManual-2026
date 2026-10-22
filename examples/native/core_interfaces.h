#ifndef HANDBOOK_CORE_INTERFACES_H
#define HANDBOOK_CORE_INTERFACES_H
#include <pthread.h>
#define CORE_OK 0
#define CORE_ERROR -1
struct core_thread_counter { pthread_mutex_t mutex; int value; };
int core_thread_counter_init(struct core_thread_counter *counter);
int core_thread_counter_add(struct core_thread_counter *counter, int delta);
int core_thread_counter_get(struct core_thread_counter *counter);
void core_thread_counter_destroy(struct core_thread_counter *counter);
#endif
