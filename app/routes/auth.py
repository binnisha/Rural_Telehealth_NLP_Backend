from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.utils.database import get_db
from app.utils.auth import hash_password, verify_password, create_access_token
from app.models.models import Patient, Doctor

router = APIRouter()

class PatientRegister(BaseModel):
    full_name: str
    age: int
    gender: str
    location: str
    preferred_language: str = "hi"
    phone_number: str
    password: str

class DoctorRegister(BaseModel):
    full_name: str
    specialization: str
    email: str
    phone_number: str
    password: str

class LoginRequest(BaseModel):
    phone_number: str = None
    email: str = None
    password: str
    role: str

@router.post("/register/patient")
def register_patient(data: PatientRegister, db: Session = Depends(get_db)):
    """Register a new patient — open to everyone"""

    if len(data.password) > 72:
        raise HTTPException(
            status_code=400,
            detail="Password cannot be longer than 72 characters"
        )

    existing = db.query(Patient).filter(
        Patient.phone_number == data.phone_number
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Patient with this phone number already exists"
        )

    patient = Patient(
        full_name=data.full_name,
        age=data.age,
        gender=data.gender,
        location=data.location,
        preferred_language=data.preferred_language,
        phone_number=data.phone_number,
        password=hash_password(data.password)
    )

    db.add(patient)
    db.commit()
    db.refresh(patient)

    return {
        "success": True,
        "message": f"Patient {data.full_name} registered successfully",
        "patient_id": patient.id
    }

@router.post("/register/doctor")
def register_doctor(data: DoctorRegister, db: Session = Depends(get_db)):
    """Register a new doctor — pending admin verification"""

    if len(data.password) > 72:
        raise HTTPException(
            status_code=400,
            detail="Password cannot be longer than 72 characters"
        )

    existing = db.query(Doctor).filter(
        Doctor.email == data.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Doctor with this email already exists"
        )

    doctor = Doctor(
        full_name=data.full_name,
        specialization=data.specialization,
        email=data.email,
        phone_number=data.phone_number,
        password=hash_password(data.password),
        is_verified=False
    )

    db.add(doctor)
    db.commit()
    db.refresh(doctor)

    return {
        "success": True,
        "message": f"Doctor {data.full_name} registered successfully. Account pending verification.",
        "doctor_id": doctor.id,
        "is_verified": False,
        "note": "Your account will be activated after admin verification"
    }

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """Login for patients and doctors"""

    if data.role == "patient":
        user = db.query(Patient).filter(
            Patient.phone_number == data.phone_number
        ).first()

    elif data.role == "doctor":
        user = db.query(Doctor).filter(
            Doctor.email == data.email
        ).first()

        if user and not user.is_verified:
            raise HTTPException(
                status_code=403,
                detail="Your account is pending admin verification. Please wait for approval."
            )
    else:
        raise HTTPException(
            status_code=400,
            detail="Role must be 'patient' or 'doctor'"
        )

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token({
        "sub": str(user.id),
        "role": data.role,
        "name": user.full_name
    })

    return {
        "success": True,
        "access_token": token,
        "token_type": "bearer",
        "role": data.role,
        "name": user.full_name
    }

@router.patch("/verify/doctor/{doctor_id}")
def verify_doctor(doctor_id: int, db: Session = Depends(get_db)):
    """Admin endpoint to verify a doctor"""

    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    doctor.is_verified = True
    db.commit()

    return {
        "success": True,
        "message": f"Doctor {doctor.full_name} verified and can now login",
        "doctor_id": doctor_id
    }