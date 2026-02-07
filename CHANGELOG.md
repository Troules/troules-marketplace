# Changelog

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
