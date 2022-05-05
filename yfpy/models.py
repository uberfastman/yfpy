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
            games (list of Game): List of Yahoo Fantasy games in which the user participates/has participated.
            guid (str): Yahoo user ID.

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
            code (str): Yahoo Fantasy game code.
            game_id (int): Yahoo Fantasy game ID.
            game_key (str): Yahoo Fantasy game key.
            game_weeks (list of GameWeek): Yahoo Fantasy GameWeek objects.
            is_game_over (int): Numeric boolean (0 or 1) representing if the Yahoo Fantasy Game is complete.
            is_live_draft_lobby_active (int): Numeric boolean (0 or 1) representing if the draft lobby is active.
            is_offseason (int): Numeric boolean (0 or 1) representing if it is the offseason for the respective sport.
            is_registration_over (int): Numeric boolean (0 or 1) representing registration for the fantasy game is over.
            leagues (list of League): Yahoo Fantasy League objects.
            name (str): Yahoo Fantasy game name.
            position_types (list of PositionType): Yahoo Fantasy PositionType objects.
            roster_positions (list of RosterPosition): Yahoo Fantasy RosterPosition objects.
            season (int): Yahoo Fantasy game year.
            stat_categories (StatCategories): Yahoo Fantasy StatCategories object.
            teams (list of Team): Yahoo Fantasy Team objects.
            type (str): Yahoo Fantasy game type.
            url (str): Yahoo Fantasy game URL.

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
            display_name (str): Yahoo Fantasy GameWeek display name.
            end (str): Yahoo Fantasy GameWeek end date.
            start (str): Yahoo Fantasy GameWeek start date.
            week (int): Yahoo Fantasy GameWeek week number.

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
            type (str):
            display_name (str):

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
            allow_add_to_dl_extra_pos (int):
            current_week (int):
            draft_results (str):
            draft_status (str):
            display_name (str):
            edit_key (int):
            end_date (str):
            end_week (int):
            entry_fee (str):
            game_code (str):
            iris_group_chat_id (str):
            is_cash_league (int):
            is_finished (int):
            is_pro_league (str):
            league_id (str):
            league_key (str):
            league_type (str):
            league_update_timestamp (int):
            logo_url (str):
            name (str):
            num_teams (str):
            password (str):
            payment_deadline (str):
            players (str):
            renew (str):
            renewed (str):
            scoreboard (Scoreboard):
            matchups (list of Matchup):
            scoring_type (str):
            season (int):
            settings (Settings):
            short_invitation_url (str):
            standings (Standings):
            teams_ordered_by_standings (list of Team):
            start_date (str):
            start_week (int):
            transactions (list of Transaction):
            url (str):
            weekly_deadline (str):

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
            clinched_playoffs (int):
            division_id (str):
            draft_grade (str):
            draft_position (int):
            draft_recap_url (str):
            draft_results (list of DraftResult):
            faab_balance (int):
            has_draft_grade (int):
            league_scoring_type (str):
            managers (list of Manager | dict of str: Manager):
            matchups (list of Matchup):
            name (str):
            number_of_moves (int):
            number_of_trades (int):
            roster (Roster):
            players (list of Player):
            roster_adds (RosterAdds):
            roster_adds_value (int):
            team_id (int):
            team_key (str):
            team_logos (list of TeamLogo):
            team_points (TeamPoints):
            points (float):
            team_projected_points (TeamProjectedPoints):
            projected_points (float):
            team_standings (TeamStandings):
            wins (int):
            losses (int):
            ties (int):
            percentage (float):
            playoff_seed (int):
            points_against (float):
            points_for (float):
            rank (int):
            streak_type (str):
            streak_length (int):
            url (str):
            waiver_priority (int):
            win_probability (float):

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
            pick (int):
            round (int):
            team_key (str):
            player_key (str):
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.pick = self.extracted_data.get("pick", 0)
        self.round = self.extracted_data.get("round", 0)
        self.team_key = self.extracted_data.get("team_key", "")
        self.player_key = self.extracted_data.get("player_key", "")


# noinspection PyUnresolvedReferences
class Standings(YahooFantasyObject):
    """Model class for "standings" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the Standings child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            teams (list of Team):
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
            players (list of Player):
            status (str):
            timestamp (int):
            tradee_team_key (str):
            tradee_team_name (str):
            trader_team_key (str):
            trader_team_name (str):
            transaction_id (int):
            transaction_key (str):
            type (str):
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
            email (str):
            guid (str):
            image_url (str):
            is_comanager (int):
            manager_id (int):
            nickname (str):
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
            coverage_type (str):
            week (int):
            is_editable (int):
            players (list of Player):
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
            coverage_type (str):
            coverage_value (int):
            value (int):
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
            size (str):
            url (str):
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
            coverage_type (str):
            season (int):
            total (float):
            week (int):
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
            coverage_type (str):
            total (float):
            week (int):
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
            divisional_outcome_totals (DivisionalOutcomeTotals):
            outcome_totals (OutcomeTotals):
            playoff_seed (int):
            points_against (float):
            points_for (float):
            rank (int):
            streak (Streak):
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
            losses (int):
            ties (int):
            wins (int):
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
            losses (int):
            percentage (float):
            ties (int):
            wins (int):
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
            type (str):
            value (int):
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
            week (int):
            matchups (list of Matchup):
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
            cant_cut_list (str):
            divisions (int):
            draft_pick_time (int):
            draft_time (int):
            draft_type (str):
            has_multiweek_championship (int):
            has_playoff_consolation_games (bool):
            is_auction_draft (int):
            max_teams (int):
            num_playoff_consolation_games (int):
            num_playoff_teams (int):
            pickem_enabled (int):
            player_pool (str):
            playoff_start_week (int):
            post_draft_players (str):
            roster_positions (list of RosterPosition):
            scoring_type (str):
            stat_categories (StatCategories):
            stat_modifiers (StatModifiers):
            trade_end_date (str):
            trade_ratify_type (str):
            trade_reject_time (int):
            uses_faab (int):
            uses_fractional_points (int):
            uses_lock_eliminated_teams (int):
            uses_negative_points (int):
            uses_playoffs (int):
            uses_playoff_reseeding (int):
            waiver_rule (str):
            waiver_time (int):
            waiver_type (str):
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
            division_id (int):
            name (str):
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
            count (int):
            position (str):
            position_type (str):
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
            stats (list of Stat):
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
            stats (list of Stat):
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
            bonuses (list of Bonus):
            display_name (str):
            enabled (int):
            name (str):
            position_type (str):
            sort_order (int):
            stat_id (int):
            stat_position_types (list of PositionType):
            value (float):
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
        self.value = float(self.extracted_data.get("value", 0) or 0)


# noinspection PyUnresolvedReferences
class StatPositionType(YahooFantasyObject):
    """Model class for "stat_position_type" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the StatPositionType child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            is_only_display_stat (int):
            position_type (str):
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
            points (int):
            target (int):
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
            is_consolation (int):
            is_matchup_recap_available (int):
            is_playoffs (int):
            is_tied (int):
            matchup_grades (list of MatchupGrade):
            matchup_recap_title (str):
            matchup_recap_url (str):
            status (str):
            teams (list of Team):
            week (int):
            week_end (str):
            week_start (str):
            winner_team_key (str):
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
            grade (str):
            team_key (str):
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
            bye_weeks (ByeWeeks):
            bye (int):
            display_position (str):
            draft_analysis (DraftAnalysis):
            average_draft_pick (float):
            average_draft_round (float):
            average_draft_cost (float):
            percent_drafted (float):
            editorial_player_key (str):
            editorial_team_abbr (str):
            editorial_team_full_name (str):
            editorial_team_key (str):
            eligible_positions (list of str):
            has_player_notes (int):
            headshot (Headshot):
            headshot_size (str):
            headshot_url (str):
            is_editable (int):
            is_undroppable (int):
            name (Name):
            first_name (str):
            last_name (str):
            full_name (str):
            ownership (Ownership):
            percent_owned (PercentOwned):
            percent_owned_value (float):
            player_id (int):
            player_key (str):
            player_notes_last_timestamp (int):
            player_points (PlayerPoints):
            player_points_value (float):
            player_stats (PlayerStats):
            stats (list of Stat):
            position_type (str):
            primary_position (str):
            selected_position (SelectedPosition):
            selected_position_value (str):
            status (str):
            transaction_data (TransactionData):
            uniform_number (int):
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
        if isinstance(eligible_positions, dict):
            self.eligible_positions = [eligible_positions.get("position")]
        elif isinstance(eligible_positions, list):
            self.eligible_positions = [position.get("position") for position in eligible_positions]
        else:
            self.eligible_positions = []
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
            week (int):
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
            average_pick (float):
            average_round (float):
            average_cost (float):
            percent_drafted (float):
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.average_pick = float(self.extracted_data.get("average_pick", 0) or 0)
        self.average_round = float(self.extracted_data.get("average_round", 0) or 0)
        self.average_cost = float(self.extracted_data.get("average_cost", 0) or 0)
        self.percent_drafted = float(self.extracted_data.get("percent_drafted", 0) or 0)


# noinspection PyUnresolvedReferences
class Headshot(YahooFantasyObject):
    """Model class for "headshot" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the Headshot child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            size (str):
            url (str):
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
            ascii_first (str):
            ascii_last (str):
            first (str):
            full (str):
            last (str):
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
            ownership_type (str):
            owner_team_key (str):
            owner_team_name (str):
            teams (list of Team):
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
            coverage_type (str):
            week (int):
            value (int):
            delta (float):
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
            coverage_type (str):
            week (int):
            total (float):
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
            coverage_type (str):
            week (int):
            stats (list of Stat):
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
            coverage_type (str):
            is_flex (int):
            position (str):
            week (int):
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
            destination_team_key (str):
            destination_team_name (str):
            destination_type (str):
            source_team_key (str):
            source_team_name (str):
            source_type (str):
            type (str):
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.destination_team_key = self.extracted_data.get("destination_team_key", "")
        self.destination_team_name = self.extracted_data.get("destination_team_name", "")
        self.destination_type = self.extracted_data.get("destination_type", "")
        self.source_team_key = self.extracted_data.get("source_team_key", "")
        self.source_team_name = self.extracted_data.get("source_team_name", "")
        self.source_type = self.extracted_data.get("source_type", "")
        self.type = self.extracted_data.get("type", "")
