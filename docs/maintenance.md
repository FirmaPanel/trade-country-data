# Maintenance guide

This guide describes the review and release workflow for maintainers.

## Prerequisites

- Python 3.9 or later for build and integrity checks;
- Node.js 18 or later for npm package checks;
- packages from `requirements-dev.txt` for JSON Schema validation; and
- direct access to every source affected by a proposed change.

Install the development dependencies:

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m pip install build twine
```

## Editing data

1. Identify the canonical JSON file for the change.
2. Open the cited source and confirm the precise fact and effective status.
3. Update the data record and `data/sources.json` when provenance changes.
4. Preserve sort order and stable IDs.
5. If `countries.json` changed, rebuild the CSV.
6. Update the README coverage table when calculated metrics changed.
7. Run the complete check before review.

```bash
python3 scripts/build_csv.py
make check
```

`build_csv.py --check` is non-mutating and is used by continuous integration.
`report_coverage.py --check` similarly verifies that README coverage figures
match the canonical datasets.

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

Use `country_code` for a resource serving one country. Use a sorted
`country_codes` array only when the source explicitly supports multi-country
scope, and link the shared resource ID from every covered country record.

## Release checklist

- [ ] All data files share one `schema_version` and `as_of_date`.
- [ ] Coverage metrics in the README match the committed data.
- [ ] New and changed claims have authoritative source records.
- [ ] Membership and customs statuses reflect effective dates.
- [ ] `countries.csv` is regenerated and synchronized.
- [ ] `make check` passes on every supported Python version.
- [ ] The npm package's `datasetVersion` matches the dataset `schema_version`.
- [ ] The npm package `version` is ready for a new, unpublished npm release.
- [ ] `make npm-check` and `make npm-pack` pass.
- [ ] The PyPI package's `DATASET_VERSION` matches `schema_version`.
- [ ] The PyPI package `version` is ready for a new, unpublished PyPI release.
- [ ] `make pypi-check` and `make pypi-build` pass.
- [ ] Documentation and examples match the schema.
- [ ] `CHANGELOG.md` records coverage, limitations, and notable changes.
- [ ] Source licenses and attribution obligations have been reviewed.

Tag a `v0.x` release until the stability criteria in the README are met. Release
notes should state the as-of date, schema version, record counts, coverage, and
known limitations.

Publishing a GitHub release automatically publishes the matching npm package.
The workflow refuses to publish when the release tag and npm package version
disagree, or when the declared bundled dataset does not match the canonical
schema version. For the package's one-time initial publication, run:

```bash
cd packages/npm
npm login
npm publish --access public
```

After the package exists, configure its npm trusted publisher for the GitHub
repository `FirmaPanel/trade-country-data`, workflow `publish-npm.yml`, with
direct publishing allowed. The workflow uses npm's short-lived OIDC credentials
and publishes provenance without a repository token.

The Python package is published through PyPI trusted publishing. For its first
release, create a pending publisher for project `firmapanel-trade-country-data`
with owner `FirmaPanel`, repository `trade-country-data`, workflow
`publish-pypi.yml`, and environment `pypi`. Then run the workflow manually from
the repository's default branch. Later matching GitHub releases publish both
package formats automatically.
