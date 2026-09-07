# Dataset files

This directory contains the published FirmaPanel Trade Country Data snapshot.

## Canonical and generated files

| File | Role |
| --- | --- |
| `countries.json` | Canonical country and area records |
| `countries.csv` | Generated flat country export |
| `trade-groups.json` | Canonical typed trade-group memberships |
| `customs-relationships.json` | Canonical customs relationships |
| `customs-authorities.json` | Canonical verified customs authorities |
| `official-trade-portals.json` | Canonical verified official portals |
| `trade-agencies.json` | Canonical verified trade agencies |
| `standards-bodies.json` | Canonical verified standards bodies |
| `regions.json` | Canonical UN M49 region registry |
| `sources.json` | Canonical machine-readable source registry |

All JSON documents use a metadata envelope containing `schema_version`,
`as_of_date`, `record_count`, and `records`. Official-resource records use
`country_code` for a national resource or `country_codes` for an officially
shared multi-country resource.

Do not edit `countries.csv` directly. Change `countries.json`, run
`python3 scripts/build_csv.py` from the repository root, and commit both files.
Array values in CSV use a pipe (`|`) delimiter. `null` becomes an empty cell and
booleans use lowercase `true` and `false`.

Every release contains a complete snapshot. Consumers that need reproducible
input should use a tagged release rather than the moving `main` branch.
