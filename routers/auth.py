import os
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "733463952924-8ssq5p8hjll3os97f37niu58t3e54lua.apps.googleusercontent.com")

class GoogleAuthRequest(BaseModel):
    id_token: str
    display_name: str = ""

@router.post("/google")
def authenticate_google_user(req: GoogleAuthRequest, db: Session = Depends(get_db)):
    """
    Verify Google OAuth Token and return or create user profile.
    """
    try:
        from google.oauth2 import id_token
        from google.auth.transport import requests

        # Verify Google ID Token
        idinfo = id_token.verify_oauth2_token(req.id_token, requests.Request(), GOOGLE_CLIENT_ID)
        google_id = idinfo["sub"]
        email = idinfo.get("email", "")
        name = req.display_name or idinfo.get("name", f"Player_{google_id[:6]}")
    except Exception as e:
        # If token verification fails, return 401
        raise HTTPException(status_code=401, detail=f"Invalid Google Token: {str(e)}")

    # Check if user already exists
    user = db.query(models.UdUserMaster).filter(models.UdUserMaster.ud_user_master_gmail_id == google_id).first()
    if not user:
        from routers.users import generate_unique_user_id
        new_id = generate_unique_user_id(db)
        user = models.UdUserMaster(
            id=new_id,
            auth_id=google_id,
            ud_user_master_name=name,
            ud_user_master_display_name=name,
            is_ud_user_master_gmail=True,
            ud_user_master_gmail_id=google_id,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        # Create initial wallet & stats record
        wallet = models.UdUserWallet(
            linked_ud_user_master=user.id,
            ud_user_wallet_currency_dictionary={"coins": 500, "gems": 10}
        )
        db.add(wallet)

        stats = models.UdUserStats(linked_ud_user_master=user.id)
        db.add(stats)
        db.commit()

    return {
        "status": "success",
        "user_id": user.id,
        "display_name": user.ud_user_master_display_name,
        "email": email,
    }
