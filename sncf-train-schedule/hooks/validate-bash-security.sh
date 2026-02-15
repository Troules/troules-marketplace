#!/bin/bash
# PreToolUse hook (Bash): Warn if hardcoded API tokens appear in commands
# Non-blocking — always exits 0, warns on potential token exposure

# Read the tool input from stdin
INPUT=$(cat)

# Extract the command field from the JSON input
COMMAND=$(echo "$INPUT" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data.get('input', {}).get('command', ''))
except:
    print('')
" 2>/dev/null)

# Check for UUID-like patterns (common API token format)
# Navitia tokens look like: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
if echo "$COMMAND" | grep -qE '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'; then
    cat >&2 << 'EOF'
SNCF Plugin Security Warning: Possible hardcoded API token detected in command.

Use environment variables instead:
  curl -H "Authorization: $NAVITIA_API_TOKEN" "URL"

Or source from .env:
  source .env && curl -H "Authorization: $NAVITIA_API_TOKEN" "URL"
EOF
fi

exit 0
