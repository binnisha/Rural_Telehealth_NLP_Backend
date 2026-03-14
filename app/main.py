from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
    try:
        from app.utils.database import create_tables
        create_tables()
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"⚠️ Database setup error: {e}")

# Core routes - always load
try:
    from app.routes import translate
    app.include_router(translate.router, tags=["Translation"])
    print("✅ Translation routes loaded")
except Exception as e:
    print(f"⚠️ Translation routes error: {e}")

try:
    from app.routes import auth
    app.include_router(auth.router, tags=["Authentication"])
    print("✅ Auth routes loaded")
except Exception as e:
    print(f"⚠️ Auth routes error: {e}")

# Whisper routes - only if available
try:
    from app.routes import transcribe
    app.include_router(transcribe.router, tags=["Transcription"])
    print("✅ Transcription routes loaded")
except Exception as e:
    print(f"⚠️ Transcription routes not available: {e}")

try:
    from app.routes import pipeline
    app.include_router(pipeline.router, tags=["Pipeline"])
    print("✅ Pipeline routes loaded")
except Exception as e:
    print(f"⚠️ Pipeline routes not available: {e}")

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