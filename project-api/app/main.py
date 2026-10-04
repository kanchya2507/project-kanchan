from fastapi import FastAPI
from datetime import datetime

app = FastAPI(
    title="Project API",
    description="Sample FastAPI application deployed on AWS ECS Fargate",
    version="1.1.0"  # 1. Bumped version to 1.1.0
)


@app.get("/")
def root():
    return {
        # 2. Updated the message to clearly state it went through the pipeline
        "message": "Hello from FastAPI! Successfully deployed via automated GitHub Actions CD!",
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
            {"id": 3, "name": "Priya"},
            {"id": 4, "name": "Kanchan (Added via CD)"}  # 3. Added a new user to test database/data updates
        ]
    }
