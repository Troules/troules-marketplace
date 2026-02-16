# Design: Delay & Disruption Support

**Date:** 2026-02-16
**Status:** Approved

## Problem

The scripts partially detect delays (comparing `base_*` vs actual datetime) but show only "⚠️ Delayed (scheduled: HH:MM)" without a minute count. `plan_journey.py` has no delay info at all. The mobile response template has no delay format. Users cannot see how late a train is or whether it is cancelled.

## Approach

Full integration across scripts, mobile template, and documentation. Delay info is automatically included when `data_freshness=realtime` (the default) — no new CLI flags needed.

## API Data Model

Two mechanisms from the Navitia API:

**`stop_date_time` fields** (departures, arrivals, journey sections):
- `base_departure_date_time` / `base_arrival_date_time` — scheduled timetable time
- `departure_date_time` / `arrival_date_time` — current realtime time
- Delay minutes = `(actual - base) / 60`. Negative = early.

**Journey-level `status` field:**
| Value | Meaning |
|-------|---------|
| `""` (empty) | On time |
| `"SIGNIFICANT_DELAYS"` | Train is late |
| `"NO_SERVICE"` | Cancelled |
| `"MODIFIED_SERVICE"` | Rerouted or stop added |

## Script Changes

### `get_departures.py` and `get_arrivals.py`

Upgrade `format_output()`:
- Compute delay minutes from `base_*` vs actual `*_date_time`
- Show `+Xmin` suffix on the time line (e.g. `14:32 +7min`)
- Show `❌ SUPPRIMÉ` for `NO_SERVICE`
- On time: no extra output

### `plan_journey.py`

Upgrade `format_output()` for `public_transport` sections:
- Show `+Xmin` next to departure time in each section line
- Show `❌ SUPPRIMÉ` if `NO_SERVICE`
- Append `⚠️` to journey summary line if any section has a delay

## Mobile Response Template (`response-template.md`)

**Departure/Arrival board:**
```
14:32 +7min  Marseille StC
             TGV INOUÏ 6173
──────────────────────────────
❌ SUPPRIMÉ  Bordeaux
             TGV 8531
```

**Journey search:**
```
2  08:37→13:46  3h09 ⚠️+12min
   TGV INOUÏ  Direct
```

**Journey section (cancelled):**
```
╷ 08:37 TGV 6007
❌ SUPPRIMÉ
```

New variable added to the variables table:
| Variable | Max | Example |
|----------|-----|---------|
| `{DELAY}` | 7 | `+7min` |

`{DELAY}` is omitted entirely when on time.

## Documentation Changes

### `api-reference.md`

New "Delays & Disruptions" section:
- `stop_date_time` fields used to compute delay
- Journey `status` values and meanings
- Python snippet for delay calculation
- JSON path reference for delay-related fields

### `SKILL.md`

- **Response Format section**: add rule for `+Xmin`, `❌ SUPPRIMÉ`, nothing for on-time
- **Instructions step 7**: add delay parsing instruction referencing `response-template.md`

## Out of Scope

- No changes to Quick Start checklists or Quick Reference curl examples
- No `delay_utils.py` shared module (delay logic is ~10 lines, inline is clearer)
- No new CLI flags
