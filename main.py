from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import restaurants, reviews, users

app = FastAPI(
    title="Restaurant Discovery API",
    description="FastAPI backend for restaurant discovery app",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(restaurants.router, prefix="/restaurants", tags=["restaurants"])
app.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
app.include_router(users.router, prefix="/users", tags=["users"])


@app.get("/")
def root():
    return {"message": "Restaurant Discovery API", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}
