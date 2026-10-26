import java.nio.charset.StandardCharsets;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

// Java SE example. Android service lifecycle is a separate integration contract.
public final class PahoLocal {
    public static void main(String[] args) throws Exception {
        if (args.length != 1 || !args[0].equals("--local-broker")) {
            System.out.println("No connection. Use --local-broker for 127.0.0.1:1883.");
            return;
        }
        MqttClient client = new MqttClient("tcp://127.0.0.1:1883",
                MqttClient.generateClientId(), new MemoryPersistence());
        try {
            MqttConnectOptions options = new MqttConnectOptions();
            options.setCleanSession(true);
            options.setConnectionTimeout(3);
            options.setAutomaticReconnect(false);
            client.setTimeToWait(3000);
            client.connect(options);
            MqttMessage message = new MqttMessage("sample".getBytes(StandardCharsets.UTF_8));
            message.setQos(1);
            message.setRetained(false);
            client.publish("handbook/demo", message);
            System.out.println("MQTT publish completed");
        } finally {
            try {
                if (client.isConnected()) client.disconnect(1000);
            } finally {
                client.close();
            }
        }
    }
}
