from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, Any
from database import get_db
import models

router = APIRouter(
    prefix="/leaderboard",
    tags=["leaderboard"],
)

@router.get("/{gd_leaderboard_name}", response_model=Dict[str, Any])
def get_leaderboard(gd_leaderboard_name: str, db: Session = Depends(get_db)):
    leaderboard = db.query(models.GdLeaderboard).filter(
        models.GdLeaderboard.gd_leaderboard_name == gd_leaderboard_name
    ).first()
    
    if not leaderboard:
        raise HTTPException(status_code=404, detail="Leaderboard not found")
        
    max_reward_rank = db.query(func.max(models.GdLeaderboardReward.gd_leaderboard_reward_end_rank)).filter(
        models.GdLeaderboardReward.linked_gd_leaderboard == leaderboard.id
    ).scalar() or 50
    
    display_limit = min(int(1.5 * max_reward_rank), 100)
    
    top_users = db.query(models.UdLeaderboardUser).filter(
        models.UdLeaderboardUser.linked_gd_leaderboard == leaderboard.id
    ).order_by(
        models.UdLeaderboardUser.current_rank.asc()
    ).limit(display_limit).all()
    
    results = []
    for user in top_users:
        user_name = "Player"
        if user.linked_ud_user_master:
            um = db.query(models.UdUserMaster).filter(models.UdUserMaster.id == user.linked_ud_user_master).first()
            if um:
                user_name = um.ud_user_master_display_name or um.ud_user_master_name
        elif user.linked_gd_bot_profile:
            bot = db.query(models.GdBotProfile).filter(models.GdBotProfile.id == user.linked_gd_bot_profile).first()
            if bot:
                user_name = getattr(bot, "gd_bot_display_name", f"Bot #{bot.id}")
                
        results.append({
            "rank": user.current_rank,
            "name": user_name,
            "score": user.score,
            "is_bot": user.linked_gd_bot_profile is not None
        })
        
    return {
        "leaderboard_name": leaderboard.gd_leaderboard_name,
        "title": leaderboard.gd_leaderboard_title,
        "entries": results
    }
