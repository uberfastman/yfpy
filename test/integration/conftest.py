# -*- coding: utf-8 -*-
"""Pytest integration test conftest.py.

"""
__author__ = "Wren J. R. (uberfastman)"
__email__ = "uberfastman@uberfastman.dev"

import os
from pathlib import Path
from typing import Union

import pytest

from yfpy import Data
from yfpy.query import YahooFantasySportsQuery

"""
Example public Yahoo league URL: "https://archive.fantasysports.yahoo.com/nfl/2014/729259"

Example vars using public Yahoo leagues still require auth through a personal Yahoo account: see README.md
"""


@pytest.fixture
def auth_dir() -> Path:
    """Put private.json (see README.md) in yfpy/test/integration/ directory."""
    return Path(__file__).parent


@pytest.fixture
def data_dir() -> Path:
    """Code tests will output data to this directory."""
    return Path(__file__).parent / "test_output"


@pytest.fixture
def yahoo_data(data_dir: Union[Path, str]) -> Data:
    """Instantiate yfpy Data object."""
    return Data(data_dir)


@pytest.fixture
def yahoo_query(auth_dir: Union[Path, str], league_id: str, game_id, game_code: str,
                browser_callback: bool) -> YahooFantasySportsQuery:
    """Instantiate yfpy YahooFantasySportsQuery object and override league key."""
    yahoo_query = YahooFantasySportsQuery(
        auth_dir,
        league_id,
        game_id=game_id,
        game_code=game_code,
        offline=False,
        all_output_as_json=False,
        consumer_key=os.environ["YFPY_CONSUMER_KEY"],
        consumer_secret=os.environ["YFPY_CONSUMER_SECRET"],
        browser_callback=browser_callback
    )

    # Manually override league key for example code to work
    yahoo_query.league_key = f"{game_id}.l.{league_id}"

    return yahoo_query


@pytest.fixture
def browser_callback() -> bool:
    """Turn on/off automatic opening of browser window for OAuth."""
    browser_callback = True
    return browser_callback


@pytest.fixture
def season() -> int:
    """Set Yahoo Fantasy Sports season for testing."""

    # season = 2012
    # season = 2014
    # season = 2015
    # season = 2019
    # season = 2020
    season = 2021
    # season = 2022

    return season


@pytest.fixture
def chosen_week() -> int:
    """Set Yahoo Fantasy Sports chosen week for testing."""

    chosen_week = 1

    return chosen_week


@pytest.fixture
def chosen_date() -> str:
    """Set Yahoo Fantasy Sports chosen date for testing."""

    chosen_date = "2013-04-15"  # NHL - 2013 (for 2012)
    # chosen_date = "2013-04-16"  # NHL - 2013
    # chosen_date = "2021-10-25"  # NHL - 2021

    # chosen_date = "2021-04-01"  # MLB - 2021
    # chosen_date = "2022-04-10"  # MLB - 2022

    return chosen_date


@pytest.fixture
def league_id() -> str:
    """Set Yahoo Fantasy Sports league ID for testing."""

    # league_id = "907359"  # NFL - 2015 (testing for league with divisions)
    # league_id = "79230"  # NFL - 2019
    # league_id = "655434"  # NFL - 2020
    league_id = "413954"  # NFL - 2021

    # league_id = "69624"  # NHL - 2012
    # league_id = "101592"  # NHL - 2021

    # league_id = "40134"  # MLB - 2021

    return league_id


@pytest.fixture
def game_id() -> int:
    """Set Yahoo Fantasy Sports game ID for testing."""

    # game_id = 331  # NFL - 2014
    # game_id = 348  # NFL - 2015 (testing for league with divisions)
    # game_id = 390  # NFL - 2019
    # game_id = 399  # NFL - 2020
    game_id = 406  # NFL - 2021

    # game_id = 303  # NHL - 2012
    # game_id = 411  # NHL - 2021

    # game_id = 404  # MLB - 2021
    # game_id = 412  # MLB - 2022

    return game_id


@pytest.fixture
def game_key() -> str:
    """Set Yahoo Fantasy Sports game key for testing."""

    # game_key = "331"  # NFL - 2014
    # game_key = "348"  # NFL - 2015 (testing for league with divisions)
    # game_key = "390"  # NFL - 2019
    # game_key = "399"  # NFL - 2020
    game_key = "406"  # NFL - 2021

    # game_key = "303"  # NHL - 2012
    # game_key = "411"  # NHL - 2021

    # game_key = "404"  # MLB - 2021
    # game_key = "412"  # MLB - 2022

    return game_key


@pytest.fixture
def game_code() -> str:
    """Set Yahoo Fantasy Sports game code for testing."""

    game_code = "nfl"  # NFL

    # game_code = "nhl"  # NHL

    # game_code = "mlb"  # MLB

    return game_code


@pytest.fixture
def team_id() -> int:
    """Set Yahoo Fantasy Sports team ID for testing."""

    team_id = 1  # NFL

    # team_id = 2  # NHL (2012)

    return team_id


@pytest.fixture
def team_name() -> str:
    """Set Yahoo Fantasy Sports team name for testing."""

    team_name = "Legion"  # NFL

    # team_name = "The Bateleurs"  # NHL (2012)

    return team_name


@pytest.fixture
def player_id() -> int:
    """Create and set Yahoo Fantasy Sports player ID for testing."""

    player_id = 7200  # NFL: Aaron Rodgers - 2020/2021

    # player_id = 4588  # NHL: Braden Holtby - 2012
    # player_id = 8205  # NHL: Jeffrey Viel - 2021
    # player_id = 3637  # NHL: Alex Ovechkin - 2021

    # player_id = 9897  # MLB: Tim Anderson - 2021/2022

    return player_id


@pytest.fixture
def player_key(game_id, player_id) -> str:
    """Create and set Yahoo Fantasy Sports player key for testing."""

    player_key = f"{game_id}.p.{player_id}"

    return player_key


@pytest.fixture
def league_player_limit() -> int:
    """Set Yahoo Fantasy Sports league player retrieval limit for testing."""

    league_player_limit = 101
    # league_player_limit = 2610

    return league_player_limit
