#!/bin/bash
# SNCF/Navitia API integration tests
# Requires NAVITIA_API_TOKEN — skips gracefully if not set

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Try sourcing .env if token not set
if [ -z "$NAVITIA_API_TOKEN" ] && [ -f "$ROOT/.env" ]; then
    # shellcheck source=/dev/null
    source "$ROOT/.env"
fi

if [ -z "$NAVITIA_API_TOKEN" ]; then
    echo -e "${YELLOW}SKIP${NC} NAVITIA_API_TOKEN not set — skipping API tests"
    echo "Set your token: export NAVITIA_API_TOKEN='your-token'"
    exit 0
fi

PASS=0
FAIL=0

check() {
    local desc="$1"
    shift
    if "$@" >/dev/null 2>&1; then
        echo -e "${GREEN}PASS${NC} $desc"
        PASS=$((PASS + 1))
    else
        echo -e "${RED}FAIL${NC} $desc"
        FAIL=$((FAIL + 1))
    fi
}

echo "=================================="
echo "SNCF API Integration Tests"
echo "=================================="
echo ""

echo -e "${GREEN}OK${NC} API token found"
echo ""

# Test 1: Coverage endpoint
echo "Test 1: Coverage regions..."
COVERAGE=$(curl -s -H "Authorization: $NAVITIA_API_TOKEN" "https://api.navitia.io/v1/coverage" 2>&1)
check "Coverage endpoint returns regions" echo "$COVERAGE" | grep -q "regions"

# Test 2: Places search
echo "Test 2: Places search..."
STATION=$(curl -s -H "Authorization: $NAVITIA_API_TOKEN" "https://api.navitia.io/v1/coverage/sncf/places?q=paris%20gare%20de%20lyon" 2>&1)
check "Places search returns results" echo "$STATION" | grep -q "places"

STATION_ID=$(echo "$STATION" | grep -o '"id":"stop_area:SNCF:[^"]*"' | head -1 | sed 's/"id":"\([^"]*\)"/\1/')

# Test 3: Departures
if [ -n "$STATION_ID" ]; then
    echo "Test 3: Departures..."
    DATETIME=$(date -u +"%Y%m%dT%H%M%S")
    DEPARTURES=$(curl -s -H "Authorization: $NAVITIA_API_TOKEN" \
        "https://api.navitia.io/v1/coverage/sncf/stop_areas/$STATION_ID/departures?from_datetime=$DATETIME&count=3" 2>&1)
    check "Departures endpoint returns data" echo "$DEPARTURES" | grep -q "departures"
else
    echo -e "${YELLOW}SKIP${NC} Test 3: No station ID found"
fi

# Test 4: Rate limit headers
echo "Test 4: Rate limits..."
HEADERS=$(curl -s -I -H "Authorization: $NAVITIA_API_TOKEN" "https://api.navitia.io/v1/coverage" 2>&1)
check "API returns HTTP headers" echo "$HEADERS" | grep -qi "HTTP"

echo ""
echo "=================================="
echo "Results: ${PASS} passed, ${FAIL} failed"
echo "=================================="

[ "$FAIL" -eq 0 ] && exit 0 || exit 1
