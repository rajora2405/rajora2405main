import cv2
import json
import time
import paho.mqtt.client as mqtt
from ultralytics import YOLO

from ai.congestion import calculate_congestion
from database.db import create_database, insert_traffic_data


# ==============================
# CONFIGURATION
# ==============================

BROKER = "localhost"
PORT = 1883
TOPIC = "traffic/congestion"

MODEL_PATH = "yolo11n.pt"
VIDEO_PATH = "data/videos/traffic.mp4"

PUBLISH_INTERVAL = 2

VEHICLE_CLASSES = {
    2: "Car",
    3: "Motorcycle",
    5: "Bus",
    7: "Truck"
}


# ==============================
# DATABASE
# ==============================

print("Initializing database...")

create_database()

print("Database ready.")


# ==============================
# MQTT
# ==============================

print("Connecting to MQTT broker...")

client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)

client.connect(BROKER, PORT, 60)

client.loop_start()

print("Connected to MQTT broker.")


# ==============================
# YOLO MODEL
# ==============================

print("Loading YOLO model...")

model = YOLO(MODEL_PATH)

print("YOLO model loaded successfully.")


# ==============================
# VIDEO
# ==============================

cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():

    print("ERROR: Could not open traffic video.")

    client.loop_stop()
    client.disconnect()

    exit()


fps = cap.get(cv2.CAP_PROP_FPS)

if fps <= 0:
    fps = 30


delay = int(1000 / fps)


print("Traffic video opened successfully.")
print(f"Video FPS: {fps:.2f}")
print("Video Resolution: 1920 x 1080")
print("Detecting vehicles...")
print("Publishing MQTT data...")
print("Saving data to SQLite...")
print("Full-screen mode enabled.")
print("Press Q to stop.")


# ==============================
# FULL-SCREEN WINDOW
# ==============================

window_name = "Intelligent Traffic Congestion Detection"

cv2.namedWindow(
    window_name,
    cv2.WINDOW_NORMAL
)

cv2.setWindowProperty(
    window_name,
    cv2.WND_PROP_FULLSCREEN,
    cv2.WINDOW_FULLSCREEN
)


# ==============================
# MAIN LOOP
# ==============================

last_publish_time = 0


while True:

    ret, frame = cap.read()

    if not ret:

        print("Video finished.")

        break


    # ==============================
    # YOLO DETECTION
    # ==============================

    results = model(
        frame,
        verbose=False
    )


    vehicle_count = 0

    annotated_frame = frame.copy()


    # ==============================
    # PROCESS VEHICLES
    # ==============================

    for box in results[0].boxes:

        class_id = int(box.cls[0])

        confidence = float(box.conf[0])


        if class_id not in VEHICLE_CLASSES:
            continue


        vehicle_count += 1


        x1, y1, x2, y2 = map(
            int,
            box.xyxy[0].tolist()
        )


        vehicle_name = VEHICLE_CLASSES[class_id]

        label = f"{vehicle_name} {confidence:.2f}"


        # Draw bounding box

        cv2.rectangle(
            annotated_frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            3
        )


        # Draw vehicle label

        cv2.putText(
            annotated_frame,
            label,
            (x1, max(y1 - 10, 30)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )


    # ==============================
    # CONGESTION
    # ==============================

    congestion = calculate_congestion(
        vehicle_count
    )


    # ==============================
    # MQTT + DATABASE
    # ==============================

    current_time = time.time()


    if current_time - last_publish_time >= PUBLISH_INTERVAL:

        data = {
            "camera_id": "CAM_01",
            "vehicle_count": vehicle_count,
            "congestion_level": congestion
        }


        message = json.dumps(data)


        # Publish MQTT

        client.publish(
            TOPIC,
            message
        )


        print(
            "MQTT Published:",
            message
        )


        # Save to database

        insert_traffic_data(
            "CAM_01",
            vehicle_count,
            congestion
        )


        print(
            "Database Saved:",
            f"Vehicles={vehicle_count},",
            f"Congestion={congestion}"
        )


        last_publish_time = current_time


    # ==============================
    # DISPLAY INFORMATION
    # ==============================

    cv2.putText(
        annotated_frame,
        f"Vehicles: {vehicle_count}",
        (30, 55),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.3,
        (0, 255, 0),
        3
    )


    cv2.putText(
        annotated_frame,
        f"Congestion: {congestion}",
        (30, 105),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.3,
        (0, 255, 255),
        3
    )


    cv2.putText(
        annotated_frame,
        f"FPS: {fps:.0f}",
        (30, 155),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (255, 255, 0),
        3
    )


    cv2.putText(
        annotated_frame,
        "CAM_01",
        (30, 205),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (255, 255, 255),
        3
    )


    # ==============================
    # SHOW FULL-SCREEN VIDEO
    # ==============================

    cv2.imshow(
        window_name,
        annotated_frame
    )


    # ==============================
    # KEYBOARD CONTROL
    # ==============================

    key = cv2.waitKey(delay) & 0xFF


    if key == ord("q"):

        print("Stopped by user.")

        break


# ==============================
# CLEANUP
# ==============================

cap.release()

cv2.destroyAllWindows()

client.loop_stop()

client.disconnect()


print("MQTT disconnected.")
print("Detection stopped.")
print("Traffic data saved to database/traffic.db")