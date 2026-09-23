import streamlit as st
import os
import asyncio
import time  # సమయాన్ని లెక్కించడానికి
from faster_whisper import WhisperModel
from deep_translator import GoogleTranslator
import edge_tts
from moviepy.editor import VideoFileClip, AudioFileClip

# Streamlit UI సెటప్
st.set_page_config(page_title="World AI Video Dubbing Engine", layout="wide")
st.title("🌐 World AI Video Dubbing Engine (Telugu & Multi-Language)")
st.write("Upload a video, transcribe it, translate it, and generate a high-quality AI voiceover!")

# లాంగ్వేజ్ మ్యాపింగ్ (Edge-TTS వాయిస్ కోడ్స్)
LANGUAGE_OPTIONS = {
    "Telugu (తెలుగు)": {"code": "te", "voice": "te-IN-MohanNeural"},
    "Hindi (हिंदी)": {"code": "hi", "voice": "hi-IN-MadhurNeural"},
    "English (US)": {"code": "en", "voice": "en-US-AriaNeural"},
    "Spanish (Español)": {"code": "es", "voice": "es-ES-AlvaroNeural"},
    "French (Français)": {"code": "fr", "voice": "fr-FR-DeniseNeural"}
}

# Edge-TTS వాయిస్ జనరేట్ చేయడానికి asynchronous ఫంక్షన్
async def generate_edge_tts(text, voice_name, output_path):
    communicate = edge_tts.Communicate(text, voice_name)
    await communicate.save(output_path)

# ఫైల్ అప్‌లోడర్
uploaded_file = st.file_uploader("Choose a video file...", type=["mp4", "mov", "avi"])

# టార్గెట్ లాంగ్వేజ్ సెలెక్షన్
selected_lang_name = st.selectbox("Select Target Language for Dubbing:", list(LANGUAGE_OPTIONS.keys()))
target_info = LANGUAGE_OPTIONS[selected_lang_name]

if uploaded_file is not None:
    # టెంపరరీగా ఇన్‌పుట్ వీడియో సేవ్ చేయడం
    with open("input_video.mp4", "wb") as f:
        f.write(uploaded_file.read())
        
    st.video("input_video.mp4")
    
    if st.button("🚀 Start AI Dubbing Process"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # ⏱️ డబ్బింగ్ టైమ్ లెక్కించడం ప్రారంభం
        start_time = time.time()
        
        try:
            # స్టెప్ 1: ఆడియో ఎక్స్‌ట్రాక్షన్ మరియు వీడియో నిడివి లెక్కించడం
            status_text.text("🔄 Step 1: Extracting audio from video...")
            video_clip = VideoFileClip("input_video.mp4")
            
            # 🎥 వీడియో నిడివి (Duration) సెకన్లలో కనుగొనడం
            video_duration_seconds = video_clip.duration
            
            video_clip.audio.write_audiofile("extracted_audio.mp3", logger=None)
            progress_bar.progress(20)
            
            # స్టెప్ 2: Faster-Whisper తో ట్రాన్స్‌క్రిప్షన్
            status_text.text("🎙️ Step 2: Transcribing audio using Faster-Whisper...")
            model = WhisperModel("base", device="cpu", compute_type="int8")
            segments, info = model.transcribe("extracted_audio.mp3", beam_size=5)
            
            original_text = " ".join([segment.text for segment in segments])
            st.info(f"**Detected Original Text:** {original_text}")
            progress_bar.progress(50)
            
            # స్టెప్ 3: అనువాదం (Translation)
            status_text.text(f"🔤 Step 3: Translating text to {selected_lang_name}...")
            translated_text = GoogleTranslator(source='auto', target=target_info["code"]).translate(original_text)
            st.success(f"**Translated Text ({selected_lang_name}):** {translated_text}")
            progress_bar.progress(70)
            
            # స్టెప్ 4: Microsoft Edge AI Voice తో వాయిస్ ఓవర్ సృష్టించడం
            status_text.text("🗣️ Step 4: Generating natural AI voiceover...")
            asyncio.run(generate_edge_tts(translated_text, target_info["voice"], "translated_audio.mp3"))
            progress_bar.progress(85)
            
            # స్టెప్ 5: కొత్త ఆడియోను వీడియోకి కలపడం (Merge)
            status_text.text("🎬 Step 5: Merging new voiceover with video...")
            new_audio_clip = AudioFileClip("translated_audio.mp3")
            
            final_clip = video_clip.set_audio(new_audio_clip)
            final_clip.write_videofile("output_dubbed_video.mp4", codec="libx264", audio_codec="aac", logger=None)
            
            # మెమరీ క్లియర్ చేయడం
            video_clip.close()
            new_audio_clip.close()
            final_clip.close()
            
            progress_bar.progress(100)
            status_text.text("🎉 Dubbing Completed Successfully!")
            
            # ⏱️ డబ్బింగ్ టైమ్ లెక్కించడం ముగింపు
            end_time = time.time()
            total_dubbing_time = end_time - start_time
            
            # 📊 వీడియో వివరాల కోసం కొత్త సెక్షన్ (Time Analysis)
            st.subheader("📊 Video & Processing Details")
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="🎥 Video Duration (వీడియో నిడివి)", value=f"{video_duration_seconds:.2f} Seconds")
            with col2:
                st.metric(label="⏱️ Total Dubbing Time (పట్టిన సమయం)", value=f"{total_dubbing_time:.2f} Seconds")
            
            # అవుట్‌పుట్ వీడియో ప్లేయర్ మరియు డౌన్‌లోడ్ బటన్
            st.subheader("📺 Dubbed Output Video")
            st.video("output_dubbed_video.mp4")
            
            with open("output_dubbed_video.mp4", "rb") as file:
                st.download_button(
                    label="📥 Download Dubbed Video",
                    data=file,
                    file_name="dubbed_video.mp4",
                    mime="video/mp4"
                )
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("💡 Suggestion: If it fails on memory, make sure your video is short (less than 1 minute) for testing.")
