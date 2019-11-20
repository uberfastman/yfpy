__author__ = "Wren J. R. (uberfastman)"
__email__ = "wrenjr@yahoo.com"

import logging
import os
import pprint
import unittest
import warnings
from unittest import skip, TestCase

from yfpy import Data
from yfpy.models import Game, StatCategories, User, Scoreboard, Settings, Standings, League, Player, Team, \
    TeamPoints, TeamStandings, Roster
from yfpy.query import YahooFantasySportsQuery


class QueryTestCase(TestCase):

    def setUp(self):
        # Suppress YahooFantasySportsQuery debug logging
        logging.getLogger("yfpy.query").setLevel(level=logging.INFO)

        # Ignore resource warnings from unittest module
        warnings.simplefilter("ignore", ResourceWarning)

        # Turn on/off example code stdout printing output
        self.print_output = False

        # Put private.json (see README.md) in examples directory
        auth_dir = "."

        # Example code will output data here
        self.data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_output")

        # Example vars using public Yahoo league (still requires auth through a personal Yahoo account - see README.md)
        self.game_id = "331"
        # self.game_id = "390"
        # self.game_id = "303"  # NHL
        # self.game_id = "348"  # divisions
        self.game_code = "nfl"
        # self.game_code = "nhl"  # NHL
        self.season = "2014"
        # self.season = "2019"
        # self.season = "2012"  # NHL
        # self.season = "2015"  # divisions
        self.league_id = "729259"
        # self.league_id = "79230"
        # self.league_id = "69624"  # NHL
        # self.league_id = "907359"  # divisions
        # example_public_league_url = "https://archive.fantasysports.yahoo.com/nfl/2014/729259"

        # Test vars
        self.chosen_week = 1
        self.chosen_date = "2013-04-15"  # NHL
        # self.chosen_date = "2013-04-16"  # NHL
        self.team_id = 1
        self.team_name = "Legion"
        self.player_id = "7200"  # NFL: Aaron Rodgers
        # self.player_id = "4588"  # NHL: Braden Holtby
        self.player_key = self.game_id + ".p." + self.player_id

        # Instantiate yfpy objects
        self.yahoo_data = Data(self.data_dir)
        self.yahoo_query = YahooFantasySportsQuery(auth_dir, self.league_id, game_id=self.game_id,
                                                   game_code=self.game_code, offline=False)

        # Manually override league key for example code to work
        self.yahoo_query.league_key = self.game_id + ".l." + self.league_id

    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ •
    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ SAVING AND LOADING FANTASY FOOTBALL GAME DATA • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ •
    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ •

    def test_get_all_yahoo_fantasy_game_keys(self):
        """Retrieve all Yahoo fantasy football game keys.
        """
        query_result_data = self.yahoo_data.save(self.game_code + "-game_keys",
                                                 self.yahoo_query.get_all_yahoo_fantasy_game_keys)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load(self.game_code + "-game_keys")
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    def test_get_game_key_by_season(self):
        """Retrieve specific game key by season.
        """
        query_result_data = self.yahoo_query.get_game_key_by_season(season=self.season)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, self.game_id)

    def test_get_current_game_info(self):
        """Retrieve game info for current fantasy season.
        """
        query_result_data = self.yahoo_data.save("current-game-info", self.yahoo_query.get_current_game_info)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load("current-game-info", Game)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    def test_get_current_game_metadata(self):
        """Retrieve game metadata for current fantasy season.
        """
        query_result_data = self.yahoo_data.save("current-game-metadata", self.yahoo_query.get_current_game_metadata)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load("current-game-metadata", Game)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    def test_get_game_info_by_game_id(self):
        """Retrieve game info for specific game by id.
        """
        new_data_dir = os.path.join(self.data_dir, str(self.season))
        query_result_data = self.yahoo_data.save(str(self.game_id) + "-game-info",
                                                 self.yahoo_query.get_game_info_by_game_id,
                                                 params={"game_id": self.game_id}, new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load(str(self.game_id) + "-game-info", Game, new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    def test_get_game_metadata_by_game_id(self):
        """Retrieve game metadata for specific game by id.
        """
        new_data_dir = os.path.join(self.data_dir, str(self.season))
        query_result_data = self.yahoo_data.save(str(self.game_id) + "-game-metadata",
                                                 self.yahoo_query.get_game_metadata_by_game_id,
                                                 params={"game_id": self.game_id}, new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load(str(self.game_id) + "-game-metadata", Game, new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    def test_get_league_key(self):
        """Retrieve league key for selected league.
        """
        query_result_data = self.yahoo_query.get_league_key()
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, self.game_id + ".l." + self.league_id)

    def test_get_game_weeks_by_game_id(self):
        """Retrieve all valid weeks of a specific game by id.
        """
        new_data_dir = os.path.join(self.data_dir, str(self.season))
        query_result_data = self.yahoo_data.save(str(self.game_id) + "-game-weeks",
                                                 self.yahoo_query.get_game_weeks_by_game_id,
                                                 params={"game_id": self.game_id}, new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load(str(self.game_id) + "-game-weeks", new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    def test_get_game_stat_categories_by_game_id(self):
        """Retrieve all valid stat categories of a specific game by id.
        """
        new_data_dir = os.path.join(self.data_dir, str(self.season))
        query_result_data = self.yahoo_data.save(str(self.game_id) + "-game-stat_categories",
                                                 self.yahoo_query.get_game_stat_categories_by_game_id,
                                                 params={"game_id": self.game_id}, new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load(str(self.game_id) + "-game-stat_categories", StatCategories,
                                                  new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    def test_get_game_position_types_by_game_id(self):
        """Retrieve all valid position types for specific game by id.
        """
        new_data_dir = os.path.join(self.data_dir, str(self.season))
        query_result_data = self.yahoo_data.save(str(self.game_id) + "-game-position_types",
                                                 self.yahoo_query.get_game_position_types_by_game_id,
                                                 params={"game_id": self.game_id}, new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load(str(self.game_id) + "-game-position_types", new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    def test_get_game_roster_positions_by_game_id(self):
        """Retrieve all valid roster positions for specific game by id.
        """
        new_data_dir = os.path.join(self.data_dir, str(self.season))
        query_result_data = self.yahoo_data.save(str(self.game_id) + "-game-roster_positions",
                                                 self.yahoo_query.get_game_roster_positions_by_game_id,
                                                 params={"game_id": self.game_id}, new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load(str(self.game_id) + "-game-roster_positions",
                                                  new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~
    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ SAVING AND LOADING USER HISTORICAL DATA • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~
    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~

    def test_get_current_user(self):
        """Retrieve metadata for current logged-in user.
        """
        new_data_dir = self.data_dir
        query_result_data = self.yahoo_data.save("user", self.yahoo_query.get_current_user, new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load("user", User, new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    def test_get_user_games(self):
        """Retrieve game history for current logged-in user.
        """
        new_data_dir = self.data_dir
        query_result_data = self.yahoo_data.save("user-games", self.yahoo_query.get_user_games,
                                                 new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load("user-games", new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    @skip("skipping get_user_leagues_by_game_key when current logged-in user has no leagues from test season/year")
    def test_get_user_leagues_by_game_id(self):
        """Retrieve league history for current logged-in user for specific game by id.
        """
        new_data_dir = self.data_dir
        query_result_data = self.yahoo_data.save("user-leagues", self.yahoo_query.get_user_leagues_by_game_key,
                                                 params={"game_id": self.game_id}, new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load("user-leagues", new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    def test_get_user_teams(self):
        """Retrieve teams for all leagues for current logged-in user for current game.
        """
        new_data_dir = self.data_dir
        query_result_data = self.yahoo_data.save("user-teams", self.yahoo_query.get_user_teams,
                                                 new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load("user-teams", new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~
    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ SAVING AND LOADING FANTASY FOOTBALL LEAGUE DATA • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~
    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~

    def test_get_league_info(self):
        """Retrieve info for chosen league.
        """
        new_data_dir = os.path.join(self.data_dir, str(self.season), str(self.game_id) + ".l." + str(self.league_id))
        query_result_data = self.yahoo_data.save(str(self.league_id) + "-league-info",
                                                 self.yahoo_query.get_league_info, new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load(str(self.league_id) + "-league-info", League,
                                                  new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    def test_get_league_metadata(self):
        """Retrieve metadata for chosen league.
        """
        new_data_dir = os.path.join(self.data_dir, str(self.season), str(self.game_id) + ".l." + str(self.league_id))
        query_result_data = self.yahoo_data.save(str(self.league_id) + "-league-metadata",
                                                 self.yahoo_query.get_league_metadata, new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load(str(self.league_id) + "-league-metadata", League,
                                                  new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    def test_get_league_settings(self):
        """Retrieve settings (rules) for chosen league.
        """
        new_data_dir = os.path.join(self.data_dir, str(self.season), str(self.game_id) + ".l." + str(self.league_id))
        query_result_data = self.yahoo_data.save(str(self.league_id) + "-league-settings",
                                                 self.yahoo_query.get_league_settings, new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load(str(self.league_id) + "-league-settings", Settings,
                                                  new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    def test_get_league_standings(self):
        """Retrieve standings for chosen league.
        """
        new_data_dir = os.path.join(self.data_dir, str(self.season), str(self.game_id) + ".l." + str(self.league_id))
        query_result_data = self.yahoo_data.save(str(self.league_id) + "-league-standings",
                                                 self.yahoo_query.get_league_standings, new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load(str(self.league_id) + "-league-standings", Standings,
                                                  new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    def test_get_league_teams(self):
        """Retrieve teams for chosen league.
        """
        new_data_dir = os.path.join(self.data_dir, str(self.season), str(self.game_id) + ".l." + str(self.league_id))
        query_result_data = self.yahoo_data.save(str(self.league_id) + "-league-teams",
                                                 self.yahoo_query.get_league_teams, new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load(str(self.league_id) + "-league-teams", new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    def test_get_league_players(self):
        """Retrieve valid players for chosen league.
        """
        new_data_dir = os.path.join(self.data_dir, str(self.season), str(self.game_id) + ".l." + str(self.league_id))
        query_result_data = self.yahoo_data.save(str(self.league_id) + "-league-players",
                                                 self.yahoo_query.get_league_players, new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load(str(self.league_id) + "-league-players", new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    def test_get_league_draft_results(self):
        """Retrieve draft results for chosen league.
        """
        new_data_dir = os.path.join(self.data_dir, str(self.season), str(self.game_id) + ".l." + str(self.league_id))
        query_result_data = self.yahoo_data.save(str(self.league_id) + "-league-draft_results",
                                                 self.yahoo_query.get_league_draft_results, new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load(str(self.league_id) + "-league-draft_results",
                                                  new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    def test_get_league_transactions(self):
        """Retrieve transactions for chosen league.
        """
        new_data_dir = os.path.join(self.data_dir, str(self.season), str(self.game_id) + ".l." + str(self.league_id))
        query_result_data = self.yahoo_data.save(str(self.league_id) + "-league-transactions",
                                                 self.yahoo_query.get_league_transactions, new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load(str(self.league_id) + "-league-transactions",
                                                  new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    def test_get_league_scoreboard_by_week(self):
        """Retrieve scoreboard for chosen league by week.
        """
        new_data_dir = os.path.join(self.data_dir, str(self.season), str(self.game_id) + ".l." + str(self.league_id),
                                    "week_" +
                                    str(self.chosen_week))
        query_result_data = self.yahoo_data.save("week_" + str(self.chosen_week) + "-scoreboard",
                                                 self.yahoo_query.get_league_scoreboard_by_week,
                                                 params={"chosen_week": self.chosen_week}, new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load("week_" + str(self.chosen_week) + "-scoreboard", Scoreboard,
                                                  new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    def test_get_league_matchups_by_week(self):
        """Retrieve matchups for chosen league by week.
        """
        new_data_dir = os.path.join(self.data_dir, str(self.season), str(self.game_id) + ".l." + str(self.league_id),
                                    "week_" +
                                    str(self.chosen_week))
        query_result_data = self.yahoo_data.save("week_" + str(self.chosen_week) + "-matchups",
                                                 self.yahoo_query.get_league_matchups_by_week,
                                                 params={"chosen_week": self.chosen_week}, new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load("week_" + str(self.chosen_week) + "-matchups",
                                                  new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ •
    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • SAVING AND LOADING SPECIFIC TEAM DATA ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ •
    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ •

    def test_get_team_info(self):
        """Retrieve info of specific team by team_id for chosen league.
        """
        new_data_dir = os.path.join(self.data_dir, str(self.season),
                                    str(self.game_id) + ".l." + str(self.league_id), "teams",
                                    str(self.team_id) + "-" + self.team_name)
        query_result_data = self.yahoo_data.save(str(self.team_id) + "-" + self.team_name + "-info",
                                                 self.yahoo_query.get_team_info,
                                                 params={"team_id": self.team_id}, new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load(str(self.team_id) + "-" + self.team_name + "-info", Team,
                                                  new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    def test_get_team_metadata(self):
        """Retrieve metadata of specific team by team_id for chosen league.
        """
        new_data_dir = os.path.join(self.data_dir, str(self.season),
                                    str(self.game_id) + ".l." + str(self.league_id), "teams",
                                    str(self.team_id) + "-" + self.team_name)
        query_result_data = self.yahoo_data.save(str(self.team_id) + "-" + self.team_name + "-metadata",
                                                 self.yahoo_query.get_team_metadata,
                                                 params={"team_id": self.team_id}, new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load(str(self.team_id) + "-" + self.team_name + "-metadata", Team,
                                                  new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    def test_get_team_stats(self):
        """Retrieve stats of specific team by team_id for chosen league.
        """
        new_data_dir = os.path.join(self.data_dir, str(self.season),
                                    str(self.game_id) + ".l." + str(self.league_id), "teams",
                                    str(self.team_id) + "-" + self.team_name)
        query_result_data = self.yahoo_data.save(str(self.team_id) + "-" + self.team_name + "-stats",
                                                 self.yahoo_query.get_team_stats,
                                                 params={"team_id": self.team_id}, new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load(str(self.team_id) + "-" + self.team_name + "-stats", TeamPoints,
                                                  new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    def test_get_team_stats_by_week(self):
        """Retrieve stats of specific team by team_id and by week for chosen league.
        """
        new_data_dir = os.path.join(self.data_dir, str(self.season),
                                    str(self.game_id) + ".l." + str(self.league_id), "week_" + str(self.chosen_week))
        query_result_data = self.yahoo_data.save(str(self.team_id) + "-" + self.team_name + "-stats",
                                                 self.yahoo_query.get_team_stats_by_week,
                                                 params={"team_id": self.team_id, "chosen_week": self.chosen_week},
                                                 new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load(str(self.team_id) + "-" + self.team_name + "-stats",
                                                  new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    def test_get_team_standings(self):
        """Retrieve standings of specific team by team_id for chosen league.
        """
        new_data_dir = os.path.join(self.data_dir, str(self.season),
                                    str(self.game_id) + ".l." + str(self.league_id), "teams",
                                    str(self.team_id) + "-" + self.team_name)
        query_result_data = self.yahoo_data.save(str(self.team_id) + "-" + self.team_name + "-standings",
                                                 self.yahoo_query.get_team_standings,
                                                 params={"team_id": self.team_id}, new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load(str(self.team_id) + "-" + self.team_name + "-standings",
                                                  TeamStandings, new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()
        self.assertEqual(query_result_data, loaded_result_data)

    def test_get_team_roster_by_week(self):
        """Retrieve roster of specific team by team_id and by week for chosen league.
        """
        new_data_dir = os.path.join(self.data_dir, str(self.season),
                                    str(self.game_id) + ".l." + str(self.league_id), "week_" + str(self.chosen_week),
                                    "rosters")
        query_result_data = self.yahoo_data.save(str(self.team_id) + "-" + self.team_name + "-roster_by_week",
                                                 self.yahoo_query.get_team_roster_by_week,
                                                 params={"team_id": self.team_id, "chosen_week": self.chosen_week},
                                                 new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load(str(self.team_id) + "-" + self.team_name + "-roster_by_week", Roster,
                                                  new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    def test_get_team_roster_player_info_by_week(self):
        """Retrieve roster with player info of specific team by team_id and by week for chosen league.
        """
        new_data_dir = os.path.join(self.data_dir, str(self.season),
                                    str(self.game_id) + ".l." + str(self.league_id), "week_" + str(self.chosen_week),
                                    "rosters")
        query_result_data = self.yahoo_data.save(str(self.team_id) + "-" + self.team_name +
                                                 "-roster-player_info_by_week",
                                                 self.yahoo_query.get_team_roster_player_info_by_week,
                                                 params={"team_id": self.team_id, "chosen_week": self.chosen_week},
                                                 new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load(str(self.team_id) + "-" + self.team_name +
                                                  "-roster-player_info_by_week",
                                                  new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    @skip  # skip because this is only for NHL/NBA/MLB, not NFL
    def test_get_team_roster_player_info_by_date(self):
        """Retrieve roster with player info of specific team by team_id and by date for chosen league.
        """
        new_data_dir = os.path.join(self.data_dir, str(self.season),
                                    str(self.game_id) + ".l." + str(self.league_id), str(self.chosen_date),
                                    "rosters")
        query_result_data = self.yahoo_data.save(str(self.team_id) + "-" + self.team_name +
                                                 "-roster-player_info_by_date",
                                                 self.yahoo_query.get_team_roster_player_info_by_date,
                                                 params={"team_id": self.team_id, "chosen_date": self.chosen_date},
                                                 new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load(str(self.team_id) + "-" + self.team_name +
                                                  "-roster-player_info_by_date",
                                                  new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    def test_get_team_roster_player_stats(self):
        """Retrieve roster with player info for season of specific team by team_id for chosen league.
        """
        new_data_dir = os.path.join(self.data_dir, str(self.season),
                                    str(self.game_id) + ".l." + str(self.league_id), "rosters")
        query_result_data = self.yahoo_data.save(str(self.team_id) + "-" + self.team_name + "-roster-player_stats",
                                                 self.yahoo_query.get_team_roster_player_stats,
                                                 params={"team_id": self.team_id},
                                                 new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load(str(self.team_id) + "-" + self.team_name + "-roster-player_stats",
                                                  new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    def test_get_team_roster_player_stats_by_week(self):
        """Retrieve roster with player stats of specific team by team_id and by week for chosen league.
        """
        new_data_dir = os.path.join(self.data_dir, str(self.season),
                                    str(self.game_id) + ".l." + str(self.league_id), "week_" + str(self.chosen_week),
                                    "rosters")
        query_result_data = self.yahoo_data.save(str(self.team_id) + "-" + self.team_name +
                                                 "-roster-player_stats_by_week",
                                                 self.yahoo_query.get_team_roster_player_stats_by_week,
                                                 params={"team_id": self.team_id, "chosen_week": self.chosen_week},
                                                 new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load(str(self.team_id) + "-" + self.team_name +
                                                  "-roster-player_stats_by_week",
                                                  new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    def test_get_team_draft_results(self):
        """Retrieve draft results of specific team by team_id for chosen league.
        """
        new_data_dir = os.path.join(self.data_dir, str(self.season),
                                    str(self.game_id) + ".l." + str(self.league_id), "teams",
                                    str(self.team_id) + "-" + self.team_name)
        query_result_data = self.yahoo_data.save(str(self.team_id) + "-" + self.team_name + "-draft_results",
                                                 self.yahoo_query.get_team_draft_results,
                                                 params={"team_id": self.team_id}, new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load(str(self.team_id) + "-" + self.team_name + "-draft_results",
                                                  new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    def test_get_team_matchups(self):
        """Retrieve matchups of specific team by team_id for chosen league.
        """
        new_data_dir = os.path.join(self.data_dir, str(self.season),
                                    str(self.game_id) + ".l." + str(self.league_id), "teams",
                                    str(self.team_id) + "-" + self.team_name)
        query_result_data = self.yahoo_data.save(str(self.team_id) + "-" + self.team_name + "-matchups",
                                                 self.yahoo_query.get_team_matchups,
                                                 params={"team_id": self.team_id}, new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load(str(self.team_id) + "-" + self.team_name + "-matchups",
                                                  new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ •
    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • SAVING AND LOADING SPECIFIC PLAYER DATA • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ •
    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ •

    def test_get_player_stats_for_season(self):
        """Retrieve stats of specific player by player_key for season for chosen league.
        """
        new_data_dir = os.path.join(self.data_dir, str(self.season), str(self.game_id) + ".l." + str(self.league_id),
                                    "players")
        query_result_data = self.yahoo_data.save(str(self.player_id) + "-player-season-stats",
                                                 self.yahoo_query.get_player_stats_for_season,
                                                 params={"player_key": str(self.player_key)},
                                                 new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load(str(self.player_id) + "-player-season-stats", Player,
                                                  new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    def test_get_player_stats_by_week(self):
        """Retrieve stats of specific player by player_key and by week for chosen league.
        """
        new_data_dir = os.path.join(self.data_dir, str(self.season), str(self.game_id) + ".l." + str(self.league_id),
                                    "week_" +
                                    str(self.chosen_week), "players")
        query_result_data = self.yahoo_data.save(str(self.player_id) + "-player-stats",
                                                 self.yahoo_query.get_player_stats_by_week,
                                                 params={"player_key": str(self.player_key),
                                                         "chosen_week": str(self.chosen_week)},
                                                 new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load(str(self.player_id) + "-player-stats", Player,
                                                  new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    @skip  # skip because this is only for NHL/NBA/MLB, not NFL
    def test_get_player_stats_by_date(self):
        """Retrieve stats of specific player by player_key and by date for chosen league.
        """
        new_data_dir = os.path.join(self.data_dir, str(self.season), str(self.game_id) + ".l." + str(self.league_id),
                                    str(self.chosen_date), "players")
        query_result_data = self.yahoo_data.save(str(self.player_id) + "-player-stats",
                                                 self.yahoo_query.get_player_stats_by_date,
                                                 params={"player_key": str(self.player_key),
                                                         "chosen_date": self.chosen_date},
                                                 new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load(str(self.player_id) + "-player-stats", Player,
                                                  new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    def test_get_player_ownership(self):
        """Retrieve ownership of specific player by player_key for chosen league.
        """
        new_data_dir = os.path.join(self.data_dir, str(self.season), str(self.game_id) + ".l." + str(self.league_id),
                                    "players")
        query_result_data = self.yahoo_data.save(str(self.player_id) + "-player-ownership",
                                                 self.yahoo_query.get_player_ownership,
                                                 params={"player_key": str(self.player_key)},
                                                 new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load(str(self.player_id) + "-player-ownership", Player,
                                                  new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    def test_get_player_percent_owned_by_week(self):
        """Retrieve percent-owned of specific player by player_key and by week for chosen league.
        """
        new_data_dir = os.path.join(self.data_dir, str(self.season), str(self.game_id) + ".l." + str(self.league_id),
                                    "week_" +
                                    str(self.chosen_week), "players")
        query_result_data = self.yahoo_data.save(str(self.player_id) + "-player-percent_owned",
                                                 self.yahoo_query.get_player_percent_owned_by_week,
                                                 params={"player_key": str(self.player_key),
                                                         "chosen_week": str(self.chosen_week)},
                                                 new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load(str(self.player_id) + "-player-percent_owned", Player,
                                                  new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)

    def test_get_player_draft_analysis(self):
        """Retrieve draft analysis of specific player by player_key for chosen league.
        """
        new_data_dir = os.path.join(self.data_dir, str(self.season), str(self.game_id) + ".l." + str(self.league_id),
                                    "players")
        query_result_data = self.yahoo_data.save(str(self.player_id) + "-player-draft_analysis",
                                                 self.yahoo_query.get_player_draft_analysis,
                                                 params={"player_key": str(self.player_key)},
                                                 new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(query_result_data)
            print("-" * 100)
            print()

        loaded_result_data = self.yahoo_data.load(str(self.player_id) + "-player-draft_analysis", Player,
                                                  new_data_dir=new_data_dir)
        if self.print_output:
            pprint.pprint(loaded_result_data)
            print("-" * 100)
            print()

        self.assertEqual(query_result_data, loaded_result_data)


if __name__ == '__main__':
    # Run all test with highest verbosity (options: 0, 1, 2)
    unittest.main(verbosity=2)
