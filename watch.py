import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture("rtsp://localhost:8554/cam1", cv2.CAP_FFMPEG)

print("Watching stream... Ctrl+C to stop")

while True:
    ret, frame = cap.read()
    if not ret:
        continue
    results = model(frame, verbose=False)
    labels = [model.names[int(b.cls)] for r in results for b in r.boxes]
    if labels:
        print("Detected:", labels)
