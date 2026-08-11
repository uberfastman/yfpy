# Export Yahoo Fantasy League Data

This script exports comprehensive Yahoo Fantasy League data to CSV and JSON files.

## Features

The script downloads and exports:

- **League Settings** - Playoff start week, roster positions, stat categories
- **Teams & Standings** - Team info, manager details, records, points
- **Players & Statistics** - Player rosters, weekly stats, scoring by category
- **Trades** - Trade history with player details and picks
- **Add/Drops** - Transaction history
- **Matchups** - Weekly matchup results and projections

## Requirements

- Python 3.7+
- `requests`
- `xmltodict`
- `pandas`

Install dependencies:

```bash
pip install requests xmltodict pandas
```

Or using the project's virtual environment:

```bash
make install
```

## Getting an Access Token

1. Visit https://lemon-dune-0cd4b231e.azurestaticapps.net/
2. Log in with your Yahoo account
3. Copy the generated Access Token

**Note:** Keep your token secure. Do not commit it to version control.

## Usage

### Command Line

```bash
python scripts/export_league_data.py <TOKEN> <LEAGUE_KEY> [OPTIONS]
```

#### Arguments

- `TOKEN` - Yahoo Fantasy API access token
- `LEAGUE_KEY` - League key (e.g., `461.l.35322`)

#### Options

- `-o, --output` - Output directory (default: current directory)
- `-s, --start-week` - Start week for player statistics (default: 1)
- `-e, --end-week` - End week for player statistics (default: 17)
- `-v, --verbose` - Enable verbose logging

### Examples

Export all data for a league:

```bash
python scripts/export_league_data.py YOUR_TOKEN 461.l.35322 -o ./league_data
```

Export data for weeks 1-14 (regular season):

```bash
python scripts/export_league_data.py YOUR_TOKEN 461.l.35322 -s 1 -e 14 -o ./league_data
```

## Output Files

The script generates the following files in the output directory:

| File | Description |
|------|-------------|
| `league_settings_YYYY.json` | League configuration and playoff settings |
| `teams_YYYY.csv` | Teams, managers, and final standings |
| `players_YYYY.csv` | Player rosters and weekly statistics |
| `trades_YYYY.csv` | Trade history and involved players |
| `add_drops_YYYY.csv` | Add/drop transaction history |
| `matchups_YYYY.csv` | Weekly matchup results |

Where `YYYY` is the league season year.

## Using in Python

You can also use the `YahooFantasyDataExporter` class directly:

```python
from scripts.export_league_data import YahooFantasyDataExporter
from pathlib import Path

exporter = YahooFantasyDataExporter(
    access_token="YOUR_TOKEN",
    output_dir=Path("./league_data")
)

# Export all data
exporter.export_all("461.l.35322", start_week=1, end_week=17)

# Or export specific data types
leagues = exporter.get_user_leagues()
teams = exporter.export_teams("461.l.35322")
players = exporter.export_players("461.l.35322", start_week=1, end_week=17)
trades = exporter.export_trades("461.l.35322")
add_drops = exporter.export_add_drops("461.l.35322")
matchups = exporter.export_matchups("461.l.35322")
```

## Notes

- The script respects Yahoo Fantasy's API rate limits with built-in delays
- Large leagues with many players may take several minutes to export
- All timestamps are converted to local time
- Player statistics are aggregated from weekly stat endpoints

## Troubleshooting

### Authentication Error

If you get an authentication error, ensure your access token is:
- Valid and not expired
- Copied exactly without extra whitespace
- Not included in version control

### Rate Limit Issues

If you encounter rate limit errors:
- Run the script during off-peak hours
- Reduce the week range with `--start-week` and `--end-week`
- Increase the delay in the code if needed

### Missing Data

Some data fields may be empty for:
- Teams without trades
- Leagues without divisions
- Mid-season exports (future weeks have no statistics)

## Related

For more information about the Yahoo Fantasy API, see:
- [Yahoo Fantasy API Documentation](https://developer.yahoo.com/fantasysports/rest_api_guide/)
- [yfpy Documentation](../docs)
