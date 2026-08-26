"""
Backend Bot Brain Service
=========================
Advanced Goal-Oriented Trajectory Bot ("Billiards Style")
1. Analyzes the board to pick a strategic Goal (Takeout, Guard, Draw, Freeze).
2. Mathematically calculates the required arc using Iterative Refinement.
3. Simulates full board with elastic collisions to predict shot outcomes.
4. Picks the trajectory that produces the best scored board state.
"""

import math
import random
from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class BotAction:
    action: str
    delay: float
    startX: Optional[float] = None
    angle: Optional[float] = None
    power: Optional[float] = None
    curl: Optional[float] = None
    strategy: Optional[str] = None
    target_x: Optional[float] = None
    target_z: Optional[float] = None

    def to_dict(self):
        d = {"action": self.action, "delay": self.delay}
        if self.startX is not None: d["startX"] = self.startX
        if self.angle is not None:  d["angle"]  = self.angle
        if self.power is not None:  d["power"]  = self.power
        if self.curl  is not None:  d["curl"]   = self.curl
        if self.strategy is not None: d["strategy"] = self.strategy
        if self.target_x is not None: d["target_x"] = self.target_x
        if self.target_z is not None: d["target_z"] = self.target_z
        return d


GRAVITY = 9.81


# ---------------------------------------------------------------------------
# Simulated Stone (used by full-board collision simulation)
# ---------------------------------------------------------------------------

@dataclass
class SimStone:
    """Mirrors Unity DeterministicPhysicsEngine.StoneData."""
    x: float
    z: float
    vx: float = 0.0
    vz: float = 0.0
    mass: float = 20.0
    radius: float = 0.5
    elasticity: float = 0.85
    friction: float = 0.046
    curl: float = 0.0
    curl_modifier: float = 1.0
    surf_factor: float = 1.0
    max_curl: float = 15.0
    owner: str = ""
    is_moving: bool = False


# ---------------------------------------------------------------------------
# Physics Simulation Engine (Mirrors Unity Exactly)
# ---------------------------------------------------------------------------

def simulate_single_stone(startX, angle_deg, power, curl, throw_start_z, base_friction, max_curl, curl_modifier, surf_factor):
    """Simulate a single stone in isolation (no collisions). Returns final (x, z)."""
    x = startX
    z = throw_start_z
    angle_rad = math.radians(angle_deg)
    vx = math.sin(angle_rad) * power
    vz = math.cos(angle_rad) * power

    dt = 0.02  # Unity fixed timestep

    while math.sqrt(vx*vx + vz*vz) > 0.01:
        spd = math.sqrt(vx*vx + vz*vz)
        dir_x, dir_z = vx / spd, vz / spd

        accel_fx = -dir_x * base_friction * GRAVITY
        accel_fz = -dir_z * base_friction * GRAVITY

        perp_x, perp_z = dir_z, -dir_x
        # NEGATE curl to match Unity's curlEffect = -selectedCurl logic
        C = (curl_modifier + surf_factor) * (-curl / max_curl) * 0.0005
        accel_lat = 2.0 * C * spd * spd

        ax = accel_fx + perp_x * accel_lat
        az = accel_fz + perp_z * accel_lat

        x += vx * dt + 0.5 * ax * dt * dt
        z += vz * dt + 0.5 * az * dt * dt
        vx += ax * dt
        vz += az * dt

        if vx * dir_x + vz * dir_z <= 0:
            break

    return x, z


# ---------------------------------------------------------------------------
# Full Board Simulation with Elastic Collisions
# Port of Unity DeterministicPhysicsEngine.StepPhysics + ResolveCollision
# ---------------------------------------------------------------------------

def _resolve_collision(a: SimStone, b: SimStone):
    """
    Elastic collision resolver.
    Exact port of Unity DeterministicPhysicsEngine.ResolveCollision().
    """
    dx = b.x - a.x
    dz = b.z - a.z
    dist_sq = dx * dx + dz * dz
    radius_sum = a.radius + b.radius

    if dist_sq >= radius_sum * radius_sum or dist_sq < 0.0001:
        return

    dist = math.sqrt(dist_sq)
    nx = dx / dist
    nz = dz / dist

    # 1. Separate overlapping stones
    overlap = radius_sum - dist
    a.x -= nx * (overlap * 0.5)
    a.z -= nz * (overlap * 0.5)
    b.x += nx * (overlap * 0.5)
    b.z += nz * (overlap * 0.5)

    # 2. Relative velocity along collision normal
    rel_vx = b.vx - a.vx
    rel_vz = b.vz - a.vz
    vel_along_normal = rel_vx * nx + rel_vz * nz

    # Already separating — don't bounce again
    if vel_along_normal > 0:
        return

    # 3. Impulse-based momentum transfer (mirrors Unity exactly)
    combined_restitution = a.elasticity * b.elasticity
    j = -(1.0 + combined_restitution) * vel_along_normal
    j /= (1.0 / a.mass) + (1.0 / b.mass)

    impulse_x = nx * j
    impulse_z = nz * j

    a.vx -= impulse_x / a.mass
    a.vz -= impulse_z / a.mass
    b.vx += impulse_x / b.mass
    b.vz += impulse_z / b.mass

    a.is_moving = True
    b.is_moving = True


def simulate_full_board(stones: List[SimStone], max_steps: int = 3000) -> List[SimStone]:
    """
    Simulate all stones with full collision detection until everything stops.
    Exact port of Unity DeterministicPhysicsEngine.StepPhysics().
    """
    dt = 0.02

    for step in range(max_steps):
        any_moving = False

        # 1. Update positions and velocities for all moving stones
        for stone in stones:
            if not stone.is_moving:
                continue
            any_moving = True

            spd = math.sqrt(stone.vx ** 2 + stone.vz ** 2)
            if spd < 0.01:
                stone.vx = 0.0
                stone.vz = 0.0
                stone.is_moving = False
                continue

            dir_x = stone.vx / spd
            dir_z = stone.vz / spd

            # Friction deceleration
            accel_fx = -dir_x * stone.friction * GRAVITY
            accel_fz = -dir_z * stone.friction * GRAVITY

            # Curl steering (perpendicular to velocity direction)
            perp_x = dir_z
            perp_z = -dir_x
            C = (stone.curl_modifier + stone.surf_factor) * (-stone.curl / stone.max_curl) * 0.0005
            accel_lat = 2.0 * C * spd * spd

            ax = accel_fx + perp_x * accel_lat
            az = accel_fz + perp_z * accel_lat

            # Verlet position update: S = UT + 0.5AT²
            stone.x += stone.vx * dt + 0.5 * ax * dt * dt
            stone.z += stone.vz * dt + 0.5 * az * dt * dt

            # Velocity update: V = U + AT
            stone.vx += ax * dt
            stone.vz += az * dt

            # If friction reversed direction, stone has stopped
            if stone.vx * dir_x + stone.vz * dir_z <= 0:
                stone.vx = 0.0
                stone.vz = 0.0
                stone.is_moving = False

        # 2. Resolve pairwise collisions (elastic bouncing)
        n = len(stones)
        for i in range(n):
            for j in range(i + 1, n):
                _resolve_collision(stones[i], stones[j])

        if not any_moving:
            break

    return stones


# ---------------------------------------------------------------------------
# Board State Scoring
# ---------------------------------------------------------------------------

def score_board_state(stones: List[SimStone], house_cx: float, house_cz: float, house_radius: float) -> float:
    """
    Evaluate a board state from the bot's perspective. Higher = better for bot.

    Mirrors actual curling scoring rules:
    - The team with the stone closest to the button scores
    - They score 1 point for each stone closer than the opponent's nearest
    - Weighted by proximity to center for tiebreaking between trajectories
    """
    bot_dists = []
    player_dists = []

    for s in stones:
        d = math.sqrt((s.x - house_cx) ** 2 + (s.z - house_cz) ** 2)
        if d <= house_radius:
            if s.owner == "bot":
                bot_dists.append(d)
            elif s.owner == "player":
                player_dists.append(d)

    bot_dists.sort()
    player_dists.sort()

    bot_nearest = bot_dists[0] if bot_dists else float('inf')
    player_nearest = player_dists[0] if player_dists else float('inf')

    if bot_nearest == float('inf') and player_nearest == float('inf'):
        return 0.0  # Empty house — neutral

    score = 0.0
    if bot_nearest < player_nearest:
        # Bot is winning — count scoring stones (closer than opponent's nearest)
        for d in bot_dists:
            if d < player_nearest:
                score += 1.0 + (house_radius - d) / house_radius  # 1.0–2.0 per stone
    else:
        # Player is winning — negative score
        for d in player_dists:
            if d < bot_nearest:
                score -= 1.0 + (house_radius - d) / house_radius

    return score


# ---------------------------------------------------------------------------
# Sim Board Builder
# ---------------------------------------------------------------------------

def _build_sim_board(
    stones: List[dict],
    startX: float, angle_deg: float, power: float, curl: float,
    throw_start_z: float, base_friction: float,
    curl_modifier: float, surf_factor: float, max_curl: float,
    bot_mass: float, bot_radius: float, bot_elasticity: float,
) -> List[SimStone]:
    """Construct a list of SimStones from the raw board state + the new thrown bot stone."""
    sim_stones = []

    # Add existing stones on ice (stationary)
    for s in stones:
        sim_stones.append(SimStone(
            x=s["x"], z=s["z"],
            vx=0.0, vz=0.0,
            mass=s.get("mass", 20.0),
            radius=s.get("radius", bot_radius),
            elasticity=s.get("elasticity", 0.85),
            friction=base_friction,
            curl=0.0,  # Stationary stones have no curl
            curl_modifier=curl_modifier,
            surf_factor=surf_factor,
            max_curl=max_curl,
            owner=s.get("owner", ""),
            is_moving=False,
        ))

    # Add the thrown bot stone (moving)
    angle_rad = math.radians(angle_deg)
    vx = math.sin(angle_rad) * power
    vz = math.cos(angle_rad) * power

    sim_stones.append(SimStone(
        x=startX, z=throw_start_z,
        vx=vx, vz=vz,
        mass=bot_mass,
        radius=bot_radius,
        elasticity=bot_elasticity,
        friction=base_friction,
        curl=curl,
        curl_modifier=curl_modifier,
        surf_factor=surf_factor,
        max_curl=max_curl,
        owner="bot",
        is_moving=True,
    ))

    return sim_stones


# ---------------------------------------------------------------------------
# Single-Stone Iterative Aiming
# ---------------------------------------------------------------------------

def find_perfect_aim(target_x, target_z, startX, curl, throw_start_z, base_friction, max_curl, curl_modifier, surf_factor, max_power, fixed_power=None):
    """Iteratively refine angle and power so a single stone lands exactly at (target_x, target_z)."""
    dx = target_x - startX
    dz = target_z - throw_start_z
    dist = math.sqrt(dx * dx + dz * dz)

    if fixed_power is not None:
        power = fixed_power
    else:
        power = math.sqrt(2.0 * (base_friction * GRAVITY) * dist)

    # Initial angle guess with curl compensation
    angle_deg = math.degrees(math.atan2(dx, dz)) - ((-curl / max_curl) * 3.5)

    # Iterative refinement to guarantee it lands perfectly
    for _ in range(12):
        fx, fz = simulate_single_stone(startX, angle_deg, power, curl, throw_start_z, base_friction, max_curl, curl_modifier, surf_factor)
        err_x = target_x - fx
        err_z = target_z - fz

        if abs(err_x) < 0.02 and abs(err_z) < 0.02:
            break

        # The longitudinal distance traveled (must be positive so atan2 doesn't invert for Player 2)
        z_dist = abs(fz - throw_start_z)
        # Avoid div by zero if it didn't move
        if z_dist < 0.1: z_dist = 0.1

        # If we threw from positive Z towards negative Z, the error direction is inverted relative to angle
        if target_z < throw_start_z:
            angle_deg -= math.degrees(math.atan2(err_x, z_dist)) * 0.8
        else:
            angle_deg += math.degrees(math.atan2(err_x, z_dist)) * 0.8

        if fixed_power is None:
            current_dist = math.sqrt((fx - startX)**2 + (fz - throw_start_z)**2)
            target_dist = math.sqrt((target_x - startX)**2 + (target_z - throw_start_z)**2)
            if current_dist > 0.1:
                power *= math.sqrt(target_dist / current_dist)

    power = min(power, max_power)
    return angle_deg, power


# ---------------------------------------------------------------------------
# Trajectory Projection — Fast Pre-Filter
# ---------------------------------------------------------------------------

def is_path_clear(
    startX: float, angle_deg: float, power: float, curl: float,
    throw_start_z: float, target_z: float,
    stones: List[dict],
    base_friction: float, max_curl: float, curl_modifier: float, surf_factor: float,
    rink_width: float, rock_radius: float
) -> float:
    """Simulates the arc and returns distance survived before hitting a stone. Returns float('inf') if clear."""

    x = startX
    z = throw_start_z
    angle_rad = math.radians(angle_deg)
    vx = math.sin(angle_rad) * power
    vz = math.cos(angle_rad) * power

    dt = 0.02  # Match Unity fixed timestep perfectly
    collision_dist_sq = (rock_radius * 2.0) ** 2

    # Stop checking when we reach the target zone
    total_z_dist = abs(target_z - throw_start_z) - (rock_radius * 2.0)

    while abs(z - throw_start_z) < total_z_dist and math.sqrt(vx*vx + vz*vz) > 0.1:
        spd = math.sqrt(vx*vx + vz*vz)
        dir_x, dir_z = vx / spd, vz / spd

        accel_fx = -dir_x * base_friction * GRAVITY
        accel_fz = -dir_z * base_friction * GRAVITY

        perp_x, perp_z = dir_z, -dir_x
        # NEGATE curl to match Unity
        C = (curl_modifier + surf_factor) * (-curl / max_curl) * 0.0005
        accel_lat = 2.0 * C * spd * spd

        ax = accel_fx + perp_x * accel_lat
        az = accel_fz + perp_z * accel_lat

        x += vx * dt + 0.5 * ax * dt * dt
        z += vz * dt + 0.5 * az * dt * dt
        vx += ax * dt
        vz += az * dt

        # Check OOB
        if abs(x) > (rink_width / 2.0):
            return 0.0

        # Check collision with other stones
        for s in stones:
            sdx = x - s["x"]
            sdz = z - s["z"]
            if sdx*sdx + sdz*sdz < collision_dist_sq:
                return abs(z - throw_start_z)  # Return distance it survived

    return float('inf')


# ---------------------------------------------------------------------------
# The Brain (Goal Selection, Board Simulation & Trajectory Optimization)
# ---------------------------------------------------------------------------

def find_best_shot(
    stones: List[dict],
    house_cx: float, house_cz: float, throw_start_z: float,
    base_friction: float, curl_modifier: float, surf_factor: float,
    rock_radius: float,
    bot_mass: float, bot_elasticity: float,
    takeout_prob: float, guard_prob: float, chances_left: int,
    max_power: float = 25.0, rink_width: float = 4.75, house_radius: float = 2.5, max_curl: float = 15.0,
) -> Tuple[float, float, float, float, float, str, float, float]:

    # 1. Analyze Board — find nearest stone to the house center
    closest_dist = float("inf")
    nearest_stone = None

    for s in stones:
        dx = s["x"] - house_cx
        dz = s["z"] - house_cz
        dist = math.sqrt(dx*dx + dz*dz)
        if dist < closest_dist:
            closest_dist = dist
            nearest_stone = s

    # If nearest stone is entirely outside the house, ignore it
    if nearest_stone is not None and closest_dist > house_radius:
        nearest_stone = None

    # 2. Strategy Selection (with difficulty-based probability gating)
    target_power_modifier = 1.0
    intent_strategy = ""
    target_power = None  # None = let find_perfect_aim calculate power

    if nearest_stone is not None:
        if nearest_stone["owner"] == "bot":
            # Bot's stone is nearest → Guard (probability gated by guard_prob)
            if random.random() <= guard_prob:
                intent_strategy = "Guard"
                target_x = nearest_stone["x"]
                # Clamped guard offset: max contribution from chances_left capped at 3
                guard_offset = rock_radius + 0.5 + (random.uniform(0.2, 0.5) * min(chances_left, 3))
                if throw_start_z > house_cz:
                    target_z = nearest_stone["z"] + guard_offset
                else:
                    target_z = nearest_stone["z"] - guard_offset
                target_power_modifier = 0.95
            else:
                # Difficulty downgrade: Draw instead of Guard
                intent_strategy = "Draw"
                target_x = house_cx
                target_z = house_cz
        else:
            # Player's stone is nearest
            # Freeze opportunity: late game AND stone near center
            if chances_left <= 3 and closest_dist < house_radius * 0.5:
                intent_strategy = "Freeze"
                target_x = nearest_stone["x"]
                # Land just touching the player's stone (from throw side)
                if throw_start_z > house_cz:
                    target_z = nearest_stone["z"] + (rock_radius * 2.0 + 0.05)
                else:
                    target_z = nearest_stone["z"] - (rock_radius * 2.0 + 0.05)
                target_power_modifier = 0.98  # Gentle delivery
            elif random.random() <= takeout_prob:
                intent_strategy = "Takeout"
                target_x = nearest_stone["x"]
                target_z = nearest_stone["z"]
                target_power = max_power
            else:
                # Difficulty downgrade: Draw instead of Takeout
                intent_strategy = "Draw"
                target_x = house_cx
                target_z = house_cz
    else:
        # No stone in house → Draw to center
        intent_strategy = "Draw"
        target_x = house_cx
        target_z = house_cz

    # 3. Search for Best Trajectory via Full Board Simulation
    test_starts = [0.0, 0.5, -0.5, 1.0, -1.0]
    test_curls = [0.0, max_curl * 0.3, -max_curl * 0.3, max_curl * 0.6, -max_curl * 0.6, max_curl, -max_curl]

    best_score = float('-inf')
    best_params = None
    fallback_params = None
    fallback_survival = -1.0

    # Strategies that deliberately target an existing stone skip the path-clear pre-filter
    skip_prefilter = intent_strategy in ("Takeout", "Freeze")

    for startX in test_starts:
        for curl in test_curls:
            angle, power = find_perfect_aim(
                target_x, target_z, startX, curl, throw_start_z,
                base_friction, max_curl, curl_modifier, surf_factor, max_power,
                fixed_power=target_power
            )

            # Apply power modifier (Guard=0.95, Freeze=0.98, others=1.0)
            if target_power is None:
                power *= target_power_modifier

            # Fast pre-filter for Draw/Guard (skip for Takeout/Freeze)
            if not skip_prefilter:
                survival_dist = is_path_clear(
                    startX, angle, power, curl, throw_start_z, target_z,
                    stones, base_friction, max_curl, curl_modifier, surf_factor,
                    rink_width, rock_radius
                )
                if survival_dist != float('inf'):
                    # Path is blocked — track as fallback by survival distance
                    if survival_dist > fallback_survival:
                        fallback_survival = survival_dist
                        fallback_params = (startX, angle, power, curl)
                    continue

            # Full board simulation to evaluate shot outcome
            sim_board = _build_sim_board(
                stones, startX, angle, power, curl,
                throw_start_z, base_friction, curl_modifier, surf_factor, max_curl,
                bot_mass, rock_radius, bot_elasticity
            )
            simulate_full_board(sim_board)
            board_score = score_board_state(sim_board, house_cx, house_cz, house_radius)

            if board_score > best_score:
                best_score = board_score
                best_params = (startX, angle, power, curl)

    if best_params is not None:
        return (*best_params, best_score, intent_strategy, target_x, target_z)

    # Fallback: use trajectory that survived the longest before collision
    if fallback_params is not None:
        return (*fallback_params, 0.0, intent_strategy, target_x, target_z)

    # Ultimate fallback: straight shot to target
    angle, power = find_perfect_aim(
        target_x, target_z, 0.0, 0.0, throw_start_z,
        base_friction, max_curl, curl_modifier, surf_factor, max_power,
        fixed_power=target_power
    )
    return 0.0, angle, power, 0.0, 0.0, intent_strategy, target_x, target_z


# ---------------------------------------------------------------------------
# Public entry: build full human-like action sequence
# ---------------------------------------------------------------------------

def generate_bot_actions(
    stones_raw: List[dict],
    house_cx: float, house_cz: float, throw_start_z: float,
    rink_friction: float, bot_rock_friction: float, bot_rock_curl_modifier: float,
    bot_rock_mass: float, bot_rock_radius: float, bot_rock_elasticity: float,
    curl_factor: float, drift_variance: float, perfect_release_probability: float,
    takeout_probability: float, guard_probability: float, chances_left: int,
    max_power: float = 25.0, rink_width: float = 4.75, house_radius: float = 2.5, max_curl: float = 15.0,
) -> List[dict]:

    base_friction = bot_rock_friction + rink_friction
    base_friction = max(base_friction, 0.01)

    startX, angle, power, curl, score, intent_strategy, target_x, target_z = find_best_shot(
        stones=stones_raw,
        house_cx=house_cx, house_cz=house_cz, throw_start_z=throw_start_z,
        base_friction=base_friction, curl_modifier=bot_rock_curl_modifier, surf_factor=curl_factor,
        rock_radius=bot_rock_radius,
        bot_mass=bot_rock_mass, bot_elasticity=bot_rock_elasticity,
        takeout_prob=takeout_probability, guard_prob=guard_probability, chances_left=chances_left,
        max_power=max_power, rink_width=rink_width, house_radius=house_radius, max_curl=max_curl
    )

    # Percentage Drift Fuzzing
    drift = max(drift_variance, 0.001)
    perfect_power, perfect_angle = power, angle
    power *= random.uniform(1.0 - drift, 1.0 + drift)
    angle += random.uniform(-drift * 5.0, drift * 5.0)

    if random.random() <= perfect_release_probability:
        power = perfect_power
        angle = perfect_angle

    # Human-like timing
    think_delay = random.uniform(0.5, 1.0)
    hold_delay  = random.uniform(0.5, 1.0)
    curl_delay  = random.uniform(0.3, 0.8)
    power_delay = random.uniform(0.2, 0.7)

    actions = [
        BotAction("intent_log",         delay=0.0,          strategy=intent_strategy, target_x=round(target_x, 3), target_z=round(target_z, 3)),
        BotAction("adjusting_position", delay=0.0,          startX=round(startX, 3)),
        BotAction("hold",               delay=think_delay),
        BotAction("set_curl",           delay=hold_delay,   curl=round(curl, 2)),
        BotAction("set_power",          delay=curl_delay,   power=round(power, 3)),
        BotAction("release",            delay=power_delay,
                  startX=round(startX, 3),
                  angle=round(angle, 3),
                  power=round(power, 3),
                  curl=round(curl, 2)),
    ]

    return [a.to_dict() for a in actions]
