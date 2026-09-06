# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and releases follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
principles for a versioned dataset.

## [Unreleased]

### Added

- Initial `v0.1.0`-maturity snapshot as of 2026-09-06.
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

### Limitations

- Official-resource coverage is intentionally limited to three reviewed
  countries in the initial snapshot.
- Only UN-designated Land Locked Developing Countries have `landlocked: true`;
  other values remain `null` pending a complete physical-status source.
- One ISO-assigned entry has no separate current UN M49 table row, and two
  records consequently have no UN M49 regional assignment.

[Unreleased]: https://github.com/FirmaPanel/trade-country-data/commits/main
