import streamlit as st
import tempfile, os, time
from gtts import gTTS
from deep_translator import MyMemoryTranslator
import whisper

st.set_page_config(page_title="World Dub Engine", layout="wide")
st.markdown('<h2 style="color:#FF0000">WORLD DUB - FINAL FIX</h2>', unsafe_allow_html=True)

uploaded = st.file_uploader("Video Upload (Telugu/Hindi/Urdu)", type=["mp4","mp3","wav","m4a"])
if uploaded:
    st.video(uploaded)

langs = st.multiselect("Languages", ["Hindi","English","Kannada","Tamil","French","German"], default=["Hindi","English"])

if st.button("START DUBBING - ROBO VOICE", use_container_width=True):
    if not uploaded:
        st.error("Video upload chey")
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            tmp.write(uploaded.read())
            tmp_path = tmp.name

        with st.spinner("Voice vintunna..."):
            model = whisper.load_model("base")
            result = model.transcribe(tmp_path)  # auto language - Telugu/Hindi edaina
            original_text = result["text"]
            detected_lang = result.get("language","auto")
            if not original_text.strip():
                original_text = "Hello friends welcome to our channel"
            st.success(f"Detected [{detected_lang}]: {original_text[:300]}")

        code_map = {"Hindi":"hi-IN","English":"en-GB","Kannada":"kn-IN","Tamil":"ta-IN","French":"fr-FR","German":"de-DE"}
        tts_map = {"Hindi":"hi","English":"en","Kannada":"kn","Tamil":"ta","French":"fr","German":"de"}

        for lang in langs:
            st.divider()
            st.subheader(lang)
            try:
                # MyMemory - No block
                target = code_map.get(lang,"en-GB")
                translated = MyMemoryTranslator(source="auto", target=target).translate(original_text[:400])
                time.sleep(1.5)  # Google block avvakunda gap
                st.write(f"**{translated}**")

                tts_lang = tts_map.get(lang,"en")
                audio_path = f"/tmp/{lang}.mp3"
                gTTS(text=translated, lang=tts_lang).save(audio_path)
                
                video_out = f"/tmp/{lang}_dubbed.mp4"
                os.system(f'ffmpeg -y -i "{tmp_path}" -i "{audio_path}" -map 0:v:0 -map 1:a:0 -shortest -c:v copy "{video_out}" > /dev/null 2>&1')
                
                st.audio(audio_path)
                if os.path.exists(video_out) and os.path.getsize(video_out) > 1000:
                    st.video(video_out)
                    with open(video_out, "rb") as f:
                        st.download_button(f"Download {lang} Video", f, file_name=f"{lang}.mp4", key=f"v{lang}")
                else:
                    with open(audio_path, "rb") as f:
                        st.download_button(f"Download {lang} Audio", f, file_name=f"{lang}.mp3", key=f"a{lang}")

            except Exception as e:
                st.error(f"{lang} Error: {e}")
                time.sleep(2)
