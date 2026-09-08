import os
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from sqlalchemy import text

# Local cache to prevent redundant database hits on rapid successive queries
_cached_offset = 0.0
_last_cache_time = 0.0
CACHE_TTL_SECONDS = 2.0

def _get_db():
    import database
    return database.SessionLocal()

def get_offset_seconds() -> float:
    """
    Fetches the authoritative time offset in seconds from the MySQL database (server_time_state table).
    Caches for CACHE_TTL_SECONDS to ensure multi-instance consistency without excessive DB load.
    """
    global _cached_offset, _last_cache_time
    now = time.time()
    if (now - _last_cache_time) < CACHE_TTL_SECONDS:
        return _cached_offset

    try:
        db = _get_db()
        try:
            row = db.execute(text("SELECT offset_seconds FROM server_time_state WHERE id = 1")).fetchone()
            if row is not None:
                _cached_offset = float(row[0])
            else:
                db.execute(text("""
                    CREATE TABLE IF NOT EXISTS `server_time_state` (
                        `id` INT PRIMARY KEY,
                        `offset_seconds` DOUBLE NOT NULL DEFAULT 0.0,
                        `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                    )
                """))
                db.execute(text("INSERT IGNORE INTO server_time_state (id, offset_seconds) VALUES (1, 0.0)"))
                db.commit()
                _cached_offset = 0.0
            _last_cache_time = now
        finally:
            db.close()
    except Exception as e:
        print(f"[TimeUtils] Warning reading server_time_state from DB: {e}")

    return _cached_offset

def _save_offset_to_db(offset_sec: float):
    global _cached_offset, _last_cache_time
    _cached_offset = float(offset_sec)
    _last_cache_time = time.time()
    try:
        db = _get_db()
        try:
            db.execute(text("""
                CREATE TABLE IF NOT EXISTS `server_time_state` (
                    `id` INT PRIMARY KEY,
                    `offset_seconds` DOUBLE NOT NULL DEFAULT 0.0,
                    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """))
            db.execute(text("""
                REPLACE INTO `server_time_state` (`id`, `offset_seconds`) VALUES (1, :offset)
            """), {"offset": offset_sec})
            db.commit()
        finally:
            db.close()
    except Exception as e:
        print(f"[TimeUtils] Error saving server_time_state to DB: {e}")
        raise e

def get_server_time() -> datetime:
    """
    Returns the current authoritative server time, incorporating any active time shift offset.
    """
    offset = get_offset_seconds()
    return datetime.utcnow() + timedelta(seconds=offset)

def get_time_status() -> Dict[str, Any]:
    """
    Returns diagnostic information about the server time and active offset.
    """
    offset = get_offset_seconds()
    real_utc = datetime.utcnow()
    shifted_time = real_utc + timedelta(seconds=offset)
    return {
        "server_time_utc": shifted_time.isoformat() + "Z",
        "real_time_utc": real_utc.isoformat() + "Z",
        "offset_seconds": offset,
        "offset_hours": round(offset / 3600.0, 2),
        "offset_days": round(offset / 86400.0, 2),
        "is_time_shifted": abs(offset) > 0.001
    }

def shift_server_time(
    shift_seconds: Optional[float] = None,
    shift_hours: Optional[float] = None,
    shift_days: Optional[float] = None,
    target_date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Shifts the server time by an additive offset or to an absolute target date.
    Persists across all Cloud Run instances via MySQL.
    """
    current_offset = get_offset_seconds()

    if target_date:
        try:
            clean_date = target_date.replace("Z", "+00:00")
            dt = datetime.fromisoformat(clean_date).replace(tzinfo=None)
            real_now = datetime.utcnow()
            new_offset = (dt - real_now).total_seconds()
        except Exception as e:
            raise ValueError(f"Invalid target date format '{target_date}': {e}")
    else:
        delta = 0.0
        if shift_seconds is not None:
            delta += float(shift_seconds)
        if shift_hours is not None:
            delta += float(shift_hours) * 3600.0
        if shift_days is not None:
            delta += float(shift_days) * 86400.0
        new_offset = current_offset + delta

    _save_offset_to_db(new_offset)
    print(f"[TimeUtils] Server Time Shifted! New Server Time: {get_server_time().isoformat()}Z (Offset: {new_offset}s)")
    return get_time_status()

def reset_server_time() -> Dict[str, Any]:
    """
    Resets the server time offset back to 0 (real live UTC).
    """
    _save_offset_to_db(0.0)
    print(f"[TimeUtils] Server Time Reset to live UTC: {get_server_time().isoformat()}Z")
    return get_time_status()
