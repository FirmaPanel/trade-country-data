# FirmaPanel Trade Country Data

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-2f6f4e.svg)](LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22639118.svg)](https://doi.org/10.5281/zenodo.22639118)
[![Release: v0.3.0](https://img.shields.io/badge/release-v0.3.0-blue.svg)](https://github.com/FirmaPanel/trade-country-data/releases/tag/v0.3.0)
[![Dataset checks](https://github.com/FirmaPanel/trade-country-data/actions/workflows/validate.yml/badge.svg)](https://github.com/FirmaPanel/trade-country-data/actions/workflows/validate.yml)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-blue.svg)](CONTRIBUTING.md)

Trade-focused country reference data for procurement, logistics, customs,
sourcing, and import-export software.

**Direct downloads:** [Raw JSON](https://raw.githubusercontent.com/FirmaPanel/trade-country-data/main/data/countries.json)
· [Raw CSV](https://raw.githubusercontent.com/FirmaPanel/trade-country-data/main/data/countries.csv)

**DOI:** [10.5281/zenodo.22639118](https://doi.org/10.5281/zenodo.22639118)

This project is not another general-purpose list of capitals, flags, calling
codes, or time zones. It connects stable country identifiers to currencies,
trade-group memberships, customs relationships, and verified official trade
resources.

The project is maintained by [FirmaPanel](https://firmapanel.com), a B2B
supplier discovery and procurement platform.

## Why this dataset exists

International trade applications often need more than a country selector.
Procurement, sourcing, customs, and logistics workflows need normalized answers
to questions such as:

- Which trade groups include this country?
- Does the country participate in a documented customs relationship?
- Where is the official customs or import-export guidance?
- Which organization represents the country in national standardization?
- Which source supports each published value, and when was it checked?

This repository supplies those joins without publishing volatile tariff rates,
duty rates, tax percentages, sanctions status, trade volumes, or other values
that should be obtained from a current legal or operational source.

## Snapshot and coverage

The current release is `v0.3.0`, with an `as_of_date` of **2026-09-07**.
Coverage figures are calculated from the committed data:

| Dataset area | Coverage |
| --- | ---: |
| ISO 3166-1 country and area records | 249 |
| Records joined to a UN M49 country/area row | 248 |
| Records with a UN M49 regional assignment | 247 |
| Records with one or more active tender currency codes | 248 |
| Country/customs-territory WTO members | 165 |
| Trade groups and agreements | 11 |
| Customs relationships | 5 |
| Countries with a verified customs authority | 65 |
| Countries with a verified official trade portal | 65 |
| Countries with a verified trade agency | 65 |
| Countries with a verified national standards body | 65 |

Print the calculated table or verify that these published figures are current:

```bash
python3 scripts/report_coverage.py
python3 scripts/report_coverage.py --check
```

Official-resource coverage is intentionally conservative. Missing records use
`null` or an empty array and never a fabricated placeholder.

The reviewed official-resource set covers 65 countries. It now includes every
EU member state and every direct-country member in the G20, EFTA, GCC, ASEAN,
and the active MERCOSUR state-party set represented by this snapshot. Shared
official services are modeled once and linked to each country they serve.

The `landlocked` field is also conservative in this release. The 32 entries
marked `true` are supported by the UN M49 Land Locked Developing Countries
classification. Every other entry is `null`; `null` does not mean coastal.

## Published data

JSON files are canonical. The country CSV is a deterministic generated export.

| File | Purpose |
| --- | --- |
| [`countries.json`](data/countries.json) | Compact country and area records with stable references |
| [`countries.csv`](data/countries.csv) | Flat spreadsheet and database export |
| [`trade-groups.json`](data/trade-groups.json) | Typed memberships for trade groups, organizations, and agreements |
| [`customs-relationships.json`](data/customs-relationships.json) | Scoped customs unions and arrangements |
| [`customs-authorities.json`](data/customs-authorities.json) | Verified national customs authorities |
| [`official-trade-portals.json`](data/official-trade-portals.json) | Official import, export, customs, and trade guidance |
| [`trade-agencies.json`](data/trade-agencies.json) | Trade and export-promotion organizations |
| [`standards-bodies.json`](data/standards-bodies.json) | Verified national standards bodies |
| [`regions.json`](data/regions.json) | UN M49 region hierarchy |
| [`sources.json`](data/sources.json) | Machine-readable provenance registry |

Every JSON file has the same dataset envelope:

```json
{
  "schema_version": "0.3.0",
  "as_of_date": "2026-09-07",
  "record_count": 249,
  "records": []
}
```

## Quick start

Clone and run the dependency-free integrity checks with Python 3.9 or later:

```bash
git clone https://github.com/FirmaPanel/trade-country-data.git
cd trade-country-data
python3 scripts/build_csv.py --check
python3 scripts/validate.py
```

Read a country record in Python:

```python
import json
from pathlib import Path

document = json.loads(Path("data/countries.json").read_text(encoding="utf-8"))
turkiye = next(record for record in document["records"] if record["iso2"] == "TR")
print(turkiye["trade_group_ids"])
print(turkiye["customs_relationship_ids"])
```

Fetch the same canonical data in JavaScript (Node.js 18 or later):

```javascript
const url =
  "https://raw.githubusercontent.com/FirmaPanel/trade-country-data/main/data/countries.json";
const response = await fetch(url);

if (!response.ok) {
  throw new Error(`Dataset request failed: ${response.status}`);
}

const { records } = await response.json();
const turkiye = records.find((record) => record.iso2 === "TR");

console.log(turkiye.trade_group_ids);
console.log(turkiye.customs_relationship_ids);
```

Or query the published JSON without cloning:

```bash
curl -fsSL \
  https://raw.githubusercontent.com/FirmaPanel/trade-country-data/main/data/countries.json \
  | jq '.records[] | select(.iso2 == "TR")'
```

## Country record

Country records remain compact and link to richer datasets through stable IDs:

```json
{
  "name": "Türkiye",
  "official_name": "Republic of Türkiye",
  "iso2": "TR",
  "iso3": "TUR",
  "numeric_code": "792",
  "region_id": "asia",
  "subregion_id": "western-asia",
  "intermediate_region_id": null,
  "currency_codes": [
    "TRY"
  ],
  "trade_group_ids": [
    "group-of-twenty",
    "world-trade-organization"
  ],
  "customs_relationship_ids": [
    "eu-turkiye-customs-union"
  ],
  "wto_member": true,
  "customs_authority_id": "tr-general-directorate-of-customs",
  "trade_portal_ids": [
    "tr-easy-export-platform"
  ],
  "trade_agency_ids": [
    "tr-turkiye-exporters-assembly"
  ],
  "standards_body_id": "tr-turkish-standards-institution",
  "landlocked": null,
  "aliases": [],
  "source_ids": [
    "un-m49",
    "unicode-cldr"
  ]
}
```

The abbreviated `source_ids` above are illustrative; the canonical record
contains every applicable source reference. See the [field reference](docs/fields.md)
and [data model](docs/data-model.md) for the complete contract.

## Relationship semantics

The project deliberately uses **trade groups**, not a generic `trade_blocs`
field. Each group has a controlled `relationship_type` that distinguishes:

- customs unions;
- free-trade areas and trade agreements;
- economic and political unions;
- international or intergovernmental organizations; and
- informal intergovernmental groups.

Participants are typed as either `country` or `trade-group`. A G20 reference to
the African Union, for example, cannot be confused with an ISO country code.
Membership statuses distinguish members and parties from signatories or
suspended participants.

Customs relationships include a scope note. They must never be interpreted as a
promise that every product receives the same treatment.

## Scope methodology

The country scope is the current 249-entry ISO 3166-1 assigned set represented by
the `iso-codes` source package. Of these, 248 join to the English UN M49 country
or area table. The single ISO-only entry is retained with its M49 region fields
set to `null`; Antarctica is present in M49 but has no regional assignment.

This approach includes countries, dependencies, territories, and special areas
with officially assigned ISO codes. It excludes user-assigned, reserved,
transitional, and deleted codes. Inclusion is a coding and interoperability
decision and does not express a position on political status, recognition,
borders, or sovereignty.

Currency arrays contain active tender currencies from Unicode CLDR at the
dataset `as_of_date`. An empty array means no value was published by that method;
it does not mean that commerce cannot occur in the area.

Read [SOURCES.md](SOURCES.md) and the
[source policy](docs/source-policy.md) before interpreting or extending the
dataset.

## Validation and development

Install the standards-validation dependencies and run the complete CI-equivalent
check:

```bash
python3 -m pip install -r requirements-dev.txt
make check
```

The checks verify:

- every JSON document against JSON Schema Draft 2020-12;
- coverage metrics in this README against the canonical JSON;
- dataset metadata, controlled values, dates, IDs, and HTTPS URLs;
- unique ISO codes, record IDs, members, participants, and resource URLs;
- every country, group, relationship, region, resource, and source reference;
- consistency between WTO flags and WTO group membership;
- absence of prohibited volatile data fields; and
- byte-for-byte synchronization of canonical JSON and generated CSV.

Run the unit suite with measured branch coverage:

```bash
make coverage
```

Continuous integration requires at least 95% total coverage.

Do not edit `data/countries.csv` directly. Edit the canonical JSON, run
`python3 scripts/build_csv.py`, and commit both files. See the
[maintenance guide](docs/maintenance.md) for the full workflow.

## Repository layout

```text
trade-country-data/
├── data/                  # Canonical JSON and generated country CSV
├── docs/                  # Field, model, source, maintenance, and legal guides
├── schema/                # JSON Schema Draft 2020-12 contracts
├── scripts/               # Build and validation utilities
├── tests/                 # Unit and CLI regression tests
├── .github/               # CI workflow and contribution templates
├── SOURCES.md             # Human-readable provenance methodology
├── ATTRIBUTION.md         # Reuse and attribution guidance
├── CONTRIBUTING.md        # Contribution and source requirements
├── CITATION.cff           # Citation metadata
└── LICENSE                # CC BY 4.0 for the compilation and documentation
```

## Versioning and maturity

Releases follow semantic-versioning principles for the dataset contract:

- patch releases correct data, URLs, or source metadata;
- minor releases add records or backward-compatible fields; and
- major releases make incompatible schema, ID, or classification changes.

The project remains `v0.x` while official-resource coverage expands and the
schemas receive real-world use. A `v1.0.0` release requires reviewed provenance,
stable schemas, complete core identity data, and fully resolving relationships.
Tagged releases are recommended for reproducible downstream use.

## Contributing

Corrections and carefully sourced additions are welcome. Contributions must
identify the affected record, provide an authoritative source URL and retrieval
date, and explain any replacement of an existing value. Unsourced trade or
customs relationships will not be accepted.

Read [CONTRIBUTING.md](CONTRIBUTING.md) and the
[Code of Conduct](CODE_OF_CONDUCT.md) before opening an issue or pull request.

## License and attribution

FirmaPanel's original compilation, normalization, schemas, and documentation are
available under the [Creative Commons Attribution 4.0 International License](LICENSE).
Maintenance utilities in `scripts/` are available under the
[MIT License](scripts/LICENSE).

Some normalized facts originate from upstream sources with their own terms.
CC BY 4.0 does not replace those terms or grant rights in ISO standards, legal
texts, organization names, or third-party material. See [SOURCES.md](SOURCES.md)
and [ATTRIBUTION.md](ATTRIBUTION.md).

Preferred attribution:

> FirmaPanel Trade Country Data, version 0.3.0, by
> [FirmaPanel](https://firmapanel.com),
> [https://doi.org/10.5281/zenodo.22639118](https://doi.org/10.5281/zenodo.22639118),
> licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

## Disclaimer

This repository provides general reference data for software and informational
use. Trade agreements, customs rules, tariffs, sanctions, taxes, and
import/export requirements may change and may depend on product, origin,
destination, and other factors.

Always verify current requirements with the relevant official authority before
making legal, customs, tax, compliance, or commercial decisions. See the full
[legal and accuracy disclaimer](docs/legal-disclaimer.md).

## About FirmaPanel

[FirmaPanel](https://firmapanel.com) connects B2B product discovery with private
inquiries, supplier quotations, and trade tracking. Trade Country Data is part
of FirmaPanel's open-data initiative for procurement, sourcing, and
international trade developers, maintained through the
[FirmaPanel GitHub organization](https://github.com/FirmaPanel).
