# -*- coding: utf-8 -*-
"""Pytest integration tests for Yahoo Fantasy Sports API game data.

Note:
    Tests saving and loading all Yahoo Fantasy Sports API game data.

Attributes:
    logger (Logger): Game data integration tests logger.

"""
__author__ = "Wren J. R. (uberfastman)"
__email__ = "uberfastman@uberfastman.dev"

import logging
import warnings

import pytest

from yfpy.logger import get_logger
from yfpy.models import Game, StatCategories
from yfpy.utils import prettify_data

logger = get_logger(__name__)

# Suppress YahooFantasySportsQuery debug logging
logging.getLogger("yfpy.query").setLevel(level=logging.INFO)

# Ignore resource warnings from unittest module
warnings.simplefilter("ignore", ResourceWarning)


@pytest.mark.integration
def test_get_all_yahoo_fantasy_game_keys(yahoo_query, yahoo_data, game_code, game_id, show_log_output):
    """Integration test for retrieval of all Yahoo fantasy football game keys.

    Note:
        Tests :func:`~yfpy.query.YahooFantasySportsQuery.get_all_yahoo_fantasy_game_keys`.

    """
    query_result_data = yahoo_data.save(
        f"{game_code}-game_keys",
        yahoo_query.get_all_yahoo_fantasy_game_keys
    )
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(
        f"{game_code}-game_keys",
        all_output_as_json_str=yahoo_query.all_output_as_json_str
    )
    if show_log_output:
        logger.info(f"{prettify_data(loaded_result_data)}\n----------\n")

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_game_key_by_season(yahoo_query, season, game_key, show_log_output):
    """Integration test for retrieval of specific game key by season.

    Note:
        Tests :func:`~yfpy.query.YahooFantasySportsQuery.get_game_key_by_season`.

    """
    query_result_data = yahoo_query.get_game_key_by_season(season=season)
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    assert query_result_data == game_key


@pytest.mark.integration
def test_get_current_game_info(yahoo_query, yahoo_data, data_dir, season, game_id, show_log_output):
    """Integration test for retrieval of game info for current fantasy season.

    Note:
        Tests :func:`~yfpy.query.YahooFantasySportsQuery.get_current_game_info`.

    """
    query_result_data = yahoo_data.save(
        "current-game-info",
        yahoo_query.get_current_game_info
    )
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(
        "current-game-info",
        Game,
        all_output_as_json_str=yahoo_query.all_output_as_json_str
    )
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_current_game_metadata(yahoo_query, yahoo_data, data_dir, season, game_id, show_log_output):
    """Integration test for retrieval of game metadata for current fantasy season.

    Note:
        Tests :func:`~yfpy.query.YahooFantasySportsQuery.get_current_game_metadata`.

    """
    query_result_data = yahoo_data.save(
        "current-game-metadata",
        yahoo_query.get_current_game_metadata
    )
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(
        "current-game-metadata",
        Game,
        all_output_as_json_str=yahoo_query.all_output_as_json_str
    )
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_game_info_by_game_id(yahoo_query, yahoo_data, data_dir, season, game_id, show_log_output):
    """Integration test for retrieval of game info for specific game by id.

    Note:
        Tests :func:`~yfpy.query.YahooFantasySportsQuery.get_game_info_by_game_id`.

    """
    new_data_dir = data_dir / str(season)
    query_result_data = yahoo_data.save(
        f"{game_id}-game-info",
        yahoo_query.get_game_info_by_game_id,
        params={"game_id": game_id},
        new_data_dir=new_data_dir
    )
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(
        f"{game_id}-game-info",
        Game,
        new_data_dir=new_data_dir,
        all_output_as_json_str=yahoo_query.all_output_as_json_str
    )
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_game_metadata_by_game_id(yahoo_query, yahoo_data, data_dir, season, game_id, show_log_output):
    """Integration test for retrieval of game metadata for specific game by id.

    Note:
        Tests :func:`~yfpy.query.YahooFantasySportsQuery.get_game_metadata_by_game_id`.

    """
    new_data_dir = data_dir / str(season)
    query_result_data = yahoo_data.save(
        f"{game_id}-game-metadata",
        yahoo_query.get_game_metadata_by_game_id,
        params={"game_id": game_id},
        new_data_dir=new_data_dir
    )
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(
        f"{game_id}-game-metadata",
        Game,
        new_data_dir=new_data_dir,
        all_output_as_json_str=yahoo_query.all_output_as_json_str
    )
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_league_key(yahoo_query, yahoo_data, data_dir, season, game_id, league_id, show_log_output):
    """Integration test for retrieval of league key for selected league.

    Note:
        Tests :func:`~yfpy.query.YahooFantasySportsQuery.get_league_key`.

    """
    query_result_data = yahoo_query.get_league_key()
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    assert query_result_data == f"{game_id}.l.{league_id}"


@pytest.mark.integration
def test_get_game_weeks_by_game_id(yahoo_query, yahoo_data, data_dir, season, game_id, show_log_output):
    """Integration test for retrieval of all valid weeks of a specific game by id.

    Note:
        Tests :func:`~yfpy.query.YahooFantasySportsQuery.get_game_weeks_by_game_id`.

    """
    new_data_dir = data_dir / str(season)
    query_result_data = yahoo_data.save(
        f"{game_id}-game-weeks",
        yahoo_query.get_game_weeks_by_game_id,
        params={"game_id": game_id},
        new_data_dir=new_data_dir
    )
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(
        f"{game_id}-game-weeks",
        new_data_dir=new_data_dir,
        all_output_as_json_str=yahoo_query.all_output_as_json_str
    )
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_game_stat_categories_by_game_id(yahoo_query, yahoo_data, data_dir, season, game_id, show_log_output):
    """Integration test for retrieval of all valid stat categories of a specific game by id.

    Note:
        Tests :func:`~yfpy.query.YahooFantasySportsQuery.get_game_stat_categories_by_game_id`.

    """
    new_data_dir = data_dir / str(season)
    query_result_data = yahoo_data.save(
        f"{game_id}-game-stat_categories",
        yahoo_query.get_game_stat_categories_by_game_id,
        params={"game_id": game_id},
        new_data_dir=new_data_dir
    )
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(
        f"{game_id}-game-stat_categories",
        StatCategories,
        new_data_dir=new_data_dir,
        all_output_as_json_str=yahoo_query.all_output_as_json_str
    )
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_game_position_types_by_game_id(yahoo_query, yahoo_data, data_dir, season, game_id, show_log_output):
    """Integration test for retrieval of all valid position types for specific game by id.

    Note:
        Tests :func:`~yfpy.query.YahooFantasySportsQuery.get_game_position_types_by_game_id`.

    """
    new_data_dir = data_dir / str(season)
    query_result_data = yahoo_data.save(
        f"{game_id}-game-position_types",
        yahoo_query.get_game_position_types_by_game_id,
        params={"game_id": game_id},
        new_data_dir=new_data_dir
    )
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(
        f"{game_id}-game-position_types",
        new_data_dir=new_data_dir,
        all_output_as_json_str=yahoo_query.all_output_as_json_str
    )
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_game_roster_positions_by_game_id(yahoo_query, yahoo_data, data_dir, season, game_id, show_log_output):
    """Integration test for retrieval of all valid roster positions for specific game by id.

    Note:
        Tests :func:`~yfpy.query.YahooFantasySportsQuery.get_game_roster_positions_by_game_id`.

    """
    new_data_dir = data_dir / str(season)
    query_result_data = yahoo_data.save(
        f"{game_id}-game-roster_positions",
        yahoo_query.get_game_roster_positions_by_game_id,
        params={"game_id": game_id},
        new_data_dir=new_data_dir
    )
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(
        f"{game_id}-game-roster_positions",
        new_data_dir=new_data_dir,
        all_output_as_json_str=yahoo_query.all_output_as_json_str
    )
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data
