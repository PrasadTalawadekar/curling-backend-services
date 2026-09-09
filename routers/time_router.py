import os
from fastapi import APIRouter, Header, HTTPException, Query, Body
from pydantic import BaseModel
from typing import Optional
from services.time_service import time_service

router = APIRouter(tags=["Time & LiveOps TimeShift"])

ADMIN_SECRET_KEY = os.getenv("ADMIN_SECRET_KEY", "curling_admin_secret_2026")

class TimeshiftRequest(BaseModel):
    add_days: Optional[float] = 0.0
    add_hours: Optional[float] = 0.0
    add_minutes: Optional[float] = 0.0
    offset_seconds: Optional[float] = None
    target_iso: Optional[str] = None
    reset: Optional[bool] = False

@router.get("/time")
@router.get("/api/time")
def get_current_time():
    """
    Returns the current authoritative game time (with any active LiveOps shift).
    Queried by the Unity game client and liveops tools.
    """
    return time_service.get_status_dict()

@router.get("/api/admin/timeshift/status")
def get_timeshift_status():
    """
    Returns the current timeshift status and details.
    """
    return time_service.get_status_dict()

@router.post("/api/admin/timeshift")
def update_timeshift(
    req: TimeshiftRequest,
    x_admin_key: Optional[str] = Header(None)
):
    """
    Adjusts the game time shift for testing and LiveOps event validation.
    """
    # Verify admin key if provided in env
    expected_key = os.getenv("ADMIN_KEY")
    if expected_key and x_admin_key != expected_key:
        raise HTTPException(status_code=403, detail="Invalid admin key")

    if req.reset:
        time_service.reset()
    elif req.target_iso:
        try:
            time_service.set_target_time(req.target_iso)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid target_iso format: {e}")
    elif req.offset_seconds is not None:
        time_service.set_offset_seconds(req.offset_seconds)
    elif req.add_days or req.add_hours or req.add_minutes:
        time_service.shift_by(days=req.add_days or 0, hours=req.add_hours or 0, minutes=req.add_minutes or 0)

    return {
        "message": "Timeshift updated successfully",
        **time_service.get_status_dict()
    }
