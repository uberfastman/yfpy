# -*- coding: utf-8 -*-
"""Pytest integration tests for Yahoo Fantasy Sports API league data.

Note:
    Tests saving and loading all Yahoo Fantasy Sports API league data.

Attributes:
    logger (Logger): Game data integration tests logger.
    env_path (Path): Path to the local .env file used to set environment variables at runtime.

"""
__author__ = "Wren J. R. (uberfastman)"
__email__ = "uberfastman@uberfastman.dev"

import logging
import warnings
from pathlib import Path

import pytest
from dotenv import load_dotenv

from yfpy.logger import get_logger
from yfpy.models import Scoreboard, Settings, Standings, League
from yfpy.utils import prettify_data

logger = get_logger(__name__)

# Suppress YahooFantasySportsQuery debug logging
logging.getLogger("yfpy.query").setLevel(level=logging.INFO)

# Ignore resource warnings from unittest module
warnings.simplefilter("ignore", ResourceWarning)

# load python-dotenv to parse environment variables
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)


@pytest.mark.integration
def test_get_league_info(yahoo_query, yahoo_data, data_dir, season, game_id, league_id, show_log_output):
    """Retrieve info for chosen league.
    """
    new_data_dir = data_dir / str(season) / (str(game_id) + ".l." + str(league_id))
    query_result_data = yahoo_data.save(str(league_id) + "-league-info",
                                        yahoo_query.get_league_info, new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(league_id) + "-league-info", League,
                                         new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_league_metadata(yahoo_query, yahoo_data, data_dir, season, game_id, league_id, show_log_output):
    """Retrieve metadata for chosen league.
    """
    new_data_dir = data_dir / str(season) / (str(game_id) + ".l." + str(league_id))
    query_result_data = yahoo_data.save(str(league_id) + "-league-metadata",
                                        yahoo_query.get_league_metadata, new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(league_id) + "-league-metadata", League,
                                         new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_league_settings(yahoo_query, yahoo_data, data_dir, season, game_id, league_id, show_log_output):
    """Retrieve settings (rules) for chosen league.
    """
    new_data_dir = data_dir / str(season) / (str(game_id) + ".l." + str(league_id))
    query_result_data = yahoo_data.save(str(league_id) + "-league-settings",
                                        yahoo_query.get_league_settings, new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(league_id) + "-league-settings", Settings,
                                         new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_league_standings(yahoo_query, yahoo_data, data_dir, season, game_id, league_id, show_log_output):
    """Retrieve standings for chosen league.
    """
    new_data_dir = data_dir / str(season) / (str(game_id) + ".l." + str(league_id))
    query_result_data = yahoo_data.save(str(league_id) + "-league-standings",
                                        yahoo_query.get_league_standings, new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(league_id) + "-league-standings", Standings,
                                         new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_league_teams(yahoo_query, yahoo_data, data_dir, season, game_id, league_id, show_log_output):
    """Retrieve teams for chosen league.
    """
    new_data_dir = data_dir / str(season) / (str(game_id) + ".l." + str(league_id))
    query_result_data = yahoo_data.save(str(league_id) + "-league-teams",
                                        yahoo_query.get_league_teams, new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(league_id) + "-league-teams", new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.skip(
    reason="Skipping test_get_league_players: high player volume slows down tests. Run this test separately."
)
@pytest.mark.integration
def test_get_league_players(yahoo_query, yahoo_data, data_dir, season, game_id, league_id, show_log_output):
    """Retrieve valid players for chosen league.
    """
    new_data_dir = data_dir / str(season) / (str(game_id) + ".l." + str(league_id))
    query_result_data = yahoo_data.save(str(league_id) + "-league-players",
                                        yahoo_query.get_league_players,
                                        # params={"player_count_start": 1400, "player_count_limit": 1475},
                                        new_data_dir=new_data_dir)

    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(league_id) + "-league-players", new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_league_players_with_limit(yahoo_query, yahoo_data, data_dir, season, game_id, league_id,
                                       league_player_limit, show_log_output):
    """Retrieve valid players for chosen league.
    """
    new_data_dir = data_dir / str(season) / (str(game_id) + ".l." + str(league_id))
    query_result_data = yahoo_data.save(str(league_id) + "-league-players",
                                        yahoo_query.get_league_players,
                                        params={"player_count_limit": league_player_limit}, new_data_dir=new_data_dir)

    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(league_id) + "-league-players", new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_league_draft_results(yahoo_query, yahoo_data, data_dir, season, game_id, league_id, show_log_output):
    """Retrieve draft results for chosen league.
    """
    new_data_dir = data_dir / str(season) / (str(game_id) + ".l." + str(league_id))
    query_result_data = yahoo_data.save(str(league_id) + "-league-draft_results",
                                        yahoo_query.get_league_draft_results, new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(league_id) + "-league-draft_results",
                                         new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_league_transactions(yahoo_query, yahoo_data, data_dir, season, game_id, league_id, show_log_output):
    """Retrieve transactions for chosen league.
    """
    new_data_dir = data_dir / str(season) / (str(game_id) + ".l." + str(league_id))
    query_result_data = yahoo_data.save(str(league_id) + "-league-transactions",
                                        yahoo_query.get_league_transactions, new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(league_id) + "-league-transactions",
                                         new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_league_scoreboard_by_week(yahoo_query, yahoo_data, data_dir, season, chosen_week, game_id, league_id,
                                       show_log_output):
    """Retrieve scoreboard for chosen league by week.
    """
    new_data_dir = data_dir / str(season) / (str(game_id) + ".l." + str(league_id)) / ("week_" + str(chosen_week))
    query_result_data = yahoo_data.save("week_" + str(chosen_week) + "-scoreboard",
                                        yahoo_query.get_league_scoreboard_by_week,
                                        params={"chosen_week": chosen_week}, new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load("week_" + str(chosen_week) + "-scoreboard", Scoreboard,
                                         new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_league_matchups_by_week(yahoo_query, yahoo_data, data_dir, season, chosen_week, game_id, league_id,
                                     show_log_output):
    """Retrieve matchups for chosen league by week.
    """
    new_data_dir = data_dir / str(season) / (str(game_id) + ".l." + str(league_id)) / ("week_" + str(chosen_week))
    query_result_data = yahoo_data.save("week_" + str(chosen_week) + "-matchups",
                                        yahoo_query.get_league_matchups_by_week,
                                        params={"chosen_week": chosen_week}, new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load("week_" + str(chosen_week) + "-matchups",
                                         new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data
