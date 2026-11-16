// Validate the MangaSeries examples and a set of test cases against the JSON Schema.
//
// Usage: node tools/validate/validate_json.mjs
// Needs: ajv (run `npm install` in tools/validate)
// Exit code 0 when every case behaves as expected, 1 otherwise.

import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import Ajv2020 from "ajv/dist/2020.js";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..", "..");
const EXAMPLES = ["manga-volume", "manhwa-chapter"];

const readJson = (path) => JSON.parse(readFileSync(resolve(ROOT, path), "utf8"));
const ajv = new Ajv2020({ allErrors: true });
const validate = ajv.compile(readJson("schema/1/MangaSeries.schema.json"));
let failures = 0;

// Validate one document and compare the result with what is expected.
function check(label, doc, wantValid) {
  const isValid = validate(doc);
  const asExpected = isValid === wantValid;
  if (!asExpected) failures++;
  console.log(asExpected ? "PASS" : "FAIL", label, "->", isValid ? "valid" : "invalid");
  if (!asExpected && !isValid) console.log("     ", ajv.errorsText(validate.errors));
}

for (const name of EXAMPLES) {
  check(`example ${name}`, readJson(`examples/${name}/MangaSeries.json`), true);
}

const base = { version: "1.0.0", titles: [{ text: "T", primary: true }] };
const twoPrimaries = [
  { text: "A", primary: true },
  { text: "B", primary: true },
];

// Each case: label, document, expected validity.
const CASES = [
  ["minimal file", base, true],
  ["year only", { ...base, startDate: { year: 2020 } }, true],
  ["relation with title", { ...base, relations: [{ type: "sequel", title: "X" }] }, true],
  ["extension contents are free", { ...base, extensions: { tool: { any: [1, { x: null }] } } }, true],
  ["misspelled field", { ...base, titel: "x" }, false],
  ["missing version", { titles: base.titles }, false],
  ["no primary title", { version: "1.0.0", titles: [{ text: "T" }] }, false],
  ["two primary titles", { version: "1.0.0", titles: twoPrimaries }, false],
  ["bad enum value", { ...base, readingMode: "webtoon" }, false],
  ["day without month", { ...base, startDate: { year: 2020, day: 3 } }, false],
  ["uppercase provider key", { ...base, externalIds: [{ provider: "AniList", id: "1" }] }, false],
  ["numeric external id", { ...base, externalIds: [{ provider: "anilist", id: 1 }] }, false],
  ["version 2.0.0", { ...base, version: "2.0.0" }, false],
  ["total of zero", { ...base, totalVolumes: 0 }, false],
  ["relation without target", { ...base, relations: [{ type: "sequel" }] }, false],
  ["score is rejected", { ...base, score: 9.1 }, false],
];

for (const [label, doc, wantValid] of CASES) {
  check(label, doc, wantValid);
}

console.log("json failures:", failures);
process.exit(failures ? 1 : 0);
