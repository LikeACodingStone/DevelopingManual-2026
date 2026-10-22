#include <stdarg.h>
#include <stdio.h>
#if defined(__GNUC__) || defined(__clang__)
__attribute__((format(printf, 1, 2)))
#endif
static int log_message(const char *format, ...) {
    va_list args;
    va_start(args, format);
    int result = vprintf(format, args);
    va_end(args);
    return result;
}
int main(void) {
    return log_message("name=%s count=%d ratio=%.1f\n", "PCM", 2, 0.5) < 0;
}
