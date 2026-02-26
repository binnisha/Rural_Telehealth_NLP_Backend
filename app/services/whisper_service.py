import whisper
import os

# Load the Whisper model
# "base" is good for starting - fast and decent accuracy
# Later we can upgrade to "medium" or "large" for better accuracy
model = whisper.load_model("medium")

def transcribe_audio(file_path: str) -> dict:
    """
    Takes an audio file path and returns transcribed text
    with detected language information
    """
    try:
        # Transcribe the audio
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