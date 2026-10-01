import cv2

src = r"data\videos\traffic.mp4"
dst = r"data\videos\traffic_1080p.mp4"

cap = cv2.VideoCapture(src)

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

out = cv2.VideoWriter(
    dst,
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps,
    (1920, 1080)
)

print("Upscaling video...")
print("Original:", width, "x", height)
print("Output: 1920 x 1080")
print("FPS:", fps)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame_1080 = cv2.resize(
        frame,
        (1920, 1080),
        interpolation=cv2.INTER_CUBIC
    )

    out.write(frame_1080)

cap.release()
out.release()

print("Created:", dst)