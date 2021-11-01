__author__ = "Wren J. R. (uberfastman)"
__email__ = "uberfastman@uberfastman.dev"

import logging
import os
import warnings
from pathlib import Path

import pytest
from dotenv import load_dotenv

from yfpy import Data
from yfpy.logger import get_logger
from yfpy.models import Game, StatCategories, User, Scoreboard, Settings, Standings, League, Player, Team, \
    TeamPoints, TeamStandings, Roster
from yfpy.query import YahooFantasySportsQuery
from yfpy.utils import prettify_data

logger = get_logger(__name__)

# Suppress YahooFantasySportsQuery debug logging
logging.getLogger("yfpy.query").setLevel(level=logging.INFO)

# Ignore resource warnings from unittest module
warnings.simplefilter("ignore", ResourceWarning)

# load python-dotenv to parse environment variables
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Turn on/off example code stdout logging output
log_output = False

# Turn on/off automatic opening of browser window for OAuth
browser_callback = True

# Put private.json (see README.md) in test/ directory
auth_dir = Path(".")

# Example code will output data here
data_dir = Path(__file__).parent / "test_output"

# Example vars using public Yahoo league (still requires auth through a personal Yahoo account - see README.md)

# # # # # # # # # # # # # # # # # # # # # # # #
# # # # Yahoo Fantasy Sports: General # # # # #
# # # # # # # # # # # # # # # # # # # # # # # #

# season = "2012"
# season = "2014"
# season = "2015"
# season = "2019"
# season = "2020"
season = "2021"

chosen_week = 1

league_player_limit = 101
# league_player_limit = 2610

# # # # # # # # # # # # # # # # # # # # # # # #
# # # # # Yahoo Fantasy Football: NFL # # # # #
# # # # # # # # # # # # # # # # # # # # # # # #

# example_public_league_url = "https://archive.fantasysports.yahoo.com/nfl/2014/729259"

# game_key = "331"  # NFL - 2014
# game_key = "348"  # NFL - 2015 (testing for league with divisions)
# game_key = "390"  # NFL - 2019
# game_key = "399"  # NFL - 2020
game_key = "406"  # NFL - 2021

game_code = "nfl"

# league_id = "907359"  # NFL - 2015 (testing for league with divisions)
# league_id = "79230"  # NFL - 2019
# league_id = "655434"  # NFL - 2020
league_id = "413954"  # NFL - 2021

team_id = 1
team_name = "Legion"
player_id = "7200"  # NFL: Aaron Rodgers - 2020/2021

# # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # #
# # # # # Yahoo Fantasy Hockey: NHL # # # # #
# # # # # # # # # # # # # # # # # # # # # # #

# game_key = "303"  # NHL - 2012
# game_key = "411"  # NHL - 2021

# game_code = "nhl"  # NHL

# league_id = "69624"  # NHL - 2012
# league_id = "101592"  # NHL - 2021

# chosen_date = "2013-04-15"  # NHL - 2013
# chosen_date = "2013-04-16"  # NHL - 2013
chosen_date = "2021-10-25"  # NHL - 2021

# player_id = "4588"  # NHL: Braden Holtby - 2012
# player_id = "8205"  # NHL: Jeffrey Viel - 2021
# player_id = "3637"  # NHL: Alex Ovechkin - 2021

# # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # #

player_key = game_key + ".p." + player_id

# Instantiate yfpy objects
yahoo_data = Data(data_dir)
yahoo_query = YahooFantasySportsQuery(
    auth_dir,
    league_id,
    game_id=game_key,
    game_code=game_code,
    offline=False,
    all_output_as_json=False,
    consumer_key=os.environ["YFPY_CONSUMER_KEY"],
    consumer_secret=os.environ["YFPY_CONSUMER_SECRET"],
    browser_callback=browser_callback
)

# Manually override league key for example code to work
yahoo_query.league_key = game_key + ".l." + league_id


# ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ •
# ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ SAVING AND LOADING FANTASY FOOTBALL GAME DATA • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ •
# ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ •

def test_get_all_yahoo_fantasy_game_keys():
    """Retrieve all Yahoo fantasy football game keys.
    """
    query_result_data = yahoo_data.save(game_code + "-game_keys",
                                        yahoo_query.get_all_yahoo_fantasy_game_keys)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(game_code + "-game_keys")
    if log_output:
        logger.info(f"{prettify_data(loaded_result_data)}\n----------\n")

    assert query_result_data == loaded_result_data


def test_get_game_key_by_season():
    """Retrieve specific game key by season.
    """
    query_result_data = yahoo_query.get_game_key_by_season(season=season)
    if log_output:
        logger.info(prettify_data(query_result_data))

    assert query_result_data == game_key


def test_get_current_game_info():
    """Retrieve game info for current fantasy season.
    """
    query_result_data = yahoo_data.save("current-game-info", yahoo_query.get_current_game_info)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load("current-game-info", Game)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


def test_get_current_game_metadata():
    """Retrieve game metadata for current fantasy season.
    """
    query_result_data = yahoo_data.save("current-game-metadata", yahoo_query.get_current_game_metadata)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load("current-game-metadata", Game)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


def test_get_game_info_by_game_id():
    """Retrieve game info for specific game by id.
    """
    new_data_dir = data_dir / str(season)
    query_result_data = yahoo_data.save(str(game_key) + "-game-info",
                                        yahoo_query.get_game_info_by_game_id,
                                        params={"game_id": game_key}, new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(game_key) + "-game-info", Game, new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


def test_get_game_metadata_by_game_id():
    """Retrieve game metadata for specific game by id.
    """
    new_data_dir = data_dir / str(season)
    query_result_data = yahoo_data.save(str(game_key) + "-game-metadata",
                                        yahoo_query.get_game_metadata_by_game_id,
                                        params={"game_id": game_key}, new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(game_key) + "-game-metadata", Game, new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


def test_get_league_key():
    """Retrieve league key for selected league.
    """
    query_result_data = yahoo_query.get_league_key()
    if log_output:
        logger.info(prettify_data(query_result_data))

    assert query_result_data == game_key + ".l." + league_id


def test_get_game_weeks_by_game_id():
    """Retrieve all valid weeks of a specific game by id.
    """
    new_data_dir = data_dir / str(season)
    query_result_data = yahoo_data.save(str(game_key) + "-game-weeks",
                                        yahoo_query.get_game_weeks_by_game_id,
                                        params={"game_id": game_key}, new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(game_key) + "-game-weeks", new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


def test_get_game_stat_categories_by_game_id():
    """Retrieve all valid stat categories of a specific game by id.
    """
    new_data_dir = data_dir / str(season)
    query_result_data = yahoo_data.save(str(game_key) + "-game-stat_categories",
                                        yahoo_query.get_game_stat_categories_by_game_id,
                                        params={"game_id": game_key}, new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(game_key) + "-game-stat_categories", StatCategories,
                                         new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(query_result_data))

    assert query_result_data == loaded_result_data


def test_get_game_position_types_by_game_id():
    """Retrieve all valid position types for specific game by id.
    """
    new_data_dir = data_dir / str(season)
    query_result_data = yahoo_data.save(str(game_key) + "-game-position_types",
                                        yahoo_query.get_game_position_types_by_game_id,
                                        params={"game_id": game_key}, new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(game_key) + "-game-position_types", new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


def test_get_game_roster_positions_by_game_id():
    """Retrieve all valid roster positions for specific game by id.
    """
    new_data_dir = data_dir / str(season)
    query_result_data = yahoo_data.save(str(game_key) + "-game-roster_positions",
                                        yahoo_query.get_game_roster_positions_by_game_id,
                                        params={"game_id": game_key}, new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(game_key) + "-game-roster_positions",
                                         new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


# ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~
# ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ SAVING AND LOADING USER HISTORICAL DATA • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~
# ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~

def test_get_current_user():
    """Retrieve metadata for current logged-in user.
    """
    new_data_dir = data_dir
    query_result_data = yahoo_data.save("user", yahoo_query.get_current_user, new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load("user", User, new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


def test_get_user_games():
    """Retrieve game history for current logged-in user.
    """
    new_data_dir = data_dir
    query_result_data = yahoo_data.save("user-games", yahoo_query.get_user_games,
                                        new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load("user-games", new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.skip(
    reason="Skipping get_user_leagues_by_game_key: current logged-in user must have leagues from test season/year."
)
def test_get_user_leagues_by_game_id():
    """Retrieve league history for current logged-in user for specific game by id.
    """
    new_data_dir = data_dir
    query_result_data = yahoo_data.save(
        "user-leagues",
        yahoo_query.get_user_leagues_by_game_key,
        params={"game_key": game_key},
        new_data_dir=new_data_dir
    )

    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load("user-leagues", new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


def test_get_user_teams():
    """Retrieve teams for all leagues for current logged-in user for current game.
    """
    new_data_dir = data_dir
    query_result_data = yahoo_data.save("user-teams", yahoo_query.get_user_teams,
                                        new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load("user-teams", new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


# ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~
# ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ SAVING AND LOADING FANTASY FOOTBALL LEAGUE DATA • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~
# ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~

def test_get_league_info():
    """Retrieve info for chosen league.
    """
    new_data_dir = data_dir / str(season) / (str(game_key) + ".l." + str(league_id))
    query_result_data = yahoo_data.save(str(league_id) + "-league-info",
                                        yahoo_query.get_league_info, new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(league_id) + "-league-info", League,
                                         new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


def test_get_league_metadata():
    """Retrieve metadata for chosen league.
    """
    new_data_dir = data_dir / str(season) / (str(game_key) + ".l." + str(league_id))
    query_result_data = yahoo_data.save(str(league_id) + "-league-metadata",
                                        yahoo_query.get_league_metadata, new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(league_id) + "-league-metadata", League,
                                         new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


def test_get_league_settings():
    """Retrieve settings (rules) for chosen league.
    """
    new_data_dir = data_dir / str(season) / (str(game_key) + ".l." + str(league_id))
    query_result_data = yahoo_data.save(str(league_id) + "-league-settings",
                                        yahoo_query.get_league_settings, new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(league_id) + "-league-settings", Settings,
                                         new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


def test_get_league_standings():
    """Retrieve standings for chosen league.
    """
    new_data_dir = data_dir / str(season) / (str(game_key) + ".l." + str(league_id))
    query_result_data = yahoo_data.save(str(league_id) + "-league-standings",
                                        yahoo_query.get_league_standings, new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(league_id) + "-league-standings", Standings,
                                         new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


def test_get_league_teams():
    """Retrieve teams for chosen league.
    """
    new_data_dir = data_dir / str(season) / (str(game_key) + ".l." + str(league_id))
    query_result_data = yahoo_data.save(str(league_id) + "-league-teams",
                                        yahoo_query.get_league_teams, new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(league_id) + "-league-teams", new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.skip(
    reason="Skipping test_get_league_players: high player volume slows down tests. Run this test separately."
)
def test_get_league_players():
    """Retrieve valid players for chosen league.
    """
    new_data_dir = data_dir / str(season) / (str(game_key) + ".l." + str(league_id))
    query_result_data = yahoo_data.save(str(league_id) + "-league-players",
                                        yahoo_query.get_league_players,
                                        # params={"player_count_start": 1400, "player_count_limit": 1475},
                                        new_data_dir=new_data_dir)

    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(league_id) + "-league-players", new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


def test_get_league_players_with_limit():
    """Retrieve valid players for chosen league.
    """
    new_data_dir = data_dir / str(season) / (str(game_key) + ".l." + str(league_id))
    query_result_data = yahoo_data.save(str(league_id) + "-league-players",
                                        yahoo_query.get_league_players,
                                        params={"player_count_limit": league_player_limit}, new_data_dir=new_data_dir)

    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(league_id) + "-league-players", new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


def test_get_league_draft_results():
    """Retrieve draft results for chosen league.
    """
    new_data_dir = data_dir / str(season) / (str(game_key) + ".l." + str(league_id))
    query_result_data = yahoo_data.save(str(league_id) + "-league-draft_results",
                                        yahoo_query.get_league_draft_results, new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(league_id) + "-league-draft_results",
                                         new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


def test_get_league_transactions():
    """Retrieve transactions for chosen league.
    """
    new_data_dir = data_dir / str(season) / (str(game_key) + ".l." + str(league_id))
    query_result_data = yahoo_data.save(str(league_id) + "-league-transactions",
                                        yahoo_query.get_league_transactions, new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(league_id) + "-league-transactions",
                                         new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


def test_get_league_scoreboard_by_week():
    """Retrieve scoreboard for chosen league by week.
    """
    new_data_dir = data_dir / str(season) / (str(game_key) + ".l." + str(league_id)) / ("week_" + str(chosen_week))
    query_result_data = yahoo_data.save("week_" + str(chosen_week) + "-scoreboard",
                                        yahoo_query.get_league_scoreboard_by_week,
                                        params={"chosen_week": chosen_week}, new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load("week_" + str(chosen_week) + "-scoreboard", Scoreboard,
                                         new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


def test_get_league_matchups_by_week():
    """Retrieve matchups for chosen league by week.
    """
    new_data_dir = data_dir / str(season) / (str(game_key) + ".l." + str(league_id)) / ("week_" + str(chosen_week))
    query_result_data = yahoo_data.save("week_" + str(chosen_week) + "-matchups",
                                        yahoo_query.get_league_matchups_by_week,
                                        params={"chosen_week": chosen_week}, new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load("week_" + str(chosen_week) + "-matchups",
                                         new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


# ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ •
# ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • SAVING AND LOADING SPECIFIC TEAM DATA ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ •
# ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ •

def test_get_team_info():
    """Retrieve info of specific team by team_id for chosen league.
    """
    new_data_dir = (data_dir / str(season) / (str(game_key) + ".l." + str(league_id)) / "teams"
                    / (str(team_id) + "-" + team_name))
    query_result_data = yahoo_data.save(str(team_id) + "-" + team_name + "-info",
                                        yahoo_query.get_team_info,
                                        params={"team_id": team_id}, new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(team_id) + "-" + team_name + "-info", Team,
                                         new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


def test_get_team_metadata():
    """Retrieve metadata of specific team by team_id for chosen league.
    """
    new_data_dir = (data_dir / str(season) / (str(game_key) + ".l." + str(league_id)) / "teams"
                    / (str(team_id) + "-" + team_name))
    query_result_data = yahoo_data.save(str(team_id) + "-" + team_name + "-metadata",
                                        yahoo_query.get_team_metadata,
                                        params={"team_id": team_id}, new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(team_id) + "-" + team_name + "-metadata", Team,
                                         new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


def test_get_team_stats():
    """Retrieve stats of specific team by team_id for chosen league.
    """
    new_data_dir = (data_dir / str(season) / (str(game_key) + ".l." + str(league_id)) / "teams"
                    / (str(team_id) + "-" + team_name))
    query_result_data = yahoo_data.save(str(team_id) + "-" + team_name + "-stats",
                                        yahoo_query.get_team_stats,
                                        params={"team_id": team_id}, new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(team_id) + "-" + team_name + "-stats", TeamPoints,
                                         new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


def test_get_team_stats_by_week():
    """Retrieve stats of specific team by team_id and by week for chosen league.
    """
    new_data_dir = data_dir / str(season) / (str(game_key) + ".l." + str(league_id)) / ("week_" + str(chosen_week))
    query_result_data = yahoo_data.save(str(team_id) + "-" + team_name + "-stats",
                                        yahoo_query.get_team_stats_by_week,
                                        params={"team_id": team_id, "chosen_week": chosen_week},
                                        new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(team_id) + "-" + team_name + "-stats",
                                         new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


def test_get_team_standings():
    """Retrieve standings of specific team by team_id for chosen league.
    """
    new_data_dir = (data_dir / str(season) / (str(game_key) + ".l." + str(league_id)) / "teams"
                    / (str(team_id) + "-" + team_name))
    query_result_data = yahoo_data.save(str(team_id) + "-" + team_name + "-standings",
                                        yahoo_query.get_team_standings,
                                        params={"team_id": team_id}, new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(team_id) + "-" + team_name + "-standings",
                                         TeamStandings, new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


def test_get_team_roster_by_week():
    """Retrieve roster of specific team by team_id and by week for chosen league.
    """
    new_data_dir = (data_dir / str(season) / (str(game_key) + ".l." + str(league_id)) / ("week_" + str(chosen_week))
                    / "rosters")
    query_result_data = yahoo_data.save(str(team_id) + "-" + team_name + "-roster_by_week",
                                        yahoo_query.get_team_roster_by_week,
                                        params={"team_id": team_id, "chosen_week": chosen_week},
                                        new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(team_id) + "-" + team_name + "-roster_by_week", Roster,
                                         new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


def test_get_team_roster_player_info_by_week():
    """Retrieve roster with player info of specific team by team_id and by week for chosen league.
    """
    new_data_dir = (data_dir / str(season) / (str(game_key) + ".l." + str(league_id)) / ("week_" + str(chosen_week))
                    / "rosters")
    query_result_data = yahoo_data.save(str(team_id) + "-" + team_name
                                        + "-roster-player_info_by_week",
                                        yahoo_query.get_team_roster_player_info_by_week,
                                        params={"team_id": team_id, "chosen_week": chosen_week},
                                        new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(team_id) + "-" + team_name
                                         + "-roster-player_info_by_week",
                                         new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.skip(
    reason="Skipping test_get_team_roster_player_info_by_date: retrieval by date supported by NHL/NBA/MLB, not NFL."
)
def test_get_team_roster_player_info_by_date():
    """Retrieve roster with player info of specific team by team_id and by date for chosen league.
    """
    new_data_dir = data_dir / str(season) / (str(game_key) + ".l." + str(league_id)) / str(chosen_date) / "rosters"
    query_result_data = yahoo_data.save(str(team_id) + "-" + team_name
                                        + "-roster-player_info_by_date",
                                        yahoo_query.get_team_roster_player_info_by_date,
                                        params={"team_id": team_id, "chosen_date": chosen_date},
                                        new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(team_id) + "-" + team_name
                                         + "-roster-player_info_by_date",
                                         new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


def test_get_team_roster_player_stats():
    """Retrieve roster with player info for season of specific team by team_id for chosen league.
    """
    new_data_dir = data_dir / str(season) / (str(game_key) + ".l." + str(league_id)) / "rosters"
    query_result_data = yahoo_data.save(str(team_id) + "-" + team_name + "-roster-player_stats",
                                        yahoo_query.get_team_roster_player_stats,
                                        params={"team_id": team_id},
                                        new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(team_id) + "-" + team_name + "-roster-player_stats",
                                         new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


def test_get_team_roster_player_stats_by_week():
    """Retrieve roster with player stats of specific team by team_id and by week for chosen league.
    """
    new_data_dir = (data_dir / str(season) / (str(game_key) + ".l." + str(league_id)) / ("week_" + str(chosen_week))
                    / "rosters")

    query_result_data = yahoo_data.save(str(team_id) + "-" + team_name
                                        + "-roster-player_stats_by_week",
                                        yahoo_query.get_team_roster_player_stats_by_week,
                                        params={"team_id": team_id, "chosen_week": chosen_week},
                                        new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(team_id) + "-" + team_name
                                         + "-roster-player_stats_by_week",
                                         new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


def test_get_team_draft_results():
    """Retrieve draft results of specific team by team_id for chosen league.
    """
    new_data_dir = (data_dir / str(season) / (str(game_key) + ".l." + str(league_id)) / "teams"
                    / (str(team_id) + "-" + team_name))
    query_result_data = yahoo_data.save(str(team_id) + "-" + team_name + "-draft_results",
                                        yahoo_query.get_team_draft_results,
                                        params={"team_id": team_id}, new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(team_id) + "-" + team_name + "-draft_results",
                                         new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


def test_get_team_matchups():
    """Retrieve matchups of specific team by team_id for chosen league.
    """
    new_data_dir = (data_dir / str(season) / (str(game_key) + ".l." + str(league_id)) / "teams"
                    / (str(team_id) + "-" + team_name))
    query_result_data = yahoo_data.save(str(team_id) + "-" + team_name + "-matchups",
                                        yahoo_query.get_team_matchups,
                                        params={"team_id": team_id}, new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(team_id) + "-" + team_name + "-matchups",
                                         new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


# ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ •
# ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • SAVING AND LOADING SPECIFIC PLAYER DATA • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ •
# ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ •

def test_get_player_stats_for_season():
    """Retrieve stats of specific player by player_key for season for chosen league.
    """
    new_data_dir = data_dir / str(season) / (str(game_key) + ".l." + str(league_id)) / "players"
    query_result_data = yahoo_data.save(str(player_id) + "-player-season-stats",
                                        yahoo_query.get_player_stats_for_season,
                                        params={"player_key": str(player_key)},
                                        new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(player_id) + "-player-season-stats", Player,
                                         new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


def test_get_player_stats_by_week():
    """Retrieve stats of specific player by player_key and by week for chosen league.
    """
    new_data_dir = (data_dir / str(season) / (str(game_key) + ".l." + str(league_id)) / ("week_" + str(chosen_week))
                    / "players")
    query_result_data = yahoo_data.save(str(player_id) + "-player-stats",
                                        yahoo_query.get_player_stats_by_week,
                                        params={"player_key": str(player_key),
                                                "chosen_week": str(chosen_week)},
                                        new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(player_id) + "-player-stats", Player,
                                         new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.skip(
    reason="Skipping test_get_player_stats_by_date: retrieval by date supported by NHL/NBA/MLB, not NFL."
)
def test_get_player_stats_by_date():
    """Retrieve stats of specific player by player_key and by date for chosen league.
    """
    new_data_dir = data_dir / str(season) / (str(game_key) + ".l." + str(league_id)) / str(chosen_date) / "players"
    query_result_data = yahoo_data.save(str(player_id) + "-player-stats",
                                        yahoo_query.get_player_stats_by_date,
                                        params={"player_key": str(player_key),
                                                "chosen_date": chosen_date},
                                        new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(player_id) + "-player-stats", Player,
                                         new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


def test_get_player_ownership():
    """Retrieve ownership of specific player by player_key for chosen league.
    """
    new_data_dir = data_dir / str(season) / (str(game_key) + ".l." + str(league_id)) / "players"
    query_result_data = yahoo_data.save(str(player_id) + "-player-ownership",
                                        yahoo_query.get_player_ownership,
                                        params={"player_key": str(player_key)},
                                        new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(player_id) + "-player-ownership", Player,
                                         new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


def test_get_player_percent_owned_by_week():
    """Retrieve percent-owned of specific player by player_key and by week for chosen league.
    """
    new_data_dir = (data_dir / str(season) / (str(game_key) + ".l." + str(league_id)) / ("week_" + str(chosen_week))
                    / "players")
    query_result_data = yahoo_data.save(str(player_id) + "-player-percent_owned",
                                        yahoo_query.get_player_percent_owned_by_week,
                                        params={"player_key": str(player_key),
                                                "chosen_week": str(chosen_week)},
                                        new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(player_id) + "-player-percent_owned", Player,
                                         new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


def test_get_player_draft_analysis():
    """Retrieve draft analysis of specific player by player_key for chosen league.
    """
    new_data_dir = data_dir / str(season) / (str(game_key) + ".l." + str(league_id)) / "players"
    query_result_data = yahoo_data.save(str(player_id) + "-player-draft_analysis",
                                        yahoo_query.get_player_draft_analysis,
                                        params={"player_key": str(player_key)},
                                        new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(player_id) + "-player-draft_analysis", Player,
                                         new_data_dir=new_data_dir)
    if log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


if __name__ == "__main__":

    log_output = True

    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ •
    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ SAVING AND LOADING FANTASY FOOTBALL GAME DATA • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ •
    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ •
    # test_get_all_yahoo_fantasy_game_keys()
    # test_get_game_key_by_season()
    # test_get_current_game_info()
    # test_get_current_game_metadata()
    # test_get_game_info_by_game_id()
    # test_get_game_metadata_by_game_id()
    # test_get_league_key()
    # test_get_game_weeks_by_game_id()
    # test_get_game_stat_categories_by_game_id()
    # test_get_game_position_types_by_game_id()
    # test_get_game_roster_positions_by_game_id()

    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~
    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ SAVING AND LOADING USER HISTORICAL DATA • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~
    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~
    # test_get_current_user()
    # test_get_user_games()
    # test_get_user_leagues_by_game_id()
    # test_get_user_teams()

    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~
    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ SAVING AND LOADING FANTASY FOOTBALL LEAGUE DATA • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~
    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~
    # test_get_league_info()
    # test_get_league_metadata()
    # test_get_league_settings()
    # test_get_league_standings()
    # test_get_league_teams()
    # test_get_league_players()
    # test_get_league_players_with_limit()
    # test_get_league_draft_results()
    # test_get_league_transactions()
    # test_get_league_scoreboard_by_week()
    # test_get_league_matchups_by_week()

    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ •
    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • SAVING AND LOADING SPECIFIC TEAM DATA ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ •
    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ •
    # test_get_team_info()
    # test_get_team_metadata()
    # test_get_team_stats()
    # test_get_team_stats_by_week()
    # test_get_team_standings()
    # test_get_team_roster_by_week()
    # test_get_team_roster_player_info_by_week()
    # test_get_team_roster_player_info_by_date()
    # test_get_team_roster_player_stats()
    # test_get_team_roster_player_stats_by_week()
    # test_get_team_draft_results()
    # test_get_team_matchups()

    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ •
    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • SAVING AND LOADING SPECIFIC PLAYER DATA • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ •
    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ •
    # test_get_player_stats_for_season()
    # test_get_player_stats_by_week()
    # test_get_player_stats_by_date()
    # test_get_player_ownership()
    # test_get_player_percent_owned_by_week()
    # test_get_player_draft_analysis()

    pass
