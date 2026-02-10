#!/bin/bash
# Plugin structure validation tests
# No API token required — validates file layout and conventions

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

PASS=0
FAIL=0
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

check() {
    local desc="$1"
    shift
    if "$@" >/dev/null 2>&1; then
        echo -e "${GREEN}PASS${NC} $desc"
        PASS=$((PASS + 1))
    else
        echo -e "${RED}FAIL${NC} $desc"
        FAIL=$((FAIL + 1))
    fi
}

echo "=================================="
echo "Plugin Structure Tests"
echo "=================================="
echo ""

# plugin.json
check "plugin.json exists" test -f "$ROOT/.claude-plugin/plugin.json"
check "plugin.json is valid JSON" python3 -c "import json; json.load(open('$ROOT/.claude-plugin/plugin.json'))"
check "plugin.json has name field" python3 -c "import json; d=json.load(open('$ROOT/.claude-plugin/plugin.json')); assert 'name' in d"
check "plugin.json has description field" python3 -c "import json; d=json.load(open('$ROOT/.claude-plugin/plugin.json')); assert 'description' in d"
check "plugin.json has version field" python3 -c "import json; d=json.load(open('$ROOT/.claude-plugin/plugin.json')); assert 'version' in d"

# Version consistency check
PLUGIN_VERSION=$(python3 -c "import json; print(json.load(open('$ROOT/.claude-plugin/plugin.json'))['version'])")
CHANGELOG_VERSION=$(grep -m 1 -oP '## \d{4}-\d{2}-\d{2} - v\K[0-9]+\.[0-9]+\.[0-9]+' "$ROOT/CHANGELOG.md")
check "plugin.json version matches CHANGELOG" bash -c "[ '$PLUGIN_VERSION' = '$CHANGELOG_VERSION' ]"
if [ "$PLUGIN_VERSION" = "$CHANGELOG_VERSION" ]; then
    echo "  ✓ Version matches: $PLUGIN_VERSION"
else
    echo "  ✗ Version mismatch: plugin.json=$PLUGIN_VERSION, CHANGELOG=$CHANGELOG_VERSION"
fi

# SKILL.md
check "SKILL.md exists" test -f "$ROOT/skills/sncf-train-schedule/SKILL.md"
check "SKILL.md has YAML frontmatter" bash -c "head -1 '$ROOT/skills/sncf-train-schedule/SKILL.md' | grep -q '^---'"
check "SKILL.md under 2000 words" bash -c "[ \$(wc -w < '$ROOT/skills/sncf-train-schedule/SKILL.md') -lt 2000 ]"

# hooks.json
check "hooks.json exists" test -f "$ROOT/hooks/hooks.json"
check "hooks.json is valid JSON" python3 -c "import json; json.load(open('$ROOT/hooks/hooks.json'))"

# Hook scripts
check "check-token.sh exists" test -f "$ROOT/hooks/check-token.sh"
check "check-token.sh is executable" test -x "$ROOT/hooks/check-token.sh"
check "validate-bash-security.sh exists" test -f "$ROOT/hooks/validate-bash-security.sh"
check "validate-bash-security.sh is executable" test -x "$ROOT/hooks/validate-bash-security.sh"

# Reference files
check "api-reference.md exists" test -f "$ROOT/skills/sncf-train-schedule/references/api-reference.md"
check "usage-examples.md exists" test -f "$ROOT/skills/sncf-train-schedule/examples/usage-examples.md"
check "save-journey.sh exists" test -f "$ROOT/skills/sncf-train-schedule/scripts/save-journey.sh"

# .env gitignored
check ".env is gitignored" bash -c "grep -q '^\.env$' '$ROOT/.gitignore'"

# No .env committed
check "No .env file in repo" bash -c "test ! -f '$ROOT/.env' || ! git -C '$ROOT' ls-files --error-unmatch .env 2>/dev/null"

echo ""
echo "=================================="
echo "Results: ${PASS} passed, ${FAIL} failed"
echo "=================================="

[ "$FAIL" -eq 0 ] && exit 0 || exit 1
