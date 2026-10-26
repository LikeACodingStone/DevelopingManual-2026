/* New local-only MQTT client. No connection without explicit --local-broker. */
#include <mosquitto.h>
#include <stdio.h>
#include <string.h>
static int delivered;
static void published(struct mosquitto *client, void *context, int mid) {
    (void)client; (void)context; (void)mid;
    delivered = 1;
}
int main(int argc, char **argv) {
    if (argc != 2 || strcmp(argv[1], "--local-broker")) {
        puts("No connection. Use --local-broker for 127.0.0.1:1883.");
        return 0;
    }
    if (mosquitto_lib_init() != MOSQ_ERR_SUCCESS) return 1;
    struct mosquitto *client = mosquitto_new(NULL, true, NULL);
    if (!client) { mosquitto_lib_cleanup(); return 1; }
    mosquitto_publish_callback_set(client, published);
    int rc = mosquitto_connect(client, "127.0.0.1", 1883, 10);
    if (rc == MOSQ_ERR_SUCCESS)
        rc = mosquitto_publish(client, NULL, "handbook/demo", 6, "sample", 1, false);
    for (int i = 0; rc == MOSQ_ERR_SUCCESS && !delivered && i < 30; ++i)
        rc = mosquitto_loop(client, 100, 1);
    if (rc == MOSQ_ERR_SUCCESS && delivered) puts("MQTT PUBACK received");
    mosquitto_disconnect(client);
    mosquitto_destroy(client);
    mosquitto_lib_cleanup();
    return rc == MOSQ_ERR_SUCCESS && delivered ? 0 : 1;
}
