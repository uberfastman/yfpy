
import os
import sys
from pathlib import Path
import logging
logging.disable(logging.CRITICAL)
import pandas as pd
from unidecode import unidecode

from dotenv import load_dotenv

project_dir = Path(__file__).parent.parent
sys.path.insert(0, str(project_dir))

from yfpy.data import Data
from yfpy.query import YahooFantasySportsQuery



######ENVIRONMENT SETUP######

# load .env file in order to read local environment variables
load_dotenv(dotenv_path=project_dir / "auth" / ".env")
# set directory location of private.json for authentication
auth_dir = project_dir / "auth"
# set target directory for data output
data_dir = Path(__file__).parent.parent / "data"
# create YFPY Data instance for saving/loading data
data = Data(data_dir)

# %5
######VARIABLE SETUP######

# set desired Yahoo Fantasy Sports game code
def get_game_code():
    game_code = "mlb"  # MLB

    return game_code


game_code = get_game_code()


# set desired Yahoo Fantasy Sports game ID (see the get_all_yahoo_fantasy_game_keys query to retrieve values)
def get_game_id():
    game_id = 431  # MLB - 2024

    return game_id


game_id = get_game_id()


def get_league_id():
    league_id = "6636"  # MLB - 2024


    return league_id


league_id = get_league_id()


# set desired team ID within desired league
def get_team_id():
    team_id = 4  # MLB (2024)

    return team_id


team_id = get_team_id()


# set desired team name within desired league
def get_team_name():
    # BASEBALL
    team_name = "Air Yordan"  # MLB (202)4
    
    return team_name


team_name = get_team_name()


# set the maximum number players you wish the get_league_players query to retrieve
def get_league_player_limit():
    league_player_limit = 200

    return league_player_limit


league_player_limit = get_league_player_limit()

######QUERY SETUP######

def get_yahoo_driver():
    # configure the Yahoo Fantasy Sports query (change all_output_as_json_str=True if you want to output JSON strings)
    driver = YahooFantasySportsQuery(
        auth_dir,
        league_id,
        game_code,
        game_id=game_id,
        offline=False,
        all_output_as_json_str=False,
        consumer_key=os.environ["YFPY_CONSUMER_KEY"],
        consumer_secret=os.environ["YFPY_CONSUMER_SECRET"]
    )

    return driver


def get_available_hitters(driver):
    for _ in range(2):  # Try twice
        try:
            available_hitters = driver.get_all_available_players_by_pos(player_count_limit=1000, position='Util')
            break
        except Exception as e:
            print(f"An error occurred: {e}. Retrying...")
            
    hitters = []
    for player in available_hitters:
        if isinstance(player, dict):
            hitters.append([player["player"].full_name, player["player"].player_key])
        else:
            hitters.append([player.full_name, player.player_key])

    hitters = [[unidecode(player[0]).replace('.',''), player[1]] for player in hitters]
    
    return hitters


def get_available_sp(driver):
    for _ in range(2):  # Try twice
        try:
            available_sp = driver.get_all_available_players_by_pos(player_count_limit=1000, position='SP')
            break
        except Exception as e:
            print(f"An error occurred: {e}. Retrying...")
            
    sp = []
    for player in available_sp:
        if isinstance(player, dict):
            sp.append([player["player"].full_name, player["player"].player_key])
        else:
            sp.append([player.full_name, player.player_key])

    sp = [[unidecode(player[0]).replace('.',''), player[1]] for player in sp]
    
    return sp


def get_available_rp(driver):
    for _ in range(2):  # Try twice
        try:
            available_rp = driver.get_all_available_players_by_pos(player_count_limit=1000, position='RP')
            break
        except Exception as e:
            print(f"An error occurred: {e}. Retrying...")
            
    rp = []
    for player in available_rp:
        if isinstance(player, dict):
            rp.append([player["player"].full_name, player["player"].player_key])
        else:
            rp.append([player.full_name, player.player_key])

    rp = [[unidecode(player[0]).replace('.',''), player[1]] for player in rp]
    
    return rp


def get_my_hitters(driver):
    for _ in range(2):  # Try twice
        try:
            my_hitters = driver.get_team_roster_by_week(4)
            break
        except Exception as e:
            print(f"An error occurred: {e}. Retrying...")
            
    hitters = []
    for player in my_hitters.players:
        if player.position_type == 'B':
            hitters.append([player.full_name, player.player_key])

    hitters = [[unidecode(player[0]).replace('.',''), player[1]] for player in hitters]
    
    return hitters


def get_my_SP(driver):
    for _ in range(2):  # Try twice
        try:
            my_sp = driver.get_team_roster_by_week(4)
            break
        except Exception as e:
            print(f"An error occurred: {e}. Retrying...")
            
    sp = []
    for player in my_sp.players:
        if player.primary_position == 'SP':
            sp.append([player.full_name, player.player_key])

    sp = [[unidecode(player[0]).replace('.',''), player[1]] for player in sp]
    
    return sp


def get_my_RP(driver):
    for _ in range(2):  # Try twice
        try:
            my_rp = driver.get_team_roster_by_week(4)
            break
        except Exception as e:
            print(f"An error occurred: {e}. Retrying...")
            
    rp = []
    for player in my_rp.players:
        if player.primary_position == 'RP':
            rp.append([player.full_name, player.player_key])

    rp = [[unidecode(player[0]).replace('.',''), player[1]] for player in rp]
    
    return rp
