import os
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from sqlalchemy import text

# Local cache to prevent redundant database hits on rapid successive queries
_cached_offset = 0.0
_last_cache_time = 0.0
CACHE_TTL_SECONDS = 2.0

TIME_SHIFT_COLUMNS = [
    ("gd_challenge_config", ["gd_challenge_config_start_date", "gd_challenge_config_end_date"]),
    ("gd_pvp_config", ["gd_pvp_config_start_date", "gd_pvp_config_end_date"]),
    ("gd_leaderboard", ["gd_leaderboard_start_time", "gd_leaderboard_end_time"]),
    ("gd_user_message", ["created_at", "expires_at"]),
    ("gd_game_details", ["gd_game_details_maintenance_off_date_time"]),
    ("ud_user_challenge", ["last_completed_at"]),
    ("ud_user_give_away", ["claimed_at"]),
    ("ud_user_rewardhighway", ["claimed_at"]),
    ("ud_user_rock", ["ud_user_rock_aquired_date", "ud_user_rock_expiry_date"]),
    ("ud_user_broom", ["ud_user_broom_aquired_date", "ud_user_broom_expiry_date"]),
]

def _get_db():
    import database
    return database.SessionLocal()

def _ensure_state_table(db):
    db.execute(text("""
        CREATE TABLE IF NOT EXISTS `server_time_state` (
            `id` INT PRIMARY KEY,
            `offset_seconds` DOUBLE NOT NULL DEFAULT 0.0,
            `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
    """))
    db.commit()

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
                _ensure_state_table(db)
                db.execute(text("INSERT IGNORE INTO server_time_state (id, offset_seconds) VALUES (1, 0.0)"))
                db.commit()
                _cached_offset = 0.0
            _last_cache_time = now
        finally:
            db.close()
    except Exception as e:
        print(f"[TimeUtils] Warning reading server_time_state from DB: {e}")

    return _cached_offset

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
    Shifts all database date columns directly so Direct MySQL (Unity client) and REST API both reflect the shift.
    """
    global _cached_offset, _last_cache_time
    current_offset = get_offset_seconds()

    if target_date:
        try:
            clean_date = target_date.replace("Z", "+00:00")
            dt = datetime.fromisoformat(clean_date).replace(tzinfo=None)
            real_now = datetime.utcnow()
            new_offset = (dt - real_now).total_seconds()
            delta_seconds = new_offset - current_offset
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
        delta_seconds = delta
        new_offset = current_offset + delta

    if abs(delta_seconds) > 0.001:
        int_delta = int(round(delta_seconds))
        db = _get_db()
        try:
            _ensure_state_table(db)
            # Shift all database date columns
            for table_name, columns in TIME_SHIFT_COLUMNS:
                try:
                    set_clauses = [f"`{col}` = DATE_SUB(`{col}`, INTERVAL :delta_sec SECOND)" for col in columns]
                    where_clauses = [f"`{col}` IS NOT NULL" for col in columns]
                    sql = f"UPDATE `{table_name}` SET {', '.join(set_clauses)} WHERE {' OR '.join(where_clauses)}"
                    db.execute(text(sql), {"delta_sec": int_delta})
                except Exception as ex:
                    print(f"[TimeUtils] Warning shifting table {table_name}: {ex}")

            # Update offset record
            db.execute(text("""
                REPLACE INTO `server_time_state` (`id`, `offset_seconds`) VALUES (1, :offset)
            """), {"offset": new_offset})
            db.commit()
            _cached_offset = new_offset
            _last_cache_time = time.time()
        except Exception as e:
            db.rollback()
            print(f"[TimeUtils] Error shifting server time in DB: {e}")
            raise e
        finally:
            db.close()

    print(f"[TimeUtils] Server Time Shifted! New Server Time: {get_server_time().isoformat()}Z (Offset: {new_offset}s)")
    return get_time_status()

def reset_server_time() -> Dict[str, Any]:
    """
    Resets the server time offset back to 0 (real live UTC) and restores original database dates.
    """
    global _cached_offset, _last_cache_time
    current_offset = get_offset_seconds()

    if abs(current_offset) > 0.001:
        int_offset = int(round(current_offset))
        db = _get_db()
        try:
            _ensure_state_table(db)
            # Restore all database date columns by adding back the accumulated offset
            for table_name, columns in TIME_SHIFT_COLUMNS:
                try:
                    set_clauses = [f"`{col}` = DATE_ADD(`{col}`, INTERVAL :offset_sec SECOND)" for col in columns]
                    where_clauses = [f"`{col}` IS NOT NULL" for col in columns]
                    sql = f"UPDATE `{table_name}` SET {', '.join(set_clauses)} WHERE {' OR '.join(where_clauses)}"
                    db.execute(text(sql), {"offset_sec": int_offset})
                except Exception as ex:
                    print(f"[TimeUtils] Warning restoring table {table_name}: {ex}")

            db.execute(text("""
                REPLACE INTO `server_time_state` (`id`, `offset_seconds`) VALUES (1, 0.0)
            """))
            db.commit()
            _cached_offset = 0.0
            _last_cache_time = time.time()
        except Exception as e:
            db.rollback()
            print(f"[TimeUtils] Error resetting server time in DB: {e}")
            raise e
        finally:
            db.close()

    print(f"[TimeUtils] Server Time Reset to live UTC: {get_server_time().isoformat()}Z")
    return get_time_status()
