from fastapi import APIRouter, HTTPException
from app.models import ReviewCreate
from app import database

router = APIRouter()


@router.get("/")
def list_reviews():
    return database.get_all_reviews()


@router.get("/restaurant/{restaurant_id}")
def get_reviews_for_restaurant(restaurant_id: int):
    restaurant = database.get_restaurant(restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return database.get_reviews_for_restaurant(restaurant_id)


@router.get("/{review_id}")
def get_review(review_id: int):
    review = database.get_review(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@router.post("/", status_code=201)
def create_review(data: ReviewCreate):
    restaurant = database.get_restaurant(data.restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    user = database.get_user(data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return database.create_review(data.model_dump())
