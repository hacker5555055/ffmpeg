from flask import Flask, request, send_file
import subprocess

app = Flask(__name__)

@app.route('/process_video', methods=['POST'])
def process_video():
    # Expecting a video and audio file in the POST request
    video_file = request.files['video']
    audio_file = request.files['audio']

    # Save files locally
    video_path = '/app/input_video.mp4'
    audio_path = '/app/input_audio.mp3'
    output_path = '/app/output_video.mp4'

    video_file.save(video_path)
    audio_file.save(audio_path)

    # Run FFmpeg command to merge video and audio
    ffmpeg_command = [
        'ffmpeg', '-i', video_path, '-i', audio_path, 
        '-c:v', 'copy', '-c:a', 'aac', '-shortest', output_path
    ]
    subprocess.run(ffmpeg_command)

    # Return the processed video file
    return send_file(output_path, as_attachment=True, download_name='output_video.mp4')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
