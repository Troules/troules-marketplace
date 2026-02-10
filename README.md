# SNCF Train Schedule — Claude Code Plugin

A Claude Code plugin for checking French train schedules, departures, arrivals, and planning journeys using the SNCF/Navitia API.

## Installation

### Via Marketplace (recommended)

```bash
/plugin marketplace add Troules/sncf-train-schedule
/plugin install sncf-train-schedule
```

### Manual Install

```bash
git clone https://github.com/Troules/sncf-train-schedule
claude --plugin-dir ./sncf-train-schedule
```

Or add to your Claude Code settings to load automatically.

## Prerequisites

1. **API Token**: Register at https://numerique.sncf.com/startup/api/token-developpeur/ for a free token
2. Set the token as an environment variable:
   ```bash
   export NAVITIA_API_TOKEN="your-token-here"
   ```
   Or create a `.env` file in the plugin directory:
   ```bash
   echo 'NAVITIA_API_TOKEN=your-token-here' > .env
   ```

## Quick Start

Once installed, ask Claude about French trains:

- "What are the next trains from Paris Gare de Lyon?"
- "Plan a journey from Paris to Marseille tomorrow at 3pm"
- "Show me arrivals at Lyon Part-Dieu"
- "When is the next train to Bordeaux?"

## Features

- Real-time departures and arrivals
- Journey planning with transfers and CO2 emissions
- Station search and autocomplete
- Delay and disruption information
- Platform and track details
- Saved search results (private, gitignored `results/` folder)

## Plugin Structure

```
sncf-train-schedule/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest
├── skills/
│   └── sncf-train-schedule/
│       ├── SKILL.md             # Core skill instructions
│       ├── references/
│       │   └── api-reference.md # Detailed API docs
│       ├── examples/
│       │   └── usage-examples.md
│       └── scripts/
│           ├── save-journey.sh  # Journey result saver
│           └── test-api.sh      # API test script
├── hooks/
│   ├── hooks.json               # Hook manifest
│   ├── check-token.sh           # Token validation (SessionStart)
│   └── validate-bash-security.sh # Security check (PreToolUse)
├── tests/
│   ├── test-plugin-structure.sh # Structure validation
│   └── test-api-integration.sh  # API integration tests
├── .env.example
├── .gitignore
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
└── LICENSE
```

## Configuration

| Variable | Description | Required |
|----------|-------------|----------|
| `NAVITIA_API_TOKEN` | Navitia API token | Yes |

The plugin reads the token from the `NAVITIA_API_TOKEN` environment variable or a `.env` file.

## Search Results History

Journey searches are saved to `results/` with timestamps:
- **Format**: `results/YYYY-MM-DD_HHMM_origin-destination.txt`
- **Privacy**: The folder is gitignored — search history stays private

```bash
ls results/                    # List saved searches
cat results/2026-02-08_*.txt   # View specific results
```

## Testing

```bash
# Structure tests (no token needed)
bash tests/test-plugin-structure.sh

# API tests (requires token)
export NAVITIA_API_TOKEN="your-token"
bash tests/test-api-integration.sh
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License — see [LICENSE](LICENSE) for details.

## Resources

- [Navitia API Documentation](https://doc.navitia.io/)
- [SNCF Open Data](https://numerique.sncf.com/ressources/api/)

## Support

For issues or questions:
- Get API token: https://numerique.sncf.com/startup/api/token-developpeur/
- API documentation: https://doc.navitia.io/
- Plugin issues: Open an issue in this repository
