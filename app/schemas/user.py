from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# ============ REQUEST SCHEMAS ============
# What the frontend SENDS to us

class UserRegisterRequest(BaseModel):
    """
    What frontend sends when signing up.
    
    Pydantic validates:
    - email is valid email format
    - password is at least 8 characters
    """
    email: EmailStr  # Validates email format automatically
    full_name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8, max_length=100)
    phone: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "john@example.com",
                "full_name": "John Doe",
                "password": "securePassword123",
                "phone": "+1-555-0123"
            }
        }

class UserLoginRequest(BaseModel):
    """
    What frontend sends when logging in.
    """
    email: EmailStr
    password: str = Field(..., min_length=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "john@example.com",
                "password": "securePassword123"
            }
        }

# ============ RESPONSE SCHEMAS ============
# What we SEND back to frontend

class UserResponse(BaseModel):
    """
    User data we send back (NEVER includes password!).
    
    Why separate schemas?
    - Registration returns user data + token
    - Login returns user data + token
    - GET /me returns just user data
    """
    user_id: str
    email: str
    full_name: str
    phone: Optional[str]
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True  # Convert SQLAlchemy model to dict

class RegisterResponse(BaseModel):
    """
    Response when user successfully registers.
    """
    user: UserResponse
    token: str
    token_type: str = "bearer"  # HTTP authentication type
    
    class Config:
        json_schema_extra = {
            "example": {
                "user": {
                    "user_id": "123-456-789",
                    "email": "john@example.com",
                    "full_name": "John Doe",
                    "phone": "+1-555-0123",
                    "created_at": "2026-06-28T10:00:00",
                    "is_active": True
                },
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }

class LoginResponse(BaseModel):
    """
    Response when user successfully logs in.
    """
    user: UserResponse
    token: str
    token_type: str = "bearer"

class TokenResponse(BaseModel):
    """
    Just the token (for refresh operations).
    """
    access_token: str
    token_type: str = "bearer"