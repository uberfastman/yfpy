import json
import logging

import stringcase

from yffpy.utils import complex_json_handler

logger = logging.getLogger(__name__)


class YahooFantasyObject(object):

    def __init__(self, extracted_data):
        self.extracted_data = extracted_data
        self._index = 0
        if isinstance(extracted_data, dict):
            self._keys = list(self.extracted_data.keys())

    def __str__(self):
        # return json.load({self.__class__.__module__ + "." + self.__class__.__qualname__: self.to_json()})
        return self.to_json()

    def __repr__(self):
        # return json.load({self.__class__.__module__ + "." + self.__class__.__qualname__: self.to_json()})
        return self.to_json()

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

    def subclass_dict(self):
        return {stringcase.snakecase(cls.__name__): cls for cls in self.__class__.__subclasses__()}

    def clean_data_dict(self):
        clean_dict = {}
        for k, v in self.__dict__.items():
            if k in self._keys:
                clean_dict[k] = v.clean_data_dict() if type(v) in self.subclass_dict().values() else v
        return clean_dict

    def serialized(self):
        serializable_dict = dict()
        for a, v in self.clean_data_dict().items():
            if hasattr(v, "serialized"):
                serializable_dict[a] = v.serialized()
            else:
                serializable_dict[a] = v
        return serializable_dict

    def to_json(self):
        return json.dumps(self.serialized(), indent=2, default=complex_json_handler, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_data: dict):
        # return cls(**json_data)
        return cls(json_data)


# class YahooFantasyObjectParent(YahooFantasyObject):
#
#     def __init__(self, extracted_data):
#         YahooFantasyObject.__init__(self, extracted_data)
#         self.copyright = self.extracted_data.get("copyright", "")
#         self.league = self.extracted_data.get("league", "")  # type: League
#         self.refresh_rate = self.extracted_data.get("refresh_rate", "")
#         self.time = self.extracted_data.get("time", "")
#         self.xml_lang = self.extracted_data.get("xml:lang", "")
#         self.yahoo_uri = self.extracted_data.get("yahoo:uri", "")


class User(YahooFantasyObject):
    """
    """

    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.games = self.extracted_data.get("games", "")
        self.guid = self.extracted_data.get("guid", "")


class Game(YahooFantasyObject):
    """
    """

    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.code = self.extracted_data.get("code", "")
        self.game_id = self.extracted_data.get("game_id", "")
        self.game_key = self.extracted_data.get("game_key", "")
        self.is_game_over = self.extracted_data.get("is_game_over", "")
        self.is_live_draft_lobby_active = self.extracted_data.get("is_live_draft_lobby_active", "")
        self.is_offseason = self.extracted_data.get("is_offseason", "")
        self.is_registration_over = self.extracted_data.get("is_registration_over", "")
        self.leagues = self.extracted_data.get("leagues", "")
        self.name = self.extracted_data.get("name", "")
        self.season = self.extracted_data.get("season", "")
        self.type = self.extracted_data.get("type", "")
        self.url = self.extracted_data.get("url", "")


class League(YahooFantasyObject):
    """
    """

    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.allow_add_to_dl_extra_pos = self.extracted_data.get("allow_add_to_dl_extra_pos", "")
        self.current_week = self.extracted_data.get("current_week", "")
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
        self.renew = self.extracted_data.get("renew", "")
        self.renewed = self.extracted_data.get("renewed", "")
        self.scoring_type = self.extracted_data.get("scoring_type", "")
        self.season = self.extracted_data.get("season", "")
        self.settings = self.extracted_data.get("settings", "")  # type: Settings
        self.short_invitation_url = self.extracted_data.get("short_invitation_url", "")
        self.standings = self.extracted_data.get("standings", "")  # type: Standings
        self.start_date = self.extracted_data.get("start_date", "")
        self.start_week = self.extracted_data.get("start_week", "")
        self.url = self.extracted_data.get("url", "")
        self.weekly_deadline = self.extracted_data.get("weekly_deadline", "")


class Team(YahooFantasyObject):
    """
    """

    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.clinched_playoffs = self.extracted_data.get("clinched_playoffs", "")
        self.draft_grade = self.extracted_data.get("draft_grade", "")
        self.draft_recap_url = self.extracted_data.get("draft_recap_url", "")
        self.has_draft_grade = self.extracted_data.get("has_draft_grade", "")
        self.league_scoring_type = self.extracted_data.get("league_scoring_type", "")
        self.managers = self.extracted_data.get("managers", "")
        self.name = self.extracted_data.get("name", "").encode("utf-8")
        self.number_of_moves = self.extracted_data.get("number_of_moves", "")
        self.number_of_trades = self.extracted_data.get("number_of_trades", "")
        self.roster_adds = self.extracted_data.get("roster_adds", "")  # type: RosterAdds
        self.team_id = self.extracted_data.get("team_id", "")
        self.team_key = self.extracted_data.get("team_key", "")
        self.team_logos = self.extracted_data.get("team_logos", "")
        self.team_points = self.extracted_data.get("team_points", "")  # type: TeamPoints
        self.team_standings = self.extracted_data.get("team_standings", "")  # type: TeamStandings
        self.url = self.extracted_data.get("url", "")
        self.waiver_priority = self.extracted_data.get("waiver_priority", "")


class Standings(YahooFantasyObject):
    """
    """

    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.teams = self.extracted_data.get("teams", "")


class Manager(YahooFantasyObject):
    """
    """

    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.email = self.extracted_data.get("email", "")
        self.guid = self.extracted_data.get("guid", "")
        self.image_url = self.extracted_data.get("image_url", "")
        self.is_comanager = self.extracted_data.get("is_comanager", "")
        self.manager_id = self.extracted_data.get("manager_id", "")
        self.nickname = self.extracted_data.get("nickname", "")


class RosterAdds(YahooFantasyObject):
    """
    """

    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.coverage_type = self.extracted_data.get("coverage_type", "")
        self.coverage_value = self.extracted_data.get("coverage_value", "")
        self.value = self.extracted_data.get("value", 0)


class TeamLogo(YahooFantasyObject):
    """
    """

    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.size = self.extracted_data.get("size", "")
        self.url = self.extracted_data.get("url", "")


class TeamPoints(YahooFantasyObject):
    """
    """

    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.coverage_type = self.extracted_data.get("coverage_type", "")
        self.season = self.extracted_data.get("season", "")
        self.total = self.extracted_data.get("total", 0)


class TeamStandings(YahooFantasyObject):
    """
    """

    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.outcome_totals = self.extracted_data.get("outcome_totals")  # type: OutcomeTotals
        self.playoff_seed = self.extracted_data.get("playoff_seed", 0)
        self.points_against = self.extracted_data.get("points_against", 0)
        self.points_for = self.extracted_data.get("points_for", 0)
        self.rank = self.extracted_data.get("rank", 0)
        self.streak = self.extracted_data.get("streak")  # type: Streak


class OutcomeTotals(YahooFantasyObject):
    """
    """

    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.losses = int(self.extracted_data.get("losses", 0))
        self.percentage = float(self.extracted_data.get("percentage", 0))
        self.ties = int(self.extracted_data.get("ties", 0) or 0)
        self.wins = int(self.extracted_data.get("wins", 0))


class Streak(YahooFantasyObject):
    """
    """

    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.type = self.extracted_data.get("type", "")
        self.value = self.extracted_data.get("value", "")


class Settings(YahooFantasyObject):
    """
    """

    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.cant_cut_list = self.extracted_data.get("cant_cut_list", "")
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
        self.stat_categories = self.extracted_data.get("stat_categories", "")  # type: StatCategories
        self.stat_modifiers = self.extracted_data.get("stat_modifiers", "")  # type: StatModifiers
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


class RosterPosition(YahooFantasyObject):
    """
    """

    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.count = self.extracted_data.get("count", "")
        self.position = self.extracted_data.get("position", "")
        self.position_type = self.extracted_data.get("position_type", "")


class StatCategories(YahooFantasyObject):
    """
    """

    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.stats = self.extracted_data.get("stats", "")


class StatModifiers(YahooFantasyObject):
    """
    """

    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.stats = self.extracted_data.get("stats", "")


class Stat(YahooFantasyObject):
    """
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
    """
    """

    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.is_only_display_stat = self.extracted_data.get("is_only_display_stat", "")
        self.position_type = self.extracted_data.get("position_type", "")


class Bonus(YahooFantasyObject):
    """
    """

    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.points = self.extracted_data.get("points", "")
        self.target = self.extracted_data.get("target", "")


class Matchup(YahooFantasyObject):
    """
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
        self.teams = self.extracted_data.get("teams")
        self.week = self.extracted_data.get("week", "")
        self.week_end = self.extracted_data.get("week_end", "")
        self.week_start = self.extracted_data.get("week_start", "")
        self.winner_team_key = self.extracted_data.get("winner_team_key", "")


class MatchupGrade(YahooFantasyObject):
    """
    """

    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.grade = self.extracted_data.get("grade", "")
        self.team_key = self.extracted_data.get("team_key", "")


class Player(YahooFantasyObject):
    """
    """

    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.bye_weeks = self.extracted_data.get("bye_weeks")  # type: ByeWeeks
        self.display_position = self.extracted_data.get("display_position", "")
        self.editorial_player_key = self.extracted_data.get("editorial_player_key", "")
        self.editorial_team_abbr = self.extracted_data.get("editorial_team_abbr", "")
        self.editorial_team_full_name = self.extracted_data.get("editorial_team_full_name", "")
        self.editorial_team_key = self.extracted_data.get("editorial_team_key", "")
        self.eligible_positions = self.extracted_data.get("eligible_positions", "")
        self.has_player_notes = self.extracted_data.get("has_player_notes", "")
        self.headshot = self.extracted_data.get("headshot", "")  # type: Headshot
        self.is_editable = self.extracted_data.get("is_editable", "")
        self.is_undroppable = self.extracted_data.get("is_undroppable", "")
        self.name = self.extracted_data.get("name", "")  # type: Name
        self.player_id = self.extracted_data.get("player_id", "")
        self.player_key = self.extracted_data.get("player_key", "")
        self.player_notes_last_timestamp = self.extracted_data.get("player_notes_last_timestamp", "")
        self.player_points = self.extracted_data.get("player_points", "")  # type: PlayerPoints
        self.player_stats = self.extracted_data.get("player_stats", "")  # type: PlayerStats
        self.position_type = self.extracted_data.get("position_type", "")
        self.primary_position = self.extracted_data.get("primary_position", "")
        self.selected_position = self.extracted_data.get("selected_position", "")  # type: SelectedPosition
        self.status = self.extracted_data.get("status", "")
        self.uniform_number = self.extracted_data.get("uniform_number", "")


class ByeWeeks(YahooFantasyObject):
    """
    """
    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.week = self.extracted_data.get("week", "")


class Headshot(YahooFantasyObject):
    """
    """

    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.size = self.extracted_data.get("size", "")
        self.url = self.extracted_data.get("url", "")


class Name(YahooFantasyObject):
    """
    """

    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.ascii_first = self.extracted_data.get("ascii_first", "")
        self.ascii_last = self.extracted_data.get("ascii_last", "")
        self.first = self.extracted_data.get("first", "")
        self.full = self.extracted_data.get("full", "")
        self.last = self.extracted_data.get("last", "")


class PlayerPoints(YahooFantasyObject):
    """
    """

    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.coverage_type = self.extracted_data.get("coverage_type", "")
        self.week = self.extracted_data.get("week", "")
        self.total = float(self.extracted_data.get("total", 0) or 0)


class PlayerStats(YahooFantasyObject):
    """
    """

    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.coverage_type = self.extracted_data.get("coverage_type", "")
        self.week = self.extracted_data.get("week", "")
        self.stats = self.extracted_data.get("stats", "")


class SelectedPosition(YahooFantasyObject):
    """
    """

    def __init__(self, extracted_data):
        YahooFantasyObject.__init__(self, extracted_data)
        self.coverage_type = self.extracted_data.get("coverage_type", "")
        self.is_flex = self.extracted_data.get("is_flex", "")
        self.position = self.extracted_data.get("position", "")
        self.week = self.extracted_data.get("week", "")
