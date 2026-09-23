# World AI Video Dubbing Engine

This Streamlit application creates a real dubbed video in the selected language:

1. Extracts audio with FFmpeg.
2. Transcribes speech with Faster-Whisper, including timestamps.
3. Translates every timestamped speech segment.
4. Generates a clear Microsoft Edge neural voice in the selected language.
5. Fits each voice segment to its original timing and replaces the original audio track.

## Run locally

```bash
sudo apt-get install ffmpeg
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The first run downloads the selected Whisper model. `base` is a good balance of quality and CPU usage; `small` gives better transcription quality but uses more memory.

## Docker

```bash
docker build -t world-dub-engine .
docker run --rm -p 8501:8501 world-dub-engine
```

Open <http://localhost:8501>. For a GPU server, set `WHISPER_DEVICE=cuda` and `WHISPER_COMPUTE_TYPE=float16` and use a CUDA-compatible Faster-Whisper environment.

## Important

- The translation provider and Edge TTS require network access.
- Do not use this tool to imitate a real person's voice without their permission. The app uses licensed, generic neural voices.
- Large videos need sufficient disk space, RAM, and processing time.
