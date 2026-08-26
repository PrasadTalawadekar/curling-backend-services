from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import get_db

router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"]
)

@router.get("/", response_model=List[schemas.UdUserMaster])
def get_all_users(db: Session = Depends(get_db)):
    """
    Get all users.
    """
    return db.query(models.UdUserMaster).all()

@router.get("/{user_id}", response_model=schemas.UdUserMaster)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get a specific user by ID.
    """
    user = db.query(models.UdUserMaster).filter(models.UdUserMaster.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/{user_id}/wallet", response_model=schemas.UdUserWallet)
def get_user_wallet(user_id: int, db: Session = Depends(get_db)):
    """
    Get a user's wallet
    """
    wallet = db.query(models.UdUserWallet).filter(models.UdUserWallet.linked_ud_user_master == user_id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet

@router.get("/{user_id}/loadout", response_model=schemas.UdUserLoadout)
def get_user_loadout(user_id: int, db: Session = Depends(get_db)):
    """
    Get a user's active loadout
    """
    loadout = db.query(models.UdUserLoadout).filter(models.UdUserLoadout.linked_ud_user_master == user_id).first()
    if not loadout:
        raise HTTPException(status_code=404, detail="Loadout not found")
    return loadout

@router.get("/{user_id}/profile-container")
def get_user_profile_container(user_id: int, db: Session = Depends(get_db)):
    """
    Get dynamic data for the user profile container.
    """
    user = db.query(models.UdUserMaster).filter(models.UdUserMaster.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    return {
        "user_id": user.id,
        "name": user.ud_user_master_display_name or user.ud_user_master_name,
        "level": 1, # TODO: Dynamic level calculation
        "next_level_xp": 100, # TODO: Dynamic XP logic
    }
