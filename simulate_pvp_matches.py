"""
PvP Real-Time Matchmaking & 50-Match Physics Simulator
======================================================
Runs 50 simultaneous PvP matches (100 WebSocket clients) in parallel,
simulates full 2D continuous physics and elastic collisions locally,
detects anomalies, and renders visual ASCII rock maps for every match.

Usage:
    python simulate_pvp_matches.py --matches 50 --url wss://curling-mobile-game.onrender.com/ws/matchmaking
    python simulate_pvp_matches.py --matches 10 --url ws://localhost:8000/ws/matchmaking --visualize
"""

import asyncio
import json
import math
import random
import sys
import time
import argparse
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    import websockets
except ImportError:
    print("Error: 'websockets' library is required. Install via: pip install websockets")
    sys.exit(1)

# Physics constants matching game
GRAVITY = 9.81
DT = 0.02
DEFAULT_ROCK_RADIUS = 0.5
DEFAULT_ROCK_MASS = 20.0
DEFAULT_ELASTICITY = 0.85
RINK_WIDTH = 4.75
DEFAULT_HOUSE_CX = 0.0
DEFAULT_HOUSE_CZ = 40.0
THROW_START_Z = 2.0


@dataclass
class Stone:
    id: int
    owner: str  # "P1" or "P2"
    x: float
    z: float
    vx: float = 0.0
    vz: float = 0.0
    mass: float = DEFAULT_ROCK_MASS
    radius: float = DEFAULT_ROCK_RADIUS
    elasticity: float = DEFAULT_ELASTICITY
    friction: float = 0.0001
    curl: float = 0.0
    curl_modifier: float = 1.0
    surf_factor: float = 1.0
    is_moving: bool = False
    is_out_of_bounds: bool = False


@dataclass
class AnomalyReport:
    match_id: int
    anomalies: List[str] = field(default_factory=list)

    def add(self, code: str, detail: str):
        self.anomalies.append(f"[{code}] {detail}")


@dataclass
class MatchResult:
    match_id: int
    seed: int
    p1_stones: List[Stone]
    p2_stones: List[Stone]
    winner: str  # "P1", "P2", "Draw"
    closest_distance: float
    p1_score: int
    p2_score: int
    total_collisions: int
    duration_sec: float
    anomalies: List[str]


# ---------------------------------------------------------------------------
# Physics Simulation Engine (Exact Game Kinematics)
# ---------------------------------------------------------------------------

class PhysicsWorld:
    def __init__(self, rink_width: float = RINK_WIDTH, max_z: float = 50.0):
        self.rink_width = rink_width
        self.max_z = max_z
        self.stones: List[Stone] = []
        self.collision_count = 0

    def add_stone(self, stone: Stone):
        self.stones.append(stone)

    def step(self) -> bool:
        """Runs 1 physics tick (0.02s). Returns True if any stone is still moving."""
        any_moving = False
        active_stones = [s for s in self.stones if not s.is_out_of_bounds]

        # 1. Update velocities and positions
        for s in active_stones:
            if not s.is_moving:
                continue

            speed = math.hypot(s.vx, s.vz)
            if speed < 0.02:
                s.vx = 0.0
                s.vz = 0.0
                s.is_moving = False
                continue

            any_moving = True

            # Deceleration
            decel = s.mass * s.friction * GRAVITY
            new_speed = max(0.0, speed - decel * DT)

            if new_speed <= 0.0001:
                s.vx = 0.0
                s.vz = 0.0
                s.is_moving = False
                continue

            # Direction unit vector
            dir_x = s.vx / speed
            dir_z = s.vz / speed

            # Curl angular rotation
            effective_curl = s.curl * s.curl_modifier * s.surf_factor
            d_theta = 2.0 * effective_curl * math.radians(1.0) * new_speed * DT
            cos_t = math.cos(-d_theta)
            sin_t = math.sin(-d_theta)
            rot_x = dir_x * cos_t - dir_z * sin_t
            rot_z = dir_x * sin_t + dir_z * cos_t

            s.vx = rot_x * new_speed
            s.vz = rot_z * new_speed

            s.x += s.vx * DT
            s.z += s.vz * DT

            # Boundary checks
            if abs(s.x) > self.rink_width / 2.0 or s.z > self.max_z or s.z < -5.0:
                s.is_out_of_bounds = True
                s.is_moving = False
                s.vx = 0.0
                s.vz = 0.0

        # 2. Collision resolution (stone to stone)
        for i in range(len(active_stones)):
            s1 = active_stones[i]
            if s1.is_out_of_bounds:
                continue

            for j in range(i + 1, len(active_stones)):
                s2 = active_stones[j]
                if s2.is_out_of_bounds:
                    continue

                dx = s2.x - s1.x
                dz = s2.z - s1.z
                dist_sq = dx * dx + dz * dz
                min_dist = s1.radius + s2.radius

                if dist_sq < min_dist * min_dist and dist_sq > 0.000001:
                    dist = math.sqrt(dist_sq)
                    nx = dx / dist
                    nz = dz / dist

                    # Relative velocity along normal
                    rel_vx = s1.vx - s2.vx
                    rel_vz = s1.vz - s2.vz
                    vn = rel_vx * nx + rel_vz * nz

                    if vn > 0:  # Moving towards each other
                        self.collision_count += 1
                        rebound = min(s1.elasticity, s2.elasticity)
                        impulse = -(1.0 + rebound) * vn / (1.0 / s1.mass + 1.0 / s2.mass)

                        s1.vx += (impulse / s1.mass) * nx
                        s1.vz += (impulse / s1.mass) * nz
                        s2.vx -= (impulse / s2.mass) * nx
                        s2.vz -= (impulse / s2.mass) * nz

                        s1.is_moving = True
                        s2.is_moving = True

                        # Overlap separation
                        overlap = 0.5 * (min_dist - dist)
                        s1.x -= nx * overlap
                        s1.z -= nz * overlap
                        s2.x += nx * overlap
                        s2.z += nz * overlap

        return any_moving

    def run_until_stopped(self, max_ticks: int = 2500):
        for _ in range(max_ticks):
            if not self.step():
                break


# ---------------------------------------------------------------------------
# Bot AI Shot Calculator
# ---------------------------------------------------------------------------

def calculate_bot_shot(house_cx: float, house_cz: float, stones_on_ice: List[Stone], my_team: str, strategy: str = "draw") -> Tuple[float, float, float, float]:
    """Generates realistic curling shot parameters (startX, angle_deg, power, curl)."""
    dist_to_house = house_cz - THROW_START_Z
    
    # Calculate base velocity needed for distance: v = sqrt(2 * a * d)
    decel = DEFAULT_ROCK_MASS * 0.0001 * GRAVITY
    ideal_speed = math.sqrt(2.0 * decel * dist_to_house)

    if strategy == "takeout":
        # Target opponent stone closest to button
        opp_stones = [s for s in stones_on_ice if s.owner != my_team and not s.is_out_of_bounds]
        if opp_stones:
            target = min(opp_stones, key=lambda s: math.hypot(s.x - house_cx, s.z - house_cz))
            dx = target.x - 0.0
            dz = target.z - THROW_START_Z
            angle_deg = math.degrees(math.atan2(dx, dz))
            takeout_speed = ideal_speed * 1.35
            return (0.0, angle_deg, takeout_speed, 0.0)

    # Standard Draw / Guard
    lateral_target_x = house_cx + random.uniform(-0.8, 0.8)
    dx = lateral_target_x - 0.0
    dz = dist_to_house
    angle_deg = math.degrees(math.atan2(dx, dz))
    curl = random.choice([-2.0, 0.0, 2.0])
    power = ideal_speed * random.uniform(0.98, 1.02)
    start_x = random.uniform(-0.15, 0.15)
    return (start_x, angle_deg, power, curl)


async def recv_json(ws, target_types: Optional[List[str]] = None, timeout: float = 6.0) -> dict:
    """Reads JSON from WebSocket, skipping background status messages like 'waiting'."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        remaining = max(0.1, deadline - time.time())
        raw = await asyncio.wait_for(ws.recv(), timeout=remaining)
        data = json.loads(raw)
        m_type = data.get("type")
        if m_type == "waiting" and (target_types is None or "waiting" not in target_types):
            continue
        if target_types is None or m_type in target_types:
            return data
    raise asyncio.TimeoutError(f"Timed out waiting for message types: {target_types}")


# ---------------------------------------------------------------------------
# Virtual PvP Match Runner (Async WebSockets)
# ---------------------------------------------------------------------------

async def run_single_match(match_index: int, server_url: str, pvp_mode: str, chances_per_user: int = 3) -> MatchResult:
    """Simulates 1 complete match between two WebSocket clients (P1 & P2)."""
    start_time = time.time()
    anomalies = []
    
    p1_ws = None
    p2_ws = None
    p1_stones: List[Stone] = []
    p2_stones: List[Stone] = []
    
    # Use dedicated mode room key per simulated pair to ensure clean 1v1 pairing
    room_mode = f"{pvp_mode}_{match_index}"
    p1_url = f"{server_url}?mode={room_mode}&rock=534"
    p2_url = f"{server_url}?mode={room_mode}&rock=535"

    world = PhysicsWorld()
    match_seed = 0

    try:
        # 1. Connect Player 1
        p1_ws = await websockets.connect(p1_url, open_timeout=8.0, close_timeout=2.0)
        # Small delay before P2 joins so P1 enters matchmaking queue first
        await asyncio.sleep(0.15)
        # 2. Connect Player 2 (Will match with Player 1)
        p2_ws = await websockets.connect(p2_url, open_timeout=8.0, close_timeout=2.0)

        # Receive match_start from both (handling any preceding 'waiting' messages)
        msg1 = await recv_json(p1_ws, ["match_start"], timeout=8.0)
        msg2 = await recv_json(p2_ws, ["match_start"], timeout=8.0)

        match_seed = msg1.get("match_seed", random.randint(1000, 9999))
        random.seed(match_seed + match_index)

        # Total stones in match
        total_throws = chances_per_user * 2
        current_turn_p1 = msg1.get("your_turn", True)

        for throw_num in range(total_throws):
            current_team = "P1" if current_turn_p1 else "P2"
            active_ws = p1_ws if current_turn_p1 else p2_ws
            passive_ws = p2_ws if current_turn_p1 else p1_ws

            # Strategy selection
            strategy = "takeout" if (throw_num >= 3 and random.random() < 0.4) else "draw"
            startX, angle, power, curl = calculate_bot_shot(DEFAULT_HOUSE_CX, DEFAULT_HOUSE_CZ, world.stones, current_team, strategy)

            # Send aim & throw message over websocket
            throw_msg = {
                "type": "throw",
                "player_id": 1 if current_turn_p1 else 2,
                "startX": startX,
                "angle": angle,
                "power": power,
                "curl": curl
            }
            await active_ws.send(json.dumps(throw_msg))

            # Passive player receives the throw
            recv_msg = await recv_json(passive_ws, ["throw"], timeout=4.0)

            # Spawn stone in local physics engine
            rad = math.radians(angle)
            vx = math.sin(rad) * power
            vz = math.cos(rad) * power

            stone = Stone(
                id=throw_num + 1,
                owner=current_team,
                x=startX,
                z=THROW_START_Z,
                vx=vx,
                vz=vz,
                curl=curl,
                is_moving=True
            )
            world.add_stone(stone)

            if current_team == "P1":
                p1_stones.append(stone)
            else:
                p2_stones.append(stone)

            # Simulate physics until stone and all chain collisions stop
            world.run_until_stopped()

            # Swap turn
            current_turn_p1 = not current_turn_p1
            swap_msg = {"type": "turn_swap", "player_id": 1 if current_turn_p1 else 2}
            await active_ws.send(json.dumps(swap_msg))
            _ = await recv_json(passive_ws, ["turn_swap"], timeout=4.0)

    except asyncio.TimeoutError:
        anomalies.append("[TIMEOUT] WebSocket response timed out during matchmaking or throw sequence.")
    except Exception as e:
        anomalies.append(f"[EXCEPTION] Match error: {type(e).__name__}: {str(e)}")
    finally:
        if p1_ws:
            try: await p1_ws.close()
            except: pass
        if p2_ws:
            try: await p2_ws.close()
            except: pass

    # -----------------------------------------------------------------------
    # Post-Match Anomaly Detection & Scoring
    # -----------------------------------------------------------------------
    active_stones = [s for s in world.stones if not s.is_out_of_bounds]

    # Check for NaN / Inf anomalies
    for s in world.stones:
        if math.isnan(s.x) or math.isnan(s.z) or math.isinf(s.x) or math.isinf(s.z):
            anomalies.append(f"[NAN_CORRUPTION] Stone {s.id} ({s.owner}) has invalid coordinates: X={s.x}, Z={s.z}")

    # Check for overlapping stopped stones
    for i in range(len(active_stones)):
        for j in range(i + 1, len(active_stones)):
            s1, s2 = active_stones[i], active_stones[j]
            dist = math.hypot(s1.x - s2.x, s1.z - s2.z)
            if dist < (s1.radius + s2.radius - 0.05):
                anomalies.append(f"[COLLISION_OVERLAP] Stones {s1.id} and {s2.id} overlapping: distance={dist:.3f}m < {s1.radius+s2.radius}m")

    # Score calculation
    p1_score = 0
    p2_score = 0
    winner = "Draw"
    closest_dist = float("inf")

    if active_stones:
        stones_with_dist = [(s, math.hypot(s.x - DEFAULT_HOUSE_CX, s.z - DEFAULT_HOUSE_CZ)) for s in active_stones]
        stones_with_dist.sort(key=lambda item: item[1])

        closest_stone, closest_dist = stones_with_dist[0]
        winner = closest_stone.owner

        # Count how many stones of the winning team are closer than the best opponent stone
        opp_team = "P2" if winner == "P1" else "P1"
        opp_dists = [d for s, d in stones_with_dist if s.owner == opp_team]
        cutoff = opp_dists[0] if opp_dists else float("inf")

        for s, d in stones_with_dist:
            if s.owner == winner and d < cutoff and d <= 2.5:  # Within house
                if winner == "P1": p1_score += 1
                else: p2_score += 1

    duration = time.time() - start_time
    return MatchResult(
        match_id=match_index + 1,
        seed=match_seed,
        p1_stones=p1_stones,
        p2_stones=p2_stones,
        winner=winner,
        closest_distance=closest_dist if closest_dist != float("inf") else 0.0,
        p1_score=p1_score,
        p2_score=p2_score,
        total_collisions=world.collision_count,
        duration_sec=duration,
        anomalies=anomalies
    )


# ---------------------------------------------------------------------------
# ASCII 2D Rock Map Visualizer
# ---------------------------------------------------------------------------

def render_ascii_rock_map(res: MatchResult, rink_width: float = 4.0, z_range: float = 4.0) -> str:
    """Renders a 2D top-down ASCII map of the Curling House and stones."""
    grid_w, grid_h = 41, 21
    grid = [[" " for _ in range(grid_w)] for _ in range(grid_h)]

    cx, cz = DEFAULT_HOUSE_CX, DEFAULT_HOUSE_CZ
    x_min, x_max = cx - rink_width / 2.0, cx + rink_width / 2.0
    z_min, z_max = cz - z_range / 2.0, cz + z_range / 2.0

    def to_grid(x: float, z: float) -> Tuple[int, int]:
        gx = int((x - x_min) / (x_max - x_min) * (grid_w - 1))
        gz = int((z - z_min) / (z_max - z_min) * (grid_h - 1))
        return (max(0, min(grid_w - 1, gx)), max(0, min(grid_h - 1, gz)))

    # Draw house boundary circles
    for gy in range(grid_h):
        for gx in range(grid_w):
            rx = x_min + (gx / (grid_w - 1)) * (x_max - x_min)
            rz = z_min + (gy / (grid_h - 1)) * (z_max - z_min)
            d = math.hypot(rx - cx, rz - cz)

            if abs(d - 1.83) < 0.08:  # 12-foot ring
                grid[gy][gx] = "."
            elif abs(d - 1.22) < 0.08:  # 8-foot ring
                grid[gy][gx] = ":"
            elif abs(d - 0.61) < 0.08:  # 4-foot ring
                grid[gy][gx] = "="
            elif d < 0.18:  # Button center
                grid[gy][gx] = "+"

    # Plot Stones
    for s in res.p1_stones:
        if not s.is_out_of_bounds:
            gx, gz = to_grid(s.x, s.z)
            grid[gz][gx] = "Y"  # Yellow / P1

    for s in res.p2_stones:
        if not s.is_out_of_bounds:
            gx, gz = to_grid(s.x, s.z)
            grid[gz][gx] = "R"  # Red / P2

    header = f"+--- MATCH #{res.match_id:02d} ROCK MAP (Y=Player 1, R=Player 2, +=Button) ---+\n"
    lines = [header]
    for row in reversed(grid):
        lines.append("| " + "".join(row) + " |\n")
    lines.append("+------------------------------------------------------------+\n")
    return "".join(lines)


# ---------------------------------------------------------------------------
# Master Runner (Concurrent Matches with Concurrency Pool)
# ---------------------------------------------------------------------------

async def run_guarded_match(sem: asyncio.Semaphore, match_idx: int, url: str, mode: str, total: int, results_list: list):
    async with sem:
        res = await run_single_match(match_idx, url, mode)
        results_list.append(res)
        done = len(results_list)
        if done % 25 == 0 or done == total:
            print(f"  -> Progress: {done}/{total} matches completed ({(done/total)*100:.1f}%)")
        return res

async def main():
    parser = argparse.ArgumentParser(description="Real-Time PvP Simulation Load Tester")
    parser.add_argument("--matches", type=int, default=50, help="Total number of matches to simulate (default: 50)")
    parser.add_argument("--concurrency", type=int, default=25, help="Max simultaneous active matches (default: 25)")
    parser.add_argument("--url", type=str, default="wss://curling-backend-pvp-733463952924.asia-south1.run.app/ws/matchmaking", help="WebSocket URL")
    parser.add_argument("--mode", type=str, default="1", help="PvP Mode ID")
    parser.add_argument("--visualize", action="store_true", help="Print ASCII rock map for all matches")
    args = parser.parse_args()

    print("=" * 75)
    print(f"  CURLING MOBILE GAME -- REAL-TIME MATCH LOAD TESTER")
    print(f"  Target Server   : {args.url}")
    print(f"  Total Matches   : {args.matches} matches ({args.matches * 2} WebSockets)")
    print(f"  Concurrency Pool: {args.concurrency} simultaneous matches ({args.concurrency * 2} active sockets)")
    print("=" * 75)
    print("\n[Matchmaker] Launching simulation worker pool...")

    start_all = time.time()
    sem = asyncio.Semaphore(args.concurrency)
    results: List[MatchResult] = []
    
    tasks = [run_guarded_match(sem, i, args.url, args.mode, args.matches, results) for i in range(args.matches)]
    await asyncio.gather(*tasks)
    total_time = time.time() - start_all

    # Sort results by match_id for display
    results.sort(key=lambda r: r.match_id)

    # -----------------------------------------------------------------------
    # Summary & Anomaly Reporting
    # -----------------------------------------------------------------------
    p1_wins = sum(1 for r in results if r.winner == "P1")
    p2_wins = sum(1 for r in results if r.winner == "P2")
    draws   = sum(1 for r in results if r.winner == "Draw")
    total_anomalies = sum(len(r.anomalies) for r in results)

    print("\n" + "=" * 75)
    print(f"  BATCH SIMULATION RESULTS ({args.matches} MATCHES COMPLETED IN {total_time:.2f}s)")
    print("=" * 75)
    print(f"  [P1] Player 1 (Yellow) Wins : {p1_wins:2d} ({p1_wins/args.matches*100:5.1f}%)")
    print(f"  [P2] Player 2 (Red) Wins    : {p2_wins:2d} ({p2_wins/args.matches*100:5.1f}%)")
    print(f"  [--] Draws / Ties           : {draws:2d} ({draws/args.matches*100:5.1f}%)")
    print(f"  [!!] Total Anomalies        : {total_anomalies:2d}")
    print("=" * 75)

    # Detailed Match Log Table
    print("\n| Match | Winner | Score | Closest Stone | Collisions | Duration | Anomalies |")
    print("|:-----:|:------:|:-----:|:-------------:|:----------:|:--------:|:---------:|")
    for r in results:
        status = "[OK]" if not r.anomalies else f"[WARN: {len(r.anomalies)}]"
        print(f"| #{r.match_id:02d}  |   {r.winner:4s} | {r.p1_score}-{r.p2_score} | {r.closest_distance:5.2f}m       | {r.total_collisions:10d} | {r.duration_sec:6.2f}s  | {status:9s} |")

    # Anomaly Details
    if total_anomalies > 0:
        print("\n" + "!" * 75)
        print("  ANOMALY INVESTIGATION LOG")
        print("!" * 75)
        for r in results:
            if r.anomalies:
                print(f"\n[Match #{r.match_id:02d} | Seed {r.seed}]:")
                for a in r.anomalies:
                    print(f"   -> {a}")

    # Visual Rock Maps (if requested or for first 3 samples)
    sample_count = args.matches if args.visualize else min(3, args.matches)
    print(f"\n" + "=" * 75)
    print(f"  ROCK MAP SAMPLES (Showing {sample_count} matches | Y=Yellow(P1), R=Red(P2), +=Button)")
    print("=" * 75)
    for i in range(sample_count):
        print(render_ascii_rock_map(results[i]))


if __name__ == "__main__":
    asyncio.run(main())
