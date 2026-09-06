#!/usr/bin/env python3
"""Validate every canonical JSON dataset against JSON Schema Draft 2020-12."""

from __future__ import annotations

import sys

try:
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource
except ImportError:
    print(
        "Development dependencies are missing. "
        "Run: python3 -m pip install -r requirements-dev.txt",
        file=sys.stderr,
    )
    raise SystemExit(2)

from dataset_tools import DATASET_FILES, SCHEMA_DIR, SCHEMA_FILES, load_json


def main() -> int:
    schema_paths = sorted(SCHEMA_DIR.glob("*.schema.json"))
    schemas = {path: load_json(path) for path in schema_paths}
    registry = Registry()
    for schema in schemas.values():
        Draft202012Validator.check_schema(schema)
        registry = registry.with_resource(
            schema["$id"], Resource.from_contents(schema)
        )

    errors: list[str] = []
    for family, data_path in DATASET_FILES.items():
        schema = schemas[SCHEMA_FILES[family]]
        validator = Draft202012Validator(schema, registry=registry)
        schema_errors = sorted(
            validator.iter_errors(load_json(data_path)),
            key=lambda error: list(error.absolute_path),
        )
        for error in schema_errors:
            location = ".".join(str(part) for part in error.absolute_path) or "root"
            errors.append(f"{data_path.name}:{location}: {error.message}")

    if errors:
        print("JSON Schema validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(DATASET_FILES)} datasets against Draft 2020-12 schemas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
