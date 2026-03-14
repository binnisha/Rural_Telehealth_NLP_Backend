from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Try Railway environment first, then fall back to .env
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    try:
        from dotenv import load_dotenv
        load_dotenv()
        DATABASE_URL = os.environ.get("DATABASE_URL")
    except:
        pass

# Fix Railway postgres:// to postgresql://
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

print(f"Database URL prefix: {DATABASE_URL[:20] if DATABASE_URL else 'NOT FOUND'}")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    from app.models.models import Base
    Base.metadata.create_all(bind=engine)
    
