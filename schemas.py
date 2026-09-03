from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, List
import json
import ast
from datetime import datetime

# --- GdFeature ---
class GdFeatureBase(BaseModel):
    gd_feature_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_feature: Optional[bool] = True
    gd_feature_backend_short_code: Optional[str] = None
    gd_feature_gameplay_short_code: Optional[str] = None
    gd_feature_description: Optional[str] = None
    unlock_ftue_step: Optional[int] = 0

class GdFeatureCreate(GdFeatureBase):
    pass

class GdFeatureUpdate(GdFeatureBase):
    pass

class GdFeature(GdFeatureBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- GdWidget ---
class GdWidgetBase(BaseModel):
    gd_widget_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_widget: Optional[bool] = True
    gd_widget_asset: Optional[str] = None
    is_gd_widget_asset: Optional[bool] = False
    gd_widget_image_url: Optional[str] = None
    gd_widget_screen_description: Optional[str] = None
    gd_widget_multiplier: Optional[float] = 1.0
    widget_width: Optional[float] = None
    widget_height: Optional[float] = None

class GdWidgetCreate(GdWidgetBase):
    pass

class GdWidgetUpdate(GdWidgetBase):
    pass

class GdWidget(GdWidgetBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- GdGameScreen ---
class GdGameScreenBase(BaseModel):
    gd_game_screen_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_game_screen: Optional[bool] = True
    gd_game_screen_asset: Optional[str] = None
    is_gd_game_screen_asset: Optional[bool] = False
    gd_game_screen_image_url: Optional[str] = None
    gd_game_screen_description: Optional[str] = None

class GdGameScreenCreate(GdGameScreenBase):
    pass

class GdGameScreenUpdate(GdGameScreenBase):
    pass

class GdGameScreen(GdGameScreenBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- GdSegment ---
class GdSegmentBase(BaseModel):
    gd_segment_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_segment: Optional[bool] = True
    gd_segment_rule: Optional[str] = None
    gd_segment_description: Optional[str] = None

class GdSegmentCreate(GdSegmentBase):
    pass

class GdSegmentUpdate(GdSegmentBase):
    pass

class GdSegment(GdSegmentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- GdGameScreenWidgetFeatureMapper ---
class GdGameScreenWidgetFeatureMapperBase(BaseModel):
    gd_game_screen_widget_feature_mapper_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_game_screen_widget_feature_mapper: Optional[bool] = True
    linked_gd_game_screen: Optional[int] = None
    linked_gd_widget: Optional[int] = None
    linked_gd_feature: Optional[int] = None
    widget_x_axis: Optional[float] = 0.0
    widget_y_axis: Optional[float] = 0.0
    is_goto_gd_game_screen: Optional[bool] = False
    linked_goto_gd_game_screen: Optional[int] = None
    linked_gd_segment: Optional[int] = None
    is_non_scrollable: Optional[bool] = False

class GdGameScreenWidgetFeatureMapperCreate(GdGameScreenWidgetFeatureMapperBase):
    pass

class GdGameScreenWidgetFeatureMapperUpdate(GdGameScreenWidgetFeatureMapperBase):
    pass

class GdGameScreenWidgetFeatureMapper(GdGameScreenWidgetFeatureMapperBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- GdGameflowConfig ---
class GdGameflowConfigBase(BaseModel):
    gd_gameflow_config_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_gameflow_config: Optional[bool] = True
    gd_gameflow_config_description: Optional[str] = None

class GdGameflowConfigCreate(GdGameflowConfigBase):
    pass

class GdGameflowConfigUpdate(GdGameflowConfigBase):
    pass

class GdGameflowConfig(GdGameflowConfigBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- GdGameflow ---
class GdGameflowBase(BaseModel):
    gd_gameflow_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_gameflow: Optional[bool] = True
    linked_gd_gameflow_config: Optional[int] = None
    gd_gameflow_priority: Optional[int] = 0
    linked_gd_game_screen: Optional[int] = None

class GdGameflowCreate(GdGameflowBase):
    pass

class GdGameflowUpdate(GdGameflowBase):
    pass

class GdGameflow(GdGameflowBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- Game Items & Economy Schemas ---

class GdGameCurrencyBase(BaseModel):
    gd_game_currency_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_game_currency: Optional[bool] = True
    gd_game_currency_short_code: Optional[str] = None
    gd_game_currency_display_name: Optional[str] = None

class GdGameCurrencyCreate(GdGameCurrencyBase):
    pass

class GdGameCurrency(GdGameCurrencyBase):
    id: int
    class Config:
        orm_mode = True



class GdRockBase(BaseModel):
    gd_rock_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_free: Optional[bool] = False
    is_gd_rock: Optional[bool] = True
    gd_rock_display_name: Optional[str] = None
    linked_gd_rock_asset: Optional[int] = None
    gd_rock_weight: Optional[float] = 0.0
    gd_rock_spin_coefficient: Optional[float] = 0.0
    gd_rock_friction: Optional[float] = 0.0
    gd_rock_decay_coefficient: Optional[float] = 0.0
    gd_rock_decay_start_match: Optional[float] = 0.0
    gd_rock_description: Optional[str] = None
    gd_rock_curl_modifier: Optional[float] = 0.0
    gd_rock_rebound_elasticity: Optional[float] = 0.0
    gd_rock_max_speed: Optional[float] = 0.0
    gd_rock_size: Optional[float] = 1.0

class GdRockCreate(GdRockBase):
    pass

class GdRock(GdRockBase):
    id: int
    class Config:
        orm_mode = True

class GdBroomAssetBase(BaseModel):
    gd_broom_asset_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_broom_asset: Optional[bool] = True
    gd_broom_asset_gamplay_short_code: Optional[str] = None
    gd_broom_asset_desciription: Optional[str] = None

class GdBroomAssetCreate(GdBroomAssetBase):
    pass

class GdBroomAsset(GdBroomAssetBase):
    id: int
    class Config:
        orm_mode = True

class GdBroomBase(BaseModel):
    gd_broom_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_free: Optional[bool] = False
    is_gd_broom: Optional[bool] = True
    gd_broom_display_name: Optional[str] = None
    linked_gd_broom_asset: Optional[int] = None
    gd_broom_friction: Optional[float] = 0.0
    gd_broom_weight: Optional[float] = 0.0
    gd_broom_decay_coefficient: Optional[float] = 0.0
    gd_broom_decay_start_match: Optional[float] = 0.0
    gd_broom_description: Optional[str] = None

class GdBroomCreate(GdBroomBase):
    pass

class GdBroom(GdBroomBase):
    id: int
    class Config:
        orm_mode = True

class GdRockPusherAssetBase(BaseModel):
    gd_rock_pusher_asset_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_free: Optional[bool] = False
    is_gd_rock_pusher_asset: Optional[bool] = True
    gd_rock_pusher_asset_gamplay_short_code: Optional[str] = None
    gd_rock_pusher_asset_desciription: Optional[str] = None

class GdRockPusherAssetCreate(GdRockPusherAssetBase):
    pass

class GdRockPusherAsset(GdRockPusherAssetBase):
    id: int
    class Config:
        orm_mode = True

class GdRockPusherBase(BaseModel):
    gd_rock_pusher_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_free: Optional[bool] = False
    is_gd_rock_pusher: Optional[bool] = True
    linked_gd_rock_pusher_asset: Optional[int] = None
    gd_rock_pusher_display_name: Optional[str] = None
    gd_rock_pusher_force_multiplier: Optional[float] = 0.0
    gd_rock_pusher_description: Optional[str] = None
    gd_rock_pusher_uses_per_match: Optional[int] = 1
    gd_rock_pusher_duration_seconds: Optional[float] = 0.0
    gd_rock_pusher_cooldown_seconds: Optional[float] = 0.0

class GdRockPusherCreate(GdRockPusherBase):
    pass

class GdRockPusher(GdRockPusherBase):
    id: int
    class Config:
        orm_mode = True

class GdSurfaceMaterialBase(BaseModel):
    gd_surface_material_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_surface_material: Optional[bool] = True
    gd_surface_material_game_play_short_code: Optional[str] = None
    gd_surface_material_description: Optional[str] = None

class GdSurfaceMaterialCreate(GdSurfaceMaterialBase):
    pass

class GdSurfaceMaterial(GdSurfaceMaterialBase):
    id: int
    class Config:
        orm_mode = True

class GdSurfaceBase(BaseModel):
    gd_surface_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_surface: Optional[bool] = True
    linked_gd_surface_material: Optional[int] = None
    gd_surface_display_name: Optional[str] = None
    gd_surface_length: Optional[float] = 0.0
    gd_surface_width: Optional[float] = 0.0
    gd_surface_friction_coefficient: Optional[float] = 0.0
    gd_surface_decay_friction_coefficient: Optional[float] = 0.0
    gd_surface_target_radius: Optional[float] = 0.0
    gd_surface_curl_factor: Optional[float] = 0.0

class GdSurfaceCreate(GdSurfaceBase):
    pass

class GdSurface(GdSurfaceBase):
    id: int
    class Config:
        orm_mode = True


class GdPvpMatchesConfigBase(BaseModel):
    gd_pvp_matches_config_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_pvp_matches_config: Optional[bool] = True
    gd_pvp_matches_config_priority: Optional[int] = 0
    gd_pvp_matches_config_row: Optional[int] = 0
    gd_pvp_matches_config_column: Optional[int] = 0

# --- Game Items & Economy Schemas ---

class GdGameCurrencyBase(BaseModel):
    gd_game_currency_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_game_currency: Optional[bool] = True
    gd_game_currency_short_code: Optional[str] = None
    gd_game_currency_display_name: Optional[str] = None

class GdGameCurrencyCreate(GdGameCurrencyBase):
    pass

class GdGameCurrency(GdGameCurrencyBase):
    id: int
    class Config:
        orm_mode = True

class GdRockAssetBase(BaseModel):
    gd_rock_asset_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_rock_asset: Optional[bool] = True
    gd_rock_asset_gamplay_short_code: Optional[str] = None
    gd_rock_asset_desciription: Optional[str] = None
    linked_gd_material_for_stone: Optional[int] = None
    linked_gd_material_for_handle: Optional[int] = None

class GdMaterialBase(BaseModel):
    gd_material_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_material: Optional[bool] = True
    gd_material_base_colour_hex: Optional[str] = None
    gd_material_metallic: Optional[float] = 0.0
    gd_material_roughness: Optional[float] = 0.0

class GdMaterialCreate(GdMaterialBase):
    pass

class GdMaterial(GdMaterialBase):
    id: int
    class Config:
        orm_mode = True

class GdRockAssetCreate(GdRockAssetBase):
    pass

class GdRockAsset(GdRockAssetBase):
    id: int
    class Config:
        orm_mode = True

class GdRockBase(BaseModel):
    gd_rock_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_rock: Optional[bool] = True
    gd_rock_display_name: Optional[str] = None
    linked_gd_rock_asset: Optional[int] = None
    gd_rock_weight: Optional[float] = 0.0
    gd_rock_spin_coefficient: Optional[float] = 0.0
    gd_rock_friction: Optional[float] = 0.0
    gd_rock_decay_coefficient: Optional[float] = 0.0
    gd_rock_decay_start_match: Optional[float] = 0.0
    gd_rock_description: Optional[str] = None
    gd_rock_curl_modifier: Optional[float] = 0.0
    gd_rock_rebound_elasticity: Optional[float] = 0.0
    gd_rock_max_speed: Optional[float] = 0.0

class GdRockCreate(GdRockBase):
    pass

class GdRock(GdRockBase):
    id: int
    class Config:
        orm_mode = True

class GdBroomAssetBase(BaseModel):
    gd_broom_asset_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_broom_asset: Optional[bool] = True
    gd_broom_asset_gamplay_short_code: Optional[str] = None
    gd_broom_asset_desciription: Optional[str] = None

class GdBroomAssetCreate(GdBroomAssetBase):
    pass

class GdBroomAsset(GdBroomAssetBase):
    id: int
    class Config:
        orm_mode = True

class GdBroomBase(BaseModel):
    gd_broom_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_broom: Optional[bool] = True
    gd_broom_display_name: Optional[str] = None
    linked_gd_broom_asset: Optional[int] = None
    gd_broom_friction: Optional[float] = 0.0
    gd_broom_weight: Optional[float] = 0.0
    gd_broom_decay_coefficient: Optional[float] = 0.0
    gd_broom_decay_start_match: Optional[float] = 0.0
    gd_broom_description: Optional[str] = None

class GdBroomCreate(GdBroomBase):
    pass

class GdBroom(GdBroomBase):
    id: int
    class Config:
        orm_mode = True

class GdRockPusherAssetBase(BaseModel):
    gd_rock_pusher_asset_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_rock_pusher_asset: Optional[bool] = True
    gd_rock_pusher_asset_gamplay_short_code: Optional[str] = None
    gd_rock_pusher_asset_desciription: Optional[str] = None

class GdRockPusherAssetCreate(GdRockPusherAssetBase):
    pass

class GdRockPusherAsset(GdRockPusherAssetBase):
    id: int
    class Config:
        orm_mode = True

class GdRockPusherBase(BaseModel):
    gd_rock_pusher_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_rock_pusher: Optional[bool] = True
    linked_gd_rock_pusher_asset: Optional[int] = None
    gd_rock_pusher_display_name: Optional[str] = None
    gd_rock_pusher_force_multiplier: Optional[float] = 0.0
    gd_rock_pusher_description: Optional[str] = None
    gd_rock_pusher_uses_per_match: Optional[int] = 1
    gd_rock_pusher_duration_seconds: Optional[float] = 0.0
    gd_rock_pusher_cooldown_seconds: Optional[float] = 0.0

class GdRockPusherCreate(GdRockPusherBase):
    pass

class GdRockPusher(GdRockPusherBase):
    id: int
    class Config:
        orm_mode = True

class GdSurfaceMaterialBase(BaseModel):
    gd_surface_material_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_surface_material: Optional[bool] = True
    gd_surface_material_game_play_short_code: Optional[str] = None
    gd_surface_material_description: Optional[str] = None

class GdSurfaceMaterialCreate(GdSurfaceMaterialBase):
    pass

class GdSurfaceMaterial(GdSurfaceMaterialBase):
    id: int
    class Config:
        orm_mode = True

class GdSurfaceBase(BaseModel):
    gd_surface_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_surface: Optional[bool] = True
    linked_gd_surface_material: Optional[int] = None
    gd_surface_display_name: Optional[str] = None
    gd_surface_length: Optional[float] = 0.0
    gd_surface_width: Optional[float] = 0.0
    gd_surface_friction_coefficient: Optional[float] = 0.0
    gd_surface_decay_friction_coefficient: Optional[float] = 0.0
    gd_surface_target_radius: Optional[float] = 0.0
    gd_surface_target_x_axis: Optional[float] = 0.0
    gd_surface_target_y_axis: Optional[float] = 0.0
    gd_surface_curl_factor: Optional[float] = 0.0

class GdSurfaceCreate(GdSurfaceBase):
    pass

class GdSurface(GdSurfaceBase):
    id: int
    class Config:
        orm_mode = True

class GdPlottedStoneConfigBase(BaseModel):
    gd_plotted_stone_config_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_plotted_stone_config: Optional[bool] = True
    gd_plotted_stone_config_description: Optional[str] = None

class GdPlottedStoneConfigCreate(GdPlottedStoneConfigBase):
    pass

class GdPlottedStoneConfig(GdPlottedStoneConfigBase):
    id: int
    class Config:
        orm_mode = True

class GdPlottedStoneBase(BaseModel):
    gd_plotted_stone_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_plotted_stone: Optional[bool] = True
    linked_gd_plotted_stone_config: int
    is_user_stone: Optional[bool] = False
    gd_plotted_stone_x_axis: Optional[float] = 0.0
    gd_plotted_stone_y_axis: Optional[float] = 0.0

class GdPlottedStoneCreate(GdPlottedStoneBase):
    pass

class GdPlottedStone(GdPlottedStoneBase):
    id: int
    class Config:
        orm_mode = True


class GdPvpModuleBase(BaseModel):
    gd_pvp_module_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_pvp_module: Optional[bool] = True
    gd_pvp_module_shortcode: Optional[str] = None
    gd_pvp_module_description: Optional[str] = None

class GdPvpModuleCreate(GdPvpModuleBase):
    pass

class GdPvpModule(GdPvpModuleBase):
    id: int
    class Config:
        orm_mode = True

class GdPvpConfigBase(BaseModel):
    gd_pvp_config_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_pvp_config: Optional[bool] = True
    linked_gd_pvp_module: Optional[int] = None
    linked_gd_game_screen: Optional[int] = None
    gd_pvp_config_start_date: Optional[datetime] = None
    gd_pvp_config_end_date: Optional[datetime] = None
    is_gd_pvp_config_repeatable: Optional[bool] = False
    gd_pvp_config_refresh_in_mins: Optional[int] = 0
    linked_gd_game_screen_for_return: Optional[int] = None
    linked_gd_segment: Optional[int] = None

class GdPvpConfigCreate(GdPvpConfigBase):
    pass

class GdPvpConfig(GdPvpConfigBase):
    id: int
    class Config:
        orm_mode = True

class GdPvpBase(BaseModel):
    gd_pvp_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_pvp: Optional[bool] = True
    linked_gd_pvp_config: Optional[int] = None
    gd_pvp_priority: Optional[int] = 0
    gd_pvp_row: Optional[int] = 0
    gd_pvp_column: Optional[int] = 0
    gd_pvp_display_image_url: Optional[str] = None
    linked_gd_game_currency: Optional[int] = None
    gd_pvp_entry_quantity: Optional[int] = 0
    linked_gd_give_away_for_winner_csv: Optional[str] = None
    linked_gd_give_away_for_loser_csv: Optional[str] = None
    gd_pvp_chance_per_user: Optional[int] = 0
    gd_pvp_time_per_chance: Optional[float] = 0.0
    linked_gd_surface: Optional[int] = None
    linked_gd_environment: Optional[int] = None
    linked_gd_game_screen_return: Optional[int] = None
    linked_gd_plotted_stone_config_csv: Optional[str] = None
    is_bot_strict: Optional[bool] = False
    bot_rule: Optional[str] = None
    enforce_bot_timeout: Optional[str] = None
    gd_pvp_unlock_level: Optional[int] = 1

class GdPvpCreate(GdPvpBase):
    pass

class GdPvp(GdPvpBase):
    id: int
    class Config:
        orm_mode = True

class GdChallengeModuleBase(BaseModel):
    gd_challenge_module_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_challenge_module: Optional[bool] = True
    gd_challenge_module_shortcode: Optional[str] = None
    gd_challenge_module_description: Optional[str] = None

class GdChallengeModuleCreate(GdChallengeModuleBase):
    pass

class GdChallengeModule(GdChallengeModuleBase):
    id: int
    class Config:
        orm_mode = True

class GdScenarioBase(BaseModel):
    gd_scenario_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_scenario: Optional[bool] = True
    gd_scenario_display_description: Optional[str] = None
    gd_scenario_condition_gameplay_formula: Optional[str] = None
    gd_scenario_description: Optional[str] = None

class GdScenarioCreate(GdScenarioBase):
    pass

class GdScenario(GdScenarioBase):
    id: int
    class Config:
        orm_mode = True

class GdChallengeConfigBase(BaseModel):
    gd_challenge_config_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_challenge_config: Optional[bool] = True
    linked_gd_challenge_module: Optional[int] = None
    linked_gd_game_screen: Optional[int] = None
    gd_challenge_config_start_date: Optional[datetime] = None
    gd_challenge_config_end_date: Optional[datetime] = None
    is_gd_challenge_config_repeatable: Optional[bool] = False
    gd_challenge_config_refresh_in_mins: Optional[int] = 0
    linked_gd_game_screen_for_return: Optional[int] = None
    linked_gd_segment: Optional[int] = None

class GdChallengeConfigCreate(GdChallengeConfigBase):
    pass

class GdChallengeConfig(GdChallengeConfigBase):
    id: int
    class Config:
        orm_mode = True

class GdChallengeBase(BaseModel):
    gd_challenge_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_challenge: Optional[bool] = True
    linked_gd_challenge_config: Optional[int] = None
    gd_challenge_priority: Optional[int] = 0
    gd_challenge_row: Optional[int] = 0
    gd_challenge_column: Optional[int] = 0
    gd_challenge_display_image_url: Optional[str] = None
    gd_challenge_is_entry_fee: Optional[bool] = False
    linked_gd_game_currency_entry_fee: Optional[int] = None
    gd_challenge_entry_quantity: Optional[int] = 0
    linked_gd_give_away_for_winner_csv: Optional[str] = None
    linked_gd_give_away_for_loser_csv: Optional[str] = None
    linked_gd_scenario: Optional[int] = None
    gd_challenge_is_user_rock: Optional[bool] = False
    linked_user_rock: Optional[int] = None
    linked_gd_rock_for_opponent: Optional[int] = None
    linked_gd_surface: Optional[int] = None
    linked_gd_environment: Optional[int] = None
    linked_gd_game_currency_unlock: Optional[int] = None
    gd_challenge_unlock_currency_quantity: Optional[int] = 0
    linked_gd_plotted_stone_config_csv: Optional[str] = None
    gd_challenge_is_tutorial: Optional[bool] = False
    linked_gd_challenge_for_unlock: Optional[int] = None
    gd_challenge_number_of_chances: Optional[int] = 1

class GdChallengeCreate(GdChallengeBase):
    pass

class GdChallenge(GdChallengeBase):
    id: int
    class Config:
        orm_mode = True

# --- Give Away Schemas ---

class GdGiveAwayBase(BaseModel):
    gd_give_away_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_give_away: Optional[bool] = True
    gd_give_away_display_name: Optional[str] = None
    gd_give_away_display_image_url: Optional[str] = None
    is_gd_give_away_probability: Optional[bool] = False

class GdGiveAwayCreate(GdGiveAwayBase):
    pass

class GdGiveAway(GdGiveAwayBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class GdGiveAwayItemBase(BaseModel):
    gd_give_away_item_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_give_away_item: Optional[bool] = True
    gd_give_away_item_type: Optional[str] = None
    linked_gd_item: Optional[str] = None
    gd_give_away_item_quantity: Optional[int] = 1
    gd_give_away_item_probability: Optional[float] = 0.0

class GdGiveAwayItemCreate(GdGiveAwayItemBase):
    pass

class GdGiveAwayItem(GdGiveAwayItemBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class GdGiveAwayItemMapperBase(BaseModel):
    gd_give_away_item_mapper_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_give_away_item_mapper: Optional[bool] = True
    linked_gd_give_away: Optional[int] = None
    linked_gd_give_away_item_csv: Optional[str] = None
    gd_give_away_item_mapper_priority: Optional[int] = 0

class GdGiveAwayItemMapperCreate(GdGiveAwayItemMapperBase):
    pass

class GdGiveAwayItemMapper(GdGiveAwayItemMapperBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class GdGiveAwayFeatureMapperBase(BaseModel):
    gd_give_away_feature_mapper_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_give_away_feature_mapper: Optional[bool] = True
    linked_gd_feature: Optional[int] = None
    is_gd_game_currency: Optional[bool] = False
    linked_gd_game_currency: Optional[int] = None
    game_currency_amount: Optional[int] = 0
    is_gd_real_money: Optional[bool] = False
    iap_value_android: Optional[str] = None
    iap_value_ios: Optional[str] = None
    iap_equivalent_inr: Optional[float] = 0.0
    is_ad_mob: Optional[bool] = False
    linked_gd_ad_mob: Optional[int] = None
    linked_gd_give_away: Optional[int] = None
    maximum_draw: Optional[int] = 1

class GdGiveAwayFeatureMapperCreate(GdGiveAwayFeatureMapperBase):
    pass

class GdGiveAwayFeatureMapper(GdGiveAwayFeatureMapperBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class GdAdMobBase(BaseModel):
    gd_ad_mob_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_ad_mob: Optional[bool] = True
    gd_ad_mob_short_code: Optional[str] = None
    gd_ad_mob_count_for_reward: Optional[int] = 1

class GdAdMobCreate(GdAdMobBase):
    pass

class GdAdMob(GdAdMobBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- Reward Highway Schemas ---
class GdRewardhighwayConfigBase(BaseModel):
    gd_rewardhighway_config_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_rewardhighway_config: Optional[bool] = True
    gd_rewardhighway_config_description: Optional[str] = None
    linked_currency_unit_for_progress: Optional[int] = None

class GdRewardhighwayConfigCreate(GdRewardhighwayConfigBase):
    pass

class GdRewardhighwayConfigUpdate(GdRewardhighwayConfigBase):
    pass

class GdRewardhighwayConfig(GdRewardhighwayConfigBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class GdRewardhighwayBase(BaseModel):
    gd_rewardhighway_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_rewardhighway: Optional[bool] = True
    linked_gd_rewardhighway_config: Optional[int] = None
    gd_rewardhighway_priority: Optional[int] = 0
    gd_rewardhighway_currency_value: Optional[int] = 0
    linked_gd_give_away: Optional[int] = None
    gd_rewardhighway_description: Optional[str] = None

class GdRewardhighwayCreate(GdRewardhighwayBase):
    pass

class GdRewardhighwayUpdate(GdRewardhighwayBase):
    pass

class GdRewardhighway(GdRewardhighwayBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- Global Config Schemas ---
class GdGameDetailsBase(BaseModel):
    gd_game_details_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_game_details: Optional[bool] = True
    gd_game_details_version: Optional[str] = None
    gd_game_details_forced_update_version: Optional[str] = None
    gd_game_details_on_maintenance: Optional[bool] = False
    gd_game_details_maintenance_off_date_time: Optional[datetime] = None
    gd_game_details_maintenance_message: Optional[str] = None
    gd_game_details_update_message: Optional[str] = None
    gd_game_details_is_android: Optional[bool] = False
    gd_game_details_is_ios: Optional[bool] = False
    gd_game_details_store_url: Optional[str] = None
    gd_game_details_asset_bundle: Optional[str] = None

class GdGameDetailsCreate(GdGameDetailsBase):
    pass

class GdGameDetailsUpdate(GdGameDetailsBase):
    pass

class GdGameDetails(GdGameDetailsBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- Leaderboard Schemas ---
class GdLeaderboardBase(BaseModel):
    gd_leaderboard_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_leaderboard: Optional[bool] = True
    gd_leaderboard_title: Optional[str] = None
    linked_gd_currency: Optional[int] = None
    gd_leaderboard_start_level: Optional[int] = 0
    gd_leaderboard_end_level: Optional[int] = 0
    gd_leaderboard_start_time: Optional[datetime] = None
    gd_leaderboard_end_time: Optional[datetime] = None
    gd_leaderboard_refresh_mins: Optional[int] = 5

class GdLeaderboardCreate(GdLeaderboardBase):
    pass

class GdLeaderboardUpdate(GdLeaderboardBase):
    pass

class GdLeaderboard(GdLeaderboardBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class GdLeaderboardRewardBase(BaseModel):
    gd_leaderboard_reward_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_leaderboard_reward: Optional[bool] = True
    gd_leaderboard_reward_title: Optional[str] = None
    linked_gd_give_away: Optional[int] = None
    linked_gd_leaderboard: Optional[int] = None
    gd_leaderboard_reward_start_rank: Optional[int] = 1
    gd_leaderboard_reward_end_rank: Optional[int] = 1

class GdLeaderboardRewardCreate(GdLeaderboardRewardBase):
    pass

class GdLeaderboardRewardUpdate(GdLeaderboardRewardBase):
    pass

class GdLeaderboardReward(GdLeaderboardRewardBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- Gameplay Stats & Leveling Schemas ---
class GdUserLevelBase(BaseModel):
    gd_user_level_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_user_level: Optional[bool] = True
    gd_user_level_number: Optional[int] = 1
    gd_user_level_min_xp: Optional[int] = 0
    gd_user_level_max_xp: Optional[int] = 0
    linked_gd_give_away_for_level: Optional[int] = None

class GdUserLevelCreate(GdUserLevelBase):
    pass

class GdUserLevelUpdate(GdUserLevelBase):
    pass

class GdUserLevel(GdUserLevelBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class GdGameplayStatsBase(BaseModel):
    gd_gameplay_stats_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_gameplay_stats: Optional[bool] = True
    gd_gameplay_stats_type: Optional[str] = None
    gd_gameplay_stats_short_code: Optional[str] = None
    gd_gameplay_stats_description: Optional[str] = None

class GdGameplayStatsCreate(GdGameplayStatsBase):
    pass

class GdGameplayStatsUpdate(GdGameplayStatsBase):
    pass

class GdGameplayStats(GdGameplayStatsBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class GdGameplayStatsXpMapperBase(BaseModel):
    gd_gameplay_stats_xp_mapper_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_gameplay_stats_xp_mapper: Optional[bool] = True
    linked_gd_gameplay_stats: Optional[int] = None
    xp_reward_count: Optional[int] = 0
    gd_gameplay_stats_xp_mapper_description: Optional[str] = None

class GdGameplayStatsXpMapperCreate(GdGameplayStatsXpMapperBase):
    pass

class GdGameplayStatsXpMapperUpdate(GdGameplayStatsXpMapperBase):
    pass

class GdGameplayStatsXpMapper(GdGameplayStatsXpMapperBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- User Data Schemas (ud_) ---

from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime

class UdUserMasterBase(BaseModel):
    auth_id: Optional[str] = None
    ud_user_master_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_ud_user_master: Optional[bool] = True
    ud_user_master_display_name: Optional[str] = None
    ud_user_master_display_name_change_instances: Optional[int] = 0
    is_ud_user_master_gmail: Optional[bool] = False
    ud_user_master_gmail_id: Optional[str] = None
    is_ud_user_master_apple: Optional[bool] = False
    ud_user_master_apple_id: Optional[str] = None
    is_ud_user_master_facebook: Optional[bool] = False
    ud_user_master_facebook_id: Optional[str] = None
    ud_user_master_ftue_step: Optional[int] = 0

class UdUserMasterCreate(UdUserMasterBase):
    pass

class UdUserMaster(UdUserMasterBase):
    id: int
    ud_user_master_created_at: datetime
    ud_user_master_last_updated: datetime
    model_config = ConfigDict(from_attributes=True)

class UdUserRockBase(BaseModel):
    ud_user_rock_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_ud_user_rock: Optional[bool] = True
    linked_ud_user_master: Optional[int] = None
    linked_gd_rock: Optional[int] = None
    is_ud_user_rock_expire: Optional[bool] = False
    ud_user_rock_expiry_date: Optional[datetime] = None
    ud_user_rock_weight: Optional[float] = 1.0
    ud_user_rock_spin_coefficient: Optional[float] = 1.0
    ud_user_rock_weight_curl_modifier: Optional[float] = 1.0
    ud_user_rock_rebound_elasticity: Optional[float] = 1.0
    ud_user_rock_max_speed: Optional[float] = 100.0
    ud_user_rock_size: Optional[float] = 1.0
    linked_gd_game_currency_repair: Optional[int] = None
    ud_user_rock_repair_quantity: Optional[int] = 0

class UdUserRockCreate(UdUserRockBase):
    pass

class UdUserRock(UdUserRockBase):
    id: int
    ud_user_rock_aquired_date: datetime
    model_config = ConfigDict(from_attributes=True)

class UdUserBroomBase(BaseModel):
    ud_user_broom_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_ud_user_broom: Optional[bool] = True
    linked_ud_user_master: Optional[int] = None
    linked_gd_broom: Optional[int] = None
    is_ud_user_broom_expire: Optional[bool] = False
    ud_user_broom_expiry_date: Optional[datetime] = None
    ud_user_broom_friction: Optional[float] = 1.0
    ud_user_broom_weight: Optional[float] = 1.0
    ud_user_broom_decay_coefficient: Optional[float] = 0.1
    linked_gd_game_currency_repair: Optional[int] = None
    ud_user_broom_repair_quantity: Optional[int] = 0

class UdUserBroomCreate(UdUserBroomBase):
    pass

class UdUserBroom(UdUserBroomBase):
    id: int
    ud_user_broom_aquired_date: datetime
    model_config = ConfigDict(from_attributes=True)

class UdUserRockPusherBase(BaseModel):
    ud_user_rock_pusher_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_ud_user_rock_pusher: Optional[bool] = True
    linked_ud_user_master: Optional[int] = None
    linked_gd_rock_pusher: Optional[int] = None
    is_ud_user_rock_pusher_expire: Optional[bool] = False
    ud_user_rock_pusher_expiry_date: Optional[datetime] = None
    ud_user_rock_pusher_force_multiplier: Optional[float] = 1.0
    ud_user_rock_pusher_uses_per_match: Optional[int] = 1
    ud_user_rock_pusher_duration_seconds: Optional[float] = 5.0
    ud_user_rock_pusher_cooldown_seconds: Optional[float] = 10.0
    linked_gd_game_currency_refill: Optional[int] = None
    ud_user_rock_pusher_refill_quantity: Optional[int] = 0

class UdUserRockPusherCreate(UdUserRockPusherBase):
    pass

class UdUserRockPusher(UdUserRockPusherBase):
    id: int
    ud_user_rock_pusher_aquired_date: datetime
    model_config = ConfigDict(from_attributes=True)

class UdUserLoadoutBase(BaseModel):
    linked_ud_user_master: Optional[int] = None
    linked_ud_user_rock: Optional[int] = None
    linked_ud_user_broom: Optional[int] = None
    linked_ud_user_rock_pusher: Optional[int] = None

class UdUserLoadoutCreate(UdUserLoadoutBase):
    pass

class UdUserLoadout(UdUserLoadoutBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class UdUserWalletBase(BaseModel):
    linked_ud_user_master: Optional[int] = None
    ud_user_wallet_currency_dictionary: Optional[Dict[str, Any]] = {}

class UdUserWalletCreate(UdUserWalletBase):
    pass

class UdUserWallet(UdUserWalletBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class UdUserStatsBase(BaseModel):
    linked_ud_user_master: Optional[int] = None
    ud_user_stats_xp: Optional[int] = 0
    ud_user_stats_total_match_played: Optional[int] = 0
    ud_user_stats_total_match_won: Optional[int] = 0
    ud_user_stats_current_win_streak: Optional[int] = 0
    ud_user_stats_total_spent_currencies_dictionary: Optional[Dict[str, Any]] = {}
    ud_user_stats_total_earned_currencies_dictionary: Optional[Dict[str, Any]] = {}
    ud_user_stats_gameplay_stats_dictionary: Optional[Dict[str, Any]] = {}

class UdUserStatsCreate(UdUserStatsBase):
    pass

class UdUserStats(UdUserStatsBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- Bot Data Schemas (gd_bot_) ---

class GdBotProfileBase(BaseModel):
    gd_bot_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_bot_profile: Optional[bool] = True
    gd_bot_display_image_url: Optional[str] = None
    gd_bot_difficulty_tier: Optional[int] = 1
    gd_bot_display_name: Optional[str] = None
    gd_bot_xp: Optional[int] = 0
    linked_gd_rock: Optional[int] = None
    linked_gd_broom: Optional[int] = None
    linked_gd_rock_pusher: Optional[int] = None

class GdBotProfileCreate(GdBotProfileBase):
    pass

class GdBotProfile(GdBotProfileBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class GdBotBehaviorBase(BaseModel):
    gd_bot_behavior_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    linked_gd_bot_profile: Optional[int] = None
    gd_bot_behavior_target_accuracy_percentage: Optional[float] = 100.0
    gd_bot_behavior_takeout_probability: Optional[float] = 0.0
    gd_bot_behavior_perfect_release_probability: Optional[float] = 0.0
    gd_bot_behavior_sweep_efficiency: Optional[float] = 1.0
    gd_bot_behavior_min_think_time_seconds: Optional[float] = 1.0
    gd_bot_behavior_max_think_time_seconds: Optional[float] = 3.0
    gd_bot_behaviour_guard_placement_probability: Optional[float] = 0.0
    gd_bot_behaviour_pusher_usage_probability: Optional[float] = 0.0
    gd_bot_behaviour_choke_probability: Optional[float] = 0.0
    gd_bot_behaviour_target_drift_variance: Optional[float] = 0.0
    gd_bot_behaviour_surrender_probability: Optional[float] = 0.0

class GdBotBehaviorCreate(GdBotBehaviorBase):
    pass

class GdBotBehavior(GdBotBehaviorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- Environment Data Schemas (gd_environment_) ---

class GdEnvironmentAssetBase(BaseModel):
    gd_environment_asset_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_environment_asset: Optional[bool] = True
    gd_environment_asset_short_code: Optional[str] = None

class GdEnvironmentAssetCreate(GdEnvironmentAssetBase):
    pass

class GdEnvironmentAsset(GdEnvironmentAssetBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class GdEnvironmentBase(BaseModel):
    gd_environment_name: Optional[str] = None
    is_enabled: Optional[bool] = True
    is_gd_environment: Optional[bool] = True
    linked_gd_environment_asset: Optional[int] = None
    gd_environment_ambient_light_hex: Optional[str] = None
    gd_environment_fog_density: Optional[float] = None
    gd_environment_is_rebound: Optional[bool] = False
    gd_environment_rebound_elasticity: Optional[float] = 1.0

class GdEnvironmentCreate(GdEnvironmentBase):
    pass

class GdEnvironment(GdEnvironmentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UdLeaderboardUserBase(BaseModel):
    linked_ud_user_master: Optional[int] = None
    linked_gd_bot_profile: Optional[int] = None
    linked_gd_leaderboard: Optional[int] = None
    score: Optional[float] = 0.0
    current_rank: Optional[int] = 0

class UdLeaderboardUserCreate(UdLeaderboardUserBase):
    pass

class UdLeaderboardUser(UdLeaderboardUserBase):
    id: int
    class Config:
        orm_mode = True
