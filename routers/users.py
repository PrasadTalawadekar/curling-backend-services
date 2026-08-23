import datetime
import random
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"]
)


def generate_unique_user_id(db: Session) -> int:
    """Generates a random 9-digit integer player ID (100,000,000 - 999,999,999)."""
    while True:
        uid = random.randint(100_000_000, 999_999_999)
        if not db.query(models.UdUserMaster).filter(models.UdUserMaster.id == uid).first():
            return uid


class LoginRequest(BaseModel):
    auth_id: Optional[str] = None
    display_name: Optional[str] = None
    platform: Optional[str] = "Android"
    app_version: Optional[str] = "1.0.0"
    gmail_id: Optional[str] = None


class SyncRequest(BaseModel):
    user_id: int
    wallet_currencies: Optional[Dict[str, int]] = None
    stats: Optional[Dict[str, Any]] = None
    loadout: Optional[Dict[str, Any]] = None
    platform: Optional[str] = "Android"
    app_version: Optional[str] = "1.0.0"


class UpdateNameRequest(BaseModel):
    display_name: str


class DailyActivityRequest(BaseModel):
    p_user_id: int
    p_platform: Optional[str] = "Android"
    p_app_version: Optional[str] = "1.0.0"


@router.post("/login")
def login_or_register(req: LoginRequest, db: Session = Depends(get_db)):
    """
    Unified 1-call login: returns User Profile, Wallet, Stats, Loadout, and Inventory in 1 response.
    """
    user = None

    # 1. Try finding existing user by auth_id or gmail_id
    if req.auth_id:
        user = db.query(models.UdUserMaster).filter(models.UdUserMaster.auth_id == req.auth_id).first()
    elif req.gmail_id:
        user = db.query(models.UdUserMaster).filter(models.UdUserMaster.ud_user_master_gmail_id == req.gmail_id).first()

    # 2. Create new user with 9-digit ID if not found
    is_new_user = False
    if not user:
        is_new_user = True
        new_id = generate_unique_user_id(db)
        default_name = req.display_name or f"Player #{str(new_id)[-4:]}"

        user = models.UdUserMaster(
            id=new_id,
            auth_id=req.auth_id or f"guest_{new_id}",
            ud_user_master_name=default_name,
            ud_user_master_display_name=default_name,
            is_ud_user_master_gmail=bool(req.gmail_id),
            ud_user_master_gmail_id=req.gmail_id,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        # Create starting wallet (500 coins, 10 gems)
        wallet = models.UdUserWallet(
            linked_ud_user_master=user.id,
            ud_user_wallet_currency_dictionary={"coins": 500, "gems": 10}
        )
        db.add(wallet)

        # Create starting stats
        stats = models.UdUserStats(
            linked_ud_user_master=user.id,
            ud_user_stats_xp=0,
            ud_user_stats_total_match_played=0,
            ud_user_stats_total_match_won=0,
            ud_user_stats_current_win_streak=0
        )
        db.add(stats)

        # Create default starting Rock
        free_rock = db.query(models.GdRock).filter(models.GdRock.is_free == True).first()
        free_rock_id = free_rock.id if free_rock else 1
        user_rock = models.UdUserRock(
            linked_ud_user_master=user.id,
            linked_gd_rock=free_rock_id,
            ud_user_rock_name="Default Granite"
        )
        db.add(user_rock)

        # Create default starting Broom
        free_broom = db.query(models.GdBroom).filter(models.GdBroom.is_free == True).first()
        free_broom_id = free_broom.id if free_broom else 1
        user_broom = models.UdUserBroom(
            linked_ud_user_master=user.id,
            linked_gd_broom=free_broom_id,
            ud_user_broom_name="Standard Broom"
        )
        db.add(user_broom)
        db.commit()

        # Create starting Loadout
        loadout = models.UdUserLoadout(
            linked_ud_user_master=user.id,
            linked_ud_user_rock=user_rock.id,
            linked_ud_user_broom=user_broom.id
        )
        db.add(loadout)
        db.commit()

    # 3. Fetch current user state
    wallet = db.query(models.UdUserWallet).filter(models.UdUserWallet.linked_ud_user_master == user.id).first()
    stats = db.query(models.UdUserStats).filter(models.UdUserStats.linked_ud_user_master == user.id).first()
    loadout = db.query(models.UdUserLoadout).filter(models.UdUserLoadout.linked_ud_user_master == user.id).first()
    owned_rocks = db.query(models.UdUserRock).filter(models.UdUserRock.linked_ud_user_master == user.id).all()
    owned_brooms = db.query(models.UdUserBroom).filter(models.UdUserBroom.linked_ud_user_master == user.id).all()

    # 4. Record Daily Retention Log
    try:
        activity = models.AnalysisUserDailyActivity(
            p_user_id=user.id,
            p_platform=req.platform or "Android",
            p_app_version=req.app_version or "1.0.0",
            p_first_seen_date=user.ud_user_master_created_at
        )
        db.add(activity)
        db.commit()
    except Exception:
        pass

    return {
        "status": "success",
        "is_new_user": is_new_user,
        "user": {
            "id": user.id,
            "display_name": user.ud_user_master_display_name,
            "created_at": user.ud_user_master_created_at.isoformat() if user.ud_user_master_created_at else None,
            "ftue_step": user.ud_user_master_ftue_step,
            "is_gmail": user.is_ud_user_master_gmail,
        },
        "wallet": wallet.ud_user_wallet_currency_dictionary if wallet else {},
        "stats": {
            "xp": stats.ud_user_stats_xp if stats else 0,
            "matches_played": stats.ud_user_stats_total_match_played if stats else 0,
            "matches_won": stats.ud_user_stats_total_match_won if stats else 0,
            "win_streak": stats.ud_user_stats_current_win_streak if stats else 0,
        },
        "loadout": {
            "rock_id": loadout.linked_ud_user_rock if loadout else None,
            "broom_id": loadout.linked_ud_user_broom if loadout else None,
        },
        "owned_rocks": [{"id": r.id, "rock_id": r.linked_gd_rock, "name": r.ud_user_rock_name} for r in owned_rocks],
        "owned_brooms": [{"id": b.id, "broom_id": b.linked_gd_broom, "name": b.ud_user_broom_name} for b in owned_brooms],
    }


@router.post("/sync")
def sync_user_data(req: SyncRequest, db: Session = Depends(get_db)):
    """
    Sync wallet balances, match stats, and save gameplay progression.
    """
    user = db.query(models.UdUserMaster).filter(models.UdUserMaster.id == req.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if req.wallet_currencies is not None:
        wallet = db.query(models.UdUserWallet).filter(models.UdUserWallet.linked_ud_user_master == user.id).first()
        if wallet:
            wallet.ud_user_wallet_currency_dictionary = req.wallet_currencies

    if req.stats is not None:
        stats = db.query(models.UdUserStats).filter(models.UdUserStats.linked_ud_user_master == user.id).first()
        if stats:
            if "xp" in req.stats: stats.ud_user_stats_xp = req.stats["xp"]
            if "matches_played" in req.stats: stats.ud_user_stats_total_match_played = req.stats["matches_played"]
            if "matches_won" in req.stats: stats.ud_user_stats_total_match_won = req.stats["matches_won"]
            if "win_streak" in req.stats: stats.ud_user_stats_current_win_streak = req.stats["win_streak"]

    user.ud_user_master_last_updated = datetime.datetime.utcnow()
    db.commit()
    return {"status": "success", "user_id": user.id}


@router.patch("/{user_id}/display_name")
def update_display_name(user_id: int, req: UpdateNameRequest, db: Session = Depends(get_db)):
    user = db.query(models.UdUserMaster).filter(models.UdUserMaster.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.ud_user_master_display_name = req.display_name
    user.ud_user_master_display_name_change_instances += 1
    db.commit()
    return {"status": "success", "display_name": user.ud_user_master_display_name}


@router.post("/record_daily_activity")
def record_daily_activity(req: DailyActivityRequest, db: Session = Depends(get_db)):
    user = db.query(models.UdUserMaster).filter(models.UdUserMaster.id == req.p_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    activity = models.AnalysisUserDailyActivity(
        p_user_id=user.id,
        p_platform=req.p_platform,
        p_app_version=req.p_app_version,
        p_first_seen_date=user.ud_user_master_created_at
    )
    db.add(activity)
    db.commit()
    return {"status": "success"}
