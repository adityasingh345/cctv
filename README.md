# CCTV to AI Pipeline - Prototype

## What this is

A small working prototype that shows how CCTV camera footage can be sent live into an AI system that automatically detects objects (like people) in the video, in real time.

This is a proof of concept built on a single laptop, using simulated cameras, to test if the overall approach works before doing it with real cameras and real infrastructure.

## What I built, in simple terms

**1. Simulated cameras**
Since I don't have real CCTV cameras to test with, I used a tool called FFmpeg to take a normal video file and make it act exactly like a live camera feed. This gave me two fake "cameras" streaming live video, the same way real IP cameras would.

**2. A video server**
I set up a small server (MediaMTX) that receives the video from these cameras, the same way a real CCTV system has a central box that all cameras connect to.

**3. Pulling frames out of the video**
I wrote a small script that connects to a camera's live stream and grabs individual images (frames) from it, a few times per second. This turns "video" into individual pictures that a program can actually look at and analyze.

**4. A queue in the middle**
Instead of connecting the camera directly to the AI, I added a queue (using a tool called Redis) in between. The camera script just drops frames into this queue, and doesn't care what happens to them after that.

This is an important design choice: it means the part that watches the camera and the part that runs the AI are completely separate. I can add more cameras, or more AI processing power, without them affecting each other.

**5. AI detection**
I wrote a second script that picks up frames from the queue and runs an AI model (YOLO) on them to detect objects. It correctly identifies things like people in the video.

**6. Multiple cameras at once**
I tested this with two simulated cameras running at the same time, both feeding into the same queue. One single AI script was able to handle detections from both cameras at the same time, and correctly tell which camera each detection came from. Adding the second camera required no changes to the AI script at all, which is the main thing I wanted to prove.

## What works right now

- Two live simulated camera feeds running at the same time
- A working video server receiving both feeds
- Frames being pulled from each camera automatically
- One AI process detecting objects (people) from both camera feeds live
- Detected events (which camera, what was detected) being pushed into the queue

## What is not done yet

- Detections are only shown on screen right now, nothing is being saved permanently. Next step is to store this in a proper database so it can be searched later (e.g. "show all detections from camera 2 yesterday between 2-3 PM")
- Only tested with one AI process. For more cameras, this needs to be able to run in parallel across multiple processes
- Still using fake/simulated cameras, not real CCTV hardware
- No alerts, no security/login, no encryption yet
- No monitoring to check if a camera feed drops or the system is running smoothly


Once all of this is running, detections will start printing on screen, showing which camera and what was detected, live.

## What's next

1. Save the detections into a proper database instead of just printing them, so they can be searched and reviewed later
2. Run multiple AI processes at once so it can handle more cameras without slowing down
3. Replace the fake cameras with real CCTV cameras
4. Add basic security (login, encrypted connections)
5. Add monitoring so we know if a camera goes offline or something breaks
6. Move this from a laptop to proper servers/cloud so it can actually run at scale
