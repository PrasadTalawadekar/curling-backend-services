"""
FastAPI WebSocket Router for Real-Time PvP Matchmaking
======================================================
- Real-time 1v1 matchmaking with atomic concurrency lock
- Instant fallback to BotSession after BOT_WAIT_SECONDS
- Ping/Pong cellular heartbeat keep-alive
- Clean disconnection handling and room disposal
"""

import asyncio
import json
import random
import uuid
from typing import Dict, Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from services.bot_brain import generate_bot_actions

router = APIRouter()

# In-memory matchmaking & active rooms
waiting_players: Dict[str, Optional[dict]] = {}
active_rooms: Dict[WebSocket, "MatchRoom"] = {}
matchmaking_lock = asyncio.Lock()

BOT_WAIT_SECONDS = 3  # Wait this long for human opponent before spawning BotSession


class MatchRoom:
    def __init__(self, p1_ws: WebSocket, p2_ws: WebSocket):
        self.p1_ws = p1_ws
        self.p2_ws = p2_ws
        self.room_id = str(uuid.uuid4())

    async def relay(self, sender_ws: WebSocket, message: dict):
        target = self.p2_ws if sender_ws == self.p1_ws else self.p1_ws
        try:
            await target.send_json(message)
        except Exception:
            pass


class BotSession:
    def __init__(self, player_ws: WebSocket, match_seed: int):
        self.player_ws = player_ws
        self.match_seed = match_seed

    async def handle_message(self, message: dict):
        msg_type = message.get("type")
        if msg_type == "bot_turn_request":
            await self._execute_bot_turn(message)

    async def _execute_bot_turn(self, req: dict):
        try:
            stones_raw = req.get("stones", [])
            house_cx = float(req.get("house_cx", 0.0))
            house_cz = float(req.get("house_cz", 0.0))
            throw_start_z = float(req.get("throw_start_z", 0.0))
            rink_friction = float(req.get("rink_friction", 0.035))
            bot_rock_friction = float(req.get("bot_rock_friction", 0.011))
            bot_rock_curl_modifier = float(req.get("bot_rock_curl_modifier", 1.0))
            bot_rock_mass = float(req.get("bot_rock_mass", 20.0))
            bot_rock_radius = float(req.get("bot_rock_radius", 0.5))
            bot_rock_elasticity = float(req.get("bot_rock_elasticity", 0.85))
            curl_factor = float(req.get("curl_factor", 1.0))
            drift_variance = float(req.get("drift_variance", 0.02))
            perfect_release_prob = float(req.get("perfect_release_prob", 0.7))
            takeout_probability = float(req.get("takeout_probability", 0.6))
            guard_probability = float(req.get("guard_probability", 0.4))
            chances_left = int(req.get("chances_left", 3))

            actions = generate_bot_actions(
                stones_raw=stones_raw,
                house_cx=house_cx, house_cz=house_cz, throw_start_z=throw_start_z,
                rink_friction=rink_friction, bot_rock_friction=bot_rock_friction,
                bot_rock_curl_modifier=bot_rock_curl_modifier,
                bot_rock_mass=bot_rock_mass, bot_rock_radius=bot_rock_radius,
                bot_rock_elasticity=bot_rock_elasticity,
                curl_factor=curl_factor, drift_variance=drift_variance,
                perfect_release_probability=perfect_release_prob,
                takeout_probability=takeout_probability, guard_probability=guard_probability,
                chances_left=chances_left,
            )

            for action in actions:
                delay = action.get("delay", 0.0)
                if delay > 0:
                    await asyncio.sleep(delay)
                await self.player_ws.send_json(action)
        except Exception as e:
            print(f"[BotSession] Error generating bot actions: {e}")


@router.websocket("/ws/matchmaking")
async def websocket_endpoint(websocket: WebSocket, mode: str = "default", rock: int = 534):
    await websocket.accept()

    p1_data = None
    async with matchmaking_lock:
        if mode not in waiting_players or waiting_players[mode] is None:
            # Player 1 enters queue
            waiting_players[mode] = {"ws": websocket, "rock": rock}
            is_p1 = True
        else:
            # Player 2 pairs with Player 1
            p1_data = waiting_players[mode]
            waiting_players[mode] = None
            is_p1 = False

    if is_p1:
        await websocket.send_json({"type": "waiting", "message": f"Waiting for opponent in mode {mode}..."})

        # Wait up to BOT_WAIT_SECONDS for human player 2
        try:
            await asyncio.wait_for(_wait_for_opponent(websocket), timeout=BOT_WAIT_SECONDS)
        except asyncio.TimeoutError:
            pass

        async with matchmaking_lock:
            no_human = (waiting_players.get(mode) and waiting_players[mode]["ws"] == websocket)
            if no_human:
                waiting_players[mode] = None

        if no_human:
            # Fallback to intelligent bot match
            await _run_bot_match(websocket)
        elif websocket in active_rooms:
            # Human joined! Keep relaying messages
            try:
                while True:
                    data = await websocket.receive_text()
                    msg = json.loads(data)
                    if msg.get("type") == "ping":
                        await websocket.send_json({"type": "pong"})
                        continue
                    if websocket in active_rooms:
                        await active_rooms[websocket].relay(websocket, msg)
            except WebSocketDisconnect:
                _cleanup_room(websocket)

    else:
        # Player 2 joined human Player 1
        p1_ws = p1_data["ws"]
        p1_rock = p1_data["rock"]
        p2_ws = websocket
        p2_rock = rock

        room = MatchRoom(p1_ws, p2_ws)
        active_rooms[p1_ws] = room
        active_rooms[p2_ws] = room

        match_seed = random.randint(1000, 999999)
        p1_first = random.choice([True, False])
        p1_id = 1 if p1_first else 2
        p2_id = 2 if p1_first else 1

        await p1_ws.send_json({"type": "match_start", "player_id": p1_id, "your_turn": p1_first, "match_seed": match_seed, "opponent_rock_id": p2_rock})
        await p2_ws.send_json({"type": "match_start", "player_id": p2_id, "your_turn": not p1_first, "match_seed": match_seed, "opponent_rock_id": p1_rock})

        try:
            while True:
                data = await websocket.receive_text()
                msg = json.loads(data)
                if msg.get("type") == "ping":
                    await websocket.send_json({"type": "pong"})
                    continue
                if websocket in active_rooms:
                    await active_rooms[websocket].relay(websocket, msg)
        except WebSocketDisconnect:
            _cleanup_room(websocket)


async def _wait_for_opponent(p1_ws: WebSocket):
    while True:
        data = await p1_ws.receive_text()
        msg = json.loads(data)
        if msg.get("type") == "ping":
            await p1_ws.send_json({"type": "pong"})
            continue
        if p1_ws in active_rooms:
            await active_rooms[p1_ws].relay(p1_ws, msg)


async def _run_bot_match(p1_ws: WebSocket):
    match_seed = random.randint(1000, 999999)
    bot_session = BotSession(p1_ws, match_seed)

    await p1_ws.send_json({
        "type": "match_start",
        "player_id": 1,
        "your_turn": True,
        "match_seed": match_seed,
        "is_vs_bot": True
    })

    try:
        while True:
            data = await p1_ws.receive_text()
            message = json.loads(data)
            if message.get("type") == "ping":
                await p1_ws.send_json({"type": "pong"})
                continue
            if message.get("type") == "bot_turn_request":
                asyncio.create_task(bot_session.handle_message(message))
    except WebSocketDisconnect:
        pass


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
