#!/usr/bin/env python3
"""Check package, dataset, and optional release-tag versions."""

from __future__ import annotations

import argparse
import json
import re
import runpy
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("release_tag", nargs="?")
    args = parser.parse_args()

    versions = runpy.run_path(
        str(PACKAGE_ROOT / "src" / "firmapanel_trade_country_data" / "_version.py")
    )
    package_version = versions["__version__"]
    dataset_version = versions["DATASET_VERSION"]
    countries = json.loads(
        (REPOSITORY_ROOT / "data" / "countries.json").read_text(encoding="utf-8")
    )

    pyproject = (PACKAGE_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    if not re.search(
        rf'^version = "{re.escape(package_version)}"$', pyproject, flags=re.MULTILINE
    ):
        raise SystemExit("pyproject.toml and _version.py package versions disagree")
    if not re.search(
        rf'^dataset-version = "{re.escape(dataset_version)}"$',
        pyproject,
        flags=re.MULTILINE,
    ):
        raise SystemExit("pyproject.toml and _version.py dataset versions disagree")
    if dataset_version != countries["schema_version"]:
        raise SystemExit(
            f"Bundled dataset {dataset_version} does not match schema version "
            f"{countries['schema_version']}"
        )
    if args.release_tag and args.release_tag != f"v{package_version}":
        raise SystemExit(
            f"Release tag {args.release_tag} does not match package version v{package_version}"
        )

    print(f"Package {package_version} bundles dataset {dataset_version}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
