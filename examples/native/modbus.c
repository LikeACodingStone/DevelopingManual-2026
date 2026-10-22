#include <modbus/modbus.h>
#include <stdio.h>
/* Read-only local simulator example; no device writes. */
int main(void) {
    modbus_t *ctx = modbus_new_tcp("127.0.0.1", 1502);
    if (!ctx) return 1;
    int ok = modbus_set_slave(ctx, 1) == 0 &&
             modbus_set_response_timeout(ctx, 2, 0) == 0;
    int connected = ok && modbus_connect(ctx) == 0;
    uint16_t values[2];
    int count = connected ? modbus_read_registers(ctx, 0, 2, values) : -1;
    if (count == 2) printf("registers=%u,%u\n", values[0], values[1]);
    else perror("modbus");
    if (connected) modbus_close(ctx);
    modbus_free(ctx);
    return count != 2;
}
