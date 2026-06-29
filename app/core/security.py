import os
from dotenv import load_dotenv

# Load environment variables from .env file (for local dev)
load_dotenv()

# --- SECRET KEY ---
SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY not set in environment variables!")

if SECRET_KEY == "your-secret-key-change-this-in-production":
    raise ValueError(
        "You MUST change SECRET_KEY! "
        "Run: python3 -c 'import secrets; print(secrets.token_urlsafe(32))'"
    )

# --- JWT SETTINGS ---
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

# --- DATABASE ---
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set in environment variables!")

# --- CLOUDINARY ---
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

# --- FRONTEND ---
FRONTEND_URL = os.getenv("FRONTEND_URL", "*")
