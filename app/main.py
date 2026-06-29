from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import init_db
from app.api import auth

# Initialize database (create tables)
init_db()

app = FastAPI(
    title="Restaurant Discovery API",
    description="API for restaurant discovery and recipe suggestions",
    version="1.0.0"
)

# Allow frontend to call this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include authentication routes
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Restaurant Discovery API!"}


@app.get("/api/health")
def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
