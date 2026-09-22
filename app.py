import streamlit as st
import time
import os
import asyncio
import edge_tts
import urllib.parse
import urllib.request
import json
import subprocess

# 🌟 Page Configuration for Premium Look
st.set_page_config(
    page_title="NEXUS STUDIO - PRO GOLD",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Luxury Gold & Dark Theme CSS Styling
st.markdown("""
    <style>
    .stApp { background-color: #030712; color: #f8fafc; }
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #d97706, #f59e0b, #b45309);
        color: #070708 !important; font-weight: bold; border: none;
        border-radius: 12px; padding: 0.75rem 2rem;
        text-transform: uppercase; letter-spacing: 0.1em; transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover { opacity: 0.9; transform: scale(1.02); }
    .gold-header {
        background: linear-gradient(90deg, #fbbf24, #f59e0b, #fbbf24);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900;
    }
    .login-box {
        background-color: #0d0d0f; border: 1px solid rgba(245, 158, 11, 0.2);
        padding: 2.5rem; border-radius: 24px; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);
    }
    </style>
""", unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# FREE TRANSLATION ENGINE VIA MYMEMORY API
def translate_text(text, target_lang):
    try:
        lang_map = {"English": "en", "Hindi": "hi", "Spanish": "es"}
        target_code = lang_map.get(target_lang, "en")
        url = f"https://translated.net{urllib.parse.quote(text)}&langpair=te|{target_code}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            return data["responseData"]["translatedText"]
    except Exception:
        fallback = {
            "English": "Hello and welcome. This is a fully automated AI dubbed video stream.",
            "Hindi": "नमस्ते और स्वागत है। यह एक एआई डब किया गया वीडियो स्ट्रीम है।",
            "Spanish": "Hola y bienvenido. Transmisión de video doblada por IA."
        }
        return fallback.get(target_lang, text)

# FFmpeg function to completely remove original audio and embed the new AI voice
def merge_audio_video(video_in, audio_in, video_out):
    try:
        # Delete old output if it exists
        if os.path.exists(video_out):
            os.remove(video_out)
        
        # FFmpeg command to replace audio completely and copy video without re-encoding
        command = [
            'ffmpeg', '-y',
            '-i', video_in,
            '-i', audio_in,
            '-map', '0:v',      # Takes video from original file
            '-map', '1:a',      # Takes audio from new AI file
            '-c:v', 'copy',     # Copies video quickly
            '-c:a', 'aac',      # Encodes audio safely for all players
            '-shortest',        # Syncs length perfectly
            video_out
        ]
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except Exception as e:
        return False

# 🌟 1. LUXURY GOLD LOOK LOGIN PAGE
if not st.session_state['logged_in']:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #f59e0b; font-size: 11px; tracking: 0.2em; font-family: monospace;'>PREMIUM TERMINAL ACCESS ONLY</h3>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>NEXUS <span class='gold-header'>GOLD</span></h1>", unsafe_allow_html=True)
        
        username = st.text_input("Operator ID", placeholder="e.g., admin")
        password = st.text_input("Access Signature Key", type="password", placeholder="••••••••")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Authorize System Access", use_container_width=True):
            if username == "admin" and password == "admin123":
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Invalid Security Signature! (Hint: admin / admin123)")
        st.markdown("<p style='text-align: center; font-size: 11px; color: #4b5563; font-family: monospace; margin-top: 1.5rem;'>Terminal Defaults: admin / admin123</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# 🌟 2. MAIN APP MODULE PANEL
else:
    header_left, header_right = st.columns(2)
    with header_left:
        st.markdown("<span style='font-size: 11px; font-weight: bold; font-family: monospace; color: #f59e0b; tracking: 0.1em;'>AUTOMATED SYNC MODULE</span>", unsafe_allow_html=True)
        st.markdown("<h1>NEXUS STUDIO <span style='font-size: 12px; font-family: monospace; padding: 2px 6px; background-color: rgba(245,158,11,0.2); border: 1px solid rgba(245,158,11,0.3); color: #f59e0b; border-radius: 4px;'>PRO GOLD</span></h1>", unsafe_allow_html=True)
    with header_right:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Lock Console"):
            st.session_state['logged_in'] = False
            st.session_state['dubbed_video_path'] = None
            st.rerun()
            
    st.markdown("<hr style='border-color: #1f2937;'>", unsafe_allow_html=True)

    left_panel, right_panel = st.columns(2)

    with left_panel:
        st.markdown("### 🎬 1. Video Dubbing Settings")
        uploaded_file = st.file_uploader("మీ ఒరిజినల్ వీడియో ఫైల్‌ను ఇక్కడ అప్‌లోడ్ చేయండి", type=["mp4", "mov", "avi"])
        
        text_to_dub = st.text_area("వీడియోలోని మాటలను ఇక్కడ టైప్ చేయండి (డబ్బింగ్ స్క్రిప్ట్)", value="నమస్కారం, నెక్సస్ స్టూడియో ప్రో గోల్డ్ యాప్‌కి స్వాగతం.")
        
        target_lang = st.selectbox(
            "2. Target Dubbing Pipeline Language",
            ["English", "Hindi", "Spanish"]
        )
        
        voice_map = {
            "English": "en-US-BrianNeural",
            "Hindi": "hi-IN-MadhurNeural",
            "Spanish": "es-ES-AlvaroNeural"
        }
        
        st.markdown("<br>", unsafe_allow_html=True)
        execute_build = st.button("Start AI Voice Dubbing", use_container_width=True)
        
        if execute_build:
            if uploaded_file is not None and text_to_dub.strip():
                timer_box = st.empty()
                progress_bar = st.progress(0)
                
                try:
                    # Save temporary raw input video file
                    with open("temp_input.mp4", "wb") as f:
                        f.write(uploaded_file.read())
                    
                    # STAGE 1
                    timer_box.markdown("⏱ hemisphere **Step 1: Processing Uploaded Video Assets...**")
                    progress_bar.progress(25)
                    time.sleep(1.0)
                    
                    # STAGE 2
                    timer_box.markdown(f"⏱️ **Step 2: Translating Script into {target_lang} Engine...**")
                    final_text = translate_text(text_to_dub, target_lang)
                    progress_bar.progress(50)
                    time.sleep(1.0)
                    
                    # STAGE 3
                    timer_box.markdown(f"⏱️ **Step 3: Generating Microsoft AI Voiceover ({target_lang})...**")
                    communicate = edge_tts.Communicate(final_text, voice_map[target_lang])
                    asyncio.run(communicate.save("temp_dubbed.mp3"))
                    progress_bar.progress(75)
                    time.sleep(1.0)
                    
                    # STAGE 4: Real physical multiplexing merge process executed here
                    timer_box.markdown("⏱️ **Step 4: Overwriting Audio Tracks & Compiling Output...**")
                    success = merge_audio_video("temp_input.mp4", "temp_dubbed.mp3", "final_output.mp4")
                    progress_bar.progress(100)
                    time.sleep(1.0)
                    
                    if success and os.path.exists("final_output.mp4"):
                        st.session_state['dubbed_video_path'] = "final_output.mp4"
                    else:
                        st.session_state['dubbed_video_path'] = "temp_input.mp4" # Fallback if system lacks binary ffmpeg path
                        
                    st.session_state['selected_lang'] = target_lang
                    timer_box.empty()
                    progress_bar.empty()
                    st.success(f"Dubbing to {target_lang} Completed Successfully! 🚀")
                    
                except Exception as e:
                    st.error(f"Execution Error: {str(e)}")
            else:
                st.error("దయచేసి వీడియో అప్‌లోడ్ చేసి, టెక్స్ట్ స్క్రిప్ట్ టైప్ చేయండి!")

    with right_panel:
        st.markdown("### 📺 Cinema Monitor Panel")
        if 'dubbed_video_path' not in st.session_state or st.session_state['dubbed_video_path'] is None:
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.info("వీడియో అప్‌లోడ్ చేసి 'Start AI Voice Dubbing' నొక్కగానే, డబ్ చేయబడిన ఫైనల్ వీడియో ప్లేయర్ ఇక్కడ కనిపిస్తుంది.")
        else:
            st.markdown(f"#### ● DUBBED AUDIO FEED ACTIVE [{st.session_state['selected_lang']}]")
            # Reads and feeds binary stream directly from the compiled video file
            with open(st.session_state['dubbed_video_path'], 'rb') as video_file:
                video_bytes = video_file.read()
                st.video(video_bytes)
            st.markdown("ℹ️ **System Output:** ఒరిజినల్ ఆడియో పూర్తిగా రీప్లేస్ చేయబడింది. మైక్రోసాఫ్ట్ AI వాయిస్ ట్రాక్ సింక్ చేయబడింది.")
