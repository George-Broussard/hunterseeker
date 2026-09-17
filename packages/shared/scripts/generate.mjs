// Stub for the API type codegen.
//
// The real implementation generates TypeScript types from the FastAPI OpenAPI schema
// (AGENTS.md §4: never hand-maintain duplicate type definitions across the language
// boundary). It lands with the API interface issue. Until then this is a no-op so
// `pnpm --filter @hunterseeker/shared generate` is a stable entry point.
console.log(
  "[@hunterseeker/shared] generate: codegen not wired up yet (see the API interface issue).",
);
