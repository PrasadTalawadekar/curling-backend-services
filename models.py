from sqlalchemy import Column, Integer, String, Float, Boolean, JSON, DateTime, ForeignKey, Sequence
from sqlalchemy.orm import relationship
from database import Base
import datetime

# Global sequence for auto-incrementing IDs across all game data tables
global_id_seq = Sequence('global_game_data_id_seq')

# --- Meta Design Models ---

class GdSegment(Base):
    __tablename__ = "gd_segment"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_segment_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_segment = Column(Boolean, default=True)
    gd_segment_rule = Column(JSON)
    gd_segment_description = Column(String)

class GdFeature(Base):
    __tablename__ = "gd_feature"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_feature_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_feature = Column(Boolean, default=True)
    gd_feature_backend_short_code = Column(String)
    gd_feature_gameplay_short_code = Column(String)
    gd_feature_description = Column(String)
    unlock_ftue_step = Column(Integer, default=0)

class GdWidget(Base):
    __tablename__ = "gd_widget"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_widget_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_widget = Column(Boolean, default=True)
    gd_widget_asset = Column(String)
    is_gd_widget_asset = Column(Boolean, default=False)
    gd_widget_image_url = Column(String)
    gd_widget_screen_description = Column(String)
    gd_widget_multiplier = Column(Float, default=1.0)

class GdGameScreen(Base):
    __tablename__ = "gd_game_screen"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_game_screen_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_game_screen = Column(Boolean, default=True)
    gd_game_screen_asset = Column(String)
    is_gd_game_screen_asset = Column(Boolean, default=False)
    gd_game_screen_image_url = Column(String)
    gd_game_screen_description = Column(String)
    is_scrollable_horizontal = Column(Boolean, default=False)
    is_scrollable_vertical = Column(Boolean, default=False)

class GdGameScreenWidgetFeatureMapper(Base):
    __tablename__ = "gd_game_screen_widget_feature_mapper"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_game_screen_widget_feature_mapper_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_game_screen_widget_feature_mapper = Column(Boolean, default=True)
    linked_gd_game_screen = Column(Integer, ForeignKey("gd_game_screen.id", ondelete="CASCADE"))
    linked_gd_widget = Column(Integer, ForeignKey("gd_widget.id"))
    linked_gd_feature = Column(Integer, ForeignKey("gd_feature.id"), nullable=True)
    widget_x_axis = Column(Float, default=0.0)
    widget_y_axis = Column(Float, default=0.0)
    is_goto_gd_game_screen = Column(Boolean, default=False)
    linked_goto_gd_game_screen = Column(Integer, ForeignKey("gd_game_screen.id", ondelete="CASCADE"), nullable=True)
    linked_gd_segment = Column(Integer, ForeignKey("gd_segment.id", ondelete="CASCADE"), nullable=True)

class GdGameflowConfig(Base):
    __tablename__ = "gd_gameflow_config"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_gameflow_config_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_gameflow_config = Column(Boolean, default=True)
    gd_gameflow_config_description = Column(String)

class GdGameflow(Base):
    __tablename__ = "gd_gameflow"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_gameflow_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_gameflow = Column(Boolean, default=True)
    linked_gd_gameflow_config = Column(Integer, ForeignKey("gd_gameflow_config.id"))
    gd_gameflow_priority = Column(Integer, default=0)
    linked_gd_game_screen = Column(Integer, ForeignKey("gd_game_screen.id", ondelete="CASCADE"))

# --- Game Items & Economy Models ---

class GdGameCurrency(Base):
    __tablename__ = "gd_game_currency"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_game_currency_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_game_currency = Column(Boolean, default=True)
    gd_game_currency_short_code = Column(String)
    gd_game_currency_display_name = Column(String)

class GdRockAsset(Base):
    __tablename__ = "gd_rock_asset"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_rock_asset_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_rock_asset = Column(Boolean, default=True)
    gd_rock_asset_gamplay_short_code = Column(String)
    gd_rock_asset_desciription = Column(String)
    linked_gd_material_for_stone = Column(Integer, ForeignKey("gd_material.id"))
    linked_gd_material_for_handle = Column(Integer, ForeignKey("gd_material.id"))

class GdMaterial(Base):
    __tablename__ = "gd_material"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_material_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_material = Column(Boolean, default=True)
    gd_material_base_colour_hex = Column(String)
    gd_material_metallic = Column(Float, default=0.0)
    gd_material_roughness = Column(Float, default=0.0)

class GdRock(Base):
    __tablename__ = "gd_rock"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_rock_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_free = Column(Boolean, default=False)
    is_gd_rock = Column(Boolean, default=True)
    gd_rock_display_name = Column(String)
    linked_gd_rock_asset = Column(Integer, ForeignKey("gd_rock_asset.id"))
    gd_rock_weight = Column(Float, default=0.0)
    gd_rock_spin_coefficient = Column(Float, default=0.0)
    gd_rock_friction = Column(Float, default=0.0)
    gd_rock_decay_coefficient = Column(Float, default=0.0)
    gd_rock_decay_start_match = Column(Float, default=0.0)
    gd_rock_description = Column(String)
    gd_rock_curl_modifier = Column(Float, default=0.0)
    gd_rock_rebound_elasticity = Column(Float, default=0.0)
    gd_rock_max_speed = Column(Float, default=0.0)
    gd_rock_size = Column(Float, default=1.0)

class GdBroomAsset(Base):
    __tablename__ = "gd_broom_asset"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_broom_asset_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_broom_asset = Column(Boolean, default=True)
    gd_broom_asset_gamplay_short_code = Column(String)
    gd_broom_asset_desciription = Column(String)
    linked_material_for_handle = Column(Integer, ForeignKey("gd_material.id"), nullable=True)
    linked_material_for_broom_base = Column(Integer, ForeignKey("gd_material.id"), nullable=True)
    linked_material_for_broom_top = Column(Integer, ForeignKey("gd_material.id"), nullable=True)

class GdBroom(Base):
    __tablename__ = "gd_broom"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_broom_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_free = Column(Boolean, default=False)
    is_gd_broom = Column(Boolean, default=True)
    gd_broom_display_name = Column(String)
    linked_gd_broom_asset = Column(Integer, ForeignKey("gd_broom_asset.id"))
    gd_broom_friction = Column(Float, default=0.0)
    gd_broom_weight = Column(Float, default=0.0)
    gd_broom_decay_coefficient = Column(Float, default=0.0)
    gd_broom_decay_start_match = Column(Float, default=0.0)
    gd_broom_description = Column(String)

class GdRockPusherAsset(Base):
    __tablename__ = "gd_rock_pusher_asset"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_rock_pusher_asset_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_free = Column(Boolean, default=False)
    is_gd_rock_pusher_asset = Column(Boolean, default=True)
    gd_rock_pusher_asset_gamplay_short_code = Column(String)
    gd_rock_pusher_asset_desciription = Column(String)

class GdRockPusher(Base):
    __tablename__ = "gd_rock_pusher"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_rock_pusher_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_free = Column(Boolean, default=False)
    is_gd_rock_pusher = Column(Boolean, default=True)
    linked_gd_rock_pusher_asset = Column(Integer, ForeignKey("gd_rock_pusher_asset.id"))
    gd_rock_pusher_display_name = Column(String)
    gd_rock_pusher_force_multiplier = Column(Float, default=0.0)
    gd_rock_pusher_description = Column(String)
    gd_rock_pusher_uses_per_match = Column(Integer, default=1)
    gd_rock_pusher_duration_seconds = Column(Float, default=0.0)
    gd_rock_pusher_cooldown_seconds = Column(Float, default=0.0)

class GdSurfaceMaterial(Base):
    __tablename__ = "gd_surface_material"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_surface_material_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_surface_material = Column(Boolean, default=True)
    gd_surface_material_game_play_short_code = Column(String)
    gd_surface_material_description = Column(String)

class GdSurface(Base):
    __tablename__ = "gd_surface"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_surface_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_surface = Column(Boolean, default=True)
    linked_gd_surface_material = Column(Integer, ForeignKey("gd_surface_material.id"))
    gd_surface_display_name = Column(String)
    gd_surface_length = Column(Float, default=0.0)
    gd_surface_width = Column(Float, default=0.0)
    gd_surface_friction_coefficient = Column(Float, default=0.0)
    gd_surface_decay_friction_coefficient = Column(Float, default=0.0)
    gd_surface_target_radius = Column(Float, default=0.0)
    gd_surface_target_x_axis = Column(Float, default=0.0)
    gd_surface_target_y_axis = Column(Float, default=0.0)
    gd_surface_curl_factor = Column(Float, default=0.0)

class GdPlottedStoneConfig(Base):
    __tablename__ = "gd_plotted_stone_config"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_plotted_stone_config_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_plotted_stone_config = Column(Boolean, default=True)
    gd_plotted_stone_config_description = Column(String)

class GdPlottedStone(Base):
    __tablename__ = "gd_plotted_stone"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_plotted_stone_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_plotted_stone = Column(Boolean, default=True)
    linked_gd_plotted_stone_config = Column(Integer, ForeignKey("gd_plotted_stone_config.id", ondelete="CASCADE"), nullable=False)
    is_user_stone = Column(Boolean, default=False)
    gd_plotted_stone_x_axis = Column(Float, default=0.0)
    gd_plotted_stone_y_axis = Column(Float, default=0.0)

class GdPvpModule(Base):
    __tablename__ = "gd_pvp_module"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_pvp_module_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_pvp_module = Column(Boolean, default=True)
    gd_pvp_module_shortcode = Column(String)
    gd_pvp_module_description = Column(String)

class GdPvpConfig(Base):
    __tablename__ = "gd_pvp_config"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_pvp_config_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_pvp_config = Column(Boolean, default=True)
    linked_gd_pvp_module = Column(Integer, ForeignKey("gd_pvp_module.id", ondelete="CASCADE"))
    linked_gd_game_screen = Column(Integer, ForeignKey("gd_game_screen.id", ondelete="CASCADE"), nullable=True)
    gd_pvp_config_start_date = Column(DateTime, nullable=True)
    gd_pvp_config_end_date = Column(DateTime, nullable=True)
    is_gd_pvp_config_repeatable = Column(Boolean, default=False)
    gd_pvp_config_refresh_in_mins = Column(Integer, default=0)
    linked_gd_game_screen_for_return = Column(Integer, ForeignKey("gd_game_screen.id", ondelete="CASCADE"), nullable=True)
    linked_gd_segment = Column(Integer, ForeignKey("gd_segment.id", ondelete="CASCADE"), nullable=True)
    linked_gd_rewardhighway_config = Column(Integer, ForeignKey("gd_rewardhighway_config.id", ondelete="CASCADE"), nullable=True)
    widget_x_axis = Column(Float, default=50.0)
    widget_y_axis = Column(Float, default=25.0)

class GdPvp(Base):
    __tablename__ = "gd_pvp"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_pvp_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_pvp = Column(Boolean, default=True)
    linked_gd_pvp_config = Column(Integer, ForeignKey("gd_pvp_config.id", ondelete="CASCADE"))
    gd_pvp_priority = Column(Integer, default=0)
    gd_pvp_row = Column(Integer, default=0)
    gd_pvp_column = Column(Integer, default=0)
    gd_pvp_display_image_url = Column(String)
    linked_gd_game_currency = Column(Integer, ForeignKey("gd_game_currency.id"))
    gd_pvp_entry_quantity = Column(Integer, default=0)
    linked_gd_give_away_for_winner_csv = Column(String, nullable=True)
    linked_gd_give_away_for_loser_csv = Column(String, nullable=True)
    gd_pvp_chance_per_user = Column(Integer, default=0)
    gd_pvp_time_per_chance = Column(Float, default=0.0)
    linked_gd_surface = Column(Integer, ForeignKey("gd_surface.id"))
    linked_gd_environment = Column(Integer, ForeignKey("gd_environment.id", ondelete="CASCADE"), nullable=True)
    linked_gd_game_screen_return = Column(Integer, ForeignKey("gd_game_screen.id", ondelete="CASCADE"), nullable=True)
    linked_gd_plotted_stone_config_csv = Column(String, nullable=True)
    is_bot_strict = Column(Boolean, default=False)
    bot_rule = Column(String)
    enforce_bot_timeout = Column(String)
    gd_pvp_unlock_level = Column(Integer, default=1)

# --- Leaderboard Models ---

class GdLeaderboard(Base):
    __tablename__ = "gd_leaderboard"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_leaderboard_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_leaderboard = Column(Boolean, default=True)
    gd_leaderboard_title = Column(String)
    linked_gd_currency = Column(Integer, ForeignKey("gd_game_currency.id", ondelete="CASCADE"), nullable=True)
    gd_leaderboard_start_level = Column(Integer, default=0)
    gd_leaderboard_end_level = Column(Integer, default=0)
    gd_leaderboard_start_time = Column(DateTime, nullable=True)
    gd_leaderboard_end_time = Column(DateTime, nullable=True)

class GdLeaderboardReward(Base):
    __tablename__ = "gd_leaderboard_reward"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_leaderboard_reward_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_leaderboard_reward = Column(Boolean, default=True)
    gd_leaderboard_reward_title = Column(String)
    linked_gd_give_away = Column(Integer, nullable=True)
    linked_gd_leaderboard = Column(Integer, ForeignKey("gd_leaderboard.id", ondelete="CASCADE"))
    gd_leaderboard_reward_start_rank = Column(Integer, default=1)
    gd_leaderboard_reward_end_rank = Column(Integer, default=1)

# --- User Data Models ---

class UdUserMaster(Base):
    __tablename__ = "ud_user_master"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    auth_id = Column(String, unique=True, index=True, nullable=True)
    ud_user_master_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_ud_user_master = Column(Boolean, default=True)
    ud_user_master_display_name = Column(String)
    ud_user_master_display_name_change_instances = Column(Integer, default=0)
    ud_user_master_created_at = Column(DateTime, default=datetime.datetime.utcnow)
    ud_user_master_last_updated = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    is_ud_user_master_gmail = Column(Boolean, default=False)
    ud_user_master_gmail_id = Column(String, nullable=True)
    is_ud_user_master_apple = Column(Boolean, default=False)
    ud_user_master_apple_id = Column(String, nullable=True)
    is_ud_user_master_facebook = Column(Boolean, default=False)
    ud_user_master_facebook_id = Column(String, nullable=True)
    ud_user_master_ftue_step = Column(Integer, default=0)

class UdUserStats(Base):
    __tablename__ = "ud_user_stats"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    linked_ud_user_master = Column(Integer, ForeignKey("ud_user_master.id", ondelete="CASCADE"))
    ud_user_stats_xp = Column(Integer, default=0)
    ud_user_stats_total_match_played = Column(Integer, default=0)
    ud_user_stats_total_match_won = Column(Integer, default=0)
    ud_user_stats_current_win_streak = Column(Integer, default=0)
    ud_user_stats_total_spent_currencies_dictionary = Column(JSON, default=dict)
    ud_user_stats_total_earned_currencies_dictionary = Column(JSON, default=dict)
    ud_user_stats_gameplay_stats_dictionary = Column(JSON, default=dict)

class UdLeaderboardUser(Base):
    __tablename__ = "ud_leaderboard_user"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    linked_ud_user_master = Column(Integer, ForeignKey("ud_user_master.id", ondelete="CASCADE"), nullable=True)
    linked_gd_bot_profile = Column(Integer, nullable=True)
    linked_gd_leaderboard = Column(Integer, ForeignKey("gd_leaderboard.id", ondelete="CASCADE"))
    score = Column(Float, default=0.0)
    current_rank = Column(Integer, default=0)

class GdBotProfile(Base):
    __tablename__ = "gd_bot_profile"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_bot_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_bot_profile = Column(Boolean, default=True)
    gd_bot_display_image_url = Column(String)
    gd_bot_difficulty_tier = Column(Integer, default=1)
    gd_bot_display_name = Column(String)
    gd_bot_xp = Column(Integer, default=0)
