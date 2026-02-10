#!/usr/bin/env python3
"""
Get departures from an SNCF station.

Usage:
    python get_departures.py "stop_area:SNCF:87686006"
    python get_departures.py "stop_area:SNCF:87686006" --count 5 --datetime "20260210T140000"
"""

import argparse
import json
import os
import sys
from datetime import datetime

try:
    import requests
except ImportError:
    print("❌ Error: 'requests' package not found", file=sys.stderr)
    print("Install with: pip install requests", file=sys.stderr)
    sys.exit(1)


def get_departures(station_id, api_token, count=10, from_datetime=None, data_freshness="realtime"):
    """
    Get departures from a station.

    Args:
        station_id: Station ID (e.g., "stop_area:SNCF:87686006")
        api_token: Navitia API token
        count: Number of departures to return
        from_datetime: Starting datetime in YYYYMMDDTHHmmss format (None = now)
        data_freshness: "realtime" or "base_schedule"

    Returns:
        List of departure dictionaries
    """
    url = f"https://api.sncf.com/v1/coverage/sncf/stop_areas/{station_id}/departures"
    params = {
        "count": count,
        "data_freshness": data_freshness
    }
    if from_datetime:
        params["from_datetime"] = from_datetime

    headers = {"Authorization": api_token}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        departures = data.get("departures", [])
        if not departures:
            print(f"⚠️  No departures found for station '{station_id}'", file=sys.stderr)
            if from_datetime:
                print(f"Try a different datetime or check the station ID", file=sys.stderr)
            return []

        return departures

    except requests.exceptions.Timeout:
        print("❌ API timeout - network may be slow", file=sys.stderr)
        print("Retry the request or check your connection", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("❌ Invalid API token", file=sys.stderr)
            print("Get a token at: https://numerique.sncf.com/startup/api/token-developpeur/", file=sys.stderr)
            print("Set it with: export NAVITIA_API_TOKEN='your-token'", file=sys.stderr)
        elif e.response.status_code == 404:
            print(f"❌ Station ID '{station_id}' not found", file=sys.stderr)
            print("Search stations with: python scripts/search_stations.py 'name'", file=sys.stderr)
        else:
            print(f"❌ API error: HTTP {e.response.status_code}", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}", file=sys.stderr)
        sys.exit(1)


def format_datetime(dt_string):
    """Convert YYYYMMDDTHHmmss to readable format."""
    try:
        dt = datetime.strptime(dt_string, "%Y%m%dT%H%M%S")
        return dt.strftime("%H:%M")
    except:
        return dt_string


def format_output(departures, output_format="human"):
    """Format departure results for display."""
    if output_format == "json":
        return json.dumps(departures, indent=2, ensure_ascii=False)

    # Human-readable format
    output = []
    for i, dep in enumerate(departures, 1):
        # Extract key information
        route = dep.get("route", {})
        display_info = dep.get("display_informations", {})
        stop_point = dep.get("stop_point", {})

        line = display_info.get("code", "?")
        direction = display_info.get("direction", "Unknown")
        dep_time = format_datetime(dep.get("stop_date_time", {}).get("departure_date_time", ""))

        output.append(f"{i}. [{line}] → {direction}")
        output.append(f"   Departure: {dep_time}")

        # Show delay if in realtime mode
        if "stop_date_time" in dep:
            base_time = dep["stop_date_time"].get("base_departure_date_time")
            actual_time = dep["stop_date_time"].get("departure_date_time")
            if base_time and actual_time and base_time != actual_time:
                output.append(f"   ⚠️  Delayed (scheduled: {format_datetime(base_time)})")

        output.append("")

    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="Get departures from an SNCF station",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python get_departures.py "stop_area:SNCF:87686006"
  python get_departures.py "stop_area:SNCF:87686006" --count 5
  python get_departures.py "stop_area:SNCF:87686006" --datetime "20260210T140000"
  python get_departures.py "stop_area:SNCF:87686006" --format json
        """
    )
    parser.add_argument("station_id", help="Station ID (e.g., stop_area:SNCF:87686006)")
    parser.add_argument("--count", type=int, default=10,
                       help="Number of departures (default: 10)")
    parser.add_argument("--datetime", dest="from_datetime",
                       help="Starting datetime in YYYYMMDDTHHmmss format")
    parser.add_argument("--data-freshness", choices=["realtime", "base_schedule"],
                       default="realtime", help="Data freshness (default: realtime)")
    parser.add_argument("--format", choices=["human", "json"], default="human",
                       help="Output format (default: human)")

    args = parser.parse_args()

    # Get API token from environment
    api_token = os.getenv("NAVITIA_API_TOKEN")
    if not api_token:
        print("❌ NAVITIA_API_TOKEN environment variable not set", file=sys.stderr)
        print("Set it with: export NAVITIA_API_TOKEN='your-token'", file=sys.stderr)
        print("Get a token at: https://numerique.sncf.com/startup/api/token-developpeur/", file=sys.stderr)
        sys.exit(1)

    # Get departures
    departures = get_departures(
        args.station_id,
        api_token,
        args.count,
        args.from_datetime,
        args.data_freshness
    )

    if departures:
        print(format_output(departures, args.format))
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
