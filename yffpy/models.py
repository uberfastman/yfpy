__author__ = "Wren J. R. (uberfastman)"
__email__ = "wrenjr@yahoo.com"

import json
import logging

import stringcase

from yffpy.utils import complex_json_handler, flatten_to_objects

logger = logging.getLogger(__name__)


class YahooFantasyObject(object):
    """Base Yahoo fantasy football data object.
    """

    def __init__(self, extracted_data):
        """Instantiate a Yahoo fantasy football object.

        :param extracted_data: parsed and cleaned data retrieved from Yahoo fantasy football API
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

    def _equality_field_dict(self):
        return {k: v for k, v in self.__dict__.items() if k not in ["extracted_data", "_index", "_keys"]}

    def subclass_dict(self):
        """Derive snake case dict keys from custom object type camel case class names.

        :return: dict with snake case strings of all subclasses of YahooFantasyObject as keys and subclasses as values
        """
        return {stringcase.snakecase(cls.__name__): cls for cls in self.__class__.__mro__[-2].__subclasses__()}

    def clean_data_dict(self):
        """Recursive method to un-type custom class type objects for serialization.

        :return: dictionary that extracts serializable data from custom objects
        """
        clean_dict = {}
        for k, v in self.__dict__.items():
            if k in self._keys:
                clean_dict[k] = v.clean_data_dict() if type(v) in self.subclass_dict().values() else v
        return clean_dict

    def serialized(self):
        """Pack up all object content into nested dictionaries for json serialization.

        :return: serializable dictionary
        """
        serializable_dict = dict()
        for a, v in self.clean_data_dict().items():
            if hasattr(v, "serialized"):
                serializable_dict[a] = v.serialized()
            else:
                serializable_dict[a] = v
        return serializable_dict

    def to_json(self):
        """Serialize the class object to json.

        :return: json string derived from the serializable version of the class object
        """
        return json.dumps(self.serialized(), indent=2, default=complex_json_handler, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_data: dict):
        return cls(json_data)


class User(YahooFantasyObject):
    """Yahoo fantasy football object for "user" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.games = self.extracted_data.get("games", [])
        self.guid = self.extracted_data.get("guid", "")


class Game(YahooFantasyObject):
    """Yahoo fantasy football object for "game" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.code = self.extracted_data.get("code", "")
        self.game_id = self.extracted_data.get("game_id", "")
        self.game_key = self.extracted_data.get("game_key", "")
        self.game_weeks = self.extracted_data.get("game_weeks", "")
        self.is_game_over = self.extracted_data.get("is_game_over", "")
        self.is_live_draft_lobby_active = self.extracted_data.get("is_live_draft_lobby_active", "")
        self.is_offseason = self.extracted_data.get("is_offseason", "")
        self.is_registration_over = self.extracted_data.get("is_registration_over", "")
        self.leagues = self.extracted_data.get("leagues", [])
        self.name = self.extracted_data.get("name", "")
        self.position_types = self.extracted_data.get("position_types", [])
        self.roster_positions = self.extracted_data.get("roster_positions", [])
        self.season = self.extracted_data.get("season", "")
        self.stat_categories = self.extracted_data.get("stat_categories", StatCategories({}))  # type: StatCategories
        self.teams = self.extracted_data.get("teams", [])
        self.type = self.extracted_data.get("type", "")
        self.url = self.extracted_data.get("url", "")


class GameWeek(YahooFantasyObject):
    """Yahoo fantasy football object for "game_week" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.display_name = self.extracted_data.get("display_name", "")
        self.end = self.extracted_data.get("end", "")
        self.start = self.extracted_data.get("start", "")
        self.week = self.extracted_data.get("week", "")


class PositionType(YahooFantasyObject):
    """Yahoo fantasy football object for "position_type" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.type = self.extracted_data.get("type", "")
        self.display_name = self.extracted_data.get("display_name", "")


class League(YahooFantasyObject):
    """Yahoo fantasy football object for "league" data key.
    """
    def __init__(self, extracted_data):
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
        self.league_id = self.extracted_data.get("league_id", "")
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
        self.season = self.extracted_data.get("season", "")
        self.settings = self.extracted_data.get("settings", Settings({}))  # type: Settings
        self.short_invitation_url = self.extracted_data.get("short_invitation_url", "")
        self.standings = self.extracted_data.get("standings", Standings({}))  # type: Standings
        self.teams_ordered_by_standings = self.standings.teams
        self.start_date = self.extracted_data.get("start_date", "")
        self.start_week = self.extracted_data.get("start_week", "")
        self.transactions = self.extracted_data.get("transactions", "")
        self.url = self.extracted_data.get("url", "")
        self.weekly_deadline = self.extracted_data.get("weekly_deadline", "")


class Team(YahooFantasyObject):
    """Yahoo fantasy football object for "team" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.clinched_playoffs = self.extracted_data.get("clinched_playoffs", "")
        self.division_id = self.extracted_data.get("division_id")
        self.draft_grade = self.extracted_data.get("draft_grade", "")
        self.draft_position = self.extracted_data.get("draft_position", "")
        self.draft_recap_url = self.extracted_data.get("draft_recap_url", "")
        self.draft_results = self.extracted_data.get("draft_results", "")
        self.faab_balance = self.extracted_data.get("faab_balance", "")
        self.has_draft_grade = self.extracted_data.get("has_draft_grade", "")
        self.league_scoring_type = self.extracted_data.get("league_scoring_type", "")
        self.managers = self.extracted_data.get("managers", "")
        self.matchups = self.extracted_data.get("matchups", "")
        self.name = self.extracted_data.get("name", "").encode("utf-8")
        self.number_of_moves = self.extracted_data.get("number_of_moves", "")
        self.number_of_trades = self.extracted_data.get("number_of_trades", "")
        self.roster = self.extracted_data.get("roster", Roster({}))  # type: Roster
        self.players = self.roster.players
        self.roster_adds = self.extracted_data.get("roster_adds", RosterAdds({}))  # type: RosterAdds
        self.roster_adds_value = self.roster_adds.value
        self.team_id = self.extracted_data.get("team_id", "")
        self.team_key = self.extracted_data.get("team_key", "")
        self.team_logos = self.extracted_data.get("team_logos", "")
        self.team_points = self.extracted_data.get("team_points", TeamPoints({}))  # type: TeamPoints
        self.points = float(self.team_points.total)
        self.team_projected_points = self.extracted_data.get("team_projected_points",
                                                             TeamProjectedPoints({}))  # type: TeamProjectedPoints
        self.projected_points = float(self.team_projected_points.total)
        self.team_standings = self.extracted_data.get("team_standings", TeamStandings({}))  # type: TeamStandings
        self.wins = int(self.team_standings.outcome_totals.wins)
        self.losses = int(self.team_standings.outcome_totals.losses)
        self.ties = int(self.team_standings.outcome_totals.ties)
        self.percentage = float(self.team_standings.outcome_totals.percentage)
        self.playoff_seed = self.team_standings.playoff_seed
        self.points_against = self.team_standings.points_against
        self.points_for = self.team_standings.points_for
        self.rank = self.team_standings.rank
        self.streak_type = self.team_standings.streak.type
        self.streak_length = self.team_standings.streak.value
        self.url = self.extracted_data.get("url", "")
        self.waiver_priority = self.extracted_data.get("waiver_priority", "")
        self.win_probability = self.extracted_data.get("win_probability", "")


class DraftResult(YahooFantasyObject):
    """Yahoo fantasy football object for "draft_result" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.pick = self.extracted_data.get("pick", "")
        self.round = self.extracted_data.get("round", "")
        self.team_key = self.extracted_data.get("team_key", "")
        self.player_key = self.extracted_data.get("player_key", "")


class Standings(YahooFantasyObject):
    """Yahoo fantasy football object for "standings" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.teams = self.extracted_data.get("teams", "")


class Transaction(YahooFantasyObject):
    """Yahoo fantasy football object for "transaction" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.players = self.extracted_data.get("players", "")
        self.status = self.extracted_data.get("status", "")
        self.timestamp = self.extracted_data.get("timestamp", "")
        self.transaction_id = self.extracted_data.get("transaction_id", "")
        self.transaction_key = self.extracted_data.get("transaction_key", "")
        self.type = self.extracted_data.get("type", "")


class Manager(YahooFantasyObject):
    """Yahoo fantasy football object for "manager" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.email = self.extracted_data.get("email", "")
        self.guid = self.extracted_data.get("guid", "")
        self.image_url = self.extracted_data.get("image_url", "")
        self.is_comanager = self.extracted_data.get("is_comanager", "")
        self.manager_id = self.extracted_data.get("manager_id", "")
        self.nickname = self.extracted_data.get("nickname", "")


class Roster(YahooFantasyObject):
    """Yahoo fantasy football object for "roster" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.coverage_type = self.extracted_data.get("coverage_type", "")
        self.week = self.extracted_data.get("week", "")
        self.is_editable = self.extracted_data.get("is_editable", "")
        self.players = self.extracted_data.get("players", "")


class RosterAdds(YahooFantasyObject):
    """Yahoo fantasy football object for "roster_adds" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.coverage_type = self.extracted_data.get("coverage_type", "")
        self.coverage_value = self.extracted_data.get("coverage_value", "")
        self.value = self.extracted_data.get("value", 0)


class TeamLogo(YahooFantasyObject):
    """Yahoo fantasy football object for "team_logo" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.size = self.extracted_data.get("size", "")
        self.url = self.extracted_data.get("url", "")


class TeamPoints(YahooFantasyObject):
    """Yahoo fantasy football object for "team_points" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.coverage_type = self.extracted_data.get("coverage_type", "")
        self.season = self.extracted_data.get("season", "")
        self.total = self.extracted_data.get("total", 0)
        self.week = self.extracted_data.get("week", "")


class TeamProjectedPoints(YahooFantasyObject):
    """Yahoo fantasy football object for "team_projected_points" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.coverage_type = self.extracted_data.get("coverage_type", "")
        self.total = self.extracted_data.get("total", 0)
        self.week = self.extracted_data.get("week", "")


class TeamStandings(YahooFantasyObject):
    """Yahoo fantasy football object for "team_standings" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.divisional_outcome_totals = self.extracted_data.get(
            "divisional_outcome_totals", DivisionalOutcomeTotals({}))  # type: DivisionalOutcomeTotals
        self.outcome_totals = self.extracted_data.get("outcome_totals", OutcomeTotals({}))  # type: OutcomeTotals
        self.playoff_seed = self.extracted_data.get("playoff_seed", 0)
        self.points_against = float(self.extracted_data.get("points_against", 0) or 0)
        self.points_for = float(self.extracted_data.get("points_for", 0) or 0)
        self.rank = self.extracted_data.get("rank", 0)
        self.streak = self.extracted_data.get("streak", Streak({}))  # type: Streak


class DivisionalOutcomeTotals(YahooFantasyObject):
    """Yahoo fantasy football object for "divisional_outcome_totals" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.losses = int(self.extracted_data.get("losses", 0) or 0)
        self.ties = int(self.extracted_data.get("ties", 0) or 0)
        self.wins = int(self.extracted_data.get("wins", 0) or 0)


class OutcomeTotals(YahooFantasyObject):
    """Yahoo fantasy football object for "outcome_totals" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.losses = int(self.extracted_data.get("losses", 0) or 0)
        self.percentage = float(self.extracted_data.get("percentage", 0) or 0)
        self.ties = int(self.extracted_data.get("ties", 0) or 0)
        self.wins = int(self.extracted_data.get("wins", 0) or 0)


class Streak(YahooFantasyObject):
    """Yahoo fantasy football object for "streak" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.type = self.extracted_data.get("type", "")
        self.value = self.extracted_data.get("value", "")


class Scoreboard(YahooFantasyObject):
    """Yahoo fantasy football object for "scoreboard" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.week = self.extracted_data.get("week", "")
        self.matchups = self.extracted_data.get("matchups", [])


class Settings(YahooFantasyObject):
    """Yahoo fantasy football object for "settings" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.cant_cut_list = self.extracted_data.get("cant_cut_list", "")
        self.divisions = self.extracted_data.get("divisions", "")
        self.draft_pick_time = self.extracted_data.get("draft_pick_time", "")
        self.draft_time = self.extracted_data.get("draft_time", "")
        self.draft_type = self.extracted_data.get("draft_type", "")
        self.has_multiweek_championship = self.extracted_data.get("has_multiweek_championship", "")
        self.has_playoff_consolation_games = self.extracted_data.get("has_playoff_consolation_games", "")
        self.is_auction_draft = self.extracted_data.get("is_auction_draft", "")
        self.max_teams = self.extracted_data.get("max_teams", "")
        self.num_playoff_consolation_teams = self.extracted_data.get("num_playoff_consolation_teams", "")
        self.num_playoff_teams = self.extracted_data.get("num_playoff_teams", "")
        self.pickem_enabled = self.extracted_data.get("pickem_enabled", "")
        self.player_pool = self.extracted_data.get("player_pool", "")
        self.playoff_start_week = self.extracted_data.get("playoff_start_week", "")
        self.post_draft_players = self.extracted_data.get("post_draft_players", "")
        self.roster_positions = self.extracted_data.get("roster_positions", "")
        self.scoring_type = self.extracted_data.get("scoring_type", "")
        self.stat_categories = self.extracted_data.get("stat_categories", StatCategories({}))  # type: StatCategories
        self.stat_modifiers = self.extracted_data.get("stat_modifiers", StatModifiers({}))  # type: StatModifiers
        self.trade_end_date = self.extracted_data.get("trade_end_date", "")
        self.trade_ratify_type = self.extracted_data.get("trade_ratify_type", "")
        self.trade_reject_time = self.extracted_data.get("trade_reject_time", "")
        self.uses_faab = self.extracted_data.get("uses_faab", "")
        self.uses_fractional_points = self.extracted_data.get("uses_fractional_points", "")
        self.uses_lock_eliminated_teams = self.extracted_data.get("uses_lock_eliminated_teams", "")
        self.uses_negative_points = self.extracted_data.get("uses_negative_points", "")
        self.uses_playoff = self.extracted_data.get("uses_playoff", "")
        self.uses_playoff_reseeding = self.extracted_data.get("uses_playoff_reseeding", "")
        self.waiver_rule = self.extracted_data.get("waiver_rule", "")
        self.waiver_time = self.extracted_data.get("waiver_time", "")
        self.waiver_type = self.extracted_data.get("waiver_type", "")


class Division(YahooFantasyObject):
    """Yahoo fantasy football object for "division" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.division_id = self.extracted_data.get("division_id", "")
        self.name = self.extracted_data.get("name", "")


class RosterPosition(YahooFantasyObject):
    """Yahoo fantasy football object for "roster_position" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.count = self.extracted_data.get("count", "")
        self.position = self.extracted_data.get("position", "")
        self.position_type = self.extracted_data.get("position_type", "")


class StatCategories(YahooFantasyObject):
    """Yahoo fantasy football object for "stat_categories" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.stats = self.extracted_data.get("stats", "")


class StatModifiers(YahooFantasyObject):
    """Yahoo fantasy football object for "stat_modifiers" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.stats = self.extracted_data.get("stats", "")


class Stat(YahooFantasyObject):
    """Yahoo fantasy football object for "stat" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.bonuses = self.extracted_data.get("bonuses", {})
        self.display_name = self.extracted_data.get("display_name", "")
        self.enabled = self.extracted_data.get("enabled", "")
        self.name = self.extracted_data.get("name", "")
        self.position_type = self.extracted_data.get("position_type", "")
        self.sort_order = self.extracted_data.get("sort_order", "")
        self.stat_id = self.extracted_data.get("stat_id", "")
        self.stat_position_types = self.extracted_data.get("stat_position_types", [])
        self.value = self.extracted_data.get("value", "")


class StatPositionType(YahooFantasyObject):
    """Yahoo fantasy football object for "stat_position_type" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.is_only_display_stat = self.extracted_data.get("is_only_display_stat", "")
        self.position_type = self.extracted_data.get("position_type", "")


class Bonus(YahooFantasyObject):
    """Yahoo fantasy football object for "bonus" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.points = self.extracted_data.get("points", 0)
        self.target = self.extracted_data.get("target", "")


class Matchup(YahooFantasyObject):
    """Yahoo fantasy football object for "matchup" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.matchup = self.extracted_data.get("matchup", "")
        self.is_consolation = self.extracted_data.get("is_consolation", "")
        self.is_matchup_recap_available = self.extracted_data.get("is_matchup_recap_available", "")
        self.is_playoffs = self.extracted_data.get("is_playoffs", "")
        self.is_tied = self.extracted_data.get("is_tied", "")
        self.matchup_grades = self.extracted_data.get("matchup_grades", "")
        self.matchup_recap_title = self.extracted_data.get("matchup_recap_title", "")
        self.matchup_recap_url = self.extracted_data.get("matchup_recap_url", "")
        self.status = self.extracted_data.get("status", "")
        self.teams = self.extracted_data.get("teams", "")
        self.week = self.extracted_data.get("week", "")
        self.week_end = self.extracted_data.get("week_end", "")
        self.week_start = self.extracted_data.get("week_start", "")
        self.winner_team_key = self.extracted_data.get("winner_team_key", "")


class MatchupGrade(YahooFantasyObject):
    """Yahoo fantasy football object for "matchup_grade" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.grade = self.extracted_data.get("grade", "")
        self.team_key = self.extracted_data.get("team_key", "")


class Player(YahooFantasyObject):
    """Yahoo fantasy football object for "player" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.bye_weeks = self.extracted_data.get("bye_weeks", ByeWeeks({}))  # type: ByeWeeks
        self.bye = self.bye_weeks.week
        self.display_position = self.extracted_data.get("display_position", "")
        self.draft_analysis = self.extracted_data.get("draft_analysis", DraftAnalysis({}))  # type: DraftAnalysis
        self.average_draft_pick = self.draft_analysis.average_pick
        self.average_draft_round = self.draft_analysis.average_round
        self.average_draft_cost = self.draft_analysis.average_cost
        self.percent_drafted = self.draft_analysis.percent_drafted
        self.editorial_player_key = self.extracted_data.get("editorial_player_key", "")
        self.editorial_team_abbr = self.extracted_data.get("editorial_team_abbr", "")
        self.editorial_team_full_name = self.extracted_data.get("editorial_team_full_name", "")
        self.editorial_team_key = self.extracted_data.get("editorial_team_key", "")
        self.eligible_positions = self.extracted_data.get("eligible_positions", "")
        self.has_player_notes = self.extracted_data.get("has_player_notes", "")
        self.headshot = self.extracted_data.get("headshot", Headshot({}))  # type: Headshot
        self.headshot_size = self.headshot.size
        self.headshot_url = self.headshot.url
        self.is_editable = self.extracted_data.get("is_editable", "")
        self.is_undroppable = self.extracted_data.get("is_undroppable", "")
        self.name = self.extracted_data.get("name", Name({}))  # type: Name
        self.first_name = self.name.first
        self.last_name = self.name.last
        self.full_name = self.name.full
        self.ownership = self.extracted_data.get("ownership", Ownership({}))  # type: Ownership
        self.percent_owned = self.extracted_data.get("percent_owned", PercentOwned({}))  # type: PercentOwned
        self.percent_owned_value = self.percent_owned.value
        self.player_id = self.extracted_data.get("player_id", "")
        self.player_key = self.extracted_data.get("player_key", "")
        self.player_notes_last_timestamp = self.extracted_data.get("player_notes_last_timestamp", "")
        self.player_points = self.extracted_data.get("player_points", PlayerPoints({}))  # type: PlayerPoints
        self.player_points_value = self.player_points.total
        self.player_stats = self.extracted_data.get("player_stats", PlayerStats({}))  # type: PlayerStats
        self.stats = self.player_stats.stats
        self.position_type = self.extracted_data.get("position_type", "")
        self.primary_position = self.extracted_data.get("primary_position", "")
        self.selected_position = self.extracted_data.get("selected_position",
                                                         SelectedPosition({}))  # type: SelectedPosition
        self.selected_position_value = self.selected_position.position
        self.status = self.extracted_data.get("status", "")
        self.uniform_number = self.extracted_data.get("uniform_number", "")


class ByeWeeks(YahooFantasyObject):
    """Yahoo fantasy football object for "bye_weeks" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.week = self.extracted_data.get("week", "")


class DraftAnalysis(YahooFantasyObject):
    """Yahoo fantasy football object for "draft_analysis" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.average_pick = self.extracted_data.get("average_pick", "")
        self.average_round = self.extracted_data.get("average_round", "")
        self.average_cost = self.extracted_data.get("average_cost", "")
        self.percent_drafted = self.extracted_data.get("percent_drafted", "")


class Headshot(YahooFantasyObject):
    """Yahoo fantasy football object for "headshot" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.size = self.extracted_data.get("size", "")
        self.url = self.extracted_data.get("url", "")


class Name(YahooFantasyObject):
    """Yahoo fantasy football object for "name" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.ascii_first = self.extracted_data.get("ascii_first", "")
        self.ascii_last = self.extracted_data.get("ascii_last", "")
        self.first = self.extracted_data.get("first", "")
        self.full = self.extracted_data.get("full", "")
        self.last = self.extracted_data.get("last", "")


class Ownership(YahooFantasyObject):
    """Yahoo fantasy football object for "ownership" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.ownership_type = self.extracted_data.get("ownership_type", "")
        self.owner_team_key = self.extracted_data.get("owner_team_key", "")
        self.owner_team_name = self.extracted_data.get("owner_team_name", "")
        self.teams = self.extracted_data.get("teams", "")


class PercentOwned(YahooFantasyObject):
    """Yahoo fantasy football object for "percent_owned" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.coverage_type = self.extracted_data.get("coverage_type", "")
        self.week = self.extracted_data.get("week", "")
        self.value = self.extracted_data.get("value", "")
        self.delta = self.extracted_data.get("delta", "")


class PlayerPoints(YahooFantasyObject):
    """Yahoo fantasy football object for "player_points" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.coverage_type = self.extracted_data.get("coverage_type", "")
        self.week = self.extracted_data.get("week", "")
        self.total = float(self.extracted_data.get("total", 0) or 0)


class PlayerStats(YahooFantasyObject):
    """Yahoo fantasy football object for "player_stats" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.coverage_type = self.extracted_data.get("coverage_type", "")
        self.week = self.extracted_data.get("week", "")
        self.stats = self.extracted_data.get("stats", "")


class SelectedPosition(YahooFantasyObject):
    """Yahoo fantasy football object for "selected_position" data key.
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.coverage_type = self.extracted_data.get("coverage_type", "")
        self.is_flex = self.extracted_data.get("is_flex", "")
        self.position = self.extracted_data.get("position", "")
        self.week = self.extracted_data.get("week", "")
