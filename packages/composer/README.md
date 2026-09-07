# firmapanel/trade-country-data

The official Composer distribution of
[FirmaPanel Trade Country Data](https://github.com/FirmaPanel/trade-country-data),
a trade-focused country reference dataset for procurement, logistics, customs,
sourcing, and import-export software.

Explore FirmaPanel's free procurement and import-export tools at
[firmapanel.com/tools](https://firmapanel.com/tools).

## Install

```bash
composer require firmapanel/trade-country-data
```

The package supports PHP 8.1 or later and has no third-party runtime
dependencies.

## Usage

```php
<?php

use FirmaPanel\TradeCountryData\TradeCountryData;

require __DIR__ . '/vendor/autoload.php';

$countries = TradeCountryData::loadDataset('countries');
$turkiye = array_values(array_filter(
    $countries['records'],
    static fn (array $record): bool => $record['iso2'] === 'TR',
))[0];

print_r($turkiye['trade_group_ids']);
print_r($turkiye['customs_relationship_ids']);
```

Use `datasetNames()` to list all nine datasets. JSON Schemas are available
through `loadSchema()` and `schemaNames()`, while `readCountriesCsv()` returns
the generated country CSV. The corresponding canonical file paths are exposed
by `datasetPath()` and `schemaPath()`.

## Versioning and license

Composer versions come from repository tags. `TradeCountryData::DATASET_VERSION`
identifies the bundled canonical snapshot, allowing package-only patch releases
without changing the data schema.

The dataset is licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Retain attribution
when reusing it. See the repository's
[attribution guidance](https://github.com/FirmaPanel/trade-country-data/blob/main/ATTRIBUTION.md)
and [source registry](https://github.com/FirmaPanel/trade-country-data/blob/main/data/sources.json).
