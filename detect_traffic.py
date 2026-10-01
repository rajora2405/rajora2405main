import cv2
from ultralytics import YOLO

from ai.congestion import calculate_congestion


print("Loading YOLO model...")

model = YOLO("yolo11n.pt")

video_path = "data/videos/traffic.mp4"

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("ERROR: Could not open traffic video.")
    exit()


# Get video FPS
fps = cap.get(cv2.CAP_PROP_FPS)

if fps <= 0:
    fps = 30

delay = int(1000 / fps)


print("Traffic video opened successfully!")
print(f"Video FPS: {fps:.0f}")
print("Detecting only vehicles...")
print("Press Q inside the video window to stop.")


# Vehicle classes from COCO dataset
vehicle_classes = {
    2: "Car",
    3: "Motorcycle",
    5: "Bus",
    7: "Truck"
}


while True:

    ret, frame = cap.read()

    if not ret:
        print("Video finished.")
        break


    # YOLO detection
    results = model(frame, verbose=False)


    vehicle_count = 0


    # Copy original frame
    annotated_frame = frame.copy()


    # Process detections
    for box in results[0].boxes:

        class_id = int(box.cls[0])
        confidence = float(box.conf[0])


        # Ignore non-vehicles
        if class_id not in vehicle_classes:
            continue


        vehicle_count += 1


        # Bounding box
        x1, y1, x2, y2 = map(
            int,
            box.xyxy[0].tolist()
        )


        vehicle_name = vehicle_classes[class_id]


        # Label
        label = f"{vehicle_name} {confidence:.2f}"


        # Draw bounding box
        cv2.rectangle(
            annotated_frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )


        # Draw vehicle label
        cv2.putText(
            annotated_frame,
            label,
            (x1, max(y1 - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )


    # Calculate congestion
    congestion = calculate_congestion(vehicle_count)


    # Display vehicle count
    cv2.putText(
        annotated_frame,
        f"Vehicles: {vehicle_count}",
        (20, 45),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )


    # Display congestion level
    cv2.putText(
        annotated_frame,
        f"Congestion: {congestion}",
        (20, 85),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        2
    )


    # Display FPS
    cv2.putText(
        annotated_frame,
        f"FPS: {fps:.0f}",
        (20, 125),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 0),
        2
    )


    # Show video
    cv2.imshow(
        "Intelligent Traffic Congestion Detection",
        annotated_frame
    )


    # Maintain original speed
    key = cv2.waitKey(delay) & 0xFF


    # Press Q to stop
    if key == ord("q"):

        print("Stopped by user.")
        break


cap.release()

cv2.destroyAllWindows()

print("Detection stopped.")