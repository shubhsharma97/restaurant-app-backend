from fastapi import APIRouter, HTTPException
from app.models import UserCreate
from app import database

router = APIRouter()


@router.get("/")
def list_users():
    return database.get_all_users()


@router.get("/{user_id}")
def get_user(user_id: int):
    user = database.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", status_code=201)
def create_user(data: UserCreate):
    return database.create_user(data.model_dump())
