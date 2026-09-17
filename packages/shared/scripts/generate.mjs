// Generate `src/api.d.ts` from `openapi.json` (AGENTS.md §4: never hand-maintain duplicate
// type definitions across the language boundary).
//
//   1. apps/api:        uv run python scripts/export_openapi.py   -> packages/shared/openapi.json
//   2. packages/shared: pnpm generate                              -> packages/shared/src/api.d.ts
//
// Both outputs are committed; CI regenerates them and fails if they differ from the tree.
// Pass `--check` to fail instead of writing when the output is stale.

import { readFile, writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";

import openapiTS, { astToString } from "openapi-typescript";

const SPEC = new URL("../openapi.json", import.meta.url);
const OUT = new URL("../src/api.d.ts", import.meta.url);

const HEADER = `/**
 * GENERATED FILE — DO NOT EDIT.
 *
 * Source: packages/shared/openapi.json (exported from apps/api by scripts/export_openapi.py).
 * Regenerate with \`pnpm --filter @hunterseeker/shared generate\`.
 */
`;

const check = process.argv.includes("--check");

const ast = await openapiTS(SPEC, {
  // Unions from Python \`Literal\` become TS string-literal unions rather than enums.
  enum: false,
  // \`x | null\` (Pydantic \`T | None\`) stays \`T | null\`; no \`?\` for required-but-nullable.
  defaultNonNullable: true,
});
const rendered = HEADER + astToString(ast);

if (check) {
  const current = await readFile(OUT, "utf8").catch(() => null);
  if (current !== rendered) {
    console.error(
      `${fileURLToPath(OUT)} is stale. Run \`pnpm --filter @hunterseeker/shared generate\` and commit.`,
    );
    process.exit(1);
  }
  console.log(`${fileURLToPath(OUT)} is up to date.`);
} else {
  await writeFile(OUT, rendered);
  console.log(`wrote ${fileURLToPath(OUT)}`);
}
