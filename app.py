import streamlit as st
st.set_page_config(
    page_title="AI Meeting Summarizer",
    page_icon="📝",
    layout="centered"
)
from components.uploader import file_uploader
from components.transcript import show_transcript
from components.summary import show_summary
from services.transcription import transcribe_audio
from services.summarization import summarize_text
from services.translation import translate_summary, LANG_CODES
import os

# --- Custom CSS for modern blue-purple RGBA gradient background, card, and modern UI ---
st.markdown(
    '''
    <style>
    body {
        background: linear-gradient(135deg, rgba(102,126,234,0.95) 0%, rgba(118,75,162,0.95) 100%) !important;
    }
    .stApp {
        background: linear-gradient(135deg, rgba(102,126,234,0.95) 0%, rgba(118,75,162,0.95) 100%) !important;
        min-height: 100vh;
    }
    .main-card {
        background: rgba(255,255,255,0.92);
        border-radius: 18px;
        box-shadow: 0 6px 32px 0 rgba(79,139,249,0.10);
        padding: 2.5rem 2rem 2rem 2rem;
        max-width: 700px;
        margin: 2.5rem auto 2rem auto;
    }
    .gradient-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ff9966 0%, #ff5e62 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-fill-color: transparent;
        margin-bottom: 0.5em;
        text-align: center;
        letter-spacing: 1px;
        text-shadow: 0 2px 8px rgba(79,139,249,0.10);
    }
    .main-card * {
        color: #1a1a1a !important;
        font-family: 'Segoe UI', 'Arial', sans-serif;
    }
    /* Selected value in selectbox */
    .stSelectbox div[data-baseweb="select"] > div {
        color: #111 !important;
    }
    .stButton>button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6em 1.5em;
        font-weight: 600;
        font-size: 1.1em;
        box-shadow: 0 2px 8px rgba(102,126,234,0.15);
        transition: 0.2s;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #764ba2 0%, #667eea 100%);
        color: #fff;
        box-shadow: 0 4px 16px rgba(118,75,162,0.15);
    }
    .stDownloadButton>button {
        background: linear-gradient(90deg, #764ba2 0%, #667eea 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6em 1.5em;
        font-weight: 600;
        font-size: 1.1em;
        box-shadow: 0 2px 8px rgba(118,75,162,0.15);
        transition: 0.2s;
    }
    .stDownloadButton>button:hover {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: #fff;
        box-shadow: 0 4px 16px rgba(102,126,234,0.15);
    }
    .stSelectbox>div>div {
        background: #f5f6fa !important;
        border-radius: 8px !important;
    }
    .stExpanderHeader {
        font-weight: 700;
        color: #667eea !important;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

with st.container():
    
    st.markdown('<div class="gradient-title">AI Meeting Summarizer</div>', unsafe_allow_html=True)
    st.markdown("""
    Upload your meeting audio, and get a summary in your preferred language!
    """)

    with st.expander("ℹ️ Model Info"):
        st.markdown("""
        - **Transcription:** [OpenAI Whisper base](https://github.com/openai/whisper)
        - **Summarization:** [facebook/bart-large-cnn](https://huggingface.co/facebook/bart-large-cnn)
        - **Translation:** [facebook/nllb-200-distilled-600M](https://huggingface.co/facebook/nllb-200-distilled-600M)
        """)

    uploaded_file = file_uploader()
    output_lang = st.selectbox("Select summary language", list(LANG_CODES.keys()), index=0, help="Choose the language for your summary.")

    if uploaded_file:
        st.info("Step 1: File uploaded. Starting transcription...")
        with st.spinner("Transcribing audio (Whisper)..."):
            transcript, tmpfile_path, wav_path, transcribe_err = transcribe_audio(uploaded_file)
        if transcribe_err:
            st.error(f"Transcription failed: {transcribe_err}")
        else:
            st.success("Step 2: Transcription complete.")
            show_transcript(transcript)
            st.download_button(
                label="Download Transcript",
                data=transcript,
                file_name="transcript.txt"
            )
            st.info("Step 3: Summarizing transcript...")
            with st.spinner("Summarizing (BART)..."):
                summary, summary_err = summarize_text(transcript)
            if summary_err:
                st.error(f"Summarization failed: {summary_err}")
            else:
                st.success("Step 4: Summary ready.")
                show_summary(summary, lang="English")
                st.button("Copy Summary to Clipboard", on_click=lambda: st.session_state.update({'clipboard': summary}), help="Copy the English summary.")
                if output_lang != "English":
                    st.info(f"Step 5: Translating summary to {output_lang}...")
                    with st.spinner(f"Translating to {output_lang} (NLLB-200)..."):
                        translated_summary, translate_err = translate_summary(summary, output_lang)
                    if translate_err:
                        st.error(f"Translation failed: {translate_err}")
                    else:
                        st.success(f"Summary translated to {output_lang}.")
                        show_summary(translated_summary, lang=output_lang)
                        st.button(f"Copy {output_lang} Summary to Clipboard", on_click=lambda: st.session_state.update({'clipboard': translated_summary}), help=f"Copy the {output_lang} summary.")
            # Clean up temp files
            if tmpfile_path and os.path.exists(tmpfile_path):
                os.remove(tmpfile_path)
            if wav_path and wav_path != tmpfile_path and os.path.exists(wav_path):
                os.remove(wav_path)
    st.markdown('</div>', unsafe_allow_html=True) 