import cv2, redis, base64, sys, time

cam_id = sys.argv[1]          # e.g. "cam1"
rtsp_url = sys.argv[2]        # e.g. rtsp://localhost:8554/cam1

r = redis.Redis()
cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)

print(f"[{cam_id}] ingesting...")

while True:
    ret, frame = cap.read()
    if not ret:
        continue
    _, buf = cv2.imencode('.jpg', frame)
    r.xadd(f"frames:{cam_id}", {"jpg": base64.b64encode(buf).decode()})
    time.sleep(0.5)  # sample ~2 frames/sec instead of flooding the queue
