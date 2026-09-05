import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db, SessionLocal
import models

router = APIRouter(
    prefix="/leaderboard",
    tags=["leaderboard"],
    responses={404: {"description": "Not found"}},
)

_last_sync_times: Dict[int, datetime] = {}

def sync_leaderboard_data(db: Session, leaderboard_id: Optional[int] = None):
    """
    Scans all user wallets in ud_user_wallet, extracts currency scores for active leaderboards,
    sorts descending, and upserts into ud_leaderboard_user.
    """
    now = datetime.utcnow()
    query = db.query(models.GdLeaderboard).filter(models.GdLeaderboard.is_enabled == True)
    if leaderboard_id is not None:
        query = query.filter(models.GdLeaderboard.id == leaderboard_id)
        
    leaderboards = query.all()
    
    for lb in leaderboards:
        # Check active time window
        if lb.gd_leaderboard_start_time and lb.gd_leaderboard_start_time > now:
            continue
        if lb.gd_leaderboard_end_time and lb.gd_leaderboard_end_time < now:
            continue
            
        # 1. Resolve tracked currency name
        curr_name = "gd_game_currency_star"
        if lb.linked_gd_currency:
            curr = db.query(models.GdGameCurrency).filter(models.GdGameCurrency.id == lb.linked_gd_currency).first()
            if curr and curr.gd_game_currency_name:
                curr_name = curr.gd_game_currency_name
        stripped_name = curr_name.replace("gd_game_currency_", "")
        
        # 2. Extract scores from all user wallets
        wallets = db.query(models.UdUserWallet).all()
        user_scores = []
        for w in wallets:
            if not w.linked_ud_user_master or not w.ud_user_wallet_currency_dictionary:
                continue
            try:
                dict_obj = w.ud_user_wallet_currency_dictionary
                curr_dict = json.loads(dict_obj) if isinstance(dict_obj, str) else dict_obj
                score = curr_dict.get(curr_name, 0)
                if score == 0:
                    score = curr_dict.get(stripped_name, 0)
                if score > 0:
                    user_scores.append({
                        "user_id": w.linked_ud_user_master,
                        "score": float(score)
                    })
            except Exception:
                continue
                
        # 3. Sort players by score descending
        user_scores.sort(key=lambda x: x["score"], reverse=True)
        
        # 4. Upsert into ud_leaderboard_user
        for rank_idx, item in enumerate(user_scores, start=1):
            u_id = item["user_id"]
            score = item["score"]
            existing = db.query(models.UdLeaderboardUser).filter(
                models.UdLeaderboardUser.linked_gd_leaderboard == lb.id,
                models.UdLeaderboardUser.linked_ud_user_master == u_id
            ).first()
            
            if existing:
                existing.score = score
                existing.current_rank = rank_idx
            else:
                new_row = models.UdLeaderboardUser(
                    linked_gd_leaderboard=lb.id,
                    linked_ud_user_master=u_id,
                    score=score,
                    current_rank=rank_idx
                )
                db.add(new_row)
                
        db.commit()
        _last_sync_times[lb.id] = now
        print(f"[{now}] Synced Leaderboard ID {lb.id} ('{lb.gd_leaderboard_name}') with {len(user_scores)} users.")

@router.get("/{gd_leaderboard_name}", response_model=Dict[str, Any])
def get_leaderboard(gd_leaderboard_name: str, db: Session = Depends(get_db)):
    # 1. Look up the leaderboard
    leaderboard = db.query(models.GdLeaderboard).filter(
        models.GdLeaderboard.gd_leaderboard_name == gd_leaderboard_name
    ).first()
    
    if not leaderboard:
        raise HTTPException(status_code=404, detail="Leaderboard not found")
        
    # Check if dynamic refresh is needed based on gd_leaderboard_refresh_mins
    refresh_mins = getattr(leaderboard, "gd_leaderboard_refresh_mins", 5) or 5
    last_sync = _last_sync_times.get(leaderboard.id)
    time_since_sync = (datetime.utcnow() - last_sync).total_seconds() if last_sync else 999999
    
    if time_since_sync >= (refresh_mins * 60):
        try:
            sync_leaderboard_data(db, leaderboard.id)
        except Exception as e:
            print(f"[Leaderboard] Error during dynamic refresh: {e}")
        
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
            um = db.query(models.UdUserMaster).filter(models.UdUserMaster.id == user.linked_ud_user_master).first()
            if um:
                user_name = um.ud_user_master_display_name or um.ud_user_master_name
        elif user.linked_gd_bot_profile:
            bot = db.query(models.GdBotProfile).filter(models.GdBotProfile.id == user.linked_gd_bot_profile).first()
            if bot:
                try:
                    user_name = bot.gd_bot_profile_name
                except:
                    user_name = f"Bot #{bot.id}"
                
        results.append({
            "user_id": user.linked_ud_user_master or 0,
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
