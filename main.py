from fastapi import FastAPI
import models
from database import engine
from routers import pvp_ws, leaderboard, auth

# Auto-create all tables in Cloud SQL PostgreSQL
try:
    models.Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"[Database] Warning creating tables on startup: {e}")

app = FastAPI(title="Curling Mobile Game Backend Services")

# Register core routers
app.include_router(pvp_ws.router)
app.include_router(leaderboard.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {
        "service": "Curling Mobile Game Backend",
        "status": "online",
        "pvp_websocket": "/ws/matchmaking",
        "leaderboard": "/leaderboard",
        "auth": "/auth/google"
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}
