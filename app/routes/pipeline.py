from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
from app.services.whisper_service import transcribe_audio
from app.services.translation_service import translate_to_english

router = APIRouter()

UPLOAD_DIR = "temp_audio"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/transcribe-and-translate")
async def transcribe_and_translate(file: UploadFile = File(...)):
    """
    THE MONEY ENDPOINT
    Send audio in any Indian language
    Get back English translation directly
    One API call. That's it.
    """

    # Step 1 - Accept audio file
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

    # Step 2 - Save audio temporarily
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Step 3 - Whisper transcribes audio
    transcription = transcribe_audio(file_path)

    # Clean up temp file
    os.remove(file_path)

    if not transcription["success"]:
        raise HTTPException(
            status_code=500,
            detail=f"Transcription failed: {transcription['error']}"
        )

    # Step 4 - Translate transcribed text to English
    translation = translate_to_english(
        transcription["transcribed_text"],
        transcription["detected_language"]
    )

    if not translation["success"]:
        raise HTTPException(
            status_code=500,
            detail=f"Translation failed: {translation['error']}"
        )

    # Step 5 - Return complete result
    return {
        "success": True,
        "detected_language": transcription["detected_language"],
        "original_text": transcription["transcribed_text"],
        "english_translation": translation["translated_text"],
        "filename": file.filename,
        "message": "Audio successfully transcribed and translated"
    }