import { copyFile, mkdir, readdir, rm } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import path from "node:path";

const packageRoot = fileURLToPath(new URL("../", import.meta.url));
const repositoryRoot = fileURLToPath(new URL("../../../", import.meta.url));
const generatedRoot = path.join(packageRoot, "generated");

async function copyDirectory(source, destination, include) {
  await mkdir(destination, { recursive: true });

  for (const entry of await readdir(source, { withFileTypes: true })) {
    if (entry.isFile() && include(entry.name)) {
      await copyFile(path.join(source, entry.name), path.join(destination, entry.name));
    }
  }
}

await rm(generatedRoot, { force: true, recursive: true });

await copyDirectory(
  path.join(repositoryRoot, "data"),
  path.join(generatedRoot, "data"),
  (name) => name.endsWith(".json") || name === "countries.csv",
);
await copyDirectory(
  path.join(repositoryRoot, "schema"),
  path.join(generatedRoot, "schema"),
  (name) => name.endsWith(".json"),
);

for (const name of ["ATTRIBUTION.md", "LICENSE"]) {
  await copyFile(path.join(repositoryRoot, name), path.join(packageRoot, name));
}

console.log("Prepared npm package data from the repository snapshot.");
