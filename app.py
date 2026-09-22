import streamlit as st
import tempfile, os, time
from gtts import gTTS
from deep_translator import GoogleTranslator
import whisper

st.set_page_config(layout="centered")
st.markdown("<h3 style='color:red; text-align:center'>FINAL FIX - VIDEO MARUTUNDI</h3>", unsafe_allow_html=True)

uploaded = st.file_uploader("Video Upload", type=["mp4","mp3"])
langs = st.multiselect("Dub to", ["English","Hindi","Telugu","Kannada","Tamil"], default=["English"])

if uploaded:
    st.write("👇 ORIGINAL VIDEO (Idi marchipothundi)")
    st.video(uploaded)

if uploaded and st.button("START DUBBING - ORIGINAL POTUNDI", type="primary", use_container_width=True):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(uploaded.read())
        v_path = tmp.name

    # Transcribe
    with st.spinner("Vintunna..."):
        model = whisper.load_model("base")
        result = model.transcribe(v_path, language="hi")
        text = result["text"][:500]
        if not text.strip():
            text = "Namaste dosto"
        st.success(f"Text: {text}")

    # DUBBING - FORCE NEW VIDEO
    for lang in langs:
        st.divider()
        st.write(f"🔊 DUBBING TO {lang}...")
        try:
            code = {"English":"en","Hindi":"hi","Telugu":"te","Kannada":"kn","Tamil":"ta"}.get(lang,"en")
            translated = GoogleTranslator(source='auto', target=code).translate(text)
            time.sleep(1)
            st.write(f"Translated: {translated}")

            audio_path = f"/tmp/{lang}_{int(time.time())}.mp3"
            out_path = f"/tmp/{lang}_{int(time.time())}_NEW.mp4"
            
            gTTS(text=translated, lang=code, slow=False).save(audio_path)
            
            # *** MAIN FIX - FULL RE-ENCODE, NOT COPY ***
            cmd = f'ffmpeg -y -i "{v_path}" -i "{audio_path}" -map 0:v:0 -map 1:a:0 -c:v libx264 -c:a aac -shortest "{out_path}"'
            os.system(cmd)

            if os.path.exists(out_path) and os.path.getsize(out_path) > 5000:
                st.success(f"✅ {lang} KOTHA VIDEO READY - Idi original kaadu!")
                st.write("👇 DUBBED VIDEO (Kotha voice tho):")
                st.video(out_path)
                st.audio(audio_path)
                
                # File size chupista - Original kanna different ani proof
                orig_size = os.path.getsize(v_path)
                new_size = os.path.getsize(out_path)
                st.caption(f"Original size: {orig_size} | Dubbed size: {new_size} - Marindi kada!")

                with open(out_path, "rb") as f:
                    st.download_button(f"⬇️ {lang} KOTHA VIDEO DOWNLOAD", f, file_name=f"{lang}_DUBBED_NEW.mp4", key=f"{lang}{time.time()}")
            else:
                st.error("ffmpeg fail ayindi - Audio matrame vachu")
                st.audio(audio_path)

        except Exception as e:
            st.error(str(e))
