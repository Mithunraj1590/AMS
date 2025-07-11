import streamlit as st

st.title("About AI Meeting Summarizer")

st.markdown("""
This project is an open-source AI-powered tool to help you transcribe, summarize, and translate your meeting audio into multiple Indian languages.

**Features:**
- Free and privacy-friendly: all processing is local on your machine
- Supports English, Hindi, Tamil, Telugu, Malayalam, Kannada
- Modern, easy-to-use interface

**Powered by:**
- [OpenAI Whisper](https://github.com/openai/whisper) for transcription
- [facebook/bart-large-cnn](https://huggingface.co/facebook/bart-large-cnn) for summarization
- [facebook/nllb-200-distilled-600M](https://huggingface.co/facebook/nllb-200-distilled-600M) for translation

**Made with [Streamlit](https://streamlit.io/)**

---

*Created by Mithun raj. Contributions welcome!*
""") 