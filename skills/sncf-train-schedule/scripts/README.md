# SNCF Train Schedule Utility Scripts

All scripts require the `NAVITIA_API_TOKEN` environment variable to be set.

Get your API token at: https://numerique.sncf.com/startup/api/token-developpeur/

```bash
export NAVITIA_API_TOKEN='your-token-here'
```

## Quick Reference

| Script | Purpose | Example |
|--------|---------|---------|
| `search_stations.py` | Find station IDs by name | `python search_stations.py "Paris"` |
| `validate_station_id.py` | Verify a station ID exists | `python validate_station_id.py "stop_area:SNCF:87686006"` |
| `validate_datetime.py` | Check/convert datetime format | `python validate_datetime.py "20260210T140000"` |
| `get_departures.py` | Get departures from a station | `python get_departures.py "stop_area:SNCF:87686006"` |
| `get_arrivals.py` | Get arrivals at a station | `python get_arrivals.py "stop_area:SNCF:87686006"` |
| `plan_journey.py` | Plan journey between stations | `python plan_journey.py "stop_area:SNCF:87686006" "stop_area:SNCF:87722025"` |

## Installation

**Required Python packages:**

```bash
pip install requests python-dotenv
```

**Optional tools:**
- `jq` - for manual JSON parsing (install: `apt-get install jq` or `brew install jq`)

## Script Details

### search_stations.py

Search for SNCF station IDs by name. Returns matching stations with their IDs and coordinates.

**Usage:**
```bash
python search_stations.py "Paris Gare de Lyon"
python search_stations.py "Lyon" --count 10
python search_stations.py "Marseille" --format json
```

**Parameters:**
- `query` - Station name to search for (required)
- `--count` - Maximum number of results (default: 10)
- `--format` - Output format: `human` or `json` (default: human)

**Example output:**
```
1. Paris Gare de Lyon
   ID: stop_area:SNCF:87686006
   Coordinates: 2.373456;48.844444
   Quality: 100

2. Lyon Part Dieu
   ID: stop_area:SNCF:87722025
   Coordinates: 4.859488;45.760403
   Quality: 100
```

### validate_station_id.py

Validate that a station ID exists and is accessible via the API.

**Usage:**
```bash
python validate_station_id.py "stop_area:SNCF:87686006"
```

**Exit codes:**
- `0` - Valid station ID
- `1` - Invalid or not found

**Example output:**
```
✅ Valid station: Paris Gare de Lyon
   ID: stop_area:SNCF:87686006
   Coordinates: 2.373456;48.844444
```

### validate_datetime.py

Validate datetime format for the SNCF API (YYYYMMDDTHHmmss). Can also convert from common datetime formats.

**Usage:**
```bash
# Validate API format
python validate_datetime.py "20260210T140000"

# Convert from ISO format
python validate_datetime.py "2026-02-10 14:00:00" --convert
python validate_datetime.py "2026-02-10T14:00" --convert
```

**Parameters:**
- `datetime` - Datetime string to validate (required)
- `--convert` - Attempt to convert from common formats

**Supported input formats (with --convert):**
- `YYYY-MM-DD HH:MM:SS` - 2026-02-10 14:00:00
- `YYYY-MM-DDTHH:MM:SS` - 2026-02-10T14:00:00
- `YYYY-MM-DD HH:MM` - 2026-02-10 14:00
- `DD/MM/YYYY HH:MM` - 10/02/2026 14:00
- And more...

**Example output:**
```
✅ Valid datetime: 20260210T140000
   Converted from %Y-%m-%d %H:%M:%S
   Monday, February 10, 2026 at 14:00:00
```

### get_departures.py

Get departures from an SNCF station. Shows next trains leaving the station with real-time delay information.

**Usage:**
```bash
# Get next 10 departures (default)
python get_departures.py "stop_area:SNCF:87686006"

# Get next 5 departures
python get_departures.py "stop_area:SNCF:87686006" --count 5

# Get departures starting from specific time
python get_departures.py "stop_area:SNCF:87686006" --datetime "20260210T140000"

# Get theoretical schedule only (no real-time delays)
python get_departures.py "stop_area:SNCF:87686006" --data-freshness base_schedule

# Get JSON output
python get_departures.py "stop_area:SNCF:87686006" --format json
```

**Parameters:**
- `station_id` - Station ID (required, e.g., `stop_area:SNCF:87686006`)
- `--count` - Number of departures (default: 10)
- `--datetime` - Starting datetime in YYYYMMDDTHHmmss format
- `--data-freshness` - `realtime` or `base_schedule` (default: realtime)
- `--format` - Output format: `human` or `json` (default: human)

**Example output:**
```
1. [TGV 6601] → Marseille St Charles
   Departure: 14:15

2. [TER 17234] → Melun
   Departure: 14:22
   ⚠️  Delayed (scheduled: 14:18)

3. [RER D] → Melun
   Departure: 14:25
```

### get_arrivals.py

Get arrivals at an SNCF station. Shows trains arriving at the station with real-time delay information.

**Usage:**
```bash
# Get next 10 arrivals (default)
python get_arrivals.py "stop_area:SNCF:87686006"

# Get next 5 arrivals
python get_arrivals.py "stop_area:SNCF:87686006" --count 5

# Get arrivals starting from specific time
python get_arrivals.py "stop_area:SNCF:87686006" --datetime "20260210T140000"

# Get theoretical schedule only
python get_arrivals.py "stop_area:SNCF:87686006" --data-freshness base_schedule

# Get JSON output
python get_arrivals.py "stop_area:SNCF:87686006" --format json
```

**Parameters:**
- `station_id` - Station ID (required)
- `--count` - Number of arrivals (default: 10)
- `--datetime` - Starting datetime in YYYYMMDDTHHmmss format
- `--data-freshness` - `realtime` or `base_schedule` (default: realtime)
- `--format` - Output format: `human` or `json` (default: human)

**Example output:**
```
1. [TGV 6604] from Marseille St Charles
   Arrival: 14:10

2. [TER 17233] from Melun
   Arrival: 14:18
   ⚠️  Delayed (scheduled: 14:15)
```

### plan_journey.py

Plan a journey between two SNCF locations (stations or coordinates). Returns multiple journey options with transfers and timing details.

**Usage:**
```bash
# Journey between station IDs
python plan_journey.py "stop_area:SNCF:87686006" "stop_area:SNCF:87722025"

# Journey between coordinates (lon;lat format)
python plan_journey.py "2.3522;48.8566" "4.8357;45.7640"

# Depart at specific time
python plan_journey.py "stop_area:SNCF:87686006" "stop_area:SNCF:87722025" \
    --datetime "20260210T140000"

# Arrive by specific time
python plan_journey.py "stop_area:SNCF:87686006" "stop_area:SNCF:87722025" \
    --datetime "20260210T180000" --datetime-represents arrival

# Get more journey options
python plan_journey.py "stop_area:SNCF:87686006" "stop_area:SNCF:87722025" --count 10

# Get JSON output
python plan_journey.py "stop_area:SNCF:87686006" "stop_area:SNCF:87722025" --format json
```

**Parameters:**
- `from_location` - Origin station ID or coordinates (required)
- `to_location` - Destination station ID or coordinates (required)
- `--datetime` - Datetime in YYYYMMDDTHHmmss format
- `--datetime-represents` - `departure` or `arrival` (default: departure)
- `--count` - Number of journey options (default: 5)
- `--data-freshness` - `realtime` or `base_schedule` (default: realtime)
- `--format` - Output format: `human` or `json` (default: human)

**Example output:**
```
============================================================
Journey 1: 14:15 → 16:20 (2h 5min)
Transfers: 0

  1. [TGV 6601] → Lyon Part Dieu
     Paris Gare de Lyon (14:15) → Lyon Part Dieu (16:20)

============================================================
Journey 2: 14:45 → 17:05 (2h 20min)
Transfers: 1

  1. [TER 17240] → Dijon Ville
     Paris Gare de Lyon (14:45) → Dijon Ville (16:10)

  2. Transfer (walking, 10min)

  3. [TGV 6615] → Lyon Part Dieu
     Dijon Ville (16:20) → Lyon Part Dieu (17:05)
```

## Common Workflows

### Check Next Departures from a Station

```bash
# 1. Search for station
python search_stations.py "Paris Gare de Lyon"

# 2. Validate the station ID (optional but recommended)
python validate_station_id.py "stop_area:SNCF:87686006"

# 3. Get departures
python get_departures.py "stop_area:SNCF:87686006" --count 5
```

### Plan a Journey

```bash
# 1. Search for origin station
python search_stations.py "Paris Gare de Lyon"

# 2. Search for destination station
python search_stations.py "Lyon Part Dieu"

# 3. Validate both station IDs (optional)
python validate_station_id.py "stop_area:SNCF:87686006"
python validate_station_id.py "stop_area:SNCF:87722025"

# 4. Plan the journey
python plan_journey.py "stop_area:SNCF:87686006" "stop_area:SNCF:87722025"
```

### Check Specific Time

```bash
# 1. Validate and convert datetime format
python validate_datetime.py "2026-02-10 14:00:00" --convert

# 2. Use the converted datetime
python get_departures.py "stop_area:SNCF:87686006" --datetime "20260210T140000"
```

## Error Handling

All scripts provide helpful error messages:

- **Missing API token**: Tells you how to get and set the token
- **Invalid station ID**: Suggests using search_stations.py
- **Invalid datetime**: Shows the correct format and examples
- **API timeouts**: Suggests retrying or checking connection
- **Network errors**: Shows specific error and suggests solutions

## Tips

1. **Use --format json** when you need to process results programmatically
2. **Validate inputs** before making expensive API calls (journey planning)
3. **Use --count** to limit results and reduce API load
4. **Save common station IDs** to avoid repeated searches
5. **Check --help** on any script for detailed usage information

## Troubleshooting

**"requests package not found"**
```bash
pip install requests
```

**"NAVITIA_API_TOKEN environment variable not set"**
```bash
export NAVITIA_API_TOKEN='your-token'
# Or add to your ~/.bashrc or ~/.zshrc
```

**"API timeout"**
- Check your internet connection
- The SNCF API may be slow during peak hours
- Journey planning takes longer than simple queries

**"Invalid station ID"**
- Use search_stations.py to find the correct ID
- Station IDs must start with "stop_area:"
- Verify the ID with validate_station_id.py

## See Also

- Main documentation: `../SKILL.md`
- API reference: `../references/api-reference.md`
- Test scripts: `./test-api.sh`, `./save-journey.sh`
