from fastapi import FastAPI

app = FastAPI(
    title="MediBridge API",
    description="Multilingual speech-to-text translation system for rural healthcare",
    version="1.0.0"
)

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