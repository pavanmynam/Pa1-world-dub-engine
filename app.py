import asyncio
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Callable, Dict, List, Optional

import edge_tts
import streamlit as st
from faster_whisper import WhisperModel
from deep_translator import GoogleTranslator


LANGUAGES: Dict[str, Dict[str, str]] = {
    "English": {"code": "en", "voice": "en-US-JennyNeural"},
    "Hindi": {"code": "hi", "voice": "hi-IN-SwaraNeural"},
    "Telugu": {"code": "te", "voice": "te-IN-ShrutiNeural"},
    "Tamil": {"code": "ta", "voice": "ta-IN-PallaviNeural"},
    "Kannada": {"code": "kn", "voice": "kn-IN-SapnaNeural"},
    "Malayalam": {"code": "ml", "voice": "ml-IN-SobhanaNeural"},
    "Spanish": {"code": "es", "voice": "es-ES-ElviraNeural"},
    "French": {"code": "fr", "voice": "fr-FR-DeniseNeural"},
    "German": {"code": "de", "voice": "de-DE-KatjaNeural"},
    "Arabic": {"code": "ar", "voice": "ar-SA-ZariyahNeural"},
    "Japanese": {"code": "ja", "voice": "ja-JP-NanamiNeural"},
    "Korean": {"code": "ko", "voice": "ko-KR-SunHiNeural"},
    "Portuguese": {"code": "pt", "voice": "pt-BR-FranciscaNeural"},
}

SOURCE_LANGUAGES = {
    "Auto detect": None,
    "Telugu": "te",
    "Hindi": "hi",
    "English": "en",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml",
}


@st.cache_resource(show_spinner=False)
def load_whisper_model(model_size: str) -> WhisperModel:
    # CPU/int8 keeps deployment affordable. Set WHISPER_DEVICE=cuda for a GPU host.
    device = os.getenv("WHISPER_DEVICE", "cpu")
    compute_type = os.getenv("WHISPER_COMPUTE_TYPE", "int8" if device == "cpu" else "float16")
    return WhisperModel(model_size, device=device, compute_type=compute_type)


def run_ffmpeg(args: List[str]) -> None:
    process = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args], text=True, capture_output=True)
    if process.returncode:
        raise RuntimeError(process.stderr.strip() or "FFmpeg failed")


def transcribe_video(video_path: Path, source_language: Optional[str], model_size: str):
    with tempfile.TemporaryDirectory() as directory:
        audio_path = Path(directory) / "audio.wav"
        run_ffmpeg(["-i", str(video_path), "-vn", "-ac", "1", "-ar", "16000", str(audio_path)])
        model = load_whisper_model(model_size)
        segments, info = model.transcribe(
            str(audio_path),
            language=source_language,
            vad_filter=True,
            beam_size=5,
            condition_on_previous_text=True,
        )
        result = [{"start": float(s.start), "end": float(s.end), "text": s.text.strip()} for s in segments if s.text.strip()]
        detected = source_language or info.language
        return result, detected


def split_text(text: str, limit: int = 450) -> List[str]:
    words = text.split()
    chunks: List[str] = []
    current = ""
    for word in words:
        if current and len(current) + len(word) + 1 > limit:
            chunks.append(current)
            current = word
        else:
            current = f"{current} {word}".strip()
    if current:
        chunks.append(current)
    return chunks or [text]


def translate_segments(segments: List[dict], target_code: str, source_code: Optional[str], progress: Optional[Callable[[int], None]] = None) -> List[dict]:
    translated: List[dict] = []
    translator = GoogleTranslator(source=source_code or "auto", target=target_code)
    for index, segment in enumerate(segments):
        text = segment["text"]
        if source_code == target_code:
            output = text
        else:
            # Translation services have request-size limits, so translate each segment in safe pieces.
            output = " ".join(translator.translate(part) for part in split_text(text))
        translated.append({**segment, "text": output})
        if progress:
            progress(int((index + 1) * 100 / max(1, len(segments))))
    return translated


async def save_tts(text: str, voice: str, output: Path) -> None:
    communicator = edge_tts.Communicate(text=text, voice=voice, rate="+0%", volume="+0%")
    await communicator.save(str(output))


def create_dubbed_track(segments: List[dict], voice: str, output: Path, progress: Optional[Callable[[int], None]] = None) -> None:
    if not segments:
        raise RuntimeError("No speech was detected in the video")
    with tempfile.TemporaryDirectory() as directory:
        work = Path(directory)
        concat_entries: List[str] = []
        for index, segment in enumerate(segments):
            raw = work / f"speech_{index:05d}.mp3"
            fitted = work / f"fitted_{index:05d}.wav"
            asyncio.run(save_tts(segment["text"], voice, raw))
            duration = max(0.25, segment["end"] - segment["start"])
            # atempo supports 0.5..2.0 per filter. Chaining handles larger adjustments.
            ratio = max(0.5, min(2.0, duration / max(0.05, get_media_duration(raw))))
            filters = []
            while ratio < 0.5:
                filters.append("atempo=0.5")
                ratio /= 0.5
            while ratio > 2.0:
                filters.append("atempo=2.0")
                ratio /= 2.0
            filters.append(f"atempo={ratio:.6f}")
            run_ffmpeg(["-i", str(raw), "-af", ",".join(filters), "-ar", "48000", "-ac", "1", str(fitted)])
            delay_ms = max(0, int(segment["start"] * 1000))
            delayed = work / f"delayed_{index:05d}.wav"
            run_ffmpeg(["-i", str(fitted), "-af", f"adelay={delay_ms}:all=1", "-ar", "48000", "-ac", "1", str(delayed)])
            concat_entries.append(str(delayed))
            if progress:
                progress(int((index + 1) * 100 / len(segments)))

        # Mix overlapping speech segments instead of dropping one of them.
        inputs: List[str] = []
        for item in concat_entries:
            inputs.extend(["-i", item])
        filter_graph = "".join(f"[{i}:a]" for i in range(len(concat_entries))) + f"amix=inputs={len(concat_entries)}:duration=longest:dropout_transition=0:normalize=0[a]"
        run_ffmpeg([*inputs, "-filter_complex", filter_graph, "-map", "[a]", "-ar", "48000", "-ac", "2", str(output)])


def get_media_duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        check=True, text=True, capture_output=True,
    )
    return float(result.stdout.strip())


def merge_audio_video(video_path: Path, audio_path: Path, output_path: Path) -> None:
    run_ffmpeg(["-i", str(video_path), "-i", str(audio_path), "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(output_path)])


def main() -> None:
    st.set_page_config(page_title="World Dub Engine", page_icon="🎙️", layout="wide")
    st.title("🎙️ World AI Video Dubbing")
    st.caption("Transcribe → translate → generate a clear neural voice → replace the original audio")

    with st.sidebar:
        st.header("Dubbing settings")
        source_name = st.selectbox("Original language", list(SOURCE_LANGUAGES))
        target_name = st.selectbox("Dub into", list(LANGUAGES), index=0)
        model_size = st.selectbox("Speech recognition model", ["tiny", "base", "small"], index=1, help="Use small for better accuracy if your server has enough RAM.")
        st.info(f"Voice: {LANGUAGES[target_name]['voice']}")

    upload = st.file_uploader("Upload a video", type=["mp4", "mov", "mkv", "webm", "avi"])
    if not upload:
        st.warning("Upload a video to begin.")
        return

    if st.button("🚀 Create dubbed video", type="primary", use_container_width=True):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            input_path = folder / (Path(upload.name).stem + Path(upload.name).suffix)
            output_path = folder / "dubbed_video.mp4"
            audio_path = folder / "dubbed_audio.wav"
            input_path.write_bytes(upload.getbuffer())
            progress = st.progress(0)
            status = st.empty()
            try:
                status.info("1/4 Listening to the original speech…")
                segments, detected_code = transcribe_video(input_path, SOURCE_LANGUAGES[source_name], model_size)
                if not segments:
                    raise RuntimeError("No speech was detected. Try a clearer video or another source-language setting.")
                progress.progress(25)

                status.info(f"2/4 Translating speech to {target_name}…")
                translated = translate_segments(segments, LANGUAGES[target_name]["code"], detected_code, lambda p: progress.progress(25 + p // 4))
                progress.progress(50)

                status.info("3/4 Generating the selected neural voice and syncing timing…")
                create_dubbed_track(translated, LANGUAGES[target_name]["voice"], audio_path, lambda p: progress.progress(50 + p // 4))
                progress.progress(75)

                status.info("4/4 Replacing the original audio track…")
                merge_audio_video(input_path, audio_path, output_path)
                progress.progress(100)
                status.success(f"Done — {target_name} dubbing is ready. Detected source: {detected_code}.")
                st.video(str(output_path))
                st.download_button("⬇️ Download dubbed video", output_path.read_bytes(), "dubbed_video.mp4", "video/mp4", use_container_width=True)
            except Exception as error:
                status.empty()
                st.error(f"Dubbing failed: {error}")


if __name__ == "__main__":
    main()
