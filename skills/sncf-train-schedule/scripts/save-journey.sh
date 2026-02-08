#!/bin/bash
# Helper script to save journey results
# Usage: ./save-journey.sh "origin" "destination" "datetime" "results-file.txt"

TOKEN="${NAVITIA_API_TOKEN}"
FROM="$1"
TO="$2"
DATETIME="$3"
OUTPUT_FILE="${4:-results/$(date +%Y-%m-%d_%H%M)_journey.txt}"

if [ -z "$TOKEN" ]; then
    echo "Error: NAVITIA_API_TOKEN not set"
    echo "Please set it with: export NAVITIA_API_TOKEN='your-token'"
    exit 1
fi

if [ -z "$FROM" ] || [ -z "$TO" ] || [ -z "$DATETIME" ]; then
    echo "Usage: $0 <from_station_id> <to_station_id> <datetime_YYYYMMDDTHHMMSS> [output_file]"
    echo ""
    echo "Example:"
    echo "  $0 stop_area:SNCF:87723197 stop_area:SNCF:87726000 20260208T110000"
    exit 1
fi

# Create results directory if it doesn't exist
mkdir -p results

echo "Fetching journey from $FROM to $TO at $DATETIME..."

curl -s -H "Authorization: $TOKEN" \
    "https://api.navitia.io/v1/coverage/sncf/journeys?from=$FROM&to=$TO&datetime=$DATETIME&count=5" | \
    python3 << 'EOF' | tee "$OUTPUT_FILE"
import sys, json
from datetime import datetime

data = json.load(sys.stdin)

def format_time(dt_str):
    """Convert YYYYMMDDTHHMMSS to HH:MM"""
    return f"{dt_str[9:11]}:{dt_str[11:13]}"

def format_date(dt_str):
    """Convert YYYYMMDDTHHMMSS to readable date"""
    return f"{dt_str[6:8]}/{dt_str[4:6]}/{dt_str[0:4]}"

print("╔═══════════════════════════════════════════════════════════════╗")
print("║              SNCF Journey Search Results                      ║")
print("╚═══════════════════════════════════════════════════════════════╝\n")

if data.get('journeys'):
    first = data['journeys'][0]
    print(f"Search Date: {format_date(first['requested_date_time'])}")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

for idx, journey in enumerate(data.get('journeys', [])[:5], 1):
    duration_sec = journey.get('duration', 0)
    duration_min = duration_sec // 60
    duration_h = duration_min // 60
    duration_m = duration_min % 60

    dep_time = journey.get('departure_date_time', '')
    arr_time = journey.get('arrival_date_time', '')
    transfers = journey.get('nb_transfers', 0)
    co2 = journey.get('co2_emission', {}).get('value', 0)

    print(f"{'═' * 63}")
    print(f"Option {idx}: {'⭐ RECOMMENDED' if journey.get('type') == 'best' else 'Alternative'}")
    print(f"{'═' * 63}")
    print(f"🕐 Depart:  {format_time(dep_time)}")
    print(f"🕐 Arrive:  {format_time(arr_time)}")
    print(f"⏱️  Duration: {duration_h}h {duration_m:02d}min")
    print(f"🔄 Transfers: {transfers}")
    print(f"🌱 CO2: {co2:.0f}g")

    print(f"\n📍 Route Details:")
    for section in journey.get('sections', []):
        sec_type = section.get('type', '')
        if sec_type == 'public_transport':
            from_name = section.get('from', {}).get('name', '').split(' (')[0]
            to_name = section.get('to', {}).get('name', '').split(' (')[0]
            line = section.get('display_informations', {}).get('code', 'N/A')
            commercial_mode = section.get('display_informations', {}).get('commercial_mode', 'Train')
            dep = section.get('departure_date_time', '')
            arr = section.get('arrival_date_time', '')
            print(f"\n  🚆 {commercial_mode} {line}")
            print(f"     └─ {from_name} ({format_time(dep)}) → {to_name} ({format_time(arr)})")
        elif sec_type == 'transfer' or sec_type == 'waiting':
            duration = section.get('duration', 0) // 60
            if duration > 0:
                transfer_type = section.get('transfer_type', 'connection')
                print(f"     🔄 {transfer_type.title()}: {duration} min")

    print()

print(f"{'═' * 63}")
print(f"Total options: {len(data.get('journeys', []))}")
print(f"{'═' * 63}")
EOF

echo ""
echo "✅ Results saved to: $OUTPUT_FILE"
