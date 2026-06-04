from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.models import Restaurant, RestaurantCreate
from app import database

router = APIRouter()


@router.get("/", response_model=List[dict])
def list_restaurants(cuisine: Optional[str] = None, city: Optional[str] = None):
    restaurants = database.get_all_restaurants()
    if cuisine:
        restaurants = [r for r in restaurants if r["cuisine"].lower() == cuisine.lower()]
    if city:
        restaurants = [r for r in restaurants if r["location"]["city"].lower() == city.lower()]
    return restaurants


@router.get("/{restaurant_id}")
def get_restaurant(restaurant_id: int):
    restaurant = database.get_restaurant(restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant


@router.post("/", status_code=201)
def create_restaurant(data: RestaurantCreate):
    return database.create_restaurant(data.model_dump())


@router.delete("/{restaurant_id}", status_code=204)
def delete_restaurant(restaurant_id: int):
    if not database.delete_restaurant(restaurant_id):
        raise HTTPException(status_code=404, detail="Restaurant not found")
