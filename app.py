import os
from flask import Flask, render_template, request, redirect, url_for
import json
import subprocess

app = Flask(__name__)
app.config['DATA_FOLDER'] = './static/data/'  # For processed files
app.config['UPLOAD_FOLDER'] = './static/data/'  # Same as DATA_FOLDER for now

# Ensure the data directory exists
os.makedirs(app.config['DATA_FOLDER'], exist_ok=True)

# Define speaker colors (add more colors if necessary)
colors = ['chat-speaker-0', 'chat-speaker-1', 'chat-speaker-2', 'chat-speaker-3', 'chat-speaker-4', 'chat-speaker-5', 'chat-speaker-6']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))

    # Save the uploaded file in the 'data' folder
    video_file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(video_file_path)

    # Define paths for the audio and transcription output files based on the uploaded filename
    base_filename = os.path.splitext(file.filename)[0]
    audio_file_path = os.path.join(app.config['DATA_FOLDER'], f"{base_filename}.mp3")
    transcription_file_path = os.path.join(app.config['DATA_FOLDER'], f"{base_filename}.json")

    # Set the environment variable for the API key (if necessary for preprocess.py)
    os.environ["PYANNOTE_API_KEY"] = "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"

    # Run preprocess.py with the appropriate arguments using subprocess.Popen
    try:
        process = subprocess.Popen(
            ['python3', 'preprocess.py', video_file_path, audio_file_path, transcription_file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()  # Wait for the process to finish
        if process.returncode != 0:
            return f"Error processing video: {stderr.decode()}", 500
    except Exception as e:
        return f"Error running preprocess.py: {str(e)}", 500

    # Load chat data from the JSON transcription file
    try:
        with open(transcription_file_path) as f:
            data = json.load(f)
            chat_data = data['contributions']
    except FileNotFoundError:
        return "Transcription file not found", 500
    except json.JSONDecodeError:
        return "Error decoding transcription file", 500

    # Generate speaker_classes dictionary
    speaker_classes = {}
    color_index = 0
    for message in chat_data:
        speaker = message['speaker']
        if speaker not in speaker_classes:
            speaker_classes[speaker] = colors[color_index]
            color_index = (color_index + 1) % len(colors)

    return render_template('results.html', chat_data=chat_data, speaker_classes=speaker_classes)

@app.route('/back', methods=['POST'])
def back():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
