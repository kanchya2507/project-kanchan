from fastapi import FastAPI
from datetime import datetime

app = FastAPI(
    title="Project API",
    description="Sample FastAPI application deployed on AWS ECS Fargate",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Hello from FastAPI running on AWS ECS!",
        "status": "success"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/api/users")
def get_users():
    return {
        "users": [
            {"id": 1, "name": "Rohit"},
            {"id": 2, "name": "Amit"},
            {"id": 3, "name": "Priya"}
        ]
    }