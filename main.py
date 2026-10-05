import asyncio
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import engine, get_db, SessionLocal
from routers import gamedata, pvp_ws, leaderboard, users, auth, time_router

app = FastAPI(title="Curling Mobile Game LiveOps, PvP & Leaderboard Backend")

# Register core routers
app.include_router(auth.router)
app.include_router(gamedata.router)
app.include_router(pvp_ws.router)
app.include_router(leaderboard.router)
app.include_router(users.router)
app.include_router(time_router.router)

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

import os
from fastapi.responses import HTMLResponse, PlainTextResponse

# Cache templates
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
LANDING_HTML_PATH = os.path.join(TEMPLATES_DIR, "landing.html")
PLAY_HTML_PATH = os.path.join(TEMPLATES_DIR, "play.html")

LANDING_HTML_CONTENT = ""
if os.path.exists(LANDING_HTML_PATH):
    with open(LANDING_HTML_PATH, "r", encoding="utf-8") as f:
        LANDING_HTML_CONTENT = f.read()

PLAY_HTML_CONTENT = ""
if os.path.exists(PLAY_HTML_PATH):
    with open(PLAY_HTML_PATH, "r", encoding="utf-8") as f:
        PLAY_HTML_CONTENT = f.read()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(periodic_leaderboard_sync())

@app.get("/", response_class=HTMLResponse)
def read_root():
    if LANDING_HTML_CONTENT:
        return HTMLResponse(content=LANDING_HTML_CONTENT, status_code=200)
    return HTMLResponse(content="<h1>Curling Mobile Game</h1><p>Welcome to Curling Mobile Game!</p>", status_code=200)

@app.get("/play", response_class=HTMLResponse)
@app.get("/download", response_class=HTMLResponse)
def get_play_redirect():
    if PLAY_HTML_CONTENT:
        return HTMLResponse(content=PLAY_HTML_CONTENT, status_code=200)
    if LANDING_HTML_CONTENT:
        return HTMLResponse(content=LANDING_HTML_CONTENT, status_code=200)
    return HTMLResponse(content="<h1>Curling Mobile Game</h1><p><a href='https://play.google.com/store/apps/details?id=com.curling.mobile.game'>Download on Google Play</a></p>", status_code=200)

@app.get("/app-ads.txt", response_class=PlainTextResponse)
def get_app_ads():
    return PlainTextResponse("google.com, pub-1474686776703930, DIRECT, f08c47fec0942fa0\n", media_type="text/plain")

@app.get("/privacy-policy", response_class=HTMLResponse)
def get_privacy_policy():
    if LANDING_HTML_CONTENT:
        return HTMLResponse(content=LANDING_HTML_CONTENT, status_code=200)
    return HTMLResponse(content="<h1>Privacy Policy</h1><p>Curling Mobile Game Privacy Policy</p>", status_code=200)

@app.get("/api")
def read_api_metadata():
    return {
        "service": "Curling Mobile Game LiveOps, PvP & Leaderboard Backend",
        "status": "online",
        "play_redirect": "/play",
        "rest_api": "/rest/v1/{table_name}",
        "pvp_websocket": "/ws/matchmaking",
        "leaderboard": "/leaderboard",
        "app_ads": "/app-ads.txt"
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}


