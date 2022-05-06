# -*- coding: utf-8 -*-
"""YFPY module containing Python object models representing all currently known Yahoo Fantasy Sports REST API data.

This module is built to abstract away the intricacies of parsing the complex and oftentimes messy data returned by the
Yahoo Fantasy Sports REST API, and instead provide the user with a collection of custom classes making it easy and
intuitive to access the data content.

Attributes:
    logger (Logger): Module level logger for usage and debugging.

"""
__author__ = "Wren J. R. (uberfastman)"
__email__ = "uberfastman@uberfastman.dev"

import json
from typing import Dict

import stringcase

from yfpy.logger import get_logger
from yfpy.utils import complex_json_handler

# from yfpy.utils import flatten_to_objects

logger = get_logger(__name__)


class YahooFantasyObject(object):
    """Base Yahoo Fantasy Sports data object from which all model classes inherit their methods and attributes.
    """

    def __init__(self, extracted_data: Dict):
        """Instantiate a Yahoo Fantasy Object.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        """
        self.extracted_data = extracted_data
        self._index = 0
        if isinstance(extracted_data, dict):
            self._keys = list(self.extracted_data.keys())

    def __str__(self):
        return self.to_json()

    def __repr__(self):
        return self.to_json()

    # def __getattribute__(self, item):
    #     return flatten_to_objects(item)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._equality_field_dict() == other._equality_field_dict()

    def __len__(self):
        return len(self.extracted_data)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            if isinstance(self.extracted_data, dict):
                result = self.extracted_data.get(self._keys[self._index])
            else:
                result = self.extracted_data[self._index]
        except IndexError:
            raise StopIteration
        self._index += 1
        return result

    def __reversed__(self):
        return reversed(self._keys)

    def _equality_field_dict(self) -> Dict:
        return {k: v for k, v in self.__dict__.items() if k not in ["extracted_data", "_index", "_keys"]}

    def subclass_dict(self) -> Dict:
        """Derive snake case dictionary keys from custom object type camel case class names.

        Returns:
            dict: Dictionary with snake case strings of all subclasses of YahooFantasyObject as keys and subclasses as
            values.

        """
        return {stringcase.snakecase(cls.__name__): cls for cls in self.__class__.__mro__[-2].__subclasses__()}

    def clean_data_dict(self) -> Dict:
        """Recursive method to un-type custom class type objects for serialization.

        Returns:
            dict: Dictionary that extracts serializable data from custom objects.

        """
        clean_dict = {}
        for k, v in self.__dict__.items():
            if k in self._keys:
                clean_dict[k] = v.clean_data_dict() if type(v) in self.subclass_dict().values() else v
        return clean_dict

    def serialized(self) -> Dict:
        """Pack up all object content into nested dictionaries for JSON serialization.

        Returns:
            dict: Serializable dictionary.

        """
        serializable_dict = dict()
        for a, v in self.clean_data_dict().items():
            if hasattr(v, "serialized"):
                serializable_dict[a] = v.serialized()
            else:
                serializable_dict[a] = v
        return serializable_dict

    def to_json(self) -> str:
        """Serialize the class object to JSON.

        Returns:
            str: JSON string derived from the serializable version of the class object.

        """
        return json.dumps(self.serialized(), indent=2, default=complex_json_handler, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_data: Dict):
        """Deserialize JSON to a class object.

        Returns:
            object: Class object derived from JSON data.

        """
        return cls(json_data)


# noinspection DuplicatedCode, PyUnresolvedReferences
class User(YahooFantasyObject):
    """Model class for "user" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the User child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            games (list[Game]): The Yahoo Fantasy games in which the user participates/has participated.
            guid (str): The Yahoo user ID.

        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.games = self.extracted_data.get("games", [])
        self.guid = self.extracted_data.get("guid", "")


# noinspection PyUnresolvedReferences
class Game(YahooFantasyObject):
    """Model class for "game" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the Game child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            code (str): The Yahoo Fantasy game code.
            game_id (int): The Yahoo Fantasy game ID.
            game_key (str): The Yahoo Fantasy game key.
            game_weeks (list[GameWeek]): A list of YFPY GameWeek instances.
            is_game_over (int): Numeric boolean (0 or 1) representing if the Yahoo Fantasy game is complete.
            is_live_draft_lobby_active (int): Numeric boolean (0 or 1) representing if the draft lobby is active.
            is_offseason (int): Numeric boolean (0 or 1) representing if it is the offseason for the respective sport.
            is_registration_over (int): Numeric boolean (0 or 1) representing registration for the fantasy game is over.
            leagues (list[League]): A list of YFPY League instances.
            name (str): The name of the Yahoo Fantasy game.
            position_types (list[PositionType]): A list of YFPY PositionType instances.
            roster_positions (list[RosterPosition]): A list of YFPY RosterPosition instances.
            season (int): The Yahoo Fantasy game year.
            stat_categories (StatCategories): A YFPY StatCategories instance.
            teams (list[Team]): A list of YFPY Team instances.
            type (str): The type of the Yahoo Fantasy game.
            url (str): The direct URL of the Yahoo Fantasy game.

        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.code = self.extracted_data.get("code", "")
        self.game_id = self.extracted_data.get("game_id", 0)
        self.game_key = str(self.extracted_data.get("game_key", ""))
        self.game_weeks = self.extracted_data.get("game_weeks", [])
        self.is_game_over = self.extracted_data.get("is_game_over", 0)
        self.is_live_draft_lobby_active = self.extracted_data.get("is_live_draft_lobby_active", 0)
        self.is_offseason = self.extracted_data.get("is_offseason", 0)
        self.is_registration_over = self.extracted_data.get("is_registration_over", 0)
        self.leagues = self.extracted_data.get("leagues", [])
        self.name = self.extracted_data.get("name", "")
        self.position_types = self.extracted_data.get("position_types", [])
        self.roster_positions = self.extracted_data.get("roster_positions", [])
        self.season = self.extracted_data.get("season", 0)
        self.stat_categories = self.extracted_data.get("stat_categories", StatCategories({}))  # type: StatCategories
        self.teams = self.extracted_data.get("teams", [])
        self.type = self.extracted_data.get("type", "")
        self.url = self.extracted_data.get("url", "")


# noinspection PyUnresolvedReferences
class GameWeek(YahooFantasyObject):
    """Model class for "game_week" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the GameWeek child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            display_name (str): The display name of the Yahoo Fantasy game week.
            end (str): The end date of the Yahoo Fantasy game week.
            start (str): The start date of the Yahoo Fantasy game week.
            week (int): The week number of the Yahoo Fantasy game week.

        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.display_name = self.extracted_data.get("display_name", "")
        self.end = self.extracted_data.get("end", "")
        self.start = self.extracted_data.get("start", "")
        self.week = self.extracted_data.get("week", 0)


# noinspection PyUnresolvedReferences
class PositionType(YahooFantasyObject):
    """Model class for "position_type" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the PositionType child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            type (str): The type of the player position ("offense", "defense", etc.).
            display_name (str): The full text display of the position type.

        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.type = self.extracted_data.get("type", "")
        self.display_name = self.extracted_data.get("display_name", "")


# noinspection PyUnresolvedReferences
class League(YahooFantasyObject):
    """Model class for "league" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the League child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            allow_add_to_dl_extra_pos (int): Numeric boolean (0 or 1) representing if the leagues allows adding extra
                positions to the DL (currently uncertain what this is).
            current_week (int): The current week number.
            draft_results (list[DraftResult]): A list of YFPY DraftResult instances.
            draft_status (str): The status of the draft ("postdraft", etc.).
            display_name (str): The display name of the league.
            edit_key (int): The Yahoo edit key for the league.
            end_date (str): A date string representing the end date of the league (format: "YYYY-MM-DD").
            end_week (int): The number of the last week of the league.
            entry_fee (str): The entry fee for Yahoo paid leagues (USD).
            game_code (str): The Yahoo game code ("nfl", "nhl", "nba", "mlb").
            iris_group_chat_id (str | null): The unique IRIS group chat ID for the league.
            is_cash_league (int): Numeric boolean (0 or 1) representing if the league is a Yahoo paid league.
            is_finished (int): Numeric boolean (0 or 1) representing if the league season has completed.
            is_pro_league (str): Numeric boolean (0 or 1) representing if the league is a Yahoo Pro league.
            league_id (str): The unique Yahoo league ID.
            league_key (str): The Yahoo league key.
            league_type (str): The type of the league ("private", "public").
            league_update_timestamp (int): A timestamp representing the last time the league was updated.
            logo_url (str): The direct URL of the league logo photo.
            name (str): The name of the league.
            num_teams (str): The number of teams in the league.
            password (str | null): The password required to join the league (if applicable).
            payment_deadline (str): A date string representing the deadline by which all league dues payments must be
                made (format: "YYYY-MM-DD").
            players (list[Player]): A list of YFPY Player instances.
            renew (str | null): A string indicating the previous Yahoo game code and previous Yahoo league ID (Ex.:
                "371_811308") (if applicable).
            renewed (str | null): A string indicating the next Yahoo game code and next Yahoo league ID (Ex.:
                "390_303233") (if applicable).
            scoreboard (Scoreboard): A YFPY Scoreboard instance.
            matchups (list[Matchup]): A list of YFPY Matchup instances.
            scoring_type (str): The scoring type of the league ("head" for head-to-head, etc.).
            season (int): The season year of the league.
            settings (Settings): A YFPY Settings instance.
            short_invitation_url (str): The sharable short URL sent by invite allowing players to join the league.
            standings (Standings): A YFPY Standings instance.
            teams_ordered_by_standings (list[Team]): A list of YFPY Team instances ordered by their ranks in the league
                standings.
            start_date (str): A date string representing the start date of the league (format: "YYYY-MM-DD").
            start_week (int): The number of the first week of the league.
            transactions (list[Transaction]): A list of YFPY Transaction instances.
            url (str): The direct URL of the league.
            weekly_deadline (str | null): The weekly deadline of the league (if applicable).

        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.allow_add_to_dl_extra_pos = self.extracted_data.get("allow_add_to_dl_extra_pos", "")
        self.current_week = self.extracted_data.get("current_week", "")
        self.draft_results = self.extracted_data.get("draft_results", "")
        self.draft_status = self.extracted_data.get("draft_status", "")
        self.edit_key = self.extracted_data.get("edit_key", "")
        self.end_date = self.extracted_data.get("end_date", "")
        self.end_week = self.extracted_data.get("end_week", "")
        self.entry_fee = self.extracted_data.get("entry_fee", "")
        self.game_code = self.extracted_data.get("game_code", "")
        self.iris_group_chat_id = self.extracted_data.get("iris_group_chat_id", "")
        self.is_cash_league = self.extracted_data.get("is_cash_league", "")
        self.is_finished = self.extracted_data.get("is_finished", "")
        self.is_pro_league = self.extracted_data.get("is_pro_league", "")
        self.league_id = str(self.extracted_data.get("league_id", ""))
        self.league_key = self.extracted_data.get("league_key", "")
        self.league_type = self.extracted_data.get("league_type", "")
        self.league_update_timestamp = self.extracted_data.get("league_update_timestamp", "")
        self.logo_url = self.extracted_data.get("logo_url", "")
        self.name = self.extracted_data.get("name", "")
        self.num_teams = self.extracted_data.get("num_teams", "")
        self.password = self.extracted_data.get("password", "")
        self.payment_deadline = self.extracted_data.get("payment_deadline", "")
        self.players = self.extracted_data.get("players", [])
        self.renew = self.extracted_data.get("renew", "")
        self.renewed = self.extracted_data.get("renewed", "")
        self.scoreboard = self.extracted_data.get("scoreboard", Scoreboard({}))  # type: Scoreboard
        self.matchups = self.scoreboard.matchups
        self.scoring_type = self.extracted_data.get("scoring_type", "")
        self.season = self.extracted_data.get("season", 0)
        self.settings = self.extracted_data.get("settings", Settings({}))  # type: Settings
        self.short_invitation_url = self.extracted_data.get("short_invitation_url", "")
        self.standings = self.extracted_data.get("standings", Standings({}))  # type: Standings
        self.teams_ordered_by_standings = self.standings.teams or []
        self.start_date = self.extracted_data.get("start_date", "")
        self.start_week = self.extracted_data.get("start_week", 0)
        self.transactions = self.extracted_data.get("transactions", [])
        self.url = self.extracted_data.get("url", "")
        self.weekly_deadline = self.extracted_data.get("weekly_deadline", "")


# noinspection PyUnresolvedReferences
class Team(YahooFantasyObject):
    """Model class for "team" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the Team child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            clinched_playoffs (int): Numeric boolean (0 or 1) representing if the team has clinched a playoff berth.
            division_id (str): The unique ID number of the division containing the team (if applicable).
            draft_grade (str): The letter grade assigned to the draft completed by the team ("A+", "A", ..., "F-").
            draft_position (int): The draft order/position of the team.
            draft_recap_url (str): The direct URL of the draft recap for the team.
            draft_results (list[DraftResult]): A list of YFPY DraftResult instances.
            faab_balance (int): The available balance of FAAB (Free Agent Acquisition Budget) (if applicable).
            has_draft_grade (int): Numeric boolean (0 or 1) representing if the team has a draft grade available.
            league_scoring_type (str): Value designating the type of scoring used by the league ("head" for
                head-to-head, etc.).
            managers (list[Manager] | dict[str, Manager]): A list or dict (depending on source data) of YFPY Manager
                instances.
            matchups (list[Matchup]): A list of YFPY Matchup instances.
            name (str): The team name.
            number_of_moves (int): The number of moves made by the team (adds/drops/trades/etc.).
            number_of_trades (int): The number of trades made by the team.
            roster (Roster): A YFPY Roster instance.
            players (list[Player]): A list of YFPY Player instances.
            roster_adds (RosterAdds): A YFPY RosterAdds instance.
            roster_adds_value (int): The number of roster adds made by the team.
            team_id (int): The unique team ID in the league.
            team_key (str): The Yahoo team key.
            team_logos (list[TeamLogo]): A list of YFPY TeamLogo instances.
            team_points (TeamPoints): A YFPY TeamPoints instance.
            points (float): The total points scored by the team.
            team_projected_points (TeamProjectedPoints): A YFPY TeamProjectedPoints instance.
            projected_points (float): The total projected points for the team.
            team_standings (TeamStandings): A YFPY TeamStandings instance.
            wins (int): The number of wins by the team.
            losses (int): The number of losses by the team.
            ties (int): The number of ties by the team.
            percentage (float): The win percentage of the team.
            playoff_seed (int): The playoff seed of the team.
            points_against (float): The total team points against.
            points_for (float): The total team points for.
            rank (int): The rank of the team in the league standings.
            streak_type (str): The active team win/loss/tie streak.
            streak_length (int): The length of the streak.
            url (str): The direct URL to the team.
            waiver_priority (int): The waiver priority of the team.
            win_probability (float): The active win probability of the team in its current matchup (ranges from 0.0 to
                1.0).

        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.clinched_playoffs = self.extracted_data.get("clinched_playoffs", 0)
        self.division_id = self.extracted_data.get("division_id")
        self.draft_grade = self.extracted_data.get("draft_grade", "")
        self.draft_position = self.extracted_data.get("draft_position", 0)
        self.draft_recap_url = self.extracted_data.get("draft_recap_url", "")
        self.draft_results = self.extracted_data.get("draft_results", [])
        self.faab_balance = self.extracted_data.get("faab_balance", 0)
        self.has_draft_grade = self.extracted_data.get("has_draft_grade", 0)
        self.league_scoring_type = self.extracted_data.get("league_scoring_type", "")
        self.managers = self.extracted_data.get("managers", {})
        self.matchups = self.extracted_data.get("matchups", [])
        self.name = self.extracted_data.get("name", "").encode("utf-8")
        self.number_of_moves = self.extracted_data.get("number_of_moves", 0)
        self.number_of_trades = self.extracted_data.get("number_of_trades", 0)
        self.roster = self.extracted_data.get("roster", Roster({}))  # type: Roster
        self.players = self.roster.players or []
        self.roster_adds = self.extracted_data.get("roster_adds", RosterAdds({}))  # type: RosterAdds
        self.roster_adds_value = self.roster_adds.value
        self.team_id = self.extracted_data.get("team_id", 0)
        self.team_key = self.extracted_data.get("team_key", "")
        self.team_logos = self.extracted_data.get("team_logos", [])
        self.team_points = self.extracted_data.get("team_points", TeamPoints({}))  # type: TeamPoints
        self.points = float(self.team_points.total or 0)
        self.team_projected_points = self.extracted_data.get("team_projected_points",
                                                             TeamProjectedPoints({}))  # type: TeamProjectedPoints
        self.projected_points = float(self.team_projected_points.total or 0)
        self.team_standings = self.extracted_data.get("team_standings", TeamStandings({}))  # type: TeamStandings
        self.wins = int(self.team_standings.outcome_totals.wins or 0)
        self.losses = int(self.team_standings.outcome_totals.losses or 0)
        self.ties = int(self.team_standings.outcome_totals.ties or 0)
        self.percentage = float(self.team_standings.outcome_totals.percentage or 0)
        self.playoff_seed = self.team_standings.playoff_seed or 0
        self.points_against = self.team_standings.points_against or 0.0
        self.points_for = self.team_standings.points_for or 0.0
        self.rank = self.team_standings.rank or 0
        self.streak_type = self.team_standings.streak.type or ""
        self.streak_length = self.team_standings.streak.value or 0
        self.url = self.extracted_data.get("url", "")
        self.waiver_priority = self.extracted_data.get("waiver_priority", 0)
        self.win_probability = float(self.extracted_data.get("win_probability", 0) or 0)


# noinspection PyUnresolvedReferences
class DraftResult(YahooFantasyObject):
    """Model class for "draft_result" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the DraftResult child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            pick (int): The draft pick number.
            round (int): The draft round.
            team_key (str): The Yahoo team key of the team that made the draft pick.
            player_key (str): The Yahoo player key of the player that was drafted.
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.pick = self.extracted_data.get("pick", 0)
        self.round = self.extracted_data.get("round", 0)
        self.team_key = self.extracted_data.get("team_key", "")
        self.player_key = self.extracted_data.get("player_key", "")


# noinspection PyUnresolvedReferences,GrazieInspection
class Standings(YahooFantasyObject):
    """Model class for "standings" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the Standings child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            teams (list[Team]): A list of YFPY Team instances with standings data.
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.teams = self.extracted_data.get("teams", [])


# noinspection PyUnresolvedReferences
class Transaction(YahooFantasyObject):
    """Model class for "transaction" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the Transaction child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            players (list[Player]): A list of YFPY Player instances.
            status (str): The transaction status ("successful", etc.).
            timestamp (int): The timestamp of when the transaction occurred.
            tradee_team_key (str): The Yahoo team key for the team receiving the player (if applicable).
            tradee_team_name (str): The team name of the team receiving the player (if applicable).
            trader_team_key (str): The Yahoo team key for the team sending the player (if applicable).
            trader_team_name (str): The team name for the team sending the player (if applicable).
            transaction_id (int): The unique transaction ID number.
            transaction_key (str): The Yahoo transaction key (Ex.: "406.l.413954.tr.555").
            type (str): The type of the transaction ("add", "drop", "trade", etc.).
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.players = self.extracted_data.get("players", [])
        self.status = self.extracted_data.get("status", "")
        self.timestamp = self.extracted_data.get("timestamp", 0)
        self.tradee_team_key = self.extracted_data.get("tradee_team_key", "")
        self.tradee_team_name = self.extracted_data.get("tradee_team_name", "")
        self.trader_team_key = self.extracted_data.get("trader_team_key", "")
        self.trader_team_name = self.extracted_data.get("trader_team_name", "")
        self.transaction_id = self.extracted_data.get("transaction_id", 0)
        self.transaction_key = self.extracted_data.get("transaction_key", "")
        self.type = self.extracted_data.get("type", "")


# noinspection PyUnresolvedReferences
class Manager(YahooFantasyObject):
    """Model class for "manager" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the Manager child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            email (str): The email address of the manager.
            guid (str): The unique Yahoo GUID of the user account associated with manager.
            image_url (str): The direct URL of the manager profile image.
            is_comanager (int): Numeric boolean (0 or 1) representing if the manager is a co-manager.
            manager_id (int): The unique manager ID in the league.
            nickname (str): The display nickname of the manager.
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.email = self.extracted_data.get("email", "")
        self.guid = self.extracted_data.get("guid", "")
        self.image_url = self.extracted_data.get("image_url", "")
        self.is_comanager = self.extracted_data.get("is_comanager", 0)
        self.manager_id = self.extracted_data.get("manager_id", 0)
        self.nickname = self.extracted_data.get("nickname", "")


# noinspection PyUnresolvedReferences
class Roster(YahooFantasyObject):
    """Model class for "roster" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the Roster child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            coverage_type (str): The timeframe for the selected roster ("week", "date", "season", etc.).
            week (int): The week number.
            is_editable (int): Numeric boolean (0 or 1) representing if the roster is editable.
            players (list[Player]): A list of YFPY Player instances.
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.coverage_type = self.extracted_data.get("coverage_type", "")
        self.week = self.extracted_data.get("week", 0)
        self.is_editable = self.extracted_data.get("is_editable", 0)
        self.players = self.extracted_data.get("players", [])


# noinspection PyUnresolvedReferences
class RosterAdds(YahooFantasyObject):
    """Model class for "roster_adds" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the RosterAdds child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            coverage_type (str): The timeframe for the selected roster ("week", "date", "season", etc.).
            coverage_value (int): The value of the coverage type (week number, for instance).
            value (int): The number of roster adds within the coverage timeframe.
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.coverage_type = self.extracted_data.get("coverage_type", "")
        self.coverage_value = self.extracted_data.get("coverage_value", 0)
        self.value = self.extracted_data.get("value", 0)


# noinspection PyUnresolvedReferences
class TeamLogo(YahooFantasyObject):
    """Model class for "team_logo" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the TeamLogo child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            size (str): The size of the team logo photo ("small", "large", etc.)
            url (str): The direct URL of the team logo photo.
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.size = self.extracted_data.get("size", "")
        self.url = self.extracted_data.get("url", "")


# noinspection PyUnresolvedReferences
class TeamPoints(YahooFantasyObject):
    """Model class for "team_points" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the TeamPoints child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            coverage_type (str): The timeframe for the selected team points ("week", "date", "season", etc.).
            season (int): The season year.
            total (float): The total team points for the coverage timeframe.
            week (int): The week number (if applicable).
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.coverage_type = self.extracted_data.get("coverage_type", "")
        self.season = self.extracted_data.get("season", 0)
        self.total = float(self.extracted_data.get("total", 0) or 0)
        self.week = self.extracted_data.get("week", 0)


# noinspection PyUnresolvedReferences
class TeamProjectedPoints(YahooFantasyObject):
    """Model class for "team_projected_points" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the TeamProjectedPoints child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            coverage_type (str): The timeframe for the selected team projected points ("week", "date", "season", etc.).
            total (float): The total team projected points for the coverage timeframe.
            week (int): The week number.
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.coverage_type = self.extracted_data.get("coverage_type", "")
        self.total = float(self.extracted_data.get("total", 0) or 0)
        self.week = self.extracted_data.get("week", 0)


# noinspection PyUnresolvedReferences
class TeamStandings(YahooFantasyObject):
    """Model class for "team_standings" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the TeamStandings child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            divisional_outcome_totals (DivisionalOutcomeTotals): A list of YFPY DivisionalOutcomeTotals instances.
            outcome_totals (OutcomeTotals): A YFPY OutcomeTotals instance.
            playoff_seed (int): The playoff seed position for the team.
            points_against (float): The total team points against.
            points_for (float): The total team points for.
            rank (int): The rank of the team in the league standings.
            streak (Streak): A YFPY Streak instance.
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.divisional_outcome_totals = self.extracted_data.get(
            "divisional_outcome_totals", DivisionalOutcomeTotals({}))  # type: DivisionalOutcomeTotals
        self.outcome_totals = self.extracted_data.get("outcome_totals", OutcomeTotals({}))  # type: OutcomeTotals
        self.playoff_seed = self.extracted_data.get("playoff_seed", 0)
        self.points_against = float(self.extracted_data.get("points_against", 0) or 0)
        self.points_for = float(self.extracted_data.get("points_for", 0) or 0)
        self.rank = self.extracted_data.get("rank", 0)
        self.streak = self.extracted_data.get("streak", Streak({}))  # type: Streak


# noinspection PyUnresolvedReferences
class DivisionalOutcomeTotals(YahooFantasyObject):
    """Model class for "divisional_outcome_totals" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the DivisionOutcomeTotals child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            losses (int): The number of losses by the team within the division.
            ties (int): The number of ties by the team within the division.
            wins (int): The number of wins by the team within the division.
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.losses = int(self.extracted_data.get("losses", 0) or 0)
        self.ties = int(self.extracted_data.get("ties", 0) or 0)
        self.wins = int(self.extracted_data.get("wins", 0) or 0)


# noinspection PyUnresolvedReferences
class OutcomeTotals(YahooFantasyObject):
    """Model class for "outcome_totals" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the OutcomeTotals child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            losses (int): The number of losses by the team.
            percentage (float): The win percentage of the team.
            ties (int): The number of ties by the team.
            wins (int): The number of wins by the team.
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.losses = int(self.extracted_data.get("losses", 0) or 0)
        self.percentage = float(self.extracted_data.get("percentage", 0) or 0)
        self.ties = int(self.extracted_data.get("ties", 0) or 0)
        self.wins = int(self.extracted_data.get("wins", 0) or 0)


# noinspection PyUnresolvedReferences
class Streak(YahooFantasyObject):
    """Model class for "streak" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the Streak child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            type (str): The streak type ("W" for win, "L" for loss, "T" for tie).
            value (int): The length of the streak.
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.type = self.extracted_data.get("type", "")
        self.value = self.extracted_data.get("value", 0)


# noinspection PyUnresolvedReferences
class Scoreboard(YahooFantasyObject):
    """Model class for "scoreboard" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the Scoreboard child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            week (int): The week for which the scoreboard applies.
            matchups (list[Matchup]): A list of YFPY Matchup instances representing the matchups for the week.
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.week = self.extracted_data.get("week", 0)
        self.matchups = self.extracted_data.get("matchups", [])


# noinspection DuplicatedCode, PyUnresolvedReferences
class Settings(YahooFantasyObject):
    """Model class for "settings" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the Settings child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            cant_cut_list (str): Numeric boolean (0 or 1) representing if the league uses the Yahoo "can't cut list".
            divisions (int): Numeric boolean (0 or 1) representing if the league has divisions.
            draft_pick_time (int): The number of seconds allowed to make each draft pick.
            draft_time (int): A timestamp representing when the draft will start.
            draft_type (str): The type of draft ("live", "offline", etc.)
            has_multiweek_championship (int): Numeric boolean (0 or 1) representing if the league has a multi-week
                championship matchup.
            has_playoff_consolation_games (bool): Numeric boolean (0 or 1) representing if the league has a consolation
                playoff bracket.
            is_auction_draft (int): Numeric boolean (0 or 1) representing if the league uses an auction draft.
            max_teams (int): The maximum number of teams allowed in the league.
            num_playoff_consolation_teams (int): The number of teams that make the consolation playoff bracket.
            num_playoff_teams (int): The number of teams that make the playoffs.
            pickem_enabled (int): Numeric boolean (0 or 1) representing if the league has enabled the built-in Yahoo
                "pick 'em" game that allows managers to pick winners of each fantasy matchup each week in the league.
            player_pool (str): Value designating what player pool is allowed for the league ("ALL", etc.).
            playoff_start_week (int): The week number on which the playoffs start.
            post_draft_players (str): Value designating what happens to players after the draft ("W" for waivers, etc.).
            roster_positions (list[RosterPosition]): A list of YFPY RosterPosition instances.
            scoring_type (str): Value designating what type of scoring the league uses ("head" for head-to-head, etc.).
            stat_categories (StatCategories): A YFPY StatCategories instance.
            stat_modifiers (StatModifiers): A YFPY StatModifiers instance.
            trade_end_date (str): A date string representing when trading is no longer allowed (format: "YYYY-MM-DD").
            trade_ratify_type (str): Value designating how trades are ratified ("commish" for commissioner, etc.).
            trade_reject_time (int): The number of days during which a trade can be rejected.
            uses_faab (int): Numeric boolean (0 or 1) representing if the league uses FAAB (Free Agent Acquisition
                Budget).
            uses_fractional_points (int): Numeric boolean (0 or 1) representing if the league allows fractional scoring.
            uses_lock_eliminated_teams (int): Numeric boolean (0 or 1) representing if the league locks teams
                eliminated from the playoffs.
            uses_negative_points (int): Numeric boolean (0 or 1) representing if the league allows negative scoring.
            uses_playoffs (int): Numeric boolean (0 or 1) representing if the league has playoffs.
            uses_playoff_reseeding (int): Numeric boolean (0 or 1) representing if the league reseeds the playoffs once
                the fantasy regular season is complete.
            waiver_rule (str): Value designating when players go to waivers ("gametime", etc.).
            waiver_time (int): The number of days that players remain on waivers.
            waiver_type (str): Value designating what type of waivers are used by the league ("R" for rolling, etc.).
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.cant_cut_list = self.extracted_data.get("cant_cut_list", "")
        self.divisions = self.extracted_data.get("divisions", 0)
        self.draft_pick_time = self.extracted_data.get("draft_pick_time", 0)
        self.draft_time = self.extracted_data.get("draft_time", 0)
        self.draft_type = self.extracted_data.get("draft_type", "")
        self.has_multiweek_championship = self.extracted_data.get("has_multiweek_championship", 0)
        self.has_playoff_consolation_games = self.extracted_data.get("has_playoff_consolation_games", False)
        self.is_auction_draft = self.extracted_data.get("is_auction_draft", 0)
        self.max_teams = self.extracted_data.get("max_teams", 0)
        self.num_playoff_consolation_teams = self.extracted_data.get("num_playoff_consolation_teams", 0)
        self.num_playoff_teams = self.extracted_data.get("num_playoff_teams", 0)
        self.pickem_enabled = self.extracted_data.get("pickem_enabled", 0)
        self.player_pool = self.extracted_data.get("player_pool", "")
        self.playoff_start_week = self.extracted_data.get("playoff_start_week", 0)
        self.post_draft_players = self.extracted_data.get("post_draft_players", "")
        self.roster_positions = self.extracted_data.get("roster_positions", [])
        self.scoring_type = self.extracted_data.get("scoring_type", "")
        self.stat_categories = self.extracted_data.get("stat_categories", StatCategories({}))  # type: StatCategories
        self.stat_modifiers = self.extracted_data.get("stat_modifiers", StatModifiers({}))  # type: StatModifiers
        self.trade_end_date = self.extracted_data.get("trade_end_date", "")
        self.trade_ratify_type = self.extracted_data.get("trade_ratify_type", "")
        self.trade_reject_time = self.extracted_data.get("trade_reject_time", 0)
        self.uses_faab = self.extracted_data.get("uses_faab", 0)
        self.uses_fractional_points = self.extracted_data.get("uses_fractional_points", 0)
        self.uses_lock_eliminated_teams = self.extracted_data.get("uses_lock_eliminated_teams", 0)
        self.uses_negative_points = self.extracted_data.get("uses_negative_points", 0)
        self.uses_playoff = self.extracted_data.get("uses_playoff", 0)
        self.uses_playoff_reseeding = self.extracted_data.get("uses_playoff_reseeding", 0)
        self.waiver_rule = self.extracted_data.get("waiver_rule", "")
        self.waiver_time = self.extracted_data.get("waiver_time", 0)
        self.waiver_type = self.extracted_data.get("waiver_type", "")


# noinspection PyUnresolvedReferences
class Division(YahooFantasyObject):
    """Model class for "division" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the Division child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            division_id (int): The unique division ID number in the league.
            name (str): The division name.
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.division_id = self.extracted_data.get("division_id", 0)
        self.name = self.extracted_data.get("name", "")


# noinspection PyUnresolvedReferences
class RosterPosition(YahooFantasyObject):
    """Model class for "roster_position" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the RosterPosition child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            count (int): The number of roster slots available for this position.
            position (str): The position string.
            position_type (str): The position type ("O" for offense, etc.)
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.count = self.extracted_data.get("count", 0)
        self.position = self.extracted_data.get("position", "")
        self.position_type = self.extracted_data.get("position_type", "")


# noinspection PyUnresolvedReferences
class StatCategories(YahooFantasyObject):
    """Model class for "stat_categories" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the StatCategories child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            stats (list[Stat]): A list of YFPY Stat instances representing the league stat categories.
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.stats = self.extracted_data.get("stats", [])


# noinspection PyUnresolvedReferences
class StatModifiers(YahooFantasyObject):
    """Model class for "stat_modifiers" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the StatModifiers child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            stats (list[Stat]): A list of YFPY Stat instances containing modifiers for each stat category.
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.stats = self.extracted_data.get("stats", [])


# noinspection PyUnresolvedReferences
class Stat(YahooFantasyObject):
    """Model class for "stat" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the Stat child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            bonuses (list[Bonus]): A list of YFPY Bonus instances available for this stat category.
            display_name (str): The abbreviated display name of the stat.
            enabled (int): Numeric boolean (0 or 1) representing if this stat is enabled for league scoring.
            name (str): The full name of the stat.
            position_type (str): The player position type eligible for the stat.
            sort_order (int): Numeric boolean (0 or 1) representing if the stat is sorted highest to lowest (1) or
                lowest to highest (0).
            stat_id (int): The unique stat ID number in the league.
            stat_position_types (list[PositionType]): A list of YFPY PositionType instances.
            value (float): The value of the stat (if applicable).
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.bonuses = self.extracted_data.get("bonuses", [])
        self.display_name = self.extracted_data.get("display_name", "")
        self.enabled = self.extracted_data.get("enabled", 0)
        self.name = self.extracted_data.get("name", "")
        self.position_type = self.extracted_data.get("position_type", "")
        self.sort_order = self.extracted_data.get("sort_order", 0)
        self.stat_id = self.extracted_data.get("stat_id", 0)
        self.stat_position_types = self.extracted_data.get("stat_position_types", [])
        try:
            self.value = float(self.extracted_data.get("value", 0) or 0)
        except ValueError:
            self.value = 0.0


# noinspection PyUnresolvedReferences
class StatPositionType(YahooFantasyObject):
    """Model class for "stat_position_type" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the StatPositionType child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            is_only_display_stat (int): Numeric boolean (0 or 1) representing if the stat is only for display (such as
                if it is just the player position string).
            position_type (str): The type of the position ("O" for offense, etc.)
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.is_only_display_stat = self.extracted_data.get("is_only_display_stat", 0)
        self.position_type = self.extracted_data.get("position_type", "")


# noinspection PyUnresolvedReferences
class Bonus(YahooFantasyObject):
    """Model class for "bonus" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the Bonus child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            points (int): The points awarded when the bonus is won.
            target (int): The stat value target required to be awarded the bonus.
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.points = self.extracted_data.get("points", 0)
        self.target = self.extracted_data.get("target", 0)


# noinspection PyUnresolvedReferences
class Matchup(YahooFantasyObject):
    """Model class for "matchup" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the Matchup child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            is_consolation (int): Numeric boolean (0 or 1) representing if the matchup is in a consolation bracket.
            is_matchup_recap_available (int): Numeric boolean (0 or 1) representing if the matchup recap is available.
            is_playoffs (int): Numeric boolean (0 or 1) representing if the matchup is in the playoffs bracket.
            is_tied (int): Numeric boolean (0 or 1) representing if the matchup result is tied.
            matchup_grades (list[MatchupGrade]): A list of YFPY MatchupGrade instances.
            matchup_recap_title (str): The title of the matchup recap.
            matchup_recap_url (str): The direct URL of the matchup recap.
            status (str): The status of the matchup ("postevent", etc.).
            teams (list[Team]): A list of YFPY Team instances for teams in the matchup.
            week (int): The week number of the matchup.
            week_end (str): A date string representing the end of the matchup week (format: "YYYY-MM-DD").
            week_start (str): A date string representing the start of the matchup week (format: "YYYY-MM-DD").
            winner_team_key (str): The Yahoo team key of the team that won the matchup.
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.is_consolation = self.extracted_data.get("is_consolation", 0)
        self.is_matchup_recap_available = self.extracted_data.get("is_matchup_recap_available", 0)
        self.is_playoffs = self.extracted_data.get("is_playoffs", 0)
        self.is_tied = self.extracted_data.get("is_tied", 0)
        self.matchup_grades = self.extracted_data.get("matchup_grades", [])
        self.matchup_recap_title = self.extracted_data.get("matchup_recap_title", "")
        self.matchup_recap_url = self.extracted_data.get("matchup_recap_url", "")
        self.status = self.extracted_data.get("status", "")
        self.teams = self.extracted_data.get("teams", [])
        self.week = self.extracted_data.get("week", 0)
        self.week_end = self.extracted_data.get("week_end", "")
        self.week_start = self.extracted_data.get("week_start", "")
        self.winner_team_key = self.extracted_data.get("winner_team_key", "")


# noinspection PyUnresolvedReferences
class MatchupGrade(YahooFantasyObject):
    """Model class for "matchup_grade" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the MatchupGrade child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            grade (str): The letter grade assigned to the matchup performance ("A+", "A", ..., "F-").
            team_key (str): The Yahoo team key for the team receiving the matchup grade.
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.grade = self.extracted_data.get("grade", "")
        self.team_key = self.extracted_data.get("team_key", "")


# noinspection PyUnresolvedReferences
class Player(YahooFantasyObject):
    """Model class for "player" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the Player child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            bye_weeks (ByeWeeks): A YFPY ByeWeeks instance.
            bye (int): The week number that the player is on bye.
            display_position (str): The display string for the player position.
            draft_analysis (DraftAnalysis): A YFPY DraftAnalysis instance.
            average_draft_pick (float): The average pick at which the player was drafted.
            average_draft_round (float): The average round in which the player was drafted.
            average_draft_cost (float): The average price paid for the player to be drafted.
            percent_drafted (float): The overall percentage the player was drafted.
            editorial_player_key (str): The Yahoo player key using the game key.
            editorial_team_abbr (str): The abbreviation of the professional team name for which the player plays.
            editorial_team_full_name (str): The name of the professional team for which the player plays.
            editorial_team_key (str): The Yahoo team key using the game key.
            eligible_positions (list[str]): A list of positions for which the player is eligible.
            has_player_notes (int): Numeric boolean (0 or 1) representing if the player has any notes.
            headshot (Headshot): A YFPY Headshot instance.
            headshot_size (str): The headshot photo size ("small", "large", etc.)
            headshot_url (str): The direct URL of the headshot photo.
            is_editable (int): Numeric boolean (0 or 1) representing if the player is editable.
            is_undroppable (int): Numeric boolean (0 or 1) representing if the player is undroppable.
            name (Name): A YFPY Name instance.
            first_name (str): The first name of the player.
            last_name (str): The last name of the player.
            full_name (str): The full name of the player.
            ownership (Ownership): A YFPY Ownership instance.
            percent_owned (PercentOwned): A YFPY PercentOwned instanced.
            percent_owned_value (float): The percentage value the player is/was owned in the coverage timeframe.
            player_id (int): The unique player ID.
            player_key (str): The Yahoo player key.
            player_notes_last_timestamp (int): A timestamp of the most recent players notes.
            player_points (PlayerPoints): A YFPY PlayerPoints instance.
            player_points_value (float): The total points for the player within the coverage timeframe.
            player_stats (PlayerStats): A YFPY PlayerStats instance.
            stats (list[Stat]): A list of YFPY Stat instances.
            position_type (str): The position type of the player ("offense", "defense", etc.).
            primary_position (str): The primary position of the player.
            selected_position (SelectedPosition): A YFPY SelectedPosition instance.
            selected_position_value (str): The selected position of the player.
            status (str): The status of the player ("IR", "PUP", "O", "Q", etc.).
            transaction_data (TransactionData): A YFPY TransactionData instance.
            uniform_number (int): The uniform number of the player.
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.bye_weeks = self.extracted_data.get("bye_weeks", ByeWeeks({}))  # type: ByeWeeks
        self.bye = int(self.bye_weeks.week or 0)
        self.display_position = self.extracted_data.get("display_position", "")
        self.draft_analysis = self.extracted_data.get("draft_analysis", DraftAnalysis({}))  # type: DraftAnalysis
        self.average_draft_pick = float(self.draft_analysis.average_pick or 0)
        self.average_draft_round = float(self.draft_analysis.average_round or 0)
        self.average_draft_cost = float(self.draft_analysis.average_cost or 0)
        self.percent_drafted = float(self.draft_analysis.percent_drafted or 0)
        self.editorial_player_key = self.extracted_data.get("editorial_player_key", "")
        self.editorial_team_abbr = self.extracted_data.get("editorial_team_abbr", "")
        self.editorial_team_full_name = self.extracted_data.get("editorial_team_full_name", "")
        self.editorial_team_key = self.extracted_data.get("editorial_team_key", "")
        eligible_positions = self.extracted_data.get("eligible_positions")
        self.eligible_positions = []
        if isinstance(eligible_positions, dict):
            self.eligible_positions.append(eligible_positions.get("position"))
        elif isinstance(eligible_positions, list):
            for position in eligible_positions:
                if isinstance(position, dict):
                    self.eligible_positions.append(position.get("position"))
                else:
                    self.eligible_positions.append(position)
        elif isinstance(eligible_positions, str):
            self.eligible_positions.append(eligible_positions)
        self.has_player_notes = self.extracted_data.get("has_player_notes", 0)
        self.headshot = self.extracted_data.get("headshot", Headshot({}))  # type: Headshot
        self.headshot_size = self.headshot.size or ""
        self.headshot_url = self.headshot.url or ""
        self.is_editable = self.extracted_data.get("is_editable", 0)
        self.is_undroppable = self.extracted_data.get("is_undroppable", 0)
        self.name = self.extracted_data.get("name", Name({}))  # type: Name
        self.first_name = self.name.first or ""
        self.last_name = self.name.last or ""
        self.full_name = self.name.full or ""
        self.ownership = self.extracted_data.get("ownership", Ownership({}))  # type: Ownership
        self.percent_owned = self.extracted_data.get("percent_owned", PercentOwned({}))  # type: PercentOwned
        self.percent_owned_value = self.percent_owned.value or 0.0
        self.player_id = self.extracted_data.get("player_id", 0)
        self.player_key = self.extracted_data.get("player_key", "")
        self.player_notes_last_timestamp = self.extracted_data.get("player_notes_last_timestamp", 0)
        self.player_points = self.extracted_data.get("player_points", PlayerPoints({}))  # type: PlayerPoints
        self.player_points_value = self.player_points.total or 0.0
        self.player_stats = self.extracted_data.get("player_stats", PlayerStats({}))  # type: PlayerStats
        self.stats = self.player_stats.stats or []
        self.position_type = self.extracted_data.get("position_type", "")
        self.primary_position = self.extracted_data.get("primary_position", "")
        self.selected_position = self.extracted_data.get("selected_position",
                                                         SelectedPosition({}))  # type: SelectedPosition
        self.selected_position_value = self.selected_position.position or ""
        self.status = self.extracted_data.get("status", "")
        self.transaction_data = self.extracted_data.get("transaction_data",
                                                        TransactionData({}))  # type: TransactionData
        self.uniform_number = self.extracted_data.get("uniform_number", 0)


# noinspection PyUnresolvedReferences
class ByeWeeks(YahooFantasyObject):
    """Model class for "bye_weeks" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the ByeWeeks child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            week (int): The week number that the player is on bye.
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.week = self.extracted_data.get("week", 0)


# noinspection PyUnresolvedReferences
class DraftAnalysis(YahooFantasyObject):
    """Model class for "draft_analysis" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the DraftAnalysis child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            average_pick (float): The average pick at which the player was drafted.
            average_round (float): The average round in which the player was drafted.
            average_cost (float): The average price paid for the player to be drafted.
            percent_drafted (float): The overall percentage the player was drafted.
        """
        YahooFantasyObject.__init__(self, extracted_data)
        try:
            self.average_pick = float(self.extracted_data.get("average_pick", 0) or 0)
        except ValueError:
            self.average_pick = 0.0
        try:
            self.average_round = float(self.extracted_data.get("average_round", 0) or 0)
        except ValueError:
            self.average_round = 0.0
        try:
            self.average_cost = float(self.extracted_data.get("average_cost", 0) or 0)
        except ValueError:
            self.average_cost = 0.0
        try:
            self.percent_drafted = float(self.extracted_data.get("percent_drafted", 0) or 0)
        except ValueError:
            self.percent_drafted = 0.0


# noinspection PyUnresolvedReferences
class Headshot(YahooFantasyObject):
    """Model class for "headshot" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the Headshot child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            size (str): The size of the headshot photo ("small", "large", etc.)
            url (str): The direct URL of the headshot photo.
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.size = self.extracted_data.get("size", "")
        self.url = self.extracted_data.get("url", "")


# noinspection PyUnresolvedReferences
class Name(YahooFantasyObject):
    """Model class for "name" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the Name child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            ascii_first (str): The ASCII encoded string of the first name of the player.
            ascii_last (str): The ASCII encoded string of the last name of the player.
            first (str): The first name of the player.
            full (str): The full name of the player.
            last (str): The last name of teh player.
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.ascii_first = self.extracted_data.get("ascii_first", "")
        self.ascii_last = self.extracted_data.get("ascii_last", "")
        self.first = self.extracted_data.get("first", "")
        self.full = self.extracted_data.get("full", "")
        self.last = self.extracted_data.get("last", "")


# noinspection PyUnresolvedReferences
class Ownership(YahooFantasyObject):
    """Model class for "ownership" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the Ownership child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            ownership_type (str): The current location of the player in the league ("team", "waivers", etc.).
            owner_team_key (str): The Yahoo team key for the team that owns the player.
            owner_team_name (str): The team name for the team that owns the player.
            teams (list[Team]): A list of YFPY Team instances.
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.ownership_type = self.extracted_data.get("ownership_type", "")
        self.owner_team_key = self.extracted_data.get("owner_team_key", "")
        self.owner_team_name = self.extracted_data.get("owner_team_name", "")
        self.teams = self.extracted_data.get("teams", [])


# noinspection PyUnresolvedReferences
class PercentOwned(YahooFantasyObject):
    """Model class for "percent_owned" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the PercentOwned child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            coverage_type (str): The timeframe for the selected player ownership ("week", "date", "season", etc.).
            week (int): The week number (when applicable).
            value (int): The percentage value the player is/was owned in the coverage timeframe.
            delta (float): The change in the percentage value from the previous coverage timeframe to the current
                coverage timeframe.
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.coverage_type = self.extracted_data.get("coverage_type", "")
        self.week = self.extracted_data.get("week", 0)
        self.value = self.extracted_data.get("value", 0)
        self.delta = float(self.extracted_data.get("delta", 0) or 0)


# noinspection PyUnresolvedReferences
class PlayerPoints(YahooFantasyObject):
    """Model class for "player_points" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the PlayerPoints child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            coverage_type (str): The timeframe for the selected player points ("week", "date", "season", etc.).
            week (int): The week number (when applicable).
            total (float): The total points for the player within the coverage timeframe.
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.coverage_type = self.extracted_data.get("coverage_type", "")
        self.week = self.extracted_data.get("week", 0)
        self.total = float(self.extracted_data.get("total", 0) or 0)


# noinspection PyUnresolvedReferences
class PlayerStats(YahooFantasyObject):
    """Model class for "player_stats" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the PlayerStats child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            coverage_type (str): The timeframe for the selected player stats ("week", "date", "season", etc.).
            week (int): The week number (when applicable).
            stats (list[Stat]): A list of YFPY Stat instances for the player.
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.coverage_type = self.extracted_data.get("coverage_type", "")
        self.week = self.extracted_data.get("week", 0)
        self.stats = self.extracted_data.get("stats", [])


# noinspection PyUnresolvedReferences
class SelectedPosition(YahooFantasyObject):
    """Model class for "selected_position" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the SelectedPosition child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            coverage_type (str): The timeframe for the selected position ("week", "date", "season", etc.).
            is_flex (int): Numeric boolean (0 or 1) representing if the selected player is in a flex roster slot.
            position (str): The selected position of the player.
            week (int): The week number (when applicable).
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.coverage_type = self.extracted_data.get("coverage_type", "")
        self.is_flex = self.extracted_data.get("is_flex", 0)
        self.position = self.extracted_data.get("position", "")
        self.week = self.extracted_data.get("week", 0)


# noinspection PyUnresolvedReferences
class TransactionData(YahooFantasyObject):
    """Model class for "transaction_data" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the TransactionData child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            destination_team_key (str): The Yahoo team key for the receiving team.
            destination_team_name (str): The name of the receiving team.
            destination_type (str): The destination of the player (waivers, free agency, another team, etc.).
            source_team_key (str): The Yahoo team key of the sending team.
            source_team_name (str): The name of the sending team.
            source_type (str): The origin of the player (waivers, free agency, another team, etc.).
            type (str): The type of the transaction ("add", "drop", "trade", etc.).
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.destination_team_key = self.extracted_data.get("destination_team_key", "")
        self.destination_team_name = self.extracted_data.get("destination_team_name", "")
        self.destination_type = self.extracted_data.get("destination_type", "")
        self.source_team_key = self.extracted_data.get("source_team_key", "")
        self.source_team_name = self.extracted_data.get("source_team_name", "")
        self.source_type = self.extracted_data.get("source_type", "")
        self.type = self.extracted_data.get("type", "")
