export type DateString = string;
export type Identifier = string;
export type ISO2Code = string;
export type ISO3Code = string;
export type NumericCode = string;
export type CurrencyCode = string;

export interface Dataset<T> {
  schema_version: string;
  as_of_date: DateString;
  record_count: number;
  records: T[];
}

export interface Country {
  name: string;
  official_name: string | null;
  iso2: ISO2Code;
  iso3: ISO3Code;
  numeric_code: NumericCode;
  region_id: Identifier | null;
  subregion_id: Identifier | null;
  intermediate_region_id: Identifier | null;
  currency_codes: CurrencyCode[];
  trade_group_ids: Identifier[];
  customs_relationship_ids: Identifier[];
  wto_member: boolean;
  customs_authority_id: Identifier | null;
  trade_portal_ids: Identifier[];
  trade_agency_ids: Identifier[];
  standards_body_id: Identifier | null;
  landlocked: boolean | null;
  aliases: string[];
  source_ids: Identifier[];
}

export type CountryScope =
  | { country_code: ISO2Code; country_codes?: never }
  | { country_code?: never; country_codes: ISO2Code[] };

export type CustomsAuthority = CountryScope & {
  id: Identifier;
  name: string;
  authority_type:
    | "border-and-customs-administration"
    | "customs-administration"
    | "tax-and-customs-authority";
  website: string;
  languages: string[];
  source_ids: Identifier[];
  last_verified: DateString;
};

export interface Participant {
  type: "country" | "trade-group";
  id: string;
}

export interface CustomsRelationship {
  id: Identifier;
  name: string;
  relationship_type: "customs-arrangement" | "customs-union";
  participants: Participant[];
  status: "active" | "inactive" | "superseded";
  effective_from: DateString | null;
  effective_to: DateString | null;
  scope_note: string;
  source_ids: Identifier[];
  last_verified: DateString;
}

export type OfficialTradePortal = CountryScope & {
  id: Identifier;
  name: string;
  portal_type:
    | "customs"
    | "export-guidance"
    | "import-guidance"
    | "single-window"
    | "standards"
    | "tariff-lookup"
    | "trade-information"
    | "trade-statistics";
  website: string;
  topics: Array<
    | "customs"
    | "export"
    | "import"
    | "market-information"
    | "standards"
    | "tariffs"
    | "trade-regulations"
  >;
  languages: string[];
  source_ids: Identifier[];
  last_verified: DateString;
};

export interface Region {
  id: Identifier;
  code: NumericCode;
  name: string;
  parent_id: Identifier | null;
  level: "region" | "subregion" | "intermediate-region";
  classification_system: "UN-M49";
  source_ids: Identifier[];
}

export interface Source {
  id: Identifier;
  title: string;
  authority: string;
  url: string;
  license: string | null;
  license_url: string | null;
  reuse_conditions: string;
  retrieved_date: DateString;
  last_verified: DateString;
  normalization: string;
  dataset_fields: string[];
  update_frequency: "annual" | "before-release" | "quarterly" | "when-notified";
}

export type StandardsBody = CountryScope & {
  id: Identifier;
  name: string;
  acronym: string;
  organization_type: "national-standards-body";
  website: string;
  source_ids: Identifier[];
  last_verified: DateString;
};

export type TradeAgency = CountryScope & {
  id: Identifier;
  name: string;
  agency_type:
    | "export-promotion"
    | "government-trade-agency"
    | "investment-promotion"
    | "trade-and-investment"
    | "trade-promotion";
  website: string;
  services: Array<
    | "buyer-seller-matching"
    | "export-guidance"
    | "investment-support"
    | "market-information"
    | "trade-events"
  >;
  source_ids: Identifier[];
  last_verified: DateString;
};

export interface Membership extends Participant {
  status: "member" | "party" | "signatory" | "suspended";
  effective_from?: DateString | null;
  effective_to?: DateString | null;
}

export interface TradeGroup {
  id: Identifier;
  name: string;
  short_name: string | null;
  relationship_type:
    | "customs-union"
    | "economic-and-political-union"
    | "free-trade-area"
    | "free-trade-association"
    | "intergovernmental-group"
    | "intergovernmental-organization"
    | "international-organization"
    | "trade-agreement";
  members: Membership[];
  official_website: string;
  source_ids: Identifier[];
  last_verified: DateString;
  notes?: string;
}

export const countries: Dataset<Country>;
export const customsAuthorities: Dataset<CustomsAuthority>;
export const customsRelationships: Dataset<CustomsRelationship>;
export const officialTradePortals: Dataset<OfficialTradePortal>;
export const regions: Dataset<Region>;
export const sources: Dataset<Source>;
export const standardsBodies: Dataset<StandardsBody>;
export const tradeAgencies: Dataset<TradeAgency>;
export const tradeGroups: Dataset<TradeGroup>;

declare const datasets: Readonly<{
  countries: typeof countries;
  customsAuthorities: typeof customsAuthorities;
  customsRelationships: typeof customsRelationships;
  officialTradePortals: typeof officialTradePortals;
  regions: typeof regions;
  sources: typeof sources;
  standardsBodies: typeof standardsBodies;
  tradeAgencies: typeof tradeAgencies;
  tradeGroups: typeof tradeGroups;
}>;

export default datasets;
