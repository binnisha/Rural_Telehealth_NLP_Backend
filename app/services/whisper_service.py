try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

model = None

def load_model():
    global model
    if WHISPER_AVAILABLE and model is None:
        model = whisper.load_model("medium")
    return model

def transcribe_audio(file_path: str):
    if not WHISPER_AVAILABLE:
        return {
            "success": False,
            "error": "Whisper not available on this server. Use local deployment for transcription."
        }
    try:
        m = load_model()
        result = m.transcribe(file_path)
        return {
            "success": True,
            "transcribed_text": result["text"],
            "detected_language": result["language"]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}