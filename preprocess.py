from sociaml.analysis import *
from sociaml.preprocessing import *

import os


os.environ["PYANNOTE_API_KEY"] = "PUTKEYHERE"


# preprocess video, only the viddeo_file must exist, the other two will be created

video_file = "./data/oath.webm"
audio_file = "./data/oath.mp3"
transcription_file = "./data/oath.json"


audio_extractor = AudioExtractor()
audio, samplerate = audio_extractor.process(video_file, audio_path=audio_file)


# transcripe and anonymize
transcriber = TranscriberAndDiarizer(
    pyannote_api_key=os.getenv("PYANNOTE_API_KEY"), merge_consecutive_speakers=False
)
anonymizer = Anonymizer()
transcript = transcriber.process(video_file)
transcript = anonymizer.process(transcript)


with open(transcription_file, "w") as f:
    f.write(transcript.to_json())


#
