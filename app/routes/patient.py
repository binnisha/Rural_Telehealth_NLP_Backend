from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.models.models import Patient, Consultation
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

# --- Schemas ---

class PatientCreate(BaseModel):
    full_name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    location: Optional[str] = None
    preferred_language: Optional[str] = "hi"
    phone_number: Optional[str] = None

class ConsultationSave(BaseModel):
    patient_id: int
    original_text: str
    translated_text: str
    detected_language: str
    audio_filename: str
    symptoms: Optional[str] = None

# --- Routes ---

@router.post("/add-patient")
def add_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    new_patient = Patient(
        full_name=patient.full_name,
        age=patient.age,
        gender=patient.gender,
        location=patient.location,
        preferred_language=patient.preferred_language,
        phone_number=patient.phone_number
    )
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return {
        "success": True,
        "message": "Patient added successfully",
        "patient_id": new_patient.id,
        "patient_name": new_patient.full_name
    }

@router.post("/save-consultation")
def save_consultation(data: ConsultationSave, db: Session = Depends(get_db)):
    # Check patient exists
    patient = db.query(Patient).filter(Patient.id == data.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    new_consultation = Consultation(
        patient_id=data.patient_id,
        original_text=data.original_text,
        translated_text=data.translated_text,
        detected_language=data.detected_language,
        audio_filename=data.audio_filename,
        symptoms=data.symptoms
    )
    db.add(new_consultation)
    db.commit()
    db.refresh(new_consultation)
    return {
        "success": True,
        "message": "Consultation saved successfully",
        "consultation_id": new_consultation.id,
        "patient_name": patient.full_name,
        "translated_text": new_consultation.translated_text
    }

@router.get("/patient/{patient_id}/consultations")
def get_patient_consultations(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return {
        "patient": patient.full_name,
        "total_consultations": len(patient.consultations),
        "consultations": [
            {
                "id": c.id,
                "original_text": c.original_text,
                "translated_text": c.translated_text,
                "detected_language": c.detected_language,
                "date": c.created_at
            } for c in patient.consultations
        ]
    }