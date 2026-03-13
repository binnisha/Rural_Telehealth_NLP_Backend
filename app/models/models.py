from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    age = Column(Integer)
    gender = Column(String(10))
    location = Column(String(200))
    preferred_language = Column(String(10), default="hi")
    phone_number = Column(String(15))
    is_verified = Column(Boolean, default=False)
    password = Column(String(200), nullable=False) 
    created_at = Column(DateTime, default=datetime.utcnow)
    
    consultations = relationship("Consultation", back_populates="patient")

class Doctor(Base):
    __tablename__ = "doctors"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    specialization = Column(String(100))
    email = Column(String(100), unique=True)
    phone_number = Column(String(15))
    is_verified = Column(Boolean, default=False)
    password = Column(String(200), nullable=False) 
    created_at = Column(DateTime, default=datetime.utcnow)
    
    consultations = relationship("Consultation", back_populates="doctor")

class Consultation(Base):
    __tablename__ = "consultations"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    
    original_text = Column(Text)
    translated_text = Column(Text)
    detected_language = Column(String(10))
    audio_filename = Column(String(200))
    
    symptoms = Column(Text)
    diagnosis = Column(Text)
    prescription = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="consultations")
    doctor = relationship("Doctor", back_populates="consultations")
    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(10), default="patient")
    is_active = Column(String(10), default="true")
    created_at = Column(DateTime, default=datetime.utcnow)