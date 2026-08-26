from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import engine, get_db
from routers import pvp_ws, leaderboard, users

app = FastAPI(title="Curling Mobile Game PvP & Leaderboard Backend")

# Register core routers
app.include_router(pvp_ws.router)
app.include_router(leaderboard.router)
app.include_router(users.router)

@app.get("/")
def read_root():
    return {
        "service": "Curling Mobile Game PvP & Leaderboard Backend",
        "status": "online",
        "pvp_websocket": "/ws/matchmaking",
        "leaderboard": "/leaderboard"
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}
