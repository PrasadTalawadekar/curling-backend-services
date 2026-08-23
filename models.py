from sqlalchemy import Column, Integer, String, Float, Boolean, JSON, DateTime, ForeignKey, Sequence
from sqlalchemy.orm import relationship
from database import Base
import datetime

# Global sequence for auto-incrementing IDs across all game data tables
global_id_seq = Sequence('global_game_data_id_seq')

# =====================================================================
# 1. META & SCREEN NAVIGATION
# =====================================================================

class GdSegment(Base):
    __tablename__ = "gd_segment"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_segment_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_segment = Column(Boolean, default=True)
    gd_segment_rule = Column(JSON)
    gd_segment_description = Column(String, nullable=True)

class GdFeature(Base):
    __tablename__ = "gd_feature"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_feature_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_feature = Column(Boolean, default=True)
    gd_feature_gameplay_short_code = Column(String)
    unlock_ftue_step = Column(Integer, default=0)
    gd_feature_description = Column(String, nullable=True)

class GdWidget(Base):
    __tablename__ = "gd_widget"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_widget_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_widget = Column(Boolean, default=True)
    gd_widget_asset = Column(String, nullable=True)
    is_gd_widget_asset = Column(Boolean, default=False)
    gd_widget_image_url = Column(String, nullable=True)
    gd_widget_multiplier = Column(Float, default=1.0)
    gd_widget_screen_description = Column(String, nullable=True)

class GdGameScreen(Base):
    __tablename__ = "gd_game_screen"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_game_screen_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_game_screen = Column(Boolean, default=True)
    gd_game_screen_asset = Column(String, nullable=True)
    is_gd_game_screen_asset = Column(Boolean, default=False)
    gd_game_screen_image_url = Column(String, nullable=True)
    is_scrollable_horizontal = Column(Boolean, default=False)
    is_scrollable_vertical = Column(Boolean, default=False)
    gd_game_screen_description = Column(String, nullable=True)

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
    gd_gameflow_config_description = Column(String, nullable=True)

class GdGameflow(Base):
    __tablename__ = "gd_gameflow"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_gameflow_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_gameflow = Column(Boolean, default=True)
    linked_gd_gameflow_config = Column(Integer, ForeignKey("gd_gameflow_config.id"))
    gd_gameflow_priority = Column(Integer, default=0)
    linked_gd_game_screen = Column(Integer, ForeignKey("gd_game_screen.id", ondelete="CASCADE"))

# =====================================================================
# 2. CORE GAME ITEMS & ASSETS
# =====================================================================

class GdGameCurrency(Base):
    __tablename__ = "gd_game_currency"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_game_currency_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_game_currency = Column(Boolean, default=True)
    gd_game_currency_asset = Column(String, nullable=True)
    is_asset = Column(Boolean, default=False)
    gd_game_currency_image_url = Column(String, nullable=True)
    gd_game_currency_display_name = Column(String)

class GdMaterial(Base):
    __tablename__ = "gd_material"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_material_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_material = Column(Boolean, default=True)
    gd_material_base_colour_hex = Column(String)
    gd_material_metallic = Column(Float, default=0.0)
    gd_material_roughness = Column(Float, default=0.0)

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
    gd_rock_friction = Column(Float, default=0.0)
    gd_rock_decay_coefficient = Column(Float, default=0.0)
    gd_rock_decay_start_match = Column(Float, default=0.0)
    gd_rock_curl_modifier = Column(Float, default=0.0)
    gd_rock_rebound_elasticity = Column(Float, default=0.0)
    gd_rock_max_speed = Column(Float, default=0.0)
    gd_rock_size = Column(Float, default=1.0)
    gd_rock_description = Column(String, nullable=True)

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
    gd_broom_description = Column(String, nullable=True)

class GdSurfaceMaterial(Base):
    __tablename__ = "gd_surface_material"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_surface_material_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_surface_material = Column(Boolean, default=True)
    gd_surface_material_asset = Column(String, nullable=True)
    linked_gd_material = Column(Integer, ForeignKey("gd_material.id"), nullable=True)
    gd_surface_material_description = Column(String, nullable=True)

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
    gd_plotted_stone_config_description = Column(String, nullable=True)

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

class GdEnvironmentAsset(Base):
    __tablename__ = "gd_environment_asset"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_environment_asset_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_environment_asset = Column(Boolean, default=True)
    gd_environment_asset = Column(String, nullable=True)

class GdEnvironment(Base):
    __tablename__ = "gd_environment"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_environment_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_environment = Column(Boolean, default=True)
    linked_gd_environment_asset = Column(Integer, ForeignKey("gd_environment_asset.id", ondelete="CASCADE"), nullable=True)
    gd_environment_ambient_light_hex = Column(String, nullable=True)
    gd_environment_fog_density = Column(Float, default=0.0)
    gd_environment_is_rebound = Column(Boolean, default=False)
    gd_environment_rebound_elasticity = Column(Float, default=0.0)

# =====================================================================
# 3. REWARD LOOT DROPS & STORE PURCHASES
# =====================================================================

class GdAdMob(Base):
    __tablename__ = "gd_ad_mob"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_ad_mob_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_ad_mob = Column(Boolean, default=True)
    gd_ad_mob_short_code = Column(String)
    gd_ad_mob_count_for_reward = Column(Integer, default=1)

class GdGiveAway(Base):
    __tablename__ = "gd_give_away"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_give_away_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_give_away = Column(Boolean, default=True)
    gd_give_away_display_name = Column(String)
    gd_give_away_display_image_url = Column(String, nullable=True)
    is_gd_give_away_probability = Column(Boolean, default=False)

class GdGiveAwayItem(Base):
    __tablename__ = "gd_give_away_item"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_give_away_item_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_give_away_item = Column(Boolean, default=True)
    gd_give_away_item_type = Column(String)
    linked_gd_item = Column(String)
    gd_give_away_item_quantity = Column(Integer, default=1)
    gd_give_away_item_probability = Column(Float, default=0.0)

class GdGiveAwayItemMapper(Base):
    __tablename__ = "gd_give_away_item_mapper"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_give_away_item_mapper_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_give_away_item_mapper = Column(Boolean, default=True)
    linked_gd_give_away = Column(Integer, ForeignKey("gd_give_away.id"))
    linked_gd_give_away_item_csv = Column(String, nullable=True)
    gd_give_away_item_mapper_priority = Column(Integer, default=0)

class GdGiveAwayFeatureMapper(Base):
    __tablename__ = "gd_give_away_feature_mapper"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_give_away_feature_mapper_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_give_away_feature_mapper = Column(Boolean, default=True)
    linked_gd_feature = Column(Integer, ForeignKey("gd_feature.id"))
    is_gd_game_currency = Column(Boolean, default=False)
    linked_gd_game_currency = Column(Integer, ForeignKey("gd_game_currency.id"), nullable=True)
    game_currency_amount = Column(Integer, default=0)
    is_gd_real_money = Column(Boolean, default=False)
    iap_value_android = Column(String, nullable=True)
    iap_value_ios = Column(String, nullable=True)
    iap_equivalent_usd = Column(Float, default=0.0)
    is_ad_mob = Column(Boolean, default=False)
    linked_gd_ad_mob = Column(Integer, ForeignKey("gd_ad_mob.id"), nullable=True)
    linked_gd_give_away = Column(Integer, ForeignKey("gd_give_away.id"), nullable=True)
    maximum_draw = Column(Integer, default=1)

# =====================================================================
# 4. REWARD HIGHWAY (BATTLE PASS)
# =====================================================================

class GdRewardhighwayConfig(Base):
    __tablename__ = "gd_rewardhighway_config"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_rewardhighway_config_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_rewardhighway_config = Column(Boolean, default=True)
    linked_currency_unit_for_progress = Column(Integer, ForeignKey("gd_game_currency.id", ondelete="CASCADE"), nullable=True)
    linked_gd_widget = Column(Integer, ForeignKey("gd_widget.id", ondelete="CASCADE"), nullable=True)
    gd_rewardhighway_config_description = Column(String, nullable=True)

class GdRewardhighway(Base):
    __tablename__ = "gd_rewardhighway"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_rewardhighway_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_rewardhighway = Column(Boolean, default=True)
    linked_gd_rewardhighway_config = Column(Integer, ForeignKey("gd_rewardhighway_config.id", ondelete="CASCADE"))
    gd_rewardhighway_priority = Column(Integer, default=0)
    gd_rewardhighway_currency_value = Column(Integer, default=0)
    linked_gd_give_away = Column(Integer, ForeignKey("gd_give_away.id", ondelete="CASCADE"), nullable=True)
    image_url = Column(String, nullable=True)
    gd_rewardhighway_description = Column(String, nullable=True)

# =====================================================================
# 5. PVP & CHALLENGE GAME MODES
# =====================================================================

class GdPvpModule(Base):
    __tablename__ = "gd_pvp_module"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_pvp_module_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_pvp_module = Column(Boolean, default=True)
    gd_pvp_module_shortcode = Column(String)
    linked_gd_feature = Column(Integer, ForeignKey("gd_feature.id", ondelete="CASCADE"), nullable=True)
    gd_pvp_module_description = Column(String, nullable=True)

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
    gd_pvp_display_image_url = Column(String, nullable=True)
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
    bot_rule = Column(String, nullable=True)
    enforce_bot_timeout = Column(String, nullable=True)
    gd_pvp_unlock_level = Column(Integer, default=1)

class GdChallengeModule(Base):
    __tablename__ = "gd_challenge_module"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_challenge_module_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_challenge_module = Column(Boolean, default=True)
    gd_challenge_module_shortcode = Column(String)
    linked_gd_feature = Column(Integer, ForeignKey("gd_feature.id", ondelete="CASCADE"), nullable=True)
    gd_challenge_module_description = Column(String, nullable=True)

class GdScenario(Base):
    __tablename__ = "gd_scenario"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_scenario_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_scenario = Column(Boolean, default=True)
    gd_scenario_display_description = Column(String, nullable=True)
    gd_scenario_condition_gameplay_formula = Column(String, nullable=True)
    gd_scenario_description = Column(String, nullable=True)

class GdChallengeConfig(Base):
    __tablename__ = "gd_challenge_config"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_challenge_config_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_challenge_config = Column(Boolean, default=True)
    linked_gd_challenge_module = Column(Integer, ForeignKey("gd_challenge_module.id", ondelete="CASCADE"))
    linked_gd_game_screen = Column(Integer, ForeignKey("gd_game_screen.id", ondelete="CASCADE"), nullable=True)
    gd_challenge_config_start_date = Column(DateTime, nullable=True)
    gd_challenge_config_end_date = Column(DateTime, nullable=True)
    is_gd_challenge_config_repeatable = Column(Boolean, default=False)
    gd_challenge_config_refresh_in_mins = Column(Integer, default=0)
    linked_gd_game_screen_for_return = Column(Integer, ForeignKey("gd_game_screen.id", ondelete="CASCADE"), nullable=True)
    linked_gd_segment = Column(Integer, ForeignKey("gd_segment.id", ondelete="CASCADE"), nullable=True)
    linked_gd_rewardhighway_config = Column(Integer, ForeignKey("gd_rewardhighway_config.id", ondelete="CASCADE"), nullable=True)
    widget_x_axis = Column(Float, default=50.0)
    widget_y_axis = Column(Float, default=25.0)

class GdChallenge(Base):
    __tablename__ = "gd_challenge"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_challenge_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_challenge = Column(Boolean, default=True)
    linked_gd_challenge_config = Column(Integer, ForeignKey("gd_challenge_config.id", ondelete="CASCADE"))
    gd_challenge_priority = Column(Integer, default=0)
    gd_challenge_row = Column(Integer, default=0)
    gd_challenge_column = Column(Integer, default=0)
    gd_challenge_display_image_url = Column(String, nullable=True)
    gd_challenge_is_entry_fee = Column(Boolean, default=False)
    linked_gd_game_currency_entry_fee = Column(Integer, ForeignKey("gd_game_currency.id", ondelete="CASCADE"), nullable=True)
    gd_challenge_entry_quantity = Column(Integer, default=0)
    linked_gd_give_away_for_winner_csv = Column(String, nullable=True)
    linked_gd_give_away_for_loser_csv = Column(String, nullable=True)
    linked_gd_scenario = Column(Integer, ForeignKey("gd_scenario.id", ondelete="CASCADE"), nullable=True)
    gd_challenge_is_user_rock = Column(Boolean, default=False)
    linked_user_rock = Column(Integer, ForeignKey("gd_rock.id", ondelete="CASCADE"), nullable=True)
    linked_gd_rock_for_opponent = Column(Integer, ForeignKey("gd_rock.id", ondelete="CASCADE"), nullable=True)
    linked_gd_surface = Column(Integer, ForeignKey("gd_surface.id", ondelete="CASCADE"), nullable=True)
    linked_gd_environment = Column(Integer, ForeignKey("gd_environment.id", ondelete="CASCADE"), nullable=True)
    linked_gd_game_currency_unlock = Column(Integer, ForeignKey("gd_game_currency.id", ondelete="CASCADE"), nullable=True)
    gd_challenge_unlock_currency_quantity = Column(Integer, default=0)
    linked_gd_plotted_stone_config_csv = Column(String, nullable=True)
    gd_challenge_is_tutorial = Column(Boolean, default=False)
    linked_gd_challenge_for_unlock = Column(Integer, ForeignKey("gd_challenge.id", ondelete="CASCADE"), nullable=True)
    gd_challenge_number_of_chances = Column(Integer, default=1)

# =====================================================================
# 6. LEADERBOARDS
# =====================================================================

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
    linked_gd_give_away = Column(Integer, ForeignKey("gd_give_away.id", ondelete="SET NULL"), nullable=True)
    linked_gd_leaderboard = Column(Integer, ForeignKey("gd_leaderboard.id", ondelete="CASCADE"))
    gd_leaderboard_reward_start_rank = Column(Integer, default=1)
    gd_leaderboard_reward_end_rank = Column(Integer, default=1)

# =====================================================================
# 7. PROGRESSION, BOT AI & SYSTEM CONFIGS
# =====================================================================

class GdUserLevel(Base):
    __tablename__ = "gd_user_level"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_user_level_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_user_level = Column(Boolean, default=True)
    gd_user_level_number = Column(Integer, default=1)
    gd_user_level_min_xp = Column(Integer, default=0)
    gd_user_level_max_xp = Column(Integer, default=100)
    linked_gd_give_away_for_level = Column(Integer, ForeignKey("gd_give_away.id", ondelete="SET NULL"), nullable=True)

class GdGameplayStats(Base):
    __tablename__ = "gd_gameplay_stats"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_gameplay_stats_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_gameplay_stats = Column(Boolean, default=True)
    gd_gameplay_stats_type = Column(String, nullable=True)
    gd_gameplay_stats_short_code = Column(String)
    gd_gameplay_stats_description = Column(String, nullable=True)

class GdGameplayStatsXpMapper(Base):
    __tablename__ = "gd_gameplay_stats_xp_mapper"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_gameplay_stats_xp_mapper_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_gameplay_stats_xp_mapper = Column(Boolean, default=True)
    linked_gd_gameplay_stats = Column(Integer, ForeignKey("gd_gameplay_stats.id", ondelete="CASCADE"))
    xp_reward_count = Column(Integer, default=0)
    gd_gameplay_stats_xp_mapper_description = Column(String, nullable=True)

class GdUserMessage(Base):
    __tablename__ = "gd_user_message"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_user_message_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    sender_name = Column(String)
    message_title = Column(String)
    message_body = Column(String)
    linked_gd_give_away = Column(Integer, ForeignKey("gd_give_away.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    target_user_id = Column(Integer, nullable=True)

class GdGameDetails(Base):
    __tablename__ = "gd_game_details"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_game_details_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_game_details = Column(Boolean, default=True)
    gd_game_details_version = Column(String)
    gd_game_details_forced_update_version = Column(String)
    gd_game_details_on_maintenance = Column(Boolean, default=False)
    gd_game_details_maintenance_off_date_time = Column(DateTime, nullable=True)
    gd_game_details_maintenance_message = Column(String, nullable=True)
    gd_game_details_update_message = Column(String, nullable=True)
    gd_game_details_is_android = Column(Boolean, default=True)
    gd_game_details_is_ios = Column(Boolean, default=False)
    gd_game_details_store_url = Column(String, nullable=True)
    gd_game_details_asset_bundle = Column(String, default="na")

class GdBotProfile(Base):
    __tablename__ = "gd_bot_profile"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    gd_bot_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_gd_bot_profile = Column(Boolean, default=True)
    gd_bot_display_name = Column(String)
    gd_bot_display_image_url = Column(String, nullable=True)
    gd_bot_difficulty_tier = Column(Integer, default=1)
    gd_bot_xp = Column(Integer, default=0)
    linked_gd_rock = Column(String, nullable=True)
    linked_gd_broom = Column(String, nullable=True)
    gd_bot_target_accuracy_percentage = Column(Float, default=100.0)
    gd_bot_takeout_probability = Column(Float, default=1.0)
    gd_bot_perfect_release_probability = Column(Float, default=1.0)
    gd_bot_sweep_efficiency = Column(Float, default=1.0)
    gd_bot_min_think_time_seconds = Column(Float, default=0.5)
    gd_bot_max_think_time_seconds = Column(Float, default=1.0)
    gd_bot_guard_placement_probability = Column(Float, default=0.8)
    gd_bot_choke_probability = Column(Float, default=0.0)
    gd_bot_target_drift_variance = Column(Float, default=0.0)
    gd_bot_surrender_probability = Column(Float, default=0.0)

# =====================================================================
# 8. USER DATA MODELS (All with 9-digit Master ID)
# =====================================================================

class UdUserMaster(Base):
    __tablename__ = "ud_user_master"
    id = Column(Integer, primary_key=True, index=True, autoincrement=False)  # Random 9-digit Player ID
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

class UdUserWallet(Base):
    __tablename__ = "ud_user_wallet"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    linked_ud_user_master = Column(Integer, ForeignKey("ud_user_master.id", ondelete="CASCADE"), unique=True)
    ud_user_wallet_currency_dictionary = Column(JSON, default=dict)

class UdUserStats(Base):
    __tablename__ = "ud_user_stats"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    linked_ud_user_master = Column(Integer, ForeignKey("ud_user_master.id", ondelete="CASCADE"), unique=True)
    ud_user_stats_xp = Column(Integer, default=0)
    ud_user_stats_total_match_played = Column(Integer, default=0)
    ud_user_stats_total_match_won = Column(Integer, default=0)
    ud_user_stats_current_win_streak = Column(Integer, default=0)
    ud_user_stats_total_spent_currencies_dictionary = Column(JSON, default=dict)
    ud_user_stats_total_earned_currencies_dictionary = Column(JSON, default=dict)
    ud_user_stats_gameplay_stats_dictionary = Column(JSON, default=dict)

class UdUserRock(Base):
    __tablename__ = "ud_user_rock"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    ud_user_rock_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_ud_user_rock = Column(Boolean, default=True)
    linked_ud_user_master = Column(Integer, ForeignKey("ud_user_master.id", ondelete="CASCADE"))
    linked_gd_rock = Column(Integer, ForeignKey("gd_rock.id", ondelete="CASCADE"))
    ud_user_rock_aquired_date = Column(DateTime, default=datetime.datetime.utcnow)
    is_ud_user_rock_expire = Column(Boolean, default=False)
    ud_user_rock_expiry_date = Column(DateTime, nullable=True)
    ud_user_rock_weight = Column(Float, default=1.0)
    ud_user_rock_spin_coefficient = Column(Float, default=1.0)
    ud_user_rock_weight_curl_modifier = Column(Float, default=1.0)
    ud_user_rock_rebound_elasticity = Column(Float, default=1.0)
    ud_user_rock_max_speed = Column(Float, default=100.0)
    ud_user_rock_size = Column(Float, default=1.0)

class UdUserBroom(Base):
    __tablename__ = "ud_user_broom"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    ud_user_broom_name = Column(String, index=True)
    is_enabled = Column(Boolean, default=True)
    is_ud_user_broom = Column(Boolean, default=True)
    linked_ud_user_master = Column(Integer, ForeignKey("ud_user_master.id", ondelete="CASCADE"))
    linked_gd_broom = Column(Integer, ForeignKey("gd_broom.id", ondelete="CASCADE"))
    ud_user_broom_aquired_date = Column(DateTime, default=datetime.datetime.utcnow)
    is_ud_user_broom_expire = Column(Boolean, default=False)
    ud_user_broom_expiry_date = Column(DateTime, nullable=True)
    ud_user_broom_friction = Column(Float, default=0.1)
    ud_user_broom_weight = Column(Float, default=1.0)
    ud_user_broom_decay_coefficient = Column(Float, default=0.1)

class UdUserLoadout(Base):
    __tablename__ = "ud_user_loadout"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    linked_ud_user_master = Column(Integer, ForeignKey("ud_user_master.id", ondelete="CASCADE"), unique=True)
    linked_ud_user_rock = Column(Integer, ForeignKey("ud_user_rock.id", ondelete="SET NULL"), nullable=True)
    linked_ud_user_broom = Column(Integer, ForeignKey("ud_user_broom.id", ondelete="SET NULL"), nullable=True)

class UdUserChallenge(Base):
    __tablename__ = "ud_user_challenge"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    linked_ud_user_master = Column(Integer, ForeignKey("ud_user_master.id", ondelete="CASCADE"))
    linked_gd_challenge = Column(Integer, ForeignKey("gd_challenge.id", ondelete="CASCADE"))
    last_completed_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_completed = Column(Boolean, default=False)
    completion_count_with_user_stone = Column(JSON, default=dict)

class AnalysisUserDailyActivity(Base):
    __tablename__ = "analysis_user_daily_activity"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    p_user_id = Column(Integer, ForeignKey("ud_user_master.id", ondelete="CASCADE"))
    p_platform = Column(String, default="Android")
    p_app_version = Column(String, default="1.0.0")
    p_first_seen_date = Column(DateTime, default=datetime.datetime.utcnow)
    activity_date = Column(DateTime, default=datetime.datetime.utcnow)

class UdLeaderboardUser(Base):
    __tablename__ = "ud_leaderboard_user"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    linked_ud_user_master = Column(Integer, ForeignKey("ud_user_master.id", ondelete="CASCADE"), nullable=True)
    linked_gd_bot_profile = Column(Integer, nullable=True)
    linked_gd_leaderboard = Column(Integer, ForeignKey("gd_leaderboard.id", ondelete="CASCADE"))
    score = Column(Float, default=0.0)
    current_rank = Column(Integer, default=0)

class UdUserRewardhighway(Base):
    __tablename__ = "ud_user_rewardhighway"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    linked_ud_user_master = Column(Integer, ForeignKey("ud_user_master.id", ondelete="CASCADE"))
    linked_gd_rewardhighway = Column(Integer, ForeignKey("gd_rewardhighway.id", ondelete="CASCADE"))
    claimed_at = Column(DateTime, default=datetime.datetime.utcnow)

class UdUserGiveAway(Base):
    __tablename__ = "ud_user_give_away"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    linked_ud_user_master = Column(Integer, ForeignKey("ud_user_master.id", ondelete="CASCADE"))
    linked_gd_give_away = Column(Integer, ForeignKey("gd_give_away.id", ondelete="CASCADE"))
    linked_gd_give_away_item = Column(Integer, ForeignKey("gd_give_away_item.id", ondelete="CASCADE"), nullable=True)
    claimed_at = Column(DateTime, default=datetime.datetime.utcnow)

class UdUserMessageMaster(Base):
    __tablename__ = "ud_user_message_master"
    id = Column(Integer, global_id_seq, primary_key=True, index=True)
    linked_ud_user_master = Column(Integer, ForeignKey("ud_user_master.id", ondelete="CASCADE"))
    linked_gd_user_message = Column(Integer, ForeignKey("gd_user_message.id", ondelete="CASCADE"))
    is_read = Column(Boolean, default=False)
    is_claimed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
