from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import get_db

router = APIRouter(
    prefix="/api/v1/giveaways",
    tags=["giveaways"]
)

@router.get("/", response_model=List[schemas.GdGiveAway])
def get_giveaways(db: Session = Depends(get_db)):
    """
    Get all active giveaways
    """
    return db.query(models.GdGiveAway).filter(models.GdGiveAway.is_enabled == True).all()

@router.get("/{giveaway_id}/items", response_model=List[schemas.GdGiveAwayItem])
def get_giveaway_items(giveaway_id: int, db: Session = Depends(get_db)):
    """
    Get all active items linked to a specific giveaway via the mapper table
    """
    # Find all mappers for this giveaway
    mappers = db.query(models.GdGiveAwayItemMapper).filter(
        models.GdGiveAwayItemMapper.linked_gd_give_away == giveaway_id,
        models.GdGiveAwayItemMapper.is_enabled == True
    ).order_by(models.GdGiveAwayItemMapper.gd_give_away_item_mapper_priority.desc()).all()
    
    if not mappers:
        return []
        
    item_ids = []
    for mapper in mappers:
        if mapper.linked_gd_give_away_item_csv:
            item_ids.extend([int(x.strip()) for x in mapper.linked_gd_give_away_item_csv.split(',') if x.strip()])
    
    if not item_ids:
        return []
    
    # Fetch the actual items
    items = db.query(models.GdGiveAwayItem).filter(
        models.GdGiveAwayItem.id.in_(item_ids),
        models.GdGiveAwayItem.is_enabled == True
    ).all()
    
    return items
