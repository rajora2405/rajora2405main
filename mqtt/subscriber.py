import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "traffic/congestion"


def on_connect(client, userdata, flags, reason_code, properties):

    print("Connected to MQTT broker.")

    client.subscribe(TOPIC)

    print(f"Subscribed to: {TOPIC}")


def on_message(client, userdata, message):

    data = message.payload.decode()

    print("Received:", data)


client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)

client.on_connect = on_connect
client.on_message = on_message

print("Connecting...")

client.connect(BROKER, PORT, 60)

client.loop_forever()