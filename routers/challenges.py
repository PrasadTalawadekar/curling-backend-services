from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

import models, schemas
from database import get_db

router = APIRouter(
    prefix="/api/v1/challenges",
    tags=["challenges"],
)

class GdChallengeConfigNested(schemas.GdChallengeConfig):
    scenario: Optional[schemas.GdScenario] = None
    stone: Optional[schemas.GdRock] = None
    surface: Optional[schemas.GdSurface] = None
    environment: Optional[schemas.GdEnvironment] = None
    entry_fee_currency: Optional[schemas.GdGameCurrency] = None
    unlock_currency: Optional[schemas.GdGameCurrency] = None

    class Config:
        from_attributes = True
        orm_mode = True

@router.get("/features", response_model=List[schemas.GdChallenge])
def read_challenge_features(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.GdChallenge).offset(skip).limit(limit).all()

@router.get("/configs", response_model=List[GdChallengeConfigNested])
def read_challenge_configs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    configs = db.query(models.GdChallengeConfig).offset(skip).limit(limit).all()
    
    result = []
    for config in configs:
        # Construct nested payload manually since models.py lacks SQLAlchemy relationship() declarations
        nested = GdChallengeConfigNested.from_orm(config)
        
        if config.linked_gd_scenario:
            nested.scenario = db.query(models.GdScenario).filter(models.GdScenario.id == config.linked_gd_scenario).first()
        
        if config.linked_user_rock:
            nested.stone = db.query(models.GdRock).filter(models.GdRock.id == config.linked_user_rock).first()
            
        if config.linked_gd_surface:
            nested.surface = db.query(models.GdSurface).filter(models.GdSurface.id == config.linked_gd_surface).first()
            
        if config.linked_gd_environment:
            nested.environment = db.query(models.GdEnvironment).filter(models.GdEnvironment.id == config.linked_gd_environment).first()
            
        if config.linked_gd_game_currency_entry_fee:
            nested.entry_fee_currency = db.query(models.GdGameCurrency).filter(models.GdGameCurrency.id == config.linked_gd_game_currency_entry_fee).first()
            
        if config.linked_gd_game_currency_unlock:
            nested.unlock_currency = db.query(models.GdGameCurrency).filter(models.GdGameCurrency.id == config.linked_gd_game_currency_unlock).first()
            
        result.append(nested)
        
    return result
