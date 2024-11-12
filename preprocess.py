import sys
from sociaml.analysis import *
from sociaml.preprocessing import *
import os

# Set the API key directly in the script
os.environ["PYANNOTE_API_KEY"] = "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"
#pyannote_api_key = os.getenv("PYANNOTE_API_KEY")

# Paths provided through command-line arguments
video_file = sys.argv[1]
audio_file = sys.argv[2]
transcription_file = sys.argv[3]

# Extract audio from the video
audio_extractor = AudioExtractor()
audio, samplerate = audio_extractor.process(video_file, audio_path=audio_file)

# Transcribe and anonymize
transcriber = TranscriberAndDiarizer(
    pyannote_api_key=os.getenv("PYANNOTE_API_KEY"),
    merge_consecutive_speakers=False   
)

anonymizer = Anonymizer()
transcript = transcriber.process(video_file)
transcript = anonymizer.process(transcript)

# Save the transcription to a JSON file
with open(transcription_file, "w") as f:
    f.write(transcript.to_json())
