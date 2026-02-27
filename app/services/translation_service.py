from deep_translator import GoogleTranslator

LANGUAGE_NAMES = {
    "hi": "Hindi",
    "bn": "Bengali", 
    "ta": "Tamil",
    "te": "Telugu",
    "mr": "Marathi",
    "gu": "Gujarati",
    "kn": "Kannada",
    "ml": "Malayalam",
    "pa": "Punjabi",
    "or": "Odia",
    "mai": "Maithili"
}

def translate_to_english(text: str, source_language: str) -> dict:
    """
    Translates text from any Indian language to English
    """
    try:
        translated_text = GoogleTranslator(
            source=source_language,
            target="en"
        ).translate(text)

        return {
            "success": True,
            "original_text": text,
            "translated_text": translated_text,
            "source_language": LANGUAGE_NAMES.get(source_language, source_language),
            "target_language": "English"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "original_text": text,
            "translated_text": None
        }