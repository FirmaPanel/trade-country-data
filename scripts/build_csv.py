#!/usr/bin/env python3
"""Build or check the generated countries CSV export."""

from __future__ import annotations

import argparse
import sys

from dataset_tools import COUNTRIES_CSV, DATASET_FILES, ROOT, load_json, render_countries_csv


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify the committed export without changing it",
    )
    args = parser.parse_args()

    content = render_countries_csv(load_json(DATASET_FILES["countries"]))
    if args.check:
        if not COUNTRIES_CSV.exists():
            print("Missing generated export: data/countries.csv", file=sys.stderr)
            return 1
        if COUNTRIES_CSV.read_text(encoding="utf-8") != content:
            print(
                "Outdated generated export: data/countries.csv. "
                "Run python3 scripts/build_csv.py.",
                file=sys.stderr,
            )
            return 1
        print("Generated countries CSV is up to date.")
        return 0

    changed = not COUNTRIES_CSV.exists() or COUNTRIES_CSV.read_text(
        encoding="utf-8"
    ) != content
    if changed:
        with COUNTRIES_CSV.open("w", encoding="utf-8", newline="") as output:
            output.write(content)
        print(f"Updated: {COUNTRIES_CSV.relative_to(ROOT)}")
    else:
        print("Countries CSV is already up to date.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
