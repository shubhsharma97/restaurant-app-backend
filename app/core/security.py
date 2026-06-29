from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import jwt

# Configure password hashing
# bcrypt is the industry standard (slow = secure against attacks)
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# JWT configuration
SECRET_KEY = "your-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # Token valid for 24 hours

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
    
    # Encode the token
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
        return None
    except jwt.InvalidTokenError:
        # Token is invalid/forged
        return None