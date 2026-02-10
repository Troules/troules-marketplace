# Common SNCF Station IDs

Quick reference for major French train stations. Use these IDs directly with the API or utility scripts.

## Paris Area

| Station Name | Station ID | Coordinates |
|--------------|------------|-------------|
| Paris Gare de Lyon | `stop_area:SNCF:87686006` | 2.373456;48.844444 |
| Paris Gare du Nord | `stop_area:SNCF:87271007` | 2.355389;48.880931 |
| Paris Gare de l'Est | `stop_area:SNCF:87113001` | 2.358611;48.876944 |
| Paris Montparnasse | `stop_area:SNCF:87391003` | 2.320556;48.840833 |
| Paris Saint-Lazare | `stop_area:SNCF:87384008` | 2.325556;48.876111 |
| Paris Austerlitz | `stop_area:SNCF:87547000` | 2.365278;48.840833 |
| Paris Bercy | `stop_area:SNCF:87686048` | 2.383333;48.840278 |

## Major Cities

| Station Name | Station ID | Coordinates |
|--------------|------------|-------------|
| Lyon Part Dieu | `stop_area:SNCF:87722025` | 4.859488;45.760403 |
| Lyon Perrache | `stop_area:SNCF:87723197` | 4.826111;45.749722 |
| Marseille St Charles | `stop_area:SNCF:87751008` | 5.380694;43.302778 |
| Lille Flandres | `stop_area:SNCF:87286005` | 3.073889;50.636111 |
| Lille Europe | `stop_area:SNCF:87223263` | 3.075833;50.638889 |
| Bordeaux St Jean | `stop_area:SNCF:87581009` | -0.555928;44.826067 |
| Toulouse Matabiau | `stop_area:SNCF:87611004` | 1.453889;43.611389 |
| Nice Ville | `stop_area:SNCF:87756056` | 7.261389;43.703889 |
| Strasbourg | `stop_area:SNCF:87212027` | 7.735;48.585 |
| Nantes | `stop_area:SNCF:87481002` | -1.541111;47.217222 |
| Rennes | `stop_area:SNCF:87471003` | -1.672222;48.103333 |
| Montpellier St Roch | `stop_area:SNCF:87773002` | 3.879722;43.604722 |

## Airport Connections

| Station Name | Station ID | Coordinates |
|--------------|------------|-------------|
| Aéroport Charles de Gaulle 2 TGV | `stop_area:SNCF:87271460` | 2.573056;49.003889 |
| Lyon Saint-Exupéry TGV | `stop_area:SNCF:87739847` | 5.079167;45.726111 |

## Tips

- **For other stations**: Use `python scripts/search_stations.py "station name"`
- **Verify IDs**: Use `python scripts/validate_station_id.py "id"` before making journey requests
- **Coordinates format**: lon;lat (longitude first, then latitude)
- **ID format**: Always starts with `stop_area:SNCF:` followed by the UIC code

## Notes

- IDs are based on UIC station codes (International Union of Railways)
- Major stations may have multiple IDs for different areas/platforms
- The IDs above are for the main station areas (`stop_area`)
- For precise platform information, you may need specific stop point IDs
