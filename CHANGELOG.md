# Changelog

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
