from yfpy.data import Data
from yfpy.query import YahooFantasySportsQuery

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



# #  Get game keys if needed
# print(repr(yahoo_query.get_all_yahoo_fantasy_game_keys()))