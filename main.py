from fastapi import FastAPI
import models
from database import engine
from routers import pvp_ws, leaderboard, auth, users, gamedata

from sqlalchemy import text

# Auto-create all tables and ensure schema migrations in Cloud SQL
try:
    models.Base.metadata.create_all(bind=engine)
    with engine.connect() as conn:
        conn.execute(text("ALTER TABLE gd_challenge_module ADD COLUMN IF NOT EXISTS linked_gd_feature INTEGER;"))
        conn.execute(text("ALTER TABLE gd_pvp_module ADD COLUMN IF NOT EXISTS linked_gd_feature INTEGER;"))
        conn.commit()
except Exception as e:
    print(f"[Database] Startup schema migration: {e}")

app = FastAPI(title="Curling Mobile Game Backend Services")

# Register core routers
app.include_router(gamedata.router)
app.include_router(pvp_ws.router)
app.include_router(leaderboard.router)
app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
def read_root():
    return {
        "service": "Curling Mobile Game Backend",
        "status": "online",
        "rest_api": "/rest/v1/{table_name}",
        "pvp_websocket": "/ws/matchmaking",
        "leaderboard": "/leaderboard",
        "auth": "/auth/google"
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}
