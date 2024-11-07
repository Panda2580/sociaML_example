# sociaml demo

Example of how to use the [sociaML library](https://github.com/davidrzs/sociaML) for video processing and transcription.

## Setup

1. Use [uv](https://github.com/astral-sh/uv) for managing Python virtual environment
2. Get your HuggingFace token from https://huggingface.co/settings/tokens
3. Replace `PUTKEYHERE` in main.py with your token

## Running

```bash
# Install dependencies
uv sync

# Run the preprocessing
uv run preprocess.py

# Run the main analysis
uv run preprocess.py
```

You will need a Huggingface API key which has access to [Pyannote](https://huggingface.co/pyannote/speaker-diarization-3.1) to run the preprocessing.