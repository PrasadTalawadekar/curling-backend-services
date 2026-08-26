from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any

from database import get_db
import models

router = APIRouter(
    prefix="/leaderboard",
    tags=["leaderboard"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{gd_leaderboard_name}", response_model=Dict[str, Any])
def get_leaderboard(gd_leaderboard_name: str, db: Session = Depends(get_db)):
    # 1. Look up the leaderboard
    leaderboard = db.query(models.GdLeaderboard).filter(
        models.GdLeaderboard.gd_leaderboard_name == gd_leaderboard_name
    ).first()
    
    if not leaderboard:
        raise HTTPException(status_code=404, detail="Leaderboard not found")
        
    # 2. Look up the max reward rank for this leaderboard
    max_reward_rank = db.query(func.max(models.GdLeaderboardReward.gd_leaderboard_reward_end_rank)).filter(
        models.GdLeaderboardReward.linked_gd_leaderboard == leaderboard.id
    ).scalar()
    
    if not max_reward_rank:
        max_reward_rank = 0
        
    # 3. Calculate the display limit
    display_limit = int(1.5 * max_reward_rank)
    
    # 4. Query ud_leaderboard_user for the top players
    top_users = db.query(models.UdLeaderboardUser).filter(
        models.UdLeaderboardUser.linked_gd_leaderboard == leaderboard.id
    ).order_by(
        models.UdLeaderboardUser.current_rank.asc()
    ).limit(display_limit).all()
    
    # Format the response
    results = []
    for user in top_users:
        user_name = "Unknown"
        if user.linked_ud_user_master:
            # Need to get user master name
            um = db.query(models.UdUserMaster).filter(models.UdUserMaster.id == user.linked_ud_user_master).first()
            if um:
                user_name = um.ud_user_master_display_name or um.ud_user_master_name
        elif user.linked_gd_bot_profile:
            # Assuming gd_bot_profile exists with this model format
            bot = db.query(models.GdBotProfile).filter(models.GdBotProfile.id == user.linked_gd_bot_profile).first()
            if bot:
                # Based on standard naming, gd_bot_profile_name
                try:
                    user_name = bot.gd_bot_profile_name
                except:
                    user_name = f"Bot #{bot.id}"
                
        results.append({
            "rank": user.current_rank,
            "name": user_name,
            "score": user.score,
            "is_bot": user.linked_gd_bot_profile is not None
        })
        
    return {
        "leaderboard_name": leaderboard.gd_leaderboard_name,
        "leaderboard_title": leaderboard.gd_leaderboard_title,
        "max_rewards_given": max_reward_rank,
        "display_limit": display_limit,
        "rankings": results
    }
