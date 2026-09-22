import streamlit as st
import tempfile, os, time
from gtts import gTTS
import whisper
from deep_translator import MyMemoryTranslator

st.set_page_config(layout="centered")
st.markdown("<h3 style='text-align:center;color:red'>FIXED - NO GOOGLE BLOCK</h3>", unsafe_allow_html=True)

uploaded = st.file_uploader("Video Upload", type=["mp4","mp3"])
langs = st.multiselect("Dub to (Okkasari 1 select chey fast kosam)", ["English","Hindi","Telugu","Kannada","Tamil"], default=["English"])

if uploaded and st.button("START DUBBING", type="primary", use_container_width=True):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(uploaded.read())
        v_path = tmp.name
    st.video(uploaded)

    with st.spinner("Text vintunna..."):
        model = whisper.load_model("base")
        result = model.transcribe(v_path)
        text = result["text"].strip()[:400]  # 400 chars only - block raadu
        st.success(f"Original: {text}")

    # FIXED TRANSLATION - MyMemory (No Block)
    for lang in langs:
        st.divider()
        try:
            st.write(f"DUBBING TO {lang}...")
            # MyMemory codes
            codes = {"English":"en-GB","Hindi":"hi-IN","Telugu":"te-IN","Kannada":"kn-IN","Tamil":"ta-IN"}
            target = codes.get(lang,"en-GB")
            
            # MyMemory - No request limit
            translated = MyMemoryTranslator(source="en-US", target=target).translate(text)
            time.sleep(2)  # 2 sec gap - Google la block kaadu
            
            st.success(f"{lang}: {translated}")

            tts_codes = {"English":"en","Hindi":"hi","Telugu":"te","Kannada":"kn","Tamil":"ta"}
            audio_path = f"/tmp/{lang}_{int(time.time())}.mp3"
            out_path = f"/tmp/{lang}_{int(time.time())}.mp4"
            
            gTTS(text=translated, lang=tts_codes.get(lang,"en"), slow=False).save(audio_path)
            
            # Final Video Merge - 100% New Video
            os.system(f'ffmpeg -y -i "{v_path}" -i "{audio_path}" -map 0:v:0 -map 1:a:0 -c:v libx264 -c:a aac -shortest "{out_path}" > /dev/null 2>&1')
            
            if os.path.exists(out_path):
                st.video(out_path)
                with open(out_path,"rb") as f:
                    st.download_button(f"⬇️ {lang} DOWNLOAD", f, file_name=f"{lang}_dub.mp4", key=f"{lang}{time.time()}")
        except Exception as e:
            st.error(f"{lang} Error: {e} - 2 min aagi malli try chey")
