import cv2, redis, base64, json, numpy as np
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
r = redis.Redis()

# Track the last-seen message ID per camera stream
streams = {"frames:cam1": "$", "frames:cam2": "$"}

print("AI worker watching:", list(streams.keys()))

while True:
    resp = r.xread(streams, block=1000, count=1)
    for stream_name, messages in resp or []:
        stream_name = stream_name.decode()
        for msg_id, data in messages:
            streams[stream_name] = msg_id  # move cursor forward
            jpg = base64.b64decode(data[b"jpg"])
            frame = cv2.imdecode(np.frombuffer(jpg, np.uint8), cv2.IMREAD_COLOR)

            results = model(frame, verbose=False)
            labels = [model.names[int(b.cls)] for res in results for b in res.boxes]

            cam_id = stream_name.split(":")[1]
            if labels:
                event = {"camera": cam_id, "detections": json.dumps(labels)}
                r.xadd("events", event)
                print(event)
