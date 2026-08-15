from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # downloads automatically first run (~6MB)
results = model("frame.jpg", save=True)

for r in results:
    for box in r.boxes:
        label = model.names[int(box.cls)]
        confidence = float(box.conf)
        print(f"Detected: {label} ({confidence:.2f} confidence)")
