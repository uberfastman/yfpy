# -*- coding: utf-8 -*-
"""YFPY demo.

"""
__author__ = "Wren J. R. (uberfastman)"
__email__ = "uberfastman@uberfastman.dev"

import os
import sys
from logging import DEBUG
from pathlib import Path

from dotenv import load_dotenv

project_dir = Path(__file__).parent.parent
sys.path.insert(0, str(project_dir))

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
load_dotenv(dotenv_path=project_dir / "auth" / ".env")

# set directory location of private.json for authentication
auth_dir = project_dir / "auth"

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
    season = 2023
    return season


season = get_season()


# set desired week
def get_chosen_week():
    chosen_week = 1
    return chosen_week


chosen_week = get_chosen_week()


# set desired date
def get_chosen_date():
    # HOCKEY
    # chosen_date = "2013-04-15"  # NHL - 2013 (for 2012 season)
    chosen_date = "2021-10-25"  # NHL - 2021

    # BASEBALL
    # chosen_date = "2021-04-01"  # MLB - 2021
    # chosen_date = "2022-04-10"  # MLB - 2022

    return chosen_date


chosen_date = get_chosen_date()


# set desired Yahoo Fantasy Sports game code
def get_game_code():
    # FOOTBALL
    game_code = "nfl"  # NFL

    # HOCKEY
    # game_code = "nhl"  # NHL

    # BASEBALL
    # game_code = "mlb"  # MLB

    return game_code


game_code = get_game_code()


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
    game_id = 423  # NFL - 2023

    # HOCKEY
    # game_id = 303  # NHL - 2012
    # game_id = 411  # NHL - 2021
    # game_id = 427  # NHL - 2023

    # BASEBALL
    # game_id = 404  # MLB - 2021
    # game_id = 412  # MLB - 2022

    return game_id


game_id = get_game_id()


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
    game_key = "423"  # NFL - 2023

    # HOCKEY
    # game_key = "303"  # NHL - 2012
    # game_key = "411"  # NHL - 2021
    # game_key = "427"  # NHL - 2023

    # BASEBALL
    # game_key = "404"  # MLB - 2021
    # game_key = "412"  # MLB - 2022

    return game_key


game_key = get_game_key()


# set desired league ID (see README.md for finding value)
def get_league_id():
    # FOOTBALL
    # league_id = "907359"  # NFL - 2015 (divisions)
    # league_id = "79230"  # NFL - 2019
    # league_id = "655434"  # NFL - 2020
    # league_id = "413954"  # NFL - 2021
    # league_id = "791337"  # NFL - 2022 (divisions)
    league_id = "321958"  # NFL - 2023

    # HOCKEY
    # league_id = "69624"  # NHL - 2012
    # league_id = "101592"  # NHL - 2021
    # league_id = "6546"  # NHL - 2021 (draft pick trading)
    # league_id = "22827"  # NHL - 2023
    # league_id = "1031"  # NHL - 2023 (FAAB)

    # BASEBALL
    # league_id = "40134"  # MLB - 2021

    return league_id


league_id = get_league_id()


# set desired team ID within desired league
def get_team_id():
    # FOOTBALL
    team_id = 1  # NFL

    # HOCKEY
    # team_id = 2  # NHL (2012)

    return team_id


team_id = get_team_id()


# set desired team name within desired league
def get_team_name():
    # FOOTBALL
    team_name = "Legion"  # NFL

    # HOCKEY
    # team_name = "The Bateleurs"  # NHL (2012)

    return team_name


team_name = get_team_name()


# set desired team ID within desired league
def get_player_id():
    # FOOTBALL
    player_id = 30123  # NFL: Patrick Mahomes - 2020/2021/2023

    # HOCKEY
    # player_id = 4588  # NHL: Braden Holtby - 2012
    # player_id = 8205  # NHL: Jeffrey Viel - 2021
    # player_id = 3637  # NHL: Alex Ovechkin - 2021

    # BASEBALL
    # player_id = 9897  # MLB: Tim Anderson - 2021/2022

    return player_id


player_id = get_player_id()


# set the maximum number players you wish the get_league_players query to retrieve
def get_league_player_limit():
    league_player_limit = 101

    return league_player_limit


league_player_limit = get_league_player_limit()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# QUERY SETUP # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# configure the Yahoo Fantasy Sports query (change all_output_as_json_str=True if you want to output JSON strings)
yahoo_query = YahooFantasySportsQuery(
    auth_dir,
    league_id,
    game_code,
    game_id=game_id,
    offline=False,
    all_output_as_json_str=False,
    consumer_key=os.environ["YFPY_CONSUMER_KEY"],
    consumer_secret=os.environ["YFPY_CONSUMER_SECRET"]
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
