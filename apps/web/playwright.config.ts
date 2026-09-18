import { defineConfig, devices } from "@playwright/test";

/**
 * E2E for the auth flow (issue #7).
 *
 * By default a tiny in-memory stand-in for the FastAPI auth endpoints (`e2e/mock-api.mjs`)
 * is started so the suite runs anywhere Node runs. Set `E2E_API_URL` to point at a real
 * `apps/api` instance (with its database migrated) to exercise the whole stack.
 */
const WEB_PORT = 3007;
const MOCK_API_PORT = 8007;
const apiUrl = process.env.E2E_API_URL ?? `http://localhost:${MOCK_API_PORT}`;
const baseURL = `http://localhost:${WEB_PORT}`;

const authSecret = process.env.AUTH_SECRET ?? "e2e-only-secret-not-for-production-32b";

const webEnv = {
  ...process.env,
  API_URL: apiUrl,
  AUTH_URL: baseURL,
  AUTH_SECRET: authSecret,
  NEXT_TELEMETRY_DISABLED: "1",
};

export default defineConfig({
  testDir: "./e2e",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  reporter: process.env.CI ? [["github"], ["list"]] : "list",
  use: { baseURL, trace: "retain-on-failure" },
  metadata: { apiUrl },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
  webServer: [
    ...(process.env.E2E_API_URL
      ? []
      : [
          {
            command: `node e2e/mock-api.mjs ${MOCK_API_PORT}`,
            url: `http://localhost:${MOCK_API_PORT}/health`,
            env: { AUTH_SECRET: authSecret },
            reuseExistingServer: false,
          },
        ]),
    {
      command: `pnpm exec next dev --port ${WEB_PORT}`,
      url: `${baseURL}/login`,
      env: webEnv,
      reuseExistingServer: false,
      timeout: 120_000,
    },
  ],
});
