"""Setuptools backend that prepares monorepo data before package builds."""

from __future__ import annotations

import runpy
from pathlib import Path
from typing import Any, Optional

from setuptools import build_meta as _setuptools

PACKAGE_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = PACKAGE_ROOT.parents[1]
MODULE_ROOT = PACKAGE_ROOT / "src" / "firmapanel_trade_country_data"
DATA_FILES = (
    "countries.csv",
    "countries.json",
    "customs-authorities.json",
    "customs-relationships.json",
    "official-trade-portals.json",
    "regions.json",
    "sources.json",
    "standards-bodies.json",
    "trade-agencies.json",
    "trade-groups.json",
)
SCHEMA_FILES = (
    "common.schema.json",
    "country.schema.json",
    "customs-authority.schema.json",
    "customs-relationship.schema.json",
    "region.schema.json",
    "source.schema.json",
    "standards-body.schema.json",
    "trade-agency.schema.json",
    "trade-group.schema.json",
    "trade-portal.schema.json",
)


def _prepare() -> None:
    build_script = PACKAGE_ROOT / "scripts" / "build_package.py"
    if (
        (REPOSITORY_ROOT / "data" / "countries.json").is_file()
        and build_script.is_file()
    ):
        script = runpy.run_path(str(build_script))
        script["prepare"]()
        return

    required = [
        PACKAGE_ROOT / "LICENSE",
        PACKAGE_ROOT / "ATTRIBUTION.md",
    ]
    required.extend(MODULE_ROOT / "data" / name for name in DATA_FILES)
    required.extend(MODULE_ROOT / "schema" / name for name in SCHEMA_FILES)
    missing = [path.relative_to(PACKAGE_ROOT) for path in required if not path.is_file()]
    if missing:
        names = ", ".join(str(path) for path in missing)
        raise RuntimeError(f"Source distribution is missing generated files: {names}")


def get_requires_for_build_wheel(config_settings: Any = None) -> list[str]:
    _prepare()
    return _setuptools.get_requires_for_build_wheel(config_settings)


def prepare_metadata_for_build_wheel(
    metadata_directory: str,
    config_settings: Any = None,
) -> str:
    _prepare()
    return _setuptools.prepare_metadata_for_build_wheel(
        metadata_directory,
        config_settings,
    )


def build_wheel(
    wheel_directory: str,
    config_settings: Any = None,
    metadata_directory: Optional[str] = None,
) -> str:
    _prepare()
    return _setuptools.build_wheel(
        wheel_directory,
        config_settings,
        metadata_directory,
    )


def get_requires_for_build_sdist(config_settings: Any = None) -> list[str]:
    _prepare()
    return _setuptools.get_requires_for_build_sdist(config_settings)


def build_sdist(sdist_directory: str, config_settings: Any = None) -> str:
    _prepare()
    return _setuptools.build_sdist(sdist_directory, config_settings)


def get_requires_for_build_editable(config_settings: Any = None) -> list[str]:
    _prepare()
    return _setuptools.get_requires_for_build_editable(config_settings)


def prepare_metadata_for_build_editable(
    metadata_directory: str,
    config_settings: Any = None,
) -> str:
    _prepare()
    return _setuptools.prepare_metadata_for_build_editable(
        metadata_directory,
        config_settings,
    )


def build_editable(
    wheel_directory: str,
    config_settings: Any = None,
    metadata_directory: Optional[str] = None,
) -> str:
    _prepare()
    return _setuptools.build_editable(
        wheel_directory,
        config_settings,
        metadata_directory,
    )
