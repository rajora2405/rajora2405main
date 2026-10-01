from ultralytics import YOLO
import torch

print("PyTorch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())

print("Loading YOLO model...")

model = YOLO("yolo11n.pt")

print("YOLO model loaded successfully!")