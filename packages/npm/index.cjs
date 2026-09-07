"use strict";

const countries = require("./generated/data/countries.json");
const customsAuthorities = require(
  "./generated/data/customs-authorities.json",
);
const customsRelationships = require(
  "./generated/data/customs-relationships.json",
);
const officialTradePortals = require(
  "./generated/data/official-trade-portals.json",
);
const regions = require("./generated/data/regions.json");
const sources = require("./generated/data/sources.json");
const standardsBodies = require("./generated/data/standards-bodies.json");
const tradeAgencies = require("./generated/data/trade-agencies.json");
const tradeGroups = require("./generated/data/trade-groups.json");

const datasets = {
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

Object.defineProperty(datasets, "default", { value: datasets });
module.exports = Object.freeze(datasets);
