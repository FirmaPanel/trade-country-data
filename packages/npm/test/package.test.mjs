import assert from "node:assert/strict";
import { createRequire } from "node:module";
import test from "node:test";

import datasets, {
  countries,
  customsAuthorities,
  customsRelationships,
  officialTradePortals,
  regions,
  sources,
  standardsBodies,
  tradeAgencies,
  tradeGroups,
} from "../index.js";

const require = createRequire(import.meta.url);
const commonJs = require("../index.cjs");

const namedDatasets = {
  countries,
  customsAuthorities,
  customsRelationships,
  officialTradePortals,
  regions,
  sources,
  standardsBodies,
  tradeAgencies,
  tradeGroups,
};

test("all ESM datasets have valid envelopes", () => {
  assert.deepEqual(datasets, namedDatasets);

  for (const document of Object.values(datasets)) {
    assert.match(document.schema_version, /^\d+\.\d+\.\d+$/);
    assert.equal(document.record_count, document.records.length);
    assert.ok(document.records.length > 0);
  }
});

test("CommonJS exposes the same datasets", () => {
  assert.equal(commonJs.countries.record_count, countries.record_count);
  assert.equal(commonJs.default, commonJs);
});

test("the declared dataset version matches every dataset", async () => {
  const packageJson = require("../package.json");

  for (const document of Object.values(datasets)) {
    assert.equal(document.schema_version, packageJson.datasetVersion);
  }

  const versionCheck = await import("../scripts/check-version.mjs");
  assert.ok(versionCheck);
});
