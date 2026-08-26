from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import get_db

router = APIRouter(
    prefix="/bots",
    tags=["bots"],
)

# --- GdBotProfile ---
@router.get("/profiles/", response_model=List[schemas.GdBotProfile])
def read_bot_profiles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.GdBotProfile).offset(skip).limit(limit).all()

@router.get("/profiles/{bot_id}", response_model=schemas.GdBotProfile)
def read_bot_profile(bot_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(models.GdBotProfile).filter(models.GdBotProfile.id == bot_id).first()
    if db_obj is None:
        raise HTTPException(status_code=404, detail="Bot Profile not found")
    return db_obj



# --- GdBotBehavior ---
@router.get("/behaviors/", response_model=List[schemas.GdBotBehavior])
def read_bot_behaviors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.GdBotBehavior).offset(skip).limit(limit).all()

@router.get("/behaviors/{behavior_id}", response_model=schemas.GdBotBehavior)
def read_bot_behavior(behavior_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(models.GdBotBehavior).filter(models.GdBotBehavior.id == behavior_id).first()
    if db_obj is None:
        raise HTTPException(status_code=404, detail="Bot Behavior not found")
    return db_obj
