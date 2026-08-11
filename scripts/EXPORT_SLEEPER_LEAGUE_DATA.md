# Sleeper Fantasy League Data Export

This script exports comprehensive Sleeper Fantasy League data to CSV and JSON files.

## Features

The script downloads and exports:

- **League Summary** - League settings, scoring settings, draft information
- **Teams & Standings** - Team records, points for/against, current rankings
- **Rosters** - Player rosters with positions, starters vs bench designation
- **Matchups** - Weekly matchup results and projected points

## Usage

### Command Line

```bash
python scripts/export_sleeper_league_data.py <LEAGUE_ID> [OPTIONS]
```

#### Arguments

- `LEAGUE_ID` - Sleeper league ID (numeric string from league URL)

#### Options

- `-o, --output` - Output directory (default: current directory)
- `-w, --weeks` - Specific weeks to export (default: 1-17, e.g., `-w 1 2 3 4`)
- `-v, --verbose` - Enable verbose logging

### Examples

Export all data for a Sleeper league:

```bash
python scripts/export_sleeper_league_data.py 1389378429505241088 -o ./league_data
```

Export specific weeks:

```bash
python scripts/export_sleeper_league_data.py 1389378429505241088 -w 1 2 3 4 5 -o ./league_data
```

## Output Files

The script generates the following files:

| File | Description |
|------|-------------|
| `sleeper_league_summary_{ID}.json` | League configuration and settings |
| `sleeper_teams_{ID}.csv` | Teams and final standings |
| `sleeper_rosters_{ID}.csv` | Player rosters with details |
| `sleeper_matchups_{ID}.csv` | Weekly matchup results |

## Using in Python

```python
from scripts.export_sleeper_league_data import SleeperFantasyDataExporter

exporter = SleeperFantasyDataExporter("./league_data")
exporter.export_all("1389378429505241088")
```

## API Rate Limits

Sleeper has generous rate limits. This script includes minimal delays between requests.

## Notes

- League IDs are long numeric strings (19 digits)
- Sleeper API is public - no authentication required
- All data is fetched from Sleeper's public API endpoints
