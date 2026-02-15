# SNCF/Navitia API Reference

Detailed API documentation, examples, and troubleshooting for the SNCF Train Schedule plugin.

## Common Station IDs

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

Use `/places` search with city name + "gare" to find other stations.

## Curl Examples

### Example 1: Next Departures from Paris Gare de Lyon
```bash
# Find station ID
curl -H "Authorization: $NAVITIA_API_TOKEN" \
  "https://api.navitia.io/v1/coverage/sncf/places?q=paris%20gare%20de%20lyon"

# Get departures
curl -H "Authorization: $NAVITIA_API_TOKEN" \
  "https://api.navitia.io/v1/coverage/sncf/stop_areas/stop_area:SNCF:87686006/departures?from_datetime=20260207T140000&count=5"
```

### Example 2: Journey from Paris to Lyon
```bash
# Search for origin and destination
curl -H "Authorization: $NAVITIA_API_TOKEN" \
  "https://api.navitia.io/v1/coverage/sncf/places?q=paris"
curl -H "Authorization: $NAVITIA_API_TOKEN" \
  "https://api.navitia.io/v1/coverage/sncf/places?q=lyon"

# Plan journey
curl -H "Authorization: $NAVITIA_API_TOKEN" \
  "https://api.navitia.io/v1/coverage/sncf/journeys?from=2.373543;48.844421&to=4.832011;45.760220&datetime=20260207T180000"
```

### Example 3: Real-time Arrivals
```bash
curl -H "Authorization: $NAVITIA_API_TOKEN" \
  "https://api.navitia.io/v1/coverage/sncf/stop_areas/stop_area:SNCF:87686006/arrivals?from_datetime=20260207T140000&data_freshness=realtime&count=10"
```

### Example 4: Multi-step Journey Planning (Recommended Approach)
```bash
#!/bin/bash
TOKEN="$NAVITIA_API_TOKEN"

# Step 1: Search for stations and save results
curl -H "Authorization: $TOKEN" \
  "https://api.navitia.io/v1/coverage/sncf/places?q=paris%20gare%20de%20lyon" > /tmp/origin.json
curl -H "Authorization: $TOKEN" \
  "https://api.navitia.io/v1/coverage/sncf/places?q=marseille" > /tmp/dest.json

# Step 2: Extract station IDs
ORIGIN_ID=$(python3 -c "import json; print([p['id'] for p in json.load(open('/tmp/origin.json'))['places'] if p.get('embedded_type')=='stop_area'][0])")
DEST_ID=$(python3 -c "import json; print([p['id'] for p in json.load(open('/tmp/dest.json'))['places'] if p.get('embedded_type')=='stop_area'][0])")

# Step 3: Plan journey
DATETIME="20260208T110000"
curl -H "Authorization: $TOKEN" \
  "https://api.navitia.io/v1/coverage/sncf/journeys?from=$ORIGIN_ID&to=$DEST_ID&datetime=$DATETIME&count=3" > /tmp/journey.json

# Step 4: Parse results
python3 << 'EOF'
import json
with open('/tmp/journey.json') as f:
    data = json.load(f)
    for journey in data.get('journeys', [])[:3]:
        pass  # Format output here
EOF
```

## Implementation Patterns

### Pattern 1: Script Files for Complex Queries
For multi-step operations, create bash scripts:
```bash
cat > /tmp/scratchpad/query.sh << 'EOF'
#!/bin/bash
TOKEN="$NAVITIA_API_TOKEN"
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

with open('response.json') as f:
    data = json.load(f)

def format_time(dt_str):
    """Convert YYYYMMDDTHHMMSS to HH:MM"""
    return f"{dt_str[9:11]}:{dt_str[11:13]}"

def clean_station_name(name):
    """Remove city suffix from station names"""
    return name.replace(' (Lyon)', '').replace(' (Paris)', '')

for journey in data.get('journeys', []):
    dep_time = format_time(journey['departure_date_time'])
    arr_time = format_time(journey['arrival_date_time'])
    duration_min = journey['duration'] // 60
```

## Response Format (JSON Paths)

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
**Symptoms**: API returns `{"message":"no token..."}`

**Solutions**:
1. Verify token is set: `echo $NAVITIA_API_TOKEN`
2. Use header auth (NOT basic auth `-u`): `curl -H "Authorization: $TOKEN" "URL"`
3. Token doesn't persist between separate Bash commands — use script files or `source .env` in same command
4. Check token is not wrapped in extra quotes in the header

### "permission denied" or 403 Error
**Solutions**:
1. Try `sncf` region instead of `fr-idf` or other regional codes
2. Check token permissions at https://numerique.sncf.com/startup/api/token-developpeur/
3. Verify endpoint URL is correct (check for typos in region or stop_area IDs)

### Empty or Unexpected JSON Response
**Solutions**:
1. Verify station name spelling (try "gare de lyon" vs "lyon")
2. Check if searching in correct region (`sncf` covers all SNCF stations)
3. Try broader search terms (city name instead of full station name)
4. Use URL encoding for special characters (`%20` for spaces)

### Time Parsing Issues
**Symptoms**: Times display as "T1:10" instead of "11:10"

**Solutions**:
1. Parse `YYYYMMDDTHHmmss`: Hours = chars 9–10, Minutes = chars 11–12
2. Example: `20260208T110000` → `11:00`
3. Python: `dt_str[9:11] + ":" + dt_str[11:13]`

### Token Not Persisting Between Commands
**Solutions**:
1. Create a script file with token embedded (best approach)
2. Chain commands with `&&` in single Bash call
3. Source .env within the same command: `source .env && curl...`

## Additional Resources

- [Navitia API Documentation](https://doc.navitia.io/)
- [Register for API token](https://numerique.sncf.com/startup/api/token-developpeur/)
- [Coverage regions](https://api.navitia.io/v1/coverage)
