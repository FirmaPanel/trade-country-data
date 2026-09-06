# Sources and methodology

Source transparency is part of the dataset contract. The canonical,
machine-readable registry is [`data/sources.json`](data/sources.json); this file
explains how those sources are selected and interpreted.

## Source hierarchy

The project prefers, in order:

1. the organization responsible for the identifier, membership, agreement, or
   public resource;
2. an official national ministry, customs administration, or standards body;
3. an intergovernmental organization with responsibility for the subject; and
4. a specialist secondary source only when an authoritative source does not
   publish a usable current list.

Crowdsourced country databases, search-result snippets, vendor directories, and
unsourced lists are not accepted as primary evidence.

## Core country identity

### UN M49

The [United Nations Statistics Division M49 overview](https://unstats.un.org/unsd/methodology/m49/overview/)
supplies English short names, M49 numeric codes, ISO alpha codes, geographic
regions, subregions, intermediate regions, and the Land Locked Developing
Countries marker.

The table is normalized as follows:

- codes remain strings so leading zeroes are preserved;
- region names become stable lowercase kebab-case IDs;
- hierarchy records are deduplicated into `regions.json`;
- country records reference those region IDs; and
- an `x` in the LLDC column maps to `landlocked: true`.

Absence from the LLDC column does not prove coastal access, so every unconfirmed
`landlocked` value remains `null` in this release.

### ISO codes and official names

The assigned ISO 3166-1 set, English official names, and aliases were joined from
the [`iso-codes` project](https://salsa.debian.org/iso-codes-team/iso-codes),
version 4.20.1. That package is licensed under LGPL-2.1-or-later. ISO states that
its country codes may be used free of charge; this repository does not reproduce
or claim ownership of the ISO standard.

The selected scope contains 249 currently assigned ISO 3166-1 entries. A code
without a current UN M49 table row is retained for interoperability with region
fields set to `null`. User-assigned, reserved, transitional, and deleted codes
are excluded.

### Currency codes

Current tender currencies come from the Unicode Consortium's
[CLDR 48 supplemental currency data](https://raw.githubusercontent.com/unicode-org/cldr/release-48/common/supplemental/supplementalData.xml),
licensed under the Unicode License v3.

Entries are selected when their CLDR effective interval contains the dataset
`as_of_date` and `tender` is not false. Multiple active currencies are preserved
as an array; no currency is selected as a guessed “primary” value.

## Trade groups and memberships

Each group record cites its own membership source in `source_ids`. Principal
sources include:

- [European Union member countries](https://european-union.europa.eu/principles-countries-history/eu-countries_en);
- [European Free Trade Association](https://www.efta.int/about-efta/european-free-trade-association);
- [ASEAN](https://asean.org/timor-leste-advances-into-a-new-era-of-integration-with-asean/);
- [Gulf Cooperation Council](https://www.gcc-sg.org/en/AboutUs/Pages/FoundingDay.aspx);
- [MERCOSUR countries](https://www.mercosur.int/acerca-del-mercosur/paises);
- [USMCA](https://ustr.gov/trade-agreements/free-trade-agreements/united-states-mexico-canada-agreement);
- [African Union member states](https://au.int/en/member_states/countryprofiles2);
- [G7 membership](https://www.diplomatie.gouv.fr/en/priorites-et-actions/grands-dossiers/la-presidence-francaise-du-g7-2026);
- [G20 membership](https://g20.org/about-g20/); and
- [WTO member data](https://www.wto.org/library/groupings/country_data.js).

AfCFTA party and signatory status uses the current specialist
[tralac AfCFTA status resource](https://www.tralac.org/afcfta-resources.html).
The distinction between signing, domestic ratification, and depositing an
instrument matters. A contributor updating this record should preserve those
states and prefer a current African Union or AfCFTA Secretariat status document
when a usable one is available.

Membership records use ISO alpha-2 IDs for countries and explicit
`trade-group` references for bodies such as the EU and AU. Statuses are not
flattened into a boolean.

## Customs relationships

Relationship sources include:

- the [European Commission EU Customs strategy](https://taxation-customs.ec.europa.eu/customs/eu-customs-strategy_en);
- [EU trade relations with Türkiye](https://policy.trade.ec.europa.eu/eu-trade-relationships-country-and-region/countries-and-regions/turkiye_en);
- the [GCC customs union publication](https://www.gcc-sg.org/en/MediaCenter/DigitalLibrary/Documents/1274258579.pdf);
- [MERCOSUR's member and status page](https://www.mercosur.int/acerca-del-mercosur/paises);
- the [Southern African Customs Union](https://www.sacu.int/about-sacu).

The dataset records relationship type, participants, status, dates when safely
known, and an original scope note. It does not reproduce legal text or imply
that all goods receive identical treatment.

## Official resources

Official authorities, portals, agencies, and standards bodies are added only
after their identity and website have been verified. The reviewed v0.2.0 set
covers 23 countries across four resource categories: customs authority,
official trade portal, trade agency, and national standards body.

The coverage set comprises Australia, Belgium, Brazil, Canada, China, France,
Germany, India, Indonesia, Italy, Japan, Mexico, the Netherlands, Saudi Arabia,
Singapore, South Africa, South Korea, Spain, Türkiye, the United Arab Emirates,
the United Kingdom, the United States, and Viet Nam. Each non-standards record
cites a first-party government or organization page in `data/sources.json`.
National standards-body identity is cross-checked against the
[ISO members list](https://www.iso.org/about/members).

Resource records contain a `last_verified` date. A working URL alone is not
enough: the page must demonstrate the organization's role or the portal's
official status. Coverage remains intentionally selective: a blank resource
reference means not yet reviewed, not that the resource does not exist.

## Source registry fields

Every source record contains:

- a stable source ID;
- title and publishing authority;
- canonical HTTPS URL;
- license and license URL where known;
- a reuse-conditions note;
- retrieval and last-verification dates;
- normalization performed;
- dataset fields supported by the source; and
- planned update frequency.

`null` for a license means the project has not identified a standard open-data
license. It does not mean the source has no copyright or reuse conditions.

## Update and correction policy

Before changing sourced data:

1. open the source directly and confirm it supports the proposed value;
2. prefer a newer first-party source when sources conflict;
3. update the applicable record and source metadata together;
4. retain explicit statuses and dates instead of collapsing uncertainty;
5. regenerate the country CSV; and
6. run `make check`.

If a source is unavailable, do not silently replace it with an unsourced claim.
Open an issue, preserve the last verified value when appropriate, and document
the evidence used for any replacement.
