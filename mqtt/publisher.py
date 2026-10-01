import json
import time
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "traffic/congestion"

client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)

print("Connecting to MQTT broker...")

client.connect(BROKER, PORT, 60)

client.loop_start()

print("Connected to MQTT broker.")

for i in range(5):

    data = {
        "camera_id": "CAM_01",
        "vehicle_count": 10 + i,
        "congestion_level": "MEDIUM"
    }

    message = json.dumps(data)

    result = client.publish(TOPIC, message)

    print("Published:", message)

    time.sleep(2)

client.loop_stop()
client.disconnect()

print("MQTT publisher finished.")