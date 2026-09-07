# @firmapanel/trade-country-data

Trade-focused country reference data for procurement, logistics, customs,
sourcing, and import-export software. This is the official npm distribution of
the [FirmaPanel Trade Country Data](https://github.com/FirmaPanel/trade-country-data)
snapshot.

Explore FirmaPanel's free procurement and import-export tools at
[firmapanel.com/tools](https://firmapanel.com/tools).

## Install

```bash
npm install @firmapanel/trade-country-data
```

The package has no runtime dependencies and supports Node.js 18 or later.

## JavaScript API

Named exports work in ESM and CommonJS:

```js
import { countries, tradeGroups } from "@firmapanel/trade-country-data";

const turkiye = countries.records.find((country) => country.iso2 === "TR");
console.log(turkiye.trade_group_ids);
console.log(tradeGroups.as_of_date);
```

```js
const { countries } = require("@firmapanel/trade-country-data");
```

The package exports `countries`, `customsAuthorities`, `customsRelationships`,
`officialTradePortals`, `regions`, `sources`, `standardsBodies`, `tradeAgencies`,
and `tradeGroups`. The default export is an object containing all nine datasets.
TypeScript declarations are included.

## Raw files

Canonical files are available through explicit package subpaths:

```js
const countries = require("@firmapanel/trade-country-data/data/countries.json");
```

All JSON datasets use `@firmapanel/trade-country-data/data/<file>.json`. The CSV
export is available as `@firmapanel/trade-country-data/countries.csv`, and JSON
Schemas use `@firmapanel/trade-country-data/schema/<file>.json`.

## Versioning and license

Package version `0.3.1` contains dataset snapshot `0.3.0`. The npm distribution
can receive packaging-only patch releases without changing the canonical
dataset's `schema_version`. Pin an exact package version when reproducibility is
important.

The dataset is licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Retain attribution
when reusing it. See the repository's
[attribution guidance](https://github.com/FirmaPanel/trade-country-data/blob/main/ATTRIBUTION.md)
and [source registry](https://github.com/FirmaPanel/trade-country-data/blob/main/data/sources.json).
