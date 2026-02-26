from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
from app.services.whisper_service import transcribe_audio

router = APIRouter()

# Temporary folder to store uploaded audio files
UPLOAD_DIR = "temp_audio"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    """
    Upload an audio file and get back transcribed text
    Supports Hindi, Tamil, Telugu, Bengali and all Indian languages
    """
    
    # Check file type
    allowed_types = ["audio/mpeg", "audio/wav", "audio/mp4", "audio/m4a", "audio/ogg", "audio/webm", "video/mpeg", "video/mp4", "application/octet-stream"]
    
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: wav, mp3, m4a, ogg, webm"
        )
    
    # Save uploaded file temporarily
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Transcribe using Whisper
    result = transcribe_audio(file_path)
    
    # Clean up temp file after transcription
    os.remove(file_path)
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return {
        "success": True,
        "transcribed_text": result["transcribed_text"],
        "detected_language": result["detected_language"],
        "filename": file.filename
    }