# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and releases follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
principles for a versioned dataset.

## [Unreleased]

### Added

- A publish-ready `@firmapanel/trade-country-data` npm package under
  `packages/npm`, with ESM, CommonJS, TypeScript, and raw data/schema entry
  points. Its initial packaging release is `0.3.1` and bundles dataset `0.3.0`.
- Automated npm package validation and trusted-publishing release workflows.
- A `firmapanel-trade-country-data` Python package under `packages/pypi`, with
  dependency-free dataset, schema, and CSV access plus typed package metadata.
- Automated wheel and source-distribution validation and trusted PyPI
  publishing with OIDC.

## [0.3.0] - 2026-09-07

### Added

- A dependency-free coverage reporter that verifies README metrics against the
  canonical datasets.
- Unit and CLI regression tests with measured branch coverage enforced in CI.
- Complete four-category official-resource records for 42 additional
  countries: the remaining 21 EU members and 21 direct-country members across
  the G20, EFTA, GCC, MERCOSUR, and ASEAN coverage targets.
- A backward-compatible `country_codes` scope for resources officially shared
  by multiple countries.
- A persistent Zenodo archive for `v0.3.0` under
  [DOI 10.5281/zenodo.22639118](https://doi.org/10.5281/zenodo.22639118).

### Changed

- Expanded complete customs-authority, official-portal, trade-agency, and
  standards-body coverage from 23 to 65 countries.
- Advanced all dataset envelopes to `0.3.0` with an `as_of_date` of 2026-09-07.

## [0.2.0] - 2026-09-06

### Added

- Verified customs-authority, official-trade-portal, trade-agency, and national
  standards-body coverage for 20 additional major trading countries.
- Direct raw JSON and CSV download links near the top of the README.
- A dependency-free JavaScript consumption example for Node.js 18 and later.
- Integrity checks ensuring that every published official resource is linked
  from its matching country record.

### Changed

- Expanded complete four-category official-resource coverage from 3 to 23
  countries.
- Advanced the dataset envelope version to `0.2.0` without changing record
  compatibility.

## [0.1.0] - 2026-09-06

### Added

- Initial `v0.1.0` snapshot as of 2026-09-06.
- 249 ISO 3166-1 country and area records, including 248 UN M49 joins.
- Current tender currency-code arrays derived from Unicode CLDR 48.
- Eleven typed trade-group and agreement records, including EU, EFTA, ASEAN,
  GCC, MERCOSUR, USMCA, AfCFTA, AU, G7, G20, and WTO.
- Five scoped customs-relationship records.
- Initial verified authority, trade portal, trade agency, and standards-body
  coverage for Türkiye, the United Kingdom, and the United States.
- Machine-readable source registry with licenses, retrieval dates,
  normalization notes, field mappings, and update frequencies.
- Canonical JSON datasets and a deterministic country CSV export.
- JSON Schema Draft 2020-12 contracts for every dataset family.
- Dependency-free integrity validation and standards-based schema validation.
- Source, field, model, maintenance, licensing, and legal documentation.
- Continuous integration, structured issue forms, and pull-request guidance.

### Known limitations

- Official-resource coverage is intentionally limited to three reviewed
  countries in the initial snapshot.
- Only UN-designated Land Locked Developing Countries have `landlocked: true`;
  other values remain `null` pending a complete physical-status source.
- One ISO-assigned entry has no separate current UN M49 table row, and two
  records consequently have no UN M49 regional assignment.

[Unreleased]: https://github.com/FirmaPanel/trade-country-data/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/FirmaPanel/trade-country-data/releases/tag/v0.3.0
[0.2.0]: https://github.com/FirmaPanel/trade-country-data/releases/tag/v0.2.0
[0.1.0]: https://github.com/FirmaPanel/trade-country-data/releases/tag/v0.1.0
