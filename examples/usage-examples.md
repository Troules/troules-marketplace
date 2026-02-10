# SNCF Train Schedule Skill - Examples

This document provides practical examples of using the SNCF Train Schedule skill.

## Setup

First, make sure you have your API token set:
```bash
export NAVITIA_API_TOKEN="your-token-here"
```

## Example 1: Find Next Departures

**User Request:**
> "What are the next trains leaving from Paris Gare de Lyon?"

**Skill Actions:**
1. Search for station: "Paris Gare de Lyon"
2. Get station ID: `stop_area:SNCF:87686006`
3. Fetch departures from current time
4. Display formatted results

**Expected Output:**
```
Next departures from Paris Gare de Lyon:

1. TGV 6601 to Marseille Saint-Charles
   Departure: 14:35 (Platform 5)
   Status: On time

2. TER 17234 to Melun
   Departure: 14:42 (Platform 12)
   Status: On time

3. TGV 6703 to Lyon Part-Dieu
   Departure: 14:50 (Platform 3)
   Status: Delayed 5 minutes

4. Intercités 4052 to Clermont-Ferrand
   Departure: 15:05 (Platform 7)
   Status: On time
```

## Example 2: Plan a Journey

**User Request:**
> "I need to travel from Paris to Lyon tomorrow at 9am. Show me the options."

**Skill Actions:**
1. Search for origin: "Paris" → Select best match
2. Search for destination: "Lyon" → Select best match
3. Format datetime: Tomorrow 9am → `20260208T090000`
4. Fetch journeys
5. Display options with transfers

**Expected Output:**
```
Journey options from Paris to Lyon on Feb 8, 2026:

Option 1: Direct TGV (Recommended)
├─ Depart: Paris Gare de Lyon at 09:12
├─ Arrive: Lyon Part-Dieu at 11:09
├─ Duration: 1h 57min
├─ Transfers: 0
└─ Train: TGV 6703

Option 2: Direct TGV
├─ Depart: Paris Gare de Lyon at 10:12
├─ Arrive: Lyon Part-Dieu at 12:09
├─ Duration: 1h 57min
├─ Transfers: 0
└─ Train: TGV 6705

Option 3: With transfer
├─ Depart: Paris Gare de Lyon at 09:05
├─ Transfer: Dijon-Ville (15 min connection)
├─ Arrive: Lyon Part-Dieu at 12:45
├─ Duration: 3h 40min
└─ Transfers: 1
```

## Example 3: Check Arrivals at a Station

**User Request:**
> "What trains are arriving at Marseille Saint-Charles in the next hour?"

**Skill Actions:**
1. Search for station: "Marseille Saint-Charles"
2. Get current time + 1 hour window
3. Fetch arrivals
4. Display with real-time information

**Expected Output:**
```
Arrivals at Marseille Saint-Charles (next hour):

14:25 - TGV 6602 from Paris Gare de Lyon (Platform 3) - On time
14:38 - TER 17896 from Aix-en-Provence (Platform 8) - 2 min delay
14:52 - TGV 6108 from Lyon Part-Dieu (Platform 2) - On time
15:05 - Intercités 4753 from Toulouse (Platform 5) - 10 min delay
15:18 - TER 17902 from Toulon (Platform 7) - On time
```

## Example 4: Search for a Station

**User Request:**
> "Find the station ID for Bordeaux Saint-Jean"

**Skill Actions:**
1. Use `/places` endpoint
2. Search query: "Bordeaux Saint-Jean"
3. Return top matches

**Expected Output:**
```
Search results for "Bordeaux Saint-Jean":

1. Bordeaux-Saint-Jean (Bordeaux)
   ID: stop_area:SNCF:87581009
   Type: Train station
   Region: fr-sw

2. Bordeaux Saint-Jean (Tram stop)
   ID: stop_area:TCUB:SJ
   Type: Tram station
   Region: fr-sw
```

## Example 5: Real-time Status Check

**User Request:**
> "Is there a delay on trains from Paris to Lyon right now?"

**Skill Actions:**
1. Find Paris Gare de Lyon station
2. Get departures to Lyon with `data_freshness=realtime`
3. Filter for Lyon-bound trains
4. Show delay information

**Expected Output:**
```
Current status of Paris → Lyon trains:

TGV 6703 (departs 14:50)
├─ Status: Delayed 5 minutes
├─ New departure: 14:55
└─ Reason: Technical incident

TGV 6705 (departs 16:12)
├─ Status: On time
└─ Expected: 16:12

TGV 6707 (departs 17:12)
├─ Status: On time
└─ Expected: 17:12
```

## Example 6: Weekend Travel Planning

**User Request:**
> "What's the best way to get from Nice to Paris this Saturday afternoon?"

**Skill Actions:**
1. Calculate Saturday's date
2. Use afternoon timeframe (14:00)
3. Search Nice and Paris stations
4. Get journey options
5. Highlight fastest and most convenient options

**Expected Output:**
```
Nice → Paris journeys for Saturday, Feb 8, 2026 (afternoon):

Fastest Option: TGV 6172
├─ Depart: Nice-Ville at 14:26
├─ Arrive: Paris Gare de Lyon at 20:15
├─ Duration: 5h 49min
├─ Transfers: 0
└─ Price: From €85

Alternative: TGV 6174 (more comfortable timing)
├─ Depart: Nice-Ville at 16:26
├─ Arrive: Paris Gare de Lyon at 22:15
├─ Duration: 5h 49min
├─ Transfers: 0
└─ Price: From €95
```

## Example 7: Coverage Region Discovery

**User Request:**
> "What regions are covered by the API?"

**Skill Actions:**
1. Call `/coverage` endpoint
2. List available regions
3. Show basic info for each

**Expected Output:**
```
Available coverage regions:

1. fr-idf (Île-de-France)
   - Main city: Paris
   - Coverage: Paris metro, RER, trains, buses

2. fr-ne (Northeast France)
   - Main cities: Strasbourg, Metz, Nancy
   - Coverage: Regional trains and transport

3. fr-nw (Northwest France)
   - Main cities: Rennes, Nantes, Caen
   - Coverage: Regional trains and transport

4. fr-se (Southeast France)
   - Main cities: Lyon, Marseille, Nice
   - Coverage: Regional trains and transport

5. sandbox (Testing)
   - Test environment for development
```

## Tips for Using the Skill

1. **Be specific about locations**: "Paris Gare de Lyon" is better than just "Paris"
2. **Provide time context**: "tomorrow at 3pm" or "next Monday morning"
3. **Ask for real-time data**: "current delays" or "right now" triggers real-time mode
4. **Request multiple options**: "show me a few options" gets more journey alternatives
5. **Specify preferences**: "direct trains only" or "fastest route"

## Common API Responses

The skill handles these API response scenarios:

- ✅ **Success**: Displays formatted schedule data
- ⚠️ **No results**: Suggests alternative searches or times
- ❌ **Invalid token**: Prompts to check API token configuration
- ❌ **Station not found**: Offers similar station names
- ❌ **Rate limit**: Suggests waiting before retry

## Advanced Usage

### Custom Date/Time Formats

The skill understands natural language:
- "tomorrow at 3pm"
- "next Monday morning"
- "February 15th at 9:30am"
- "in 2 hours"

### Filtering Results

- "only direct trains"
- "show me the fastest option"
- "trains with wheelchair access"
- "departures from platform 5"

### Multi-leg Journeys

- "Paris to Lyon, then Lyon to Marseille"
- "Round trip from Paris to Bordeaux"
