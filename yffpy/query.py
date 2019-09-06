import os

from yahoo_oauth import OAuth2

from yffpy.models import *
from yffpy.utils import reformat_json_list, unpack_data

logger = logging.getLogger(__name__)
logging.getLogger("yahoo_oauth").setLevel(level=logging.INFO)


class YahooFantasyFootballQuery(object):

    def __init__(self, auth_dir, league_id, game_id=None, offline=False):

        self.league_id = league_id
        self.game_id = game_id
        self.league_key = None
        self.league_name = None

        if not offline:
            with open(os.path.join(auth_dir, "private.json")) as yahoo_app_credentials:
                auth_info = json.load(yahoo_app_credentials)
            self._yahoo_consumer_key = auth_info["consumer_key"]
            self._yahoo_consumer_secret = auth_info["consumer_secret"]

            token_file_path = os.path.join(auth_dir, "token.json")
            if os.path.isfile(token_file_path):
                with open(token_file_path) as yahoo_oauth_token:
                    auth_info = json.load(yahoo_oauth_token)
            else:
                with open(token_file_path, "w") as yahoo_oauth_token:
                    json.dump(auth_info, yahoo_oauth_token)

            if "access_token" in auth_info.keys():
                self._yahoo_access_token = auth_info["access_token"]

            self.oauth = OAuth2(None, None, from_file=token_file_path)
            if not self.oauth.token_is_valid():
                self.oauth.refresh_access_token()

    def query(self, url, data_key_list, data_type_class=None, run=True):

        if run:
            response = self.oauth.session.get(url, params={"format": "json"})
            logger.debug("RESPONSE (RAW JSON): {}".format(response.json()))
            raw_response_data = response.json().get("fantasy_content")
            logger.debug("RESPONSE (Yahoo fantasy football data extracted from: \"fantasy_content\"): {}".format(
                raw_response_data))

            for i in range(len(data_key_list)):
                if type(raw_response_data) == list:
                    raw_response_data = reformat_json_list(raw_response_data)[data_key_list[i]]
                else:
                    raw_response_data = raw_response_data.get(data_key_list[i])
            logger.debug("RESPONSE (Yahoo fantasy football data extracted from: {}): {}".format(data_key_list,
                                                                                                raw_response_data))

            unpacked = unpack_data(raw_response_data, YahooFantasyObject)
            clean_response_data = data_type_class(unpacked) if data_type_class else unpacked
            logger.debug(
                "UNPACKED AND PARSED JSON (Yahoo fantasy football data wth parent type: {}): {}".format(data_type_class,
                                                                                                        unpacked))

            return {
                "data": clean_response_data,
                "url": url,
                "raw": raw_response_data
            }
        else:
            return {
                "data": None,
                "url": url,
                "raw": None
            }

    def get_current_nfl_fantasy_game(self, run=True):
        return self.query("https://fantasysports.yahooapis.com/fantasy/v2/game/nfl", ["game"], Game, run=run)

    def get_nfl_fantasy_game(self, game_id, run=True):
        return self.query("https://fantasysports.yahooapis.com/fantasy/v2/game/" + str(game_id), ["game"], Game,
                          run=run)

    def get_league_key(self):
        if self.game_id:
            return self.get_nfl_fantasy_game(self.game_id).get("data").game_key + ".l." + self.league_id
        else:
            logger.warning(
                "No Yahoo Fantasy game id provided, defaulting to current NFL fantasy football season game id.")
            return self.get_current_nfl_fantasy_game().get("data").game_key + ".l." + self.league_id

    def get_user_game_history(self, run=True):
        return self.query("https://fantasysports.yahooapis.com/fantasy/v2/users;use_login=1/games;codes=nfl/",
                          ["users", "0", "user"], User, run=run)

    def get_user_league_history(self, run=True):
        return self.query("https://fantasysports.yahooapis.com/fantasy/v2/users;use_login=1/games;codes=nfl/leagues/",
                          ["users", "0", "user"], User, run=run)

    def get_overview(self, run=True):
        return self.query("https://fantasysports.yahooapis.com/fantasy/v2/league/" + self.league_key + "/", ["league"],
                          League, run=run)

    def get_standings(self, run=True):
        return self.query("https://fantasysports.yahooapis.com/fantasy/v2/league/" + self.league_key + "/standings",
                          ["league", "standings"], Standings, run=run)

    def get_settings(self, run=True):
        return self.query("https://fantasysports.yahooapis.com/fantasy/v2/league/" + self.league_key + "/settings",
                          ["league", "settings"], Settings, run=run)

    def get_teams(self, run=True):
        return self.query("https://fantasysports.yahooapis.com/fantasy/v2/league/" + self.league_key + "/teams",
                          ["league", "teams"], run=run)

    def get_matchups(self, chosen_week, run=True):
        return self.query(
            "https://fantasysports.yahooapis.com/fantasy/v2/league/" + self.league_key + "/scoreboard;week=" + str(
                chosen_week), ["league", "scoreboard", "0", "matchups"], run=run)

    def get_team_roster(self, team_id, chosen_week, run=True):
        team_key = self.league_key + ".t." + str(team_id)
        return self.query(
            "https://fantasysports.yahooapis.com/fantasy/v2/team/" + str(team_key) + "/roster;week=" + str(
                chosen_week) + "/players/stats", ["team", "roster", "0", "players"], run=run)

    def get_player_stats(self, player_key, chosen_week, run=True):
        return self.query(
            "https://fantasysports.yahooapis.com/fantasy/v2/league/" + self.league_key + "/players;player_keys=" + player_key + "/stats;type=week;week=" + str(
                chosen_week), ["league", "players", "0", "player"], Player, run=run)
