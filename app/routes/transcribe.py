from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
from app.services.whisper_service import transcribe_audio, WHISPER_AVAILABLE

router = APIRouter()

UPLOAD_DIR = "temp_audio"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    if not WHISPER_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Whisper not available on this server. Use local deployment."
        )

    allowed_types = [
        "audio/mpeg", "audio/wav", "audio/mp4",
        "audio/m4a", "audio/ogg", "audio/webm",
        "video/mpeg", "video/mp4", "application/octet-stream"
    ]

    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = transcribe_audio(file_path)
    os.remove(file_path)

    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["error"])

    return result