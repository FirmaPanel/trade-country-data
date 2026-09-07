# FirmaPanel Trade Country Data

The official Python distribution of
[FirmaPanel Trade Country Data](https://github.com/FirmaPanel/trade-country-data),
a trade-focused country reference dataset for procurement, logistics, customs,
sourcing, and import-export software.

Explore FirmaPanel's free procurement and import-export tools at
[firmapanel.com/tools](https://firmapanel.com/tools).

## Install

```bash
python -m pip install firmapanel-trade-country-data
```

The package supports Python 3.9 or later and has no runtime dependencies.

## Usage

Load one of the nine canonical datasets:

```python
from firmapanel_trade_country_data import load_dataset

countries = load_dataset("countries")
turkiye = next(record for record in countries["records"] if record["iso2"] == "TR")

print(turkiye["trade_group_ids"])
print(turkiye["customs_relationship_ids"])
```

Available dataset names are exposed through `DATASET_NAMES`. JSON Schemas can be
loaded using `load_schema()`, and `read_countries_csv()` returns the generated
country CSV as text.

```python
from firmapanel_trade_country_data import (
    DATASET_NAMES,
    DATASET_VERSION,
    load_schema,
    read_countries_csv,
)

print(DATASET_NAMES)
print(DATASET_VERSION)
country_schema = load_schema("country")
csv_text = read_countries_csv()
```

`dataset_file()` and `schema_file()` return `importlib.resources` Traversable
objects for consumers that need direct resource access.

## Versioning and license

Package `0.3.0` contains dataset snapshot `0.3.0`. Package versions may advance
independently for packaging-only changes; `DATASET_VERSION` always identifies
the bundled canonical snapshot.

The dataset is licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Retain attribution
when reusing it. See the repository's
[attribution guidance](https://github.com/FirmaPanel/trade-country-data/blob/main/ATTRIBUTION.md)
and [source registry](https://github.com/FirmaPanel/trade-country-data/blob/main/data/sources.json).
