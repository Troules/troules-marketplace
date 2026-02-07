# SNCF Train Schedule Checker - Claude Skill

A Claude skill for checking train schedules, departures, arrivals, and planning journeys using the SNCF/Navitia API.

## Overview

This skill enables Claude to help users:
- Check next departures and arrivals at French train stations
- Plan journeys between cities
- Get real-time train information with delays and disruptions
- Search for stations and stops
- View detailed train schedules

## Installation

### For Claude Code

1. Clone or copy this repository to your Claude skills directory:
   ```bash
   cd ~/.claude/skills/
   git clone https://github.com/Troules/sncf-train-schedule sncf-train-schedule
   ```

2. The skill will be automatically available in Claude Code

### For Claude Desktop

1. Add this folder to your Claude Desktop skills directory
2. Restart Claude Desktop

## Setup

### Get an API Token

1. Visit https://numerique.sncf.com/ressources/api/
2. Register for a free account
3. Get your API token (becomes active within 5 minutes)
4. Set it as an environment variable:
   ```bash
   export NAVITIA_API_TOKEN="your-token-here"
   ```

## Usage

Invoke the skill by asking Claude about French train schedules:

- "What are the next trains from Paris Gare de Lyon?"
- "Plan a journey from Paris to Marseille tomorrow at 3pm"
- "Show me arrivals at Marseille Saint-Charles station"
- "When is the next train to Bordeaux?"

## API Information

- **Provider**: SNCF / Navitia
- **Base URL**: https://api.navitia.io/v1/
- **Authentication**: HTTP Basic Auth (token as username)
- **Documentation**: https://doc.navitia.io/
- **Coverage**: Comprehensive French public transport, limited international

## Features

- ✅ Real-time departures and arrivals
- ✅ Journey planning with transfers
- ✅ Station search and autocomplete
- ✅ Delay and disruption information
- ✅ Platform and track information
- ✅ Multiple coverage regions across France
- ✅ **Saved search results** - Journey queries automatically saved for later reference

## Search Results History

All journey searches are automatically saved to the `results/` folder with timestamps. This allows you to:
- Review past searches and journey options
- Compare routes taken on different dates
- Keep a personal travel history
- Reference previous journey plans

**Location**: `results/YYYY-MM-DD_HHMM_origin-destination.txt`

**Example**: `results/2025-01-01_1430_Paris-Marseille.txt`

**Privacy**: The `results/` folder is gitignored - your search history stays private and won't be committed to version control.

### Viewing Saved Results

List your saved searches:
```bash
ls -lh results/
```

View a specific search:
```bash
cat results/2025-01-01_1430_Paris-Marseille.txt
```

### Using the Save Script

You can manually save journey results using the included script:
```bash
source .env  # Load your API token
./save-journey.sh <from_station_id> <to_station_id> <datetime> [output_file]

# Example:
./save-journey.sh stop_area:SNCF:87686006 stop_area:SNCF:87751008 20250101T143000
```

Or ask Claude to save results:
```
"Plan a journey from Paris to Marseille on January 1st at 2:30pm and save the results"
```

## Examples

### Check Next Departures
```
User: "Show me the next 5 trains from Paris Gare du Nord"
Claude: [Uses skill to fetch and display departures with times, destinations, platforms]
```

### Plan a Journey
```
User: "I need to get from Paris to Marseille tomorrow at 2pm"
Claude: [Uses skill to find journey options with times, transfers, and durations]
```

### Real-time Information
```
User: "Are there any delays at Marseille station right now?"
Claude: [Uses skill to check real-time arrivals/departures with delay information]
```

## Common Coverage Regions

- `fr-idf` - Île-de-France (Paris region)
- `fr-ne` - Northeast France
- `fr-nw` - Northwest France
- `fr-se` - Southeast France
- `fr-sw` - Southwest France
- `sandbox` - Testing environment

## Contributing

This is an open source skill. Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your improvements
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Resources

- [Navitia API Documentation](https://doc.navitia.io/)
- [Claude Skills Repository](https://github.com/anthropics/skills)
- [SNCF Official Site](https://www.sncf.com/)

## Support

For issues or questions:
- API issues: https://www.navitia.io/
- Skill issues: Open an issue in this repository
