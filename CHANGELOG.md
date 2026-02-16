# Changelog

## 2026-02-16 - v2.6.3: Align marketplace.json plugin name with plugin.json

### Bug Fixes
- **`marketplace.json` name**: Renamed plugin entry from `plan-journey` to `sncf-train-schedule` for consistency with `plugin.json`
- **Test script**: Updated hardcoded name lookup in `test-plugin-structure.sh` to match

### Files Modified
- `.claude-plugin/marketplace.json`
- `tests/test-plugin-structure.sh`

---

## 2026-02-16 - v2.6.2: Graceful error handling in API scripts

### Bug Fixes
- **Prevent chat crashes**: All `sys.exit(1)` calls for user-facing errors (missing token, invalid token, API errors, network errors, empty results) changed to `sys.exit(0)` across all 6 scripts
- **`.env` fallback**: All 5 API scripts now auto-load a `.env` file via `python-dotenv` (gracefully ignored if package not installed)
- **`validate_station_id.py`**: Always exits 0 — valid/invalid result communicated via stdout, not exit code

### Files Modified
- `sncf-train-schedule/skills/plan-journey/scripts/get_arrivals.py`
- `sncf-train-schedule/skills/plan-journey/scripts/get_departures.py`
- `sncf-train-schedule/skills/plan-journey/scripts/plan_journey.py`
- `sncf-train-schedule/skills/plan-journey/scripts/search_stations.py`
- `sncf-train-schedule/skills/plan-journey/scripts/validate_datetime.py`
- `sncf-train-schedule/skills/plan-journey/scripts/validate_station_id.py`

---

## 2026-02-16 - v2.6.1: Rename plugin.json name to sncf-train-schedule

### Bug Fixes
- **`plugin.json` name**: Corrected internal plugin name from `plan-journey` to `sncf-train-schedule` for consistency with the plugin directory name

### Files Modified
- `sncf-train-schedule/.claude-plugin/plugin.json`

---

## 2026-02-16 - v2.6.0: Add /check-trains slash command

### New Features
- **`/check-trains` command**: New slash command for checking French train schedules directly — supports journey planning (`Paris to Lyon`), departures (`next trains from Marseille`), arrivals, and optional datetime (`at 14:30`, `at tomorrow 9am`)
- **Datetime argument**: Datetime is validated and converted via `scripts/validate_datetime.py` before being passed to the API scripts

### CI
- Added 4 structure checks for command files in `test-plugin-structure.sh` (exists, frontmatter, description, `$ARGUMENTS` reference)

### Files Modified
- `sncf-train-schedule/commands/check-trains.md` (new)
- `tests/test-plugin-structure.sh`
- `.claude-plugin/marketplace.json`
- `sncf-train-schedule/.claude-plugin/plugin.json`

---

## 2026-02-16 - v2.5.3: Enforce scripts over ad-hoc curl commands

### Bug Fixes
- **Competing signals in SKILL.md**: Removed raw `curl` examples from `Instructions` (step 6) and `Quick Reference` that caused Claude to default to ad-hoc curl instead of the utility scripts
- **Prohibition added**: Added ⛔ hard rule at the top of `Instructions` — "NEVER write ad-hoc `curl` commands or generate Python code inline. ALWAYS use the scripts in `scripts/`. No exceptions."
- **Rationalization table added**: Added table of temptations vs. reality to resist common rationalizations for bypassing scripts
- **Quick Reference updated**: Replaced raw curl examples with equivalent script commands

### Files Modified
- `sncf-train-schedule/skills/plan-journey/SKILL.md`
- `.claude-plugin/marketplace.json`

### Closes
- Issue #34: Claude MUST use scripts in scripts folder instead of doing curls and generate python by himself

---

## 2026-02-16 - v2.5.2: Fix python3 command in skill docs

### Bug Fixes
- **`python3` command**: Replace bare `python` with `python3` across all skill command examples (SKILL.md, scripts/README.md, references/common-stations.md) — fixes `python: command not found` on systems without a `python` → `python3` symlink (e.g. WSL2, modern Linux)

### Files Modified
- `sncf-train-schedule/skills/plan-journey/SKILL.md`
- `sncf-train-schedule/skills/plan-journey/scripts/README.md`
- `sncf-train-schedule/skills/plan-journey/references/common-stations.md`

---

## 2026-02-16 - v2.5.1: Housekeeping

### Chores
- **Gitignore `docs/`**: design docs and implementation plans are now local-only (untracked from git)
- **Gitignore `__pycache__/`**: Python bytecode files (`*.pyc`, `*.pyo`) now excluded
- **`marketplace.json` sync**: plugin name updated from `sncf-train-schedule` to `plan-journey`; version bumped to `2.5.0`

### Files Modified
- `.gitignore`
- `.claude-plugin/marketplace.json`

---

## 2026-02-16 - v2.5.0: Delay & Disruption Support

### New Features
- **Delay display**: departures and arrivals now show `(+Xmin)` next to the time when a train is running late, computed from `base_departure_date_time` vs `departure_date_time`
- **Cancellation indicator**: cancelled trains show `❌ SUPPRIMÉ` instead of a time in all scripts and the mobile response template
- **Journey disruption status**: `plan_journey.py` now reads the journey-level `status` field — delayed journeys get a `⚠️` marker, cancelled journeys show `❌ SUPPRIMÉ`
- **15 new unit tests**: first pytest file in the project (`tests/test_delay_formatting.py`) covering all disruption states

### Documentation
- `response-template.md`: new `{DELAY}` variable, updated template blocks, delayed/cancelled filled example
- `api-reference.md`: new "Delays & Disruptions" section with field tables, Python delay calculation snippet, and JSON examples
- `SKILL.md`: delay/cancellation formatting rules added to Response Formatting section and Instructions step 7

### Files Modified
- `sncf-train-schedule/skills/plan-journey/scripts/get_departures.py`
- `sncf-train-schedule/skills/plan-journey/scripts/get_arrivals.py`
- `sncf-train-schedule/skills/plan-journey/scripts/plan_journey.py`
- `sncf-train-schedule/skills/plan-journey/references/response-template.md`
- `sncf-train-schedule/skills/plan-journey/references/api-reference.md`
- `sncf-train-schedule/skills/plan-journey/SKILL.md`
- `tests/test_delay_formatting.py` (new)

---

## 2026-02-16 - v2.4.2: Rename Skill to plan-journey

### Refactoring
- **Renamed skill**: `skills/sncf-train-schedule/` → `skills/plan-journey/` for a more generic, action-oriented name
- **Updated references**: `SKILL.md` frontmatter, `plugin.json` name field, and test paths updated accordingly

### Files Modified
- `sncf-train-schedule/skills/plan-journey/` — renamed from `sncf-train-schedule/skills/sncf-train-schedule/`
- `sncf-train-schedule/.claude-plugin/plugin.json` — name field updated
- `tests/test-plugin-structure.sh` — hardcoded skill paths updated

---

## 2026-02-15 - v2.4.1: README Marketplace Reframe

### Documentation
- **README rewritten**: Reframed as Troules' marketplace with a plugin directory table; split install steps (add marketplace then install plugin); updated all URLs to new repo name `troules-marketplace`

### Files Modified
- `README.md`

---

## 2026-02-15 - v2.4.0: Marketplace Structure Fix

### Bug Fixes
- **Fixed circular marketplace reference**: `marketplace.json` previously pointed to the same GitHub repo it lived in, causing plugin installation to fail. Source is now a local path (`./sncf-train-schedule`), which is the correct structure for a single-repo marketplace.

### Refactoring
- **Plugin subdirectory**: Moved `skills/`, `hooks/`, and `.claude-plugin/plugin.json` into `sncf-train-schedule/` subdirectory to match the proper marketplace layout expected by Claude Desktop
- **Updated tests**: Test paths now use `$PLUGIN_DIR` variable pointing to the plugin subdirectory

### Breaking Changes
- Plugin files have moved — existing installations should be reinstalled via `/plugin install sncf-train-schedule`

### Files Modified
- `.claude-plugin/marketplace.json` — source changed to `"./sncf-train-schedule"`
- `sncf-train-schedule/` — new plugin subdirectory (previously at repo root)
- `tests/test-plugin-structure.sh` — updated paths

---

## 2026-02-10 - v2.3.0: Marketplace Distribution

### New Features
- **Marketplace support**: Added `.claude-plugin/marketplace.json` — install with `/plugin marketplace add Troules/sncf-train-schedule` then `/plugin install sncf-train-schedule`
- **README install guide**: Added marketplace installation instructions

### Refactoring
- **Skill directory**: Restored `SKILL.md`, `examples/`, `references/`, `scripts/` to `skills/sncf-train-schedule/` (correct Claude Code convention)

### Files Modified
- `.claude-plugin/marketplace.json` *(new)*
- `skills/sncf-train-schedule/` *(restored structure)*
- `README.md`

---

## 2026-02-10 - v2.2.1: Skill Restructure and Mandatory Template Enforcement

### Bug Fixes
- **Enforce response template**: Added prominent `⚠️ MANDATORY` section in `SKILL.md` so the agent always reads and uses `references/response-template.md` before presenting train results
- **Fix test paths**: Updated `tests/test-plugin-structure.sh` paths after skill move

### Refactoring
- **Move skill to root**: Moved `SKILL.md`, `examples/`, `references/`, `scripts/` from `skills/sncf-train-schedule/` to the project root — git history preserved

### Files Modified
- `SKILL.md`, `examples/`, `references/`, `scripts/` *(moved from `skills/sncf-train-schedule/`)*
- `tests/test-plugin-structure.sh`
- `.github/workflows/release.yml` *(fix git identity for annotated tags)*

---

## 2026-02-10 - v2.2.0: Mobile Response Template and CI Fixes

### New Features
- **Mobile Response Template**: Added `references/response-template.md` with a 30-character-wide layout for mobile app display
  - Three variants: journey search, departure board, and journey with connection
  - Station name and day abbreviation tables
  - Filled examples for both direct and connecting trains
- **Automated Release Workflow**: Added `.github/workflows/release.yml` to automate tag creation, GitHub releases, and `plugin.json` version updates on CHANGELOG.md push

### Bug Fixes
- **CI YAML Syntax**: Fixed two YAML block scalar indentation errors in `release.yml` where multi-line bash strings broke out to column 0 (lines 58 and 87)

### Documentation
- Added versioning and release documentation to CLAUDE.md

### Files Modified
- `skills/sncf-train-schedule/references/response-template.md` *(new)*
- `skills/sncf-train-schedule/SKILL.md`
- `.github/workflows/release.yml` *(new, then fixed)*

---

## 2026-02-10 - v2.1.0: Python Utilities and Documentation Enhancements

### New Features
- **Python Utility Scripts**: Added 6 comprehensive Python utilities for common tasks
  - `search_stations.py` - Interactive station search with fuzzy matching
  - `validate_station_id.py` - Station ID validation and details lookup
  - `validate_datetime.py` - Journey date/time validation helper
  - `plan_journey.py` - Full journey planning with formatted output
  - `get_departures.py` - Real-time departures from a station
  - `get_arrivals.py` - Real-time arrivals at a station
- **Common Stations Reference**: Added `references/common-stations.md` with 50+ pre-populated French station IDs
- **Scripts Documentation**: Created comprehensive `scripts/README.md` with usage examples and workflows

### Enhanced Documentation
- **SKILL.md Improvements** (~150 lines added):
  - Added practical workflows and decision trees
  - Created comprehensive dependency checklist
  - Enhanced error handling patterns
  - Added Python script integration examples
- **Better Organization**: Structured references and utilities for easier discovery

### Bug Fixes
- **Frontmatter Formatting**: Fixed skill description to use single-line format for better readability

### Files Added
- `skills/sncf-train-schedule/scripts/search_stations.py`
- `skills/sncf-train-schedule/scripts/validate_station_id.py`
- `skills/sncf-train-schedule/scripts/validate_datetime.py`
- `skills/sncf-train-schedule/scripts/plan_journey.py`
- `skills/sncf-train-schedule/scripts/get_departures.py`
- `skills/sncf-train-schedule/scripts/get_arrivals.py`
- `skills/sncf-train-schedule/references/common-stations.md`
- `skills/sncf-train-schedule/scripts/README.md`

---

## 2026-02-09 - v2.0.1: Documentation and CI Fixes

### Bug Fixes
- **API Token URL**: Corrected registration URL to official SNCF developer portal
  - Updated from `navitia.io` to `https://numerique.sncf.com/startup/api/token-developpeur/`
  - Fixed in: `.env.example`, `README.md`, `SKILL.md`, `test-api.sh`

### CI/CD Improvements
- **GitHub Actions Workflow**: Fixed workflow configuration issues
  - Corrected `if` condition syntax in workflow YAML
  - Removed redundant conditionals from API tests job
  - Made hook scripts executable
- **Test Script**: Fixed pipe handling with `set -e` in test script
- **API Integration Testing**: Tested integration with GitHub secrets

---

## 2026-02-08 - v2.0.0: Plugin Migration

### Breaking Changes
- Restructured from flat skill to Claude Code plugin format
- Moved `SKILL.md` to `skills/sncf-train-schedule/SKILL.md`
- Moved `examples.md` to `skills/sncf-train-schedule/examples/usage-examples.md`
- Moved `save-journey.sh` to `skills/sncf-train-schedule/scripts/save-journey.sh`
- Moved `test-api.sh` to `skills/sncf-train-schedule/scripts/test-api.sh`

### New
- `.claude-plugin/plugin.json` — plugin manifest for marketplace
- `hooks/hooks.json` — hook manifest with SessionStart and PreToolUse hooks
- `hooks/check-token.sh` — validates API token on session start
- `hooks/validate-bash-security.sh` — warns on hardcoded tokens in commands
- `skills/sncf-train-schedule/references/api-reference.md` — extracted detailed API docs
- `tests/test-plugin-structure.sh` — structure validation tests (no token needed)
- `tests/test-api-integration.sh` — API integration tests
- `.github/workflows/test.yml` — CI pipeline

### Changed
- Compressed SKILL.md from ~2,800 to ~470 words with progressive disclosure
- Rewritten README.md for plugin installation
- Updated CONTRIBUTING.md for plugin conventions

---

## 2026-02-07 - v1.2.2: Skill Documentation Updates

### 📝 SKILL.md Enhancements
- **Results Saving Instructions**: Added clear guidance for saving journey results to `results/` folder
  - Filename format and examples
  - Privacy note (gitignored folder)
  - Metadata and formatting guidelines
- **Updated Examples**: Replaced specific routes with generic Paris-Marseille examples
- **Station IDs**: Updated reference stations to use more widely-known cities

---

## 2026-02-07 - v1.2.1: Documentation Corrections

### 📝 Documentation Fixes
- **README.md Updates**:
  - Fixed repository URL: `https://github.com/Troules/sncf-train-schedule`
  - Corrected API token source: `https://numerique.sncf.com/ressources/api/` (was incorrectly pointing to navitia.io)

---

## 2026-02-07 - v1.2.0: Search Results & Privacy Updates

### 🆕 New Features
- **Search Results History**: Added `results/` folder to save journey queries
  - Results automatically saved with timestamps
  - Format: `YYYY-MM-DD_HHMM_origin-destination.txt`
  - Private and gitignored - search history never committed
- **Save Journey Script**: New `save-journey.sh` helper script
  - Manual journey result saving
  - Formatted output with emojis and details
  - Usage examples in README

### 🔒 Privacy & Security Enhancements
- **Enhanced .gitignore**:
  - Added `results/` folder (search history)
  - Added `.claude/` directory (contains permissions with tokens)
  - Added `TEST_REPORT.md` (development only)
- **Documentation Updates**:
  - Changed examples from specific routes (Lyon-Saint-Étienne) to generic (Paris-Marseille)
  - Changed dates from current (2026-02-08) to generic (2025-01-01)
  - Removed personally identifiable travel plans from public documentation

### 📝 Documentation
- **Updated README.md**:
  - New "Search Results History" section
  - Instructions for viewing saved searches
  - Save script usage examples
  - All examples now use generic Paris-Marseille routes
- **Updated .gitignore**:
  - Explicitly added `.claude/` (previously relied on default ignore)
  - Added `results/` for search history
  - Added `TEST_REPORT.md` for development

### 🛠️ Files Added
- `save-journey.sh` - Journey result saving script
- `results/README.md` - Results folder documentation

### ✅ Verification
- Confirmed no API tokens in committed files
- Confirmed `.env` properly gitignored
- Confirmed `.claude/` properly gitignored
- Confirmed `results/` properly gitignored

---

## 2026-02-07 - v1.1.0: Major Update: Production Testing & Best Practices

### Updated Based on Real-World Testing
Skill was tested with actual journey planning (Lyon to Saint-Étienne) and updated based on learnings.

### 🔧 API Configuration Updates
- **Authentication**: Now strongly recommends header-based auth (`-H "Authorization: $TOKEN"`)
  - Added warnings about unreliable basic auth (`-u $TOKEN:`)
  - Documented WebFetch tool limitations with URL-embedded tokens
- **Region Selection**: Clarified that `sncf` region covers all SNCF trains across France
  - Other regions like `fr-idf` may have different access permissions

### 📝 Enhanced Instructions
- **Error Handling**: Added specific guidance for common errors
  - "no token" error solutions
  - Permission denied troubleshooting
  - Empty response handling
- **Time Formatting**: Added explicit instructions for parsing `YYYYMMDDTHHmmss` format
  - Extract hours from positions 9-10
  - Extract minutes from positions 11-12
- **Output Formatting**: Added recommendations for:
  - Using emojis for better readability (🚆, ⏰, 🔄)
  - Highlighting recommended options
  - Cleaning station names (remove city suffixes)
  - Including CO2 emissions data

### 🛠️ New Practical Implementation Patterns Section
Added three proven patterns:
1. **Script Files**: Using scratchpad directory for complex queries
2. **Token Management**: Multiple approaches for handling authentication
3. **Response Parsing**: Python code examples for processing JSON

### 📖 Enhanced Examples
- **Example 4**: Complete multi-step journey planning workflow
  - Station search
  - ID extraction
  - Journey planning
  - Response formatting

### 🗺️ Expanded Station IDs
Added discovered stations:
- Lyon Perrache: `stop_area:SNCF:87722025`
- Lyon Vaise: `stop_area:SNCF:87721001`
- Saint-Étienne Châteaucreux: `stop_area:SNCF:87726000`

### 🐛 New Troubleshooting Section
Added comprehensive troubleshooting guide:
- "no token" error with 4 solutions
- Permission denied / 403 errors
- Empty JSON responses
- Time parsing issues
- Token persistence problems between commands

### 📊 File Statistics
- **Lines**: 314 (increased from ~200)
- **New Sections**: 2 (Practical Implementation Patterns, Troubleshooting)
- **Examples**: 4 (added 1 comprehensive example)
- **Station IDs**: 8 (added 3)

### ✅ Testing Status
- ✓ Authentication tested and working
- ✓ Station search tested (Lyon, Saint-Étienne)
- ✓ Journey planning tested (Lyon → Saint-Étienne)
- ✓ Response parsing and formatting validated
- ✓ Time format conversion working correctly

### 🎯 Next Steps
Skill is now production-ready with:
- Proven authentication method
- Real-world tested workflows
- Comprehensive error handling
- Clear examples and patterns

---

## 2026-02-07 - Initial Release

- Created SKILL.md with basic structure
- Added API endpoints documentation
- Included example commands
- Added common station IDs
- Created README, examples, and test script
