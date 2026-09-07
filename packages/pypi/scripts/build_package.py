#!/usr/bin/env python3
"""Prepare canonical repository files for the PyPI distribution."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
MODULE_ROOT = PACKAGE_ROOT / "src" / "firmapanel_trade_country_data"


def source_files() -> list[tuple[Path, Path]]:
    files: list[tuple[Path, Path]] = []

    for source in sorted((REPOSITORY_ROOT / "data").iterdir()):
        if source.is_file() and (
            source.suffix == ".json" or source.name == "countries.csv"
        ):
            files.append((source, MODULE_ROOT / "data" / source.name))

    for source in sorted((REPOSITORY_ROOT / "schema").glob("*.json")):
        files.append((source, MODULE_ROOT / "schema" / source.name))

    files.append(
        (REPOSITORY_ROOT / "ATTRIBUTION.md", MODULE_ROOT / "ATTRIBUTION.md")
    )
    files.append(
        (REPOSITORY_ROOT / "ATTRIBUTION.md", PACKAGE_ROOT / "ATTRIBUTION.md")
    )
    files.append((REPOSITORY_ROOT / "LICENSE", PACKAGE_ROOT / "LICENSE"))
    return files


def prepare() -> None:
    for directory in (MODULE_ROOT / "data", MODULE_ROOT / "schema"):
        shutil.rmtree(directory, ignore_errors=True)

    for source, destination in source_files():
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def check() -> list[str]:
    errors: list[str] = []
    expected = source_files()

    for source, destination in expected:
        if not destination.is_file():
            errors.append(f"missing generated file: {destination.relative_to(PACKAGE_ROOT)}")
        elif source.read_bytes() != destination.read_bytes():
            errors.append(f"outdated generated file: {destination.relative_to(PACKAGE_ROOT)}")

    expected_destinations = {destination for _, destination in expected}
    for directory in (MODULE_ROOT / "data", MODULE_ROOT / "schema"):
        if directory.exists():
            for destination in directory.iterdir():
                if destination.is_file() and destination not in expected_destinations:
                    errors.append(f"unexpected generated file: {destination.relative_to(PACKAGE_ROOT)}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify generated files without changing them",
    )
    args = parser.parse_args()

    if args.check:
        errors = check()
        if errors:
            for error in errors:
                print(error)
            return 1
        print("PyPI package data is up to date.")
        return 0

    prepare()
    print("Prepared PyPI package data from the repository snapshot.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
