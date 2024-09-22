# -*- coding: utf-8 -*-
"""Pytest integration tests for Yahoo Fantasy Sports API player data.

Note:
    Tests saving and loading all Yahoo Fantasy Sports API player data.

Attributes:
    logger (Logger): Game data integration tests logger.

"""
__author__ = "Wren J. R. (uberfastman)"
__email__ = "uberfastman@uberfastman.dev"

import logging
import warnings

import pytest

from yfpy.logger import get_logger
from yfpy.models import Player
from yfpy.utils import prettify_data

logger = get_logger(__name__)

# Suppress YahooFantasySportsQuery debug logging
logging.getLogger("yfpy.query").setLevel(level=logging.INFO)

# Ignore resource warnings from unittest module
warnings.simplefilter("ignore", ResourceWarning)


@pytest.mark.integration
def test_get_player_stats_for_season(yahoo_query, yahoo_data, data_dir, season, game_id, league_id, player_id,
                                     player_key, show_log_output):
    """Integration test for retrieval of player stats by season for chosen Yahoo fantasy league.

    Note:
        Tests :func:`~yfpy.query.YahooFantasySportsQuery.get_player_stats_for_season`.

    """
    new_data_dir = data_dir / str(season) / f"{game_id}.l.{league_id}" / "players"
    query_result_data = yahoo_data.save(
        f"{player_id}-player-season-stats",
        yahoo_query.get_player_stats_for_season,
        params={"player_key": str(player_key)},
        new_data_dir=new_data_dir
    )
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(
        f"{player_id}-player-season-stats",
        Player,
        new_data_dir=new_data_dir,
        all_output_as_json_str=yahoo_query.all_output_as_json_str
    )
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_player_stats_by_week(yahoo_query, yahoo_data, data_dir, season, chosen_week, game_id, league_id,
                                  player_id, player_key, show_log_output):
    """Integration test for retrieval of player stats by week for chosen Yahoo fantasy league..

    Note:
        Tests :func:`~yfpy.query.YahooFantasySportsQuery.get_player_stats_by_week`.

    """
    new_data_dir = data_dir / str(season) / f"{game_id}.l.{league_id}" / f"week_{chosen_week}" / "players"
    query_result_data = yahoo_data.save(
        f"{player_id}-player-stats",
        yahoo_query.get_player_stats_by_week,
        params={"player_key": str(player_key), "chosen_week": str(chosen_week)},
        new_data_dir=new_data_dir
    )
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(
        f"{player_id}-player-stats",
        Player,
        new_data_dir=new_data_dir,
        all_output_as_json_str=yahoo_query.all_output_as_json_str
    )
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.skip(
    reason="Skipping test_get_player_stats_by_date: retrieval by date supported by NHL/NBA/MLB, not NFL."
)
@pytest.mark.integration
def test_get_player_stats_by_date(yahoo_query, yahoo_data, data_dir, season, chosen_date, game_id, league_id,
                                  player_id, player_key, show_log_output):
    """Integration test for retrieval of player stats by date for Yahoo fantasy league.

    Note:
        Tests :func:`~yfpy.query.YahooFantasySportsQuery.get_player_stats_by_date`.

    """
    new_data_dir = data_dir / str(season) / f"{game_id}.l.{league_id}" / str(chosen_date) / "players"
    query_result_data = yahoo_data.save(
        f"{player_id}-player-stats",
        yahoo_query.get_player_stats_by_date,
        params={"player_key": str(player_key), "chosen_date": chosen_date},
        new_data_dir=new_data_dir
    )
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(
        f"{player_id}-player-stats",
        Player,
        new_data_dir=new_data_dir,
        all_output_as_json_str=yahoo_query.all_output_as_json_str
    )
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_player_ownership(yahoo_query, yahoo_data, data_dir, season, game_id, league_id, player_id, player_key,
                              show_log_output):
    """Integration test for retrieval of ownership of chosen player for chosen Yahoo fantasy league.

    Note:
        Tests :func:`~yfpy.query.YahooFantasySportsQuery.get_player_ownership`.

    """
    new_data_dir = data_dir / str(season) / f"{game_id}.l.{league_id}" / "players"
    query_result_data = yahoo_data.save(
        f"{player_id}-player-ownership",
        yahoo_query.get_player_ownership,
        params={"player_key": str(player_key)},
        new_data_dir=new_data_dir
    )
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(
        f"{player_id}-player-ownership",
        Player,
        new_data_dir=new_data_dir,
        all_output_as_json_str=yahoo_query.all_output_as_json_str
    )
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_player_percent_owned_by_week(yahoo_query, yahoo_data, data_dir, season, chosen_week, game_id, league_id,
                                          player_id, player_key, show_log_output):
    """Integration test for retrieval of percent ownership by week of chosen player for chosen Yahoo fantasy league.

    Note:
        Tests :func:`~yfpy.query.YahooFantasySportsQuery.get_player_percent_owned_by_week`.

    """
    new_data_dir = data_dir / str(season) / f"{game_id}.l.{league_id}" / f"week_{chosen_week}" / "players"
    query_result_data = yahoo_data.save(
        f"{player_id}-player-percent_owned",
        yahoo_query.get_player_percent_owned_by_week,
        params={"player_key": str(player_key), "chosen_week": str(chosen_week)},
        new_data_dir=new_data_dir
    )
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(
        f"{player_id}-player-percent_owned",
        Player,
        new_data_dir=new_data_dir,
        all_output_as_json_str=yahoo_query.all_output_as_json_str
    )
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_player_draft_analysis(yahoo_query, yahoo_data, data_dir, season, game_id, league_id, player_id,
                                   player_key, show_log_output):
    """Integration test for retrieval of player draft analysis of chosen player for chosen Yahoo fantasy league.

    Note:
        Tests :func:`~yfpy.query.YahooFantasySportsQuery.get_player_draft_analysis`.

    """
    new_data_dir = data_dir / str(season) / f"{game_id}.l.{league_id}" / "players"
    query_result_data = yahoo_data.save(
        f"{player_id}-player-draft_analysis",
        yahoo_query.get_player_draft_analysis,
        params={"player_key": str(player_key)}, new_data_dir=new_data_dir
    )
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(
        f"{player_id}-player-draft_analysis",
        Player,
        new_data_dir=new_data_dir,
        all_output_as_json_str=yahoo_query.all_output_as_json_str
    )
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data
