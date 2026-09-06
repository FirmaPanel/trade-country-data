# Maintenance guide

This guide describes the review and release workflow for maintainers.

## Prerequisites

- Python 3.9 or later for build and integrity checks;
- packages from `requirements-dev.txt` for JSON Schema validation; and
- direct access to every source affected by a proposed change.

Install the development dependencies:

```bash
python3 -m pip install -r requirements-dev.txt
```

## Editing data

1. Identify the canonical JSON file for the change.
2. Open the cited source and confirm the precise fact and effective status.
3. Update the data record and `data/sources.json` when provenance changes.
4. Preserve sort order and stable IDs.
5. If `countries.json` changed, rebuild the CSV.
6. Run the complete check before review.

```bash
python3 scripts/build_csv.py
make check
```

`build_csv.py --check` is non-mutating and is used by continuous integration.

## Adding a country or area

A new core record requires an officially assigned ISO 3166-1 alpha-2, alpha-3,
and numeric code. Document whether the entry resolves to a UN M49 row. Leave
region fields `null` if it does not; do not infer a classification.

Update trade groups, relationships, currencies, aliases, and source references
only where the cited sources support them. A newly added country must not receive
placeholder official resources.

## Updating a membership

Review whether the change represents invitation, signature, domestic
ratification, deposited ratification, entry into force, active membership,
suspension, or withdrawal. Select the matching status and date rather than
collapsing the event into membership.

After changing group members, synchronize every affected country's
`trade_group_ids`. The validator checks exact agreement between active
`member`/`party` statuses and the country convenience field.

## Updating an official resource

Confirm both that the URL works and that the page establishes the claimed role.
Update `last_verified` only after that review. Prefer a durable organization or
service landing page over a news article or deep session URL.

If an organization has been replaced, add or update source evidence and
consider whether the stable record ID can remain. Removing or renaming an ID
may require a major release.

## Release checklist

- [ ] All data files share one `schema_version` and `as_of_date`.
- [ ] Coverage metrics in the README match the committed data.
- [ ] New and changed claims have authoritative source records.
- [ ] Membership and customs statuses reflect effective dates.
- [ ] `countries.csv` is regenerated and synchronized.
- [ ] `make check` passes on every supported Python version.
- [ ] Documentation and examples match the schema.
- [ ] `CHANGELOG.md` records coverage, limitations, and notable changes.
- [ ] Source licenses and attribution obligations have been reviewed.

Tag a `v0.x` release until the stability criteria in the README are met. Release
notes should state the as-of date, schema version, record counts, coverage, and
known limitations.
