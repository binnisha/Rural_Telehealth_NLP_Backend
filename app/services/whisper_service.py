import os

WHISPER_AVAILABLE = False
model = None

try:
    import whisper
    WHISPER_MODEL = os.environ.get("WHISPER_MODEL", "medium")
    model = whisper.load_model(WHISPER_MODEL)
    WHISPER_AVAILABLE = True
    print("✅ Whisper model loaded")
except Exception as e:
    print(f"⚠️ Whisper not available: {e}")

def transcribe_audio(file_path: str) -> dict:
    if not WHISPER_AVAILABLE:
        return {
            "success": False,
            "error": "Whisper not available on this server",
            "transcribed_text": None,
            "detected_language": None
        }
    try:
        result = model.transcribe(file_path)
        return {
            "success": True,
            "transcribed_text": result["text"],
            "detected_language": result["language"],
            "file": os.path.basename(file_path)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "transcribed_text": None,
            "detected_language": None
        }