---
name: sncf-train-schedule
description: >
  Checks French train schedules, departures, arrivals, and plans journeys using the
  SNCF/Navitia API. Trigger when users ask about French trains, SNCF schedules, journey
  planning, next departures or arrivals, or real-time train information.
---

# SNCF Train Schedule Checker

Check train schedules, departures, arrivals, and plan journeys using the SNCF/Navitia API.

## API Configuration

- **Base URL**: `https://api.navitia.io/v1/`
- **Auth**: Header-based — `curl -H "Authorization: $NAVITIA_API_TOKEN" "URL"`
- **Token**: Read from env `NAVITIA_API_TOKEN` or `.env` file. Register at https://www.navitia.io/
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

- **datetime**: `YYYYMMDDTHHmmss` (e.g., `20260208T143000`)
- **from/to**: Coordinates `lon;lat` or IDs like `stop_area:SNCF:87686006`
- **region**: `sncf` (default), `fr-idf`, `fr-ne`, `fr-nw`, `sandbox`
- **data_freshness**: `realtime` (default) or `base_schedule`
- **count**: Number of results (default 10)
- **depth**: Detail level 0–3

## Instructions

When users request train information:

1. **Get API token**: Check `NAVITIA_API_TOKEN` env var or source `.env`. If missing, direct users to https://www.navitia.io/ for a free token.

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
   - Use emoji for readability, highlight recommended options, clean station names (remove city suffixes)

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
- **Usage examples**: `examples/usage-examples.md`
- **Helper scripts**: `scripts/save-journey.sh`, `scripts/test-api.sh`
