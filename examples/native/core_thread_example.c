#include <pthread.h>
#include <stdio.h>

#include "core_interfaces.h"

int core_thread_counter_init(struct core_thread_counter *counter)
{
    /* Validate the caller supplied counter pointer. */
    if (counter == NULL)
        return CORE_ERROR;

    /* Start the counter from zero for repeatable tests. */
    counter->value = 0;

    /* Initialize the mutex used by all counter operations. */
    if (pthread_mutex_init(&counter->mutex, NULL) != 0)
        return CORE_ERROR;

    /* Return success after the mutex is ready. */
    return CORE_OK;
}

int core_thread_counter_add(struct core_thread_counter *counter, int delta)
{
    /* Validate the caller supplied counter pointer. */
    if (counter == NULL)
        return CORE_ERROR;

    /* Lock before modifying the shared value. */
    pthread_mutex_lock(&counter->mutex);

    /* Apply the requested delta. */
    counter->value += delta;

    /* Copy the value while still under the lock. */
    int result = counter->value;

    /* Unlock before returning to the caller. */
    pthread_mutex_unlock(&counter->mutex);

    /* Return the new value for simple assertions. */
    return result;
}

int core_thread_counter_get(struct core_thread_counter *counter)
{
    /* Validate the caller supplied counter pointer. */
    if (counter == NULL)
        return CORE_ERROR;

    /* Lock before reading the shared value. */
    pthread_mutex_lock(&counter->mutex);

    /* Copy the current value while protected. */
    int result = counter->value;

    /* Unlock after the read is complete. */
    pthread_mutex_unlock(&counter->mutex);

    /* Return the protected value. */
    return result;
}

void core_thread_counter_destroy(struct core_thread_counter *counter)
{
    /* Ignore NULL counters during cleanup. */
    if (counter == NULL)
        return;

    /* Destroy the mutex owned by this counter. */
    pthread_mutex_destroy(&counter->mutex);
}
