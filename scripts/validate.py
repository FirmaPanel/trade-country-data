#!/usr/bin/env python3
"""Validate dataset integrity, references, controlled values, and CSV output."""

from __future__ import annotations

import re
import sys
from collections import Counter
from datetime import date
from typing import Any, Iterable, Optional
from urllib.parse import urlparse

from dataset_tools import (
    COUNTRIES_CSV,
    DATASET_FILES,
    SCHEMA_FILES,
    load_json,
    records,
    render_countries_csv,
)


ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ISO2_PATTERN = re.compile(r"^[A-Z]{2}$")
ISO3_PATTERN = re.compile(r"^[A-Z]{3}$")
NUMERIC_PATTERN = re.compile(r"^[0-9]{3}$")
CURRENCY_PATTERN = re.compile(r"^[A-Z]{3}$")
SEMVER_PATTERN = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")

EXPECTED_ENVELOPE_FIELDS = {
    "schema_version",
    "as_of_date",
    "record_count",
    "records",
}
FORBIDDEN_VOLATILE_FIELDS = {
    "exchange_rate",
    "tariff_rate",
    "duty_rate",
    "sanctions_status",
    "customs_threshold",
    "vat_rate",
    "gst_rate",
    "gdp",
    "inflation",
    "freight_rate",
    "port_congestion",
    "clearance_time",
}
TRADE_GROUP_TYPES = {
    "customs-union",
    "economic-and-political-union",
    "free-trade-area",
    "free-trade-association",
    "intergovernmental-group",
    "intergovernmental-organization",
    "international-organization",
    "trade-agreement",
}
MEMBERSHIP_STATUSES = {"member", "party", "signatory", "suspended"}
CUSTOMS_RELATIONSHIP_TYPES = {"customs-union", "customs-arrangement"}
CUSTOMS_RELATIONSHIP_STATUSES = {"active", "inactive", "superseded"}
AUTHORITY_TYPES = {
    "border-and-customs-administration",
    "customs-administration",
    "tax-and-customs-authority",
}
PORTAL_TYPES = {
    "customs",
    "export-guidance",
    "import-guidance",
    "single-window",
    "standards",
    "tariff-lookup",
    "trade-information",
    "trade-statistics",
}
AGENCY_TYPES = {
    "export-promotion",
    "government-trade-agency",
    "investment-promotion",
    "trade-and-investment",
    "trade-promotion",
}
REGION_LEVELS = {"region", "subregion", "intermediate-region"}


def duplicates(values: Iterable[str]) -> list[str]:
    counts = Counter(values)
    return sorted(value for value, count in counts.items() if count > 1)


def valid_date(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def walk(value: Any, location: str = "root") -> Iterable[tuple[str, str, Any]]:
    if isinstance(value, dict):
        for key, child in value.items():
            child_location = f"{location}.{key}"
            yield child_location, key, child
            yield from walk(child, child_location)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk(child, f"{location}[{index}]")


def validate_envelopes(
    documents: dict[str, dict[str, Any]], errors: list[str]
) -> None:
    versions: set[str] = set()
    dates: set[str] = set()
    for family, document in documents.items():
        path = DATASET_FILES[family].name
        if not isinstance(document, dict):
            errors.append(f"{path} must contain an object")
            continue
        if set(document) != EXPECTED_ENVELOPE_FIELDS:
            errors.append(
                f"{path} envelope must contain only: "
                + ", ".join(sorted(EXPECTED_ENVELOPE_FIELDS))
            )
        version = document.get("schema_version")
        if not isinstance(version, str) or not SEMVER_PATTERN.fullmatch(version):
            errors.append(f"{path}.schema_version must be x.y.z")
        else:
            versions.add(version)
        as_of = document.get("as_of_date")
        if not valid_date(as_of):
            errors.append(f"{path}.as_of_date must be an ISO 8601 date")
        else:
            dates.add(as_of)
        dataset_records = document.get("records")
        if not isinstance(dataset_records, list):
            errors.append(f"{path}.records must be an array")
            continue
        if document.get("record_count") != len(dataset_records):
            errors.append(f"{path}.record_count does not match records length")
    if len(versions) > 1:
        errors.append("all datasets must publish the same schema_version")
    if len(dates) > 1:
        errors.append("all datasets must publish the same as_of_date")


def validate_common_values(documents: dict[str, dict[str, Any]], errors: list[str]) -> None:
    for family, document in documents.items():
        path = DATASET_FILES[family].name
        for location, key, value in walk(document, path):
            if key in FORBIDDEN_VOLATILE_FIELDS:
                errors.append(f"{location} is a forbidden volatile field")
            if key in {"as_of_date", "last_verified", "retrieved_date"} or key in {
                "effective_from",
                "effective_to",
            }:
                if value is not None and not valid_date(value):
                    errors.append(f"{location} must be an ISO 8601 date or null")
            if key in {"url", "website", "official_website", "license_url"}:
                if value is not None:
                    parsed = urlparse(value) if isinstance(value, str) else None
                    if not parsed or parsed.scheme != "https" or not parsed.netloc:
                        errors.append(f"{location} must be an absolute HTTPS URL")


def index_records(
    family: str,
    document: dict[str, Any],
    key: str,
    pattern: re.Pattern[str],
    errors: list[str],
) -> dict[str, dict[str, Any]]:
    values: list[str] = []
    indexed: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(records(document)):
        location = f"{DATASET_FILES[family].name}.records[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{location} must be an object")
            continue
        value = record.get(key)
        if not isinstance(value, str) or not pattern.fullmatch(value):
            errors.append(f"{location}.{key} has an invalid format")
            continue
        values.append(value)
        indexed[value] = record
    if repeated := duplicates(values):
        errors.append(f"{family} has duplicate {key} values: {', '.join(repeated)}")
    if values != sorted(values):
        errors.append(f"{family} records must be sorted by {key}")
    return indexed


def validate_source_references(
    documents: dict[str, dict[str, Any]], source_ids: set[str], errors: list[str]
) -> None:
    for family, document in documents.items():
        if family == "sources":
            continue
        for index, record in enumerate(records(document)):
            location = f"{DATASET_FILES[family].name}.records[{index}]"
            record_sources = record.get("source_ids") if isinstance(record, dict) else None
            if not isinstance(record_sources, list) or not record_sources:
                errors.append(f"{location}.source_ids must be a non-empty array")
                continue
            if repeated := duplicates(record_sources):
                errors.append(f"{location}.source_ids has duplicates: {', '.join(repeated)}")
            for source_id in record_sources:
                if source_id not in source_ids:
                    errors.append(f"{location} references unknown source {source_id!r}")


def validate_regions(
    regions_by_id: dict[str, dict[str, Any]], errors: list[str]
) -> None:
    for region_id, region in regions_by_id.items():
        location = f"region {region_id!r}"
        if region.get("level") not in REGION_LEVELS:
            errors.append(f"{location} has an invalid level")
        parent = region.get("parent_id")
        if parent is not None and parent not in regions_by_id:
            errors.append(f"{location} references unknown parent {parent!r}")
        seen = {region_id}
        while parent is not None and parent in regions_by_id:
            if parent in seen:
                errors.append(f"{location} has a circular parent reference")
                break
            seen.add(parent)
            parent = regions_by_id[parent].get("parent_id")


def validate_trade_groups(
    groups_by_id: dict[str, dict[str, Any]],
    country_codes: set[str],
    errors: list[str],
) -> dict[str, set[str]]:
    active_country_groups: dict[str, set[str]] = {code: set() for code in country_codes}
    graph: dict[str, set[str]] = {group_id: set() for group_id in groups_by_id}
    for group_id, group in groups_by_id.items():
        location = f"trade group {group_id!r}"
        if group.get("relationship_type") not in TRADE_GROUP_TYPES:
            errors.append(f"{location} has an invalid relationship_type")
        seen: set[tuple[Any, Any]] = set()
        for member in group.get("members", []):
            member_type = member.get("type")
            member_id = member.get("id")
            member_key = (member_type, member_id)
            if member_key in seen:
                errors.append(f"{location} has duplicate member {member_key!r}")
            seen.add(member_key)
            if member.get("status") not in MEMBERSHIP_STATUSES:
                errors.append(f"{location} member {member_id!r} has invalid status")
            if member_type == "country":
                if member_id not in country_codes:
                    errors.append(f"{location} references unknown country {member_id!r}")
                elif member.get("status") in {"member", "party"}:
                    active_country_groups[member_id].add(group_id)
            elif member_type == "trade-group":
                if member_id not in groups_by_id:
                    errors.append(f"{location} references unknown group {member_id!r}")
                else:
                    graph[group_id].add(member_id)
            else:
                errors.append(f"{location} member has invalid type {member_type!r}")

    def visit(node: str, path: set[str]) -> None:
        if node in path:
            errors.append(f"trade group references contain a cycle at {node!r}")
            return
        for child in graph[node]:
            visit(child, path | {node})

    for group_id in graph:
        visit(group_id, set())
    return active_country_groups


def validate_customs_relationships(
    relationships_by_id: dict[str, dict[str, Any]],
    country_codes: set[str],
    groups_by_id: dict[str, dict[str, Any]],
    errors: list[str],
) -> dict[str, set[str]]:
    active_country_relationships: dict[str, set[str]] = {
        code: set() for code in country_codes
    }

    def group_countries(group_id: str, path: set[str]) -> set[str]:
        if group_id in path:
            return set()
        result: set[str] = set()
        for member in groups_by_id[group_id].get("members", []):
            if member.get("status") not in {"member", "party"}:
                continue
            member_type = member.get("type")
            member_id = member.get("id")
            if member_type == "country" and member_id in country_codes:
                result.add(member_id)
            elif member_type == "trade-group" and member_id in groups_by_id:
                result.update(group_countries(member_id, path | {group_id}))
        return result

    for relationship_id, relationship in relationships_by_id.items():
        location = f"customs relationship {relationship_id!r}"
        if relationship.get("relationship_type") not in CUSTOMS_RELATIONSHIP_TYPES:
            errors.append(f"{location} has an invalid relationship_type")
        if relationship.get("status") not in CUSTOMS_RELATIONSHIP_STATUSES:
            errors.append(f"{location} has an invalid status")
        seen: set[tuple[Any, Any]] = set()
        for participant in relationship.get("participants", []):
            participant_type = participant.get("type")
            participant_id = participant.get("id")
            key = (participant_type, participant_id)
            if key in seen:
                errors.append(f"{location} has duplicate participant {key!r}")
            seen.add(key)
            if participant_type == "country" and participant_id not in country_codes:
                errors.append(f"{location} references unknown country {participant_id!r}")
            elif participant_type == "trade-group" and participant_id not in groups_by_id:
                errors.append(f"{location} references unknown group {participant_id!r}")
            elif participant_type not in {"country", "trade-group"}:
                errors.append(f"{location} participant has invalid type")

            if relationship.get("status") != "active":
                continue
            if participant_type == "country" and participant_id in country_codes:
                active_country_relationships[participant_id].add(relationship_id)
            elif participant_type == "trade-group" and participant_id in groups_by_id:
                for country_code in group_countries(participant_id, set()):
                    active_country_relationships[country_code].add(relationship_id)
    return active_country_relationships


def validate_resources(
    family: str,
    resources_by_id: dict[str, dict[str, Any]],
    country_codes: set[str],
    allowed_types: Optional[set[str]],
    type_field: Optional[str],
    errors: list[str],
) -> None:
    websites: list[str] = []
    for resource_id, resource in resources_by_id.items():
        location = f"{family} record {resource_id!r}"
        if resource.get("country_code") not in country_codes:
            errors.append(f"{location} references an unknown country")
        if type_field and resource.get(type_field) not in (allowed_types or set()):
            errors.append(f"{location} has an invalid {type_field}")
        if website := resource.get("website"):
            websites.append(website)
    if repeated := duplicates(websites):
        errors.append(f"{family} has duplicate websites: {', '.join(repeated)}")


def validate_countries(
    countries_by_code: dict[str, dict[str, Any]],
    regions_by_id: dict[str, dict[str, Any]],
    groups_by_id: dict[str, dict[str, Any]],
    active_country_groups: dict[str, set[str]],
    relationships_by_id: dict[str, dict[str, Any]],
    active_country_relationships: dict[str, set[str]],
    resources: dict[str, dict[str, dict[str, Any]]],
    errors: list[str],
) -> None:
    iso3_values: list[str] = []
    numeric_values: list[str] = []
    for iso2, country in countries_by_code.items():
        location = f"country {iso2!r}"
        iso3 = country.get("iso3")
        numeric = country.get("numeric_code")
        if not isinstance(iso3, str) or not ISO3_PATTERN.fullmatch(iso3):
            errors.append(f"{location}.iso3 has an invalid format")
        else:
            iso3_values.append(iso3)
        if not isinstance(numeric, str) or not NUMERIC_PATTERN.fullmatch(numeric):
            errors.append(f"{location}.numeric_code has an invalid format")
        else:
            numeric_values.append(numeric)
        for currency in country.get("currency_codes", []):
            if not isinstance(currency, str) or not CURRENCY_PATTERN.fullmatch(currency):
                errors.append(f"{location} has invalid currency code {currency!r}")
        for field in ("region_id", "subregion_id", "intermediate_region_id"):
            value = country.get(field)
            if value is not None and value not in regions_by_id:
                errors.append(f"{location}.{field} references unknown region {value!r}")
        declared_groups = set(country.get("trade_group_ids", []))
        for group_id in declared_groups:
            if group_id not in groups_by_id:
                errors.append(f"{location} references unknown trade group {group_id!r}")
        if declared_groups != active_country_groups.get(iso2, set()):
            errors.append(f"{location}.trade_group_ids does not match group memberships")
        is_wto_member = "world-trade-organization" in declared_groups
        if country.get("wto_member") is not is_wto_member:
            errors.append(f"{location}.wto_member is inconsistent with WTO membership")
        declared_relationships = set(country.get("customs_relationship_ids", []))
        for relationship_id in declared_relationships:
            if relationship_id not in relationships_by_id:
                errors.append(
                    f"{location} references unknown customs relationship {relationship_id!r}"
                )
        if declared_relationships != active_country_relationships.get(iso2, set()):
            errors.append(
                f"{location}.customs_relationship_ids does not match "
                "active relationship participants"
            )
        scalar_refs = (
            ("customs_authority_id", "customs_authorities"),
            ("standards_body_id", "standards_bodies"),
        )
        array_refs = (
            ("trade_portal_ids", "trade_portals"),
            ("trade_agency_ids", "trade_agencies"),
        )
        for field, family in scalar_refs:
            resource_id = country.get(field)
            if resource_id is not None:
                resource = resources[family].get(resource_id)
                if resource is None:
                    errors.append(f"{location}.{field} references unknown ID {resource_id!r}")
                elif resource.get("country_code") != iso2:
                    errors.append(f"{location}.{field} references another country")
        for field, family in array_refs:
            for resource_id in country.get(field, []):
                resource = resources[family].get(resource_id)
                if resource is None:
                    errors.append(f"{location}.{field} references unknown ID {resource_id!r}")
                elif resource.get("country_code") != iso2:
                    errors.append(f"{location}.{field} references another country")
    if repeated := duplicates(iso3_values):
        errors.append(f"duplicate ISO alpha-3 values: {', '.join(repeated)}")
    if repeated := duplicates(numeric_values):
        errors.append(f"duplicate numeric codes: {', '.join(repeated)}")


def validate_schema_metadata(errors: list[str]) -> None:
    for family, path in SCHEMA_FILES.items():
        schema = load_json(path)
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append(f"{path.name} must declare JSON Schema Draft 2020-12")
        if schema.get("type") != "object":
            errors.append(f"{path.name} root type must be object")
        if not schema.get("$id", "").endswith(path.name):
            errors.append(f"{path.name} has an inconsistent $id")


def main() -> int:
    errors: list[str] = []
    documents = {family: load_json(path) for family, path in DATASET_FILES.items()}
    validate_envelopes(documents, errors)
    validate_common_values(documents, errors)

    sources_by_id = index_records(
        "sources", documents["sources"], "id", ID_PATTERN, errors
    )
    regions_by_id = index_records(
        "regions", documents["regions"], "id", ID_PATTERN, errors
    )
    groups_by_id = index_records(
        "trade_groups", documents["trade_groups"], "id", ID_PATTERN, errors
    )
    relationships_by_id = index_records(
        "customs_relationships",
        documents["customs_relationships"],
        "id",
        ID_PATTERN,
        errors,
    )
    resources_by_family = {
        family: index_records(family, documents[family], "id", ID_PATTERN, errors)
        for family in (
            "customs_authorities",
            "trade_portals",
            "trade_agencies",
            "standards_bodies",
        )
    }
    countries_by_code = index_records(
        "countries", documents["countries"], "iso2", ISO2_PATTERN, errors
    )
    country_codes = set(countries_by_code)

    validate_source_references(documents, set(sources_by_id), errors)
    validate_regions(regions_by_id, errors)
    active_country_groups = validate_trade_groups(
        groups_by_id, country_codes, errors
    )
    active_country_relationships = validate_customs_relationships(
        relationships_by_id, country_codes, groups_by_id, errors
    )
    validate_resources(
        "customs_authorities",
        resources_by_family["customs_authorities"],
        country_codes,
        AUTHORITY_TYPES,
        "authority_type",
        errors,
    )
    validate_resources(
        "trade_portals",
        resources_by_family["trade_portals"],
        country_codes,
        PORTAL_TYPES,
        "portal_type",
        errors,
    )
    validate_resources(
        "trade_agencies",
        resources_by_family["trade_agencies"],
        country_codes,
        AGENCY_TYPES,
        "agency_type",
        errors,
    )
    validate_resources(
        "standards_bodies",
        resources_by_family["standards_bodies"],
        country_codes,
        None,
        None,
        errors,
    )
    validate_countries(
        countries_by_code,
        regions_by_id,
        groups_by_id,
        active_country_groups,
        relationships_by_id,
        active_country_relationships,
        resources_by_family,
        errors,
    )
    validate_schema_metadata(errors)

    expected_csv = render_countries_csv(documents["countries"])
    if not COUNTRIES_CSV.exists():
        errors.append("missing generated export: countries.csv")
    elif COUNTRIES_CSV.read_text(encoding="utf-8") != expected_csv:
        errors.append("generated export is outdated: countries.csv; run build_csv.py")

    if errors:
        print(f"Validation failed with {len(errors)} error(s):", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "Validated "
        f"{len(countries_by_code)} countries/areas, "
        f"{len(groups_by_id)} trade groups, "
        f"{len(relationships_by_id)} customs relationships, and "
        f"{len(sources_by_id)} source records; all references and exports resolve."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
