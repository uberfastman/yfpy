__author__ = "Wren J. R. (uberfastman)"
__email__ = "wrenjr@yahoo.com"

import logging
import os
import pprint

from yffpy import Data
from yffpy.models import Game, User, League, Standings, Settings, Player
from yffpy.query import YahooFantasyFootballQuery

if __name__ == "__main__":

    # Suppress YahooFantasyFootballQuery debug logging
    logging.getLogger("yffpy.query").setLevel(level=logging.INFO)

    # Turn on/off example code stdout printing output
    print_output = True

    # Put private.json (see README.md) in examples directory
    auth_dir = "."

    # Example code will output data here
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_output")

    # Example vars using a public Yahoo league (still requires auth through any personal Yahoo account - see README.md)
    game_id = "331"
    season = "2014"
    league_id = "729259"
    public_league_url = "https://archive.fantasysports.yahoo.com/nfl/2014/729259"

    # Instantiate yffpy objects
    yahoo_data = Data(data_dir)
    yahoo_query = YahooFantasyFootballQuery(auth_dir, league_id, game_id=game_id, offline=False)

    # Manuallu override league key for example code to work
    yahoo_query.league_key = game_id + ".l." + league_id

    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ •
    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ SAVING AND LOADING FANTASY FOOTBALL GAME DATA • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ •
    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ •

    result_data = yahoo_data.save("current_nfl_fantasy_game", yahoo_query.get_current_nfl_fantasy_game)
    if print_output:
        pprint.pprint(result_data)
        print("-" * 100)
        print()

    result_data = yahoo_data.load("current_nfl_fantasy_game", Game)
    if print_output:
        pprint.pprint(result_data)
        print("-" * 100)
        print()

    new_data_dir = os.path.join(data_dir, str(season))
    result_data = yahoo_data.save(str(game_id) + "-nfl_fantasy_game", yahoo_query.get_nfl_fantasy_game,
                                  params={"game_id": game_id}, new_data_dir=new_data_dir)
    if print_output:
        pprint.pprint(result_data)
        print("-" * 100)
        print()

    result_data = yahoo_data.load(str(game_id) + "-nfl_fantasy_game", Game, new_data_dir=new_data_dir)
    if print_output:
        pprint.pprint(result_data)
        print("-" * 100)
        print()

    result_data = yahoo_query.get_league_key()
    if print_output:
        pprint.pprint(result_data)
        print("-" * 100)
        print()

    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~
    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ SAVING AND LOADING USER HISTORICAL DATA • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~
    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~

    new_data_dir = data_dir
    result_data = yahoo_data.save("user_game_history", yahoo_query.get_user_game_history, new_data_dir=new_data_dir)
    if print_output:
        pprint.pprint(result_data)
        print("-" * 100)
        print()

    result_data = yahoo_data.load("user_game_history", User, new_data_dir=new_data_dir)
    if print_output:
        pprint.pprint(result_data)
        print("-" * 100)
        print()

    result_data = yahoo_data.save("user_league_history", yahoo_query.get_user_league_history, new_data_dir=new_data_dir)
    if print_output:
        pprint.pprint(result_data)
        print("-" * 100)
        print()

    result_data = yahoo_data.load("user_league_history", User, new_data_dir=new_data_dir)
    if print_output:
        pprint.pprint(result_data)
        print("-" * 100)
        print()

    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~
    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ SAVING AND LOADING FANTASY FOOTBALL LEAGUE DATA • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~
    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~

    new_data_dir = os.path.join(data_dir, str(season), str(game_id) + ".l." + str(league_id))
    result_data = yahoo_data.save("overview", yahoo_query.get_overview, new_data_dir=new_data_dir)
    if print_output:
        pprint.pprint(result_data)
        print("-" * 100)
        print()

    result_data = yahoo_data.load("overview", League, new_data_dir=new_data_dir)
    if print_output:
        pprint.pprint(result_data)
        print("-" * 100)
        print()

    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~
    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • SAVING AND LOADING FANTASY FOOTBALL LEAGUE STANDINGS DATA • ~ • ~ • ~ • ~ • ~ • ~ • ~
    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~

    new_data_dir = os.path.join(data_dir, str(season), str(game_id) + ".l." + str(league_id))
    result_data = yahoo_data.save("standings", yahoo_query.get_standings, new_data_dir=new_data_dir)
    if print_output:
        pprint.pprint(result_data)
        print("-" * 100)
        print()

    result_data = yahoo_data.load("standings", Standings, new_data_dir=new_data_dir)
    if print_output:
        pprint.pprint(result_data)
        print("-" * 100)
        print()

    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~
    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • SAVING AND LOADING LEAGUE SETTINGS DATA ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~
    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~

    new_data_dir = os.path.join(data_dir, str(season), str(game_id) + ".l." + str(league_id))
    result_data = yahoo_data.save("settings", yahoo_query.get_settings, new_data_dir=new_data_dir)
    if print_output:
        pprint.pprint(result_data)
        print("-" * 100)
        print()

    result_data = yahoo_data.load("settings", Settings, new_data_dir=new_data_dir)
    if print_output:
        pprint.pprint(result_data)
        print("-" * 100)
        print()

    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~
    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • SAVING AND LOADING FANTASY FOOTBALL LEAGUE TEAMS DATA • ~ • ~ • ~ • ~ • ~ • ~ • ~
    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~

    new_data_dir = os.path.join(data_dir, str(season), str(game_id) + ".l." + str(league_id))
    result_data = yahoo_data.save("teams", yahoo_query.get_teams, new_data_dir=new_data_dir)
    if print_output:
        pprint.pprint(result_data)
        print("-" * 100)
        print()

    result_data = yahoo_data.load("teams", new_data_dir=new_data_dir)
    if print_output:
        pprint.pprint(result_data)
        print("-" * 100)
        print()

    chosen_week = 1
    new_data_dir = os.path.join(data_dir, str(season), str(game_id) + ".l." + str(league_id), "week_" +
                                str(chosen_week))
    result_data = yahoo_data.save("matchups", yahoo_query.get_matchups, params={"chosen_week": chosen_week},
                                  new_data_dir=new_data_dir)
    if print_output:
        pprint.pprint(result_data)
        print("-" * 100)
        print()

    result_data = yahoo_data.load("matchups", new_data_dir=new_data_dir)
    if print_output:
        pprint.pprint(result_data)
        print("-" * 100)
        print()

    chosen_week = 1
    team_id = 1
    team_name = "Legion"
    new_data_dir = os.path.join(data_dir, str(season), str(game_id) + ".l." + str(league_id), "week_" +
                                str(chosen_week), "rosters")
    result_data = yahoo_data.save(str(team_id) + "_" + team_name, yahoo_query.get_team_roster,
                                  params={"team_id": team_id, "chosen_week": chosen_week}, new_data_dir=new_data_dir)
    if print_output:
        pprint.pprint(result_data)
        print("-" * 100)
        print()

    result_data = yahoo_data.load(str(team_id) + "_" + team_name, new_data_dir=new_data_dir)
    if print_output:
        pprint.pprint(result_data)
        print("-" * 100)
        print()

    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ •
    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • SAVING AND LOADING SPECIFIC PLAYER DATA • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ •
    # ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ • ~ •

    chosen_week = 1
    player_key = game_id + ".p.7200"
    new_data_dir = os.path.join(data_dir, str(season), str(game_id) + ".l." + str(league_id), "week_" +
                                str(chosen_week), "players")
    result_data = yahoo_data.save(str(player_key), yahoo_query.get_player_stats,
                                  params={"player_key": str(player_key), "chosen_week": str(chosen_week)},
                                  new_data_dir=new_data_dir)
    if print_output:
        pprint.pprint(result_data)
        print("-" * 100)
        print()

    result_data = yahoo_data.load(player_key, Player, new_data_dir=new_data_dir)
    if print_output:
        pprint.pprint(result_data)
        print("-" * 100)
        print()
