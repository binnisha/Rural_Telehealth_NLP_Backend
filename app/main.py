from fastapi import FastAPI
from app.routes import transcribe, translate, pipeline

app = FastAPI(
    title="MediBridge API",
    description="Multilingual speech-to-text translation system for rural healthcare",
    version="1.0.0"
)

app.include_router(transcribe.router, tags=["Transcription"])
app.include_router(translate.router, tags=["Translation"])
app.include_router(pipeline.router, tags=["Pipeline"])

@app.get("/")
def home():
    return {
        "message": "MediBridge Backend is running!",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "MediBridge API"
    }