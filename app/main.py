from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import transcribe, translate, pipeline, patient, auth
from app.utils.database import create_tables

app = FastAPI(
    title="MediBridge API",
    description="Multilingual speech-to-text translation system for rural healthcare",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
@app.on_event("startup")
def startup():
    create_tables()
    print("✅ Database tables created successfully")

app.include_router(transcribe.router, tags=["Transcription"])
app.include_router(translate.router, tags=["Translation"])
app.include_router(pipeline.router, tags=["Pipeline"])
app.include_router(patient.router, tags=["Patients"]) 
app.include_router(auth.router, tags=["Authentication"])


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