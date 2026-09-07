from __future__ import annotations

import unittest

import firmapanel_trade_country_data as trade_data


class PackageTests(unittest.TestCase):
    def test_all_datasets_have_valid_envelopes(self) -> None:
        self.assertEqual(len(trade_data.DATASET_NAMES), 9)

        for name in trade_data.DATASET_NAMES:
            with self.subTest(name=name):
                document = trade_data.load_dataset(name)
                self.assertEqual(document["schema_version"], trade_data.DATASET_VERSION)
                self.assertEqual(document["record_count"], len(document["records"]))
                self.assertGreater(document["record_count"], 0)

    def test_schema_and_csv_resources_are_available(self) -> None:
        country_schema = trade_data.load_schema("country")
        self.assertEqual(country_schema["type"], "object")
        self.assertTrue(trade_data.read_countries_csv().startswith("iso2,iso3,"))

    def test_unknown_resource_names_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unknown data name"):
            trade_data.load_dataset("missing")

        with self.assertRaisesRegex(ValueError, "Unknown schema name"):
            trade_data.load_schema("missing")

    def test_versions_are_exposed(self) -> None:
        self.assertEqual(trade_data.__version__, "0.3.0")
        self.assertEqual(trade_data.DATASET_VERSION, "0.3.0")


if __name__ == "__main__":
    unittest.main()
