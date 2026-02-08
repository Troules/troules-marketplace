#!/bin/bash

# SNCF/Navitia API Test Script
# This script tests your API token and demonstrates basic API calls

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=================================="
echo "SNCF/Navitia API Test Script"
echo "=================================="
echo ""

# Check if API token is set
if [ -z "$NAVITIA_API_TOKEN" ]; then
    echo -e "${RED}Error: NAVITIA_API_TOKEN environment variable is not set${NC}"
    echo ""
    echo "Please set your API token:"
    echo "  export NAVITIA_API_TOKEN='your-token-here'"
    echo ""
    echo "Get your token at: https://www.navitia.io/"
    exit 1
fi

echo -e "${GREEN}✓${NC} API token found"
echo ""

# Test 1: Check coverage
echo "Test 1: Checking available coverage regions..."
COVERAGE=$(curl -s -H "Authorization: $NAVITIA_API_TOKEN" "https://api.navitia.io/v1/coverage" 2>&1)

if echo "$COVERAGE" | grep -q "regions"; then
    echo -e "${GREEN}✓${NC} Coverage endpoint working"
    echo "Available regions:"
    echo "$COVERAGE" | grep -o '"id":"[^"]*"' | head -5 | sed 's/"id":"\([^"]*\)"/  - \1/'
else
    echo -e "${RED}✗${NC} Coverage endpoint failed"
    echo "Response: $COVERAGE"
    exit 1
fi
echo ""

# Test 2: Search for a station
echo "Test 2: Searching for Paris Gare de Lyon..."
STATION=$(curl -s -H "Authorization: $NAVITIA_API_TOKEN" "https://api.navitia.io/v1/coverage/sncf/places?q=paris%20gare%20de%20lyon" 2>&1)

if echo "$STATION" | grep -q "places"; then
    echo -e "${GREEN}✓${NC} Places search working"
    STATION_ID=$(echo "$STATION" | grep -o '"id":"stop_area:SNCF:[^"]*"' | head -1 | sed 's/"id":"\([^"]*\)"/\1/')
    if [ -n "$STATION_ID" ]; then
        echo "Found station ID: $STATION_ID"
    fi
else
    echo -e "${YELLOW}⚠${NC} Places search returned unexpected response"
    echo "Response preview: $(echo "$STATION" | head -c 200)"
fi
echo ""

# Test 3: Get departures (if we found a station)
if [ -n "$STATION_ID" ]; then
    echo "Test 3: Getting next departures from $STATION_ID..."
    DATETIME=$(date -u +"%Y%m%dT%H%M%S")
    DEPARTURES=$(curl -s -H "Authorization: $NAVITIA_API_TOKEN" "https://api.navitia.io/v1/coverage/sncf/stop_areas/$STATION_ID/departures?from_datetime=$DATETIME&count=3" 2>&1)

    if echo "$DEPARTURES" | grep -q "departures"; then
        echo -e "${GREEN}✓${NC} Departures endpoint working"
        DEPARTURE_COUNT=$(echo "$DEPARTURES" | grep -o '"display_informations"' | wc -l)
        echo "Found $DEPARTURE_COUNT upcoming departures"
    else
        echo -e "${YELLOW}⚠${NC} Departures endpoint returned unexpected response"
    fi
else
    echo "Test 3: Skipped (no station ID found)"
fi
echo ""

# Test 4: Check rate limit headers (optional)
echo "Test 4: Checking API rate limits..."
RATE_LIMIT=$(curl -s -I -H "Authorization: $NAVITIA_API_TOKEN" "https://api.navitia.io/v1/coverage" 2>&1 | grep -i "x-ratelimit" || true)

if [ -n "$RATE_LIMIT" ]; then
    echo -e "${GREEN}✓${NC} Rate limit information:"
    echo "$RATE_LIMIT" | while IFS= read -r line; do
        echo "  $line"
    done
else
    echo -e "${YELLOW}⚠${NC} No rate limit headers found"
fi
echo ""

echo "=================================="
echo -e "${GREEN}All tests completed!${NC}"
echo "=================================="
echo ""
echo "Your API token is working correctly."
echo "You can now use the SNCF Train Schedule skill with Claude."
echo ""
echo "Try asking Claude:"
echo '  "Show me next trains from Paris Gare de Lyon"'
echo '  "Plan a journey from Paris to Lyon"'
echo ""

exit 0
