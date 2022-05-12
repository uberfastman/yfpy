# -*- coding: utf-8 -*-
"""Pytest integration tests for Yahoo Fantasy Sports API team data.

Note:
    Tests saving and loading all Yahoo Fantasy Sports API team data.

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
from yfpy.models import Team, TeamPoints, TeamStandings, Roster
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
def test_get_team_info(yahoo_query, yahoo_data, data_dir, season, game_id, league_id, team_id, team_name,
                       show_log_output):
    """Retrieve info of specific team by team_id for chosen league.
    """
    new_data_dir = (data_dir / str(season) / (str(game_id) + ".l." + str(league_id)) / "teams"
                    / (str(team_id) + "-" + team_name))
    query_result_data = yahoo_data.save(str(team_id) + "-" + team_name + "-info",
                                        yahoo_query.get_team_info,
                                        params={"team_id": team_id}, new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(team_id) + "-" + team_name + "-info", Team,
                                         new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_team_metadata(yahoo_query, yahoo_data, data_dir, season, game_id, league_id, team_id, team_name,
                           show_log_output):
    """Retrieve metadata of specific team by team_id for chosen league.
    """
    new_data_dir = (data_dir / str(season) / (str(game_id) + ".l." + str(league_id)) / "teams"
                    / (str(team_id) + "-" + team_name))
    query_result_data = yahoo_data.save(str(team_id) + "-" + team_name + "-metadata",
                                        yahoo_query.get_team_metadata,
                                        params={"team_id": team_id}, new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(team_id) + "-" + team_name + "-metadata", Team,
                                         new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_team_stats(yahoo_query, yahoo_data, data_dir, season, game_id, league_id, team_id, team_name,
                        show_log_output):
    """Retrieve stats of specific team by team_id for chosen league.
    """
    new_data_dir = (data_dir / str(season) / (str(game_id) + ".l." + str(league_id)) / "teams"
                    / (str(team_id) + "-" + team_name))
    query_result_data = yahoo_data.save(str(team_id) + "-" + team_name + "-stats",
                                        yahoo_query.get_team_stats,
                                        params={"team_id": team_id}, new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(team_id) + "-" + team_name + "-stats", TeamPoints,
                                         new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_team_stats_by_week(yahoo_query, yahoo_data, data_dir, season, chosen_week, game_id, league_id, team_id,
                                team_name, show_log_output):
    """Retrieve stats of specific team by team_id and by week for chosen league.
    """
    new_data_dir = data_dir / str(season) / (str(game_id) + ".l." + str(league_id)) / ("week_" + str(chosen_week))
    query_result_data = yahoo_data.save(str(team_id) + "-" + team_name + "-stats",
                                        yahoo_query.get_team_stats_by_week,
                                        params={"team_id": team_id, "chosen_week": chosen_week},
                                        new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(team_id) + "-" + team_name + "-stats",
                                         new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_team_standings(yahoo_query, yahoo_data, data_dir, season, game_id, league_id, team_id, team_name,
                            show_log_output):
    """Retrieve standings of specific team by team_id for chosen league.
    """
    new_data_dir = (data_dir / str(season) / (str(game_id) + ".l." + str(league_id)) / "teams"
                    / (str(team_id) + "-" + team_name))
    query_result_data = yahoo_data.save(str(team_id) + "-" + team_name + "-standings",
                                        yahoo_query.get_team_standings,
                                        params={"team_id": team_id}, new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(team_id) + "-" + team_name + "-standings",
                                         TeamStandings, new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_team_roster_by_week(yahoo_query, yahoo_data, data_dir, season, chosen_week, game_id, league_id, team_id,
                                 team_name, show_log_output):
    """Retrieve roster of specific team by team_id and by week for chosen league.
    """
    new_data_dir = (data_dir / str(season) / (str(game_id) + ".l." + str(league_id)) / ("week_" + str(chosen_week))
                    / "rosters")
    query_result_data = yahoo_data.save(str(team_id) + "-" + team_name + "-roster_by_week",
                                        yahoo_query.get_team_roster_by_week,
                                        params={"team_id": team_id, "chosen_week": chosen_week},
                                        new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(team_id) + "-" + team_name + "-roster_by_week", Roster,
                                         new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_team_roster_player_info_by_week(yahoo_query, yahoo_data, data_dir, season, chosen_week, game_id,
                                             league_id, team_id, team_name, show_log_output):
    """Retrieve roster with player info of specific team by team_id and by week for chosen league.
    """
    new_data_dir = (data_dir / str(season) / (str(game_id) + ".l." + str(league_id)) / ("week_" + str(chosen_week))
                    / "rosters")
    query_result_data = yahoo_data.save(str(team_id) + "-" + team_name
                                        + "-roster-player_info_by_week",
                                        yahoo_query.get_team_roster_player_info_by_week,
                                        params={"team_id": team_id, "chosen_week": chosen_week},
                                        new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(team_id) + "-" + team_name
                                         + "-roster-player_info_by_week",
                                         new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.skip(
    reason="Skipping test_get_team_roster_player_info_by_date: retrieval by date supported by NHL/NBA/MLB, not NFL."
)
@pytest.mark.integration
def test_get_team_roster_player_info_by_date(yahoo_query, yahoo_data, data_dir, season, chosen_date, game_id,
                                             league_id, team_id, team_name, show_log_output):
    """Retrieve roster with player info of specific team by team_id and by date for chosen league.
    """
    new_data_dir = data_dir / str(season) / (str(game_id) + ".l." + str(league_id)) / str(chosen_date) / "rosters"
    query_result_data = yahoo_data.save(str(team_id) + "-" + team_name
                                        + "-roster-player_info_by_date",
                                        yahoo_query.get_team_roster_player_info_by_date,
                                        params={"team_id": team_id, "chosen_date": chosen_date},
                                        new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(team_id) + "-" + team_name
                                         + "-roster-player_info_by_date",
                                         new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_team_roster_player_stats(yahoo_query, yahoo_data, data_dir, season, game_id, league_id, team_id,
                                      team_name, show_log_output):
    """Retrieve roster with player info for season of specific team by team_id for chosen league.
    """
    new_data_dir = data_dir / str(season) / (str(game_id) + ".l." + str(league_id)) / "rosters"
    query_result_data = yahoo_data.save(str(team_id) + "-" + team_name + "-roster-player_stats",
                                        yahoo_query.get_team_roster_player_stats,
                                        params={"team_id": team_id},
                                        new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(team_id) + "-" + team_name + "-roster-player_stats",
                                         new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_team_roster_player_stats_by_week(yahoo_query, yahoo_data, data_dir, season, chosen_week, game_id,
                                              league_id, team_id, team_name, show_log_output):
    """Retrieve roster with player stats of specific team by team_id and by week for chosen league.
    """
    new_data_dir = (data_dir / str(season) / (str(game_id) + ".l." + str(league_id)) / ("week_" + str(chosen_week))
                    / "rosters")

    query_result_data = yahoo_data.save(str(team_id) + "-" + team_name
                                        + "-roster-player_stats_by_week",
                                        yahoo_query.get_team_roster_player_stats_by_week,
                                        params={"team_id": team_id, "chosen_week": chosen_week},
                                        new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(team_id) + "-" + team_name
                                         + "-roster-player_stats_by_week",
                                         new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_team_draft_results(yahoo_query, yahoo_data, data_dir, season, game_id, league_id, team_id, team_name,
                                show_log_output):
    """Retrieve draft results of specific team by team_id for chosen league.
    """
    new_data_dir = (data_dir / str(season) / (str(game_id) + ".l." + str(league_id)) / "teams"
                    / (str(team_id) + "-" + team_name))
    query_result_data = yahoo_data.save(str(team_id) + "-" + team_name + "-draft_results",
                                        yahoo_query.get_team_draft_results,
                                        params={"team_id": team_id}, new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(team_id) + "-" + team_name + "-draft_results",
                                         new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data


@pytest.mark.integration
def test_get_team_matchups(yahoo_query, yahoo_data, data_dir, season, game_id, league_id, team_id, team_name,
                           show_log_output):
    """Retrieve matchups of specific team by team_id for chosen league.
    """
    new_data_dir = (data_dir / str(season) / (str(game_id) + ".l." + str(league_id)) / "teams"
                    / (str(team_id) + "-" + team_name))
    query_result_data = yahoo_data.save(str(team_id) + "-" + team_name + "-matchups",
                                        yahoo_query.get_team_matchups,
                                        params={"team_id": team_id}, new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(query_result_data))

    loaded_result_data = yahoo_data.load(str(team_id) + "-" + team_name + "-matchups",
                                         new_data_dir=new_data_dir)
    if show_log_output:
        logger.info(prettify_data(loaded_result_data))

    assert query_result_data == loaded_result_data
