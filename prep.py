import os
import json
import logging
from flask import Flask, render_template, send_from_directory

# Flask App für die Anzeige der Resultate
app = Flask(__name__)
app.config['DATA_FOLDER'] = './static/data/'
colors = ['chat-speaker-0', 'chat-speaker-1', 'chat-speaker-2', 'chat-speaker-3']

# Path to the JSON file
transcription_filename = "pizza.json"

@app.route('/')
def index():
    transcription_file = os.path.join(app.config['DATA_FOLDER'], transcription_filename)

    try:
        # Load the JSON file
        with open(transcription_file) as f:
            data = json.load(f)
            chat_data = data['contributions']

        # Create the speaker_classes dictionary
        speaker_classes = {}
        color_index = 0
        for message in chat_data:
            speaker = message['speaker']
            if speaker not in speaker_classes:
                speaker_classes[speaker] = colors[color_index]
                color_index = (color_index + 1) % len(colors)

        # Render the results.html page, passing the transcription filename
        return render_template(
            'results.html',
            chat_data=chat_data,
            speaker_classes=speaker_classes,
            transcription_filename=transcription_filename
        )

    except Exception as e:
        return f"Ein Fehler ist aufgetreten: {str(e)}", 500

@app.route('/download_transcript/<filename>')
def download_transcript(filename):
    transcription_file = os.path.join(app.config['DATA_FOLDER'], filename)
    
    if not os.path.exists(transcription_file):
        logging.error("Transcription file not found.")
        return "Transcription file not found", 404
    
    return send_from_directory(
        directory=app.config['DATA_FOLDER'],
        path=filename,
        as_attachment=True
    )

if __name__ == "__main__":
    print("Öffne results.html im Browser...")
    app.run(debug=True)
