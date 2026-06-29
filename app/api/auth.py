from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)
from app.models.user import User
from app.models.schemas import (
    UserRegisterRequest,
    UserLoginRequest,
    UserResponse,
    RegisterResponse,
    LoginResponse,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])


# ============ REGISTER ENDPOINT ============

@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    responses={
        201: {"description": "User successfully registered"},
        400: {"description": "Email already registered"},
    }
)
def register(
    user_data: UserRegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new user.

    Flow:
    1. Check email not already taken
    2. Hash password
    3. Save user to database
    4. Generate JWT token
    5. Return user data + token

    Raises:
        HTTPException: If email already registered
    """

    # Step 1: Check if email already exists
    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Step 2: Hash password
    password_hash = hash_password(user_data.password)

    # Step 3: Create new user object
    new_user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        password_hash=password_hash,
        phone=user_data.phone,
    )

    # Step 4: Save to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Step 5: Generate JWT token
    access_token = create_access_token(
        data={"sub": new_user.user_id}
    )

    # Step 6: Return response
    return RegisterResponse(
        user=UserResponse.from_orm(new_user),
        token=access_token,
        token_type="bearer"
    )


# ============ LOGIN ENDPOINT ============

@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Login user",
    responses={
        200: {"description": "Successfully logged in"},
        401: {"description": "Invalid credentials"},
    }
)
def login(
    credentials: UserLoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login user with email and password.

    Flow:
    1. Find user by email
    2. Verify password matches hash
    3. Generate JWT token
    4. Return user data + token

    Raises:
        HTTPException: If email not found or password wrong
    """

    # Step 1: Find user by email
    user = db.query(User).filter(
        User.email == credentials.email
    ).first()

    # Step 2: Check if user exists and password matches
    if not user or not verify_password(
        credentials.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Step 3: Generate JWT token
    access_token = create_access_token(
        data={"sub": user.user_id}
    )

    # Step 4: Return response
    return LoginResponse(
        user=UserResponse.from_orm(user),
        token=access_token,
        token_type="bearer"
    )


# ============ GET CURRENT USER ENDPOINT ============

@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current logged-in user",
)
def get_current_user(
    token: str = Header(None),
    db: Session = Depends(get_db)
):
    """
    Get logged-in user's data from JWT token.

    Raises:
        HTTPException: If token invalid or user not found
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Remove "Bearer " prefix if present
    if token.startswith("Bearer "):
        token = token[7:]

    # Decode and verify token
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get user from database
    user = db.query(User).filter(
        User.user_id == payload["user_id"]
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserResponse.from_orm(user)
