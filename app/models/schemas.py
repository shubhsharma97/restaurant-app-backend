from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# ============ REQUEST SCHEMAS ============

class UserRegisterRequest(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    phone: Optional[str] = None


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


# ============ RESPONSE SCHEMAS ============

class UserResponse(BaseModel):
    user_id: str
    email: str
    full_name: str
    phone: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class RegisterResponse(BaseModel):
    user: UserResponse
    token: str
    token_type: str = "bearer"


class LoginResponse(BaseModel):
    user: UserResponse
    token: str
    token_type: str = "bearer"
