# -*- coding: utf-8 -*-
"""YFPY demo.

"""
__author__ = "Wren J. R. (uberfastman)"
__email__ = "uberfastman@uberfastman.dev"

import os
import sys
from logging import DEBUG
from pathlib import Path

project_dir = Path(__file__).parent.parent
sys.path.insert(0, str(project_dir))

from yfpy import Data  # noqa: E402
from yfpy.logger import get_logger  # noqa: E402
from yfpy.query import YahooFantasySportsQuery  # noqa: E402

"""
Example public Yahoo league URL: "https://archive.fantasysports.yahoo.com/nfl/2014/729259"

Example vars using public Yahoo leagues still require auth through a personal Yahoo account: see README.md
"""

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# ENVIRONMENT SETUP # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# set target directory for data output
data_dir = Path(__file__).parent / "output"

# create YFPY Data instance for saving/loading data
data = Data(data_dir)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# VARIABLE SETUP  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# set desired season year
def get_season():
    # season = 2012
    # season = 2013
    # season = 2014
    # season = 2015
    # season = 2016
    # season = 2017
    # season = 2018
    # season = 2019
    # season = 2020
    # season = 2021
    # season = 2022
    # season = 2023
    season = 2024
    return season


test_season = get_season()


# set desired week
def get_chosen_week():
    chosen_week = 1
    return chosen_week


test_chosen_week = get_chosen_week()


# set desired date
def get_chosen_date():
    # HOCKEY
    # chosen_date = "2013-04-15"  # NHL - 2013 (for 2012 season)
    chosen_date = "2021-10-25"  # NHL - 2021

    # BASEBALL
    # chosen_date = "2021-04-01"  # MLB - 2021
    # chosen_date = "2022-04-10"  # MLB - 2022

    # BASKETBALL
    # chosen_date = "2023-11-26"

    return chosen_date


test_chosen_date = get_chosen_date()


# set desired Yahoo Fantasy Sports game code
def get_game_code():
    # FOOTBALL
    game_code = "nfl"  # NFL

    # HOCKEY
    # game_code = "nhl"  # NHL

    # BASEBALL
    # game_code = "mlb"  # MLB

    # BASKETBALL
    # game_code = "nba"  # NBA

    return game_code


test_game_code = get_game_code()


# set desired Yahoo Fantasy Sports game ID (see the get_all_yahoo_fantasy_game_keys query to retrieve values)
def get_game_id():
    # FOOTBALL
    # game_id = 331  # NFL - 2014
    # game_id = 348  # NFL - 2015 (divisions)
    # game_id = 359  # NFL - 2016
    # game_id = 371  # NFL - 2017
    # game_id = 380  # NFL - 2018
    # game_id = 390  # NFL - 2019
    # game_id = 399  # NFL - 2020
    # game_id = 406  # NFL - 2021
    # game_id = 414  # NFL - 2022 (divisions)
    # game_id = 423  # NFL - 2023
    game_id = 449  # NFL - 2024

    # HOCKEY
    # game_id = 303  # NHL - 2012
    # game_id = 411  # NHL - 2021
    # game_id = 427  # NHL - 2023

    # BASEBALL
    # game_id = 404  # MLB - 2021
    # game_id = 412  # MLB - 2022

    # BASKETBALL
    # game_id = 428  # NBA - 2023

    return game_id


test_game_id = get_game_id()


# set desired Yahoo Fantasy Sports game key (see the get_all_yahoo_fantasy_game_keys query to retrieve values)
def get_game_key():
    # FOOTBALL
    # game_key = "331"  # NFL - 2014
    # game_key = "348"  # NFL - 2015 (divisions)
    # game_key = "359"  # NFL - 2016
    # game_key = "371"  # NFL - 2017
    # game_key = "380"  # NFL - 2018
    # game_key = "390"  # NFL - 2019
    # game_key = "399"  # NFL - 2020
    # game_key = "406"  # NFL - 2021
    # game_key = "414"  # NFL - 2022 (divisions)
    # game_key = "423"  # NFL - 2023
    game_key = "449"  # NFL - 2024

    # HOCKEY
    # game_key = "303"  # NHL - 2012
    # game_key = "411"  # NHL - 2021
    # game_key = "427"  # NHL - 2023

    # BASEBALL
    # game_key = "404"  # MLB - 2021
    # game_key = "412"  # MLB - 2022

    # BASKETBALL
    # game_key = "428"  # NBA - 2023

    return game_key


test_game_key = get_game_key()


# set desired league ID (see README.md for finding value)
def get_league_id():
    # FOOTBALL
    # league_id = "907359"  # NFL - 2015 (divisions)
    # league_id = "79230"  # NFL - 2019
    # league_id = "655434"  # NFL - 2020
    # league_id = "413954"  # NFL - 2021
    # league_id = "791337"  # NFL - 2022 (divisions)
    # league_id = "321958"  # NFL - 2023
    league_id = "365083"  # NFL - 2024

    # HOCKEY
    # league_id = "69624"  # NHL - 2012
    # league_id = "101592"  # NHL - 2021
    # league_id = "6546"  # NHL - 2021 (draft pick trading)
    # league_id = "22827"  # NHL - 2023
    # league_id = "1031"  # NHL - 2023 (FAAB)

    # BASEBALL
    # league_id = "40134"  # MLB - 2021

    # BASKETBALL
    # league_id = "969"  # NBA - 2023
    # league_id = "122731"  # NBA - 2023

    return league_id


test_league_id = get_league_id()


# set desired team ID within desired league
def get_team_id():
    # FOOTBALL
    team_id = 1  # NFL

    # HOCKEY
    # team_id = 2  # NHL (2012)

    return team_id


test_team_id = get_team_id()


# set desired team name within desired league
def get_team_name():
    # FOOTBALL
    team_name = "Let Baker Bake"  # NFL

    # HOCKEY
    # team_name = "The Bateleurs"  # NHL (2012)

    return team_name


test_team_name = get_team_name()


# set desired team ID within desired league
def get_player_id():
    # FOOTBALL
    player_id = 30123  # NFL: Patrick Mahomes - 2020/2021/2023/2024

    # HOCKEY
    # player_id = 4588  # NHL: Braden Holtby - 2012
    # player_id = 8205  # NHL: Jeffrey Viel - 2021
    # player_id = 3637  # NHL: Alex Ovechkin - 2021

    # BASEBALL
    # player_id = 9897  # MLB: Tim Anderson - 2021/2022

    # BASKETBALL
    # player_id = 3704  # NBA: LeBron James - 2023

    return player_id


test_player_id = get_player_id()


# set the maximum number players you wish the get_league_players query to retrieve
def get_league_player_limit():
    league_player_limit = 101

    return league_player_limit


test_league_player_limit = get_league_player_limit()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# QUERY SETUP # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# configure the Yahoo Fantasy Sports query (change all_output_as_json_str=True if you want to output JSON strings)
query = YahooFantasySportsQuery(
    test_league_id,
    test_game_code,
    test_game_id,
    yahoo_consumer_key=os.environ.get("YAHOO_CONSUMER_KEY"),
    yahoo_consumer_secret=os.environ.get("YAHOO_CONSUMER_SECRET"),
    # yahoo_access_token_json=os.environ.get("YAHOO_ACCESS_TOKEN_JSON"),
    save_token_data_to_env_file=True,
    env_var_fallback=True,
    all_output_as_json_str=False,
    offline=False
)

# query.save_access_token_data_to_env_file(project_dir, save_json_to_var=True)

# Manually override league key for example code to work
query.league_key = f"{test_game_id}.l.{test_league_id}"

# Manually override player key for example code to work
test_player_key = f"{test_game_id}.p.{test_player_id}"

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# RUN QUERIES # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# print(repr(query.get_all_yahoo_fantasy_game_keys()))
# print(repr(query.get_game_key_by_season(test_season)))
# print(repr(query.get_current_game_info()))
# print(repr(query.get_current_game_metadata()))
# print(repr(query.get_game_info_by_game_id(test_game_id)))
# print(repr(query.get_game_metadata_by_game_id(test_game_id)))
# print(repr(query.get_game_weeks_by_game_id(test_game_id)))
# print(repr(query.get_game_stat_categories_by_game_id(test_game_id)))
# print(repr(query.get_game_position_types_by_game_id(test_game_id)))
# print(repr(query.get_game_roster_positions_by_game_id(test_game_id)))
# print(repr(query.get_league_key(test_season)))
# print(repr(query.get_current_user()))
# print(repr(query.get_user_games()))
# print(repr(query.get_user_leagues_by_game_key(test_game_key)))
# print(repr(query.get_user_teams()))
# print(repr(query.get_league_info()))
# print(repr(query.get_league_metadata()))
# print(repr(query.get_league_settings()))
# print(repr(query.get_league_standings()))
# print(repr(query.get_league_teams()))
# print(repr(query.get_league_players(player_count_limit=10, player_count_start=0)))
# print(repr(query.get_league_draft_results()))
# print(repr(query.get_league_transactions()))
# print(repr(query.get_league_scoreboard_by_week(test_chosen_week)))
# print(repr(query.get_league_matchups_by_week(test_chosen_week)))
# print(repr(query.get_team_info(test_team_id)))
# print(repr(query.get_team_metadata(test_team_id)))
# print(repr(query.get_team_stats(test_team_id)))
# print(repr(query.get_team_stats_by_week(test_team_id, test_chosen_week)))
# print(repr(query.get_team_standings(test_team_id)))
# print(repr(query.get_team_roster_by_week(test_team_id, test_chosen_week)))
# print(repr(query.get_team_roster_player_info_by_week(test_team_id, test_chosen_week)))
# # print(repr(query.get_team_roster_player_info_by_date(test_team_id, test_chosen_date)))  # NHL/MLB/NBA
# print(repr(query.get_team_roster_player_stats(test_team_id)))
# print(repr(query.get_team_roster_player_stats_by_week(test_team_id, test_chosen_week)))
# print(repr(query.get_team_draft_results(test_team_id)))
# print(repr(query.get_team_matchups(test_team_id)))
# print(repr(query.get_player_stats_for_season(test_player_key)))
# print(repr(query.get_player_stats_for_season(test_player_key, limit_to_league_stats=False)))
# print(repr(query.get_player_stats_by_week(test_player_key, test_chosen_week)))
# print(repr(query.get_player_stats_by_week(test_player_key, test_chosen_week, limit_to_league_stats=False)))
# print(repr(query.get_player_stats_by_date(test_player_key, test_chosen_date)))  # NHL/MLB/NBA
# print(repr(query.get_player_stats_by_date(test_player_key, test_chosen_date, limit_to_league_stats=False)))  # NHL/MLB/NBA  # noqa: E501
# print(repr(query.get_player_ownership(test_player_key)))
# print(repr(query.get_player_percent_owned_by_week(test_player_key, test_chosen_week)))
# print(repr(query.get_player_draft_analysis(test_player_key)))

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# CHECK FOR MISSING DATA FIELDS # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

logger = get_logger("yfpy.models", DEBUG)

# query.get_all_yahoo_fantasy_game_keys()
# query.get_game_key_by_season(test_season)
# query.get_current_game_info()
# query.get_current_game_metadata()
# query.get_game_info_by_game_id(test_game_id)
# query.get_game_metadata_by_game_id(test_game_id)
# query.get_game_weeks_by_game_id(test_game_id)
# query.get_game_stat_categories_by_game_id(test_game_id)
# query.get_game_position_types_by_game_id(test_game_id)
# query.get_game_roster_positions_by_game_id(test_game_id)
# query.get_league_key(test_season)
# query.get_current_user()
# query.get_user_games()
# query.get_user_leagues_by_game_key(test_game_key)
# query.get_user_teams()
# query.get_league_info()
# query.get_league_metadata()
# query.get_league_settings()
# query.get_league_standings()
# query.get_league_teams()
# query.get_league_players(player_count_limit=10, player_count_start=0)
# query.get_league_draft_results()
# query.get_league_transactions()
# query.get_league_scoreboard_by_week(test_chosen_week)
# query.get_league_matchups_by_week(test_chosen_week)
# query.get_team_info(test_team_id)
# query.get_team_metadata(test_team_id)
# query.get_team_stats(test_team_id)
# query.get_team_stats_by_week(test_team_id, test_chosen_week)
# query.get_team_standings(test_team_id)
# query.get_team_roster_by_week(test_team_id, test_chosen_week)
# query.get_team_roster_player_info_by_week(test_team_id, test_chosen_week)
# # query.get_team_roster_player_info_by_date(test_team_id, test_chosen_date)  # NHL/MLB/NBA
# query.get_team_roster_player_stats(test_team_id)
# query.get_team_roster_player_stats_by_week(test_team_id, test_chosen_week)
# query.get_team_draft_results(test_team_id)
# query.get_team_matchups(test_team_id)
# query.get_player_stats_for_season(test_player_key)
# query.get_player_stats_for_season(test_player_key, limit_to_league_stats=False)
# query.get_player_stats_by_week(test_player_key, test_chosen_week)
# query.get_player_stats_by_week(test_player_key, test_chosen_week, limit_to_league_stats=False)
# query.get_player_stats_by_date(test_player_key, test_chosen_date)  # NHL/MLB/NBA
# query.get_player_stats_by_date(test_player_key, test_chosen_date, limit_to_league_stats=False)  # NHL/MLB/NBA
# query.get_player_ownership(test_player_key)
# query.get_player_percent_owned_by_week(test_player_key, test_chosen_week)
# query.get_player_draft_analysis(test_player_key)
