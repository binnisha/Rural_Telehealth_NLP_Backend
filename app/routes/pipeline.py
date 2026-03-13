from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
import shutil
import os
from app.services.whisper_service import transcribe_audio
from app.services.translation_service import translate_to_english
from app.utils.auth import get_current_user
from app.utils.encryption import encrypt_text

router = APIRouter()

UPLOAD_DIR = "temp_audio"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/transcribe-and-translate")
async def transcribe_and_translate(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """
    THE MONEY ENDPOINT — JWT Protected
    Send audio in any Indian language
    Get back English translation directly
    One API call. That's it.
    """

    allowed_types = [
        "audio/mpeg", "audio/wav", "audio/mp4",
        "audio/m4a", "audio/ogg", "audio/webm",
        "video/mpeg", "video/mp4", "application/octet-stream"
    ]

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Allowed: wav, mp3, m4a, ogg, webm"
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    transcription = transcribe_audio(file_path)
    os.remove(file_path)

    if not transcription["success"]:
        raise HTTPException(
            status_code=500,
            detail=f"Transcription failed: {transcription['error']}"
        )

    translation = translate_to_english(
        transcription["transcribed_text"],
        transcription["detected_language"]
    )

    if not translation["success"]:
        raise HTTPException(
            status_code=500,
            detail=f"Translation failed: {translation['error']}"
        )

    # Encrypt medical data before returning
    encrypted_original = encrypt_text(transcription["transcribed_text"])
    encrypted_translation = encrypt_text(translation["translated_text"])

    return {
        "success": True,
        "detected_language": transcription["detected_language"],
        "original_text": transcription["transcribed_text"],
        "english_translation": translation["translated_text"],
        "encrypted_original": encrypted_original,
        "encrypted_translation": encrypted_translation,
        "requested_by": current_user.get("name"),
        "role": current_user.get("role"),
        "filename": file.filename,
        "message": "Audio successfully transcribed and translated"
    }