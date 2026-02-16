# Troules Marketplace — Claude Code Plugins

A marketplace of Claude Code plugins by [Troules](https://github.com/Troules).

## Available Plugins

| Plugin | Description |
|--------|-------------|
| [sncf-train-schedule](#sncf-train-schedule) | Check French train schedules, departures, arrivals, and plan journeys using the SNCF/Navitia API |

---

## Installation

### Add the marketplace

```bash
/plugin marketplace add Troules/troules-marketplace
```

### Install a plugin

```bash
/plugin install sncf-train-schedule
```

### Manual install

```bash
git clone https://github.com/Troules/troules-marketplace
claude --plugin-dir ./troules-marketplace/sncf-train-schedule
```

---

## sncf-train-schedule

A Claude Code plugin for checking French train schedules, departures, arrivals, and planning journeys using the SNCF/Navitia API.

### Prerequisites

**API Token**: Register at https://numerique.sncf.com/startup/api/token-developpeur/ for a free token.

**Recommended — persistent setup** (survives plugin updates, gitignored):
```
/setup your-token-here
```
This saves the token to `.claude/sncf-train-schedule.local.md` in your project. All scripts and hooks pick it up automatically.

**Alternative — session only**:
```bash
export NAVITIA_API_TOKEN="your-token-here"
```

**Token lookup order**: `NAVITIA_API_TOKEN` env var → `.claude/sncf-train-schedule.local.md` → `.env`

### Quick Start

Once installed, ask Claude about French trains:

- "What are the next trains from Paris Gare de Lyon?"
- "Plan a journey from Paris to Marseille tomorrow at 3pm"
- "Show me arrivals at Lyon Part-Dieu"
- "When is the next train to Bordeaux?"

### Features

- Real-time departures and arrivals
- Journey planning with transfers and CO2 emissions
- Station search and autocomplete
- Delay and disruption information
- Platform and track details
- Saved search results (private, gitignored `results/` folder)

### Configuration

| Variable | Description | Required |
|----------|-------------|----------|
| `NAVITIA_API_TOKEN` | Navitia API token | Yes |

### Plugin Structure

```
sncf-train-schedule/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest
├── commands/
│   ├── check-trains.md          # /check-trains slash command
│   └── setup.md                 # /setup token configuration
├── skills/
│   └── plan-journey/
│       ├── SKILL.md             # Core skill instructions
│       ├── references/
│       │   └── api-reference.md # Detailed API docs
│       ├── examples/
│       │   └── usage-examples.md
│       └── scripts/
│           ├── search_stations.py
│           ├── get_departures.py
│           ├── get_arrivals.py
│           ├── plan_journey.py
│           ├── validate_station_id.py
│           └── validate_datetime.py
├── hooks/
│   ├── hooks.json               # Hook manifest
│   ├── check-token.sh           # Token validation (PreToolUse)
│   └── validate-bash-security.sh # Security check (PreToolUse)
```

### Testing

```bash
# Structure tests (no token needed)
bash tests/test-plugin-structure.sh

# API tests (requires token)
export NAVITIA_API_TOKEN="your-token"
bash tests/test-api-integration.sh
```

---

## Resources

- [Navitia API Documentation](https://doc.navitia.io/)
- [SNCF Open Data](https://numerique.sncf.com/ressources/api/)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License — see [LICENSE](LICENSE) for details.
