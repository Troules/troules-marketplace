#!/bin/bash
# SessionStart hook: Verify NAVITIA_API_TOKEN is available
# Non-blocking — always exits 0, warns if token missing

# Check env var first
if [ -n "$NAVITIA_API_TOKEN" ]; then
    exit 0
fi

# Try sourcing .env from project root
PLUGIN_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
if [ -f "$PLUGIN_ROOT/.env" ]; then
    # shellcheck source=/dev/null
    source "$PLUGIN_ROOT/.env" 2>/dev/null
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
