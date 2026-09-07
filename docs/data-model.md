# Data model

The model separates compact country records from group, relationship, resource,
region, and source registries. Stable IDs form the joins.

```text
country (ISO alpha-2 key)
├── region IDs ───────────────────────────> regions
├── trade_group_ids ──────────────────────> trade groups
├── customs_relationship_ids ─────────────> customs relationships
├── customs_authority_id ─────────────────> customs authorities
├── trade_portal_ids ─────────────────────> official trade portals
├── trade_agency_ids ─────────────────────> trade agencies
├── standards_body_id ────────────────────> standards bodies
└── source_ids ────────────────────────────> sources

trade group / customs relationship
├── typed country references ─────────────> countries
├── typed trade-group references ─────────> trade groups
└── source_ids ────────────────────────────> sources
```

## Stable identifiers

- Countries use uppercase ISO alpha-2 codes because those are the principal
  interoperability keys.
- Repository-defined records use lowercase kebab-case IDs.
- Region IDs are normalized from the corresponding UN M49 English name.
- IDs are never display labels and must not be silently reused.

Changing or removing an existing stable ID is a breaking change. A display-name
correction normally leaves the ID unchanged.

## Typed participants

Group memberships and customs relationships do not mix country codes and
organization IDs in an untyped string array. Each reference declares its target:

```json
{
  "type": "trade-group",
  "id": "european-union"
}
```

The validator confirms that the target exists in the declared dataset family,
detects duplicates, and rejects circular trade-group references.

## Shared official resources

Most official-resource records use one `country_code`. When an authoritative
source establishes that the same organization or service officially covers
multiple countries, the record uses one sorted `country_codes` array instead.
Country records can then reference that shared ID without duplicating the
resource or implying separate national organizations.

## Time and status

The dataset-level `as_of_date` describes a coherent snapshot. Individual
memberships and relationships may add effective dates where a source supports
them. Unknown dates remain absent or `null`; they are never inferred.

Membership status is explicit. In particular, `party`, `signatory`, and
`suspended` are not treated as synonyms. Only `member` and `party` memberships
are copied into a country's `trade_group_ids` convenience field.

## Null and empty values

Nulls and empty arrays are meaningful:

- `null` means a nullable scalar value is unknown or not published under the
  current method;
- `[]` means no referenced records are included in this snapshot; and
- neither form proves that no real-world value exists.

This rule is especially important for official resources and `landlocked`.

## Canonical and derived data

All JSON files are canonical and reviewable. `countries.csv` is derived from
`countries.json` and must not be edited directly. Its arrays are lossy flat
representations intended for spreadsheets and relational imports.

## Deliberately excluded data

The model excludes volatile or decision-sensitive values such as tariffs, duty
percentages, sanctions, tax rates, thresholds, trade volumes, freight rates,
and current import restrictions. Links to official lookup services may be
included, but their live values are not copied into the reference dataset.
