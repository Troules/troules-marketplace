#!/usr/bin/env python3
"""
Validate that a station ID exists and is accessible via the API.

Usage:
    python validate_station_id.py "stop_area:SNCF:87686006"
"""

import argparse
import os
import sys

try:
    import requests
except ImportError:
    print("❌ Error: 'requests' package not found", file=sys.stderr)
    print("Install with: pip install requests", file=sys.stderr)
    sys.exit(1)


def validate_station_id(station_id, api_token):
    """
    Validate a station ID by fetching its details from the API.

    Args:
        station_id: Station ID to validate (e.g., "stop_area:SNCF:87686006")
        api_token: Navitia API token

    Returns:
        True if valid, False otherwise
    """
    # Remove any surrounding whitespace or quotes
    station_id = station_id.strip().strip("'\"")

    # Check format
    if not station_id.startswith("stop_area:"):
        print(f"❌ Invalid format: '{station_id}'", file=sys.stderr)
        print("Station IDs should start with 'stop_area:'", file=sys.stderr)
        print("Example: stop_area:SNCF:87686006", file=sys.stderr)
        return False

    # Try to fetch station details
    url = f"https://api.sncf.com/v1/coverage/sncf/stop_areas/{station_id}"
    headers = {"Authorization": api_token}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Check if we got stop_areas back
        stop_areas = data.get("stop_areas", [])
        if not stop_areas:
            print(f"❌ Station ID not found: '{station_id}'", file=sys.stderr)
            print("Search for stations with: python scripts/search_stations.py 'name'", file=sys.stderr)
            return False

        # Valid station found
        station = stop_areas[0]
        name = station.get("name", "Unknown")
        print(f"✅ Valid station: {name}")
        print(f"   ID: {station_id}")

        # Show coordinates if available
        if "coord" in station:
            coord = station["coord"]
            lon = coord.get("lon")
            lat = coord.get("lat")
            print(f"   Coordinates: {lon};{lat}")

        return True

    except requests.exceptions.Timeout:
        print("❌ API timeout - network may be slow", file=sys.stderr)
        print("Retry the validation or check your connection", file=sys.stderr)
        return False
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("❌ Invalid API token", file=sys.stderr)
            print("Get a token at: https://numerique.sncf.com/startup/api/token-developpeur/", file=sys.stderr)
            print("Set it with: export NAVITIA_API_TOKEN='your-token'", file=sys.stderr)
        elif e.response.status_code == 404:
            print(f"❌ Station ID not found: '{station_id}'", file=sys.stderr)
            print("Search for stations with: python scripts/search_stations.py 'name'", file=sys.stderr)
        else:
            print(f"❌ API error: HTTP {e.response.status_code}", file=sys.stderr)
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Validate an SNCF station ID",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python validate_station_id.py "stop_area:SNCF:87686006"
  python validate_station_id.py stop_area:SNCF:87722025
        """
    )
    parser.add_argument("station_id", help="Station ID to validate")

    args = parser.parse_args()

    # Get API token from environment
    api_token = os.getenv("NAVITIA_API_TOKEN")
    if not api_token:
        print("❌ NAVITIA_API_TOKEN environment variable not set", file=sys.stderr)
        print("Set it with: export NAVITIA_API_TOKEN='your-token'", file=sys.stderr)
        print("Get a token at: https://numerique.sncf.com/startup/api/token-developpeur/", file=sys.stderr)
        sys.exit(1)

    # Validate station ID
    is_valid = validate_station_id(args.station_id, api_token)
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
