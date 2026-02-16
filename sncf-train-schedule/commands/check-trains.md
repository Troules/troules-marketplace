---
description: Check French train schedules and plan journeys
argument-hint: "<from> to <to> | next trains from <station>"
allowed-tools: ["Bash", "Read"]
---

# /check-trains - SNCF Train Schedule Checker

User request: **"$ARGUMENTS"**

## Instructions

Use the `plan-journey` skill to fulfill this request. Follow the skill workflow exactly:

1. **Parse the request** from `$ARGUMENTS`:
   - "X to Y" → plan a journey from X to Y
   - "next trains from X" / "departures from X" → get departures
   - "arrivals at X" → get arrivals
   - No arguments → ask the user what they need

2. **Follow the `plan-journey` skill** step by step (search stations, validate IDs, fetch data, format results).

3. **Present results** using the mobile template from `references/response-template.md`.

## Requirements

`NAVITIA_API_TOKEN` must be set. Get a free token at: https://numerique.sncf.com/startup/api/token-developpeur/
