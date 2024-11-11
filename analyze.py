from sociaml.analysis import *
from sociaml.preprocessing import *
from sociaml.datastructures import AnalysisMode

from sociaml.text_analysis import GlobalSentimentAnalyzer, GlobalEkmanEmotionAnalyzer, ParticipantEkmanEmotionAnalyzer, ParticipantNLTKTokenCountAnalyzer, ParticipantContributionCount,ParticipantSentimentAnalyzer,ParticipantSentenceTransformerEmbeddingAnalyzer
from sociaml.audio_analysis import ParticipantAudioSpeakingTimeAnalyzer, ParticipantMFCCAnalyzer, ParticipantAudioSilenceTimeAnalyzer, GlobalAudioEmotionAnalyzer,ParticipantAudioEmotionAnalyzer

import os

os.environ["PYANNOTE_API_KEY"] = "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"


# preprocess video, only the viddeo_file must exist, the other two will be created

video_file = "./data/convo.webm"
audio_file = "./data/convo.mp3"
transcription_file = "./data/convo.json"

with open(transcription_file) as f:
    transcription = Transcription.from_json(f.read())


analysis = Analysis(
                    
                    # textual features
                    GlobalSentimentAnalyzer(mode=AnalysisMode.ENTIRE), 
                    GlobalEkmanEmotionAnalyzer(mode=AnalysisMode.ENTIRE),
                    ParticipantEkmanEmotionAnalyzer(),
                    ParticipantSentimentAnalyzer(),
                    ParticipantNLTKTokenCountAnalyzer(),
                    ParticipantContributionCount(),
                    ParticipantSentenceTransformerEmbeddingAnalyzer(),
                    
                    
                    # audio features
                    GlobalAudioEmotionAnalyzer(mode=AnalysisMode.ENTIRE),
                    ParticipantAudioEmotionAnalyzer(),
                    ParticipantAudioSpeakingTimeAnalyzer(),
                    ParticipantMFCCAnalyzer(),
                    ParticipantAudioSilenceTimeAnalyzer(),
                    
                    
            )


global_data, participant_data, contribution_data = analysis.analyze(transcription, str(video_file), str(audio_file))

# print(global_data)
# print(participant_data)
print(contribution_data)