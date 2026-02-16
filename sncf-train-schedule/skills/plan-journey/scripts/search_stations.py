#!/usr/bin/env python3
"""
Search for SNCF station IDs by name.

Usage:
    python search_stations.py "Paris Gare de Lyon"
    python search_stations.py "Lyon" --count 10
"""

import argparse
import json
import os
import sys

try:
    import requests
except ImportError:
    print("❌ Error: 'requests' package not found", file=sys.stderr)
    print("Install with: pip install requests", file=sys.stderr)
    sys.exit(1)

from config import load_token
load_token()


def search_stations(query, api_token, count=10):
    """
    Search for stations matching the query.

    Args:
        query: Station name to search for
        api_token: Navitia API token
        count: Maximum number of results to return

    Returns:
        List of station dictionaries with id, name, and coordinates
    """
    url = "https://api.navitia.io/v1/coverage/sncf/places"
    params = {
        "q": query,
        "type[]": "stop_area",
        "count": count
    }
    headers = {"Authorization": api_token}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        places = data.get("places", [])
        if not places:
            print(f"⚠️  No stations found for '{query}'", file=sys.stderr)
            print("Try a different search term or check spelling", file=sys.stderr)
            return []

        stations = []
        for place in places:
            station = {
                "id": place.get("id"),
                "name": place.get("name"),
                "quality": place.get("quality", 0)
            }

            # Add coordinates if available
            if "stop_area" in place and "coord" in place["stop_area"]:
                coord = place["stop_area"]["coord"]
                station["coordinates"] = f"{coord.get('lon')};{coord.get('lat')}"

            stations.append(station)

        return stations

    except requests.exceptions.Timeout:
        print("❌ API timeout - network may be slow", file=sys.stderr)
        print("Retry the search or check your connection", file=sys.stderr)
        sys.exit(0)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("❌ Invalid API token", file=sys.stderr)
            print("Get a token at: https://numerique.sncf.com/startup/api/token-developpeur/", file=sys.stderr)
            print("Set it with: export NAVITIA_API_TOKEN='your-token'", file=sys.stderr)
        elif e.response.status_code == 400:
            print(f"❌ Invalid search query: '{query}'", file=sys.stderr)
        else:
            print(f"❌ API error: HTTP {e.response.status_code}", file=sys.stderr)
        sys.exit(0)
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}", file=sys.stderr)
        sys.exit(0)


def format_output(stations, output_format="human"):
    """Format station results for display."""
    if output_format == "json":
        return json.dumps(stations, indent=2, ensure_ascii=False)

    # Human-readable format
    output = []
    for i, station in enumerate(stations, 1):
        output.append(f"{i}. {station['name']}")
        output.append(f"   ID: {station['id']}")
        if "coordinates" in station:
            output.append(f"   Coordinates: {station['coordinates']}")
        output.append(f"   Quality: {station['quality']}")
        output.append("")

    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="Search for SNCF station IDs by name",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python search_stations.py "Paris Gare de Lyon"
  python search_stations.py "Lyon" --count 10 --format json
        """
    )
    parser.add_argument("query", help="Station name to search for")
    parser.add_argument("--count", type=int, default=10,
                       help="Maximum number of results (default: 10)")
    parser.add_argument("--format", choices=["human", "json"], default="human",
                       help="Output format (default: human)")

    args = parser.parse_args()

    # Get API token from environment
    api_token = os.getenv("NAVITIA_API_TOKEN")
    if not api_token:
        print("❌ NAVITIA_API_TOKEN environment variable not set", file=sys.stderr)
        print("Set it with: export NAVITIA_API_TOKEN='your-token'", file=sys.stderr)
        print("Get a token at: https://numerique.sncf.com/startup/api/token-developpeur/", file=sys.stderr)
        sys.exit(0)

    # Search for stations
    stations = search_stations(args.query, api_token, args.count)

    if stations:
        print(format_output(stations, args.format))
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
