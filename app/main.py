from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.utils.database import create_tables
import os

app = FastAPI(
    title="MediBridge API",
    description="Multilingual speech-to-text translation system for rural healthcare",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    create_tables()
    print("✅ Database tables created successfully")

# Always include these routes
from app.routes import translate, auth
app.include_router(translate.router, tags=["Translation"])
app.include_router(auth.router, tags=["Authentication"])

# Only include Whisper routes if available
try:
    from app.routes import transcribe, pipeline
    app.include_router(transcribe.router, tags=["Transcription"])
    app.include_router(pipeline.router, tags=["Pipeline"])
    print("✅ Whisper pipeline loaded")
except Exception as e:
    print(f"⚠️ Whisper not available: {e}")

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