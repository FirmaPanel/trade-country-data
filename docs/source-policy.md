# Source policy

This policy governs evidence, provenance, and review for every published record.
The human-readable source overview is [SOURCES.md](../SOURCES.md), while
[`data/sources.json`](../data/sources.json) is canonical for machine use.

## Acceptance standard

A source must be identifiable, accessible to reviewers, relevant to the exact
claim, and authoritative enough for the data family. Prefer the body that
maintains the identifier, organization, agreement, or official service.

Acceptable sources normally include:

- the United Nations, WTO, ISO, and other responsible international bodies;
- official trade-group and agreement secretariats;
- national customs, trade, commerce, and standards authorities;
- official government portals; and
- a specialist institutional source when no authoritative current status list
  is practically available.

Do not use search-result text, social-media posts, AI-generated citations,
anonymous documents, commercial country summaries, or crowdsourced databases as
the sole evidence for a record.

## Required provenance

Every non-source record has at least one `source_ids` value resolving to the
source registry. A source record documents:

- title and publishing authority;
- canonical HTTPS URL;
- known license and reuse terms;
- retrieval and last-verification dates;
- normalization and field mapping; and
- update frequency.

When one record combines multiple sources, include every source that materially
supports its published fields.

## Conflicts and uncertainty

When sources conflict:

1. compare their publication and effective dates;
2. prefer the body legally or institutionally responsible for the fact;
3. distinguish different concepts such as signing, ratification, deposit, and
   entry into force;
4. preserve status and dates rather than choosing a misleading boolean; and
5. describe unresolved uncertainty in a note or leave the value unknown.

Do not guess to improve apparent coverage.

## Licensing and extraction

Facts and identifiers may still arrive through sources with terms that must be
respected. Record the license when known, reproduce no protected legal or
standards text, and summarize scope notes in original wording.

The repository's CC BY 4.0 license applies to FirmaPanel's original compilation,
normalization, schema, documentation, and notes. It does not replace upstream
licenses or create rights in standards, trademarks, official publications, or
third-party material.

## Verification dates

`retrieved_date` says when source information entered the snapshot.
`last_verified` says when a maintainer most recently confirmed that the source
still supported the published value. These dates are evidence metadata, not a
guarantee that the real-world value has remained unchanged.

Official-resource links should be rechecked at least annually. Memberships and
customs relationships should be checked before every release and whenever a
responsible organization announces a change.

URL-availability monitoring may be automated separately, but transient network
failures must not invalidate deterministic data-integrity checks.
