# -*- coding: utf-8 -*-
"""Pytest integration test conftest.py.

"""
__author__ = "Wren J. R. (uberfastman)"
__email__ = "uberfastman@uberfastman.dev"

import os
from pathlib import Path
from typing import Union
from quickstart import quickstart

import pytest

from yfpy import Data
from yfpy.query import YahooFantasySportsQuery

"""
Example public Yahoo league URL: "https://archive.fantasysports.yahoo.com/nfl/2014/729259"

Example vars using public Yahoo leagues still require auth through a personal Yahoo account: see README.md
"""


@pytest.fixture
def auth_dir() -> Path:
    """Put private.json (see README.md) in yfpy/auth/ directory."""
    return Path(__file__).parent.parent.parent / "auth"


@pytest.fixture
def data_dir() -> Path:
    """Code tests will output data to this directory."""
    return Path(__file__).parent / "test_output"


@pytest.fixture
def yahoo_data(data_dir: Union[Path, str]) -> Data:
    """Instantiate yfpy Data object."""
    return Data(data_dir)


@pytest.fixture
def yahoo_query(auth_dir: Union[Path, str], league_id: str, game_code: str, game_id: int,
                browser_callback: bool) -> YahooFantasySportsQuery:
    """Instantiate yfpy YahooFantasySportsQuery object and override league key."""
    yahoo_query = YahooFantasySportsQuery(
        auth_dir,
        league_id,
        game_code,
        game_id=game_id,
        offline=False,
        all_output_as_json_str=False,
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
    return quickstart.get_season()


@pytest.fixture
def chosen_week() -> int:
    """Set Yahoo Fantasy Sports chosen week for testing."""
    return quickstart.get_chosen_week()


@pytest.fixture
def chosen_date() -> str:
    """Set Yahoo Fantasy Sports chosen date for testing."""
    return quickstart.get_chosen_date()


@pytest.fixture
def game_code() -> str:
    """Set Yahoo Fantasy Sports game code for testing."""
    return quickstart.get_game_code()


@pytest.fixture
def game_id() -> int:
    """Set Yahoo Fantasy Sports game ID for testing."""
    return quickstart.get_game_id()


@pytest.fixture
def game_key() -> str:
    """Set Yahoo Fantasy Sports game key for testing."""
    return quickstart.get_game_key()


@pytest.fixture
def league_id() -> str:
    """Set Yahoo Fantasy Sports league ID for testing."""
    return quickstart.get_league_id()


@pytest.fixture
def team_id() -> int:
    """Set Yahoo Fantasy Sports team ID for testing."""
    return quickstart.get_team_id()


@pytest.fixture
def team_name() -> str:
    """Set Yahoo Fantasy Sports team name for testing."""
    return quickstart.get_team_name()


@pytest.fixture
def player_id() -> int:
    """Create and set Yahoo Fantasy Sports player ID for testing."""
    return quickstart.get_player_id()


@pytest.fixture
def player_key(game_id, player_id) -> str:
    """Create and set Yahoo Fantasy Sports player key for testing."""

    player_key = f"{game_id}.p.{player_id}"

    return player_key


@pytest.fixture
def league_player_limit() -> int:
    """Set Yahoo Fantasy Sports league player retrieval limit for testing."""
    return quickstart.get_league_player_limit()
