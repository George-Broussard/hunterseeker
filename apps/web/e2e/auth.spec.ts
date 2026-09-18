import { expect, test, type Page } from "@playwright/test";

// TODO(#9): the Seeker home moves to "/". Update SEEKER_HOME (and lib/auth/roles.ts).
const SEEKER_HOME = "/seeker";
const HUNTER_HOME = "/hunter";
const PASSWORD = "correct-horse-battery";

function uniqueEmail(tag: string): string {
  return `e2e-${tag}-${Date.now()}-${Math.random().toString(36).slice(2, 8)}@example.com`;
}

async function signUp(page: Page, role: "seeker" | "hunter", email: string) {
  await page.goto("/signup");
  await page.getByRole("radio", { name: role === "seeker" ? "Seeker" : "Hunter" }).check();
  await page.getByLabel("Name").fill("E2E User");
  await page.getByLabel("Email").fill(email);
  await page.getByLabel("Password").fill(PASSWORD);
  await page.getByRole("button", { name: "Create account" }).click();
}

test.describe("signup", () => {
  test("as a Seeker lands on the Seeker home", async ({ page }) => {
    await signUp(page, "seeker", uniqueEmail("seeker"));

    await expect(page).toHaveURL(SEEKER_HOME);
    await expect(page.getByRole("heading", { name: "Job Board" })).toBeVisible();
  });

  test("as a Hunter lands on /hunter", async ({ page }) => {
    await signUp(page, "hunter", uniqueEmail("hunter"));

    await expect(page).toHaveURL(HUNTER_HOME);
    await expect(page.getByText("Hunter — placeholder")).toBeVisible();
  });

  test("shows inline validation instead of browser bubbles", async ({ page }) => {
    await page.goto("/signup");
    await page.getByLabel("Password").fill("short");
    await page.getByRole("button", { name: "Create account" }).click();

    await expect(page).toHaveURL("/signup");
    await expect(page.getByText("Choose whether you're a Seeker or a Hunter.")).toBeVisible();
    await expect(page.getByText("Enter your name.")).toBeVisible();
    await expect(page.getByText("Enter a valid email address.")).toBeVisible();
    await expect(page.getByText("Use at least 8 characters.")).toBeVisible();
  });

  test("rejects an email that is already registered", async ({ page }) => {
    const email = uniqueEmail("dup");
    await signUp(page, "seeker", email);
    await expect(page).toHaveURL(SEEKER_HOME);

    // Fresh session; the proxy would otherwise bounce us off /signup.
    await page.context().clearCookies();
    await signUp(page, "hunter", email);

    await expect(page).toHaveURL("/signup");
    await expect(page.getByText("An account with this email already exists.")).toBeVisible();
  });
});

test.describe("login", () => {
  test("wrong password shows an error and stays on /login", async ({ page }) => {
    await page.goto("/login");
    await page.getByLabel("Email").fill(uniqueEmail("nobody"));
    await page.getByLabel("Password").fill("definitely-wrong");
    await page.getByRole("button", { name: "Sign in" }).click();

    await expect(page.getByText("That email and password don't match.")).toBeVisible();
    await expect(page).toHaveURL("/login");
  });

  test("existing Hunter signs in and is routed by role", async ({ page }) => {
    const email = uniqueEmail("login");
    await signUp(page, "hunter", email);
    await expect(page).toHaveURL(HUNTER_HOME);
    await page.context().clearCookies();

    await page.goto("/login");
    await page.getByLabel("Email").fill(email);
    await page.getByLabel("Password").fill(PASSWORD);
    await page.getByRole("button", { name: "Sign in" }).click();

    await expect(page).toHaveURL(HUNTER_HOME);
  });

  test("honours a same-origin callbackUrl", async ({ page }) => {
    const email = uniqueEmail("cb");
    await signUp(page, "seeker", email);
    await page.context().clearCookies();

    await page.goto(SEEKER_HOME);
    await expect(page).toHaveURL(`/login?callbackUrl=${encodeURIComponent(SEEKER_HOME)}`);
    await page.getByLabel("Email").fill(email);
    await page.getByLabel("Password").fill(PASSWORD);
    await page.getByRole("button", { name: "Sign in" }).click();

    await expect(page).toHaveURL(SEEKER_HOME);
  });
});

test.describe("API bearer token", () => {
  test("the session's apiToken is accepted by the API and carries the role", async ({
    page,
  }, testInfo) => {
    const apiUrl = testInfo.config.metadata.apiUrl as string;
    await signUp(page, "hunter", uniqueEmail("token"));
    await expect(page).toHaveURL(HUNTER_HOME);

    const session = await (await page.request.get("/api/auth/session")).json();
    expect(session.user.role).toBe("hunter");
    expect(typeof session.apiToken).toBe("string");

    const me = await page.request.get(`${apiUrl}/api/v1/auth/me`, {
      headers: { authorization: `Bearer ${session.apiToken}` },
    });
    expect(me.status()).toBe(200);
    expect(await me.json()).toMatchObject({ id: session.user.id, role: "hunter" });

    const anonymous = await page.request.get(`${apiUrl}/api/v1/auth/me`);
    expect(anonymous.status()).toBe(401);
  });
});

test.describe("route guard", () => {
  test("unauthenticated persona routes redirect to /login", async ({ page }) => {
    await page.goto(HUNTER_HOME);
    await expect(page).toHaveURL(`/login?callbackUrl=${encodeURIComponent(HUNTER_HOME)}`);

    await page.goto("/");
    await expect(page).toHaveURL("/login");
  });

  test("signed-in users are sent away from /login and the other persona's routes", async ({
    page,
  }) => {
    await signUp(page, "seeker", uniqueEmail("guard"));
    await expect(page).toHaveURL(SEEKER_HOME);

    await page.goto("/login");
    await expect(page).toHaveURL(SEEKER_HOME);
    await page.goto("/signup");
    await expect(page).toHaveURL(SEEKER_HOME);
    await page.goto(HUNTER_HOME);
    await expect(page).toHaveURL(SEEKER_HOME);
  });
});
