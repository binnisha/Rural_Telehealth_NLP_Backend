import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# ==================== HEALTH TESTS ====================

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

# ==================== AUTH TESTS ====================

def test_register_patient():
    response = client.post("/register/patient", json={
        "full_name": "Test Patient",
        "age": 25,
        "gender": "Male",
        "location": "Delhi",
        "preferred_language": "hi",
        "phone_number": "9999999999",
        "password": "test1234"
    })
    # 200 = registered, 400 = already exists (both are fine)
    assert response.status_code in [200, 400]

def test_register_doctor():
    response = client.post("/register/doctor", json={
        "full_name": "Dr. Test Doctor",
        "specialization": "General Physician",
        "email": "testdoctor@medibridge.com",
        "phone_number": "8888888888",
        "password": "test1234"
    })
    assert response.status_code in [200, 400]

def test_login_invalid_credentials():
    response = client.post("/login", json={
        "email": "wrong@email.com",
        "password": "wrongpassword",
        "role": "doctor"
    })
    assert response.status_code in [401, 403]

def test_login_valid_doctor():
    response = client.post("/login", json={
        "email": "rahul.sharma@medibridge.com",
        "password": "doctor123",
        "role": "doctor"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_protected_endpoint_without_token():
    """Pipeline should reject requests without JWT token"""
    response = client.post("/transcribe-and-translate")
    assert response.status_code == 401

# ==================== ENCRYPTION TESTS ====================

def test_encryption():
    from app.utils.encryption import encrypt_text, decrypt_text
    original = "मेरा नाम विनीशा है"
    encrypted = encrypt_text(original)
    decrypted = decrypt_text(encrypted)
    assert encrypted != original
    assert decrypted == original

def test_encryption_empty():
    from app.utils.encryption import encrypt_text, decrypt_text
    assert encrypt_text("") == ""
    assert decrypt_text("") == ""