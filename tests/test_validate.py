from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate  # noqa: E402


class BasicValidatorTests(unittest.TestCase):
    def test_duplicates_dates_and_walk(self) -> None:
        self.assertEqual(validate.duplicates(["b", "a", "b", "a", "c"]), ["a", "b"])
        self.assertTrue(validate.valid_date("2026-09-07"))
        self.assertFalse(validate.valid_date("2026-02-30"))
        self.assertFalse(validate.valid_date(20260907))
        walked = list(validate.walk({"outer": [{"inner": 1}]}))
        self.assertIn(("root.outer[0].inner", "inner", 1), walked)

    def test_validate_envelopes_reports_all_metadata_failures(self) -> None:
        documents = {
            "countries": [],
            "regions": {
                "schema_version": "bad",
                "as_of_date": "bad",
                "record_count": 2,
                "records": {},
                "extra": True,
            },
            "sources": {
                "schema_version": "1.0.0",
                "as_of_date": "2026-09-07",
                "record_count": 2,
                "records": [],
            },
            "trade_groups": {
                "schema_version": "2.0.0",
                "as_of_date": "2026-09-08",
                "record_count": 0,
                "records": [],
            },
        }
        errors: list[str] = []
        validate.validate_envelopes(documents, errors)
        joined = "\n".join(errors)
        self.assertIn("must contain an object", joined)
        self.assertIn("envelope must contain only", joined)
        self.assertIn("schema_version must be", joined)
        self.assertIn("as_of_date must be", joined)
        self.assertIn("records must be an array", joined)
        self.assertIn("record_count does not match", joined)
        self.assertIn("same schema_version", joined)
        self.assertIn("same as_of_date", joined)

    def test_validate_common_values_rejects_volatile_invalid_date_and_url(self) -> None:
        documents = {
            "countries": {
                "records": [
                    {
                        "tariff_rate": 2,
                        "effective_to": "tomorrow",
                        "website": "http://example.test",
                        "url": 42,
                        "license_url": None,
                    }
                ]
            }
        }
        errors: list[str] = []
        validate.validate_common_values(documents, errors)
        self.assertEqual(len(errors), 4)
        self.assertTrue(any("forbidden volatile" in error for error in errors))
        self.assertTrue(any("ISO 8601" in error for error in errors))
        self.assertEqual(sum("absolute HTTPS" in error for error in errors), 2)

    def test_index_records_reports_invalid_duplicate_and_sort_order(self) -> None:
        document = {
            "records": [
                {"id": "b"},
                {"id": "a"},
                {"id": "a"},
                {"id": "INVALID"},
                "not-an-object",
            ]
        }
        errors: list[str] = []
        indexed = validate.index_records(
            "sources", document, "id", validate.ID_PATTERN, errors
        )
        self.assertEqual(set(indexed), {"a", "b"})
        self.assertTrue(any("must be an object" in error for error in errors))
        self.assertTrue(any("invalid format" in error for error in errors))
        self.assertTrue(any("duplicate id" in error for error in errors))
        self.assertTrue(any("must be sorted" in error for error in errors))

    def test_source_references_report_missing_duplicate_and_unknown(self) -> None:
        documents = {
            "sources": {"records": [{"id": "source"}]},
            "countries": {
                "records": [
                    {"source_ids": []},
                    {"source_ids": ["source", "source", "missing"]},
                    "not-an-object",
                ]
            },
        }
        errors: list[str] = []
        validate.validate_source_references(documents, {"source"}, errors)
        self.assertEqual(sum("non-empty array" in error for error in errors), 2)
        self.assertTrue(any("has duplicates" in error for error in errors))
        self.assertTrue(any("unknown source" in error for error in errors))

    def test_validate_regions_reports_level_parent_and_cycle_errors(self) -> None:
        regions = {
            "a": {"level": "invalid", "parent_id": "missing"},
            "b": {"level": "region", "parent_id": "c"},
            "c": {"level": "subregion", "parent_id": "b"},
        }
        errors: list[str] = []
        validate.validate_regions(regions, errors)
        self.assertTrue(any("invalid level" in error for error in errors))
        self.assertTrue(any("unknown parent" in error for error in errors))
        self.assertEqual(sum("circular parent" in error for error in errors), 2)


class RelationshipValidatorTests(unittest.TestCase):
    def test_validate_trade_groups_builds_active_index_and_reports_errors(self) -> None:
        groups = {
            "a": {
                "relationship_type": "invalid",
                "members": [
                    {"type": "country", "id": "TR", "status": "member"},
                    {"type": "country", "id": "TR", "status": "member"},
                    {"type": "country", "id": "XX", "status": "unknown"},
                    {"type": "trade-group", "id": "b", "status": "party"},
                    {"type": "trade-group", "id": "missing", "status": "party"},
                    {"type": "organization", "id": "x", "status": "party"},
                ],
            },
            "b": {
                "relationship_type": "customs-union",
                "members": [
                    {"type": "trade-group", "id": "a", "status": "signatory"},
                    {"type": "country", "id": "US", "status": "suspended"},
                ],
            },
        }
        errors: list[str] = []
        active = validate.validate_trade_groups(groups, {"TR", "US"}, errors)
        self.assertEqual(active, {"TR": {"a"}, "US": set()})
        joined = "\n".join(errors)
        for fragment in (
            "invalid relationship_type",
            "duplicate member",
            "invalid status",
            "unknown country",
            "unknown group",
            "invalid type",
            "contain a cycle",
        ):
            self.assertIn(fragment, joined)

    def test_validate_customs_relationships_expands_nested_active_groups(self) -> None:
        groups = {
            "parent": {
                "members": [
                    {"type": "trade-group", "id": "child", "status": "member"},
                    {"type": "country", "id": "US", "status": "signatory"},
                ]
            },
            "child": {
                "members": [
                    {"type": "country", "id": "TR", "status": "party"},
                    {"type": "trade-group", "id": "parent", "status": "member"},
                ]
            },
        }
        relationships = {
            "active": {
                "relationship_type": "customs-union",
                "status": "active",
                "participants": [
                    {"type": "trade-group", "id": "parent"},
                    {"type": "country", "id": "US"},
                ],
            },
            "bad": {
                "relationship_type": "invalid",
                "status": "invalid",
                "participants": [
                    {"type": "country", "id": "XX"},
                    {"type": "country", "id": "XX"},
                    {"type": "trade-group", "id": "missing"},
                    {"type": "organization", "id": "x"},
                ],
            },
        }
        errors: list[str] = []
        active = validate.validate_customs_relationships(
            relationships, {"TR", "US"}, groups, errors
        )
        self.assertEqual(active["TR"], {"active"})
        self.assertEqual(active["US"], {"active"})
        joined = "\n".join(errors)
        for fragment in (
            "invalid relationship_type",
            "invalid status",
            "duplicate participant",
            "unknown country",
            "unknown group",
            "participant has invalid type",
        ):
            self.assertIn(fragment, joined)

    def test_resources_report_country_type_and_duplicate_website(self) -> None:
        resources = {
            "one": {
                "country_code": "XX",
                "portal_type": "bad",
                "website": "https://example.test",
            },
            "two": {
                "country_code": "TR",
                "portal_type": "customs",
                "website": "https://example.test",
            },
        }
        errors: list[str] = []
        validate.validate_resources(
            "trade_portals",
            resources,
            {"TR"},
            validate.PORTAL_TYPES,
            "portal_type",
            errors,
        )
        self.assertEqual(len(errors), 3)
        self.assertTrue(any("unknown country" in error for error in errors))
        self.assertTrue(any("invalid portal_type" in error for error in errors))
        self.assertTrue(any("duplicate websites" in error for error in errors))

    def test_resources_accept_sorted_shared_country_scope(self) -> None:
        resources = {
            "shared": {
                "country_codes": ["LI", "NO"],
                "portal_type": "trade-information",
                "website": "https://example.test/shared",
            }
        }
        errors: list[str] = []
        validate.validate_resources(
            "trade_portals",
            resources,
            {"LI", "NO"},
            validate.PORTAL_TYPES,
            "portal_type",
            errors,
        )
        self.assertEqual(errors, [])
        self.assertEqual(validate.resource_country_codes(resources["shared"]), {"LI", "NO"})

    def test_resources_reject_unsorted_or_partly_unknown_shared_scope(self) -> None:
        resources = {
            "shared": {
                "country_codes": ["XX", "LI"],
                "portal_type": "trade-information",
            }
        }
        errors: list[str] = []
        validate.validate_resources(
            "trade_portals",
            resources,
            {"LI"},
            validate.PORTAL_TYPES,
            "portal_type",
            errors,
        )
        self.assertTrue(any("unknown country" in error for error in errors))
        self.assertTrue(any("must be sorted" in error for error in errors))


class CountryValidatorTests(unittest.TestCase):
    def base_resources(self) -> dict[str, dict[str, dict[str, str]]]:
        return {
            "customs_authorities": {"auth-tr": {"country_code": "TR"}},
            "standards_bodies": {"std-tr": {"country_code": "TR"}},
            "trade_portals": {"portal-tr": {"country_code": "TR"}},
            "trade_agencies": {"agency-tr": {"country_code": "TR"}},
        }

    def test_validate_countries_accepts_consistent_country(self) -> None:
        country = {
            "iso3": "TUR",
            "numeric_code": "792",
            "currency_codes": ["TRY"],
            "region_id": "asia",
            "subregion_id": None,
            "intermediate_region_id": None,
            "trade_group_ids": ["world-trade-organization"],
            "wto_member": True,
            "customs_relationship_ids": ["relationship"],
            "customs_authority_id": "auth-tr",
            "standards_body_id": "std-tr",
            "trade_portal_ids": ["portal-tr"],
            "trade_agency_ids": ["agency-tr"],
        }
        errors: list[str] = []
        validate.validate_countries(
            {"TR": country},
            {"asia": {}},
            {"world-trade-organization": {}},
            {"TR": {"world-trade-organization"}},
            {"relationship": {}},
            {"TR": {"relationship"}},
            self.base_resources(),
            errors,
        )
        self.assertEqual(errors, [])

    def test_validate_countries_accepts_shared_resources(self) -> None:
        country_li = {
            "iso3": "LIE",
            "numeric_code": "438",
            "currency_codes": ["CHF"],
            "region_id": None,
            "subregion_id": None,
            "intermediate_region_id": None,
            "trade_group_ids": [],
            "wto_member": False,
            "customs_relationship_ids": [],
            "customs_authority_id": "shared-auth",
            "standards_body_id": "shared-standards",
            "trade_portal_ids": ["shared-portal"],
            "trade_agency_ids": ["shared-agency"],
        }
        country_ch = country_li | {
            "iso3": "CHE",
            "numeric_code": "756",
        }
        shared = {"country_codes": ["CH", "LI"]}
        resources = {
            "customs_authorities": {"shared-auth": shared},
            "standards_bodies": {"shared-standards": shared},
            "trade_portals": {"shared-portal": shared},
            "trade_agencies": {"shared-agency": shared},
        }
        errors: list[str] = []
        validate.validate_countries(
            {"CH": country_ch, "LI": country_li},
            {},
            {},
            {"CH": set(), "LI": set()},
            {},
            {"CH": set(), "LI": set()},
            resources,
            errors,
        )
        self.assertEqual(errors, [])

        country_ch = country_ch | {"trade_portal_ids": []}
        validate.validate_countries(
            {"CH": country_ch, "LI": country_li},
            {},
            {},
            {"CH": set(), "LI": set()},
            {},
            {"CH": set(), "LI": set()},
            resources,
            errors,
        )
        self.assertTrue(
            any(
                "trade_portals resource 'shared-portal' is not linked from countries: CH"
                in error
                for error in errors
            )
        )

    def test_countries_report_formats_references_and_orphans(self) -> None:
        countries = {
            "TR": {
                "iso3": "BAD!",
                "numeric_code": "7",
                "currency_codes": ["try", 1],
                "region_id": "missing",
                "subregion_id": None,
                "intermediate_region_id": None,
                "trade_group_ids": ["missing-group"],
                "wto_member": True,
                "customs_relationship_ids": ["missing-relationship"],
                "customs_authority_id": "missing-auth",
                "standards_body_id": "std-us",
                "trade_portal_ids": ["missing-portal", "portal-us"],
                "trade_agency_ids": ["missing-agency", "agency-us"],
            },
            "US": {
                "iso3": "USA",
                "numeric_code": "840",
                "currency_codes": ["USD"],
                "region_id": None,
                "subregion_id": None,
                "intermediate_region_id": None,
                "trade_group_ids": [],
                "wto_member": False,
                "customs_relationship_ids": [],
                "customs_authority_id": None,
                "standards_body_id": None,
                "trade_portal_ids": [],
                "trade_agency_ids": [],
            },
            "CA": {
                "iso3": "USA",
                "numeric_code": "840",
                "currency_codes": [],
                "region_id": None,
                "subregion_id": None,
                "intermediate_region_id": None,
                "trade_group_ids": [],
                "wto_member": False,
                "customs_relationship_ids": [],
                "customs_authority_id": None,
                "standards_body_id": None,
                "trade_portal_ids": [],
                "trade_agency_ids": [],
            },
        }
        resources = {
            "customs_authorities": {"orphan-auth": {"country_code": "US"}},
            "standards_bodies": {"std-us": {"country_code": "US"}},
            "trade_portals": {"portal-us": {"country_code": "US"}},
            "trade_agencies": {"agency-us": {"country_code": "US"}},
        }
        errors: list[str] = []
        validate.validate_countries(
            countries,
            {},
            {},
            {"TR": set(), "US": set(), "CA": set()},
            {},
            {"TR": set(), "US": set(), "CA": set()},
            resources,
            errors,
        )
        joined = "\n".join(errors)
        for fragment in (
            "iso3 has an invalid format",
            "numeric_code has an invalid format",
            "invalid currency code",
            "references unknown region",
            "unknown trade group",
            "trade_group_ids does not match",
            "wto_member is inconsistent",
            "unknown customs relationship",
            "customs_relationship_ids does not match",
            "references unknown ID",
            "does not serve this country",
            "duplicate ISO alpha-3",
            "duplicate numeric codes",
            "resources not linked",
        ):
            self.assertIn(fragment, joined)


class MainValidatorTests(unittest.TestCase):
    def test_validate_schema_metadata_reports_each_contract_problem(self) -> None:
        fake_paths = {
            "one": Path("one.schema.json"),
            "two": Path("two.schema.json"),
        }
        schemas = {
            "one.schema.json": {"$schema": "old", "type": "array", "$id": "wrong"},
            "two.schema.json": {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "type": "object",
                "$id": "https://example.test/two.schema.json",
            },
        }
        errors: list[str] = []
        with patch.object(validate, "SCHEMA_FILES", fake_paths), patch.object(
            validate, "load_json", side_effect=lambda path: schemas[path.name]
        ):
            validate.validate_schema_metadata(errors)
        self.assertEqual(len(errors), 3)

    def test_main_accepts_current_repository(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = validate.main()
        self.assertEqual(result, 0)
        self.assertIn("Validated 249 countries", output.getvalue())

    def test_main_reports_missing_and_outdated_csv(self) -> None:
        error = io.StringIO()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "countries.csv"
            with patch.object(
                validate, "COUNTRIES_CSV", path
            ), contextlib.redirect_stderr(error):
                missing_result = validate.main()
            path.write_text("stale", encoding="utf-8")
            with patch.object(
                validate, "COUNTRIES_CSV", path
            ), contextlib.redirect_stderr(error):
                stale_result = validate.main()

        self.assertEqual((missing_result, stale_result), (1, 1))
        self.assertIn("missing generated export", error.getvalue())
        self.assertIn("generated export is outdated", error.getvalue())
