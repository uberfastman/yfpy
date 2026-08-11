#!/usr/bin/env python3
"""
Export complete Yahoo Fantasy League data to CSV and JSON files.

This script downloads comprehensive league data including:
- League settings
- Teams and standings
- Player rosters and statistics
- Trades and transactions
- Matchups and schedules

Requires a valid Yahoo Fantasy API access token.
"""

import argparse
import ast
import csv
import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
import requests
import xmltodict

logger = logging.getLogger(__name__)


class YahooFantasyDataExporter:
    """Export Yahoo Fantasy League data to files."""

    FANTASY_API_BASE = "https://fantasysports.yahooapis.com/fantasy/v2"

    def __init__(self, access_token: str, output_dir: Optional[Path] = None):
        """
        Initialize the exporter.

        Args:
            access_token: Yahoo Fantasy API access token
            output_dir: Directory to save output files (default: current directory)
        """
        self.access_token = access_token
        self.output_dir = Path(output_dir or ".")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.headers = {"Authorization": f"Bearer {access_token}"}
        self.stat_map: Dict[str, str] = {}
        self.teams_df: Optional[pd.DataFrame] = None
        self.league_start_date: Optional[datetime] = None
        self.season: Optional[int] = None

    def _request(self, uri: str) -> requests.Response:
        """Make API request with error handling."""
        logger.info(f"Requesting: {uri}")
        response = requests.get(uri, headers=self.headers)
        response.raise_for_status()
        return response

    def get_user_leagues(self) -> pd.DataFrame:
        """Get all leagues for the authenticated user."""
        logger.info("Fetching user leagues...")
        uri = f"{self.FANTASY_API_BASE}/users;use_login=1/games/leagues"
        response = self._request(uri)
        content = xmltodict.parse(response.text)

        league_dicts = []
        games = content["fantasy_content"]["users"]["user"]["games"]["game"]
        if not isinstance(games, list):
            games = [games]

        for game in games:
            if "leagues" in game and game["leagues"]:
                game_leagues = game["leagues"]["league"]
                if not isinstance(game_leagues, list):
                    game_leagues = [game_leagues]

                for league in game_leagues:
                    league_dicts.append(
                        {
                            "league_key": league["league_key"],
                            "name": league["name"],
                            "game_code": league["game_code"],
                            "season": league["season"],
                            "num_teams": league["num_teams"],
                        }
                    )

        return pd.DataFrame(league_dicts)

    def export_league_settings(self, league_key: str) -> Dict[str, Any]:
        """Export league settings."""
        logger.info(f"Fetching league settings for {league_key}...")
        uri = f"{self.FANTASY_API_BASE}/leagues;league_keys={league_key}/settings"
        response = self._request(uri)
        content = xmltodict.parse(response.text)

        settings = content["fantasy_content"]["leagues"]["league"]["settings"]

        # Build stat map
        for stat in settings["stat_categories"]["stats"]["stat"]:
            self.stat_map[stat["stat_id"]] = stat["name"]

        # Extract league settings
        league_settings = {
            "playoff_startweek": settings["playoff_start_week"],
            "positions": [],
        }

        for position in settings["roster_positions"]["roster_position"]:
            for _ in range(int(position["count"])):
                league_settings["positions"].append(position["position"])

        # Save to file
        output_file = self.output_dir / f"league_settings_{self.season}.json"
        with open(output_file, "w") as f:
            json.dump(league_settings, f, indent=2)
        logger.info(f"Saved league settings to {output_file}")

        return league_settings

    def export_teams(self, league_key: str) -> pd.DataFrame:
        """Export teams and standings data."""
        logger.info(f"Fetching teams and standings for {league_key}...")
        uri = f"{self.FANTASY_API_BASE}/leagues;league_keys={league_key}/standings"
        response = self._request(uri)
        content = xmltodict.parse(response.text)

        league = content["fantasy_content"]["leagues"]["league"]
        self.league_start_date = datetime.strptime(league["start_date"], "%Y-%m-%d")

        team_dicts = []
        for team in league["standings"]["teams"]["team"]:
            manager = team["managers"]["manager"]
            if isinstance(manager, list):
                manager = manager[0]

            team_dict = {
                "name": team["name"],
                "team_key": team["team_key"],
                "number_of_moves": int(team["number_of_moves"]),
                "number_of_trades": int(team["number_of_trades"]),
                "clinched_playoffs": team.get("clinched_playoffs") == "1",
                "manager_name": manager["nickname"],
                "division_id": team.get("division_id"),
                "draft_grade": team.get("draft_grade"),
                "rank": int(team["team_standings"]["rank"]),
                "points_for": float(team["team_standings"]["points_for"]),
                "points_against": float(team["team_standings"]["points_against"]),
                "wins": int(team["team_standings"]["outcome_totals"]["wins"]),
                "losses": int(team["team_standings"]["outcome_totals"]["losses"]),
            }
            team_dicts.append(team_dict)

        teams_df = pd.DataFrame(team_dicts)
        self.teams_df = teams_df

        output_file = self.output_dir / f"teams_{self.season}.csv"
        teams_df.to_csv(output_file, index=False)
        logger.info(f"Saved teams data to {output_file}")

        return teams_df

    def _get_team_nickname(self, team_key: str) -> str:
        """Get nickname for a team key."""
        if self.teams_df is None:
            raise ValueError("Teams data not loaded. Run export_teams first.")
        return self.teams_df[self.teams_df["team_key"] == team_key]["manager_name"].values[
            0
        ]

    def export_players(
        self, league_key: str, start_week: int = 1, end_week: int = 17
    ) -> pd.DataFrame:
        """Export player data with statistics."""
        if not self.teams_df is not None:
            raise ValueError("Teams data not loaded. Run export_teams first.")

        logger.info(f"Fetching player rosters for weeks {start_week}-{end_week}...")

        # Get rosters
        team_keys = ",".join(self.teams_df["team_key"])
        base_uri = (
            f"{self.FANTASY_API_BASE}/teams;team_keys={team_keys}/roster"
        )

        roster_content_list = []
        for week in range(start_week, end_week + 1):
            uri = f"{base_uri};week={week}"
            response = self._request(uri)
            roster_content = xmltodict.parse(response.text)
            roster_content_list.append(roster_content)

        # Parse roster data
        player_dicts = []
        for roster_content in roster_content_list:
            for team in roster_content["fantasy_content"]["teams"]["team"]:
                team_key = team["team_key"]
                for player in team["roster"]["players"]["player"]:
                    player_dict = {
                        "player_key": player["player_key"],
                        "name": player["name"]["full"],
                        "position": player["primary_position"],
                        "week": int(player["selected_position"]["week"]),
                        "started": (
                            player["selected_position"]["position"]
                            == player["primary_position"]
                            or player["selected_position"].get("is_flex") == "1"
                        ),
                        "team_key": team_key,
                        "manager_name": self._get_team_nickname(team_key),
                    }
                    player_dicts.append(player_dict)

        players_df = pd.DataFrame(player_dicts)

        # Get player statistics
        logger.info("Fetching player statistics...")
        player_keys = players_df["player_key"].unique()
        player_stats_contents = []

        for week in range(start_week, end_week + 1):
            logger.info(f"Downloading week {week}...")
            for i in range(0, len(player_keys), 25):  # API max: 25 players per request
                player_keys_subset = ",".join(player_keys[i : i + 25])
                uri = (
                    f"{self.FANTASY_API_BASE}/leagues;league_keys={league_key}"
                    f"/players;player_keys={player_keys_subset}"
                    f"/stats;type=week;week={week}"
                )
                try:
                    response = self._request(uri)
                    player_stats_content = xmltodict.parse(response.text)
                    player_stats_contents.append(player_stats_content)
                except Exception as e:
                    logger.warning(f"Failed to get stats for week {week}: {e}")

                time.sleep(0.5)  # Rate limiting

        # Parse player stats
        player_stats_dicts = []
        for player_stats_content in player_stats_contents:
            try:
                for player_stats in player_stats_content["fantasy_content"]["leagues"][
                    "league"
                ]["players"]["player"]:
                    player_stats_dict = {
                        "player_key": player_stats["player_key"],
                        "week": int(player_stats["player_stats"]["week"]),
                        "points": float(player_stats["player_points"]["total"]),
                        "name": player_stats["name"]["full"],
                    }

                    for stat in player_stats["player_stats"]["stats"]["stat"]:
                        stat_name = self.stat_map[stat["stat_id"]]
                        stat_value = ast.literal_eval(stat["value"])
                        player_stats_dict[stat_name] = stat_value

                    player_stats_dicts.append(player_stats_dict)
            except Exception as e:
                logger.warning(f"Error parsing player stats: {e}")

        player_stats_df = pd.DataFrame(player_stats_dicts)

        # Merge roster and stats
        players_df = pd.merge(
            players_df,
            player_stats_df,
            how="outer",
            left_on=["player_key", "week", "name"],
            right_on=["player_key", "week", "name"],
        )

        output_file = self.output_dir / f"players_{self.season}.csv"
        players_df.to_csv(output_file, index=False)
        logger.info(f"Saved players data to {output_file}")

        return players_df

    def export_trades(self, league_key: str) -> pd.DataFrame:
        """Export trades data."""
        if self.league_start_date is None:
            raise ValueError("League start date not set. Run export_teams first.")

        logger.info("Fetching trades...")
        uri = f"{self.FANTASY_API_BASE}/leagues;league_keys={league_key};out=transactions"
        response = self._request(uri)
        content = xmltodict.parse(response.text)

        trades = [
            t
            for t in content["fantasy_content"]["leagues"]["league"]["transactions"][
                "transaction"
            ]
            if t["type"] == "trade"
        ]

        trade_dicts = []
        for trade in trades:
            trader_team_key = trade["trader_team_key"]
            trader_player_keys = []
            trader_player_names = []
            tradee_player_keys = []
            tradee_player_names = []
            trader_picks = []
            tradee_picks = []

            if "players" in trade:
                players = trade["players"]["player"]
                if not isinstance(players, list):
                    players = [players]

                for player in players:
                    dest_team = player["transaction_data"]["destination_team_key"]
                    name = player["name"]["full"]
                    player_key = player["player_key"]

                    if dest_team == trader_team_key:
                        trader_player_keys.append(player_key)
                        trader_player_names.append(name)
                    else:
                        tradee_player_keys.append(player_key)
                        tradee_player_names.append(name)

            if "picks" in trade:
                for pick in trade["picks"]["pick"]:
                    round_num = int(pick["round"])
                    if pick["destination_team_key"] == trader_team_key:
                        trader_picks.append(round_num)
                    else:
                        tradee_picks.append(round_num)

            timestamp = int(trade["timestamp"])
            trade_date = datetime.fromtimestamp(timestamp)
            delta = trade_date - self.league_start_date
            week_enacted = delta.days // 7

            trade_dict = {
                "trader_team_key": trader_team_key,
                "trader_nickname": self._get_team_nickname(trader_team_key),
                "tradee_team_key": trade["tradee_team_key"],
                "tradee_nickname": self._get_team_nickname(trade["tradee_team_key"]),
                "trader_player_keys_received": trader_player_keys,
                "trader_player_names_received": trader_player_names,
                "tradee_player_keys_received": tradee_player_keys,
                "tradee_player_names_received": tradee_player_names,
                "trader_picks_received": trader_picks,
                "tradee_picks_received": tradee_picks,
                "week_enacted": week_enacted,
                "date": trade_date,
            }
            trade_dicts.append(trade_dict)

        trades_df = pd.DataFrame(trade_dicts)
        output_file = self.output_dir / f"trades_{self.season}.csv"
        trades_df.to_csv(output_file, index=False)
        logger.info(f"Saved trades data to {output_file}")

        return trades_df

    def export_add_drops(self, league_key: str) -> pd.DataFrame:
        """Export add/drop transactions."""
        if self.league_start_date is None:
            raise ValueError("League start date not set. Run export_teams first.")

        logger.info("Fetching add/drop transactions...")
        uri = f"{self.FANTASY_API_BASE}/leagues;league_keys={league_key};out=transactions"
        response = self._request(uri)
        content = xmltodict.parse(response.text)

        add_drops = [
            t
            for t in content["fantasy_content"]["leagues"]["league"]["transactions"][
                "transaction"
            ]
            if t["type"] == "add/drop"
        ]

        add_drop_dicts = []
        for add_drop in add_drops:
            player_keys_added = []
            player_keys_dropped = []
            player_names_added = []
            player_names_dropped = []
            manager_team_key = None

            if "players" in add_drop:
                players = add_drop["players"]["player"]
                if not isinstance(players, list):
                    players = [players]

                for player in players:
                    name = player["name"]["full"]
                    player_key = player["player_key"]
                    trans_type = player["transaction_data"]["type"]

                    if trans_type == "add":
                        player_names_added.append(name)
                        player_keys_added.append(player_key)
                        if manager_team_key is None:
                            manager_team_key = player["transaction_data"][
                                "destination_team_key"
                            ]
                    else:
                        player_names_dropped.append(name)
                        player_keys_dropped.append(player_key)

            timestamp = int(add_drop["timestamp"])
            trans_date = datetime.fromtimestamp(timestamp)
            delta = trans_date - self.league_start_date
            week_enacted = delta.days // 7

            add_drop_dict = {
                "manager_team_key": manager_team_key,
                "manager_nickname": self._get_team_nickname(manager_team_key),
                "player_keys_added": player_keys_added,
                "player_names_added": player_names_added,
                "player_keys_dropped": player_keys_dropped,
                "player_names_dropped": player_names_dropped,
                "week_enacted": week_enacted,
                "date": trans_date,
            }
            add_drop_dicts.append(add_drop_dict)

        add_drop_df = pd.DataFrame(add_drop_dicts)
        output_file = self.output_dir / f"add_drops_{self.season}.csv"
        add_drop_df.to_csv(output_file, index=False)
        logger.info(f"Saved add/drop data to {output_file}")

        return add_drop_df

    def export_matchups(self, league_key: str) -> pd.DataFrame:
        """Export matchup data."""
        logger.info("Fetching matchups...")
        if self.teams_df is None:
            raise ValueError("Teams data not loaded. Run export_teams first.")

        team_keys = ",".join(self.teams_df["team_key"])
        uri = f"{self.FANTASY_API_BASE}/teams;team_keys={team_keys}/matchups"
        response = self._request(uri)
        content = xmltodict.parse(response.text)

        matchup_dicts = []
        for team in content["fantasy_content"]["teams"]["team"]:
            for matchup in team["matchups"]["matchup"]:
                team_1 = matchup["teams"]["team"][0]
                matchup_dict = {
                    "week": int(matchup["week"]),
                    "is_playoffs": matchup["is_playoffs"] == "1",
                    "is_consolation": matchup["is_consolation"] == "1",
                    "team_1_key": team_1["team_key"],
                    "team_1_nickname": self._get_team_nickname(team_1["team_key"]),
                    "team_1_points": float(team_1["team_points"]["total"]),
                    "team_1_projected_points": float(
                        team_1["team_projected_points"]["total"]
                    ),
                }

                if matchup["teams"]["@count"] == "1":
                    matchup_dict["is_bye"] = True
                else:
                    matchup_dict["is_bye"] = False
                    team_2 = matchup["teams"]["team"][1]
                    matchup_dict["team_2_key"] = team_2["team_key"]
                    matchup_dict["team_2_nickname"] = self._get_team_nickname(
                        team_2["team_key"]
                    )
                    matchup_dict["team_2_points"] = float(
                        team_2["team_points"]["total"]
                    )
                    matchup_dict["team_2_projected_points"] = float(
                        team_2["team_projected_points"]["total"]
                    )

                matchup_dicts.append(matchup_dict)

        matchups_df = pd.DataFrame(matchup_dicts)
        output_file = self.output_dir / f"matchups_{self.season}.csv"
        matchups_df.to_csv(output_file, index=False)
        logger.info(f"Saved matchups data to {output_file}")

        return matchups_df

    def export_all(
        self,
        league_key: str,
        start_week: int = 1,
        end_week: int = 17,
    ) -> None:
        """Export all data for a league."""
        logger.info(f"Exporting all data for league {league_key}...")

        # Get league info
        leagues_df = self.get_user_leagues()
        league_info = leagues_df[leagues_df["league_key"] == league_key]
        if league_info.empty:
            raise ValueError(f"League {league_key} not found")

        self.season = league_info["season"].values[0]
        logger.info(f"League season: {self.season}")

        # Export all data
        self.export_league_settings(league_key)
        self.export_teams(league_key)
        self.export_players(league_key, start_week, end_week)
        self.export_trades(league_key)
        self.export_add_drops(league_key)
        self.export_matchups(league_key)

        logger.info(f"Export complete. Files saved to {self.output_dir}")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Export Yahoo Fantasy League data to CSV and JSON files"
    )
    parser.add_argument("token", help="Yahoo Fantasy API access token")
    parser.add_argument("league_key", help="League key (e.g., 461.l.35322)")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path.cwd(),
        help="Output directory for exported files",
    )
    parser.add_argument(
        "-s", "--start-week", type=int, default=1, help="Start week (default: 1)"
    )
    parser.add_argument(
        "-e", "--end-week", type=int, default=17, help="End week (default: 17)"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args()

    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Export data
    exporter = YahooFantasyDataExporter(args.token, args.output)
    exporter.export_all(args.league_key, args.start_week, args.end_week)


if __name__ == "__main__":
    main()
