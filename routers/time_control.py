from fastapi import APIRouter, HTTPException, Body
from typing import Optional, Dict, Any
from pydantic import BaseModel
import time_utils

router = APIRouter(prefix="/api/v1/time", tags=["TimeControl"])

class TimeShiftRequest(BaseModel):
    shift_seconds: Optional[float] = None
    shift_hours: Optional[float] = None
    shift_days: Optional[float] = None
    target_date: Optional[str] = None

@router.get("", response_model=Dict[str, Any])
@router.get("/", response_model=Dict[str, Any])
def get_time():
    """
    Returns the current server time (including any active time-shift offset) and real UTC.
    """
    return time_utils.get_time_status()

@router.post("/shift", response_model=Dict[str, Any])
def shift_time(payload: TimeShiftRequest):
    """
    Shifts the authoritative server clock forward or backward.
    """
    try:
        return time_utils.shift_server_time(
            shift_seconds=payload.shift_seconds,
            shift_hours=payload.shift_hours,
            shift_days=payload.shift_days,
            target_date=payload.target_date
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/reset", response_model=Dict[str, Any])
def reset_time():
    """
    Resets the server clock offset back to 0 (real-world UTC).
    """
    return time_utils.reset_server_time()
