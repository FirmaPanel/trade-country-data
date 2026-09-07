import { createRequire } from "node:module";

const require = createRequire(import.meta.url);

export const countries = require("./generated/data/countries.json");
export const customsAuthorities = require(
  "./generated/data/customs-authorities.json",
);
export const customsRelationships = require(
  "./generated/data/customs-relationships.json",
);
export const officialTradePortals = require(
  "./generated/data/official-trade-portals.json",
);
export const regions = require("./generated/data/regions.json");
export const sources = require("./generated/data/sources.json");
export const standardsBodies = require(
  "./generated/data/standards-bodies.json",
);
export const tradeAgencies = require("./generated/data/trade-agencies.json");
export const tradeGroups = require("./generated/data/trade-groups.json");

const datasets = Object.freeze({
  countries,
  customsAuthorities,
  customsRelationships,
  officialTradePortals,
  regions,
  sources,
  standardsBodies,
  tradeAgencies,
  tradeGroups,
});

export default datasets;
