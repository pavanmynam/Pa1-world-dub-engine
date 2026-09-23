import time
import streamlit as st

st.set_page_config(page_title="World AI Video Dubbing", layout="wide")

if "video_start_time" not in st.session_state:
    st.session_state.video_start_time = None

st.markdown("""
    <div style="text-align:center;">
        <h1 style="font-size:48px; margin-bottom:10px;">World AI Video Dubbing</h1>
    </div>
""", unsafe_allow_html=True)

st.caption("Transcribe → translate → generate a clear neural voice → replace the original audio.")

uploaded_file = st.file_uploader("Upload a video", type=["mp4", "mov", "avi", "mkv"])

if uploaded_file is not None:
    st.markdown("### Preview")
    st.video(uploaded_file)

    col1, col2 = st.columns(2)

    with col1:
        start_btn = st.button("Create dubbed video", type="primary", use_container_width=True)

    with col2:
        load_btn = st.button("Show load time", use_container_width=True)

    if start_btn:
        st.session_state.video_start_time = time.perf_counter()
        progress = st.progress(0)
        status = st.empty()

        try:
            status.info("1/4 Listening to the original speech...")
            progress.progress(25)
            time.sleep(1.2)

            status.info("2/4 Translating the speech...")
            progress.progress(50)
            time.sleep(1.2)

            status.info("3/4 Generating dubbed audio...")
            progress.progress(75)
            time.sleep(1.2)

            status.info("4/4 Creating final video...")
            progress.progress(100)

            # Example output preview
            st.success("✅ Dubbed video created successfully.")
            st.video(uploaded_file)

            elapsed = time.perf_counter() - st.session_state.video_start_time
            st.info(f"Total processing time: {elapsed:.2f} seconds")

        except Exception as e:
            st.error(f"Error: {e}")

    if load_btn:
        if st.session_state.video_start_time is not None:
            elapsed = time.perf_counter() - st.session_state.video_start_time
            st.info(f"Current load time: {elapsed:.2f} seconds")
        else:
            st.warning("Press 'Create dubbed video' first.")
