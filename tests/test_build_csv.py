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

import build_csv  # noqa: E402
import dataset_tools  # noqa: E402


class BuildCsvTests(unittest.TestCase):
    def setUp(self) -> None:
        record = {field: None for field in dataset_tools.CSV_FIELDS}
        record["iso2"] = "TR"
        self.document = {"records": [record]}
        self.expected = dataset_tools.render_countries_csv(self.document)

    def run_main(self, csv_path: Path, check: bool) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        argv = ["build_csv.py"] + (["--check"] if check else [])
        with patch.object(build_csv, "COUNTRIES_CSV", csv_path), patch.object(
            build_csv, "load_json", return_value=self.document
        ), patch.object(sys, "argv", argv), contextlib.redirect_stdout(
            stdout
        ), contextlib.redirect_stderr(stderr):
            result = build_csv.main()
        return result, stdout.getvalue(), stderr.getvalue()

    def test_check_reports_missing_export(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result, _, error = self.run_main(Path(directory) / "countries.csv", True)
        self.assertEqual(result, 1)
        self.assertIn("Missing generated export", error)

    def test_check_reports_outdated_export(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "countries.csv"
            path.write_text("stale", encoding="utf-8")
            result, _, error = self.run_main(path, True)
        self.assertEqual(result, 1)
        self.assertIn("Outdated generated export", error)

    def test_check_accepts_current_export(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "countries.csv"
            path.write_text(self.expected, encoding="utf-8")
            result, output, _ = self.run_main(path, True)
        self.assertEqual(result, 0)
        self.assertIn("up to date", output)

    def test_build_writes_changed_export(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            path = Path(directory) / "countries.csv"
            with patch.object(build_csv, "ROOT", Path(directory)):
                result, output, _ = self.run_main(path, False)
            self.assertEqual(path.read_text(encoding="utf-8"), self.expected)
        self.assertEqual(result, 0)
        self.assertIn("Updated", output)

    def test_build_leaves_current_export_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "countries.csv"
            path.write_text(self.expected, encoding="utf-8")
            result, output, _ = self.run_main(path, False)
        self.assertEqual(result, 0)
        self.assertIn("already up to date", output)
