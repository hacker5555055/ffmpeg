# app.py
from flask import Flask, request, jsonify
import os
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return "FFmpeg on Render.com is ready!"

@app.route('/process-video', methods=['POST'])
def process_video():
    input_file = request.json.get("input_file")
    output_file = "/tmp/output.mp4"  # Temporary file for storing processed video

    # Run an FFmpeg command (this example converts the video to 1-minute clip)
    try:
        command = [
            "ffmpeg", "-i", input_file, "-t", "00:01:00",  # Set duration to 1 minute
            "-c:v", "libx264", "-c:a", "aac", output_file
        ]
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            return jsonify({"error": result.stderr}), 500

        return jsonify({"message": "Video processed successfully!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
