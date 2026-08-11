# Bulk Export Multiple Fantasy Leagues

Efficiently export data from multiple Yahoo Fantasy and Sleeper leagues in a single batch operation.

## Features

- **Multi-platform support** - Export from Yahoo Fantasy and Sleeper simultaneously
- **Batch configuration** - Define all leagues in a single JSON config file
- **Flexible filtering** - Select specific weeks/years to export
- **Error tracking** - Automatically tracks successful and failed exports
- **Progress logging** - Real-time status updates during export

## Quick Start

### 1. Create a Configuration File

```bash
python scripts/bulk_export_leagues.py config ./my_leagues.json
```

This generates a template with examples.

### 2. Edit the Configuration

```json
{
  "yahoo_token": "YOUR_YAHOO_TOKEN_HERE",
  "leagues": {
    "yahoo": [
      {
        "year": 2024,
        "league_id": "42081",
        "name": "My League",
        "start_week": 1,
        "end_week": 17
      }
    ],
    "sleeper": [
      {
        "year": 2025,
        "league_id": "1389378429505241088",
        "name": "My Sleeper League",
        "weeks": null
      }
    ]
  }
}
```

### 3. Run the Export

```bash
python scripts/bulk_export_leagues.py export ./my_leagues.json -o ./all_league_data
```

## Configuration Reference

### Root Level

| Key | Type | Required | Description |
|-----|------|----------|-------------|
| `yahoo_token` | string | No* | Yahoo Fantasy API access token (*required if exporting Yahoo leagues) |
| `leagues` | object | Yes | Container for league definitions |

### League Definitions

#### Yahoo League

```json
{
  "year": 2024,
  "league_id": "12345",
  "name": "League Name",
  "start_week": 1,
  "end_week": 17
}
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `year` | integer | Required | Season year |
| `league_id` | string | Required | Yahoo league ID |
| `name` | string | Optional | Display name |
| `start_week` | integer | 1 | First week to export |
| `end_week` | integer | 17 | Last week to export |

#### Sleeper League

```json
{
  "year": 2025,
  "league_id": "1389378429505241088",
  "name": "League Name",
  "weeks": null
}
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `year` | integer | Required | Season year |
| `league_id` | string | Required | Sleeper league ID (19-digit number) |
| `name` | string | Optional | Display name |
| `weeks` | array | null | Specific weeks to export (null = all) |

## Usage Examples

### Basic Export (All Leagues)

```bash
python scripts/bulk_export_leagues.py export ./leagues.json
```

Output directory: `./league_exports/`

### Custom Output Directory

```bash
python scripts/bulk_export_leagues.py export ./leagues.json -o /data/fantasy_backups
```

### Verbose Logging

```bash
python scripts/bulk_export_leagues.py export ./leagues.json -v
```

Shows detailed progress for each league.

## Output Structure

```
league_exports/
├── yahoo_2024_42081/
│   ├── league_settings_2024.json
│   ├── teams_2024.csv
│   ├── players_2024.csv
│   ├── trades_2024.csv
│   ├── add_drops_2024.csv
│   └── matchups_2024.csv
├── sleeper_2025_1389378429505241088/
│   ├── sleeper_league_summary_1389378429505241088.json
│   ├── sleeper_teams_1389378429505241088.csv
│   ├── sleeper_rosters_1389378429505241088.csv
│   └── sleeper_matchups_1389378429505241088.csv
└── export_results_20260811_123456.json
```

## Results File

After export completes, a `export_results_*.json` file is created with:

```json
{
  "timestamp": "2026-08-11T12:30:00",
  "total_leagues": 14,
  "successful": 13,
  "failed": 1,
  "output_directory": "/path/to/exports",
  "details": {
    "successful": [...],
    "failed": [...]
  }
}
```

## Pre-configured Configuration

Use the included `your_leagues.json` file pre-populated with your leagues:

```bash
# Edit to add your Yahoo token
nano scripts/your_leagues.json

# Then export
python scripts/bulk_export_leagues.py export scripts/your_leagues.json
```

## Using in Python

```python
from scripts.bulk_export_leagues import BulkLeagueExporter

# Export with config file
exporter = BulkLeagueExporter("./output", "./leagues.json")
exporter.export_from_config()
exporter.save_results()

# Or manually add leagues
exporter = BulkLeagueExporter("./output")
yahoo_leagues = [
    {"year": 2024, "league_id": "12345", "name": "League 1"}
]
exporter.export_yahoo_leagues("TOKEN", yahoo_leagues)
exporter.save_results()
```

## Troubleshooting

### "yahoo_token" not found error

Add your Yahoo API token to the configuration file. See [EXPORT_LEAGUE_DATA.md](./EXPORT_LEAGUE_DATA.md) for how to get one.

### Some leagues failed

Check the `export_results_*.json` file for error details. Common issues:
- Invalid league ID
- Token expired (for Yahoo)
- API rate limits (wait and retry)
- Network issues (retry later)

### Slow export

Large leagues with many seasons take time. Be patient. You can:
- Filter specific weeks with `start_week` and `end_week`
- Export leagues separately instead of all at once

## Performance Notes

- Yahoo leagues typically take 2-5 minutes each (depends on season length)
- Sleeper leagues typically take 30 seconds to 2 minutes each
- Full history (12+ leagues) may take 30+ minutes
- Automatic rate limiting prevents API errors

## Integration

These scripts work best with:
- [YFPY](https://github.com/uberfastman/yfpy) - Yahoo Fantasy API wrapper
- Pandas - For data analysis of exported CSVs
- Python 3.10+

## Related Documentation

- [Yahoo Export](./EXPORT_LEAGUE_DATA.md) - Detailed Yahoo Fantasy export usage
- [Sleeper Export](./EXPORT_SLEEPER_LEAGUE_DATA.md) - Detailed Sleeper export usage
