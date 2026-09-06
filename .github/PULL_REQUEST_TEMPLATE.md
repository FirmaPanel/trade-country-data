# Pull request

## Summary

<!-- Describe what changed and why. Link related issues where applicable. -->

## Type of change

- [ ] Country identity, region, currency, or alias correction
- [ ] Trade-group membership or status change
- [ ] Customs relationship change
- [ ] Official resource addition or correction
- [ ] Source or license metadata change
- [ ] Schema, documentation, or maintenance change

## Sources and effective date

<!--
Link the authoritative source, give the retrieval date, and distinguish the
announcement date from the effective date where relevant.
-->

## Checklist

- [ ] I identified every affected stable ID.
- [ ] I used an authoritative source and updated `data/sources.json`.
- [ ] I represented status and effective dates precisely.
- [ ] I did not add volatile rates, sanctions, restrictions, or legal advice.
- [ ] I preserved `null` or empty arrays for facts that remain unverified.
- [ ] I synchronized `countries.csv` if country data changed.
- [ ] I ran `make check` successfully.
- [ ] I reviewed applicable source licensing and reuse conditions.
- [ ] I agree to CC BY 4.0 for content or MIT for code under `scripts/`.
