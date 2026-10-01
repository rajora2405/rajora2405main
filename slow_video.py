import cv2

src = r"C:\Users\Harsh Vardhan Singh\Downloads\new_traffic.mp4.mp4"
dst = r"data\videos\traffic.mp4"

cap = cv2.VideoCapture(src)

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

frames = []

print("Reading video...")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frames.append(frame)

cap.release()

print("Original FPS:", fps)
print("Original frames:", len(frames))

output_fps = 25
target_frames = 1250

out = cv2.VideoWriter(
    dst,
    cv2.VideoWriter_fourcc(*"mp4v"),
    output_fps,
    (width, height)
)

print("Creating 50-second video...")

for i in range(target_frames):
    index = int(i * len(frames) / target_frames)
    out.write(frames[index])

out.release()

print("Created:", dst)
print("Duration: 50 seconds")