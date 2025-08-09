import os
import subprocess
import time
from threading import Thread
from flask import Flask

# Get from environment variables set in Render dashboard
STREAM_URL = os.getenv("YOUTUBE_STREAM_URL")
STREAM_KEY = os.getenv("YOUTUBE_STREAM_KEY")

app = Flask(__name__)

@app.route("/")
def health():
    return "✅ Lofi Stream is live and running", 200

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

def start_stream():
    while True:
        print("🎬 Starting video loop stream...")
        
        command = [
            "ffmpeg",
            "-re",                                 # Send at real-time speed (essential)
            "-stream_loop", "-1", "-i", "out.mp4", # Loop video infinitely
            "-s", "640x360",                       # 360p resolution
            "-r", "30",                            # 30 FPS output
            "-b:v", "800k",                        # Video bitrate
            "-maxrate", "1000k",
            "-bufsize", "2000k",
            "-c:v", "libx264", "-preset", "veryfast",
            "-g", "60", "-keyint_min", "60",       # Keyframe every 2s
            "-c:a", "aac", "-b:a", "128k",         # Audio bitrate
            "-f", "flv",
            f"{STREAM_URL}/{STREAM_KEY}"
        ]

        try:
            process = subprocess.Popen(command)
            process.wait()
            print("🔁 Stream ended/crashed. Restarting in 5s...")
            time.sleep(5)
        except Exception as e:
            print(f"❌ Streaming error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    start_stream()
