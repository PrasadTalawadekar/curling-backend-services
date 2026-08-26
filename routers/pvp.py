from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models, schemas
from database import get_db

router = APIRouter(
    prefix="/api/v1/pvp",
    tags=["pvp"],
)

@router.get("/configs", response_model=List[schemas.GdPvpConfig])
def read_pvp_configs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(models.GdPvpConfig).offset(skip).limit(limit).all()
    return items
