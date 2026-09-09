"""
PvP WebSocket Matchmaking
=========================
Handles real player vs real player matchmaking.
If no second human player joins within BOT_WAIT_SECONDS,
the server auto-spawns a Bot session as Player 2.

Message flow (Unity → Server):
  { "type": "bot_turn_request", ... }  → server runs bot_brain, streams actions back

Message flow (Server → Unity):
  { "type": "bot_action", "action": "...", "delay": 0.5, ... }
"""

import json
import uuid
import asyncio
import random
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
import models
from database import SessionLocal, get_db
from services.bot_brain import generate_bot_actions

router = APIRouter()

# ---- Telemetry helper -----------------------------------------------------
async def _record_match_telemetry(mode_id: str, p1_user_id: int = None, p2_user_id: int = None, is_vs_bot: bool = False):
    def _insert():
        try:
            db = SessionLocal()
            try:
                record = models.AnalysisPvPMatches(
                    mode_id=str(mode_id),
                    p1_user_id=p1_user_id,
                    p2_user_id=p2_user_id,
                    is_vs_bot=is_vs_bot
                )
                db.add(record)
                db.commit()
            finally:
                db.close()
        except Exception as e:
            print(f"[PvP-WS Telemetry] Error recording match: {e}")

    try:
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, _insert)
    except Exception as e:
        print(f"[PvP-WS Telemetry] Async task error: {e}")

# ---- Matchmaking state (in-memory) ----------------------------------------
# Maps mode_id -> waiting WebSocket
waiting_players: dict = {}
active_rooms: dict = {}

BOT_WAIT_SECONDS = 3   # Wait this long for a real opponent before spawning a bot


# ---- Match Room (real P1 vs real P2) --------------------------------------

class MatchRoom:
    def __init__(self, p1_ws: WebSocket, p2_ws: WebSocket):
        self.p1_ws = p1_ws
        self.p2_ws = p2_ws
        self.room_id = str(uuid.uuid4())

    async def relay(self, sender_ws: WebSocket, message: dict):
        target = self.p2_ws if sender_ws == self.p1_ws else self.p1_ws
        await target.send_json(message)


# ---- Bot Session (server acts as P2) --------------------------------------

class BotSession:
    """
    Maintains the bot's side of the match.
    Listens for bot_turn_request messages from the real player
    and streams back a human-like action sequence.
    """

    def __init__(self, real_player_ws: WebSocket, match_seed: int):
        self.real_player_ws = real_player_ws
        self.match_seed = match_seed
        random.seed(match_seed)

    async def handle_message(self, message: dict):
        """Called when the real player sends a message that needs a bot response."""
        if message.get("type") == "bot_turn_request":
            await self._respond_to_turn_request(message)

    async def _respond_to_turn_request(self, req: dict):
        """Run the bot brain and stream actions back to Unity."""
        try:
            print(f"BOT TURN REQUEST: {req}")
            actions = generate_bot_actions(
                stones_raw=req.get("stones", []),
                house_cx=req.get("house_center_x", 0.0),
                house_cz=req.get("house_center_z", 40.0),
                throw_start_z=req.get("throw_start_z", 2.0),
                rink_friction=req.get("rink_friction", 0.023),
                bot_rock_friction=req.get("bot_rock_friction", 0.023),
                bot_rock_curl_modifier=req.get("bot_rock_curl_modifier", 1.0),
                bot_rock_mass=req.get("bot_rock_mass", 20.0),
                bot_rock_radius=req.get("bot_rock_radius", 0.5),
                bot_rock_elasticity=req.get("bot_rock_elasticity", 0.85),
                curl_factor=req.get("curl_factor", 1.0),
                drift_variance=req.get("drift_variance", 0.05),
                perfect_release_probability=req.get("perfect_release_probability", 0.2),
                takeout_probability=req.get("takeout_probability", 0.5),
                guard_probability=req.get("guard_probability", 0.3),
                chances_left=req.get("chances_left", 3),
                max_power=req.get("max_power", 25.0),
                rink_width=req.get("rink_width", 4.75),
                house_radius=req.get("house_radius", 2.5),
                max_curl=req.get("max_curl", 15.0)
            )

            # Keep track of current state to stream complete aim payloads
            current_x = 0.0
            current_angle = 0.0
            current_curl = 0.0
            current_power = 0.0

            # Stream each action to Unity, waiting the specified delay between them
            for action_data in actions:
                delay = action_data.get("delay", 0.5)
                await asyncio.sleep(delay)

                act_type = action_data.get("action")
                if act_type == "intent_log":
                    strategy = action_data.get("strategy", "")
                    tx = action_data.get("target_x", 0.0)
                    tz = action_data.get("target_z", 0.0)
                    await self.real_player_ws.send_json({
                        "type": "bot_intent",
                        "message": f"{strategy},{tx},{tz}"
                    })
                    continue # No aim update for this
                elif act_type == "adjusting_position":
                    current_x = action_data.get("startX", 0.0)
                elif act_type == "set_curl":
                    current_curl = action_data.get("curl", 0.0)
                elif act_type == "set_power":
                    current_power = action_data.get("power", 0.0)
                elif act_type == "release":
                    current_x = action_data.get("startX", 0.0)
                    current_angle = action_data.get("angle", 0.0)
                    current_power = action_data.get("power", 0.0)
                    current_curl = action_data.get("curl", 0.0)

                    # Send final throw message (using 39 as a dummy rockId for the bot)
                    payload = f"{current_x},{current_angle},{current_power},{current_curl},39"
                    await self.real_player_ws.send_json({
                        "type": "throw",
                        "message": payload
                    })
                    return # End of turn

                # For all intermediate steps (including "hold"), send an aim update
                # Format: "phaseInt:X,Angle,Curl,Power"
                aim_payload = f"0:{current_x},{current_angle},{current_curl},{current_power}"
                await self.real_player_ws.send_json({
                    "type": "aim",
                    "message": aim_payload
                })

        except Exception as e:
            print(f"[BotSession] Error generating bot actions: {e}")


# ---- Main WebSocket endpoint -----------------------------------------------

@router.websocket("/ws/matchmaking")
async def websocket_endpoint(
    websocket: WebSocket,
    mode: str = "default",
    rock: int = 534,
    timeout: int = 3,
    userId: int = None,
    user_id: int = None
):
    global waiting_players, active_rooms

    await websocket.accept()
    wait_timeout = max(1, timeout) if timeout else BOT_WAIT_SECONDS
    eff_user_id = user_id if user_id is not None else userId

    # 1. Check if a human opponent is already waiting in this mode
    p1_entry = waiting_players.get(mode)
    if p1_entry is not None and p1_entry.get("ws") is not None:
        p1_ws = p1_entry["ws"]
        p1_rock = p1_entry["rock"]
        p1_event = p1_entry["event"]
        p1_uid = p1_entry.get("user_id")
        waiting_players[mode] = None

        room = MatchRoom(p1_ws, websocket)
        active_rooms[p1_ws] = room
        active_rooms[websocket] = room

        match_seed = random.randint(1000, 999999)
        # Randomize who is Player 1 (Red) and Player 2 (Blue)
        p1_id = 1 if random.choice([True, False]) else 2
        p2_id = 2 if p1_id == 1 else 1

        try:
            await p1_ws.send_json({
                "type": "match_start",
                "player_id": p1_id,
                "your_turn": (p1_id == 1),
                "match_seed": match_seed,
                "opponent_rock_id": rock,
                "is_vs_bot": False
            })
            await websocket.send_json({
                "type": "match_start",
                "player_id": p2_id,
                "your_turn": (p2_id == 1),
                "match_seed": match_seed,
                "opponent_rock_id": p1_rock,
                "is_vs_bot": False
            })
        except Exception as e:
            print(f"[PvP-WS] Error notifying players: {e}")

        # Record match in database asynchronously
        asyncio.create_task(_record_match_telemetry(mode_id=mode, p1_user_id=p1_uid, p2_user_id=eff_user_id, is_vs_bot=False))

        # Unblock Player 1's waiting task
        p1_event.set()

        # Handle Player 2 message relay
        try:
            while True:
                data = await websocket.receive_text()
                if websocket in active_rooms:
                    await active_rooms[websocket].relay(websocket, json.loads(data))
        except WebSocketDisconnect:
            _cleanup_room(websocket)
        return

    # 2. Player 1: Wait up to wait_timeout for a human opponent
    matched_event = asyncio.Event()
    waiting_players[mode] = {"ws": websocket, "rock": rock, "event": matched_event, "user_id": eff_user_id}
    
    try:
        await websocket.send_json({"type": "waiting", "message": f"Waiting for opponent in mode {mode}..."})
    except Exception:
        waiting_players[mode] = None
        return

    try:
        await asyncio.wait_for(matched_event.wait(), timeout=wait_timeout)
    except asyncio.TimeoutError:
        pass

    # 3. Check result after timeout
    if waiting_players.get(mode) and waiting_players[mode]["ws"] == websocket:
        # No human joined within timeout — spawn a bot match
        p1_uid = waiting_players[mode].get("user_id")
        waiting_players[mode] = None
        asyncio.create_task(_record_match_telemetry(mode_id=mode, p1_user_id=p1_uid, p2_user_id=None, is_vs_bot=True))
        await _run_bot_match(websocket)
    elif websocket in active_rooms:
        # A human joined! Run relay loop for Player 1
        try:
            while True:
                data = await websocket.receive_text()
                if websocket in active_rooms:
                    await active_rooms[websocket].relay(websocket, json.loads(data))
        except WebSocketDisconnect:
            _cleanup_room(websocket)


# ---- Helpers ----------------------------------------------------------------

async def _run_bot_match(p1_ws: WebSocket):
    """Run a full match where the server is Player 2 (the bot)."""
    match_seed = random.randint(1000, 999999)
    bot_session = BotSession(p1_ws, match_seed)

    try:
        await p1_ws.send_json({
            "type": "match_start",
            "player_id": 1,
            "your_turn": True,
            "match_seed": match_seed,
            "is_vs_bot": True,       # flag Unity so it knows it's a bot match
            "opponent_rock_id": 535
        })
    except Exception as e:
        print(f"[PvP-WS] Error sending match_start to player: {e}")
        return

    try:
        while True:
            data = await p1_ws.receive_text()
            message = json.loads(data)

            # If the player sends a bot_turn_request, handle it
            if message.get("type") == "bot_turn_request":
                # Run bot brain asynchronously so we don't block the receive loop
                asyncio.create_task(bot_session.handle_message(message))
            # All other messages (turn_swap, etc.) are noted but need no relay
    except WebSocketDisconnect:
        print(f"[PvP-WS] Bot match ended — player disconnected.")


def _cleanup_room(ws: WebSocket):
    if ws in active_rooms:
        room = active_rooms.pop(ws)
        other = room.p2_ws if room.p1_ws == ws else room.p1_ws
        if other in active_rooms:
            del active_rooms[other]
        asyncio.create_task(_notify_disconnect(other))


async def _notify_disconnect(ws: WebSocket):
    try:
        await ws.send_json({"type": "opponent_disconnected"})
    except Exception:
        pass


# ---- Analytics REST Endpoints -----------------------------------------------

@router.get("/api/admin/analytics/pvp")
def get_pvp_analytics(db: Session = Depends(get_db)):
    """
    Returns PvP mode rankings and match counts from analysis_pvp_matches table.
    """
    try:
        results = db.query(
            models.AnalysisPvPMatches.mode_id,
            func.count(models.AnalysisPvPMatches.id).label("total_matches"),
            func.sum(func.case((models.AnalysisPvPMatches.is_vs_bot == False, 1), else_=0)).label("human_matches"),
            func.sum(func.case((models.AnalysisPvPMatches.is_vs_bot == True, 1), else_=0)).label("bot_matches"),
            func.max(models.AnalysisPvPMatches.created_at).label("last_match_at")
        ).group_by(models.AnalysisPvPMatches.mode_id).order_by(func.count(models.AnalysisPvPMatches.id).desc()).all()

        return {
            "status": "ok",
            "pvp_mode_rankings": [
                {
                    "mode_id": r.mode_id,
                    "total_matches": int(r.total_matches),
                    "human_matches": int(r.human_matches or 0),
                    "bot_matches": int(r.bot_matches or 0),
                    "last_match_at": r.last_match_at.isoformat() if r.last_match_at else None
                }
                for r in results
            ]
        }
    except Exception as e:
        return {"status": "error", "message": str(e), "pvp_mode_rankings": []}
