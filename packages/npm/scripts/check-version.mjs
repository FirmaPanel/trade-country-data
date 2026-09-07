import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";

const packageRoot = new URL("../", import.meta.url);
const repositoryRoot = new URL("../../../", import.meta.url);
const packageJson = JSON.parse(
  await readFile(new URL("package.json", packageRoot), "utf8"),
);
const countries = JSON.parse(
  await readFile(new URL("data/countries.json", repositoryRoot), "utf8"),
);
const expectedTag = `v${packageJson.version}`;
const releaseTag = process.argv[2];

if (packageJson.datasetVersion !== countries.schema_version) {
  throw new Error(
    `Bundled dataset version ${packageJson.datasetVersion} does not match schema version ${countries.schema_version}.`,
  );
}

if (releaseTag && releaseTag !== expectedTag) {
  throw new Error(
    `Release tag ${releaseTag} does not match package version ${expectedTag}.`,
  );
}

console.log(
  `Package ${packageJson.version} bundles dataset ${packageJson.datasetVersion}.`,
);
