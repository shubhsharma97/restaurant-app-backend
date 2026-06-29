from sqlalchemy import Column, String, DateTime, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    # Primary key - unique identifier for each user
    user_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Email - must be unique (no two users with same email)
    email = Column(String, unique=True, nullable=False, index=True)
    
    # Full name
    full_name = Column(String, nullable=False)
    
    # Password - NEVER store plaintext! Always hashed
    password_hash = Column(String, nullable=False)
    
    # Phone number (optional)
    phone = Column(String, nullable=True)
    
    # When account was created
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # When account was last updated
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Is account active?
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<User {self.email}>"