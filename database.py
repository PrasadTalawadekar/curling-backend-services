import os
import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

INSTANCE_CONNECTION_NAME = os.getenv("INSTANCE_CONNECTION_NAME", "curling-mobile-game:asia-south1:curling-db")
DB_TYPE = os.getenv("DB_TYPE", "mysql").lower()
DB_USER = os.getenv("DB_USER", "siddhi")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "curling_db")
DB_HOST = os.getenv("DB_HOST", "34.14.133.235")
DB_PORT = os.getenv("DB_PORT", "3306" if "mysql" in DB_TYPE else "5432")
DATABASE_URL = os.getenv("DATABASE_URL")

user_enc = urllib.parse.quote_plus(DB_USER)
pwd_enc = urllib.parse.quote_plus(DB_PASSWORD)
auth_str = f"{user_enc}:{pwd_enc}" if DB_PASSWORD else user_enc

if not DATABASE_URL or "<YOUR_" in DATABASE_URL:
    if INSTANCE_CONNECTION_NAME and os.path.exists(f"/cloudsql/{INSTANCE_CONNECTION_NAME}"):
        if "postgres" in DB_TYPE:
            DATABASE_URL = f"postgresql+psycopg2://{auth_str}@/{DB_NAME}?host=/cloudsql/{INSTANCE_CONNECTION_NAME}"
        else:
            DATABASE_URL = f"mysql+pymysql://{auth_str}@/{DB_NAME}?unix_socket=/cloudsql/{INSTANCE_CONNECTION_NAME}"
    elif DB_HOST:
        if "postgres" in DB_TYPE:
            DATABASE_URL = f"postgresql+psycopg2://{auth_str}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        else:
            DATABASE_URL = f"mysql+pymysql://{auth_str}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    else:
        DATABASE_URL = "sqlite:///./game_service.db"

connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
