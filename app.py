import streamlit as st
import tempfile, os
from gtts import gTTS
from deep_translator import GoogleTranslator
import whisper

st.set_page_config(page_title="World Dub Engine", layout="wide")

st.markdown("""
<style>
.stApp { background: #0f0f0f; }
.main-card { background: #1a1a1a; border-radius: 20px; padding: 20px; border: 1px solid #333; }
.title-text { font-size: 30px; font-weight: 800; background: linear-gradient(90deg, #FF0000, #FF6A00); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title-text">WORLD AUTO LINGUAL ENGINE - ROBO DUB</p>', unsafe_allow_html=True)

left, right = st.columns([1,1])
with left:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    uploaded = st.file_uploader("Telugu Video Upload", type=["mp4","mp3","wav","m4a"])
    if uploaded:
        st.video(uploaded)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    langs = st.multiselect("Languages", ["Hindi","English","Tamil","Kannada","Spanish","French","German","Arabic","Japanese"], default=["Hindi","English"])
    st.markdown('</div>', unsafe_allow_html=True)

if st.button("START DUBBING - ROBO VOICE", use_container_width=True):
    if not uploaded:
        st.error("Video upload chey bro")
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            tmp.write(uploaded.read())
            tmp_path = tmp.name

        with st.spinner("Telugu text chestunna..."):
            model = whisper.load_model("base")
            result = model.transcribe(tmp_path, language="te")
            telugu_text = result["text"]
            if not telugu_text.strip():
                telugu_text = "Namaste, ee video Telugu nunchi vere bhashalalo dubb ayindi."
            st.success(f"Telugu: {telugu_text[:200]}")

        code_map = {"Hindi":"hi","English":"en","Kannada":"kn","Tamil":"ta","French":"fr","German":"de","Spanish":"es","Arabic":"ar","Japanese":"ja"}

        for lang in langs:
            l_code = code_map.get(lang, "en")
            st.divider()
            st.markdown(f"### {lang}")
            try:
                translated = GoogleTranslator(source='auto', target=l_code).translate(telugu_text[:400])
                st.write(translated)
                audio_path = f"/tmp/{lang}.mp3"
                tts = gTTS(text=translated, lang=l_code)
                tts.save(audio_path)
                video_out = f"/tmp/{lang}_dubbed.mp4"
                os.system(f'ffmpeg -y -i "{tmp_path}" -i "{audio_path}" -map 0:v:0 -map 1:a:0 -shortest -c:v copy "{video_out}"')
                if os.path.exists(video_out) and os.path.getsize(video_out) > 1000:
                    st.video(video_out)
                    st.audio(audio_path)
                    with open(video_out, "rb") as f:
                        st.download_button(f"{lang} VIDEO DOWNLOAD", f, file_name=f"{lang}_dubbed.mp4", key=lang)
                else:
                    st.audio(audio_path)
            except Exception as e:
                st.error(f"{lang} Error: {e}")
