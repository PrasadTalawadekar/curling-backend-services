"""
Curling Mobile Game - Database Seeder
====================================
Seeds all LiveOps CSV game tables into Google Cloud SQL / PostgreSQL.
"""

import os
import csv
import glob
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
import models


def load_csv(file_path: str):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return list(reader)


def clean_val(val, val_type):
    if val is None or val == "":
        return None
    val = str(val).strip()
    if val_type == bool:
        return val.lower() in ("true", "1", "yes", "t")
    if val_type == int:
        try: return int(float(val))
        except: return 0
    if val_type == float:
        try: return float(val)
        except: return 0.0
    return val


def seed_table(db: Session, model_cls, csv_path: str, field_types: dict):
    rows = load_csv(csv_path)
    if not rows:
        return 0

    count = 0
    for r in rows:
        record_id = clean_val(r.get("id"), int)
        if not record_id:
            continue

        existing = db.query(model_cls).filter(model_cls.id == record_id).first()
        kwargs = {"id": record_id}

        for col, col_type in field_types.items():
            if col in r:
                kwargs[col] = clean_val(r[col], col_type)

        if existing:
            for k, v in kwargs.items():
                setattr(existing, k, v)
        else:
            db.add(model_cls(**kwargs))
        count += 1

    db.commit()
    return count


def main(csv_dir: str = None):
    if not csv_dir:
        # Default path to LiveOps Admin data directory
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        csv_dir = os.path.join(base_dir, "Curling Mobile Game", "LiveOps Admin", "data")
        if not os.path.exists(csv_dir):
            csv_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

    print("=" * 60)
    print(f"  CURLING MOBILE GAME -- DATABASE SEEDER")
    print(f"  Source CSV Dir: {csv_dir}")
    print("=" * 60)

    # 1. Create tables
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Currency
        c = seed_table(db, models.GdGameCurrency, os.path.join(csv_dir, "gd_game_currency.csv"), {
            "gd_game_currency_name": str, "is_enabled": bool, "is_game_currency": bool,
            "gd_game_currency_asset": str, "is_asset": bool, "gd_game_currency_image_url": str,
            "gd_game_currency_display_name": str
        })
        print(f"  [+] gd_game_currency      : {c:3d} rows")

        # Material
        c = seed_table(db, models.GdMaterial, os.path.join(csv_dir, "gd_material.csv"), {
            "gd_material_name": str, "is_enabled": bool, "is_gd_material": bool,
            "gd_material_base_colour_hex": str, "gd_material_metallic": float, "gd_material_roughness": float
        })
        print(f"  [+] gd_material           : {c:3d} rows")

        # Rocks
        c = seed_table(db, models.GdRockAsset, os.path.join(csv_dir, "gd_rock_asset.csv"), {
            "gd_rock_asset_name": str, "is_enabled": bool, "is_gd_rock_asset": bool,
            "gd_rock_asset_gamplay_short_code": str, "gd_rock_asset_desciription": str,
            "linked_gd_material_for_stone": int, "linked_gd_material_for_handle": int
        })
        print(f"  [+] gd_rock_asset         : {c:3d} rows")

        c = seed_table(db, models.GdRock, os.path.join(csv_dir, "gd_rock.csv"), {
            "gd_rock_name": str, "is_enabled": bool, "is_free": bool, "is_gd_rock": bool,
            "gd_rock_display_name": str, "linked_gd_rock_asset": int, "gd_rock_weight": float,
            "gd_rock_friction": float, "gd_rock_decay_coefficient": float, "gd_rock_decay_start_match": float,
            "gd_rock_curl_modifier": float, "gd_rock_rebound_elasticity": float,
            "gd_rock_max_speed": float, "gd_rock_size": float, "gd_rock_description": str
        })
        print(f"  [+] gd_rock               : {c:3d} rows")

        # Brooms
        c = seed_table(db, models.GdBroomAsset, os.path.join(csv_dir, "gd_broom_asset.csv"), {
            "gd_broom_asset_name": str, "is_enabled": bool, "is_gd_broom_asset": bool,
            "gd_broom_asset_gamplay_short_code": str, "gd_broom_asset_desciription": str,
            "linked_material_for_handle": int, "linked_material_for_broom_base": int, "linked_material_for_broom_top": int
        })
        print(f"  [+] gd_broom_asset        : {c:3d} rows")

        c = seed_table(db, models.GdBroom, os.path.join(csv_dir, "gd_broom.csv"), {
            "gd_broom_name": str, "is_enabled": bool, "is_free": bool, "is_gd_broom": bool,
            "gd_broom_display_name": str, "linked_gd_broom_asset": int, "gd_broom_friction": float,
            "gd_broom_weight": float, "gd_broom_decay_coefficient": float, "gd_broom_description": str
        })
        print(f"  [+] gd_broom              : {c:3d} rows")

        # Surfaces
        c = seed_table(db, models.GdSurfaceMaterial, os.path.join(csv_dir, "gd_surface_material.csv"), {
            "gd_surface_material_name": str, "is_enabled": bool, "is_gd_surface_material": bool,
            "gd_surface_material_asset": str, "linked_gd_material": int, "gd_surface_material_description": str
        })
        print(f"  [+] gd_surface_material   : {c:3d} rows")

        c = seed_table(db, models.GdSurface, os.path.join(csv_dir, "gd_surface.csv"), {
            "gd_surface_name": str, "is_enabled": bool, "is_gd_surface": bool,
            "linked_gd_surface_material": int, "gd_surface_display_name": str,
            "gd_surface_length": float, "gd_surface_width": float,
            "gd_surface_friction_coefficient": float, "gd_surface_decay_friction_coefficient": float,
            "gd_surface_target_radius": float, "gd_surface_target_x_axis": float, "gd_surface_target_y_axis": float,
            "gd_surface_curl_factor": float
        })
        print(f"  [+] gd_surface            : {c:3d} rows")

        # Environments
        c = seed_table(db, models.GdEnvironmentAsset, os.path.join(csv_dir, "gd_environment_asset.csv"), {
            "gd_environment_asset_name": str, "is_enabled": bool, "is_gd_environment_asset": bool,
            "gd_environment_asset": str
        })
        print(f"  [+] gd_environment_asset  : {c:3d} rows")

        c = seed_table(db, models.GdEnvironment, os.path.join(csv_dir, "gd_environment.csv"), {
            "gd_environment_name": str, "is_enabled": bool, "is_gd_environment": bool,
            "linked_gd_environment_asset": int, "gd_environment_ambient_light_hex": str,
            "gd_environment_fog_density": float, "gd_environment_is_rebound": bool,
            "gd_environment_rebound_elasticity": float
        })
        print(f"  [+] gd_environment        : {c:3d} rows")

        # PvP
        c = seed_table(db, models.GdPvpModule, os.path.join(csv_dir, "gd_pvp_module.csv"), {
            "gd_pvp_module_name": str, "is_enabled": bool, "is_gd_pvp_module": bool,
            "gd_pvp_module_shortcode": str, "gd_pvp_module_description": str
        })
        print(f"  [+] gd_pvp_module         : {c:3d} rows")

        c = seed_table(db, models.GdPvpConfig, os.path.join(csv_dir, "gd_pvp_config.csv"), {
            "gd_pvp_config_name": str, "is_enabled": bool, "is_gd_pvp_config": bool,
            "linked_gd_pvp_module": int, "widget_x_axis": float, "widget_y_axis": float
        })
        print(f"  [+] gd_pvp_config         : {c:3d} rows")

        c = seed_table(db, models.GdPvp, os.path.join(csv_dir, "gd_pvp.csv"), {
            "gd_pvp_name": str, "is_enabled": bool, "is_gd_pvp": bool, "linked_gd_pvp_config": int,
            "gd_pvp_priority": int, "gd_pvp_entry_quantity": int, "gd_pvp_chance_per_user": int,
            "gd_pvp_time_per_chance": float, "linked_gd_surface": int, "linked_gd_environment": int,
            "is_bot_strict": bool, "bot_rule": str, "gd_pvp_unlock_level": int
        })
        print(f"  [+] gd_pvp                : {c:3d} rows")

        # Leaderboards
        c = seed_table(db, models.GdLeaderboard, os.path.join(csv_dir, "gd_leaderboard.csv"), {
            "gd_leaderboard_name": str, "is_enabled": bool, "is_gd_leaderboard": bool,
            "gd_leaderboard_title": str, "linked_gd_currency": int, "gd_leaderboard_start_level": int, "gd_leaderboard_end_level": int
        })
        print(f"  [+] gd_leaderboard        : {c:3d} rows")

        # Bots
        c = seed_table(db, models.GdBotProfile, os.path.join(csv_dir, "gd_bot_profile.csv"), {
            "gd_bot_name": str, "is_enabled": bool, "is_gd_bot_profile": bool,
            "gd_bot_display_name": str, "gd_bot_display_image_url": str, "gd_bot_difficulty_tier": int, "gd_bot_xp": int,
            "linked_gd_rock": str, "linked_gd_broom": str,
            "gd_bot_target_accuracy_percentage": float, "gd_bot_takeout_probability": float,
            "gd_bot_perfect_release_probability": float, "gd_bot_sweep_efficiency": float,
            "gd_bot_min_think_time_seconds": float, "gd_bot_max_think_time_seconds": float,
            "gd_bot_guard_placement_probability": float, "gd_bot_choke_probability": float,
            "gd_bot_target_drift_variance": float, "gd_bot_surrender_probability": float
        })
        print(f"  [+] gd_bot_profile        : {c:3d} rows")

        print("=" * 60)
        print("  SUCCESS: Database seeded successfully!")
        print("=" * 60)

    finally:
        db.close()


if __name__ == "__main__":
    main()
