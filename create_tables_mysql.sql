-- ========================================================
-- Curling Mobile Game: Complete MySQL DDL Schema for Cloud SQL
-- Idempotent (CREATE TABLE IF NOT EXISTS)
-- ========================================================

CREATE DATABASE IF NOT EXISTS curling_db;
USE curling_db;

CREATE TABLE IF NOT EXISTS analysis_user_daily_activity (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	p_user_id INTEGER, 
	p_platform VARCHAR(255), 
	p_app_version VARCHAR(255), 
	p_first_seen_date DATETIME, 
	activity_date DATETIME, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_ad_mob (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_ad_mob_name VARCHAR(255), 
	is_enabled BOOL, 
	is_gd_ad_mob BOOL, 
	gd_ad_mob_short_code VARCHAR(255), 
	gd_ad_mob_count_for_reward INTEGER, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_bot_profile (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_bot_name VARCHAR(255), 
	is_enabled BOOL, 
	is_gd_bot_profile BOOL, 
	gd_bot_display_name VARCHAR(255), 
	gd_bot_display_image_url TEXT, 
	gd_bot_difficulty_tier INTEGER, 
	gd_bot_xp INTEGER, 
	linked_gd_rock VARCHAR(255), 
	linked_gd_broom VARCHAR(255), 
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
);

CREATE TABLE IF NOT EXISTS gd_broom (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_broom_name VARCHAR(255), 
	is_enabled BOOL, 
	is_free BOOL, 
	is_gd_broom BOOL, 
	gd_broom_display_name VARCHAR(255), 
	linked_gd_broom_asset INTEGER, 
	gd_broom_friction FLOAT, 
	gd_broom_weight FLOAT, 
	gd_broom_decay_coefficient FLOAT, 
	gd_broom_decay_start_match FLOAT, 
	gd_broom_description TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_broom_asset (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_broom_asset_name VARCHAR(255), 
	is_enabled BOOL, 
	is_gd_broom_asset BOOL, 
	gd_broom_asset_gamplay_short_code VARCHAR(255), 
	gd_broom_asset_desciription VARCHAR(255), 
	linked_material_for_handle INTEGER, 
	linked_material_for_broom_base INTEGER, 
	linked_material_for_broom_top INTEGER, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_challenge (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_challenge_name VARCHAR(255), 
	is_enabled BOOL, 
	is_gd_challenge BOOL, 
	linked_gd_challenge_config INTEGER, 
	gd_challenge_priority INTEGER, 
	gd_challenge_row INTEGER, 
	gd_challenge_column INTEGER, 
	gd_challenge_display_image_url TEXT, 
	gd_challenge_is_entry_fee BOOL, 
	linked_gd_game_currency_entry_fee INTEGER, 
	gd_challenge_entry_quantity INTEGER, 
	linked_gd_give_away_for_winner_csv VARCHAR(255), 
	linked_gd_give_away_for_loser_csv VARCHAR(255), 
	linked_gd_scenario INTEGER, 
	gd_challenge_is_user_rock BOOL, 
	linked_user_rock INTEGER, 
	linked_gd_rock_for_opponent INTEGER, 
	linked_gd_surface INTEGER, 
	linked_gd_environment INTEGER, 
	linked_gd_game_currency_unlock INTEGER, 
	gd_challenge_unlock_currency_quantity INTEGER, 
	linked_gd_plotted_stone_config_csv VARCHAR(255), 
	gd_challenge_is_tutorial BOOL, 
	linked_gd_challenge_for_unlock INTEGER, 
	gd_challenge_number_of_chances INTEGER, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_challenge_config (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_challenge_config_name VARCHAR(255), 
	is_enabled BOOL, 
	is_gd_challenge_config BOOL, 
	linked_gd_challenge_module INTEGER, 
	linked_gd_game_screen INTEGER, 
	gd_challenge_config_start_date DATETIME, 
	gd_challenge_config_end_date DATETIME, 
	is_gd_challenge_config_repeatable BOOL, 
	gd_challenge_config_refresh_in_mins INTEGER, 
	linked_gd_game_screen_for_return INTEGER, 
	linked_gd_segment INTEGER, 
	linked_gd_rewardhighway_config INTEGER, 
	widget_x_axis FLOAT, 
	widget_y_axis FLOAT, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_challenge_module (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_challenge_module_name VARCHAR(255), 
	is_enabled BOOL, 
	is_gd_challenge_module BOOL, 
	gd_challenge_module_shortcode VARCHAR(255), 
	gd_challenge_module_description TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_environment (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_environment_name VARCHAR(255), 
	is_enabled BOOL, 
	is_gd_environment BOOL, 
	linked_gd_environment_asset INTEGER, 
	gd_environment_ambient_light_hex VARCHAR(255), 
	gd_environment_fog_density FLOAT, 
	gd_environment_is_rebound BOOL, 
	gd_environment_rebound_elasticity FLOAT, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_environment_asset (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_environment_asset_name VARCHAR(255), 
	is_enabled BOOL, 
	is_gd_environment_asset BOOL, 
	gd_environment_asset VARCHAR(255), 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_feature (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_feature_name VARCHAR(255), 
	is_enabled BOOL, 
	is_gd_feature BOOL, 
	gd_feature_gameplay_short_code VARCHAR(255), 
	unlock_ftue_step INTEGER, 
	gd_feature_description TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_game_currency (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_game_currency_name VARCHAR(255), 
	is_enabled BOOL, 
	is_game_currency BOOL, 
	gd_game_currency_asset VARCHAR(255), 
	is_asset BOOL, 
	gd_game_currency_image_url TEXT, 
	gd_game_currency_display_name VARCHAR(255), 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_game_details (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_game_details_name VARCHAR(255), 
	is_enabled BOOL, 
	is_gd_game_details BOOL, 
	gd_game_details_version VARCHAR(255), 
	gd_game_details_forced_update_version VARCHAR(255), 
	gd_game_details_on_maintenance BOOL, 
	gd_game_details_maintenance_off_date_time DATETIME, 
	gd_game_details_maintenance_message VARCHAR(255), 
	gd_game_details_update_message VARCHAR(255), 
	gd_game_details_is_android BOOL, 
	gd_game_details_is_ios BOOL, 
	gd_game_details_store_url TEXT, 
	gd_game_details_asset_bundle VARCHAR(255), 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_game_screen (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_game_screen_name VARCHAR(255), 
	is_enabled BOOL, 
	is_gd_game_screen BOOL, 
	gd_game_screen_asset VARCHAR(255), 
	is_gd_game_screen_asset BOOL, 
	gd_game_screen_image_url TEXT, 
	is_scrollable_horizontal BOOL, 
	is_scrollable_vertical BOOL, 
	gd_game_screen_description TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_game_screen_widget_feature_mapper (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_game_screen_widget_feature_mapper_name VARCHAR(255), 
	is_enabled BOOL, 
	is_gd_game_screen_widget_feature_mapper BOOL, 
	linked_gd_game_screen INTEGER, 
	linked_gd_widget INTEGER, 
	linked_gd_feature INTEGER, 
	widget_x_axis FLOAT, 
	widget_y_axis FLOAT, 
	is_goto_gd_game_screen BOOL, 
	linked_goto_gd_game_screen INTEGER, 
	linked_gd_segment INTEGER, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_gameflow (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_gameflow_name VARCHAR(255), 
	is_enabled BOOL, 
	is_gd_gameflow BOOL, 
	linked_gd_gameflow_config INTEGER, 
	gd_gameflow_priority INTEGER, 
	linked_gd_game_screen INTEGER, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_gameflow_config (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_gameflow_config_name VARCHAR(255), 
	is_enabled BOOL, 
	is_gd_gameflow_config BOOL, 
	gd_gameflow_config_description TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_gameplay_stats (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_gameplay_stats_name VARCHAR(255), 
	is_enabled BOOL, 
	is_gd_gameplay_stats BOOL, 
	gd_gameplay_stats_type VARCHAR(255), 
	gd_gameplay_stats_short_code VARCHAR(255), 
	gd_gameplay_stats_description TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_gameplay_stats_xp_mapper (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_gameplay_stats_xp_mapper_name VARCHAR(255), 
	is_enabled BOOL, 
	is_gd_gameplay_stats_xp_mapper BOOL, 
	linked_gd_gameplay_stats INTEGER, 
	xp_reward_count INTEGER, 
	gd_gameplay_stats_xp_mapper_description TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_give_away (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_give_away_name VARCHAR(255), 
	is_enabled BOOL, 
	is_gd_give_away BOOL, 
	gd_give_away_display_name VARCHAR(255), 
	gd_give_away_display_image_url TEXT, 
	is_gd_give_away_probability BOOL, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_give_away_feature_mapper (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_give_away_feature_mapper_name VARCHAR(255), 
	is_enabled BOOL, 
	is_gd_give_away_feature_mapper BOOL, 
	linked_gd_feature INTEGER, 
	is_gd_game_currency BOOL, 
	linked_gd_game_currency INTEGER, 
	game_currency_amount INTEGER, 
	is_gd_real_money BOOL, 
	iap_value_android VARCHAR(255), 
	iap_value_ios VARCHAR(255), 
	iap_equivalent_usd FLOAT, 
	is_ad_mob BOOL, 
	linked_gd_ad_mob INTEGER, 
	linked_gd_give_away INTEGER, 
	maximum_draw INTEGER, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_give_away_item (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_give_away_item_name VARCHAR(255), 
	is_enabled BOOL, 
	is_gd_give_away_item BOOL, 
	gd_give_away_item_type VARCHAR(255), 
	linked_gd_item VARCHAR(255), 
	gd_give_away_item_quantity INTEGER, 
	gd_give_away_item_probability FLOAT, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_give_away_item_mapper (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_give_away_item_mapper_name VARCHAR(255), 
	is_enabled BOOL, 
	is_gd_give_away_item_mapper BOOL, 
	linked_gd_give_away INTEGER, 
	linked_gd_give_away_item_csv VARCHAR(255), 
	gd_give_away_item_mapper_priority INTEGER, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_leaderboard (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_leaderboard_name VARCHAR(255), 
	is_enabled BOOL, 
	is_gd_leaderboard BOOL, 
	gd_leaderboard_title VARCHAR(255), 
	linked_gd_currency INTEGER, 
	gd_leaderboard_start_level INTEGER, 
	gd_leaderboard_end_level INTEGER, 
	gd_leaderboard_start_time DATETIME, 
	gd_leaderboard_end_time DATETIME, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_leaderboard_reward (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_leaderboard_reward_name VARCHAR(255), 
	is_enabled BOOL, 
	is_gd_leaderboard_reward BOOL, 
	gd_leaderboard_reward_title VARCHAR(255), 
	linked_gd_give_away INTEGER, 
	linked_gd_leaderboard INTEGER, 
	gd_leaderboard_reward_start_rank INTEGER, 
	gd_leaderboard_reward_end_rank INTEGER, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_material (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_material_name VARCHAR(255), 
	is_enabled BOOL, 
	is_gd_material BOOL, 
	gd_material_base_colour_hex VARCHAR(255), 
	gd_material_metallic FLOAT, 
	gd_material_roughness FLOAT, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_plotted_stone (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_plotted_stone_name VARCHAR(255), 
	is_enabled BOOL, 
	is_gd_plotted_stone BOOL, 
	linked_gd_plotted_stone_config INTEGER NOT NULL, 
	is_user_stone BOOL, 
	gd_plotted_stone_x_axis FLOAT, 
	gd_plotted_stone_y_axis FLOAT, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_plotted_stone_config (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_plotted_stone_config_name VARCHAR(255), 
	is_enabled BOOL, 
	is_gd_plotted_stone_config BOOL, 
	gd_plotted_stone_config_description TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_pvp (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_pvp_name VARCHAR(255), 
	is_enabled BOOL, 
	is_gd_pvp BOOL, 
	linked_gd_pvp_config INTEGER, 
	gd_pvp_priority INTEGER, 
	gd_pvp_row INTEGER, 
	gd_pvp_column INTEGER, 
	gd_pvp_display_image_url TEXT, 
	linked_gd_game_currency INTEGER, 
	gd_pvp_entry_quantity INTEGER, 
	linked_gd_give_away_for_winner_csv VARCHAR(255), 
	linked_gd_give_away_for_loser_csv VARCHAR(255), 
	gd_pvp_chance_per_user INTEGER, 
	gd_pvp_time_per_chance FLOAT, 
	linked_gd_surface INTEGER, 
	linked_gd_environment INTEGER, 
	linked_gd_game_screen_return INTEGER, 
	linked_gd_plotted_stone_config_csv VARCHAR(255), 
	is_bot_strict BOOL, 
	bot_rule TEXT, 
	enforce_bot_timeout VARCHAR(255), 
	gd_pvp_unlock_level INTEGER, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_pvp_config (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_pvp_config_name VARCHAR(255), 
	is_enabled BOOL, 
	is_gd_pvp_config BOOL, 
	linked_gd_pvp_module INTEGER, 
	linked_gd_game_screen INTEGER, 
	gd_pvp_config_start_date DATETIME, 
	gd_pvp_config_end_date DATETIME, 
	linked_gd_game_screen_for_return INTEGER, 
	linked_gd_segment INTEGER, 
	linked_gd_rewardhighway_config INTEGER, 
	widget_x_axis FLOAT, 
	widget_y_axis FLOAT, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_pvp_module (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_pvp_module_name VARCHAR(255), 
	is_enabled BOOL, 
	is_gd_pvp_module BOOL, 
	gd_pvp_module_shortcode VARCHAR(255), 
	gd_pvp_module_description TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_rewardhighway (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_rewardhighway_name VARCHAR(255), 
	is_enabled BOOL, 
	is_gd_rewardhighway BOOL, 
	linked_gd_rewardhighway_config INTEGER, 
	gd_rewardhighway_priority INTEGER, 
	gd_rewardhighway_currency_value INTEGER, 
	linked_gd_give_away INTEGER, 
	image_url TEXT, 
	gd_rewardhighway_description TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_rewardhighway_config (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_rewardhighway_config_name VARCHAR(255), 
	is_enabled BOOL, 
	is_gd_rewardhighway_config BOOL, 
	linked_currency_unit_for_progress INTEGER, 
	linked_gd_widget INTEGER, 
	gd_rewardhighway_config_description TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_rock (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_rock_name VARCHAR(255), 
	is_enabled BOOL, 
	is_free BOOL, 
	is_gd_rock BOOL, 
	gd_rock_display_name VARCHAR(255), 
	linked_gd_rock_asset INTEGER, 
	gd_rock_weight FLOAT, 
	gd_rock_friction FLOAT, 
	gd_rock_decay_coefficient FLOAT, 
	gd_rock_decay_start_match FLOAT, 
	gd_rock_curl_modifier FLOAT, 
	gd_rock_rebound_elasticity FLOAT, 
	gd_rock_max_speed FLOAT, 
	gd_rock_size FLOAT, 
	gd_rock_description TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_rock_asset (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_rock_asset_name VARCHAR(255), 
	is_enabled BOOL, 
	is_gd_rock_asset BOOL, 
	gd_rock_asset_gamplay_short_code VARCHAR(255), 
	gd_rock_asset_desciription VARCHAR(255), 
	linked_gd_material_for_stone INTEGER, 
	linked_gd_material_for_handle INTEGER, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_scenario (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_scenario_name VARCHAR(255), 
	is_enabled BOOL, 
	is_gd_scenario BOOL, 
	gd_scenario_display_description TEXT, 
	gd_scenario_condition_gameplay_formula TEXT, 
	gd_scenario_description TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_segment (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_segment_name VARCHAR(255), 
	is_enabled BOOL, 
	is_gd_segment BOOL, 
	gd_segment_rule JSON, 
	gd_segment_description TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_surface (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_surface_name VARCHAR(255), 
	is_enabled BOOL, 
	is_gd_surface BOOL, 
	linked_gd_surface_material INTEGER, 
	gd_surface_display_name VARCHAR(255), 
	gd_surface_length FLOAT, 
	gd_surface_width FLOAT, 
	gd_surface_friction_coefficient FLOAT, 
	gd_surface_decay_friction_coefficient FLOAT, 
	gd_surface_target_radius FLOAT, 
	gd_surface_target_x_axis FLOAT, 
	gd_surface_target_y_axis FLOAT, 
	gd_surface_curl_factor FLOAT, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_surface_material (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_surface_material_name VARCHAR(255), 
	is_enabled BOOL, 
	is_gd_surface_material BOOL, 
	gd_surface_material_asset VARCHAR(255), 
	linked_gd_material INTEGER, 
	gd_surface_material_description TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_user_level (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_user_level_name VARCHAR(255), 
	is_enabled BOOL, 
	is_gd_user_level BOOL, 
	gd_user_level_number INTEGER, 
	gd_user_level_min_xp INTEGER, 
	gd_user_level_max_xp INTEGER, 
	linked_gd_give_away_for_level INTEGER, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_user_message (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_user_message_name VARCHAR(255), 
	is_enabled BOOL, 
	sender_name VARCHAR(255), 
	message_title VARCHAR(255), 
	message_body TEXT, 
	linked_gd_give_away INTEGER, 
	created_at DATETIME, 
	expires_at DATETIME, 
	target_user_id INTEGER, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS gd_widget (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	gd_widget_name VARCHAR(255), 
	is_enabled BOOL, 
	is_gd_widget BOOL, 
	gd_widget_asset VARCHAR(255), 
	is_gd_widget_asset BOOL, 
	gd_widget_image_url TEXT, 
	gd_widget_multiplier FLOAT, 
	gd_widget_screen_description TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS ud_leaderboard_user (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	linked_ud_user_master INTEGER, 
	linked_gd_bot_profile INTEGER, 
	linked_gd_leaderboard INTEGER, 
	score FLOAT, 
	current_rank INTEGER, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS ud_user_broom (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	ud_user_broom_name VARCHAR(255), 
	is_enabled BOOL, 
	is_ud_user_broom BOOL, 
	linked_ud_user_master INTEGER, 
	linked_gd_broom INTEGER, 
	ud_user_broom_aquired_date DATETIME, 
	is_ud_user_broom_expire BOOL, 
	ud_user_broom_expiry_date DATETIME, 
	ud_user_broom_friction FLOAT, 
	ud_user_broom_weight FLOAT, 
	ud_user_broom_decay_coefficient FLOAT, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS ud_user_challenge (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	linked_ud_user_master INTEGER, 
	linked_gd_challenge INTEGER, 
	last_completed_at DATETIME, 
	is_completed BOOL, 
	completion_count_with_user_stone JSON, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS ud_user_give_away (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	linked_ud_user_master INTEGER, 
	linked_gd_give_away INTEGER, 
	linked_gd_give_away_item INTEGER, 
	claimed_at DATETIME, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS ud_user_loadout (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	linked_ud_user_master INTEGER, 
	linked_ud_user_rock INTEGER, 
	linked_ud_user_broom INTEGER, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS ud_user_master (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	auth_id VARCHAR(255), 
	ud_user_master_name VARCHAR(255), 
	is_enabled BOOL, 
	is_ud_user_master BOOL, 
	ud_user_master_display_name VARCHAR(255), 
	ud_user_master_display_name_change_instances INTEGER, 
	ud_user_master_created_at DATETIME, 
	ud_user_master_last_updated DATETIME, 
	is_ud_user_master_gmail BOOL, 
	ud_user_master_gmail_id VARCHAR(255), 
	is_ud_user_master_apple BOOL, 
	ud_user_master_apple_id VARCHAR(255), 
	is_ud_user_master_facebook BOOL, 
	ud_user_master_facebook_id VARCHAR(255), 
	ud_user_master_ftue_step INTEGER, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS ud_user_message_master (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	linked_ud_user_master INTEGER, 
	linked_gd_user_message INTEGER, 
	is_read BOOL, 
	is_claimed BOOL, 
	created_at DATETIME, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS ud_user_rewardhighway (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	linked_ud_user_master INTEGER, 
	linked_gd_rewardhighway INTEGER, 
	claimed_at DATETIME, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS ud_user_rock (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	ud_user_rock_name VARCHAR(255), 
	is_enabled BOOL, 
	is_ud_user_rock BOOL, 
	linked_ud_user_master INTEGER, 
	linked_gd_rock INTEGER, 
	ud_user_rock_aquired_date DATETIME, 
	is_ud_user_rock_expire BOOL, 
	ud_user_rock_expiry_date DATETIME, 
	ud_user_rock_weight FLOAT, 
	ud_user_rock_spin_coefficient FLOAT, 
	ud_user_rock_weight_curl_modifier FLOAT, 
	ud_user_rock_rebound_elasticity FLOAT, 
	ud_user_rock_max_speed FLOAT, 
	ud_user_rock_size FLOAT, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS ud_user_stats (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	linked_ud_user_master INTEGER, 
	ud_user_stats_xp INTEGER, 
	ud_user_stats_total_match_played INTEGER, 
	ud_user_stats_total_match_won INTEGER, 
	ud_user_stats_current_win_streak INTEGER, 
	ud_user_stats_total_spent_currencies_dictionary JSON, 
	ud_user_stats_total_earned_currencies_dictionary JSON, 
	ud_user_stats_gameplay_stats_dictionary JSON, 
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS ud_user_wallet (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	linked_ud_user_master INTEGER, 
	ud_user_wallet_currency_dictionary JSON, 
	PRIMARY KEY (id)
);

