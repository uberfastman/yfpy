# -*- coding: utf-8 -*-
"""Pytest integration tests for Yahoo Fantasy Sports API user data.

Note:
    Tests saving and loading all Yahoo Fantasy Sports API user data.

Attributes:
    logger (Logger): Game data integration tests logger.

"""
__author__ = "Wren J. R. (uberfastman)"
__email__ = "uberfastman@uberfastman.dev"

import logging
import warnings

import pytest

from yfpy.logger import get_logger
from yfpy.models import User
from yfpy.utils import prettify_data

logger = get_logger(__name__)

# Suppress YahooFantasySportsQuery debug logging
logging.getLogger("yfpy.query").setLevel(level=logging.INFO)

# Ignore resource warnings from unittest module
warnings.simplefilter("ignore", ResourceWarning)


@pytest.mark.integration
def test_get_current_user(yahoo_query, yahoo_data, data_dir, season, game_id, show_log_output):
    """Integration test for retrieval of metadata for current logged-in Yahoo user.

    Note:
        Tests :func:`~yfpy.query.YahooFantasySportsQuery.get_current_user`.

    """
    new_data_dir = data_dir
    query_result_data = yahoo_data.save("user", yahoo_query.get_current_user, new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(
        "user",
        User,
        new_data_dir=new_data_dir,
        all_output_as_json_str=yahoo_query.all_output_as_json_str
    )
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_user_games(yahoo_query, yahoo_data, data_dir, season, game_id, show_log_output):
    """Integration test for retrieval of game history for current logged-in Yahoo user.

    Note:
        Tests :func:`~yfpy.query.YahooFantasySportsQuery.get_user_games`.

    """
    new_data_dir = data_dir
    query_result_data = yahoo_data.save(
        "user-games",
        yahoo_query.get_user_games,
        new_data_dir=new_data_dir
    )
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(
        "user-games",
        new_data_dir=new_data_dir,
        all_output_as_json_str=yahoo_query.all_output_as_json_str
    )
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.skip(
    reason="Skipping get_user_leagues_by_game_key: current logged-in user must have leagues from test season/year."
)
@pytest.mark.integration
def test_get_user_leagues_by_game_id(yahoo_query, yahoo_data, data_dir, season, game_id, show_log_output):
    """Integration test for retrieval of league history by game ID for current logged-in Yahoo user.

    Note:
        Tests :func:`~yfpy.query.YahooFantasySportsQuery.get_user_leagues_by_game_key`.

    """
    new_data_dir = data_dir
    query_result_data = yahoo_data.save(
        "user-leagues",
        yahoo_query.get_user_leagues_by_game_key,
        params={"game_key": game_id},
        new_data_dir=new_data_dir
    )

    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(
        "user-leagues",
        new_data_dir=new_data_dir,
        all_output_as_json_str=yahoo_query.all_output_as_json_str
    )
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_user_teams(yahoo_query, yahoo_data, data_dir, season, game_id, show_log_output):
    """Integration test for retrieval of teams for the current game for the current logged-in Yahoo user.

    Note:
        Tests :func:`~yfpy.query.YahooFantasySportsQuery.get_user_teams`.

    """
    """Retrieve teams for all leagues for current logged-in user for current game.
    """
    new_data_dir = data_dir
    query_result_data = yahoo_data.save(
        "user-teams",
        yahoo_query.get_user_teams,
        new_data_dir=new_data_dir
    )
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(
        "user-teams",
        new_data_dir=new_data_dir,
        all_output_as_json_str=yahoo_query.all_output_as_json_str
    )
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data
