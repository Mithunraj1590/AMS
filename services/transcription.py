import whisper
import tempfile
from pydub import AudioSegment
import os

def get_whisper_model():
    if not hasattr(get_whisper_model, "_model"):
        get_whisper_model._model = whisper.load_model("base")
    return get_whisper_model._model

def transcribe_audio(uploaded_file):
    tmpfile_path = None
    wav_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
            tmpfile.write(uploaded_file.read())
            tmpfile_path = tmpfile.name
        if not tmpfile_path.endswith(".wav"):
            audio = AudioSegment.from_file(tmpfile_path)
            wav_path = tmpfile_path.replace(".mp3", ".wav")
            audio.export(wav_path, format="wav")
        else:
            wav_path = tmpfile_path
        model = get_whisper_model()
        result = model.transcribe(wav_path, language=None)
        transcript = result["text"]
        return transcript, tmpfile_path, wav_path, None
    except Exception as e:
        if tmpfile_path and os.path.exists(tmpfile_path):
            os.remove(tmpfile_path)
        if wav_path and wav_path != tmpfile_path and os.path.exists(wav_path):
            os.remove(wav_path)
        return None, None, None, str(e) 