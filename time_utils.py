import os
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

STATE_FILE = os.path.join(os.path.dirname(__file__), "_server_time_offset.json")

_offset_seconds: float = 0.0

def _load_offset() -> float:
    global _offset_seconds
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                _offset_seconds = float(data.get("offset_seconds", 0.0))
        except Exception as e:
            print(f"[TimeUtils] Warning: Could not load time offset state: {e}")
            _offset_seconds = 0.0
    return _offset_seconds

def _save_offset():
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "offset_seconds": _offset_seconds,
                "updated_at_utc": datetime.utcnow().isoformat() + "Z"
            }, f, indent=2)
    except Exception as e:
        print(f"[TimeUtils] Warning: Could not save time offset state: {e}")

# Initialize offset on module load
_load_offset()

def get_server_time() -> datetime:
    """
    Returns the current authoritative server time, incorporating any active time shift offset.
    """
    return datetime.utcnow() + timedelta(seconds=_offset_seconds)

def get_time_status() -> Dict[str, Any]:
    """
    Returns diagnostic information about the server time and active offset.
    """
    real_utc = datetime.utcnow()
    shifted_time = real_utc + timedelta(seconds=_offset_seconds)
    return {
        "server_time_utc": shifted_time.isoformat() + "Z",
        "real_time_utc": real_utc.isoformat() + "Z",
        "offset_seconds": _offset_seconds,
        "offset_hours": round(_offset_seconds / 3600.0, 2),
        "offset_days": round(_offset_seconds / 86400.0, 2),
        "is_time_shifted": abs(_offset_seconds) > 0.001
    }

def shift_server_time(
    shift_seconds: Optional[float] = None,
    shift_hours: Optional[float] = None,
    shift_days: Optional[float] = None,
    target_date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Shifts the server time by an additive offset or to an absolute target date.
    """
    global _offset_seconds
    
    if target_date:
        try:
            # Parse ISO date (support 'Z' or offset)
            clean_date = target_date.replace("Z", "+00:00")
            dt = datetime.fromisoformat(clean_date).replace(tzinfo=None)
            real_now = datetime.utcnow()
            _offset_seconds = (dt - real_now).total_seconds()
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
            
        _offset_seconds += delta

    _save_offset()
    print(f"[TimeUtils] Server Time Shifted! New Server Time: {get_server_time().isoformat()}Z (Offset: {_offset_seconds}s)")
    return get_time_status()

def reset_server_time() -> Dict[str, Any]:
    """
    Resets the server time offset back to 0 (real live UTC).
    """
    global _offset_seconds
    _offset_seconds = 0.0
    _save_offset()
    print(f"[TimeUtils] Server Time Reset to live UTC: {get_server_time().isoformat()}Z")
    return get_time_status()
