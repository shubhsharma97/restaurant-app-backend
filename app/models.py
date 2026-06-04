from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class Location(BaseModel):
    address: str
    city: str
    state: str
    zip_code: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class RestaurantBase(BaseModel):
    name: str
    cuisine: str
    description: Optional[str] = None
    price_range: str = Field(..., pattern="^\\$+$", description="$ to $$$$")
    phone: Optional[str] = None
    website: Optional[str] = None
    location: Location


class RestaurantCreate(RestaurantBase):
    pass


class Restaurant(RestaurantBase):
    id: int
    average_rating: float = 0.0
    review_count: int = 0
    created_at: datetime

    class Config:
        from_attributes = True


class ReviewBase(BaseModel):
    restaurant_id: int
    rating: float = Field(..., ge=1, le=5)
    title: Optional[str] = None
    body: Optional[str] = None


class ReviewCreate(ReviewBase):
    user_id: int


class Review(ReviewBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
