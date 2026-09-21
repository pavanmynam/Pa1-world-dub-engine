                for lang in langs:
                    l_code = code_map.get(lang,"en")
                    translated = GoogleTranslator(source='auto', target=l_code).translate(telugu_text[:400])
                    tts = gTTS(text=translated, lang=l_code)
                    audio_path = f"/tmp/{lang}.mp3"
                    tts.save(audio_path)
                    
                    # VIDEO + DUBBED AUDIO MERGE
                    video_out = f"/tmp/{lang}_dubbed_video.mp4"
                    os.system(f"ffmpeg -y -i {tmp_path} -i {audio_path} -map 0:v -map 1:a -shortest -c:v copy {video_out}")

                    st.markdown(f"### 🎬 {lang} - Dubbed Video")
                    st.write(f"**Translated:** {translated[:100]}...")
                    st.video(video_out)
                    st.audio(audio_path)
                    
                    with open(video_out, "rb") as f:
                        st.download_button(f"⬇️ {lang} Dubbed VIDEO Download", f, file_name=f"{lang}_dubbed.mp4", key=f"v_{lang}")
                    st.divider()
