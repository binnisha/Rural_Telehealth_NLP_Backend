import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from dotenv import load_dotenv

load_dotenv()

# AES-256 key — 32 bytes, stored in .env
AES_KEY = os.getenv("AES_KEY", "medibridge-aes-key-32-bytes-long!")[:32].encode()

def encrypt_text(plain_text: str) -> str:
    """Encrypt medical text using AES-256"""
    if not plain_text:
        return plain_text
    
    # Generate random 16-byte IV
    iv = os.urandom(16)
    
    cipher = Cipher(
        algorithms.AES(AES_KEY),
        modes.CFB(iv),
        backend=default_backend()
    )
    
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(plain_text.encode()) + encryptor.finalize()
    
    # Combine IV + encrypted, encode as base64 string
    combined = base64.b64encode(iv + encrypted).decode()
    return combined

def decrypt_text(encrypted_text: str) -> str:
    """Decrypt AES-256 encrypted medical text"""
    if not encrypted_text:
        return encrypted_text
    
    try:
        combined = base64.b64decode(encrypted_text.encode())
        iv = combined[:16]
        encrypted = combined[16:]
        
        cipher = Cipher(
            algorithms.AES(AES_KEY),
            modes.CFB(iv),
            backend=default_backend()
        )
        
        decryptor = cipher.decryptor()
        plain_text = decryptor.update(encrypted) + decryptor.finalize()
        return plain_text.decode()
    except Exception:
        return "[Decryption failed]"