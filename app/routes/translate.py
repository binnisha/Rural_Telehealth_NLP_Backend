from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.translation_service import translate_to_english

router = APIRouter()

class TranslationRequest(BaseModel):
    text: str
    source_language: str = "hi"  # Default Hindi

@router.post("/translate")
def translate(request: TranslationRequest):
    """
    Translate text from any Indian language to English
    Supported languages: hi, bn, ta, te, mr, gu, kn, ml, pa, or, mai
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    result = translate_to_english(request.text, request.source_language)

    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["error"])

    return result