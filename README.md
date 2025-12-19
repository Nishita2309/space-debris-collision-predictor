# 🛰️ Space Debris Collision Predictor

A full-stack, physics-based platform that predicts potential collisions between active satellites and space debris using real orbital data.

## 🚀 Features
- Real orbit propagation (TLE-based)
- Multi-debris collision screening
- Collision probability scoring
- Risk classification (SAFE / WARNING / HIGH)
- 3D orbit visualization
- Interactive React dashboard

## 🧠 Tech Stack
- Backend: FastAPI, Python, Skyfield
- Frontend: React (Vite)
- Visualization: Matplotlib (3D)
- Data: TLE orbital elements

## ▶️ How to Run

### Backend
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
