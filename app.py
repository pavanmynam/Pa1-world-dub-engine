import streamlit as st

st.set_page_config(page_title="World Dub Engine", layout="wide")

# --- PREMIUM CSS ---
st.markdown("""
<style>
.stApp { background: #0f0f0f; }
.main-card {
  background: linear-gradient(145deg, #1a1a1a, #232323);
  border-radius: 20px; padding: 25px;
  border: 1px solid #333; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}
.title-text {
  font-size: 32px; font-weight: 800; 
  background: linear-gradient(90deg, #FF0000, #FF6A00);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.video-box { border-radius: 15px; overflow: hidden; border: 2px solid #333; }
.lang-chip { background: #272727; border-radius: 20px; padding: 8px 15px; color: white; margin: 5px; display: inline-block;}
</style>
""", unsafe_allow_html=True)

# --- HEADER LIKE YOUTUBE APP ---
col1, col2 = st.columns([1,5])
with col1:
    st.markdown("## ▶️")
with col2:
    st.markdown('<p class="title-text">WORLD AUTO LINGUAL ENGINE</p>', unsafe_allow_html=True)
    st.caption("Telugu YouTubers ki World Reach - Powered by AI")

st.divider()

# --- MAIN APP FRAME ---
left, right = st.columns([1.2, 1])

with left:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("### 📤 Upload Telugu Video")
    uploaded = st.file_uploader("", type=["mp4","mp3","wav"])
    if uploaded:
        st.video(uploaded)
        st.success("Video Ready for World Dubbing")
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("### 🌍 Select World Languages")
    langs = st.multiselect("Languages", 
    ["Hindi","English","Tamil","Kannada","Spanish","French","Arabic","Japanese","German","Telugu","Russian","Korean"],
    default=["Hindi","English","Tamil"])
    
    for lang in langs:
        st.markdown(f'<span class="lang-chip">🔊 {lang} ✓</span>', unsafe_allow_html=True)
    
    st.write("")
    if st.button("🚀 START WORLD DUBBING", use_container_width=True):
        st.balloons()
        st.markdown("#### 🎬 Dubbed Players")
        for lang in langs:
            with st.container():
                st.markdown(f"**{lang} - Dubbed Version**")
                if uploaded:
                    st.video(uploaded) # temporary - will be replaced with dubbed audio video
                st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3") # demo player
                st.markdown("✅ Audio Track Ready")
                st.divider()
    st.markdown('</div>', unsafe_allow_html=True)
