__author__ = "Wren J. R. (uberfastman)"
__email__ = "uberfastman@uberfastman.dev"

import pytest
from yfpy import Data
from pathlib import Path
from yfpy.query import YahooFantasySportsQuery
import os

"""
Example public Yahoo league uRL: "https://archive.fantasysports.yahoo.com/nfl/2014/729259"

Example vars using public Yahoo leagues still require auth through a personal Yahoo account: see README.md
"""


@pytest.fixture
def auth_dir():
    """Put private.json (see README.md) in yfpy/test/integration/ directory."""
    return Path(__file__).parent


@pytest.fixture
def data_dir():
    """Code tests will output data to this directory."""
    return Path(__file__).parent / "test_output"


@pytest.fixture
def yahoo_data(data_dir):
    """Instantiate yfpy Data object."""
    return Data(data_dir)


@pytest.fixture
def yahoo_query(auth_dir, league_id, game_key, game_code):
    """Instantiate yfpy YahooFantasySportsQuery object and override league key."""
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

    return yahoo_query


@pytest.fixture
def browser_callback():
    """Turn on/off automatic opening of browser window for OAuth."""
    browser_callback = True
    return browser_callback


@pytest.fixture
def season():
    """Set Yahoo Fantasy Sports season for testing."""

    # season = "2012"
    # season = "2014"
    # season = "2015"
    # season = "2019"
    # season = "2020"
    season = "2021"

    return season


@pytest.fixture
def chosen_week():
    """Set Yahoo Fantasy Sports chosen week for testing."""

    chosen_week = 1

    return chosen_week


@pytest.fixture
def chosen_date():
    """Set Yahoo Fantasy Sports chosen date for testing."""

    # chosen_date = "2013-04-15"  # NHL - 2013
    # chosen_date = "2013-04-16"  # NHL - 2013
    chosen_date = "2021-10-25"  # NHL - 2021

    return chosen_date


@pytest.fixture
def league_id():
    """Set Yahoo Fantasy Sports league ID for testing."""

    # league_id = "907359"  # NFL - 2015 (testing for league with divisions)
    # league_id = "79230"  # NFL - 2019
    # league_id = "655434"  # NFL - 2020
    league_id = "413954"  # NFL - 2021

    # league_id = "69624"  # NHL - 2012
    # league_id = "101592"  # NHL - 2021

    return league_id


@pytest.fixture
def game_key():
    """Set Yahoo Fantasy Sports game key for testing."""

    # game_key = "331"  # NFL - 2014
    # game_key = "348"  # NFL - 2015 (testing for league with divisions)
    # game_key = "390"  # NFL - 2019
    # game_key = "399"  # NFL - 2020
    game_key = "406"  # NFL - 2021

    # game_key = "303"  # NHL - 2012
    # game_key = "411"  # NHL - 2021

    return game_key


@pytest.fixture
def game_code():
    """Set Yahoo Fantasy Sports game code for testing."""

    game_code = "nfl"

    # game_code = "nhl"  # NHL

    return game_code


@pytest.fixture
def team_id():
    """Set Yahoo Fantasy Sports team ID for testing."""

    team_id = 1

    return team_id


@pytest.fixture
def team_name():
    """Set Yahoo Fantasy Sports team name for testing."""

    team_name = "Legion"

    return team_name


@pytest.fixture
def player_id():
    """Create and set Yahoo Fantasy Sports player ID for testing."""

    player_id = "7200"  # NFL: Aaron Rodgers - 2020/2021

    # player_id = "4588"  # NHL: Braden Holtby - 2012
    # player_id = "8205"  # NHL: Jeffrey Viel - 2021
    # player_id = "3637"  # NHL: Alex Ovechkin - 2021

    return player_id


@pytest.fixture
def player_key(game_key, player_id):
    """Create and set Yahoo Fantasy Sports player key for testing."""

    player_key = game_key + ".p." + player_id

    return player_key


@pytest.fixture
def league_player_limit():
    """Set Yahoo Fantasy Sports league player retrieval limit for testing."""

    league_player_limit = 101
    # league_player_limit = 2610

    return league_player_limit
