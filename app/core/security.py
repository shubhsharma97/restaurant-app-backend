from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import jwt
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure password hashing
# bcrypt is the industry standard (slow = secure against attacks)
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# ============ JWT CONFIGURATION (FROM ENVIRONMENT) ============

# Get SECRET_KEY from environment variables
SECRET_KEY = os.getenv("SECRET_KEY")

# Validate that SECRET_KEY is set
if not SECRET_KEY:
    raise ValueError(
        "❌ CRITICAL ERROR: SECRET_KEY not set in environment variables!\n"
        "Please add SECRET_KEY to your .env file or Replit secrets.\n"
        "Generate one with: python3 -c 'import secrets; print(secrets.token_urlsafe(32))'"
    )

# Prevent using the default placeholder
if SECRET_KEY == "your-secret-key-change-this-in-production":
    raise ValueError(
        "❌ ERROR: You're using the default SECRET_KEY!\n"
        "This is a SECURITY RISK! Change it immediately!\n"
        "Generate a new one with: python3 -c 'import secrets; print(secrets.token_urlsafe(32))'"
    )

# Other JWT settings
ALGORITHM = os.getenv("ALGORITHM", "HS256")  # Default to HS256 if not set
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440))  # 24 hours default

# ============ PASSWORD HASHING FUNCTIONS ============

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    Why bcrypt?
    - Deliberately SLOW (takes 0.3 seconds to hash)
    - Slows down brute force attacks
    - Industry standard

    Args:
        password: Plain text password from user

    Returns:
        Hashed password (looks like gibberish)
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.

    Why separate function?
    - Hashing is one-way (can't reverse hash)
    - We hash the input password and compare hashes

    Args:
        plain_password: Password user entered in login form
        hashed_password: Password stored in database

    Returns:
        True if passwords match, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


# ============ JWT TOKEN FUNCTIONS ============

def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT token.

    What is JWT?
    - JSON Web Token
    - Contains encoded data (user_id, email, etc.)
    - Can't be forged without secret key
    - Expires after time limit

    Args:
        data: What to encode (usually user_id)
        expires_delta: When should token expire?

    Returns:
        JWT token string

    Example:
        token = create_access_token({"sub": "user123"})
        # Returns: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    """
    to_encode = data.copy()

    # Set expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    # Encode the token using SECRET_KEY from environment
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and verify a JWT token.

    Why decode?
    - Verify token hasn't been tampered with
    - Extract user info from token
    - Check if token has expired

    Args:
        token: JWT token string from client

    Returns:
        Decoded data if valid, None if invalid/expired
    """
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id: str = payload.get("sub")

        if user_id is None:
            return None

        return {"user_id": user_id}

    except jwt.ExpiredSignatureError:
        # Token has expired
        print("⚠️ Token has expired")
        return None
    except jwt.InvalidTokenError:
        # Token is invalid/forged
        print("⚠️ Token is invalid or was tampered with")
        return None


# ============ PROTECTED ROUTE DEPENDENCY ============

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials

# This tells FastAPI to expect "Authorization: Bearer <token>" header
security = HTTPBearer()


async def get_current_user_id(credentials: HTTPAuthCredentials = Depends(security)) -> str:
    """
    Extract and verify JWT token from request.

    This is a dependency that:
    1. Extracts token from "Authorization: Bearer <token>" header
    2. Verifies token is valid
    3. Returns user_id

    Usage in endpoint:
        @app.get("/api/protected")
        def protected_route(user_id: str = Depends(get_current_user_id)):
            return {"message": f"Hello {user_id}"}

    If token missing/invalid → FastAPI returns 401 error automatically

    Args:
        credentials: HTTP credentials from header

    Returns:
        user_id from token

    Raises:
        HTTPException: If token invalid/missing
    """
    token = credentials.credentials

    # Decode and verify token
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload["user_id"]
