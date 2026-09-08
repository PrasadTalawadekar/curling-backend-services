import asyncio
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import engine, get_db, SessionLocal
from routers import gamedata, pvp_ws, leaderboard, users, auth

app = FastAPI(title="Curling Mobile Game LiveOps, PvP & Leaderboard Backend")

# Register core routers
app.include_router(auth.router)
app.include_router(gamedata.router)
app.include_router(pvp_ws.router)
app.include_router(leaderboard.router)
app.include_router(users.router)

async def periodic_leaderboard_sync():
    """
    Periodically checks gd_leaderboard for gd_leaderboard_refresh_mins and runs sync.
    """
    while True:
        try:
            db = SessionLocal()
            try:
                active_lbs = db.query(models.GdLeaderboard).filter(models.GdLeaderboard.is_enabled == True).all()
                refresh_mins = 5
                if active_lbs:
                    mins_list = [getattr(l, "gd_leaderboard_refresh_mins", 5) or 5 for l in active_lbs if (getattr(l, "gd_leaderboard_refresh_mins", 5) or 5) > 0]
                    if mins_list:
                        refresh_mins = min(mins_list)
                
                leaderboard.sync_leaderboard_data(db)
            finally:
                db.close()
                
            await asyncio.sleep(refresh_mins * 60)
        except Exception as e:
            print(f"[Main] Error in periodic_leaderboard_sync: {e}")
            await asyncio.sleep(60)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(periodic_leaderboard_sync())

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
