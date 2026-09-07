from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_schemas  # noqa: E402


class ValidateSchemasTests(unittest.TestCase):
    def test_main_accepts_repository_datasets(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = validate_schemas.main()
        self.assertEqual(result, 0)
        self.assertIn("Validated 9 datasets", output.getvalue())

    def test_main_reports_schema_errors(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            schema_path = root / "sample.schema.json"
            data_path = root / "sample.json"
            schema = {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "$id": "https://example.test/sample.schema.json",
                "type": "object",
                "required": ["name"],
                "properties": {"name": {"type": "string"}},
            }
            schema_path.write_text(json.dumps(schema), encoding="utf-8")
            data_path.write_text(json.dumps({"name": 42}), encoding="utf-8")
            error = io.StringIO()
            with patch.object(validate_schemas, "SCHEMA_DIR", root), patch.object(
                validate_schemas, "DATASET_FILES", {"sample": data_path}
            ), patch.object(
                validate_schemas, "SCHEMA_FILES", {"sample": schema_path}
            ), contextlib.redirect_stderr(error):
                result = validate_schemas.main()

        self.assertEqual(result, 1)
        self.assertIn("JSON Schema validation failed", error.getvalue())
        self.assertIn("sample.json:name", error.getvalue())
