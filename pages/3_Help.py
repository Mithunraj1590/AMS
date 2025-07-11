import streamlit as st

st.title("Help & FAQ")

st.markdown("""
**Having trouble? Here are some tips:**

- **App is slow or stuck?**
  - Large audio files may take several minutes to process, especially on CPU.
  - Try shorter audio or use a machine with a GPU for faster results.

- **Transcription/Summary/Translation failed?**
  - Make sure your audio is clear and in a supported format (.mp3, .wav, .m4a).
  - Check that you have enough RAM and disk space.
  - If you see a specific error, try searching the error message online or in the [GitHub issues](https://github.com/openai/whisper/issues).

- **How do I add more languages?**
  - You can extend the `LANG_CODES` dictionary in `services/translation.py` and use a compatible model from HuggingFace.

- **Where is my data stored?**
  - All processing is local; your files and transcripts are not uploaded anywhere.

---

**Contact:**
- For feedback or help, email: [your@email.com]
- Or open an issue on the project GitHub.
""") 