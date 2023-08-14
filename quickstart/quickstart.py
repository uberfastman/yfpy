# -*- coding: utf-8 -*-
"""YFPY demo.

"""
__author__ = "Wren J. R. (uberfastman)"
__email__ = "uberfastman@uberfastman.dev"

import os
from logging import DEBUG
from pathlib import Path

from dotenv import load_dotenv

from yfpy import Data
from yfpy.logger import get_logger
from yfpy.query import YahooFantasySportsQuery

"""
Example public Yahoo league URL: "https://archive.fantasysports.yahoo.com/nfl/2014/729259"

Example vars using public Yahoo leagues still require auth through a personal Yahoo account: see README.md
"""

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# ENVIRONMENT SETUP # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# load .env file in order to read local environment variables
load_dotenv(dotenv_path=Path(__file__).parent.parent / "auth" / ".env")

# set directory location of private.json for authentication
auth_dir = Path(__file__).parent.parent / "auth"

# set target directory for data output
data_dir = Path(__file__).parent / "output"

# create YFPY Data instance for saving/loading data
data = Data(data_dir)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# VARIABLE SETUP  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# set desired season year
season = 2021
# season = 2012

# set desired week
chosen_week = 1

# set desired date
chosen_date = "2013-04-15"  # NHL - 2013 (for 2012)
# chosen_date = "2013-04-16"  # NHL - 2013
# chosen_date = "2021-10-25"  # NHL - 2021
# chosen_date = "2021-04-01"  # MLB - 2021
# chosen_date = "2022-04-10"  # MLB - 2022

# set desired Yahoo Fantasy Sports game code
game_code = "nfl"  # NFL
# game_code = "nhl"  # NHL
# game_code = "mlb"  # MLB

# set desired Yahoo Fantasy Sports game ID (see the get_all_yahoo_fantasy_game_keys query to retrieve values)
# game_id = 331  # NFL - 2014
# game_id = 348  # NFL - 2015 (testing for league with divisions)
# game_id = 390  # NFL - 2019
# game_id = 399  # NFL - 2020
game_id = 406  # NFL - 2021
# game_id = 303  # NHL - 2012
# game_id = 411  # NHL - 2021
# game_id = 404  # MLB - 2021
# game_id = 412  # MLB - 2022

# set desired Yahoo Fantasy Sports game key (see the get_all_yahoo_fantasy_game_keys query to retrieve values)
# game_key = "331"  # NFL - 2014
# game_key = "348"  # NFL - 2015 (testing for league with divisions)
# game_key = "390"  # NFL - 2019
# game_key = "399"  # NFL - 2020
game_key = "406"  # NFL - 2021
# game_key = "303"  # NHL - 2012
# game_key = "411"  # NHL - 2021
# game_key = "404"  # MLB - 2021
# game_key = "412"  # MLB - 2022

# set desired league ID (see README.md for finding value)
# league_id = "907359"  # NFL - 2015 (testing for league with divisions)
# league_id = "79230"  # NFL - 2019
# league_id = "655434"  # NFL - 2020
league_id = "413954"  # NFL - 2021
# league_id = "69624"  # NHL - 2012
# league_id = "101592"  # NHL - 2021
# league_id = "40134"  # MLB - 2021

# set desired team ID within desired league
team_id = 1  # NFL
# team_id = 2  # NHL (2012)

# set desired team name within desired league
team_name = "Legion"  # NFL
# team_name = "The Bateleurs"  # NHL (2012)

# set desired team ID within desired league
player_id = 7200  # NFL: Aaron Rodgers - 2020/2021
# player_id = 4588  # NHL: Braden Holtby - 2012
# player_id = 8205  # NHL: Jeffrey Viel - 2021
# player_id = 3637  # NHL: Alex Ovechkin - 2021
# player_id = 9897  # MLB: Tim Anderson - 2021/2022

# set the maximum number players you wish the get_league_players query to retrieve
league_player_limit = 101
# league_player_limit = 2610

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# QUERY SETUP # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# configure the Yahoo Fantasy Sports query (change all_output_as_json_str=True if you want to output JSON strings)
yahoo_query = YahooFantasySportsQuery(
    auth_dir,
    league_id,
    game_id=game_id,
    game_code=game_code,
    offline=False,
    all_output_as_json_str=False,
    consumer_key=os.environ["YFPY_CONSUMER_KEY"],
    consumer_secret=os.environ["YFPY_CONSUMER_SECRET"],
    browser_callback=True
)

# Manually override league key for example code to work
yahoo_query.league_key = f"{game_id}.l.{league_id}"

# Manually override player key for example code to work
player_key = f"{game_id}.p.{player_id}"

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# RUN QUERIES # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# print(repr(yahoo_query.get_all_yahoo_fantasy_game_keys()))
# print(repr(yahoo_query.get_game_key_by_season(season)))
# print(repr(yahoo_query.get_current_game_info()))
# print(repr(yahoo_query.get_current_game_metadata()))
# print(repr(yahoo_query.get_game_info_by_game_id(game_id)))
# print(repr(yahoo_query.get_game_metadata_by_game_id(game_id)))
# print(repr(yahoo_query.get_game_weeks_by_game_id(game_id)))
# print(repr(yahoo_query.get_game_stat_categories_by_game_id(game_id)))
# print(repr(yahoo_query.get_game_position_types_by_game_id(game_id)))
# print(repr(yahoo_query.get_game_roster_positions_by_game_id(game_id)))
# print(repr(yahoo_query.get_league_key(season)))
# print(repr(yahoo_query.get_current_user()))
# print(repr(yahoo_query.get_user_games()))
# print(repr(yahoo_query.get_user_leagues_by_game_key(game_key)))
# print(repr(yahoo_query.get_user_teams()))
# print(repr(yahoo_query.get_league_info()))
# print(repr(yahoo_query.get_league_metadata()))
# print(repr(yahoo_query.get_league_settings()))
# print(repr(yahoo_query.get_league_standings()))
# print(repr(yahoo_query.get_league_teams()))
# print(repr(yahoo_query.get_league_players(player_count_limit=10, player_count_start=0)))
# print(repr(yahoo_query.get_league_draft_results()))
# print(repr(yahoo_query.get_league_transactions()))
# print(repr(yahoo_query.get_league_scoreboard_by_week(chosen_week)))
# print(repr(yahoo_query.get_league_matchups_by_week(chosen_week)))
# print(repr(yahoo_query.get_team_info(team_id)))
# print(repr(yahoo_query.get_team_metadata(team_id)))
# print(repr(yahoo_query.get_team_stats(team_id)))
# print(repr(yahoo_query.get_team_stats_by_week(team_id, chosen_week)))
# print(repr(yahoo_query.get_team_standings(team_id)))
# print(repr(yahoo_query.get_team_roster_by_week(team_id, chosen_week)))
# print(repr(yahoo_query.get_team_roster_player_info_by_week(team_id, chosen_week)))
# # print(repr(yahoo_query.get_team_roster_player_info_by_date(team_id, chosen_date)))  # NHL/MLB/NBA
# print(repr(yahoo_query.get_team_roster_player_stats(team_id)))
# print(repr(yahoo_query.get_team_roster_player_stats_by_week(team_id, chosen_week)))
# print(repr(yahoo_query.get_team_draft_results(team_id)))
# print(repr(yahoo_query.get_team_matchups(team_id)))
# print(repr(yahoo_query.get_player_stats_for_season(player_key)))
# print(repr(yahoo_query.get_player_stats_for_season(player_key, limit_to_league_stats=False)))
# print(repr(yahoo_query.get_player_stats_by_week(player_key, chosen_week)))
# print(repr(yahoo_query.get_player_stats_by_week(player_key, chosen_week, limit_to_league_stats=False)))
# print(repr(yahoo_query.get_player_stats_by_date(player_key, chosen_date)))  # NHL/MLB/NBA
# print(repr(yahoo_query.get_player_stats_by_date(player_key, chosen_date, limit_to_league_stats=False)))  # NHL/MLB/NBA
# print(repr(yahoo_query.get_player_ownership(player_key)))
# print(repr(yahoo_query.get_player_percent_owned_by_week(player_key, chosen_week)))
# print(repr(yahoo_query.get_player_draft_analysis(player_key)))

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# CHECK FOR MISSING DATA FIELDS # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

logger = get_logger("yfpy.models", DEBUG)

# yahoo_query.get_all_yahoo_fantasy_game_keys()
# yahoo_query.get_game_key_by_season(season)
# yahoo_query.get_current_game_info()
# yahoo_query.get_current_game_metadata()
# yahoo_query.get_game_info_by_game_id(game_id)
# yahoo_query.get_game_metadata_by_game_id(game_id)
# yahoo_query.get_game_weeks_by_game_id(game_id)
# yahoo_query.get_game_stat_categories_by_game_id(game_id)
# yahoo_query.get_game_position_types_by_game_id(game_id)
# yahoo_query.get_game_roster_positions_by_game_id(game_id)
# yahoo_query.get_league_key(season)
# yahoo_query.get_current_user()
# yahoo_query.get_user_games()
# yahoo_query.get_user_leagues_by_game_key(game_key)
# yahoo_query.get_user_teams()
# yahoo_query.get_league_info()
# yahoo_query.get_league_metadata()
# yahoo_query.get_league_settings()
# yahoo_query.get_league_standings()
# yahoo_query.get_league_teams()
# yahoo_query.get_league_players(player_count_limit=10, player_count_start=0)
# yahoo_query.get_league_draft_results()
# yahoo_query.get_league_transactions()
# yahoo_query.get_league_scoreboard_by_week(chosen_week)
# yahoo_query.get_league_matchups_by_week(chosen_week)
# yahoo_query.get_team_info(team_id)
# yahoo_query.get_team_metadata(team_id)
# yahoo_query.get_team_stats(team_id)
# yahoo_query.get_team_stats_by_week(team_id, chosen_week)
# yahoo_query.get_team_standings(team_id)
# yahoo_query.get_team_roster_by_week(team_id, chosen_week)
# yahoo_query.get_team_roster_player_info_by_week(team_id, chosen_week)
# yahoo_query.get_team_roster_player_info_by_date(team_id, chosen_date)  # NHL/MLB/NBA
# yahoo_query.get_team_roster_player_stats(team_id)
# yahoo_query.get_team_roster_player_stats_by_week(team_id, chosen_week)
# yahoo_query.get_team_draft_results(team_id)
# yahoo_query.get_team_matchups(team_id)
# yahoo_query.get_player_stats_for_season(player_key))
# yahoo_query.get_player_stats_for_season(player_key, limit_to_league_stats=False))
# yahoo_query.get_player_stats_by_week(player_key, chosen_week)
# yahoo_query.get_player_stats_by_week(player_key, chosen_week, limit_to_league_stats=False)
# yahoo_query.get_player_stats_by_date(player_key, chosen_date,)  # NHL/MLB/NBA
# yahoo_query.get_player_stats_by_date(player_key, chosen_date, limit_to_league_stats=False)  # NHL/MLB/NBA
# yahoo_query.get_player_ownership(player_key)
# yahoo_query.get_player_percent_owned_by_week(player_key, chosen_week)
# yahoo_query.get_player_draft_analysis(player_key)
