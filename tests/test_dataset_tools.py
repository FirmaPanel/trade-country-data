from __future__ import annotations

import csv
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import dataset_tools  # noqa: E402


class DatasetToolsTests(unittest.TestCase):
    def test_load_json_reads_utf8_document(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            root = Path(directory)
            path = root / "example.json"
            path.write_text(json.dumps({"name": "Türkiye"}), encoding="utf-8")
            with patch.object(dataset_tools, "ROOT", root):
                self.assertEqual(dataset_tools.load_json(path), {"name": "Türkiye"})

    def test_load_json_wraps_decode_error_with_repository_path(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            root = Path(directory)
            path = root / "broken.json"
            path.write_text("{broken", encoding="utf-8")
            with patch.object(dataset_tools, "ROOT", root):
                with self.assertRaisesRegex(ValueError, r"Invalid JSON in broken.json"):
                    dataset_tools.load_json(path)

    def test_records_returns_envelope_records(self) -> None:
        rows = [{"id": "one"}]
        self.assertIs(dataset_tools.records({"records": rows}), rows)

    def test_render_countries_csv_flattens_supported_values(self) -> None:
        record = {field: None for field in dataset_tools.CSV_FIELDS}
        record.update(
            {
                "iso2": "TR",
                "name": "Türkiye, Republic of",
                "currency_codes": ["TRY", "USD"],
                "wto_member": True,
                "landlocked": False,
                "aliases": [],
            }
        )
        rendered = dataset_tools.render_countries_csv({"records": [record]})
        row = next(csv.DictReader(io.StringIO(rendered)))

        self.assertEqual(row["name"], "Türkiye, Republic of")
        self.assertEqual(row["currency_codes"], "TRY|USD")
        self.assertEqual(row["wto_member"], "true")
        self.assertEqual(row["landlocked"], "false")
        self.assertEqual(row["aliases"], "")
        self.assertEqual(row["official_name"], "")
        self.assertTrue(rendered.endswith("\n"))
