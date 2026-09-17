import { describe, expect, expectTypeOf, it } from "vitest";

import type { ApiSchema, Persona } from "./index";
import { PERSONAS, SHARED_PACKAGE_NAME } from "./index";
import spec from "../openapi.json";

const DOMAINS = [
  "profiles",
  "matching",
  "applications",
  "ats",
  "messaging",
  "feed",
  "network",
  "imports",
];

describe("@hunterseeker/shared", () => {
  it("exports the placeholder", () => {
    expect(SHARED_PACKAGE_NAME).toBe("@hunterseeker/shared");
    expect(PERSONAS).toEqual(["seeker", "hunter"]);
  });

  it("agrees with the API contract on the persona vocabulary", () => {
    expectTypeOf<ApiSchema<"Persona">>().toEqualTypeOf<Persona>();
  });

  it("types a Match with a score and an ATS-pass flag", () => {
    expectTypeOf<ApiSchema<"MatchedJob">["score"]>().toEqualTypeOf<number>();
    expectTypeOf<ApiSchema<"MatchedJob">["ats_pass"]>().toEqualTypeOf<true>();
    expectTypeOf<ApiSchema<"FeedItem">["kind"]>().toEqualTypeOf<"post" | "matched_job">();
  });

  it("has every domain mounted under /api/v1 in the committed openapi.json", () => {
    const paths = Object.keys(spec.paths);
    for (const domain of DOMAINS) {
      expect(
        paths.some((p) => p.startsWith(`/api/v1/${domain}`)),
        domain,
      ).toBe(true);
    }
  });
});
