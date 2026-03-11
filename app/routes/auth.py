from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.models.models import User
from app.utils.auth import hash_password, verify_password, create_access_token
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

# --- Schemas ---

class UserRegister(BaseModel):
    full_name: str
    email: str
    password: str
    role: Optional[str] = "patient"  # "patient" or "doctor"

class UserLogin(BaseModel):
    email: str
    password: str

# --- Routes ---

@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        hashed_password=hash_password(user.password),
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "success": True,
        "message": "User registered successfully",
        "user_id": new_user.id,
        "email": new_user.email,
        "role": new_user.role
    }

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    # Find user by email
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Verify password
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Create JWT token
    token = create_access_token(data={"sub": db_user.email, "role": db_user.role})
    return {
        "success": True,
        "access_token": token,
        "token_type": "bearer",
        "user_name": db_user.full_name,
        "role": db_user.role
    }

@router.get("/me")
def get_current_user(token: str, db: Session = Depends(get_db)):
    from app.utils.auth import verify_token
    email = verify_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "user_id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "role": user.role
    }