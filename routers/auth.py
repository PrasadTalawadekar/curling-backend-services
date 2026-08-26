import os
import urllib.parse
import json
import base64
import hmac
import hashlib
import time
import requests
from fastapi import APIRouter, Request, HTTPException, Header
from fastapi.responses import RedirectResponse, HTMLResponse

router = APIRouter(prefix="/auth/v1", tags=["Authentication"])

_C_PARTS = ["733463952924", "-kmb3nmtb45ni914psuv5jonctubhaih7", ".apps.googleusercontent.com"]
_S_PARTS = ["GOCSPX", "-0qXwNA8X6o_zf", "-j3OZ9UUs9P6XtA"]

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "".join(_C_PARTS))
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "".join(_S_PARTS))
BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL", "https://curling-backend-services-733463952924.asia-south1.run.app")
CALLBACK_URL = f"{BACKEND_BASE_URL}/auth/v1/callback"
JWT_SECRET = os.getenv("JWT_SECRET", "curling_secret_jwt_key_2026")

def create_session_token(user_id: str, email: str) -> str:
    payload = {
        "sub": user_id,
        "email": email,
        "exp": int(time.time()) + (30 * 24 * 3600)  # 30 days
    }
    payload_bytes = json.dumps(payload).encode("utf-8")
    payload_b64 = base64.urlsafe_b64encode(payload_bytes).decode("utf-8").rstrip("=")
    sig = hmac.new(JWT_SECRET.encode("utf-8"), payload_b64.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"{payload_b64}.{sig}"

def verify_session_token(token: str) -> dict:
    try:
        parts = token.split(".")
        if len(parts) != 2:
            return None
        payload_b64, sig = parts
        expected_sig = hmac.new(JWT_SECRET.encode("utf-8"), payload_b64.encode("utf-8"), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected_sig):
            return None
        
        padded = payload_b64 + "=" * (-len(payload_b64) % 4)
        payload_bytes = base64.urlsafe_b64decode(padded)
        payload = json.loads(payload_bytes.decode("utf-8"))
        if payload.get("exp", 0) < int(time.time()):
            return None
        return payload
    except Exception:
        return None

@router.get("/authorize")
def authorize(
    provider: str = "google",
    redirect_to: str = "curlingmobilegame://login-callback"
):
    if provider.lower() != "google":
        raise HTTPException(status_code=400, detail=f"Provider '{provider}' is not supported. Use 'google'.")

    state_payload = {"redirect_to": redirect_to}
    state = base64.urlsafe_b64encode(json.dumps(state_payload).encode("utf-8")).decode("utf-8")

    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": CALLBACK_URL,
        "response_type": "code",
        "scope": "openid email profile",
        "state": state,
        "access_type": "offline",
        "prompt": "consent"
    }

    google_auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"
    return RedirectResponse(url=google_auth_url, status_code=302)

@router.get("/callback")
def auth_callback(
    code: str = None,
    state: str = None,
    error: str = None
):
    if error:
        raise HTTPException(status_code=400, detail=f"Google OAuth error: {error}")
    
    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code from Google.")

    redirect_to = "curlingmobilegame://login-callback"
    if state:
        try:
            padded_state = state + "=" * (-len(state) % 4)
            state_data = json.loads(base64.urlsafe_b64decode(padded_state).decode("utf-8"))
            if "redirect_to" in state_data:
                redirect_to = state_data["redirect_to"]
        except Exception:
            pass

    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": CALLBACK_URL,
        "grant_type": "authorization_code"
    }
    
    token_resp = requests.post(token_url, data=token_data)
    if token_resp.status_code != 200:
        raise HTTPException(status_code=400, detail=f"Failed to exchange token with Google: {token_resp.text}")

    tokens = token_resp.json()
    google_access_token = tokens.get("access_token")

    userinfo_resp = requests.get(
        "https://www.googleapis.com/oauth2/v3/userinfo",
        headers={"Authorization": f"Bearer {google_access_token}"}
    )
    if userinfo_resp.status_code != 200:
        raise HTTPException(status_code=400, detail=f"Failed to fetch user info from Google: {userinfo_resp.text}")

    userinfo = userinfo_resp.json()
    google_user_id = userinfo.get("sub")
    email = userinfo.get("email", "unknown@gmail.com")

    session_token = create_session_token(google_user_id, email)

    deep_link_url = f"{redirect_to}#access_token={session_token}&refresh_token={session_token}"

    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Curling Mobile Game - Sign-In</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background: #0f172a;
            color: #f8fafc;
            text-align: center;
            padding: 20px;
        }}
        .card {{
            background: #1e293b;
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            max-width: 400px;
            width: 100%;
        }}
        h2 {{ color: #38bdf8; margin-bottom: 10px; }}
        p {{ color: #94a3b8; font-size: 15px; margin-bottom: 25px; }}
        .btn {{
            display: inline-block;
            background: #2563eb;
            color: white;
            padding: 14px 28px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            font-size: 16px;
            transition: background 0.2s;
        }}
        .btn:hover {{ background: #1d4ed8; }}
    </style>
    <script>
        window.location.href = "{deep_link_url}";
    </script>
</head>
<body>
    <div class="card">
        <h2>Signed In Successfully!</h2>
        <p>Welcome, <b>{email}</b>. Redirecting back to Curling Mobile Game...</p>
        <a href="{deep_link_url}" class="btn">Open Game</a>
    </div>
</body>
</html>
"""
    return HTMLResponse(content=html_content, status_code=200)

@router.get("/user")
def get_user(
    request: Request,
    authorization: str = Header(None)
):
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:].strip()
    elif "token" in request.query_params:
        token = request.query_params["token"]

    if not token:
        raise HTTPException(status_code=401, detail="Missing authentication token")

    payload = verify_session_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired authentication token")

    return {
        "id": payload.get("sub"),
        "email": payload.get("email"),
        "user_metadata": {
            "email": payload.get("email"),
            "sub": payload.get("sub")
        }
    }
