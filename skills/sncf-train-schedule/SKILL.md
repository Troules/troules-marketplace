---
name: sncf-train-schedule
description: Checks French train schedules, departures, arrivals, and plans journeys using the SNCF/Navitia API. Trigger when users ask about French trains, SNCF schedules, journey planning, next departures or arrivals, or real-time train information.
---

# SNCF Train Schedule Checker

Check train schedules, departures, arrivals, and plan journeys using the SNCF/Navitia API.

## Contents

- [Required Dependencies](#required-dependencies)
- [API Configuration](#api-configuration)
- [Core Endpoints](#core-endpoints)
- [Key Parameters](#key-parameters)
- [Quick Start Workflows](#quick-start-workflows)
- [Instructions](#instructions)
- [Quick Reference](#quick-reference)
- [Utility Scripts](#utility-scripts)
- [Guidelines](#guidelines)
- [References](#references)

## Required Dependencies

This skill requires the following tools and packages:

**System tools** (usually pre-installed):
- `curl` - for API requests
- `python3` - for utility scripts (version 3.7+)

**Python packages**:
```bash
pip install requests python-dotenv
```

**Optional tools**:
- `jq` - for manual JSON parsing (install: `apt-get install jq` or `brew install jq`)

**Verification**: Run `./scripts/test-api.sh` to verify all dependencies are available and the API token is configured.

## API Configuration

- **Base URL**: `https://api.navitia.io/v1/`
- **Auth**: Header-based — `curl -H "Authorization: $NAVITIA_API_TOKEN" "URL"`
- **Token**: Read from env `NAVITIA_API_TOKEN` or `.env` file. Register at https://numerique.sncf.com/startup/api/token-developpeur/
- **Default Region**: `sncf` (covers all SNCF trains across France)

## Core Endpoints

| Endpoint | Path |
|----------|------|
| Journey Planning | `GET /coverage/{region}/journeys?from={id}&to={id}&datetime={ISO8601}` |
| Departures | `GET /coverage/{region}/stop_areas/{stop_id}/departures?from_datetime={ISO8601}` |
| Arrivals | `GET /coverage/{region}/stop_areas/{stop_id}/arrivals?from_datetime={ISO8601}` |
| Stop Schedules | `GET /coverage/{region}/stop_areas/{stop_id}/stop_schedules?from_datetime={ISO8601}` |
| Places Search | `GET /coverage/{region}/places?q={query}` |
| Coverage | `GET /coverage` |

## Key Parameters

- **datetime**: `YYYYMMDDTHHmmss` format (e.g., `20260208T143000`)
  - Use `python scripts/validate_datetime.py` to validate or convert formats
- **from/to**: Coordinates `lon;lat` or station IDs like `stop_area:SNCF:87686006`
  - Use `python scripts/search_stations.py` to find station IDs
- **region**: `sncf` (default, covers all SNCF trains nationwide), or regional codes like `fr-idf`, `fr-ne`, `fr-nw`
- **data_freshness**:
  - `realtime` (default) - includes live delays, cancellations, and platform changes
  - `base_schedule` - theoretical schedule only, no real-time updates
- **count**: Number of results to return
  - Recommended: 5-10 for quick overview (balances information vs. cognitive load)
  - Use 20+ for comprehensive searches
  - API default: 10
- **depth**: Detail level of API response
  - `0` = Minimal (just times and IDs)
  - `1` = Standard (includes line names, directions) - recommended default
  - `2` = Detailed (adds geo coordinates, disruption info)
  - `3` = Full (complete nested objects - use sparingly, increases response size)

## Quick Start Workflows

### Check Next Departures (Copy and follow this checklist)

```
Task Progress:
- [ ] Step 1: Get API token
- [ ] Step 2: Search for station
- [ ] Step 3: Validate station ID
- [ ] Step 4: Get departures
```

**Step 1: Get API token**
```bash
# Check if token is set
echo $NAVITIA_API_TOKEN

# If not set, get token at https://numerique.sncf.com/startup/api/token-developpeur/
export NAVITIA_API_TOKEN='your-token'
```

**Step 2: Search for station**
```bash
python scripts/search_stations.py "Paris Gare de Lyon"
```

**Step 3: Validate station ID** (optional but recommended)
```bash
python scripts/validate_station_id.py "stop_area:SNCF:87686006"
```

**Step 4: Get departures**
```bash
python scripts/get_departures.py "stop_area:SNCF:87686006" --count 5
```

### Plan a Journey (Copy and follow this checklist)

```
Task Progress:
- [ ] Step 1: Get API token
- [ ] Step 2: Search for origin station
- [ ] Step 3: Validate origin station ID
- [ ] Step 4: Search for destination station
- [ ] Step 5: Validate destination station ID
- [ ] Step 6: (Optional) Format datetime if specific time needed
- [ ] Step 7: Plan journey
- [ ] Step 8: Save results
```

**Steps 1-5: Get token and find stations** (see "Check Next Departures" above)

**Step 6: Format datetime** (if planning for specific time)
```bash
# Validate and convert datetime format
python scripts/validate_datetime.py "2026-02-10 14:00:00" --convert
# Returns: 20260210T140000
```

**Step 7: Plan journey**
```bash
# Depart now
python scripts/plan_journey.py "stop_area:SNCF:87686006" "stop_area:SNCF:87722025"

# Depart at specific time
python scripts/plan_journey.py "stop_area:SNCF:87686006" "stop_area:SNCF:87722025" \
  --datetime "20260210T140000"

# Arrive by specific time
python scripts/plan_journey.py "stop_area:SNCF:87686006" "stop_area:SNCF:87722025" \
  --datetime "20260210T180000" --datetime-represents arrival
```

**Step 8: Save results** (optional)
```bash
./scripts/save-journey.sh "origin" "destination" "20260210T140000"
```

**Feedback loop**: If validation fails at any step, return to the search step and try different search terms.

## Instructions

When users request train information:

1. **Get API token**: Check `NAVITIA_API_TOKEN` env var or source `.env`. If missing, direct users to https://numerique.sncf.com/startup/api/token-developpeur/ for a free token.

2. **Identify region**: Default to `sncf` for SNCF trains. Use `/coverage` to list available regions.

3. **Search locations**: Use `/places` to find station IDs. Show top results for user confirmation.

4. **Format datetime**: Convert natural language to `YYYYMMDDTHHmmss`. Use current time if not specified.

5. **Make API requests**:
   - **Always use header auth**: `curl -H "Authorization: $NAVITIA_API_TOKEN" "URL"`
   - Save JSON to files before parsing (avoid piping issues)
   - On "no token" error → check auth format; on 403 → try `sncf` region; on empty response → broaden search terms

6. **Present results clearly**:
   - Parse time: `YYYYMMDDTHHmmss` → extract positions 9–10 (HH) and 11–12 (MM)
   - Journeys: show departure/arrival times, duration, transfers, CO2
   - Departures/arrivals: show time, line, direction, platform, real-time status
   - Use the mobile template in `references/response-template.md` (30-char width target)
   - Abbreviate station names and day names as defined in the template reference
   - Highlight recommended options (fastest / most direct)

7. **Save journey results**: Save to `results/YYYY-MM-DD_HHMM_origin-destination.txt` with formatted details and metadata footer. The `results/` folder is gitignored.

## Quick Reference

```bash
# Search station
curl -H "Authorization: $NAVITIA_API_TOKEN" \
  "https://api.navitia.io/v1/coverage/sncf/places?q=paris%20gare%20de%20lyon"

# Get departures
curl -H "Authorization: $NAVITIA_API_TOKEN" \
  "https://api.navitia.io/v1/coverage/sncf/stop_areas/stop_area:SNCF:87686006/departures?from_datetime=20260208T140000&count=5"
```

## Utility Scripts

The skill provides Python utility scripts that save tokens by executing pre-written, tested code instead of generating ad-hoc commands. All scripts require `NAVITIA_API_TOKEN` environment variable.

**Core utilities**:
- `search_stations.py` - Find station IDs by name
- `get_departures.py` - Get departures from a station
- `get_arrivals.py` - Get arrivals at a station
- `plan_journey.py` - Plan journey between two locations

**Validation utilities**:
- `validate_station_id.py` - Verify a station ID exists
- `validate_datetime.py` - Validate/convert datetime formats

**See `scripts/README.md` for complete documentation and examples.**

## Guidelines

- Always include API token in every request (header auth)
- Handle errors: 401 (invalid token), 404 (not found), rate limits
- Default to `data_freshness=realtime` for current information
- Respect API rate limits — don't make excessive requests
- Never log or expose API tokens in responses
- France coverage is comprehensive; international journeys may be limited

## References

For detailed documentation, see:
- **API reference & examples**: `references/api-reference.md`
- **Common station IDs**: `references/common-stations.md`
- **Mobile response template**: `references/response-template.md`
- **Usage examples**: `examples/usage-examples.md`
- **Utility scripts documentation**: `scripts/README.md`
- **Helper scripts**: `scripts/save-journey.sh`, `scripts/test-api.sh`
