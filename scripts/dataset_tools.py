"""Shared, dependency-free helpers for trade country data."""

from __future__ import annotations

import csv
import io
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
SCHEMA_DIR = ROOT / "schema"

DATASET_FILES = {
    "countries": DATA_DIR / "countries.json",
    "trade_groups": DATA_DIR / "trade-groups.json",
    "customs_relationships": DATA_DIR / "customs-relationships.json",
    "customs_authorities": DATA_DIR / "customs-authorities.json",
    "trade_portals": DATA_DIR / "official-trade-portals.json",
    "trade_agencies": DATA_DIR / "trade-agencies.json",
    "standards_bodies": DATA_DIR / "standards-bodies.json",
    "regions": DATA_DIR / "regions.json",
    "sources": DATA_DIR / "sources.json",
}

SCHEMA_FILES = {
    "countries": SCHEMA_DIR / "country.schema.json",
    "trade_groups": SCHEMA_DIR / "trade-group.schema.json",
    "customs_relationships": SCHEMA_DIR / "customs-relationship.schema.json",
    "customs_authorities": SCHEMA_DIR / "customs-authority.schema.json",
    "trade_portals": SCHEMA_DIR / "trade-portal.schema.json",
    "trade_agencies": SCHEMA_DIR / "trade-agency.schema.json",
    "standards_bodies": SCHEMA_DIR / "standards-body.schema.json",
    "regions": SCHEMA_DIR / "region.schema.json",
    "sources": SCHEMA_DIR / "source.schema.json",
}

COUNTRIES_CSV = DATA_DIR / "countries.csv"

CSV_FIELDS = (
    "iso2",
    "iso3",
    "numeric_code",
    "name",
    "official_name",
    "region_id",
    "subregion_id",
    "intermediate_region_id",
    "currency_codes",
    "wto_member",
    "landlocked",
    "trade_group_ids",
    "customs_relationship_ids",
    "customs_authority_id",
    "trade_portal_ids",
    "trade_agency_ids",
    "standards_body_id",
    "aliases",
)


def load_json(path: Path) -> Any:
    """Load UTF-8 JSON and include the repository path in decode errors."""

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc


def records(document: dict[str, Any]) -> list[dict[str, Any]]:
    """Return records from a validated dataset envelope."""

    return document["records"]


def render_countries_csv(document: dict[str, Any]) -> str:
    """Render a deterministic RFC 4180-style flat country export."""

    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=CSV_FIELDS, lineterminator="\n")
    writer.writeheader()

    for record in records(document):
        row: dict[str, Any] = {}
        for field in CSV_FIELDS:
            value = record.get(field)
            if isinstance(value, list):
                row[field] = "|".join(value)
            elif isinstance(value, bool):
                row[field] = "true" if value else "false"
            elif value is None:
                row[field] = ""
            else:
                row[field] = value
        writer.writerow(row)

    return output.getvalue()
