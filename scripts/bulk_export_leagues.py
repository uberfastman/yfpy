#!/usr/bin/env python3
"""
Bulk export fantasy league data from multiple sources.

Supports exporting data from multiple Yahoo Fantasy and Sleeper leagues
in a single batch operation.
"""

import argparse
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class BulkLeagueExporter:
    """Coordinate exporting data from multiple leagues."""

    def __init__(self, output_dir: Optional[Path] = None, config_file: Optional[Path] = None):
        """
        Initialize the bulk exporter.

        Args:
            output_dir: Base output directory for all exports
            config_file: JSON file with league configuration
        """
        self.output_dir = Path(output_dir or ".")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = config_file
        self.config: Dict = {}
        self.results: Dict = {"successful": [], "failed": []}

        if config_file:
            self._load_config(config_file)

    def _load_config(self, config_file: Path) -> None:
        """Load league configuration from JSON file."""
        logger.info(f"Loading config from {config_file}...")
        with open(config_file, "r") as f:
            self.config = json.load(f)

    def create_config_template(self, output_file: Path) -> None:
        """Create a template configuration file."""
        template = {
            "yahoo_token": "YOUR_YAHOO_ACCESS_TOKEN_HERE",
            "leagues": {
                "yahoo": [
                    {
                        "year": 2024,
                        "league_id": "12345",
                        "name": "League Name",
                        "start_week": 1,
                        "end_week": 17,
                    }
                ],
                "sleeper": [
                    {
                        "year": 2025,
                        "league_id": "1234567890123456789",
                        "name": "League Name",
                        "weeks": None,
                    }
                ],
            },
        }

        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(template, f, indent=2)
        logger.info(f"Created config template at {output_file}")

    def export_yahoo_leagues(self, token: str, leagues: List[Dict]) -> None:
        """Export data from Yahoo Fantasy leagues."""
        try:
            from scripts.export_league_data import YahooFantasyDataExporter
        except ImportError:
            logger.error("Could not import YahooFantasyDataExporter. Make sure yfpy is installed.")
            return

        logger.info(f"Exporting {len(leagues)} Yahoo Fantasy leagues...")

        for league_config in leagues:
            league_id = league_config.get("league_id")
            year = league_config.get("year")
            name = league_config.get("name", "Unknown")
            start_week = league_config.get("start_week", 1)
            end_week = league_config.get("end_week", 17)

            league_output_dir = self.output_dir / f"yahoo_{year}_{league_id}"

            try:
                logger.info(f"  Exporting Yahoo league {year} ({league_id}): {name}")
                exporter = YahooFantasyDataExporter(token, league_output_dir)
                exporter.export_all(league_id, start_week, end_week)
                self.results["successful"].append(
                    {
                        "platform": "yahoo",
                        "year": year,
                        "league_id": league_id,
                        "name": name,
                        "output_dir": str(league_output_dir),
                    }
                )
            except Exception as e:
                logger.error(f"  Failed to export Yahoo league {year}: {e}")
                self.results["failed"].append(
                    {
                        "platform": "yahoo",
                        "year": year,
                        "league_id": league_id,
                        "name": name,
                        "error": str(e),
                    }
                )

    def export_sleeper_leagues(self, leagues: List[Dict]) -> None:
        """Export data from Sleeper leagues."""
        try:
            from scripts.export_sleeper_league_data import SleeperFantasyDataExporter
        except ImportError:
            logger.error("Could not import SleeperFantasyDataExporter. Make sure yfpy is installed.")
            return

        logger.info(f"Exporting {len(leagues)} Sleeper leagues...")

        for league_config in leagues:
            league_id = league_config.get("league_id")
            year = league_config.get("year")
            name = league_config.get("name", "Unknown")
            weeks = league_config.get("weeks")

            league_output_dir = self.output_dir / f"sleeper_{year}_{league_id}"

            try:
                logger.info(f"  Exporting Sleeper league {year} ({league_id}): {name}")
                exporter = SleeperFantasyDataExporter(league_output_dir)
                exporter.export_all(league_id, weeks)
                self.results["successful"].append(
                    {
                        "platform": "sleeper",
                        "year": year,
                        "league_id": league_id,
                        "name": name,
                        "output_dir": str(league_output_dir),
                    }
                )
            except Exception as e:
                logger.error(f"  Failed to export Sleeper league {year}: {e}")
                self.results["failed"].append(
                    {
                        "platform": "sleeper",
                        "year": year,
                        "league_id": league_id,
                        "name": name,
                        "error": str(e),
                    }
                )

    def export_from_config(self) -> None:
        """Export all leagues from loaded configuration."""
        if not self.config:
            raise ValueError("No configuration loaded")

        token = self.config.get("yahoo_token")
        leagues = self.config.get("leagues", {})

        yahoo_leagues = leagues.get("yahoo", [])
        sleeper_leagues = leagues.get("sleeper", [])

        if yahoo_leagues:
            if not token:
                logger.warning("No Yahoo token provided. Skipping Yahoo leagues.")
            else:
                self.export_yahoo_leagues(token, yahoo_leagues)

        if sleeper_leagues:
            self.export_sleeper_leagues(sleeper_leagues)

    def save_results(self, output_file: Optional[Path] = None) -> None:
        """Save export results to file."""
        if not output_file:
            output_file = self.output_dir / f"export_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        summary = {
            "timestamp": datetime.now().isoformat(),
            "total_leagues": len(self.results["successful"]) + len(self.results["failed"]),
            "successful": len(self.results["successful"]),
            "failed": len(self.results["failed"]),
            "output_directory": str(self.output_dir),
            "details": self.results,
        }

        with open(output_file, "w") as f:
            json.dump(summary, f, indent=2)

        logger.info(f"Results saved to {output_file}")
        logger.info(f"  Successful: {len(self.results['successful'])}")
        logger.info(f"  Failed: {len(self.results['failed'])}")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Bulk export fantasy league data from multiple sources"
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Config command
    config_parser = subparsers.add_parser("config", help="Create a configuration template")
    config_parser.add_argument(
        "output", type=Path, help="Output file for configuration template"
    )

    # Export command
    export_parser = subparsers.add_parser("export", help="Export leagues from config file")
    export_parser.add_argument(
        "config_file", type=Path, help="Configuration file (JSON)"
    )
    export_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path.cwd() / "league_exports",
        help="Output directory for exports",
    )
    export_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args()

    # Setup logging
    log_level = logging.DEBUG if getattr(args, "verbose", False) else logging.INFO
    logging.basicConfig(
        level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    if args.command == "config":
        exporter = BulkLeagueExporter()
        exporter.create_config_template(args.output)
        print(f"✓ Configuration template created at {args.output}")
        print(f"  Edit this file with your leagues and token, then run:")
        print(f"  python scripts/bulk_export_leagues.py export {args.output}")

    elif args.command == "export":
        if not args.config_file.exists():
            print(f"✗ Config file not found: {args.config_file}")
            exit(1)

        exporter = BulkLeagueExporter(args.output, args.config_file)
        exporter.export_from_config()
        exporter.save_results()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
