# %%
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
from pl_scraper import get_the_list
from eno_scraper import get_eno_rankings
from ss_scraper import get_ss_rankings
from razz_scraper import get_razzball_standard, get_razzball_qs

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# ENVIRONMENT SETUP # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# load .env file in order to read local environment variables
load_dotenv(dotenv_path=project_dir / "auth" / ".env")
# set directory location of private.json for authentication
auth_dir = project_dir / "auth"
# set target directory for data output
data_dir = Path(__file__).parent.parent / "data"
# create YFPY Data instance for saving/loading data
data = Data(data_dir)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# VARIABLE SETUP  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# #  Get game keys if needed
# print(repr(yahoo_query.get_all_yahoo_fantasy_game_keys()))

# set desired season year
def get_season():
    # season = 2023
    season = 2024
    return season


season = get_season()


# set desired week
def get_chosen_week():
    chosen_week = 1
    return chosen_week


chosen_week = get_chosen_week()


# set desired date
def get_chosen_date():
    # HOCKEY
    # chosen_date = "2013-04-15"  # NHL - 2013 (for 2012 season)
    chosen_date = "2021-10-25"  # NHL - 2021

    # BASEBALL
    # chosen_date = "2021-04-01"  # MLB - 2021
    # chosen_date = "2022-04-10"  # MLB - 2022

    return chosen_date


chosen_date = get_chosen_date()


# set desired Yahoo Fantasy Sports game code
def get_game_code():
    # FOOTBALL
    # game_code = "nfl"  # NFL

    # HOCKEY
    # game_code = "nhl"  # NHL

    # BASEBALL
    game_code = "mlb"  # MLB

    return game_code


game_code = get_game_code()


# set desired Yahoo Fantasy Sports game ID (see the get_all_yahoo_fantasy_game_keys query to retrieve values)
def get_game_id():
    # FOOTBALL
    # game_id = 423  # NFL - 2023

    # HOCKEY
    # game_id = 427  # NHL - 2023

    # BASEBALL
    # game_id = 422  # MLB - 2023
    game_id = 431  # MLB - 2024

    return game_id


game_id = get_game_id()


# set desired Yahoo Fantasy Sports game key (see the get_all_yahoo_fantasy_game_keys query to retrieve values)
def get_game_key():
    # FOOTBALL
    # game_key = "423"  # NFL - 2023

    # HOCKEY
    # game_key = "427"  # NHL - 2023

    # BASEBALL
    game_key = "422"  # MLB - 2023

    return game_key


game_key = get_game_key()


# set desired league ID (see README.md for finding value)
def get_league_id():
    # FOOTBALL
    # league_id = "321958"  # NFL - 2023

    # HOCKEY
    # league_id = "84997"  # NHL - 2023

    # BASEBALL
    # league_id = "3535"  # MLB - 2021
    # league_id = "22974"  # MLB - 2023
    league_id = "6636"  # MLB - 2024


    return league_id


league_id = get_league_id()


# set desired team ID within desired league
def get_team_id():
    # FOOTBALL
    # team_id = 1  # NFL

    # HOCKEY
    # team_id = 12  # NHL (2012)
    
    # BASEBALL
    team_id = 11  # MLB (2023)

    return team_id


team_id = get_team_id()


# set desired team name within desired league
def get_team_name():
    # FOOTBALL
    # team_name = "Legion"  # NFL

    # HOCKEY
    # team_name = "Pat's Primo Team"  # NHL (2012)

    # BASEBALL
    team_name = "No Way Jose"  # MLB (2023)
    
    return team_name


team_name = get_team_name()


# set desired team ID within desired league
def get_player_id():
    # FOOTBALL
    # player_id = 30123  # NFL: Patrick Mahomes - 2020/2021/2023

    # HOCKEY
    # player_id = 6777  # NHL: Sebastian Aho - 2023


    # BASEBALL
    player_id = 10883  # MLB: Yordan Alvarez - 2024

    return player_id


player_id = get_player_id()


# set the maximum number players you wish the get_league_players query to retrieve
def get_league_player_limit():
    league_player_limit = 200

    return league_player_limit


league_player_limit = get_league_player_limit()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# QUERY SETUP # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# configure the Yahoo Fantasy Sports query (change all_output_as_json_str=True if you want to output JSON strings)
yahoo_query = YahooFantasySportsQuery(
    auth_dir,
    league_id,
    game_code,
    game_id=game_id,
    offline=False,
    all_output_as_json_str=False,
    consumer_key=os.environ["YFPY_CONSUMER_KEY"],
    consumer_secret=os.environ["YFPY_CONSUMER_SECRET"]
)

yahoo_query.league_key = f"{game_id}.l.{league_id}"
player_key = f"{game_id}.p.{player_id}"

# %%
# Get all available players
available_hitters = yahoo_query.get_all_available_players_by_pos(player_count_limit=1000, position='Util')
# available_sp = yahoo_query.get_all_available_players_by_pos(player_count_limit=1000, position='SP')
# available_rp = yahoo_query.get_all_available_players_by_pos(player_count_limit=500, position='RP')


# %%
the_list = get_the_list("https://pitcherlist.com/top-100-starting-pitchers-for-2024-fantasy-baseball-3-11-update/")

# %%
eno_rankings = get_eno_rankings()

# %%
razz_rankings = get_razzball_standard()

# %%
razz_qs = get_razzball_qs()

# %%
ss_rankings = get_ss_rankings()
# %%
##############SCRATCH##############
# Manual query
league_player_count = 0
league_player_retrieval_limit = 25
is_retry = False
players = yahoo_query.query(
                    f"https://fantasysports.yahooapis.com/fantasy/v2/league/431.l.6636/players;start=0;count=25status=A;position=2B;"
                    f"start={league_player_count};count={league_player_retrieval_limit if not is_retry else 1}",
                    ["league", "players"]
                )



# %%
available = dict()
for player in available_sp:
    if player.full_name in the_list.keys():
        available[the_list[player.full_name]] = player.full_name
# %%
sorted_list = sorted(available.items())
sorted_list

# %%
pitchers = []
for player in available_sp:
    pitchers.append(player.full_name)
    
    
# %%
hitters = []
for player in available_hitters:
    # print(type(available_hitters[i]))
    if isinstance(player, dict):
        hitters.append(player["player"].full_name)
    else:
        hitters.append(player.full_name)

hitters = [unidecode(string) for string in hitters]
# %%
razz_rankings = {i: v for i, (_, v) in enumerate(razz_rankings.items(), start=1)}

# %%
df = pd.DataFrame(pitchers, columns=['Player Name'])

# %%
# %%
df['PL'] = df['Player Name'].map(the_list)
df['SS'] = df['Player Name'].map(ss_rankings)
df['Eno'] = df['Player Name'].map(eno_rankings)
df['Razz_QS'] = df['Player Name'].map(razz_qs)
# df['Razz_QS'] = df['Player Name'].map(dict5)
# %%
df[['PL', 'SS', 'Eno', 'Razz_QS']] = df[['PL', 'SS', 'Eno', 'Razz_QS']].apply(pd.to_numeric, errors='coerce')
df['Average'] = df[['PL', 'SS', 'Eno', 'Razz_QS']].mean(axis=1)
# %%
df = df.sort_values('Average', ascending=True)
# %%
df.to_csv(r'C:\Users\patri\OneDrive\Fantasy_Baseball\2024\my_yfpy\data\pitcherlist\hitters.csv', index=False)
# %%
razz_bats = get_razzball_standard()
# %%
razz_OPS = pd.read_csv(r"C:\Users\patri\OneDrive\Fantasy_Baseball\2024\razz_OBP_SLG.csv", nrows=200)
hitterlist = pd.read_csv(r"C:\Users\patri\OneDrive\Fantasy_Baseball\2024\hitterlist.csv")
my_ranks = pd.read_csv(r"C:\Users\patri\OneDrive\Fantasy_Baseball\2024\my_ranks.csv")

# %%
df = pd.DataFrame(hitters, columns=['Player Name'])

# %%
df = df.merge(razz_OPS[['#', 'Name']], left_on='Player Name',right_on = 'Name',  how='left').rename(columns={'#': 'Razz_OPS'}).drop('Name', axis=1)
df = df.merge(hitterlist[['#', 'Name']], left_on='Player Name',right_on = 'Name',  how='left').rename(columns={'#': 'hitterlist'}).drop('Name', axis=1)
df = df.merge(my_ranks[['#', 'Name']], left_on='Player Name',right_on = 'Name',  how='left').rename(columns={'#': 'my_ranks'}).drop('Name', axis=1)

# %%
df['Razz'] = df['Player Name'].map(razz_bats)

# %%
df[['Razz_OPS', 'hitterlist', 'my_ranks', 'Razz']] = df[['Razz_OPS', 'hitterlist', 'my_ranks', 'Razz']].apply(pd.to_numeric, errors='coerce')

# %%
df['Average'] = df[['Razz_OPS', 'hitterlist', 'my_ranks', 'Razz']].mean(axis=1)

# %%
df = df.dropna(subset=['Average'])
# %%
if 'Max Muncy' in hitters:
    print('String found')
else:
    print('String not found')
# %%
