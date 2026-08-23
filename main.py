from fastapi import FastAPI
import models
from database import engine
from routers import pvp_ws, leaderboard, auth, users, gamedata

from sqlalchemy import text, inspect as sa_inspect

# Auto-create all tables and ensure schema migrations in Cloud SQL
try:
    models.Base.metadata.create_all(bind=engine)
    inspector = sa_inspect(engine)
    for tbl in ['gd_challenge_module', 'gd_pvp_module']:
        if tbl in inspector.get_table_names():
            cols = [c['name'] for c in inspector.get_columns(tbl)]
            if 'linked_gd_feature' not in cols:
                with engine.connect() as conn:
                    conn.execute(text(f"ALTER TABLE {tbl} ADD COLUMN linked_gd_feature INT NULL;"))
                    conn.commit()
                    print(f"[Schema] Added linked_gd_feature to {tbl}")
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
