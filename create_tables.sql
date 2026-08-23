-- Curling Mobile Game: Complete DDL Schema for Google Cloud SQL / PostgreSQL / Supabase
-- Generated automatically from finalized models

CREATE SEQUENCE global_game_data_id_seq;


CREATE TABLE gd_ad_mob (
	id INTEGER NOT NULL, 
	gd_ad_mob_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_gd_ad_mob BOOLEAN, 
	gd_ad_mob_short_code VARCHAR, 
	gd_ad_mob_count_for_reward INTEGER, 
	PRIMARY KEY (id)
)

;


CREATE TABLE gd_bot_profile (
	id INTEGER NOT NULL, 
	gd_bot_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_gd_bot_profile BOOLEAN, 
	gd_bot_display_name VARCHAR, 
	gd_bot_display_image_url VARCHAR, 
	gd_bot_difficulty_tier INTEGER, 
	gd_bot_xp INTEGER, 
	linked_gd_rock VARCHAR, 
	linked_gd_broom VARCHAR, 
	gd_bot_target_accuracy_percentage FLOAT, 
	gd_bot_takeout_probability FLOAT, 
	gd_bot_perfect_release_probability FLOAT, 
	gd_bot_sweep_efficiency FLOAT, 
	gd_bot_min_think_time_seconds FLOAT, 
	gd_bot_max_think_time_seconds FLOAT, 
	gd_bot_guard_placement_probability FLOAT, 
	gd_bot_choke_probability FLOAT, 
	gd_bot_target_drift_variance FLOAT, 
	gd_bot_surrender_probability FLOAT, 
	PRIMARY KEY (id)
)

;


CREATE TABLE gd_challenge_module (
	id INTEGER NOT NULL, 
	gd_challenge_module_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_gd_challenge_module BOOLEAN, 
	gd_challenge_module_shortcode VARCHAR, 
	gd_challenge_module_description VARCHAR, 
	PRIMARY KEY (id)
)

;


CREATE TABLE gd_environment_asset (
	id INTEGER NOT NULL, 
	gd_environment_asset_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_gd_environment_asset BOOLEAN, 
	gd_environment_asset VARCHAR, 
	PRIMARY KEY (id)
)

;


CREATE TABLE gd_feature (
	id INTEGER NOT NULL, 
	gd_feature_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_gd_feature BOOLEAN, 
	gd_feature_gameplay_short_code VARCHAR, 
	unlock_ftue_step INTEGER, 
	gd_feature_description VARCHAR, 
	PRIMARY KEY (id)
)

;


CREATE TABLE gd_game_currency (
	id INTEGER NOT NULL, 
	gd_game_currency_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_game_currency BOOLEAN, 
	gd_game_currency_asset VARCHAR, 
	is_asset BOOLEAN, 
	gd_game_currency_image_url VARCHAR, 
	gd_game_currency_display_name VARCHAR, 
	PRIMARY KEY (id)
)

;


CREATE TABLE gd_game_details (
	id INTEGER NOT NULL, 
	gd_game_details_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_gd_game_details BOOLEAN, 
	gd_game_details_version VARCHAR, 
	gd_game_details_forced_update_version VARCHAR, 
	gd_game_details_on_maintenance BOOLEAN, 
	gd_game_details_maintenance_off_date_time DATETIME, 
	gd_game_details_maintenance_message VARCHAR, 
	gd_game_details_update_message VARCHAR, 
	gd_game_details_is_android BOOLEAN, 
	gd_game_details_is_ios BOOLEAN, 
	gd_game_details_store_url VARCHAR, 
	gd_game_details_asset_bundle VARCHAR, 
	PRIMARY KEY (id)
)

;


CREATE TABLE gd_game_screen (
	id INTEGER NOT NULL, 
	gd_game_screen_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_gd_game_screen BOOLEAN, 
	gd_game_screen_asset VARCHAR, 
	is_gd_game_screen_asset BOOLEAN, 
	gd_game_screen_image_url VARCHAR, 
	is_scrollable_horizontal BOOLEAN, 
	is_scrollable_vertical BOOLEAN, 
	gd_game_screen_description VARCHAR, 
	PRIMARY KEY (id)
)

;


CREATE TABLE gd_gameflow_config (
	id INTEGER NOT NULL, 
	gd_gameflow_config_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_gd_gameflow_config BOOLEAN, 
	gd_gameflow_config_description VARCHAR, 
	PRIMARY KEY (id)
)

;


CREATE TABLE gd_gameplay_stats (
	id INTEGER NOT NULL, 
	gd_gameplay_stats_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_gd_gameplay_stats BOOLEAN, 
	gd_gameplay_stats_type VARCHAR, 
	gd_gameplay_stats_short_code VARCHAR, 
	gd_gameplay_stats_description VARCHAR, 
	PRIMARY KEY (id)
)

;


CREATE TABLE gd_give_away (
	id INTEGER NOT NULL, 
	gd_give_away_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_gd_give_away BOOLEAN, 
	gd_give_away_display_name VARCHAR, 
	gd_give_away_display_image_url VARCHAR, 
	is_gd_give_away_probability BOOLEAN, 
	PRIMARY KEY (id)
)

;


CREATE TABLE gd_give_away_item (
	id INTEGER NOT NULL, 
	gd_give_away_item_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_gd_give_away_item BOOLEAN, 
	gd_give_away_item_type VARCHAR, 
	linked_gd_item VARCHAR, 
	gd_give_away_item_quantity INTEGER, 
	gd_give_away_item_probability FLOAT, 
	PRIMARY KEY (id)
)

;


CREATE TABLE gd_material (
	id INTEGER NOT NULL, 
	gd_material_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_gd_material BOOLEAN, 
	gd_material_base_colour_hex VARCHAR, 
	gd_material_metallic FLOAT, 
	gd_material_roughness FLOAT, 
	PRIMARY KEY (id)
)

;


CREATE TABLE gd_plotted_stone_config (
	id INTEGER NOT NULL, 
	gd_plotted_stone_config_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_gd_plotted_stone_config BOOLEAN, 
	gd_plotted_stone_config_description VARCHAR, 
	PRIMARY KEY (id)
)

;


CREATE TABLE gd_pvp_module (
	id INTEGER NOT NULL, 
	gd_pvp_module_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_gd_pvp_module BOOLEAN, 
	gd_pvp_module_shortcode VARCHAR, 
	gd_pvp_module_description VARCHAR, 
	PRIMARY KEY (id)
)

;


CREATE TABLE gd_scenario (
	id INTEGER NOT NULL, 
	gd_scenario_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_gd_scenario BOOLEAN, 
	gd_scenario_display_description VARCHAR, 
	gd_scenario_condition_gameplay_formula VARCHAR, 
	gd_scenario_description VARCHAR, 
	PRIMARY KEY (id)
)

;


CREATE TABLE gd_segment (
	id INTEGER NOT NULL, 
	gd_segment_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_gd_segment BOOLEAN, 
	gd_segment_rule JSON, 
	gd_segment_description VARCHAR, 
	PRIMARY KEY (id)
)

;


CREATE TABLE gd_widget (
	id INTEGER NOT NULL, 
	gd_widget_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_gd_widget BOOLEAN, 
	gd_widget_asset VARCHAR, 
	is_gd_widget_asset BOOLEAN, 
	gd_widget_image_url VARCHAR, 
	gd_widget_multiplier FLOAT, 
	gd_widget_screen_description VARCHAR, 
	PRIMARY KEY (id)
)

;


CREATE TABLE ud_user_master (
	id INTEGER NOT NULL, 
	auth_id VARCHAR, 
	ud_user_master_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_ud_user_master BOOLEAN, 
	ud_user_master_display_name VARCHAR, 
	ud_user_master_display_name_change_instances INTEGER, 
	ud_user_master_created_at DATETIME, 
	ud_user_master_last_updated DATETIME, 
	is_ud_user_master_gmail BOOLEAN, 
	ud_user_master_gmail_id VARCHAR, 
	is_ud_user_master_apple BOOLEAN, 
	ud_user_master_apple_id VARCHAR, 
	is_ud_user_master_facebook BOOLEAN, 
	ud_user_master_facebook_id VARCHAR, 
	ud_user_master_ftue_step INTEGER, 
	PRIMARY KEY (id)
)

;


CREATE TABLE analysis_user_daily_activity (
	id INTEGER NOT NULL, 
	p_user_id INTEGER, 
	p_platform VARCHAR, 
	p_app_version VARCHAR, 
	p_first_seen_date DATETIME, 
	activity_date DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(p_user_id) REFERENCES ud_user_master (id) ON DELETE CASCADE
)

;


CREATE TABLE gd_broom_asset (
	id INTEGER NOT NULL, 
	gd_broom_asset_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_gd_broom_asset BOOLEAN, 
	gd_broom_asset_gamplay_short_code VARCHAR, 
	gd_broom_asset_desciription VARCHAR, 
	linked_material_for_handle INTEGER, 
	linked_material_for_broom_base INTEGER, 
	linked_material_for_broom_top INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(linked_material_for_handle) REFERENCES gd_material (id), 
	FOREIGN KEY(linked_material_for_broom_base) REFERENCES gd_material (id), 
	FOREIGN KEY(linked_material_for_broom_top) REFERENCES gd_material (id)
)

;


CREATE TABLE gd_environment (
	id INTEGER NOT NULL, 
	gd_environment_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_gd_environment BOOLEAN, 
	linked_gd_environment_asset INTEGER, 
	gd_environment_ambient_light_hex VARCHAR, 
	gd_environment_fog_density FLOAT, 
	gd_environment_is_rebound BOOLEAN, 
	gd_environment_rebound_elasticity FLOAT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(linked_gd_environment_asset) REFERENCES gd_environment_asset (id) ON DELETE CASCADE
)

;


CREATE TABLE gd_game_screen_widget_feature_mapper (
	id INTEGER NOT NULL, 
	gd_game_screen_widget_feature_mapper_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_gd_game_screen_widget_feature_mapper BOOLEAN, 
	linked_gd_game_screen INTEGER, 
	linked_gd_widget INTEGER, 
	linked_gd_feature INTEGER, 
	widget_x_axis FLOAT, 
	widget_y_axis FLOAT, 
	is_goto_gd_game_screen BOOLEAN, 
	linked_goto_gd_game_screen INTEGER, 
	linked_gd_segment INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(linked_gd_game_screen) REFERENCES gd_game_screen (id) ON DELETE CASCADE, 
	FOREIGN KEY(linked_gd_widget) REFERENCES gd_widget (id), 
	FOREIGN KEY(linked_gd_feature) REFERENCES gd_feature (id), 
	FOREIGN KEY(linked_goto_gd_game_screen) REFERENCES gd_game_screen (id) ON DELETE CASCADE, 
	FOREIGN KEY(linked_gd_segment) REFERENCES gd_segment (id) ON DELETE CASCADE
)

;


CREATE TABLE gd_gameflow (
	id INTEGER NOT NULL, 
	gd_gameflow_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_gd_gameflow BOOLEAN, 
	linked_gd_gameflow_config INTEGER, 
	gd_gameflow_priority INTEGER, 
	linked_gd_game_screen INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(linked_gd_gameflow_config) REFERENCES gd_gameflow_config (id), 
	FOREIGN KEY(linked_gd_game_screen) REFERENCES gd_game_screen (id) ON DELETE CASCADE
)

;


CREATE TABLE gd_gameplay_stats_xp_mapper (
	id INTEGER NOT NULL, 
	gd_gameplay_stats_xp_mapper_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_gd_gameplay_stats_xp_mapper BOOLEAN, 
	linked_gd_gameplay_stats INTEGER, 
	xp_reward_count INTEGER, 
	gd_gameplay_stats_xp_mapper_description VARCHAR, 
	PRIMARY KEY (id), 
	FOREIGN KEY(linked_gd_gameplay_stats) REFERENCES gd_gameplay_stats (id) ON DELETE CASCADE
)

;


CREATE TABLE gd_give_away_feature_mapper (
	id INTEGER NOT NULL, 
	gd_give_away_feature_mapper_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_gd_give_away_feature_mapper BOOLEAN, 
	linked_gd_feature INTEGER, 
	is_gd_game_currency BOOLEAN, 
	linked_gd_game_currency INTEGER, 
	game_currency_amount INTEGER, 
	is_gd_real_money BOOLEAN, 
	iap_value_android VARCHAR, 
	iap_value_ios VARCHAR, 
	iap_equivalent_usd FLOAT, 
	is_ad_mob BOOLEAN, 
	linked_gd_ad_mob INTEGER, 
	linked_gd_give_away INTEGER, 
	maximum_draw INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(linked_gd_feature) REFERENCES gd_feature (id), 
	FOREIGN KEY(linked_gd_game_currency) REFERENCES gd_game_currency (id), 
	FOREIGN KEY(linked_gd_ad_mob) REFERENCES gd_ad_mob (id), 
	FOREIGN KEY(linked_gd_give_away) REFERENCES gd_give_away (id)
)

;


CREATE TABLE gd_give_away_item_mapper (
	id INTEGER NOT NULL, 
	gd_give_away_item_mapper_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_gd_give_away_item_mapper BOOLEAN, 
	linked_gd_give_away INTEGER, 
	linked_gd_give_away_item_csv VARCHAR, 
	gd_give_away_item_mapper_priority INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(linked_gd_give_away) REFERENCES gd_give_away (id)
)

;


CREATE TABLE gd_leaderboard (
	id INTEGER NOT NULL, 
	gd_leaderboard_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_gd_leaderboard BOOLEAN, 
	gd_leaderboard_title VARCHAR, 
	linked_gd_currency INTEGER, 
	gd_leaderboard_start_level INTEGER, 
	gd_leaderboard_end_level INTEGER, 
	gd_leaderboard_start_time DATETIME, 
	gd_leaderboard_end_time DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(linked_gd_currency) REFERENCES gd_game_currency (id) ON DELETE CASCADE
)

;


CREATE TABLE gd_plotted_stone (
	id INTEGER NOT NULL, 
	gd_plotted_stone_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_gd_plotted_stone BOOLEAN, 
	linked_gd_plotted_stone_config INTEGER NOT NULL, 
	is_user_stone BOOLEAN, 
	gd_plotted_stone_x_axis FLOAT, 
	gd_plotted_stone_y_axis FLOAT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(linked_gd_plotted_stone_config) REFERENCES gd_plotted_stone_config (id) ON DELETE CASCADE
)

;


CREATE TABLE gd_rewardhighway_config (
	id INTEGER NOT NULL, 
	gd_rewardhighway_config_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_gd_rewardhighway_config BOOLEAN, 
	linked_currency_unit_for_progress INTEGER, 
	linked_gd_widget INTEGER, 
	gd_rewardhighway_config_description VARCHAR, 
	PRIMARY KEY (id), 
	FOREIGN KEY(linked_currency_unit_for_progress) REFERENCES gd_game_currency (id) ON DELETE CASCADE, 
	FOREIGN KEY(linked_gd_widget) REFERENCES gd_widget (id) ON DELETE CASCADE
)

;


CREATE TABLE gd_rock_asset (
	id INTEGER NOT NULL, 
	gd_rock_asset_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_gd_rock_asset BOOLEAN, 
	gd_rock_asset_gamplay_short_code VARCHAR, 
	gd_rock_asset_desciription VARCHAR, 
	linked_gd_material_for_stone INTEGER, 
	linked_gd_material_for_handle INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(linked_gd_material_for_stone) REFERENCES gd_material (id), 
	FOREIGN KEY(linked_gd_material_for_handle) REFERENCES gd_material (id)
)

;


CREATE TABLE gd_surface_material (
	id INTEGER NOT NULL, 
	gd_surface_material_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_gd_surface_material BOOLEAN, 
	gd_surface_material_asset VARCHAR, 
	linked_gd_material INTEGER, 
	gd_surface_material_description VARCHAR, 
	PRIMARY KEY (id), 
	FOREIGN KEY(linked_gd_material) REFERENCES gd_material (id)
)

;


CREATE TABLE gd_user_level (
	id INTEGER NOT NULL, 
	gd_user_level_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_gd_user_level BOOLEAN, 
	gd_user_level_number INTEGER, 
	gd_user_level_min_xp INTEGER, 
	gd_user_level_max_xp INTEGER, 
	linked_gd_give_away_for_level INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(linked_gd_give_away_for_level) REFERENCES gd_give_away (id) ON DELETE SET NULL
)

;


CREATE TABLE gd_user_message (
	id INTEGER NOT NULL, 
	gd_user_message_name VARCHAR, 
	is_enabled BOOLEAN, 
	sender_name VARCHAR, 
	message_title VARCHAR, 
	message_body VARCHAR, 
	linked_gd_give_away INTEGER, 
	created_at DATETIME, 
	expires_at DATETIME, 
	target_user_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(linked_gd_give_away) REFERENCES gd_give_away (id) ON DELETE SET NULL
)

;


CREATE TABLE ud_user_give_away (
	id INTEGER NOT NULL, 
	linked_ud_user_master INTEGER, 
	linked_gd_give_away INTEGER, 
	linked_gd_give_away_item INTEGER, 
	claimed_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(linked_ud_user_master) REFERENCES ud_user_master (id) ON DELETE CASCADE, 
	FOREIGN KEY(linked_gd_give_away) REFERENCES gd_give_away (id) ON DELETE CASCADE, 
	FOREIGN KEY(linked_gd_give_away_item) REFERENCES gd_give_away_item (id) ON DELETE CASCADE
)

;


CREATE TABLE ud_user_stats (
	id INTEGER NOT NULL, 
	linked_ud_user_master INTEGER, 
	ud_user_stats_xp INTEGER, 
	ud_user_stats_total_match_played INTEGER, 
	ud_user_stats_total_match_won INTEGER, 
	ud_user_stats_current_win_streak INTEGER, 
	ud_user_stats_total_spent_currencies_dictionary JSON, 
	ud_user_stats_total_earned_currencies_dictionary JSON, 
	ud_user_stats_gameplay_stats_dictionary JSON, 
	PRIMARY KEY (id), 
	UNIQUE (linked_ud_user_master), 
	FOREIGN KEY(linked_ud_user_master) REFERENCES ud_user_master (id) ON DELETE CASCADE
)

;


CREATE TABLE ud_user_wallet (
	id INTEGER NOT NULL, 
	linked_ud_user_master INTEGER, 
	ud_user_wallet_currency_dictionary JSON, 
	PRIMARY KEY (id), 
	UNIQUE (linked_ud_user_master), 
	FOREIGN KEY(linked_ud_user_master) REFERENCES ud_user_master (id) ON DELETE CASCADE
)

;


CREATE TABLE gd_broom (
	id INTEGER NOT NULL, 
	gd_broom_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_free BOOLEAN, 
	is_gd_broom BOOLEAN, 
	gd_broom_display_name VARCHAR, 
	linked_gd_broom_asset INTEGER, 
	gd_broom_friction FLOAT, 
	gd_broom_weight FLOAT, 
	gd_broom_decay_coefficient FLOAT, 
	gd_broom_decay_start_match FLOAT, 
	gd_broom_description VARCHAR, 
	PRIMARY KEY (id), 
	FOREIGN KEY(linked_gd_broom_asset) REFERENCES gd_broom_asset (id)
)

;


CREATE TABLE gd_challenge_config (
	id INTEGER NOT NULL, 
	gd_challenge_config_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_gd_challenge_config BOOLEAN, 
	linked_gd_challenge_module INTEGER, 
	linked_gd_game_screen INTEGER, 
	gd_challenge_config_start_date DATETIME, 
	gd_challenge_config_end_date DATETIME, 
	is_gd_challenge_config_repeatable BOOLEAN, 
	gd_challenge_config_refresh_in_mins INTEGER, 
	linked_gd_game_screen_for_return INTEGER, 
	linked_gd_segment INTEGER, 
	linked_gd_rewardhighway_config INTEGER, 
	widget_x_axis FLOAT, 
	widget_y_axis FLOAT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(linked_gd_challenge_module) REFERENCES gd_challenge_module (id) ON DELETE CASCADE, 
	FOREIGN KEY(linked_gd_game_screen) REFERENCES gd_game_screen (id) ON DELETE CASCADE, 
	FOREIGN KEY(linked_gd_game_screen_for_return) REFERENCES gd_game_screen (id) ON DELETE CASCADE, 
	FOREIGN KEY(linked_gd_segment) REFERENCES gd_segment (id) ON DELETE CASCADE, 
	FOREIGN KEY(linked_gd_rewardhighway_config) REFERENCES gd_rewardhighway_config (id) ON DELETE CASCADE
)

;


CREATE TABLE gd_leaderboard_reward (
	id INTEGER NOT NULL, 
	gd_leaderboard_reward_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_gd_leaderboard_reward BOOLEAN, 
	gd_leaderboard_reward_title VARCHAR, 
	linked_gd_give_away INTEGER, 
	linked_gd_leaderboard INTEGER, 
	gd_leaderboard_reward_start_rank INTEGER, 
	gd_leaderboard_reward_end_rank INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(linked_gd_give_away) REFERENCES gd_give_away (id) ON DELETE SET NULL, 
	FOREIGN KEY(linked_gd_leaderboard) REFERENCES gd_leaderboard (id) ON DELETE CASCADE
)

;


CREATE TABLE gd_pvp_config (
	id INTEGER NOT NULL, 
	gd_pvp_config_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_gd_pvp_config BOOLEAN, 
	linked_gd_pvp_module INTEGER, 
	linked_gd_game_screen INTEGER, 
	gd_pvp_config_start_date DATETIME, 
	gd_pvp_config_end_date DATETIME, 
	linked_gd_game_screen_for_return INTEGER, 
	linked_gd_segment INTEGER, 
	linked_gd_rewardhighway_config INTEGER, 
	widget_x_axis FLOAT, 
	widget_y_axis FLOAT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(linked_gd_pvp_module) REFERENCES gd_pvp_module (id) ON DELETE CASCADE, 
	FOREIGN KEY(linked_gd_game_screen) REFERENCES gd_game_screen (id) ON DELETE CASCADE, 
	FOREIGN KEY(linked_gd_game_screen_for_return) REFERENCES gd_game_screen (id) ON DELETE CASCADE, 
	FOREIGN KEY(linked_gd_segment) REFERENCES gd_segment (id) ON DELETE CASCADE, 
	FOREIGN KEY(linked_gd_rewardhighway_config) REFERENCES gd_rewardhighway_config (id) ON DELETE CASCADE
)

;


CREATE TABLE gd_rewardhighway (
	id INTEGER NOT NULL, 
	gd_rewardhighway_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_gd_rewardhighway BOOLEAN, 
	linked_gd_rewardhighway_config INTEGER, 
	gd_rewardhighway_priority INTEGER, 
	gd_rewardhighway_currency_value INTEGER, 
	linked_gd_give_away INTEGER, 
	image_url VARCHAR, 
	gd_rewardhighway_description VARCHAR, 
	PRIMARY KEY (id), 
	FOREIGN KEY(linked_gd_rewardhighway_config) REFERENCES gd_rewardhighway_config (id) ON DELETE CASCADE, 
	FOREIGN KEY(linked_gd_give_away) REFERENCES gd_give_away (id) ON DELETE CASCADE
)

;


CREATE TABLE gd_rock (
	id INTEGER NOT NULL, 
	gd_rock_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_free BOOLEAN, 
	is_gd_rock BOOLEAN, 
	gd_rock_display_name VARCHAR, 
	linked_gd_rock_asset INTEGER, 
	gd_rock_weight FLOAT, 
	gd_rock_friction FLOAT, 
	gd_rock_decay_coefficient FLOAT, 
	gd_rock_decay_start_match FLOAT, 
	gd_rock_curl_modifier FLOAT, 
	gd_rock_rebound_elasticity FLOAT, 
	gd_rock_max_speed FLOAT, 
	gd_rock_size FLOAT, 
	gd_rock_description VARCHAR, 
	PRIMARY KEY (id), 
	FOREIGN KEY(linked_gd_rock_asset) REFERENCES gd_rock_asset (id)
)

;


CREATE TABLE gd_surface (
	id INTEGER NOT NULL, 
	gd_surface_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_gd_surface BOOLEAN, 
	linked_gd_surface_material INTEGER, 
	gd_surface_display_name VARCHAR, 
	gd_surface_length FLOAT, 
	gd_surface_width FLOAT, 
	gd_surface_friction_coefficient FLOAT, 
	gd_surface_decay_friction_coefficient FLOAT, 
	gd_surface_target_radius FLOAT, 
	gd_surface_target_x_axis FLOAT, 
	gd_surface_target_y_axis FLOAT, 
	gd_surface_curl_factor FLOAT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(linked_gd_surface_material) REFERENCES gd_surface_material (id)
)

;


CREATE TABLE ud_leaderboard_user (
	id INTEGER NOT NULL, 
	linked_ud_user_master INTEGER, 
	linked_gd_bot_profile INTEGER, 
	linked_gd_leaderboard INTEGER, 
	score FLOAT, 
	current_rank INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(linked_ud_user_master) REFERENCES ud_user_master (id) ON DELETE CASCADE, 
	FOREIGN KEY(linked_gd_leaderboard) REFERENCES gd_leaderboard (id) ON DELETE CASCADE
)

;


CREATE TABLE ud_user_message_master (
	id INTEGER NOT NULL, 
	linked_ud_user_master INTEGER, 
	linked_gd_user_message INTEGER, 
	is_read BOOLEAN, 
	is_claimed BOOLEAN, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(linked_ud_user_master) REFERENCES ud_user_master (id) ON DELETE CASCADE, 
	FOREIGN KEY(linked_gd_user_message) REFERENCES gd_user_message (id) ON DELETE CASCADE
)

;


CREATE TABLE gd_challenge (
	id INTEGER NOT NULL, 
	gd_challenge_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_gd_challenge BOOLEAN, 
	linked_gd_challenge_config INTEGER, 
	gd_challenge_priority INTEGER, 
	gd_challenge_row INTEGER, 
	gd_challenge_column INTEGER, 
	gd_challenge_display_image_url VARCHAR, 
	gd_challenge_is_entry_fee BOOLEAN, 
	linked_gd_game_currency_entry_fee INTEGER, 
	gd_challenge_entry_quantity INTEGER, 
	linked_gd_give_away_for_winner_csv VARCHAR, 
	linked_gd_give_away_for_loser_csv VARCHAR, 
	linked_gd_scenario INTEGER, 
	gd_challenge_is_user_rock BOOLEAN, 
	linked_user_rock INTEGER, 
	linked_gd_rock_for_opponent INTEGER, 
	linked_gd_surface INTEGER, 
	linked_gd_environment INTEGER, 
	linked_gd_game_currency_unlock INTEGER, 
	gd_challenge_unlock_currency_quantity INTEGER, 
	linked_gd_plotted_stone_config_csv VARCHAR, 
	gd_challenge_is_tutorial BOOLEAN, 
	linked_gd_challenge_for_unlock INTEGER, 
	gd_challenge_number_of_chances INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(linked_gd_challenge_config) REFERENCES gd_challenge_config (id) ON DELETE CASCADE, 
	FOREIGN KEY(linked_gd_game_currency_entry_fee) REFERENCES gd_game_currency (id) ON DELETE CASCADE, 
	FOREIGN KEY(linked_gd_scenario) REFERENCES gd_scenario (id) ON DELETE CASCADE, 
	FOREIGN KEY(linked_user_rock) REFERENCES gd_rock (id) ON DELETE CASCADE, 
	FOREIGN KEY(linked_gd_rock_for_opponent) REFERENCES gd_rock (id) ON DELETE CASCADE, 
	FOREIGN KEY(linked_gd_surface) REFERENCES gd_surface (id) ON DELETE CASCADE, 
	FOREIGN KEY(linked_gd_environment) REFERENCES gd_environment (id) ON DELETE CASCADE, 
	FOREIGN KEY(linked_gd_game_currency_unlock) REFERENCES gd_game_currency (id) ON DELETE CASCADE, 
	FOREIGN KEY(linked_gd_challenge_for_unlock) REFERENCES gd_challenge (id) ON DELETE CASCADE
)

;


CREATE TABLE gd_pvp (
	id INTEGER NOT NULL, 
	gd_pvp_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_gd_pvp BOOLEAN, 
	linked_gd_pvp_config INTEGER, 
	gd_pvp_priority INTEGER, 
	gd_pvp_row INTEGER, 
	gd_pvp_column INTEGER, 
	gd_pvp_display_image_url VARCHAR, 
	linked_gd_game_currency INTEGER, 
	gd_pvp_entry_quantity INTEGER, 
	linked_gd_give_away_for_winner_csv VARCHAR, 
	linked_gd_give_away_for_loser_csv VARCHAR, 
	gd_pvp_chance_per_user INTEGER, 
	gd_pvp_time_per_chance FLOAT, 
	linked_gd_surface INTEGER, 
	linked_gd_environment INTEGER, 
	linked_gd_game_screen_return INTEGER, 
	linked_gd_plotted_stone_config_csv VARCHAR, 
	is_bot_strict BOOLEAN, 
	bot_rule VARCHAR, 
	enforce_bot_timeout VARCHAR, 
	gd_pvp_unlock_level INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(linked_gd_pvp_config) REFERENCES gd_pvp_config (id) ON DELETE CASCADE, 
	FOREIGN KEY(linked_gd_game_currency) REFERENCES gd_game_currency (id), 
	FOREIGN KEY(linked_gd_surface) REFERENCES gd_surface (id), 
	FOREIGN KEY(linked_gd_environment) REFERENCES gd_environment (id) ON DELETE CASCADE, 
	FOREIGN KEY(linked_gd_game_screen_return) REFERENCES gd_game_screen (id) ON DELETE CASCADE
)

;


CREATE TABLE ud_user_broom (
	id INTEGER NOT NULL, 
	ud_user_broom_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_ud_user_broom BOOLEAN, 
	linked_ud_user_master INTEGER, 
	linked_gd_broom INTEGER, 
	ud_user_broom_aquired_date DATETIME, 
	is_ud_user_broom_expire BOOLEAN, 
	ud_user_broom_expiry_date DATETIME, 
	ud_user_broom_friction FLOAT, 
	ud_user_broom_weight FLOAT, 
	ud_user_broom_decay_coefficient FLOAT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(linked_ud_user_master) REFERENCES ud_user_master (id) ON DELETE CASCADE, 
	FOREIGN KEY(linked_gd_broom) REFERENCES gd_broom (id) ON DELETE CASCADE
)

;


CREATE TABLE ud_user_rewardhighway (
	id INTEGER NOT NULL, 
	linked_ud_user_master INTEGER, 
	linked_gd_rewardhighway INTEGER, 
	claimed_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(linked_ud_user_master) REFERENCES ud_user_master (id) ON DELETE CASCADE, 
	FOREIGN KEY(linked_gd_rewardhighway) REFERENCES gd_rewardhighway (id) ON DELETE CASCADE
)

;


CREATE TABLE ud_user_rock (
	id INTEGER NOT NULL, 
	ud_user_rock_name VARCHAR, 
	is_enabled BOOLEAN, 
	is_ud_user_rock BOOLEAN, 
	linked_ud_user_master INTEGER, 
	linked_gd_rock INTEGER, 
	ud_user_rock_aquired_date DATETIME, 
	is_ud_user_rock_expire BOOLEAN, 
	ud_user_rock_expiry_date DATETIME, 
	ud_user_rock_weight FLOAT, 
	ud_user_rock_spin_coefficient FLOAT, 
	ud_user_rock_weight_curl_modifier FLOAT, 
	ud_user_rock_rebound_elasticity FLOAT, 
	ud_user_rock_max_speed FLOAT, 
	ud_user_rock_size FLOAT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(linked_ud_user_master) REFERENCES ud_user_master (id) ON DELETE CASCADE, 
	FOREIGN KEY(linked_gd_rock) REFERENCES gd_rock (id) ON DELETE CASCADE
)

;


CREATE TABLE ud_user_challenge (
	id INTEGER NOT NULL, 
	linked_ud_user_master INTEGER, 
	linked_gd_challenge INTEGER, 
	last_completed_at DATETIME, 
	is_completed BOOLEAN, 
	completion_count_with_user_stone JSON, 
	PRIMARY KEY (id), 
	FOREIGN KEY(linked_ud_user_master) REFERENCES ud_user_master (id) ON DELETE CASCADE, 
	FOREIGN KEY(linked_gd_challenge) REFERENCES gd_challenge (id) ON DELETE CASCADE
)

;


CREATE TABLE ud_user_loadout (
	id INTEGER NOT NULL, 
	linked_ud_user_master INTEGER, 
	linked_ud_user_rock INTEGER, 
	linked_ud_user_broom INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (linked_ud_user_master), 
	FOREIGN KEY(linked_ud_user_master) REFERENCES ud_user_master (id) ON DELETE CASCADE, 
	FOREIGN KEY(linked_ud_user_rock) REFERENCES ud_user_rock (id) ON DELETE SET NULL, 
	FOREIGN KEY(linked_ud_user_broom) REFERENCES ud_user_broom (id) ON DELETE SET NULL
)

;

