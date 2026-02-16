---
description: Check French train schedules and plan journeys
argument-hint: "<from> to <to> [at <datetime>] | next trains from <station> [at <datetime>]"
allowed-tools: ["Bash", "Read"]
---

# /check-trains - SNCF Train Schedule Checker

User request: **"$ARGUMENTS"**

## Instructions

Use the `plan-journey` skill to fulfill this request. Follow the skill workflow exactly:

1. **Parse the request** from `$ARGUMENTS`:
   - "X to Y" → plan a journey from X to Y
   - "X to Y at <datetime>" → plan a journey departing at the given time
   - "next trains from X" / "departures from X" → get departures
   - "next trains from X at <datetime>" → get departures from the given time
   - "arrivals at X" → get arrivals
   - "arrivals at X at <datetime>" → get arrivals from the given time
   - No arguments → ask the user what they need
   - If a datetime is provided, convert it with `python3 scripts/validate_datetime.py "<datetime>" --convert` before passing to the script

2. **Follow the `plan-journey` skill** step by step (search stations, validate IDs, fetch data, format results).

3. **Present results** using the mobile template from `references/response-template.md`.

## Requirements

`NAVITIA_API_TOKEN` must be set. Get a free token at: https://numerique.sncf.com/startup/api/token-developpeur/
