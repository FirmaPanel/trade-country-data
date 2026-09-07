from __future__ import annotations

import contextlib
import io
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import report_coverage  # noqa: E402


def envelope(rows: list[dict[str, object]]) -> dict[str, object]:
    return {"records": rows}


class ReportCoverageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.documents = {
            "countries": envelope(
                [
                    {
                        "source_ids": ["un-m49"],
                        "region_id": "asia",
                        "currency_codes": ["TRY"],
                        "wto_member": True,
                        "customs_authority_id": "authority",
                        "trade_portal_ids": ["portal"],
                        "trade_agency_ids": ["agency"],
                        "standards_body_id": "standards",
                    },
                    {
                        "source_ids": [],
                        "region_id": None,
                        "currency_codes": [],
                        "wto_member": False,
                        "customs_authority_id": None,
                        "trade_portal_ids": [],
                        "trade_agency_ids": [],
                        "standards_body_id": None,
                    },
                ]
            ),
            "trade_groups": envelope([{"id": "group"}]),
            "customs_relationships": envelope([{"id": "relationship"}]),
        }

    def test_calculate_and_render_coverage(self) -> None:
        metrics = report_coverage.calculate_coverage(self.documents)
        rendered = report_coverage.render_markdown(metrics)

        self.assertEqual(metrics[report_coverage.METRIC_ORDER[0]], 2)
        self.assertTrue(all(value == 1 for value in list(metrics.values())[1:]))
        self.assertIn("| Dataset area | Coverage |", rendered)
        self.assertIn("| Countries with a verified trade agency | 1 |", rendered)

    def test_compare_readme_reports_missing_and_stale_rows(self) -> None:
        metrics = report_coverage.calculate_coverage(self.documents)
        readme = report_coverage.render_markdown(metrics).replace(
            "| Customs relationships | 1 |", "| Customs relationships | 9 |"
        )
        readme = readme.replace("| Trade groups and agreements | 1 |\n", "")

        errors = report_coverage.compare_readme(metrics, readme)

        self.assertEqual(len(errors), 2)
        self.assertTrue(any("row is missing" in error for error in errors))
        self.assertTrue(any("expected 1" in error for error in errors))

    def test_main_prints_table(self) -> None:
        output = io.StringIO()
        with patch.object(
            report_coverage, "load_coverage_documents", return_value=self.documents
        ), contextlib.redirect_stdout(output):
            result = report_coverage.main([])

        self.assertEqual(result, 0)
        self.assertIn("ISO 3166-1 country and area records | 2", output.getvalue())

    def test_main_check_succeeds_for_current_repository(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = report_coverage.main(["--check"])

        self.assertEqual(result, 0)
        self.assertIn("11 calculated metrics", output.getvalue())

    def test_main_check_prints_mismatches(self) -> None:
        error = io.StringIO()
        with patch.object(
            report_coverage, "load_coverage_documents", return_value=self.documents
        ), patch.object(
            report_coverage, "README"
        ) as readme, contextlib.redirect_stderr(error):
            readme.read_text.return_value = "# No table"
            result = report_coverage.main(["--check"])

        self.assertEqual(result, 1)
        self.assertIn("Coverage check failed with 11 error(s)", error.getvalue())

    def test_load_coverage_documents_loads_only_required_families(self) -> None:
        documents = report_coverage.load_coverage_documents()
        self.assertEqual(
            set(documents), {"countries", "trade_groups", "customs_relationships"}
        )
