from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import engine, get_db
from routers import gamedata, pvp_ws, leaderboard, users, auth

app = FastAPI(title="Curling Mobile Game LiveOps, PvP & Leaderboard Backend")

# Register core routers
app.include_router(auth.router)
app.include_router(gamedata.router)
app.include_router(pvp_ws.router)
app.include_router(leaderboard.router)
app.include_router(users.router)

@app.get("/")
def read_root():
    return {
        "service": "Curling Mobile Game LiveOps, PvP & Leaderboard Backend",
        "status": "online",
        "rest_api": "/rest/v1/{table_name}",
        "pvp_websocket": "/ws/matchmaking",
        "leaderboard": "/leaderboard"
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}
