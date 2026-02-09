#!/usr/bin/env python3
"""
Plan a journey between two SNCF stations.

Usage:
    python plan_journey.py "stop_area:SNCF:87686006" "stop_area:SNCF:87722025"
    python plan_journey.py "2.3522;48.8566" "4.8357;45.7640" --datetime "20260210T140000"
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


def plan_journey(from_location, to_location, api_token, datetime_param=None,
                 datetime_represents="departure", count=5, data_freshness="realtime"):
    """
    Plan a journey between two locations.

    Args:
        from_location: Origin (station ID or lon;lat coordinates)
        to_location: Destination (station ID or lon;lat coordinates)
        api_token: Navitia API token
        datetime_param: Datetime in YYYYMMDDTHHmmss format (None = now)
        datetime_represents: "departure" or "arrival"
        count: Number of journey options to return
        data_freshness: "realtime" or "base_schedule"

    Returns:
        List of journey dictionaries
    """
    url = "https://api.sncf.com/v1/coverage/sncf/journeys"
    params = {
        "from": from_location,
        "to": to_location,
        "count": count,
        "data_freshness": data_freshness
    }

    if datetime_param:
        params["datetime"] = datetime_param
        params["datetime_represents"] = datetime_represents

    headers = {"Authorization": api_token}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()

        journeys = data.get("journeys", [])
        if not journeys:
            print(f"⚠️  No journeys found from '{from_location}' to '{to_location}'", file=sys.stderr)
            print("Check that both locations are valid station IDs or coordinates", file=sys.stderr)
            return []

        return journeys

    except requests.exceptions.Timeout:
        print("❌ API timeout - journey planning can take longer", file=sys.stderr)
        print("Retry the request or check your connection", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("❌ Invalid API token", file=sys.stderr)
            print("Get a token at: https://numerique.sncf.com/startup/api/token-developpeur/", file=sys.stderr)
            print("Set it with: export NAVITIA_API_TOKEN='your-token'", file=sys.stderr)
        elif e.response.status_code == 404:
            print(f"❌ Invalid location", file=sys.stderr)
            print("Locations should be station IDs (stop_area:SNCF:...) or coordinates (lon;lat)", file=sys.stderr)
        elif e.response.status_code == 400:
            try:
                error_data = e.response.json()
                error_msg = error_data.get("error", {}).get("message", "Bad request")
                print(f"❌ API error: {error_msg}", file=sys.stderr)
            except:
                print(f"❌ Bad request - check your parameters", file=sys.stderr)
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


def format_duration(seconds):
    """Convert seconds to readable duration."""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    if hours > 0:
        return f"{hours}h {minutes}min"
    return f"{minutes}min"


def format_output(journeys, output_format="human"):
    """Format journey results for display."""
    if output_format == "json":
        return json.dumps(journeys, indent=2, ensure_ascii=False)

    # Human-readable format
    output = []
    for i, journey in enumerate(journeys, 1):
        dep_time = format_datetime(journey.get("departure_date_time", ""))
        arr_time = format_datetime(journey.get("arrival_date_time", ""))
        duration = format_duration(journey.get("duration", 0))
        nb_transfers = journey.get("nb_transfers", 0)

        output.append(f"{'='*60}")
        output.append(f"Journey {i}: {dep_time} → {arr_time} ({duration})")
        output.append(f"Transfers: {nb_transfers}")
        output.append("")

        # Show sections (walking, train, etc.)
        sections = journey.get("sections", [])
        for j, section in enumerate(sections):
            section_type = section.get("type", "unknown")

            if section_type == "public_transport":
                display = section.get("display_informations", {})
                line = display.get("code", "?")
                direction = display.get("direction", "Unknown")
                from_stop = section.get("from", {}).get("name", "?")
                to_stop = section.get("to", {}).get("name", "?")
                dep = format_datetime(section.get("departure_date_time", ""))
                arr = format_datetime(section.get("arrival_date_time", ""))

                output.append(f"  {j+1}. [{line}] → {direction}")
                output.append(f"     {from_stop} ({dep}) → {to_stop} ({arr})")

            elif section_type == "transfer":
                duration_sec = section.get("duration", 0)
                transfer_type = section.get("transfer_type", "walking")
                output.append(f"  {j+1}. Transfer ({transfer_type}, {format_duration(duration_sec)})")

            elif section_type in ["waiting", "crow_fly"]:
                duration_sec = section.get("duration", 0)
                output.append(f"  {j+1}. {section_type.replace('_', ' ').title()} ({format_duration(duration_sec)})")

        output.append("")

    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="Plan a journey between two SNCF locations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Journey between station IDs
  python plan_journey.py "stop_area:SNCF:87686006" "stop_area:SNCF:87722025"

  # Journey between coordinates (Paris to Lyon)
  python plan_journey.py "2.3522;48.8566" "4.8357;45.7640"

  # Journey at specific time
  python plan_journey.py "stop_area:SNCF:87686006" "stop_area:SNCF:87722025" \\
      --datetime "20260210T140000"

  # Arrive by specific time
  python plan_journey.py "stop_area:SNCF:87686006" "stop_area:SNCF:87722025" \\
      --datetime "20260210T180000" --datetime-represents arrival

  # Get more journey options
  python plan_journey.py "stop_area:SNCF:87686006" "stop_area:SNCF:87722025" --count 10
        """
    )
    parser.add_argument("from_location",
                       help="Origin station ID or coordinates (lon;lat)")
    parser.add_argument("to_location",
                       help="Destination station ID or coordinates (lon;lat)")
    parser.add_argument("--datetime",
                       help="Datetime in YYYYMMDDTHHmmss format")
    parser.add_argument("--datetime-represents", choices=["departure", "arrival"],
                       default="departure",
                       help="What the datetime represents (default: departure)")
    parser.add_argument("--count", type=int, default=5,
                       help="Number of journey options (default: 5)")
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

    # Plan journey
    journeys = plan_journey(
        args.from_location,
        args.to_location,
        api_token,
        args.datetime,
        args.datetime_represents,
        args.count,
        args.data_freshness
    )

    if journeys:
        print(format_output(journeys, args.format))
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
