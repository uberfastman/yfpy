#!/usr/bin/env python3
"""
Export complete Sleeper Fantasy League data to CSV and JSON files.

This script downloads comprehensive Sleeper league data including:
- League settings and configuration
- Teams and rosters
- Players and statistics
- Matchups and scores
- Trades (if applicable)
"""

import argparse
import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

logger = logging.getLogger(__name__)


class SleeperFantasyDataExporter:
    """Export Sleeper Fantasy League data to files."""

    SLEEPER_API_BASE = "https://api.sleeper.app/v1"

    def __init__(self, output_dir: Optional[Path] = None):
        """
        Initialize the exporter.

        Args:
            output_dir: Directory to save output files (default: current directory)
        """
        self.output_dir = Path(output_dir or ".")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.league_data: Optional[Dict[str, Any]] = None
        self.rosters: Optional[List[Dict[str, Any]]] = None
        self.users: Optional[Dict[str, Dict[str, Any]]] = None

    def _request(self, uri: str) -> Dict[str, Any]:
        """Make API request and return JSON."""
        logger.info(f"Requesting: {uri}")
        response = requests.get(uri)
        response.raise_for_status()
        return response.json()

    def get_league_info(self, league_id: str) -> Dict[str, Any]:
        """Get league information."""
        logger.info(f"Fetching league info for {league_id}...")
        uri = f"{self.SLEEPER_API_BASE}/league/{league_id}"
        league_data = self._request(uri)
        self.league_data = league_data
        return league_data

    def get_rosters(self, league_id: str) -> List[Dict[str, Any]]:
        """Get all rosters in the league."""
        logger.info(f"Fetching rosters for {league_id}...")
        uri = f"{self.SLEEPER_API_BASE}/league/{league_id}/rosters"
        rosters = self._request(uri)
        self.rosters = rosters
        return rosters

    def get_users(self, league_id: str) -> Dict[str, Dict[str, Any]]:
        """Get all users in the league."""
        logger.info(f"Fetching users for {league_id}...")
        uri = f"{self.SLEEPER_API_BASE}/league/{league_id}/users"
        users_list = self._request(uri)
        users = {user["user_id"]: user for user in users_list}
        self.users = users
        return users

    def get_matchups(self, league_id: str, week: int) -> List[Dict[str, Any]]:
        """Get matchups for a specific week."""
        logger.info(f"Fetching matchups for week {week}...")
        uri = f"{self.SLEEPER_API_BASE}/league/{league_id}/matchups/{week}"
        try:
            matchups = self._request(uri)
            return matchups
        except requests.HTTPError as e:
            logger.warning(f"Failed to fetch matchups for week {week}: {e}")
            return []

    def get_players(self) -> Dict[str, Dict[str, Any]]:
        """Get all player data."""
        logger.info("Fetching player data...")
        uri = f"{self.SLEEPER_API_BASE}/players/nfl"
        players = self._request(uri)
        return players

    def export_league_summary(self, league_id: str) -> Dict[str, Any]:
        """Export league summary information."""
        if self.league_data is None:
            self.get_league_info(league_id)

        league_info = self.league_data
        summary = {
            "league_id": league_id,
            "league_name": league_info.get("name"),
            "season": league_info.get("season"),
            "sport": league_info.get("sport"),
            "settings": league_info.get("settings", {}),
            "scoring_settings": league_info.get("scoring_settings", {}),
            "draft_id": league_info.get("draft_id"),
            "status": league_info.get("status"),
        }

        output_file = self.output_dir / f"sleeper_league_summary_{league_id}.json"
        with open(output_file, "w") as f:
            json.dump(summary, f, indent=2)
        logger.info(f"Saved league summary to {output_file}")

        return summary

    def export_teams(self, league_id: str) -> str:
        """Export teams and rosters."""
        if self.rosters is None:
            self.get_rosters(league_id)
        if self.users is None:
            self.get_users(league_id)

        team_dicts = []
        for roster in self.rosters:
            roster_id = roster.get("roster_id")
            owner_id = roster.get("owner_id")
            owner = self.users.get(owner_id, {}) if self.users else {}

            team_dict = {
                "roster_id": roster_id,
                "owner_id": owner_id,
                "owner_name": owner.get("username", "Unknown"),
                "owner_display_name": owner.get("display_name", ""),
                "wins": roster.get("wins", 0),
                "losses": roster.get("losses", 0),
                "ties": roster.get("ties", 0),
                "points_for": roster.get("points_for", 0),
                "points_against": roster.get("points_against", 0),
                "rank": roster.get("rank"),
                "player_count": len(roster.get("players", [])),
                "bench_slots": len(roster.get("bench", [])),
            }
            team_dicts.append(team_dict)

        # Save to CSV
        output_file = self.output_dir / f"sleeper_teams_{league_id}.csv"
        try:
            import pandas as pd

            teams_df = pd.DataFrame(team_dicts)
            teams_df.to_csv(output_file, index=False)
            logger.info(f"Saved teams data to {output_file}")
        except ImportError:
            # Fallback to JSON if pandas not available
            output_file = self.output_dir / f"sleeper_teams_{league_id}.json"
            with open(output_file, "w") as f:
                json.dump(team_dicts, f, indent=2)
            logger.info(f"Saved teams data to {output_file} (pandas not available)")

        return str(output_file)

    def export_rosters(self, league_id: str) -> str:
        """Export full roster data with player details."""
        if self.rosters is None:
            self.get_rosters(league_id)
        if self.users is None:
            self.get_users(league_id)

        players = self.get_players()

        roster_dicts = []
        for roster in self.rosters:
            roster_id = roster.get("roster_id")
            owner_id = roster.get("owner_id")
            owner = self.users.get(owner_id, {}) if self.users else {}
            owner_name = owner.get("username", "Unknown")

            # Add starters
            for player_id in roster.get("starters", []):
                player = players.get(player_id, {})
                roster_dicts.append(
                    {
                        "roster_id": roster_id,
                        "owner_name": owner_name,
                        "player_id": player_id,
                        "player_name": player.get("full_name", "Unknown"),
                        "position": player.get("position", ""),
                        "nfl_team": player.get("team", ""),
                        "slot_type": "starter",
                    }
                )

            # Add bench
            for player_id in roster.get("bench", []):
                player = players.get(player_id, {})
                roster_dicts.append(
                    {
                        "roster_id": roster_id,
                        "owner_name": owner_name,
                        "player_id": player_id,
                        "player_name": player.get("full_name", "Unknown"),
                        "position": player.get("position", ""),
                        "nfl_team": player.get("team", ""),
                        "slot_type": "bench",
                    }
                )

        output_file = self.output_dir / f"sleeper_rosters_{league_id}.csv"
        try:
            import pandas as pd

            rosters_df = pd.DataFrame(roster_dicts)
            rosters_df.to_csv(output_file, index=False)
            logger.info(f"Saved rosters data to {output_file}")
        except ImportError:
            output_file = self.output_dir / f"sleeper_rosters_{league_id}.json"
            with open(output_file, "w") as f:
                json.dump(roster_dicts, f, indent=2)
            logger.info(f"Saved rosters data to {output_file}")

        return str(output_file)

    def export_matchups(self, league_id: str, weeks: Optional[List[int]] = None) -> str:
        """Export matchup data."""
        if self.league_data is None:
            self.get_league_info(league_id)

        season = self.league_data.get("season")
        # Most seasons have 17 weeks
        week_list = weeks or list(range(1, 18))

        matchup_dicts = []
        for week in week_list:
            matchups = self.get_matchups(league_id, week)
            for matchup in matchups:
                if matchup.get("matchup_id") is None:
                    continue

                matchup_dict = {
                    "week": week,
                    "matchup_id": matchup.get("matchup_id"),
                    "roster_id": matchup.get("roster_id"),
                    "owner_id": matchup.get("owner_id"),
                    "points": matchup.get("points", 0),
                    "projected_points": matchup.get("projected_points", 0),
                }

                if self.users and matchup.get("owner_id"):
                    owner = self.users.get(matchup["owner_id"], {})
                    matchup_dict["owner_name"] = owner.get("username", "Unknown")

                matchup_dicts.append(matchup_dict)

            time.sleep(0.1)  # Rate limiting

        output_file = self.output_dir / f"sleeper_matchups_{league_id}.csv"
        try:
            import pandas as pd

            matchups_df = pd.DataFrame(matchup_dicts)
            matchups_df.to_csv(output_file, index=False)
            logger.info(f"Saved matchups data to {output_file}")
        except ImportError:
            output_file = self.output_dir / f"sleeper_matchups_{league_id}.json"
            with open(output_file, "w") as f:
                json.dump(matchup_dicts, f, indent=2)
            logger.info(f"Saved matchups data to {output_file}")

        return str(output_file)

    def export_all(self, league_id: str, weeks: Optional[List[int]] = None) -> None:
        """Export all data for a league."""
        logger.info(f"Exporting all data for league {league_id}...")

        self.export_league_summary(league_id)
        self.export_teams(league_id)
        self.export_rosters(league_id)
        self.export_matchups(league_id, weeks)

        logger.info(f"Export complete. Files saved to {self.output_dir}")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Export Sleeper Fantasy League data to CSV and JSON files"
    )
    parser.add_argument("league_id", help="Sleeper league ID")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path.cwd(),
        help="Output directory for exported files",
    )
    parser.add_argument(
        "-w",
        "--weeks",
        type=int,
        nargs="+",
        help="Specific weeks to export (default: 1-17)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    exporter = SleeperFantasyDataExporter(args.output)
    exporter.export_all(args.league_id, args.weeks)


if __name__ == "__main__":
    main()
