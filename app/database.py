from datetime import datetime
from typing import Dict, List, Optional

_restaurants: Dict[int, dict] = {
    1: {
        "id": 1,
        "name": "The Golden Fork",
        "cuisine": "American",
        "description": "Classic American comfort food with a modern twist.",
        "price_range": "$$",
        "phone": "555-100-0001",
        "website": "https://goldenfork.example.com",
        "location": {
            "address": "123 Main St",
            "city": "Springfield",
            "state": "IL",
            "zip_code": "62701",
            "latitude": 39.7817,
            "longitude": -89.6501,
        },
        "average_rating": 4.5,
        "review_count": 2,
        "created_at": datetime(2024, 1, 15),
    },
    2: {
        "id": 2,
        "name": "Sakura Sushi",
        "cuisine": "Japanese",
        "description": "Authentic Japanese sushi and ramen in a cozy setting.",
        "price_range": "$$$",
        "phone": "555-100-0002",
        "website": "https://sakurasushi.example.com",
        "location": {
            "address": "456 Oak Ave",
            "city": "Springfield",
            "state": "IL",
            "zip_code": "62702",
            "latitude": 39.7850,
            "longitude": -89.6480,
        },
        "average_rating": 4.8,
        "review_count": 1,
        "created_at": datetime(2024, 2, 10),
    },
    3: {
        "id": 3,
        "name": "La Piazza",
        "cuisine": "Italian",
        "description": "Family-style Italian dining with house-made pasta.",
        "price_range": "$$",
        "phone": "555-100-0003",
        "website": None,
        "location": {
            "address": "789 Elm Blvd",
            "city": "Springfield",
            "state": "IL",
            "zip_code": "62703",
            "latitude": 39.7790,
            "longitude": -89.6520,
        },
        "average_rating": 4.2,
        "review_count": 1,
        "created_at": datetime(2024, 3, 5),
    },
}

_reviews: Dict[int, dict] = {
    1: {
        "id": 1,
        "restaurant_id": 1,
        "user_id": 1,
        "rating": 5.0,
        "title": "Amazing burgers!",
        "body": "Best comfort food in town. The fries are incredible.",
        "created_at": datetime(2024, 4, 1),
    },
    2: {
        "id": 2,
        "restaurant_id": 1,
        "user_id": 2,
        "rating": 4.0,
        "title": "Great atmosphere",
        "body": "Solid food, friendly staff.",
        "created_at": datetime(2024, 4, 10),
    },
    3: {
        "id": 3,
        "restaurant_id": 2,
        "user_id": 1,
        "rating": 4.8,
        "title": "Freshest sushi around",
        "body": "The omakase is worth every penny.",
        "created_at": datetime(2024, 4, 15),
    },
    4: {
        "id": 4,
        "restaurant_id": 3,
        "user_id": 2,
        "rating": 4.2,
        "title": "Tasty pasta",
        "body": "The carbonara is excellent.",
        "created_at": datetime(2024, 4, 20),
    },
}

_users: Dict[int, dict] = {
    1: {
        "id": 1,
        "username": "foodie_alice",
        "email": "alice@example.com",
        "created_at": datetime(2024, 1, 1),
    },
    2: {
        "id": 2,
        "username": "restaurant_bob",
        "email": "bob@example.com",
        "created_at": datetime(2024, 1, 5),
    },
}

_restaurant_id_counter = 4
_review_id_counter = 5
_user_id_counter = 3


def get_all_restaurants() -> List[dict]:
    return list(_restaurants.values())


def get_restaurant(restaurant_id: int) -> Optional[dict]:
    return _restaurants.get(restaurant_id)


def create_restaurant(data: dict) -> dict:
    global _restaurant_id_counter
    restaurant = {
        **data,
        "id": _restaurant_id_counter,
        "average_rating": 0.0,
        "review_count": 0,
        "created_at": datetime.utcnow(),
    }
    _restaurants[_restaurant_id_counter] = restaurant
    _restaurant_id_counter += 1
    return restaurant


def delete_restaurant(restaurant_id: int) -> bool:
    if restaurant_id in _restaurants:
        del _restaurants[restaurant_id]
        return True
    return False


def get_all_reviews() -> List[dict]:
    return list(_reviews.values())


def get_reviews_for_restaurant(restaurant_id: int) -> List[dict]:
    return [r for r in _reviews.values() if r["restaurant_id"] == restaurant_id]


def get_review(review_id: int) -> Optional[dict]:
    return _reviews.get(review_id)


def create_review(data: dict) -> dict:
    global _review_id_counter
    review = {
        **data,
        "id": _review_id_counter,
        "created_at": datetime.utcnow(),
    }
    _reviews[_review_id_counter] = review
    _review_id_counter += 1
    restaurant_id = data["restaurant_id"]
    if restaurant_id in _restaurants:
        all_ratings = [
            r["rating"]
            for r in _reviews.values()
            if r["restaurant_id"] == restaurant_id
        ]
        all_ratings.append(data["rating"])
        _restaurants[restaurant_id]["average_rating"] = round(
            sum(all_ratings) / len(all_ratings), 2
        )
        _restaurants[restaurant_id]["review_count"] = len(all_ratings)
    return review


def get_all_users() -> List[dict]:
    return list(_users.values())


def get_user(user_id: int) -> Optional[dict]:
    return _users.get(user_id)


def create_user(data: dict) -> dict:
    global _user_id_counter
    user = {
        **data,
        "id": _user_id_counter,
        "created_at": datetime.utcnow(),
    }
    _users[_user_id_counter] = user
    _user_id_counter += 1
    return user
