import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests/browser",
  timeout: 90_000,
  expect: {
    timeout: 15_000,
  },
  fullyParallel: true,
  retries: process.env.CI ? 1 : 0,
  reporter: process.env.CI ? "github" : "line",
  use: {
    baseURL: "http://127.0.0.1:8765",
    browserName: "chromium",
    trace: "retain-on-failure",
  },
  webServer: {
    command: "python -m http.server 8765 --bind 127.0.0.1",
    url: "http://127.0.0.1:8765/",
    reuseExistingServer: !process.env.CI,
    timeout: 30_000,
  },
});
