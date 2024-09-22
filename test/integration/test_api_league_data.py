# -*- coding: utf-8 -*-
"""Pytest integration tests for Yahoo Fantasy Sports API league data.

Note:
    Tests saving and loading all Yahoo Fantasy Sports API league data.

Attributes:
    logger (Logger): Game data integration tests logger.

"""
__author__ = "Wren J. R. (uberfastman)"
__email__ = "uberfastman@uberfastman.dev"

import logging
import warnings

import pytest

from yfpy.logger import get_logger
from yfpy.models import Scoreboard, Settings, Standings, League
from yfpy.utils import prettify_data

logger = get_logger(__name__)

# Suppress YahooFantasySportsQuery debug logging
logging.getLogger("yfpy.query").setLevel(level=logging.INFO)

# Ignore resource warnings from unittest module
warnings.simplefilter("ignore", ResourceWarning)


@pytest.mark.integration
def test_get_league_info(yahoo_query, yahoo_data, data_dir, season, game_id, league_id, show_log_output):
    """Integration test for retrieval of info for chosen Yahoo fantasy league.

    Note:
        Tests :func:`~yfpy.query.YahooFantasySportsQuery.get_league_info`.

    """

    new_data_dir = data_dir / str(season) / f"{game_id}.l.{league_id}"
    query_result_data = yahoo_data.save(
        f"{league_id}-league-info",
        yahoo_query.get_league_info,
        new_data_dir=new_data_dir
    )
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(
        f"{league_id}-league-info",
        League,
        new_data_dir=new_data_dir,
        all_output_as_json_str=yahoo_query.all_output_as_json_str
    )
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_league_metadata(yahoo_query, yahoo_data, data_dir, season, game_id, league_id, show_log_output):
    """Integration test for retrieval of metadata for chosen Yahoo fantasy league..

    Note:
        Tests :func:`~yfpy.query.YahooFantasySportsQuery.get_league_metadata`.

    """
    new_data_dir = data_dir / str(season) / f"{game_id}.l.{league_id}"
    query_result_data = yahoo_data.save(
        f"{league_id}-league-metadata",
        yahoo_query.get_league_metadata,
        new_data_dir=new_data_dir
    )
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(
        f"{league_id}-league-metadata",
        League,
        new_data_dir=new_data_dir,
        all_output_as_json_str=yahoo_query.all_output_as_json_str
    )
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_league_settings(yahoo_query, yahoo_data, data_dir, season, game_id, league_id, show_log_output):
    """Integration test for retrieval of settings for chosen Yahoo fantasy league.

    Note:
        Tests :func:`~yfpy.query.YahooFantasySportsQuery.get_league_settings`.

    """
    new_data_dir = data_dir / str(season) / f"{game_id}.l.{league_id}"
    query_result_data = yahoo_data.save(
        f"{league_id}-league-settings",
        yahoo_query.get_league_settings,
        new_data_dir=new_data_dir
    )
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(
        f"{league_id}-league-settings",
        Settings,
        new_data_dir=new_data_dir,
        all_output_as_json_str=yahoo_query.all_output_as_json_str
    )
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_league_standings(yahoo_query, yahoo_data, data_dir, season, game_id, league_id, show_log_output):
    """Integration test for retrieval of standings for chosen Yahoo fantasy league.

    Note:
        Tests :func:`~yfpy.query.YahooFantasySportsQuery.get_league_standings`.

    """
    new_data_dir = data_dir / str(season) / f"{game_id}.l.{league_id}"
    query_result_data = yahoo_data.save(
        f"{league_id}-league-standings",
        yahoo_query.get_league_standings,
        new_data_dir=new_data_dir
    )
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(
        f"{league_id}-league-standings",
        Standings,
        new_data_dir=new_data_dir,
        all_output_as_json_str=yahoo_query.all_output_as_json_str
    )
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_league_teams(yahoo_query, yahoo_data, data_dir, season, game_id, league_id, show_log_output):
    """Integration test for retrieval of all teams in chosen Yahoo fantasy league.

    Note:
        Tests :func:`~yfpy.query.YahooFantasySportsQuery.get_league_teams`.

    """
    new_data_dir = data_dir / str(season) / f"{game_id}.l.{league_id}"
    query_result_data = yahoo_data.save(
        f"{league_id}-league-teams",
        yahoo_query.get_league_teams,
        new_data_dir=new_data_dir
    )
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(
        f"{league_id}-league-teams",
        new_data_dir=new_data_dir,
        all_output_as_json_str=yahoo_query.all_output_as_json_str
    )
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.skip(
    reason="Skipping test_get_league_players: high player volume slows down tests. Run this test separately."
)
@pytest.mark.integration
def test_get_league_players(yahoo_query, yahoo_data, data_dir, season, game_id, league_id, show_log_output):
    """Integration test for retrieval of players in chosen Yahoo fantasy league.

    Note:
        Tests :func:`~yfpy.query.YahooFantasySportsQuery.get_league_players`.

    """
    new_data_dir = data_dir / str(season) / f"{game_id}.l.{league_id}"
    query_result_data = yahoo_data.save(
        f"{league_id}-league-players",
        yahoo_query.get_league_players,
        # params={"player_count_start": 1400, "player_count_limit": 1475},
        new_data_dir=new_data_dir
    )
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(
        f"{league_id}-league-players",
        new_data_dir=new_data_dir,
        all_output_as_json_str=yahoo_query.all_output_as_json_str
    )
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_league_players_with_limit(yahoo_query, yahoo_data, data_dir, season, game_id, league_id,
                                       league_player_limit, show_log_output):
    """Integration test for retrieval of a specified maximum of players in chosen Yahoo fantasy league.

    Note:
        Tests :func:`~yfpy.query.YahooFantasySportsQuery.get_league_players`.

    """
    new_data_dir = data_dir / str(season) / f"{game_id}.l.{league_id}"
    query_result_data = yahoo_data.save(
        f"{league_id}-league-players",
        yahoo_query.get_league_players,
        params={"player_count_limit": league_player_limit},
        new_data_dir=new_data_dir
    )
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(
        f"{league_id}-league-players",
        new_data_dir=new_data_dir,
        all_output_as_json_str=yahoo_query.all_output_as_json_str
    )
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_league_draft_results(yahoo_query, yahoo_data, data_dir, season, game_id, league_id, show_log_output):
    """Integration test for retrieval of draft results for chosen Yahoo fantasy league.

    Note:
        Tests :func:`~yfpy.query.YahooFantasySportsQuery.get_league_draft_results`.

    """
    new_data_dir = data_dir / str(season) / f"{game_id}.l.{league_id}"
    query_result_data = yahoo_data.save(
        f"{league_id}-league-draft_results",
        yahoo_query.get_league_draft_results,
        new_data_dir=new_data_dir
    )
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(
        f"{league_id}-league-draft_results",
        new_data_dir=new_data_dir,
        all_output_as_json_str=yahoo_query.all_output_as_json_str
    )
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_league_transactions(yahoo_query, yahoo_data, data_dir, season, game_id, league_id, show_log_output):
    """Integration test for retrieval of transactions for chosen Yahoo fantasy league.

    Note:
        Tests :func:`~yfpy.query.YahooFantasySportsQuery.get_league_transactions`.

    """
    new_data_dir = data_dir / str(season) / f"{game_id}.l.{league_id}"
    query_result_data = yahoo_data.save(
        f"{league_id}-league-transactions",
        yahoo_query.get_league_transactions,
        new_data_dir=new_data_dir
    )
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(
        f"{league_id}-league-transactions",
        new_data_dir=new_data_dir,
        all_output_as_json_str=yahoo_query.all_output_as_json_str
    )
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_league_scoreboard_by_week(yahoo_query, yahoo_data, data_dir, season, chosen_week, game_id, league_id,
                                       show_log_output):
    """Integration test for retrieval of scoreboard by week for chosen Yahoo fantasy league.

    Note:
        Tests :func:`~yfpy.query.YahooFantasySportsQuery.get_league_scoreboard_by_week`.

    """
    new_data_dir = data_dir / str(season) / f"{game_id}.l.{league_id}" / f"week_{chosen_week}"
    query_result_data = yahoo_data.save(
        f"week_{chosen_week}-scoreboard",
        yahoo_query.get_league_scoreboard_by_week,
        params={"chosen_week": chosen_week},
        new_data_dir=new_data_dir
    )
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(
        f"week_{chosen_week}-scoreboard",
        Scoreboard,
        new_data_dir=new_data_dir,
        all_output_as_json_str=yahoo_query.all_output_as_json_str
    )
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_league_matchups_by_week(yahoo_query, yahoo_data, data_dir, season, chosen_week, game_id, league_id,
                                     show_log_output):
    """Integration test for retrieval of matchups by week for chosen Yahoo fantasy league.

    Note:
        Tests :func:`~yfpy.query.YahooFantasySportsQuery.get_league_matchups_by_week`.

    """
    new_data_dir = data_dir / str(season) / f"{game_id}.l.{league_id}" / f"week_{chosen_week}"
    query_result_data = yahoo_data.save(
        f"week_{chosen_week}-matchups",
        yahoo_query.get_league_matchups_by_week,
        params={"chosen_week": chosen_week},
        new_data_dir=new_data_dir
    )
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(
        f"week_{chosen_week}-matchups",
        new_data_dir=new_data_dir,
        all_output_as_json_str=yahoo_query.all_output_as_json_str
    )
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data
