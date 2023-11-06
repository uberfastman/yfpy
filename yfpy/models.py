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

import os
from operator import getitem
from typing import Union, Any, List, Dict, Type

from stringcase import snakecase

from yfpy.logger import get_logger
from yfpy.utils import jsonify_data

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
        self._extracted_data: Dict = extracted_data
        self._index: int = 0
        if isinstance(extracted_data, dict):
            self._keys: List = list(self._extracted_data.keys())

    def __str__(self):
        """Override __str__ to display YahooFantasyObject attribute values as JSON.
        """
        return f"{self.__class__.__name__}({self.to_json()})"

    def __repr__(self):
        """Override __repr__ to display YahooFantasyObject attribute values as JSON.
        """
        return f"{self.__class__.__name__}({self.to_json()})"

    def __getattribute__(self, attribute_name: str):
        """Override __getattribute__ to flatten lists of single-key dictionaries with objects as values to lists of
        objects.
        """
        attribute = object.__getattribute__(self, attribute_name)

        # skip builtin attributes that start with underscores and check if attribute is a list or dict
        if not attribute_name.startswith("_") and isinstance(attribute, (list, dict)):
            if attribute:
                # extract singular key from parent plural key
                attribute_element_name = None
                if attribute_name == "bonuses":
                    attribute_element_name = "bonus"
                elif attribute_name.endswith("s"):
                    attribute_element_name = attribute_name[:-1]

                if attribute_element_name:
                    if isinstance(attribute, list):
                        # flatten list of single-key dictionaries with object values to list of object values
                        return [el[attribute_element_name] if isinstance(el, dict) else el for el in attribute]
                    elif isinstance(attribute, dict):
                        # flatten single-key dictionary with object value to list of object
                        return [attribute[attribute_element_name]]
                    else:
                        return attribute
                else:
                    return attribute
            else:
                return attribute
        else:
            return attribute

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._equality_field_dict() == other._equality_field_dict()

    def __len__(self):
        return len(self._extracted_data)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            if isinstance(self._extracted_data, dict):
                result = self._extracted_data.get(self._keys[self._index])
            else:
                result = self._extracted_data[self._index]
        except IndexError:
            raise StopIteration
        self._index += 1
        return result

    def __reversed__(self):
        return reversed(self._keys)

    def __del__(self):
        if os.environ.get("CHECK_FOR_MISSING_YAHOO_DATA", None):
            self._check_for_missing_fields()

    def _check_for_missing_fields(self) -> List[str]:

        unknown_extracted_data_keys = list(
            set(self._keys)
            - set([att for att in (set(dir(self)) - set(dir(YahooFantasyObject))) if not att.startswith("_")])
        )
        unknown_extracted_data_key_count = len(unknown_extracted_data_keys)

        if unknown_extracted_data_key_count > 0:
            logger.debug(
                f"The Yahoo Fantasy Sports API includes {unknown_extracted_data_key_count} additional data "
                f"fields for {self.__class__.__name__} that are not included in "
                f"YFPY: {unknown_extracted_data_keys}"
            )

        return unknown_extracted_data_keys

    @staticmethod
    def _get_nested_value(obj: object, value_parents: Union[str, List], value_default: Any = None,
                          value_as: Type = None) -> Any:

        if isinstance(value_parents, str):
            value_parents = [value_parents]

        try:
            for ref in value_parents:
                if isinstance(obj, dict):
                    obj = getitem(obj, ref)
                else:
                    obj = getattr(obj, ref)
        except KeyError:
            return value_default
        except AttributeError:
            return value_default

        if obj is not None:
            if value_as is not None:
                try:
                    return value_as(obj)
                except ValueError:
                    return value_default
            else:
                return obj
        else:
            return value_default

    def _convert_to_string(self, extracted_data_key: str) -> str:
        return str(self._extracted_data.get(extracted_data_key, ""))

    def _equality_field_dict(self) -> Dict:
        return {k: v for k, v in self.__dict__.items() if k not in ["_extracted_data", "_index", "_keys"]}

    def subclass_dict(self) -> Dict:
        """Derive snake case dictionary keys from custom object type camel case class names.

        Returns:
            dict: Dictionary with snake case strings of all subclasses of YahooFantasyObject as keys and subclasses as
            values.

        """
        return {snakecase(cls.__name__): cls for cls in self.__class__.__mro__[-2].__subclasses__()}

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
        return jsonify_data(self.serialized())

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
        self.games: List = self._extracted_data.get("games", [])
        self.guid: str = self._extracted_data.get("guid", "")


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
            contest_group_id (int): The contest group ID of the Yahoo Fantasy game/contest.
            current_week (int): The current (or last if complete) week of the Yahoo Fantasy game/contest.
            editorial_season (int): The year in which the Yahoo Fantasy game/contest starts.
            game_id (int): The Yahoo Fantasy game ID.
            game_key (str): The Yahoo Fantasy game key.
            game_weeks (list[GameWeek]): A list of YFPY GameWeek instances.
            has_schedule (int): Numeric boolean (0 or 1) representing if the Yahoo Fantasy contest has a schedule.
            is_contest_over (int): Numeric boolean (0 or 1) representing if the Yahoo Fantasy contest is complete.
            is_contest_reg_active (int): Numeric boolean (0 or 1) representing if the Yahoo Fantasy contest is active.
            is_game_over (int): Numeric boolean (0 or 1) representing if the Yahoo Fantasy game is complete.
            is_live_draft_lobby_active (int): Numeric boolean (0 or 1) representing if the draft lobby is active.
            is_offseason (int): Numeric boolean (0 or 1) representing if it is the offseason for the respective sport.
            is_registration_over (int): Numeric boolean (0 or 1) representing registration for the fantasy game is over.
            leagues (list[League]): A list of YFPY League instances.
            name (str): The name of the Yahoo Fantasy game.
            picks_status (str): The status of the Yahoo Fantasy game/contest picks when applicable.
            players (list[Player]): A list of YFPY Player instances.
            position_types (list[PositionType]): A list of YFPY PositionType instances.
            roster_positions (list[RosterPosition]): A list of YFPY RosterPosition instances.
            scenario_generator (int): Numeric boolean (0 or 1) representing if the Yahoo Fantasy game has a scenario
                generator.
            season (int): The Yahoo Fantasy game year.
            stat_categories (StatCategories): A YFPY StatCategories instance.
            teams (list[Team]): A list of YFPY Team instances.
            type (str): The type of the Yahoo Fantasy game.
            url (str): The direct URL of the Yahoo Fantasy game.

        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.code: str = self._extracted_data.get("code", "")
        self.contest_group_id: int = self._extracted_data.get("contest_group_id", None)
        self.current_week: int = self._extracted_data.get("current_week", None)
        self.editorial_season: int = self._extracted_data.get("editorial_season", None)
        self.game_id: int = self._extracted_data.get("game_id", None)
        self.game_key: str = self._convert_to_string("game_key")  # convert to string to handle leading zeros
        self.game_weeks: List[GameWeek] = self._extracted_data.get("game_weeks", [])
        self.has_schedule: int = self._extracted_data.get("has_schedule", 0)
        self.is_contest_over: int = self._extracted_data.get("is_contest_over", 0)
        self.is_contest_reg_active: int = self._extracted_data.get("is_contest_reg_active", 0)
        self.is_game_over: int = self._extracted_data.get("is_game_over", 0)
        self.is_live_draft_lobby_active: int = self._extracted_data.get("is_live_draft_lobby_active", 0)
        self.is_offseason: int = self._extracted_data.get("is_offseason", 0)
        self.is_registration_over: int = self._extracted_data.get("is_registration_over", 0)
        self.leagues: List[League] = self._extracted_data.get("leagues", [])
        self.name: str = self._extracted_data.get("name", "")
        self.picks_status: str = self._extracted_data.get("picks_status", "")
        self.players: List[Player] = self._extracted_data.get("players", [])
        self.position_types: List[PositionType] = self._extracted_data.get("position_types", [])
        self.roster_positions: List[RosterPosition] = self._extracted_data.get("roster_positions", [])
        self.scenario_generator: int = self._extracted_data.get("scenario_generator", 0)
        self.season: int = self._extracted_data.get("season", None)
        self.stat_categories: StatCategories = self._extracted_data.get("stat_categories", StatCategories({}))
        self.teams: List[Team] = self._extracted_data.get("teams", [])
        self.type: str = self._extracted_data.get("type", "")
        self.url: str = self._extracted_data.get("url", "")


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
        self.display_name: str = self._extracted_data.get("display_name", "")
        self.end: str = self._extracted_data.get("end", "")
        self.start: str = self._extracted_data.get("start", "")
        self.week: int = self._extracted_data.get("week", None)


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
        self.type: str = self._extracted_data.get("type", "")
        self.display_name: str = self._extracted_data.get("display_name", "")


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
            felo_tier (str): The league fantasy ELO level (Bronze, Silver, Gold, Platinum, Diamond).
            game_code (str): The Yahoo game code ("nfl", "nhl", "nba", "mlb").
            iris_group_chat_id (str | null): The unique IRIS group chat ID for the league.
            is_cash_league (int): Numeric boolean (0 or 1) representing if the league is a Yahoo paid league.
            is_finished (int): Numeric boolean (0 or 1) representing if the league season has completed.
            is_plus_league (int): Numeric boolean (0 or 1) representing if the league has paid for Yahoo Fantasy Plus.
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
            start_date (str): A date string representing the start date of the league (format: "YYYY-MM-DD").
            start_week (int): The number of the first week of the league.
            teams (list[Team]): A list of YFPY Team instances.
            teams_ordered_by_standings (list[Team]): A list of YFPY Team instances ordered by their ranks in the league
                standings.
            transactions (list[Transaction]): A list of YFPY Transaction instances.
            url (str): The direct URL of the league.
            weekly_deadline (str | null): The weekly deadline of the league (if applicable).

        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.allow_add_to_dl_extra_pos: int = self._extracted_data.get("allow_add_to_dl_extra_pos", 0)
        self.current_week: int = self._extracted_data.get("current_week", None)
        self.draft_results: List[DraftResult] = self._extracted_data.get("draft_results", [])
        self.draft_status: str = self._extracted_data.get("draft_status", "")
        self.display_name: str = self._extracted_data.get("display_name", "")
        self.edit_key: int = self._extracted_data.get("edit_key", None)
        self.end_date: str = self._extracted_data.get("end_date", "")
        self.end_week: str = self._extracted_data.get("end_week", None)
        self.entry_fee: str = self._extracted_data.get("entry_fee", "")
        self.felo_tier: str = self._extracted_data.get("felo_tier", "")
        self.game_code: str = self._extracted_data.get("game_code", "")
        self.iris_group_chat_id: str = self._extracted_data.get("iris_group_chat_id", "")
        self.is_cash_league: int = self._extracted_data.get("is_cash_league", 0)
        self.is_finished: int = self._extracted_data.get("is_finished", 0)
        self.is_plus_league: int = self._extracted_data.get("is_plus_league", 0)
        self.is_pro_league: int = self._extracted_data.get("is_pro_league", 0)
        self.league_id: str = self._convert_to_string("league_id")  # convert to string to handle leading zeros
        self.league_key: str = self._extracted_data.get("league_key", "")
        self.league_type: str = self._extracted_data.get("league_type", "")
        self.league_update_timestamp: int = self._extracted_data.get("league_update_timestamp", None)
        self.logo_url: str = self._extracted_data.get("logo_url", "")
        self.name: bytes = self._extracted_data.get("name", "").encode("utf-8")  # support special characters
        self.num_teams: int = self._extracted_data.get("num_teams", 0)
        self.password: str = self._extracted_data.get("password", "")
        self.payment_deadline: str = self._extracted_data.get("payment_deadline", "")
        self.players: List[Player] = self._extracted_data.get("players", [])
        self.renew: str = self._extracted_data.get("renew", "")
        self.renewed: str = self._extracted_data.get("renewed", "")
        self.scoreboard: Scoreboard = self._extracted_data.get("scoreboard", Scoreboard({}))
        self.matchups: List[Matchup] = self._get_nested_value(self.scoreboard, "matchups", [])
        self.scoring_type: str = self._extracted_data.get("scoring_type", "")
        self.season: int = self._extracted_data.get("season", None)
        self.settings: Settings = self._extracted_data.get("settings", Settings({}))
        self.short_invitation_url: str = self._extracted_data.get("short_invitation_url", "")
        self.standings: Standings = self._extracted_data.get("standings", Standings({}))
        self.start_date: str = self._extracted_data.get("start_date", "")
        self.start_week: int = self._extracted_data.get("start_week", None)
        self.teams: List[Team] = self._extracted_data.get("teams", [])
        self.teams_ordered_by_standings: List[Team] = self._get_nested_value(self.standings, "teams", [])
        self.transactions: List[Transaction] = self._extracted_data.get("transactions", [])
        self.url: str = self._extracted_data.get("url", "")
        self.weekly_deadline: str = self._extracted_data.get("weekly_deadline", "")


# noinspection PyUnresolvedReferences
class Team(YahooFantasyObject):
    """Model class for "team" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the Team child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            can_edit_current_week (int): (for Survival Football) Numeric boolean (0 or 1) representing whether the user
                competing in the contest can make changes in the current week.
            champion_pick (str): (for Tourney Pick'em) The selected champion for the contest.
            champion_status (str): (for Tourney Pick'em) The final status of the selected champion for the contest.
            clinched_playoffs (int): Numeric boolean (0 or 1) representing if the team has clinched a playoff berth.
            division_id (int): The unique ID number of the division containing the team (if applicable).
            done_week (str): (might be for Tourney Pick'em or Survival Football) ATTRIBUTE MEANING UNKNOWN.
            draft_grade (str): The letter grade assigned to the draft completed by the team ("A+", "A", ..., "F-").
            draft_position (int): The draft order/position of the team.
            draft_recap_url (str): The direct URL of the draft recap for the team.
            draft_results (list[DraftResult]): A list of YFPY DraftResult instances.
            elimination_week (int): (for Survival Football) Numeric boolean (0 or 1) representing if there is an
                elimination week for the user competing in the contest.
            email_address (str): (for Tourney Pick'em) The email address of the user competing in the contest.
            faab_balance (int): The available balance of FAAB (Free Agent Acquisition Budget) (if applicable).
            has_draft_grade (int): Numeric boolean (0 or 1) representing if the team has a draft grade available.
            is_in_contest (int): (for Survival Football) Numeric boolean (0 or 1) representing if the user is in a
                contest.
            is_owned_by_current_login (int): Numeric boolean (0 or 1) representing if the team is owned by the current
                user authenticated with the Yahoo Fantasy Sports REST API.
            last_editable_week (str): (for Survival Football) String boolean ("True" or "False") representing if it is
                the last editable week for the user competing in the contest.
            league_scoring_type (str): Value designating the type of scoring used by the league ("head" for
                head-to-head, etc.).
            logo_type (str): (for Tourney Pick'em) The team logo type ("avatar", etc.) of the user competing in the
                contest.
            manager (Manager): (for Survival Football) A YFPY Manager instance for the user competing in the contest.
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
            team_logo (str): (for Tourney Pick'em) The direct URL to the team logo of the user competing in the contest.
            team_logos (list[TeamLogo]): A list of YFPY TeamLogo instances.
            team_paid (int): Numeric boolean (0 or 1) representing if the team has paid for Yahoo Fantasy Plus.
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
            status (str): (for Survival Football) The status of user competing in the contest ("dead", etc.).
            streak_type (str): The active team win/loss/tie streak.
            streak_length (int): The length of the streak.
            total_strikes (int): (for Survival Football) The total number of strikes (incorrect selections) made by the
                user competing in the contest.
            url (str): The direct URL to the team.
            user_display_name (str): (for Tourney Pick'em) The display name for the user competing in the contest.
            user_profile_image (str): (for Tourney Pick'em) The direct URL to the profile image of the user competing
                in the contest.
            waiver_priority (int): The waiver priority of the team.
            win_probability (float): The active win probability of the team in its current matchup (ranges from 0.0 to
                1.0).

        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.can_edit_current_week: int = self._extracted_data.get("can_edit_current_week", 0)
        self.champion_pick: str = self._extracted_data.get("champion_pick", "")
        self.champion_status: str = self._extracted_data.get("champion_status", "")
        self.clinched_playoffs: int = self._extracted_data.get("clinched_playoffs", 0)
        self.division_id: int = self._extracted_data.get("division_id", None)
        self.done_week: str = self._extracted_data.get("done_week", None)
        self.draft_grade: str = self._extracted_data.get("draft_grade", "")
        self.draft_position: int = self._extracted_data.get("draft_position", None)
        self.draft_recap_url: str = self._extracted_data.get("draft_recap_url", "")
        self.draft_results: List[DraftResult] = self._extracted_data.get("draft_results", [])
        self.elimination_week: int = self._extracted_data.get("elimination_week", None)
        self.email_address: str = self._extracted_data.get("email_address", "")
        self.faab_balance: int = self._extracted_data.get("faab_balance", None)
        self.has_draft_grade: int = self._extracted_data.get("has_draft_grade", 0)
        self.is_in_contest: int = self._extracted_data.get("is_in_contest", 0)
        self.is_owned_by_current_login: int = self._extracted_data.get("is_owned_by_current_login", 0)
        self.last_editable_week: str = self._extracted_data.get("last_editable_week", "")
        self.league_scoring_type: str = self._extracted_data.get("league_scoring_type", "")
        self.logo_type: str = self._extracted_data.get("logo_type", "")
        self.manager: Manager = self._extracted_data.get("manager", Manager({}))
        self.managers: List[Manager] = self._extracted_data.get("managers", [])
        self.matchups: List[Matchup] = self._extracted_data.get("matchups", [])
        self.name: bytes = self._extracted_data.get("name", "").encode("utf-8")  # support special characters
        self.number_of_moves: int = self._extracted_data.get("number_of_moves", 0)
        self.number_of_trades: int = self._extracted_data.get("number_of_trades", 0)
        self.roster: Roster = self._extracted_data.get("roster", Roster({}))
        self.players: List[Player] = self._get_nested_value(self.roster, "players", [])
        self.roster_adds: RosterAdds = self._extracted_data.get("roster_adds", RosterAdds({}))
        self.roster_adds_value: int = self._get_nested_value(self.roster_adds, "value", 0)
        self.team_id: int = self._extracted_data.get("team_id", None)
        self.team_key: str = self._extracted_data.get("team_key", "")
        self.team_logo: str = self._extracted_data.get("team_logo", "")
        self.team_logos: List[TeamLogo] = self._extracted_data.get("team_logos", [])
        self.team_paid: int = self._extracted_data.get("team_paid", 0)
        self.team_points: TeamPoints = self._extracted_data.get("team_points", TeamPoints({}))
        self.points: float = self._get_nested_value(self.team_points, "total", 0.0, float)
        self.team_projected_points: TeamProjectedPoints = self._extracted_data.get("team_projected_points",
                                                                                   TeamProjectedPoints({}))
        self.projected_points: float = self._get_nested_value(self.team_projected_points, "total", 0.0, float)
        self.team_standings: TeamStandings = self._extracted_data.get("team_standings", TeamStandings({}))
        self.wins: int = self._get_nested_value(self.team_standings, ["outcome_totals", "wins"], 0, int)
        self.losses: int = self._get_nested_value(self.team_standings, ["outcome_totals", "losses"], 0, int)
        self.ties: int = self._get_nested_value(self.team_standings, ["outcome_totals", "ties"], 0, int)
        self.percentage: float = self._get_nested_value(
            self.team_standings, ["outcome_totals", "percentage"], 0.0, float
        )
        self.playoff_seed: int = self._get_nested_value(self.team_standings, "playoff_seed", None, int)
        self.points_against: float = self._get_nested_value(self.team_standings, "points_against", 0.0, float)
        self.points_for: float = self._get_nested_value(self.team_standings, "points_for", 0.0, float)
        self.rank: int = self._get_nested_value(self.team_standings, "rank", None)
        self.status: str = self._extracted_data.get("status", "")
        self.streak_type: str = self._get_nested_value(self.team_standings, ["streak", "type"], "")
        self.streak_length: int = self._get_nested_value(self.team_standings, ["streak", "value"], None, int)
        self.total_strikes: int = self._extracted_data.get("total_strikes", 0)
        self.url: str = self._extracted_data.get("url", "")
        self.user_display_name: str = self._extracted_data.get("user_display_name", "")
        self.user_profile_image: str = self._extracted_data.get("user_profile_image", "")
        self.waiver_priority: int = self._extracted_data.get("waiver_priority", None)
        self.win_probability: float = self._get_nested_value(self._extracted_data, "win_probability", 0.0, float)


# noinspection PyUnresolvedReferences
class DraftResult(YahooFantasyObject):
    """Model class for "draft_result" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the DraftResult child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            cost (int): The player cost (for auction drafts).
            pick (int): The draft pick number.
            round (int): The draft round.
            team_key (str): The Yahoo team key of the team that made the draft pick.
            player_key (str): The Yahoo player key of the player that was drafted.
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.cost: int = self._extracted_data.get("cost", None)
        self.pick: int = self._extracted_data.get("pick", None)
        self.round: int = self._extracted_data.get("round", None)
        self.team_key: str = self._extracted_data.get("team_key", "")
        self.player_key: str = self._extracted_data.get("player_key", "")


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
        self.teams: List[Team] = self._extracted_data.get("teams", [])


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
        self.faab_bid: int = self._extracted_data.get("faab_bid", None)
        self.picks: List[Pick] = self._extracted_data.get("picks", [])
        self.players: List[Player] = self._extracted_data.get("players", [])
        self.status: str = self._extracted_data.get("status", "")
        self.timestamp: int = self._extracted_data.get("timestamp", None)
        self.tradee_team_key: str = self._extracted_data.get("tradee_team_key", "")
        self.tradee_team_name: str = self._extracted_data.get("tradee_team_name", "")
        self.trader_team_key: str = self._extracted_data.get("trader_team_key", "")
        self.trader_team_name: str = self._extracted_data.get("trader_team_name", "")
        self.transaction_id: int = self._extracted_data.get("transaction_id", None)
        self.transaction_key: str = self._extracted_data.get("transaction_key", "")
        self.type: str = self._extracted_data.get("type", "")


# noinspection PyUnresolvedReferences
class Pick(YahooFantasyObject):
    """Model class for "pick" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the Pick child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            destination_team_key (str): Team key in the format <game_key>.l.<league_id>.t.<team_id> of the team
                receiving the pick in the transaction.
            destination_team_name (str): Team name of the team receiving the pick in the transaction.
            original_team_key (str): Team key in the format <game_key>.l.<league_id>.t.<team_id> of the team to which
                the pick in the transaction originally belonged.
            original_team_name (str): Team name of the team to which the pick in the transaction originally belonged.
            round (int): The draft round of the pick in the transaction.
            source_team_key (str): Team key in the format <game_key>.l.<league_id>.t.<team_id> of the team sending the
                pick in the transaction.
            source_team_name (str): Team name of the team sending the pick in the transaction.
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.destination_team_key: str = self._extracted_data.get("destination_team_key", "")
        self.destination_team_name: str = self._extracted_data.get("destination_team_name", "")
        self.original_team_key: str = self._extracted_data.get("original_team_key", "")
        self.original_team_name: str = self._extracted_data.get("original_team_name", "")
        self.round: int = self._extracted_data.get("round", None)
        self.source_team_key: str = self._extracted_data.get("source_team_key", "")
        self.source_team_name: str = self._extracted_data.get("source_team_name", "")


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
            emails (list[str]): (for Survival Football) List of email addresses for the manager competing in the
                contest.
            fantasy_profile_url (str): (for Survival Football) The direct URL for the profile of the manager competing
                in the contest.
            felo_score (int): The manager fantasy ELO rating.
            felo_tier (str): The manager fantasy ELO level (Bronze, Silver, Gold, Platinum, Diamond).
            guid (str): The unique Yahoo GUID of the user account associated with manager.
            image_url (str): The direct URL of the manager profile image.
            is_comanager (int): Numeric boolean (0 or 1) representing if the manager is a co-manager.
            is_commissioner (int): Numeric boolean (0 or 1) representing if the manager is commissioner of the league
                from which the manager data is being retrieved.
            is_current_login (int): Numeric boolean (0 or 1) representing if the manager is the current user
                authenticated with the Yahoo Fantasy Sports REST API.
            manager_id (int): The unique manager ID in the league.
            nickname (str): The display nickname of the manager.
            profile_image_url (str): (for Survival Football) The direct URL of the profile image of the manager
                competing in the contest.
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.email: str = self._extracted_data.get("email", "")
        self.emails: List[str] = self._extracted_data.get("emails", [])
        self.fantasy_profile_url: str = self._extracted_data.get("fantasy_profile_url", "")
        self.felo_score: int = self._extracted_data.get("felo_score", None)
        self.felo_tier: str = self._extracted_data.get("felo_tier", "")
        self.guid: str = self._extracted_data.get("guid", "")
        self.image_url: str = self._extracted_data.get("image_url", "")
        self.is_comanager: int = self._extracted_data.get("is_comanager", 0)
        self.is_commissioner: int = self._extracted_data.get("is_comanager", 0)
        self.is_current_login: int = self._extracted_data.get("is_current_login", 0)
        self.manager_id: int = self._extracted_data.get("manager_id", None)
        self.nickname: str = self._extracted_data.get("nickname", "")
        self.profile_image_url: str = self._extracted_data.get("profile_image_url", "")


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
        self.coverage_type: str = self._extracted_data.get("coverage_type", "")
        self.week: int = self._extracted_data.get("week", None)
        self.is_editable: int = self._extracted_data.get("is_editable", 0)
        self.players: List[Player] = self._extracted_data.get("players", [])


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
        self.coverage_type: str = self._extracted_data.get("coverage_type", "")
        self.coverage_value: int = self._get_nested_value(self._extracted_data, "coverage_value", 0, int)
        self.value: int = self._get_nested_value(self._extracted_data, "value", 0, int)


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
        self.size: str = self._extracted_data.get("size", "")
        self.url: str = self._extracted_data.get("url", "")


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
        self.coverage_type: str = self._extracted_data.get("coverage_type", "")
        self.season: int = self._extracted_data.get("season", None)
        self.total: float = self._get_nested_value(self._extracted_data, "total", 0.0, float)
        self.week: int = self._extracted_data.get("week", None)


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
        self.coverage_type: str = self._extracted_data.get("coverage_type", "")
        self.total: float = self._get_nested_value(self._extracted_data, "total", 0.0, float)
        self.week: int = self._extracted_data.get("week", None)


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
        self.divisional_outcome_totals: DivisionalOutcomeTotals = self._extracted_data.get(
            "divisional_outcome_totals", DivisionalOutcomeTotals({}))
        self.outcome_totals: OutcomeTotals = self._extracted_data.get("outcome_totals", OutcomeTotals({}))
        self.playoff_seed: int = self._extracted_data.get("playoff_seed", 0)
        self.points_against: float = self._get_nested_value(self._extracted_data, "points_against", 0.0, float)
        self.points_for: float = self._get_nested_value(self._extracted_data, "points_for", 0.0, float)
        self.rank: int = self._extracted_data.get("rank", None)
        self.streak: Streak = self._extracted_data.get("streak", Streak({}))


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
        self.losses: int = self._get_nested_value(self._extracted_data, "losses", 0, int)
        self.ties: int = self._get_nested_value(self._extracted_data, "ties", 0, int)
        self.wins: int = self._get_nested_value(self._extracted_data, "wins", 0, int)


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
        self.losses: int = self._get_nested_value(self._extracted_data, "losses", 0, int)
        self.percentage: float = self._get_nested_value(self._extracted_data, "percentage", 0.0, float)
        self.ties: int = self._get_nested_value(self._extracted_data, "ties", 0, int)
        self.wins: int = self._get_nested_value(self._extracted_data, "wins", 0, int)


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
        self.type: str = self._extracted_data.get("type", "")
        self.value: int = self._get_nested_value(self._extracted_data, "value", 0, int)


# noinspection PyUnresolvedReferences
class Scoreboard(YahooFantasyObject):
    """Model class for "scoreboard" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the Scoreboard child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            matchups (list[Matchup]): A list of YFPY Matchup instances representing the matchups for the week.
            week (int): The week for which the scoreboard applies.
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.matchups: List[Matchup] = self._extracted_data.get("matchups", [])
        self.week: int = self._extracted_data.get("week", None)


# noinspection DuplicatedCode, PyUnresolvedReferences
class Settings(YahooFantasyObject):
    """Model class for "settings" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the Settings child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            cant_cut_list (int): Numeric boolean (0 or 1) representing if the league uses the Yahoo "can't cut list".
            divisions (list[Division]): A list of YFPY Division instances for leagues with divisions.
            draft_pick_time (int): The number of seconds allowed to make each draft pick.
            draft_time (int): A timestamp representing when the draft will start.
            draft_together (int): Numeric boolean (0 or 1) representing if the league uses Yahoo Fantasy Draft Together
                live video chat during online drafts.
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
            sendbird_channel_url (str): The in-app Sendbird channel ID.
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
            uses_median_score (int): (for paid subscribers to Yahoo Fantasy Commissioner Plus) Numeric boolean (0 or 1)
                representing if the league plays an extra game against the median each week.
            uses_negative_points (int): Numeric boolean (0 or 1) representing if the league allows negative scoring.
            uses_playoffs (int): Numeric boolean (0 or 1) representing if the league has playoffs.
            uses_playoff_reseeding (int): Numeric boolean (0 or 1) representing if the league reseeds the playoffs once
                the fantasy regular season is complete.
            waiver_rule (str): Value designating when players go to waivers ("gametime", etc.).
            waiver_time (int): The number of days that players remain on waivers.
            waiver_type (str): Value designating what type of waivers are used by the league ("R" for rolling, etc.).
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.cant_cut_list: int = self._extracted_data.get("cant_cut_list", 0)
        self.divisions: List[Division] = self._extracted_data.get("divisions", [])
        self.draft_pick_time: int = self._extracted_data.get("draft_pick_time", None)
        self.draft_time: int = self._extracted_data.get("draft_time", None)
        self.draft_together: int = self._extracted_data.get("draft_together", 0)
        self.draft_type: str = self._extracted_data.get("draft_type", "")
        self.has_multiweek_championship: int = self._extracted_data.get("has_multiweek_championship", 0)
        self.has_playoff_consolation_games: int = self._extracted_data.get("has_playoff_consolation_games", 0)
        self.is_auction_draft: int = self._extracted_data.get("is_auction_draft", 0)
        self.max_teams: int = self._extracted_data.get("max_teams", None)
        self.num_playoff_consolation_teams: int = self._extracted_data.get("num_playoff_consolation_teams", None)
        self.num_playoff_teams: int = self._extracted_data.get("num_playoff_teams", None)
        self.pickem_enabled: int = self._extracted_data.get("pickem_enabled", 0)
        self.player_pool: str = self._extracted_data.get("player_pool", "")
        self.playoff_start_week: int = self._extracted_data.get("playoff_start_week", None)
        self.post_draft_players: str = self._extracted_data.get("post_draft_players", "")
        self.roster_positions: List[RosterPosition] = self._extracted_data.get("roster_positions", [])
        self.scoring_type: str = self._extracted_data.get("scoring_type", "")
        self.sendbird_channel_url: str = self._extracted_data.get("sendbird_channel_url", "")
        self.stat_categories: StatCategories = self._extracted_data.get("stat_categories", StatCategories({}))
        self.stat_modifiers: StatModifiers = self._extracted_data.get("stat_modifiers", StatModifiers({}))
        self.trade_end_date: str = self._extracted_data.get("trade_end_date", "")
        self.trade_ratify_type: str = self._extracted_data.get("trade_ratify_type", "")
        self.trade_reject_time: int = self._extracted_data.get("trade_reject_time", None)
        self.uses_faab: int = self._extracted_data.get("uses_faab", 0)
        self.uses_fractional_points: int = self._extracted_data.get("uses_fractional_points", 0)
        self.uses_lock_eliminated_teams: int = self._extracted_data.get("uses_lock_eliminated_teams", 0)
        self.uses_median_score: int = self._extracted_data.get("uses_median_score", 0)
        self.uses_negative_points: int = self._extracted_data.get("uses_negative_points", 0)
        self.uses_playoff: int = self._extracted_data.get("uses_playoff", 0)
        self.uses_playoff_reseeding: int = self._extracted_data.get("uses_playoff_reseeding", 0)
        self.waiver_rule: str = self._extracted_data.get("waiver_rule", "")
        self.waiver_time: int = self._extracted_data.get("waiver_time", None)
        self.waiver_type: str = self._extracted_data.get("waiver_type", "")


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
        self.division_id: int = self._extracted_data.get("division_id", None)
        self.name: str = self._extracted_data.get("name", "")


# noinspection PyUnresolvedReferences
class RosterPosition(YahooFantasyObject):
    """Model class for "roster_position" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the RosterPosition child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            abbreviation (str): The abbreviated position string.
            count (int): The number of roster slots available for this position.
            display_name (str): The unabbreviated position string.
            is_bench (int): Numeric boolean (0 or 1) representing if the roster position is the bench position.
            is_starting_position (int): Numeric boolean (0 or 1) representing if the roster position is in the starting
                lineup and scores points.
            position (str): The abbreviated position string.
            position_type (str): The position type ("O" for offense, etc.)
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.abbreviation: str = self._extracted_data.get("abbreviation", "")
        self.count: int = self._extracted_data.get("count", 0)
        self.display_name: str = self._extracted_data.get("display_name", "")
        self.is_bench: int = self._extracted_data.get("is_bench", 0)
        self.is_starting_position: int = self._extracted_data.get("is_starting_position", 0)
        self.position: str = self._extracted_data.get("position", "")
        self.position_type: str = self._extracted_data.get("position_type", "")


# noinspection PyUnresolvedReferences
class StatCategories(YahooFantasyObject):
    """Model class for "stat_categories" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the StatCategories child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            groups (list[Group]): A list of YFPY Group instances representing the stat
                categories groups.
            stats (list[Stat]): A list of YFPY Stat instances representing the league stat categories.
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.groups: List[Group] = self._extracted_data.get("groups", [])
        self.stats: List[Stat] = self._extracted_data.get("stats", [])


# noinspection PyUnresolvedReferences
class Group(YahooFantasyObject):
    """Model class for "group" data key in "stat_categories" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the Group child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            group_abbr (str): The abbreviated display name of the stat categories group.
            group_display_name (str): The display name of the stat categories group.
            group_name (str): The name of the stat categories group.
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.group_abbr: str = self._extracted_data.get("group_abbr", "")
        self.group_display_name: str = self._extracted_data.get("group_display_name", "")
        self.group_name: str = self._extracted_data.get("group_name", "")


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
        self.stats: List[Stat] = self._extracted_data.get("stats", [])


# noinspection PyUnresolvedReferences
class Stat(YahooFantasyObject):
    """Model class for "stat" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the Stat child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            abbr (str): The abbreviated display name of the stat.
            bonuses (list[Bonus]): A list of YFPY Bonus instances available for this stat category.
            display_name (str): The display name of the stat.
            enabled (int): Numeric boolean (0 or 1) representing if this stat is enabled for league scoring.
            group (str): The stat category ("misc", "yds_allow", "return", "receiving", "rushing", "passing", etc.)
            is_excluded_from_display (int): Numeric boolean (0 or 1) representing if this stat is not displayed.
            is_only_display_stat (int): Numeric boolean (0 or 1) representing if this stat is only for display.
            name (str): The full name of the stat.
            position_type (str): The player position type eligible for the stat.
            position_types (list[PositionType): A list of YFPY PositionType instances.
            sort_order (int): Numeric boolean (0 or 1) representing if the stat is sorted highest to lowest (1) or
                lowest to highest (0).
            stat_id (int): The unique stat ID number in the league.
            stat_position_types (list[PositionType]): A list of YFPY PositionType instances.
            value (float): The value of the stat (if applicable).
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.abbr: str = self._extracted_data.get("abbr", "")
        self.bonuses: List[Bonus] = self._extracted_data.get("bonuses", [])
        self.display_name: str = self._extracted_data.get("display_name", "")
        self.enabled: int = self._extracted_data.get("enabled", 0)
        self.group: str = self._extracted_data.get("group", "")
        self.is_excluded_from_display: int = self._extracted_data.get("is_excluded_from_display", 0)
        self.is_only_display_stat: int = self._extracted_data.get("is_only_display_stat", 0)
        self.name: str = self._extracted_data.get("name", "")
        self.position_type: str = self._extracted_data.get("position_type", "")
        self.position_types: List[PositionType] = self._extracted_data.get("position_types", [])
        self.sort_order: int = self._extracted_data.get("sort_order", 0)
        self.stat_id: int = self._extracted_data.get("stat_id", None)
        self.stat_position_types: List[PositionType] = self._extracted_data.get("position_types", [])
        self.value: float = self._get_nested_value(self._extracted_data, "value", 0.0, float)


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
        self.is_only_display_stat: int = self._extracted_data.get("is_only_display_stat", 0)
        self.position_type: str = self._extracted_data.get("position_type", "")


# noinspection PyUnresolvedReferences
class Bonus(YahooFantasyObject):
    """Model class for "bonus" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the Bonus child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            points (float): The points awarded when the bonus is won.
            target (int): The stat value target required to be awarded the bonus.
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.points: float = self._get_nested_value(self._extracted_data, "points", 0.0, float)
        self.target: int = self._extracted_data.get("target", None)


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
        self.is_consolation: int = self._extracted_data.get("is_consolation", 0)
        self.is_matchup_recap_available: int = self._extracted_data.get("is_matchup_recap_available", 0)
        self.is_playoffs: int = self._extracted_data.get("is_playoffs", 0)
        self.is_tied: int = self._extracted_data.get("is_tied", 0)
        self.matchup_grades: List[MatchupGrade] = self._extracted_data.get("matchup_grades", [])
        self.matchup_recap_title: str = self._extracted_data.get("matchup_recap_title", "")
        self.matchup_recap_url: str = self._extracted_data.get("matchup_recap_url", "")
        self.status: str = self._extracted_data.get("status", "")
        self.teams: List[Team] = self._extracted_data.get("teams", [])
        self.week: int = self._extracted_data.get("week", None)
        self.week_end: str = self._extracted_data.get("week_end", "")
        self.week_start: str = self._extracted_data.get("week_start", "")
        self.winner_team_key: str = self._extracted_data.get("winner_team_key", "")


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
        self.grade: str = self._extracted_data.get("grade", "")
        self.team_key: str = self._extracted_data.get("team_key", "")


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
            editorial_team_key (str): The Yahoo team key of the professional team for which the player plays using the
                game key.
            editorial_team_url (str): The direct URL of the professional team for which the player plays on Yahoo
                Sports.
            eligible_positions (list[str]): A list of positions for which the player is eligible.
            has_player_notes (int): Numeric boolean (0 or 1) representing if the player has any notes.
            has_recent_player_notes (int): Numeric boolean (0 or 1) representing if the player has any recent notes.
            headshot (Headshot): A YFPY Headshot instance.
            headshot_size (str): The player headshot photo size ("small", "large", etc.)
            headshot_url (str): The direct URL of the player headshot photo.
            image_url (str): The direct URL of the player headshot photo.
            injury_note (str): The physical part of the player that is injured if the player has an injury.
            is_editable (int): Numeric boolean (0 or 1) representing if the player is editable.
            is_keeper (int): Numeric boolean (0 or 1) representing if the player is a keeper.
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
            status (str): The status abbreviation of the player ("IR", "PUP", "O", "Q", etc.).
            status_full (str): The unabbreviated status of the player ("Questionable", etc.).
            transaction_data (TransactionData): A YFPY TransactionData instance.
            uniform_number (int): The uniform number of the player.
            url (str): The direct URL of the player page on Yahoo Sports.
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.bye_weeks: ByeWeeks = self._extracted_data.get("bye_weeks", ByeWeeks({}))
        self.bye: int = self._get_nested_value(self.bye_weeks, "week", None, int)
        self.display_position: str = self._extracted_data.get("display_position", "")
        self.draft_analysis: DraftAnalysis = self._extracted_data.get("draft_analysis", DraftAnalysis({}))
        self.average_draft_pick: float = self._get_nested_value(self.draft_analysis, "average_pick", None, float)
        self.average_draft_round: float = self._get_nested_value(self.draft_analysis, "average_round", None, float)
        self.average_draft_cost: float = self._get_nested_value(self.draft_analysis, "average_cost", None, float)
        self.percent_drafted: float = self._get_nested_value(self.draft_analysis, "percent_drafted", None, float)
        self.editorial_player_key: str = self._extracted_data.get("editorial_player_key", "")
        self.editorial_team_abbr: str = self._extracted_data.get("editorial_team_abbr", "")
        self.editorial_team_full_name: str = self._extracted_data.get("editorial_team_full_name", "")
        self.editorial_team_key: str = self._extracted_data.get("editorial_team_key", "")
        self.editorial_team_url: str = self._extracted_data.get("editorial_team_url", "")
        eligible_positions = self._extracted_data.get("eligible_positions")
        self.eligible_positions: List[str] = []
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
        self.has_player_notes: int = self._extracted_data.get("has_player_notes", 0)
        self.has_recent_player_notes: int = self._extracted_data.get("has_recent_player_notes", 0)
        self.headshot: Headshot = self._extracted_data.get("headshot", Headshot({}))
        self.headshot_size: str = self._get_nested_value(self.headshot, "size", "")
        self.headshot_url: str = self._get_nested_value(self.headshot, "url", "")
        self.image_url: str = self._extracted_data.get("image_url", "")
        self.injury_note: str = self._extracted_data.get("injury_note", "")
        self.is_editable: int = self._extracted_data.get("is_editable", 0)
        self.is_keeper: int = self._extracted_data.get("is_keeper", 0)
        self.is_undroppable: int = self._extracted_data.get("is_undroppable", 0)
        self.name: Name = self._extracted_data.get("name", Name({}))
        self.first_name: str = self._get_nested_value(self.name, "first", "")
        self.last_name: str = self._get_nested_value(self.name, "last", "")
        self.full_name: str = self._get_nested_value(self.name, "full", "")
        self.ownership: Ownership = self._extracted_data.get("ownership", Ownership({}))
        self.percent_owned: PercentOwned = self._extracted_data.get("percent_owned", PercentOwned({}))
        self.percent_owned_value: float = self._get_nested_value(self.percent_owned, "value", 0.0, float)
        self.player_advanced_stats: PlayerAdvancedStats = self._extracted_data.get("player_advanced_stats",
                                                                                   PlayerAdvancedStats({}))
        self.player_id: int = self._extracted_data.get("player_id", None)
        self.player_key: str = self._extracted_data.get("player_key", "")
        self.player_notes_last_timestamp: int = self._extracted_data.get("player_notes_last_timestamp", None)
        self.player_points: PlayerPoints = self._extracted_data.get("player_points", PlayerPoints({}))
        self.player_points_value: float = self._get_nested_value(self.player_points, "total", 0.0, float)
        self.player_stats: PlayerStats = self._extracted_data.get("player_stats", PlayerStats({}))
        self.stats: List[Stat] = self._get_nested_value(self.player_stats, "stats", [])
        self.position_type: str = self._extracted_data.get("position_type", "")
        self.primary_position: str = self._extracted_data.get("primary_position", "")
        self.selected_position: SelectedPosition = self._extracted_data.get("selected_position",
                                                                            SelectedPosition({}))
        self.selected_position_value: str = self._get_nested_value(self.selected_position, "position", "")
        self.status: str = self._extracted_data.get("status", "")
        self.status_full: str = self._extracted_data.get("status_full", "")
        self.transaction_data: TransactionData = self._extracted_data.get("transaction_data",
                                                                          TransactionData({}))
        self.uniform_number: int = self._extracted_data.get("uniform_number", None)
        self.url: str = self._extracted_data.get("url", "")


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
        self.week: int = self._extracted_data.get("week", None)


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
            preseason_average_cost (float): The average price paid for the player to be drafted in the preseason.
            preseason_average_pick (float): The average pick at which the player was drafted in the preseason.
            preseason_average_round (float): The average round in which the player was drafted in the preseason.
            preseason_percent_drafted (float): The overall percentage the player was drafted in the preseason.
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.average_pick: float = self._get_nested_value(self._extracted_data, "average_pick", 0.0, float)
        self.average_round: float = self._get_nested_value(self._extracted_data, "average_round", 0.0, float)
        self.average_cost: float = self._get_nested_value(self._extracted_data, "average_cost", 0.0, float)
        self.percent_drafted: float = self._get_nested_value(self._extracted_data, "percent_drafted", 0.0, float)
        self.preseason_average_cost: float = self._get_nested_value(
            self._extracted_data, "preseason_average_cost", 0.0, float
        )
        self.preseason_average_pick: float = self._get_nested_value(
            self._extracted_data, "preseason_average_pick", 0.0, float
        )
        self.preseason_average_round: float = self._get_nested_value(
            self._extracted_data, "preseason_average_round", 0.0, float
        )
        self.preseason_percent_drafted: float = self._get_nested_value(
            self._extracted_data, "preseason_percent_drafted", 0.0, float
        )


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
        self.size: str = self._extracted_data.get("size", "")
        self.url: str = self._extracted_data.get("url", "")


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
        self.ascii_first: str = self._extracted_data.get("ascii_first", "")
        self.ascii_last: str = self._extracted_data.get("ascii_last", "")
        self.first: str = self._extracted_data.get("first", "")
        self.full: str = self._extracted_data.get("full", "")
        self.last: str = self._extracted_data.get("last", "")


# noinspection PyUnresolvedReferences
class Ownership(YahooFantasyObject):
    """Model class for "ownership" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the Ownership child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            display_date (int): The week number the player went on waivers (when applicable).
            ownership_type (str): The current location of the player in the league ("team", "waivers", etc.).
            owner_team_key (str): The Yahoo team key for the team that owns the player.
            owner_team_name (str): The team name for the team that owns the player.
            teams (list[Team]): A list of YFPY Team instances.
            waiver_date (str): The date the player went on waivers (when applicable).
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.display_date: int = self._extracted_data.get("display_date", None)
        self.ownership_type: str = self._extracted_data.get("ownership_type", "")
        self.owner_team_key: str = self._extracted_data.get("owner_team_key", "")
        self.owner_team_name: str = self._extracted_data.get("owner_team_name", "")
        self.teams: List[Team] = self._extracted_data.get("teams", [])
        self.waiver_date: str = self._extracted_data.get("waiver_date", "")


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
        self.coverage_type: str = self._extracted_data.get("coverage_type", "")
        self.week: int = self._extracted_data.get("week", None)
        self.value: int = self._get_nested_value(self._extracted_data, "value", 0, int)
        self.delta: float = self._get_nested_value(self._extracted_data, "delta", 0.0, float)


# noinspection PyUnresolvedReferences
class PlayerAdvancedStats(YahooFantasyObject):
    """Model class for "player_advanced_stats" data key.
    """

    def __init__(self, extracted_data):
        """Instantiate the PlayerAdvancedStats child class of YahooFantasyObject.

        Args:
            extracted_data (dict): Parsed and cleaned JSON data retrieved from the Yahoo Fantasy Sports REST API.

        Attributes:
            coverage_type (str): The timeframe for the selected player advanced stats ("week", "date", "season", etc.).
            season (int): The season year (when applicable).
            stats (list[Stat]): A list of advanced YFPY Stat instances for the player.
            week (int): The week number (when applicable).
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.coverage_type: str = self._extracted_data.get("coverage_type", "")
        self.season: int = self._extracted_data.get("season", None)
        self.stats: List[Stat] = self._extracted_data.get("stats", [])
        self.week: int = self._extracted_data.get("week", None)


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
            season (int): The season year (when applicable).
            total (float): The total points for the player within the coverage timeframe.
            week (int): The week number (when applicable).
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.coverage_type: str = self._extracted_data.get("coverage_type", "")
        self.season: int = self._extracted_data.get("season", None)
        self.total: float = self._get_nested_value(self._extracted_data, "total", 0.0, float)
        self.week: int = self._extracted_data.get("week", None)


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
            date (str): The YYYY-MM-DD formatted date string (when applicable).
            season (int): The season year (when applicable).
            stats (list[Stat]): A list of YFPY Stat instances for the player.
            week (int): The week number (when applicable).
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.coverage_type: str = self._extracted_data.get("coverage_type", "")
        self.date: str = self._extracted_data.get("date", "")
        self.season: int = self._extracted_data.get("season", None)
        self.stats: List[Stat] = self._extracted_data.get("stats", [])
        self.week: int = self._extracted_data.get("week", None)


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
            date (str): The YYYY-MM-DD formatted date string (when applicable).
            is_flex (int): Numeric boolean (0 or 1) representing if the selected player is in a flex roster slot.
            position (str): The selected position of the player.
            week (int): The week number (when applicable).
        """
        YahooFantasyObject.__init__(self, extracted_data)
        self.coverage_type: str = self._extracted_data.get("coverage_type", "")
        self.date: str = self._extracted_data.get("date", "")
        self.is_flex: int = self._extracted_data.get("is_flex", 0)
        self.position: str = self._extracted_data.get("position", "")
        self.week: int = self._extracted_data.get("week", None)


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
        self.destination_team_key: str = self._extracted_data.get("destination_team_key", "")
        self.destination_team_name: str = self._extracted_data.get("destination_team_name", "")
        self.destination_type: str = self._extracted_data.get("destination_type", "")
        self.source_team_key: str = self._extracted_data.get("source_team_key", "")
        self.source_team_name: str = self._extracted_data.get("source_team_name", "")
        self.source_type: str = self._extracted_data.get("source_type", "")
        self.type: str = self._extracted_data.get("type", "")
