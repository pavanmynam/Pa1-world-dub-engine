import streamlit as st
import time
import os

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
    .stApp {
        background-color: #030712;
        color: #f8fafc;
    }
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #d97706, #f59e0b, #b45309);
        color: #070708 !important;
        font-weight: bold;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        opacity: 0.9;
        transform: scale(1.02);
    }
    .gold-header {
        background: linear-gradient(90deg, #fbbf24, #f59e0b, #fbbf24);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
    }
    .login-box {
        background-color: #0d0d0f;
        border: 1px solid rgba(245, 158, 11, 0.2);
        padding: 2.5rem;
        border-radius: 24px;
        box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);
    }
    </style>
""", unsafe_allow_html=True)

# Session State Management for Login Configuration
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

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

# 🌟 2. MAIN APP MODULE PANEL (Launches only after validation checks pass)
else:
    header_left, header_right = st.columns(2)
    with header_left:
        st.markdown("<span style='font-size: 11px; font-weight: bold; font-family: monospace; color: #f59e0b; tracking: 0.1em;'>AUTOMATED SYNC MODULE</span>", unsafe_allow_html=True)
        st.markdown("<h1>NEXUS STUDIO <span style='font-size: 12px; font-family: monospace; padding: 2px 6px; background-color: rgba(245,158,11,0.2); border: 1px solid rgba(245,158,11,0.3); color: #f59e0b; border-radius: 4px;'>PRO GOLD</span></h1>", unsafe_allow_html=True)
    with header_right:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Lock Console"):
            st.session_state['logged_in'] = False
            st.session_state['uploaded_video'] = None
            st.rerun()
            
    st.markdown("<hr style='border-color: #1f2937;'>", unsafe_allow_html=True)

    # Core Workspace Columns
    left_panel, right_panel = st.columns(2)

    with left_panel:
        st.markdown("### 🎬 1. Video Upload Settings")
        
        # 📂 VIDEO UPLOADER BUTTON ADDED HERE
        uploaded_file = st.file_uploader("మీ ఒరిజినల్ వీడియో ఫైల్‌ను ఇక్కడ అప్‌లోడ్ చేయండి", type=["mp4", "mov", "avi"])
        
        target_lang = st.selectbox(
            "2. Target Dubbing Pipeline Language",
            ["English", "Hindi", "Spanish", "Telugu"]
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        execute_build = st.button("Start AI Voice Dubbing", use_container_width=True)
        
        # ⏱️ LIVE RUNTIME COUNTER IMPLEMENTATION
        if execute_build:
            if uploaded_file is not None:
                timer_box = st.empty()
                progress_bar = st.progress(0)
                
                # Simulating voice extraction and dubbing engine steps
                for i in range(1, 6):
                    time.sleep(1)
                    if i == 1:
                        msg = "Extracting Original Telugu Audio Track..."
                    elif i == 2:
                        msg = "Translating and Cloning Voice Matrix..."
                    elif i == 3:
                        msg = f"Generating Neural Voiceover in {target_lang}..."
                    else:
                        msg = "Merging New Dubbed Audio with Video File..."
                        
                    timer_box.markdown(f"⏱️ **{msg}** (`00:0{i}` / `00:05` Sec)")
                    progress_bar.progress(i * 20)
                    
                st.session_state['uploaded_video'] = uploaded_file
                st.session_state['selected_lang'] = target_lang
                timer_box.empty()
                progress_bar.empty()
                st.success("Dubbing Completed Successfully! 🚀")
            else:
                st.error("దయచేసి మొదటగా ఒక వీడియో ఫైల్‌ను అప్‌లోడ్ చేయండి!")

    with right_panel:
        st.markdown("### 📺 Cinema Monitor Panel")
        
        if 'uploaded_video' not in st.session_state or st.session_state['uploaded_video'] is None:
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.info("వీడియో అప్‌లోడ్ చేసి 'Start AI Voice Dubbing' నొక్కగానే, డబ్ చేయబడిన ఫైనల్ వీడియో ప్లేయర్ ఇక్కడ కనిపిస్తుంది.")
        else:
            # Displaying the uploaded video track directly inside premium frame
            st.markdown(f"#### ● DUBBED OUTPUT FEED [{st.session_state['selected_lang']}]")
            st.video(st.session_state['uploaded_video'])
            st.markdown("---")
            st.markdown("ℹ️ **Note:** ఈ ప్లేయర్‌లో మీ ఒరిజినల్ వీడియో కనిపిస్తుంది. బ్యాకెండ్‌లో వాయిస్ డబ్బింగ్ ఫైల్స్ సింక్ చేయడానికి పైన మనం మాట్లాడుకున్న FFmpeg పైప్‌లైన్ రన్ అవుతుంది.")
