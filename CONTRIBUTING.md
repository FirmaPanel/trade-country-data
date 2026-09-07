# Contributing to FirmaPanel Trade Country Data

Thank you for helping improve an open reference for international trade,
procurement, customs, sourcing, and logistics applications.

By participating, you agree to follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## Before you contribute

Search existing data and issues before proposing a change. Stable IDs are public
integration keys, and an empty value may represent deliberately unverified
coverage rather than an accidental omission.

Small corrections may be submitted directly as pull requests. Open an issue
first for a schema change, bulk import, new data family, changed country-scope
methodology, or renamed stable ID.

## Ways to contribute

- correct a country identity, currency, region, or alias;
- update a trade-group membership or status;
- document a customs relationship with an authoritative source;
- add or correct an official authority, portal, agency, or standards body;
- improve source licensing or provenance metadata;
- strengthen schemas, validation, exports, or documentation; or
- report a broken official-resource URL.

## Evidence requirements

Every data contribution must provide:

- the affected country, group, relationship, or resource;
- the proposed value;
- an authoritative source URL;
- the date the source was retrieved;
- the effective date or status when relevant; and
- an explanation when replacing a current value.

Prefer the responsible standards organization, treaty body, secretariat,
government, customs administration, ministry, or national standards body. Do not
submit a search-result snippet, vendor directory, or crowdsourced list as the
only evidence.

Read the [source policy](docs/source-policy.md) and [SOURCES.md](SOURCES.md)
before contributing data.

## Data rules

- Use uppercase ISO alpha-2 codes for country IDs.
- Use lowercase kebab-case for repository-defined IDs.
- Keep stable IDs unchanged unless a migration has been discussed.
- Use typed `country` or `trade-group` references.
- Preserve `member`, `party`, `signatory`, and `suspended` distinctions.
- Use ISO 8601 `YYYY-MM-DD` dates.
- Use `null` or an empty array for unknown optional data; never guess.
- Link to official tariff or guidance services instead of copying live rates.
- Do not add tax percentages, tariffs, sanctions, restrictions, or other
  volatile decision data.
- Write scope notes in concise, neutral, original language.

## Official resources

A working URL is not sufficient evidence. Confirm that the page establishes the
organization's official role, prefer a durable HTTPS landing page, and set
`last_verified` to the date of that review. Do not add a placeholder to improve
coverage metrics.

Use `country_codes` instead of `country_code` only when the cited evidence
establishes that one resource officially serves every listed country. Keep the
array sorted and link the shared record from each covered country.

## AI-assisted work

AI tools may help research or draft a contribution, but contributors remain
responsible for every fact, citation, status, and date. Do not submit invented
sources, unreviewed bulk content, or wording that may reproduce protected text.

## Development workflow

1. Fork the repository and create a focused branch from `main`.
2. Make the smallest coherent change.
3. Update source metadata with the data it supports.
4. Regenerate `countries.csv` if `countries.json` changed.
5. Install development requirements and run the complete checks.
6. Open a pull request explaining what changed and why.

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/build_csv.py
make check
```

## Pull-request checklist

- [ ] I identified every affected record and stable ID.
- [ ] I linked an authoritative source and recorded the retrieval date.
- [ ] Statuses, effective dates, and scope notes are precise.
- [ ] I did not add volatile rates, restrictions, or sanctions data.
- [ ] Source licensing and reuse conditions are documented where known.
- [ ] Generated CSV is synchronized when country data changed.
- [ ] `make check` passes locally.
- [ ] The change contains no confidential, personal, or proprietary material.

## Licensing contributions

By submitting dataset or documentation contributions, you agree that your
original contribution may be distributed under the repository's
[CC BY 4.0 license](LICENSE). By submitting code under `scripts/`, you agree that
it may be distributed under the [MIT License](scripts/LICENSE). You represent
that you have the right to submit the material. Contributors retain copyright
in their original work.

If you cannot agree to these terms, do not submit the contribution.
