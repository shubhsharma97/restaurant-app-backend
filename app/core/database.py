from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.models.user import Base
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set in environment variables!")

# Create database engine
# echo=True = log all SQL queries (useful for debugging)
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True to see SQL queries
    pool_pre_ping=True,  # Test connection before using (prevents stale connections)
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    """
    Dependency function for FastAPI.
    
    Provides database session to endpoints.
    Ensures session is closed after endpoint finishes.
    
    Usage in endpoint:
        @app.post("/api/auth/register")
        def register(data: dict, db: Session = Depends(get_db)):
            # db is automatically provided!
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Create all database tables.
    
    Run once to initialize database schema.
    """
    Base.metadata.create_all(bind=engine)