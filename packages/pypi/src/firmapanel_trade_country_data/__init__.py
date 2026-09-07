"""Access the FirmaPanel Trade Country Data snapshot."""

from __future__ import annotations

import json
from importlib import resources
from typing import Any, Dict, Tuple

from ._version import DATASET_VERSION, __version__

DATASET_NAMES: Tuple[str, ...] = (
    "countries",
    "customs-authorities",
    "customs-relationships",
    "official-trade-portals",
    "regions",
    "sources",
    "standards-bodies",
    "trade-agencies",
    "trade-groups",
)

SCHEMA_NAMES: Tuple[str, ...] = (
    "common",
    "country",
    "customs-authority",
    "customs-relationship",
    "region",
    "source",
    "standards-body",
    "trade-agency",
    "trade-group",
    "trade-portal",
)


def _named_resource(directory: str, name: str, choices: Tuple[str, ...], suffix: str) -> Any:
    if name not in choices:
        available = ", ".join(choices)
        raise ValueError(f"Unknown {directory} name {name!r}; choose one of: {available}")

    return resources.files(__package__).joinpath(directory).joinpath(f"{name}{suffix}")


def dataset_file(name: str) -> Any:
    """Return a Traversable for a canonical JSON dataset."""

    return _named_resource("data", name, DATASET_NAMES, ".json")


def schema_file(name: str) -> Any:
    """Return a Traversable for a bundled JSON Schema document."""

    return _named_resource("schema", name, SCHEMA_NAMES, ".schema.json")


def load_dataset(name: str) -> Dict[str, Any]:
    """Load a canonical dataset by name."""

    with dataset_file(name).open("r", encoding="utf-8") as stream:
        return json.load(stream)


def load_schema(name: str) -> Dict[str, Any]:
    """Load a JSON Schema document by name."""

    with schema_file(name).open("r", encoding="utf-8") as stream:
        return json.load(stream)


def read_countries_csv() -> str:
    """Return the generated flat country export as UTF-8 text."""

    return (
        resources.files(__package__)
        .joinpath("data")
        .joinpath("countries.csv")
        .read_text(encoding="utf-8")
    )


__all__ = [
    "DATASET_NAMES",
    "DATASET_VERSION",
    "SCHEMA_NAMES",
    "__version__",
    "dataset_file",
    "load_dataset",
    "load_schema",
    "read_countries_csv",
    "schema_file",
]
