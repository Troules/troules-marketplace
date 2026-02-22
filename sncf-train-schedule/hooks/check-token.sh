#!/bin/bash
# PreToolUse hook: Verify NAVITIA_API_TOKEN is available
# Non-blocking — always exits 0, warns if token missing

# Only run for SNCF-related commands
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data.get('input', {}).get('command', ''))
except:
    print('')
" 2>/dev/null)

if ! echo "$COMMAND" | grep -qiE '(navitia|sncf|plan_journey|search_stations|get_departures|get_arrivals|validate_station|validate_datetime)'; then
    exit 0
fi

# Check env var first
if [ -n "$NAVITIA_API_TOKEN" ]; then
    exit 0
fi

# Try reading from .claude/sncf-train-schedule.local.md in the project directory
# This file persists across plugin updates and is gitignored
SETTINGS_FILE="$(pwd)/.claude/sncf-train-schedule.local.md"
if [ -f "$SETTINGS_FILE" ]; then
    TOKEN=$(grep '^navitia_api_token:' "$SETTINGS_FILE" | sed 's/navitia_api_token: *//' | tr -d '"'"'"' ')
    if [ -n "$TOKEN" ]; then
        export NAVITIA_API_TOKEN="$TOKEN"
        exit 0
    fi
fi

# Try sourcing .env from current working directory
if [ -f "$(pwd)/.env" ]; then
    # shellcheck source=/dev/null
    source "$(pwd)/.env" 2>/dev/null
    if [ -n "$NAVITIA_API_TOKEN" ]; then
        exit 0
    fi
fi

# Token not found — print warning to stderr
cat >&2 << 'EOF'
SNCF Plugin: NAVITIA_API_TOKEN not found.

To use the SNCF Train Schedule plugin, set your API token:
  export NAVITIA_API_TOKEN="your-token-here"

Or create a .env file in the plugin directory:
  echo 'NAVITIA_API_TOKEN=your-token-here' > .env

Get a free token at: https://www.navitia.io/
EOF

exit 0
