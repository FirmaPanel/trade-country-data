# Field reference

JSON Schema Draft 2020-12 files in [`schema/`](../schema/) are the authoritative
machine-readable contracts. This guide explains their intended use.

## Dataset envelope

Every canonical JSON file is an object with the same four fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `schema_version` | string | Semantic version of the dataset contract |
| `as_of_date` | ISO date | Date represented by the published snapshot |
| `record_count` | integer | Number of items in `records` |
| `records` | array | Dataset-family records |

Validation requires all canonical files in a snapshot to share the same schema
version and as-of date.

## Country fields

| Field | Type | Meaning |
| --- | --- | --- |
| `name` | string | English short country or area name |
| `official_name` | string or null | English official name when published |
| `iso2` | string | ISO 3166-1 alpha-2 identifier and country key |
| `iso3` | string | ISO 3166-1 alpha-3 identifier |
| `numeric_code` | string | Three-digit numeric identifier with zeroes preserved |
| `region_id` | ID or null | UN M49 region reference |
| `subregion_id` | ID or null | UN M49 subregion reference |
| `intermediate_region_id` | ID or null | UN M49 intermediate-region reference |
| `currency_codes` | string array | Active tender currency codes at `as_of_date` |
| `trade_group_ids` | ID array | Groups in which the country is an active member or party |
| `customs_relationship_ids` | ID array | Customs relationships relevant to the country |
| `wto_member` | boolean | Convenience value synchronized with the WTO group |
| `customs_authority_id` | ID or null | Verified customs-authority reference |
| `trade_portal_ids` | ID array | Verified official portal references |
| `trade_agency_ids` | ID array | Verified trade-agency references |
| `standards_body_id` | ID or null | Verified national standards-body reference |
| `landlocked` | boolean or null | Confirmed physical status; unresolved values are null |
| `aliases` | string array | Alternate names useful for joins and search |
| `source_ids` | ID array | Provenance records supporting the country record |

An empty array means that the snapshot contains no value under its documented
methodology. It is not proof that no real-world relationship or resource exists.

## Trade-group fields

| Field | Type | Meaning |
| --- | --- | --- |
| `id` | ID | Stable group identifier |
| `name` | string | Canonical English display name |
| `short_name` | string or null | Widely used abbreviation |
| `relationship_type` | enum | Nature of the group or agreement |
| `members` | membership array | Typed references with explicit status and optional dates |
| `official_website` | HTTPS URL | Group's official website |
| `source_ids` | ID array | Membership and classification sources |
| `last_verified` | ISO date | Most recent review date |
| `notes` | string | Optional scope or interpretation note |

Controlled `relationship_type` values are `customs-union`,
`economic-and-political-union`, `free-trade-area`,
`free-trade-association`, `intergovernmental-group`,
`intergovernmental-organization`, `international-organization`, and
`trade-agreement`.

A membership has `type`, `id`, and `status`, with optional `effective_from` and
`effective_to`. Status is one of `member`, `party`, `signatory`, or `suspended`.

## Customs-relationship fields

| Field | Type | Meaning |
| --- | --- | --- |
| `id` | ID | Stable relationship identifier |
| `name` | string | Display name |
| `relationship_type` | enum | `customs-union` or `customs-arrangement` |
| `participants` | participant array | Typed country or trade-group references |
| `status` | enum | `active`, `inactive`, or `superseded` |
| `effective_from` | date or null | Known effective date |
| `effective_to` | date or null | Known end date |
| `scope_note` | string | Original caution about coverage and exclusions |
| `source_ids` | ID array | Authoritative supporting sources |
| `last_verified` | ISO date | Most recent review date |

## Official-resource fields

All resource records include a stable `id`, `name`, HTTPS `website`,
`source_ids`, and `last_verified`. A resource scoped to one country uses the
ISO alpha-2 `country_code` field. A resource officially serving multiple
countries uses a sorted, unique `country_codes` array instead. Exactly one of
those two scope fields is required.

- Customs authorities add a controlled `authority_type` and language codes.
- Trade portals add a controlled `portal_type`, topics, and language codes.
- Trade agencies add a controlled `agency_type` and services.
- Standards bodies add an acronym and the fixed organization type
  `national-standards-body`.

## Region fields

Region records have `id`, three-digit `code`, `name`, nullable `parent_id`,
`level`, fixed `classification_system: "UN-M49"`, and `source_ids`.

## Source fields

The source registry records source identity, authority, URL, known license,
reuse conditions, retrieval and verification dates, normalization, supported
fields, and update frequency. See [SOURCES.md](../SOURCES.md) for policy.

## CSV representation

`countries.csv` contains commonly joined fields in stable column order. Arrays
use a pipe (`|`) delimiter, null becomes an empty cell, and booleans use lowercase
text. Normal CSV quote escaping applies. JSON remains the source of truth.
