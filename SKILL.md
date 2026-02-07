---
name: sncf-train-schedule
description: Check train schedules, departures, arrivals, and plan journeys using the SNCF/Navitia API. Use this skill when users ask about French trains, SNCF schedules, journey planning, next departures/arrivals, or real-time train information.
---

# SNCF Train Schedule Checker

This skill helps you check train schedules, departures, arrivals, and plan journeys using the SNCF/Navitia API.

## API Configuration

- **Base URL**: `https://api.navitia.io/v1/`
- **Authentication**: Header-based authentication (REQUIRED - most reliable)
  - **Preferred method**: `curl -H "Authorization: $TOKEN" "https://api.navitia.io/v1/..."`
  - ⚠️ Basic Auth (`-u $TOKEN:`) can be unreliable - use header format instead
  - ⚠️ URL-embedded tokens (`https://$TOKEN@api...`) may not work with WebFetch tool
- **API Token**: Required (users need to register at https://www.navitia.io/)
  - Read from environment variable `NAVITIA_API_TOKEN` or `.env` file
  - Free tier available with reasonable rate limits
- **Default Region**: Use `sncf` as the default coverage region
  - `sncf` region covers all SNCF trains across France
  - Other regions like `fr-idf` include local transport (metro, buses) but may have different access permissions

## Main Endpoints

### Journey Planning
```
GET /coverage/{region}/journeys?from={origin}&to={destination}&datetime={ISO8601}
```
Plan a journey between two points with real-time data.

### Next Departures
```
GET /coverage/{region}/stop_areas/{stop_id}/departures?from_datetime={ISO8601}
```
Get upcoming departures from a station.

### Next Arrivals
```
GET /coverage/{region}/stop_areas/{stop_id}/arrivals?from_datetime={ISO8601}
```
Get upcoming arrivals at a station.

### Stop Schedules
```
GET /coverage/{region}/stop_areas/{stop_id}/stop_schedules?from_datetime={ISO8601}
```
Get detailed schedules for a specific stop.

### Places Search
```
GET /coverage/{region}/places?q={search_query}
```
Search for stations, stops, and addresses (autocomplete).

### Coverage Regions
```
GET /coverage
```
List available coverage regions (e.g., "fr-idf" for Île-de-France).

## Key Parameters

- **datetime**: ISO 8601 format `YYYYMMDDTHHmmss` (e.g., `20260207T143000`)
- **from/to**: Coordinates `longitude;latitude` or object IDs like `stop_area:SNCF:87686006`
- **region**: Coverage region (e.g., `fr-idf`, `fr-ne`, `sandbox` for testing)
- **data_freshness**: `realtime` (default) or `base_schedule`
- **count**: Number of results to return (default: 10)
- **depth**: Level of detail in response (0-3)

## Instructions

When users request train information:

1. **Ask for API token** if not provided:
   - Users need to register at https://www.navitia.io/ to get a free API token
   - Store it securely (suggest using environment variable `NAVITIA_API_TOKEN`)

2. **Identify the region**:
   - Default to `sncf` region for SNCF train queries
   - Other regions: `fr-idf` (Paris+Ile-de-France local transport), `fr-ne`, `fr-nw`, etc.
   - Use `/coverage` endpoint to see available regions
   - Most SNCF train stations are accessible via the `sncf` region

3. **Search for locations**:
   - Use `/places` endpoint to find station IDs
   - Show top results and ask user to confirm the right station

4. **Format datetime**:
   - Convert natural language ("tomorrow at 3pm") to ISO 8601 format
   - Use `YYYYMMDDTHHmmss` format (e.g., `20260207T150000`)
   - If no time specified, use current time

5. **Make API requests**:
   - **ALWAYS use header authentication**: `curl -H "Authorization: $NAVITIA_API_TOKEN" "URL"`
   - Read token from environment: Check `NAVITIA_API_TOKEN` env var or source `.env` file
   - For complex queries: Create script files in scratchpad directory with token embedded
   - Save JSON responses to files before parsing to avoid piping issues
   - **Common errors**:
     - "no token" error → Token not properly passed or auth format incorrect
     - "permission denied" → Wrong region or token doesn't have access
     - Empty response → Check if endpoint exists and parameters are correct
   - Include helpful error messages if requests fail
   - Parse JSON responses and present in readable format with proper time formatting

6. **Present results clearly**:
   - **Time format**: Parse `YYYYMMDDTHHmmss` as `HH:MM` (extract positions 9-10 and 11-12)
   - For journeys: Show departure/arrival times, duration, transfers, CO2 emissions
   - For departures/arrivals: Show time, line, direction, platform, real-time status
   - Use emoji and formatting for better readability (🚆 for trains, ⏰ for time, etc.)
   - Highlight recommended options (fastest, direct, etc.)
   - Include delays or disruptions if present in the response
   - Remove city names from station labels for cleaner display (e.g., "Lyon Part Dieu (Lyon)" → "Lyon Part Dieu")

7. **Save results for later reference** (when users request journey planning):
   - Save journey results to `results/` folder with timestamp
   - **Filename format**: `results/YYYY-MM-DD_HHMM_origin-destination.txt`
   - **Example**: `results/2026-02-08_1430_Paris-Marseille.txt`
   - Include formatted journey details (times, transfers, CO2, train info)
   - Add metadata footer (search date/time, query details)
   - The `results/` folder is gitignored - search history stays private
   - Users can review past searches with `ls results/` or `cat results/filename.txt`

## Examples

### Example 1: Next departures from Paris Gare de Lyon
```bash
# First, find the station ID
curl -H "Authorization: $NAVITIA_API_TOKEN" "https://api.navitia.io/v1/coverage/sncf/places?q=paris%20gare%20de%20lyon"

# Then get departures
curl -H "Authorization: $NAVITIA_API_TOKEN" "https://api.navitia.io/v1/coverage/sncf/stop_areas/stop_area:SNCF:87686006/departures?from_datetime=20260207T140000&count=5"
```

### Example 2: Journey from Paris to Lyon
```bash
# Search for origin and destination
curl -H "Authorization: $NAVITIA_API_TOKEN" "https://api.navitia.io/v1/coverage/sncf/places?q=paris"
curl -H "Authorization: $NAVITIA_API_TOKEN" "https://api.navitia.io/v1/coverage/sncf/places?q=lyon"

# Plan journey
curl -H "Authorization: $NAVITIA_API_TOKEN" "https://api.navitia.io/v1/coverage/sncf/journeys?from=2.373543;48.844421&to=4.832011;45.760220&datetime=20260207T180000"
```

### Example 3: Real-time arrivals at a station
```bash
curl -H "Authorization: $NAVITIA_API_TOKEN" "https://api.navitia.io/v1/coverage/sncf/stop_areas/stop_area:SNCF:87686006/arrivals?from_datetime=20260207T140000&data_freshness=realtime&count=10"
```

### Example 4: Multi-step journey planning (recommended approach)
```bash
#!/bin/bash
TOKEN="$NAVITIA_API_TOKEN"

# Step 1: Search for stations and save results
curl -H "Authorization: $TOKEN" "https://api.navitia.io/v1/coverage/sncf/places?q=paris%20gare%20de%20lyon" > /tmp/origin.json
curl -H "Authorization: $TOKEN" "https://api.navitia.io/v1/coverage/sncf/places?q=marseille" > /tmp/dest.json

# Step 2: Extract station IDs
ORIGIN_ID=$(python3 -c "import json; print([p['id'] for p in json.load(open('/tmp/origin.json'))['places'] if p.get('embedded_type')=='stop_area'][0])")
DEST_ID=$(python3 -c "import json; print([p['id'] for p in json.load(open('/tmp/dest.json'))['places'] if p.get('embedded_type')=='stop_area'][0])")

# Step 3: Plan journey and save to file
DATETIME="20260208T110000"
curl -H "Authorization: $TOKEN" "https://api.navitia.io/v1/coverage/sncf/journeys?from=$ORIGIN_ID&to=$DEST_ID&datetime=$DATETIME&count=3" > /tmp/journey.json

# Step 4: Parse and format results
python3 << 'EOF'
import json
with open('/tmp/journey.json') as f:
    data = json.load(f)
    for journey in data.get('journeys', [])[:3]:
        # Format output here
        pass
EOF
```

## Practical Implementation Patterns

### Pattern 1: Using Script Files for Complex Queries
For multi-step operations, create bash scripts in the scratchpad directory:
```bash
# Create reusable script
cat > /tmp/scratchpad/query.sh << 'EOF'
#!/bin/bash
TOKEN="your-token-here"
curl -H "Authorization: $TOKEN" "URL_HERE"
EOF
chmod +x /tmp/scratchpad/query.sh
./tmp/scratchpad/query.sh
```

### Pattern 2: Token Management
```bash
# Option 1: Source from .env file
source .env && curl -H "Authorization: $NAVITIA_API_TOKEN" "URL"

# Option 2: Inline in script
TOKEN="$NAVITIA_API_TOKEN"
curl -H "Authorization: $TOKEN" "URL"

# Option 3: Read from environment in script file
#!/bin/bash
TOKEN="${NAVITIA_API_TOKEN}"
```

### Pattern 3: Parsing API Responses
```python
import json

# Load response
with open('response.json') as f:
    data = json.load(f)

# Extract time from YYYYMMDDTHHMMSS format
def format_time(dt_str):
    return f"{dt_str[9:11]}:{dt_str[11:13]}"

# Extract station names (remove city suffix)
def clean_station_name(name):
    return name.replace(' (Lyon)', '').replace(' (Paris)', '')

# Process journeys
for journey in data.get('journeys', []):
    dep_time = format_time(journey['departure_date_time'])
    arr_time = format_time(journey['arrival_date_time'])
    duration_min = journey['duration'] // 60
```

## Guidelines

- **Always authenticate**: Include the API token in every request
- **Handle errors gracefully**: Check for 401 (invalid token), 404 (not found), rate limits
- **Use real-time data**: Default to `data_freshness=realtime` for current information
- **Format output**: Make schedules easy to read with times, platforms, and delays
- **Privacy**: Don't log or expose API tokens in responses
- **Caching**: API responses are cached for 1 minute; mention if data might be slightly outdated
- **Rate limits**: Be respectful of API limits; don't make excessive requests
- **Region-specific**: France coverage is comprehensive; international journeys may be limited

## Common Station IDs (for quick reference)

### Paris Stations
- **Paris Gare de Lyon**: `stop_area:SNCF:87686006`
- **Paris Gare du Nord**: `stop_area:SNCF:87271007`
- **Paris Montparnasse**: `stop_area:SNCF:87391003`

### Lyon Stations
- **Lyon Part-Dieu**: `stop_area:SNCF:87723197`
- **Lyon Perrache**: `stop_area:SNCF:87722025`
- **Lyon Vaise**: `stop_area:SNCF:87721001`

### Other Major Cities
- **Marseille Saint-Charles**: `stop_area:SNCF:87751008`
- **Bordeaux Saint-Jean**: `stop_area:SNCF:87581009`

(Use `/places` search to find other stations - most station searches work well with city name + "gare" or main station name)

## Response Format

Parse JSON responses and extract:
- **Journeys**: `journeys[].sections[].{from, to, departure_date_time, arrival_date_time, type, mode}`
- **Departures**: `departures[].{route.name, stop_date_time.departure_date_time, display_informations.{direction, code}}`
- **Arrivals**: `arrivals[].{route.name, stop_date_time.arrival_date_time, display_informations.{direction, code}}`

## Testing

Use the sandbox region for testing without impacting production:
```bash
curl -H "Authorization: $NAVITIA_API_TOKEN" "https://api.navitia.io/v1/coverage/sandbox"
```

## Troubleshooting

### "no token" Error
**Symptoms**: API returns `{"message":"no token. You can get one at http://www.navitia.io..."}`

**Solutions**:
1. Verify token is set: `echo $NAVITIA_API_TOKEN`
2. Use header authentication (NOT basic auth `-u`): `curl -H "Authorization: $TOKEN" "URL"`
3. If using separate Bash commands, token doesn't persist - use script files or source .env in same command
4. Check token is not wrapped in quotes in the header

### "permission denied" or 403 Error
**Symptoms**: Cannot access certain regions or endpoints

**Solutions**:
1. Try using `sncf` region instead of `fr-idf` or other regional codes
2. Check your token has the necessary permissions at https://www.navitia.io/
3. Verify the endpoint URL is correct (check for typos in region or stop_area IDs)

### Empty or Unexpected JSON Response
**Symptoms**: API returns empty `places` array or no results

**Solutions**:
1. Verify station name spelling (try alternative names: "gare de lyon" vs "lyon")
2. Check if searching in correct region (`sncf` covers all SNCF stations)
3. Try broader search terms (city name instead of full station name)
4. Use URL encoding for special characters (é → %C3%A9 or use `%20` for spaces)

### Time Parsing Issues
**Symptoms**: Times display incorrectly or as "T1:10" instead of "11:10"

**Solutions**:
1. Parse datetime string `YYYYMMDDTHHmmss` by extracting:
   - Hours: characters 9-10 (positions in string starting from 0)
   - Minutes: characters 11-12
2. Example: `20260208T110000` → Hours=`11`, Minutes=`00`
3. Use Python slicing: `dt_str[9:11] + ":" + dt_str[11:13]`

### Token Not Persisting Between Commands
**Symptoms**: First command works, subsequent commands fail with "no token"

**Solutions**:
1. **Best approach**: Create a script file with token embedded
2. **Alternative**: Chain commands with `&&` in single Bash call
3. **Alternative**: Source .env file within the same command: `source .env && curl...`

## Additional Resources

- API Documentation: https://doc.navitia.io/
- Register for API token: https://www.navitia.io/
- Coverage regions: https://api.navitia.io/v1/coverage
