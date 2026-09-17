import { describe, expect, it } from "vitest";

import { PERSONAS, SHARED_PACKAGE_NAME } from "./index";

describe("@hunterseeker/shared", () => {
  it("exports the placeholder", () => {
    expect(SHARED_PACKAGE_NAME).toBe("@hunterseeker/shared");
    expect(PERSONAS).toEqual(["seeker", "hunter"]);
  });
});
