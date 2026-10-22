#include <MQTTClient.h>
#include <stdio.h>
#include <stdlib.h>
int main(int argc, char **argv) {
    if (argc != 2) { fprintf(stderr, "usage: paho tcp://localhost:1883\n"); return 2; }
    MQTTClient client;
    int rc = MQTTClient_create(&client, argv[1], "handbook-publisher",
                              MQTTCLIENT_PERSISTENCE_NONE, NULL);
    if (rc != MQTTCLIENT_SUCCESS) return 1;
    MQTTClient_connectOptions options = MQTTClient_connectOptions_initializer;
    options.keepAliveInterval = 20; options.cleansession = 1;
    options.connectTimeout = 5;
    rc = MQTTClient_connect(client, &options);
    if (rc == MQTTCLIENT_SUCCESS) {
        MQTTClient_message msg = MQTTClient_message_initializer;
        char payload[] = "PCM";
        msg.payload = payload; msg.payloadlen = 3; msg.qos = 1; msg.retained = 0;
        MQTTClient_deliveryToken token;
        rc = MQTTClient_publishMessage(client, "handbook/demo", &msg, &token);
        if (rc == MQTTCLIENT_SUCCESS) rc = MQTTClient_waitForCompletion(client, token, 5000L);
        int disconnect_rc = MQTTClient_disconnect(client, 1000);
        if (rc == MQTTCLIENT_SUCCESS) rc = disconnect_rc;
    }
    MQTTClient_destroy(&client);
    if (rc != MQTTCLIENT_SUCCESS) fprintf(stderr, "MQTT error=%d\n", rc);
    return rc != MQTTCLIENT_SUCCESS;
}
