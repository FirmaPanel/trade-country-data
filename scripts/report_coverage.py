#!/usr/bin/env python3
"""Report dataset coverage and verify the coverage table in the README."""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Callable
from typing import Any

from dataset_tools import DATASET_FILES, ROOT, load_json, records


README = ROOT / "README.md"

COUNTRY_METRICS: tuple[tuple[str, Callable[[dict[str, Any]], bool]], ...] = (
    ("ISO 3166-1 country and area records", lambda country: True),
    (
        "Records joined to a UN M49 country/area row",
        lambda country: "un-m49" in country.get("source_ids", []),
    ),
    (
        "Records with a UN M49 regional assignment",
        lambda country: country.get("region_id") is not None,
    ),
    (
        "Records with one or more active tender currency codes",
        lambda country: bool(country.get("currency_codes")),
    ),
    (
        "Country/customs-territory WTO members",
        lambda country: country.get("wto_member") is True,
    ),
    (
        "Countries with a verified customs authority",
        lambda country: country.get("customs_authority_id") is not None,
    ),
    (
        "Countries with a verified official trade portal",
        lambda country: bool(country.get("trade_portal_ids")),
    ),
    (
        "Countries with a verified trade agency",
        lambda country: bool(country.get("trade_agency_ids")),
    ),
    (
        "Countries with a verified national standards body",
        lambda country: country.get("standards_body_id") is not None,
    ),
)

METRIC_ORDER = (
    "ISO 3166-1 country and area records",
    "Records joined to a UN M49 country/area row",
    "Records with a UN M49 regional assignment",
    "Records with one or more active tender currency codes",
    "Country/customs-territory WTO members",
    "Trade groups and agreements",
    "Customs relationships",
    "Countries with a verified customs authority",
    "Countries with a verified official trade portal",
    "Countries with a verified trade agency",
    "Countries with a verified national standards body",
)


def calculate_coverage(documents: dict[str, dict[str, Any]]) -> dict[str, int]:
    """Calculate the coverage values published in the README."""

    countries = records(documents["countries"])
    metrics = {
        label: sum(predicate(country) for country in countries)
        for label, predicate in COUNTRY_METRICS
    }
    metrics["Trade groups and agreements"] = len(records(documents["trade_groups"]))
    metrics["Customs relationships"] = len(
        records(documents["customs_relationships"])
    )
    return {label: metrics[label] for label in METRIC_ORDER}


def render_markdown(metrics: dict[str, int]) -> str:
    """Render coverage values as the Markdown table used by the README."""

    lines = ["| Dataset area | Coverage |", "| --- | ---: |"]
    lines.extend(f"| {label} | {value} |" for label, value in metrics.items())
    return "\n".join(lines)


def read_readme_coverage(readme: str) -> dict[str, int]:
    """Extract known coverage rows from README Markdown."""

    values: dict[str, int] = {}
    for label in METRIC_ORDER:
        match = re.search(
            rf"^\|\s*{re.escape(label)}\s*\|\s*([0-9]+)\s*\|\s*$",
            readme,
            flags=re.MULTILINE,
        )
        if match:
            values[label] = int(match.group(1))
    return values


def compare_readme(metrics: dict[str, int], readme: str) -> list[str]:
    """Return coverage-table mismatches between calculated data and README text."""

    published = read_readme_coverage(readme)
    errors: list[str] = []
    for label, expected in metrics.items():
        if label not in published:
            errors.append(f"README coverage row is missing: {label}")
        elif published[label] != expected:
            errors.append(
                f"README coverage for {label!r} is {published[label]}, "
                f"expected {expected}"
            )
    return errors


def load_coverage_documents() -> dict[str, dict[str, Any]]:
    """Load the canonical datasets needed for coverage calculations."""

    families = ("countries", "trade_groups", "customs_relationships")
    return {family: load_json(DATASET_FILES[family]) for family in families}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify that the README coverage table matches canonical data",
    )
    args = parser.parse_args(argv)

    metrics = calculate_coverage(load_coverage_documents())
    if not args.check:
        print(render_markdown(metrics))
        return 0

    errors = compare_readme(metrics, README.read_text(encoding="utf-8"))
    if errors:
        print(f"Coverage check failed with {len(errors)} error(s):", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"README coverage table matches {len(metrics)} calculated metrics.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
