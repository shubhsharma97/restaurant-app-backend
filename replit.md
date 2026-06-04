# restaurant-app-backend

FastAPI backend for a restaurant discovery application.

## Overview

A RESTful API built with FastAPI that provides endpoints for browsing restaurants, reading and writing reviews, and managing users. Data is stored in-memory with sample seed data included.

## Running the App

The app runs via the "Start application" workflow on port 5000.

```
uvicorn main:app --host 0.0.0.0 --port 5000 --reload
```

Interactive API docs are available at `/docs` (Swagger UI) and `/redoc`.

## Project Structure

```
main.py              # FastAPI app entry point
app/
  models.py          # Pydantic request/response models
  database.py        # In-memory data store with seed data
  routers/
    restaurants.py   # /restaurants endpoints
    reviews.py       # /reviews endpoints
    users.py         # /users endpoints
```

## API Endpoints

- `GET /` — API root info
- `GET /health` — Health check
- `GET /restaurants/` — List restaurants (filter by cuisine, city)
- `GET /restaurants/{id}` — Get single restaurant
- `POST /restaurants/` — Create restaurant
- `DELETE /restaurants/{id}` — Delete restaurant
- `GET /reviews/` — List all reviews
- `GET /reviews/restaurant/{id}` — Reviews for a restaurant
- `POST /reviews/` — Create a review
- `GET /users/` — List users
- `GET /users/{id}` — Get user
- `POST /users/` — Create user

## User Preferences

- Python 3.11
- FastAPI + uvicorn
