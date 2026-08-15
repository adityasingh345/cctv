import cv2

# Connect to the live stream (same URL you just watched in VLC)
cap = cv2.VideoCapture("rtsp://localhost:8554/cam1", cv2.CAP_FFMPEG)

if not cap.isOpened():
    print("Failed to connect to stream")
else:
    ret, frame = cap.read()
    if ret:
        cv2.imwrite("frame.jpg", frame)
        print("Saved frame.jpg — shape:", frame.shape)
    else:
        print("Connected, but couldn't read a frame")

cap.release()
