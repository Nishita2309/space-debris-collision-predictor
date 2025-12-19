from fastapi import FastAPI, Query
from core.collision import predict_collision
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Space Debris Collision Prediction API",
    version="1.0"
)

@app.get("/")
def home():
    return {"message": "Space Collision Prediction API is running"}

@app.get("/predict")
def predict(
    hours: int = Query(24, ge=1, le=72),
    step: int = Query(10, ge=1, le=60)
):
    with open("data/tle.txt") as f:
        tle_lines = f.read().strip().split("\n")

    return predict_collision(
        tle_lines,
        hours=hours,
        step_minutes=step
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

