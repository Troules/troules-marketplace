# Delay & Disruption Support Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Show delay in minutes and cancellations in all three train scripts, the mobile response template, and documentation.

**Architecture:** Navitia's `stop_date_time` object exposes `base_departure_date_time` alongside `departure_date_time`; delay = actual − base in minutes. Journey-level `status` ("NO_SERVICE", "SIGNIFICANT_DELAYS") covers `plan_journey.py`. A `compute_delay_minutes()` helper is added inline to each script (no shared module).

**Tech Stack:** Python 3 (stdlib `datetime`), existing `requests` dependency, pytest for unit tests.

---

### Task 1: Create unit tests for delay helper functions

**Files:**
- Create: `tests/test_delay_formatting.py`

**Context:** There are currently no Python unit tests — only shell-based integration tests in `tests/`. This is the first pytest file in the project.

**Step 1: Create the test file**

```python
"""Unit tests for delay helper functions used in train scripts."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'sncf-train-schedule', 'skills', 'plan-journey', 'scripts'))

from get_departures import compute_delay_minutes, format_disruption


def test_compute_delay_on_time():
    assert compute_delay_minutes("20260210T140000", "20260210T140000") == 0


def test_compute_delay_late():
    assert compute_delay_minutes("20260210T140000", "20260210T140700") == 7


def test_compute_delay_early():
    assert compute_delay_minutes("20260210T140000", "20260210T135500") == -5


def test_compute_delay_invalid_returns_zero():
    assert compute_delay_minutes(None, "20260210T140000") == 0
    assert compute_delay_minutes("bad", "20260210T140000") == 0


def test_format_disruption_on_time():
    sdt = {
        "departure_date_time": "20260210T140000",
        "base_departure_date_time": "20260210T140000",
    }
    assert format_disruption(sdt, "departure_date_time") == ""


def test_format_disruption_delayed():
    sdt = {
        "departure_date_time": "20260210T140700",
        "base_departure_date_time": "20260210T140000",
    }
    assert format_disruption(sdt, "departure_date_time") == "+7min"


def test_format_disruption_early():
    sdt = {
        "departure_date_time": "20260210T135500",
        "base_departure_date_time": "20260210T140000",
    }
    assert format_disruption(sdt, "departure_date_time") == "-5min"


def test_format_disruption_no_base_time():
    sdt = {"departure_date_time": "20260210T140000"}
    assert format_disruption(sdt, "departure_date_time") == ""


def test_format_disruption_cancelled():
    sdt = {
        "departure_date_time": "20260210T140000",
        "base_departure_date_time": "20260210T140000",
        "additional_informations": ["no_departing"],
    }
    assert format_disruption(sdt, "departure_date_time") == "❌ SUPPRIMÉ"


def test_format_disruption_arrival_key():
    sdt = {
        "arrival_date_time": "20260210T160700",
        "base_arrival_date_time": "20260210T160000",
    }
    assert format_disruption(sdt, "arrival_date_time") == "+7min"
```

**Step 2: Run tests to confirm they fail (functions don't exist yet)**

```bash
cd /path/to/troules-marketplace
python -m pytest tests/test_delay_formatting.py -v 2>&1 | head -30
```

Expected: `ImportError: cannot import name 'compute_delay_minutes'`

---

### Task 2: Add delay helpers to `get_departures.py` and make tests pass

**Files:**
- Modify: `sncf-train-schedule/skills/plan-journey/scripts/get_departures.py:82-120`

**Step 1: Insert two helper functions after `format_datetime()` (after line 88)**

Add after the `format_datetime` function and before `format_output`:

```python
def compute_delay_minutes(base_dt_str, actual_dt_str):
    """Return delay in minutes (positive = late, negative = early, 0 = on time)."""
    try:
        base = datetime.strptime(base_dt_str, "%Y%m%dT%H%M%S")
        actual = datetime.strptime(actual_dt_str, "%Y%m%dT%H%M%S")
        return int((actual - base).total_seconds() // 60)
    except (ValueError, TypeError):
        return 0


def format_disruption(stop_date_time, time_key):
    """Return disruption label: '+Xmin', '-Xmin', '❌ SUPPRIMÉ', or '' for on-time.

    Args:
        stop_date_time: The stop_date_time dict from Navitia response
        time_key: 'departure_date_time' or 'arrival_date_time'
    """
    if "no_departing" in stop_date_time.get("additional_informations", []) or \
       "no_arriving" in stop_date_time.get("additional_informations", []):
        return "❌ SUPPRIMÉ"

    base_key = f"base_{time_key}"
    base_time = stop_date_time.get(base_key)
    actual_time = stop_date_time.get(time_key)

    if not base_time or not actual_time or base_time == actual_time:
        return ""

    delay = compute_delay_minutes(base_time, actual_time)
    if delay == 0:
        return ""
    return f"+{delay}min" if delay > 0 else f"{delay}min"
```

**Step 2: Replace the delay block in `format_output()` (lines 106-118)**

Replace the current block:
```python
        dep_time = format_datetime(dep.get("stop_date_time", {}).get("departure_date_time", ""))

        output.append(f"{i}. [{line}] → {direction}")
        output.append(f"   Departure: {dep_time}")

        # Show delay if in realtime mode
        if "stop_date_time" in dep:
            base_time = dep["stop_date_time"].get("base_departure_date_time")
            actual_time = dep["stop_date_time"].get("departure_date_time")
            if base_time and actual_time and base_time != actual_time:
                output.append(f"   ⚠️  Delayed (scheduled: {format_datetime(base_time)})")
```

With:
```python
        sdt = dep.get("stop_date_time", {})
        dep_time = format_datetime(sdt.get("departure_date_time", ""))
        disruption = format_disruption(sdt, "departure_date_time")

        output.append(f"{i}. [{line}] → {direction}")
        if disruption == "❌ SUPPRIMÉ":
            output.append(f"   {disruption}")
        elif disruption:
            output.append(f"   Departure: {dep_time} ({disruption})")
        else:
            output.append(f"   Departure: {dep_time}")
```

**Step 3: Run tests to verify they pass**

```bash
python -m pytest tests/test_delay_formatting.py -v
```

Expected: All 10 tests PASS.

**Step 4: Commit**

```bash
git add sncf-train-schedule/skills/plan-journey/scripts/get_departures.py tests/test_delay_formatting.py
git commit -m "feat(delays): add delay helpers and tests to get_departures.py"
```

---

### Task 3: Apply same changes to `get_arrivals.py`

**Files:**
- Modify: `sncf-train-schedule/skills/plan-journey/scripts/get_arrivals.py:82-119`

**Step 1: Insert the same two helper functions after `format_datetime()` in `get_arrivals.py`**

Add the identical `compute_delay_minutes` and `format_disruption` functions (copy from `get_departures.py`).

**Step 2: Replace the delay block in `format_output()` (lines 103-115)**

Replace:
```python
        arr_time = format_datetime(arr.get("stop_date_time", {}).get("arrival_date_time", ""))

        output.append(f"{i}. [{line}] from {direction}")
        output.append(f"   Arrival: {arr_time}")

        # Show delay if in realtime mode
        if "stop_date_time" in arr:
            base_time = arr["stop_date_time"].get("base_arrival_date_time")
            actual_time = arr["stop_date_time"].get("arrival_date_time")
            if base_time and actual_time and base_time != actual_time:
                output.append(f"   ⚠️  Delayed (scheduled: {format_datetime(base_time)})")
```

With:
```python
        sdt = arr.get("stop_date_time", {})
        arr_time = format_datetime(sdt.get("arrival_date_time", ""))
        disruption = format_disruption(sdt, "arrival_date_time")

        output.append(f"{i}. [{line}] from {direction}")
        if disruption == "❌ SUPPRIMÉ":
            output.append(f"   {disruption}")
        elif disruption:
            output.append(f"   Arrival: {arr_time} ({disruption})")
        else:
            output.append(f"   Arrival: {arr_time}")
```

**Step 3: Add two tests covering get_arrivals.py to the test file**

Append to `tests/test_delay_formatting.py`:

```python
from get_arrivals import compute_delay_minutes as arr_compute_delay, format_disruption as arr_format_disruption


def test_arrivals_delay_helper_matches_departures():
    """Same logic — verify both scripts export compatible helpers."""
    assert arr_compute_delay("20260210T160000", "20260210T160500") == 5


def test_arrivals_format_disruption():
    sdt = {
        "arrival_date_time": "20260210T160500",
        "base_arrival_date_time": "20260210T160000",
    }
    assert arr_format_disruption(sdt, "arrival_date_time") == "+5min"
```

**Step 4: Run all tests**

```bash
python -m pytest tests/test_delay_formatting.py -v
```

Expected: All 12 tests PASS.

**Step 5: Commit**

```bash
git add sncf-train-schedule/skills/plan-journey/scripts/get_arrivals.py tests/test_delay_formatting.py
git commit -m "feat(delays): add delay display to get_arrivals.py"
```

---

### Task 4: Add delay support to `plan_journey.py`

**Files:**
- Modify: `sncf-train-schedule/skills/plan-journey/scripts/plan_journey.py:113-158`

**Context:** Journeys have a top-level `status` field rather than per-stop `base_*` times. Status values: `""` (on time), `"SIGNIFICANT_DELAYS"`, `"NO_SERVICE"`, `"MODIFIED_SERVICE"`.

**Step 1: Add a journey status helper after `format_duration()` (after line 110)**

```python
def format_journey_status(journey):
    """Return status label for a journey: '❌ SUPPRIMÉ', '⚠️', or ''."""
    status = journey.get("status", "")
    if status == "NO_SERVICE":
        return "❌ SUPPRIMÉ"
    if status in ("SIGNIFICANT_DELAYS", "MODIFIED_SERVICE"):
        return "⚠️"
    return ""
```

**Step 2: Update the journey summary line in `format_output()` (lines 121-128)**

Replace:
```python
        output.append(f"{'='*60}")
        output.append(f"Journey {i}: {dep_time} → {arr_time} ({duration})")
        output.append(f"Transfers: {nb_transfers}")
        output.append("")
```

With:
```python
        status_label = format_journey_status(journey)
        output.append(f"{'='*60}")
        if status_label == "❌ SUPPRIMÉ":
            output.append(f"Journey {i}: {dep_time} → {arr_time} ({duration}) {status_label}")
            output.append("")
            continue
        elif status_label:
            output.append(f"Journey {i}: {dep_time} → {arr_time} ({duration}) {status_label}")
        else:
            output.append(f"Journey {i}: {dep_time} → {arr_time} ({duration})")
        output.append(f"Transfers: {nb_transfers}")
        output.append("")
```

**Step 3: Add journey status tests to the test file**

Append to `tests/test_delay_formatting.py`:

```python
from plan_journey import format_journey_status


def test_journey_status_on_time():
    assert format_journey_status({}) == ""
    assert format_journey_status({"status": ""}) == ""


def test_journey_status_delayed():
    assert format_journey_status({"status": "SIGNIFICANT_DELAYS"}) == "⚠️"
    assert format_journey_status({"status": "MODIFIED_SERVICE"}) == "⚠️"


def test_journey_status_cancelled():
    assert format_journey_status({"status": "NO_SERVICE"}) == "❌ SUPPRIMÉ"
```

**Step 4: Run all tests**

```bash
python -m pytest tests/test_delay_formatting.py -v
```

Expected: All 15 tests PASS.

**Step 5: Commit**

```bash
git add sncf-train-schedule/skills/plan-journey/scripts/plan_journey.py tests/test_delay_formatting.py
git commit -m "feat(delays): add journey status display to plan_journey.py"
```

---

### Task 5: Update `response-template.md`

**Files:**
- Modify: `sncf-train-schedule/skills/plan-journey/references/response-template.md`

**Step 1: Add `{DELAY}` to the Journey Search variables table (after `{TRANSFERS}` row)**

```markdown
| `{DELAY}` | 7 | `+7min` `⚠️` `` |
```

**Step 2: Update the Journey Search template block to show delay on summary line**

Replace:
```
{#}  {DEP}→{ARR}  {DUR}
     {TRAINS}  {TRANSFERS}
```

With:
```
{#}  {DEP}→{ARR}  {DUR} {DELAY}
     {TRAINS}  {TRANSFERS}
```

**Step 3: Update the Departure Board template block to show delay on time line**

Replace:
```
{HH:MM}  {DIRECTION}
         {LINE}
```

With:
```
{HH:MM} {DELAY}  {DIRECTION}
         {LINE}
```

**Step 4: Add a new "Delayed / Cancelled" filled example section** after the "Departure board" example:

```markdown
### Delayed and cancelled trains

```
══════════════════════════════
🚉 Lyon PDieu
   Lun 10/02 · à partir 14:00
══════════════════════════════
14:00    St-Étienne
         REGIONAURA C18
──────────────────────────────
14:16 +7min  Grenoble
         TER 18045
──────────────────────────────
❌ SUPPRIMÉ  Marseille StC
         TGV INOUÏ 6173
══════════════════════════════
🔍 3 départs · 14:00
══════════════════════════════
```
```

**Step 5: Commit**

```bash
git add sncf-train-schedule/skills/plan-journey/references/response-template.md
git commit -m "docs(template): add delay and cancellation format to response template"
```

---

### Task 6: Update `api-reference.md`

**Files:**
- Modify: `sncf-train-schedule/skills/plan-journey/references/api-reference.md`

**Step 1: Add a new "Delays & Disruptions" section after "Response Format (JSON Paths)"**

Insert after the existing `## Response Format (JSON Paths)` section:

```markdown
## Delays & Disruptions

Delay data is only available when using `data_freshness=realtime` (the default in all scripts).

### Fields for Departures and Arrivals

| Field | Path | Description |
|-------|------|-------------|
| Scheduled time | `stop_date_time.base_departure_date_time` | Original timetable time |
| Actual time | `stop_date_time.departure_date_time` | Realtime-adjusted time |
| Cancellation | `stop_date_time.additional_informations[]` | Contains `"no_departing"` if cancelled |

Same pattern for arrivals: `base_arrival_date_time` vs `arrival_date_time`.

### Fields for Journeys

| Field | Path | Values |
|-------|------|--------|
| Journey status | `journeys[].status` | `""` on time · `"SIGNIFICANT_DELAYS"` · `"NO_SERVICE"` (cancelled) · `"MODIFIED_SERVICE"` (rerouted) |

### Computing Delay in Minutes

```python
from datetime import datetime

def compute_delay_minutes(base_dt_str, actual_dt_str):
    base = datetime.strptime(base_dt_str, "%Y%m%dT%H%M%S")
    actual = datetime.strptime(actual_dt_str, "%Y%m%dT%H%M%S")
    return int((actual - base).total_seconds() // 60)

# Example: base=14:00, actual=14:07 → +7min
delay = compute_delay_minutes("20260210T140000", "20260210T140700")  # returns 7
```

### Example: Delayed Departure Response (JSON excerpt)

```json
{
  "stop_date_time": {
    "departure_date_time": "20260210T140700",
    "base_departure_date_time": "20260210T140000",
    "additional_informations": []
  }
}
```

### Example: Cancelled Departure Response (JSON excerpt)

```json
{
  "stop_date_time": {
    "departure_date_time": "20260210T140000",
    "base_departure_date_time": "20260210T140000",
    "additional_informations": ["no_departing"]
  }
}
```
```

**Step 2: Commit**

```bash
git add sncf-train-schedule/skills/plan-journey/references/api-reference.md
git commit -m "docs(api-ref): add delays and disruptions section"
```

---

### Task 7: Update `SKILL.md`

**Files:**
- Modify: `sncf-train-schedule/skills/plan-journey/SKILL.md`

**Step 1: Add delay rule to the Response Formatting section**

Find the `## ⚠️ MANDATORY: Response Formatting` section. After the existing bullet list, add:

```markdown
**Delay and disruption rules:**
- On time: no extra output — keep the display clean
- Delayed: append `(+Xmin)` to the time (e.g. `14:32 (+7min)`)
- Cancelled: replace the time line with `❌ SUPPRIMÉ`
- Journey with delays: append `⚠️` to the journey summary line
```

**Step 2: Update Instructions step 7 to include delay parsing**

Find step 7 under `## Instructions`:

```
7. **Present results using the mobile template** (from `references/response-template.md`):
   - Parse time: `YYYYMMDDTHHmmss` → extract positions 9–10 (HH) and 11–12 (MM)
   - Journeys: show departure/arrival times, duration, transfers
   - Departures/arrivals: show time, line, direction, platform, real-time status
   - Abbreviate station names and day names as defined in the template
   - Highlight recommended options (fastest / most direct)
```

Replace with:

```
7. **Present results using the mobile template** (from `references/response-template.md`):
   - Parse time: `YYYYMMDDTHHmmss` → extract positions 9–10 (HH) and 11–12 (MM)
   - Journeys: show departure/arrival times, duration, transfers
   - Departures/arrivals: show time, line, direction, platform, real-time status
   - **Delays**: compare `base_departure_date_time` vs `departure_date_time`; show `(+Xmin)` suffix if different
   - **Cancellations**: show `❌ SUPPRIMÉ` if `additional_informations` contains `"no_departing"` / `"no_arriving"`, or journey `status == "NO_SERVICE"`
   - Abbreviate station names and day names as defined in the template
   - Highlight recommended options (fastest / most direct)
```

**Step 3: Commit**

```bash
git add sncf-train-schedule/skills/plan-journey/SKILL.md
git commit -m "docs(skill): add delay and disruption formatting rules"
```

---

### Task 8: Push, open PR, verify CI, merge

**Step 1: Push branch and open PR**

```bash
git push -u origin feat/delay-support
gh pr create --title "feat(delays): show delay minutes and cancellations in train results" \
  --body "Add +Xmin delay display and ❌ SUPPRIMÉ cancellation indicator to all three train scripts, mobile response template, api-reference.md, and SKILL.md. Includes 15 new unit tests."
```

**Step 2: Verify CI passes**

```bash
gh pr checks <PR_NUMBER> --watch
```

Expected: Both "Plugin Structure" and "API Integration" pass.

**Step 3: Merge**

```bash
gh pr merge <PR_NUMBER> --squash --delete-branch
git checkout main && git pull
```
