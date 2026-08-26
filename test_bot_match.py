"""
Full Match Simulator
====================
Acts as a Unity client connecting to the live Render WebSocket server.
Simulates a complete curling match (8 turns each) against the backend bot.

Run:
    python test_bot_match.py
"""

import asyncio
import json
import websockets
import random
import sys

# Force UTF-8 output (handles Render cold-start logs cleanly on Windows)
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

WS_URL = "wss://curling-mobile-game.onrender.com/ws/matchmaking"

# Simulated rink constants (mirror Unity defaults)
HOUSE_CENTER_X  = 0.0
HOUSE_CENTER_Z  = 40.0
THROW_START_Z   = 2.0
RINK_WIDTH      = 4.4
RINK_FRICTION   = 0.023
CURL_FACTOR     = 1.2
BOT_FRICTION    = 0.023
BOT_CURL_MOD    = 1.0
DRIFT_VARIANCE  = 0.05
PERFECT_PROB    = 0.2
STONE_RADIUS    = 0.145

TURNS_PER_END   = 8   # Each side throws 8 stones per end (standard curling)

# ---- Helpers ----------------------------------------------------------------

def build_bot_turn_request(stones_on_ice: list) -> str:
    return json.dumps({
        "type":                        "bot_turn_request",
        "house_center_x":              HOUSE_CENTER_X,
        "house_center_z":              HOUSE_CENTER_Z,
        "throw_start_z":               THROW_START_Z,
        "rink_friction":               RINK_FRICTION,
        "bot_rock_friction":           BOT_FRICTION,
        "bot_rock_curl_modifier":      BOT_CURL_MOD,
        "curl_factor":                 CURL_FACTOR,
        "drift_variance":              DRIFT_VARIANCE,
        "perfect_release_probability": PERFECT_PROB,
        "stones":                      stones_on_ice,
    })


def simulate_player_throw(stones_on_ice: list) -> dict:
    """Fake a human throw: aim roughly at the house with some noise."""
    start_x = random.uniform(-1.5, 1.5)
    angle   = random.uniform(-3.0, 3.0)       # degrees off-centre
    power   = random.uniform(13.0, 17.0)
    curl    = random.choice([-7.5, 0.0, 7.5])

    # Compute approximate landing (very rough, just for log)
    import math
    land_x = start_x + math.sin(math.radians(angle)) * (power / 0.46)
    land_z = THROW_START_Z + math.cos(math.radians(angle)) * (power / 0.46)
    land_z = min(land_z, HOUSE_CENTER_Z + 5)  # clamp to rink

    landed = {"owner": "player", "x": round(land_x, 3), "z": round(land_z, 3)}
    stones_on_ice.append(landed)

    print(f"  [PLAYER] Threw -> landed at x={landed['x']:.2f}, z={landed['z']:.2f}")
    return landed


def apply_bot_release_to_board(stones_on_ice: list, action: dict):
    """Estimate where the bot stone lands and add it to the board."""
    import math
    sx    = action.get("startX", 0.0)
    angle = action.get("angle",  0.0)
    power = action.get("power",  14.0)

    land_x = sx + math.sin(math.radians(angle)) * (power / 0.46)
    land_z = THROW_START_Z + math.cos(math.radians(angle)) * (power / 0.46)
    land_z = min(land_z, HOUSE_CENTER_Z + 5)

    landed = {"owner": "bot", "x": round(land_x, 3), "z": round(land_z, 3)}
    stones_on_ice.append(landed)
    print(f"  [BOT]    Stone lands at x={landed['x']:.2f}, z={landed['z']:.2f}")


def score_end(stones_on_ice: list) -> tuple:
    """Count scoring stones (closest team holds all stones closer than opponent's nearest)."""
    player_stones = sorted(
        [s for s in stones_on_ice if s["owner"] == "player"],
        key=lambda s: (s["x"] - HOUSE_CENTER_X)**2 + (s["z"] - HOUSE_CENTER_Z)**2
    )
    bot_stones = sorted(
        [s for s in stones_on_ice if s["owner"] == "bot"],
        key=lambda s: (s["x"] - HOUSE_CENTER_X)**2 + (s["z"] - HOUSE_CENTER_Z)**2
    )

    HOUSE_R_SQ = 2.5 ** 2
    if not player_stones and not bot_stones:
        return 0, 0

    p_best_dist = (player_stones[0]["x"] - HOUSE_CENTER_X)**2 + (player_stones[0]["z"] - HOUSE_CENTER_Z)**2 if player_stones else float("inf")
    b_best_dist = (bot_stones[0]["x"]    - HOUSE_CENTER_X)**2 + (bot_stones[0]["z"]    - HOUSE_CENTER_Z)**2 if bot_stones    else float("inf")

    player_score = 0
    bot_score    = 0

    if p_best_dist < b_best_dist:
        # Player scores: count player stones closer than bot's nearest
        for s in player_stones:
            d = (s["x"] - HOUSE_CENTER_X)**2 + (s["z"] - HOUSE_CENTER_Z)**2
            if d <= HOUSE_R_SQ and d < b_best_dist:
                player_score += 1
    elif b_best_dist < p_best_dist:
        for s in bot_stones:
            d = (s["x"] - HOUSE_CENTER_X)**2 + (s["z"] - HOUSE_CENTER_Z)**2
            if d <= HOUSE_R_SQ and d < p_best_dist:
                bot_score += 1

    return player_score, bot_score


# ---- Main match loop --------------------------------------------------------

async def run_match():
    print("=" * 60)
    print("  CURLING MATCH SIMULATOR - Connecting to Render server")
    print("=" * 60)

    # Render free tier spins down after inactivity.
    # Retry connection up to 5 times with increasing wait.
    ws = None
    for attempt in range(1, 6):
        try:
            print(f"[CLIENT] Connection attempt {attempt}/5 ...")
            ws = await asyncio.wait_for(
                websockets.connect(WS_URL, open_timeout=30),
                timeout=35
            )
            print("[CLIENT] Connected!")
            break
        except Exception as e:
            print(f"[CLIENT] Attempt {attempt} failed: {e}")
            if attempt < 5:
                wait = attempt * 5
                print(f"[CLIENT] Render may be waking up. Retrying in {wait}s...")
                await asyncio.sleep(wait)
            else:
                print("[CLIENT] Could not connect after 5 attempts. Is Render deployed?")
                return

    async with ws:
        # --- Step 1: Wait for match_start (server spawns bot after 5s) ---
        print("\n[CLIENT] Connected. Waiting for match_start...")
        while True:
            raw = await ws.recv()
            msg = json.loads(raw)
            print(f"[SERVER] {msg}")
            if msg.get("type") == "waiting":
                print("[CLIENT] Server acknowledged — waiting 5s for bot auto-spawn...")
            if msg.get("type") == "match_start":
                match_seed  = msg.get("match_seed", 0)
                is_vs_bot   = msg.get("is_vs_bot", False)
                my_turn     = msg.get("your_turn", True)
                print(f"\n[CLIENT] MATCH START! Seed={match_seed}  VsBot={is_vs_bot}  MyTurn={my_turn}")
                break

        # --- Step 2: Simulate turns ---
        stones_on_ice  = []
        player_total   = 0
        bot_total      = 0
        turn_num       = 0
        max_turns      = TURNS_PER_END * 2   # 8 player + 8 bot throws

        while turn_num < max_turns:
            # ---- PLAYER TURN ----
            if my_turn:
                turn_num += 1
                print(f"\n--- TURN {turn_num} | PLAYER ---")
                simulate_player_throw(stones_on_ice)
                print(f"  Stones on ice: {len(stones_on_ice)}")

                # Tell server turn is done
                await ws.send(json.dumps({"type": "turn_swap", "player_id": 2}))
                my_turn = False

            # ---- BOT TURN ----
            else:
                turn_num += 1
                print(f"\n--- TURN {turn_num} | BOT ---")
                print(f"  [CLIENT] Sending bot_turn_request with {len(stones_on_ice)} stones on ice...")
                await ws.send(build_bot_turn_request(stones_on_ice))

                # Receive the action sequence from the server
                bot_released = False
                timeout_count = 0
                while not bot_released:
                    try:
                        raw = await asyncio.wait_for(ws.recv(), timeout=15.0)
                        action_msg = json.loads(raw)
                        atype = action_msg.get("type", "")

                        if atype == "bot_action":
                            action = action_msg.get("action", "")
                            delay  = action_msg.get("delay", 0)
                            print(f"  [SERVER→BOT] action={action:25s} delay={delay:.2f}s", end="")

                            if action == "adjusting_position":
                                print(f"  startX={action_msg.get('startX')}")
                            elif action == "set_curl":
                                print(f"  curl={action_msg.get('curl')}")
                            elif action == "set_power":
                                print(f"  power={action_msg.get('power')}")
                            elif action == "release":
                                print(f"  → startX={action_msg.get('startX')} angle={action_msg.get('angle')} power={action_msg.get('power')} curl={action_msg.get('curl')}")
                                apply_bot_release_to_board(stones_on_ice, action_msg)
                                bot_released = True
                            else:
                                print()

                        elif atype == "opponent_disconnected":
                            print("[SERVER] Opponent disconnected!")
                            return
                    except asyncio.TimeoutError:
                        timeout_count += 1
                        print(f"  [CLIENT] Waiting for bot... ({timeout_count})")
                        if timeout_count > 3:
                            print("  [CLIENT] Bot timed out! Ending match.")
                            return

                my_turn = True   # Back to player

            # After every full round (player + bot), show scoreboard
            if turn_num % 2 == 0:
                ps, bs = score_end(stones_on_ice)
                print(f"  [SCORE] After turn {turn_num}: Player={ps}  Bot={bs}")

        # --- Step 3: Final score ---
        print("\n" + "=" * 60)
        print("  MATCH COMPLETE")
        print("=" * 60)
        ps, bs = score_end(stones_on_ice)
        player_total += ps
        bot_total    += bs
        print(f"  Final Score → Player: {player_total}  Bot: {bot_total}")
        if player_total > bot_total:
            print("  ** PLAYER WINS! **")
        elif bot_total > player_total:
            print("  ** BOT WINS! **")
        else:
            print("  ** TIE! **")
        print("=" * 60)
        print(f"\n  Total stones on ice: {len(stones_on_ice)}")
        for s in stones_on_ice:
            dist = ((s['x'] - HOUSE_CENTER_X)**2 + (s['z'] - HOUSE_CENTER_Z)**2) ** 0.5
            print(f"  {s['owner']:8s}  x={s['x']:6.2f}  z={s['z']:6.2f}  dist_from_button={dist:.2f}m")


# ---- Entry point ------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(run_match())
