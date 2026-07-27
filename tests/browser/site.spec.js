import { expect, test } from "@playwright/test";


test("landing page exposes the three working entry points without internal jargon", async ({ page }) => {
  await page.goto("/");

  await expect(page.getByRole("heading", { name: "Разбор реплеев" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Тренажёр стратегий" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Документация" })).toBeVisible();
  await expect(page.locator(".tool-status.ready")).toHaveCount(3);

  const body = await page.locator("body").innerText();
  expect(body).not.toContain("Reference по");
  expect(body).not.toContain("reconnaissance");
  expect(body).not.toContain("Internals (engine recon)");
});


test("documentation search, entity cards, and dual table scrolling work", async ({ page }) => {
  await page.goto("/docs/?p=reference%2F04_units%2FREADME.md");
  await expect(page.locator("#md-content h1")).toContainText("Юниты");

  const search = page.locator("#md-search-input");
  await search.fill("Академия");
  await expect(page.locator("#md-search-results .md-search-result").first()).toBeVisible();

  const topScroll = page.locator(".md-table-scroll-top:not([hidden])").first();
  const bottomScroll = topScroll.locator("xpath=following-sibling::*[contains(@class,'md-table-scroll')]");
  await expect(topScroll).toBeVisible();
  await topScroll.evaluate((element) => {
    element.scrollLeft = 120;
    element.dispatchEvent(new Event("scroll"));
  });
  await expect.poll(() => bottomScroll.evaluate((element) => element.scrollLeft)).toBeGreaterThan(0);

  await page.goto("/docs/?entity=unit%3Apikeman");
  await expect(page.locator(".entity-card h1")).toContainText("Пикинер");
  await expect(page.locator(".entity-card img")).toBeVisible();
  await expect(page.locator(".entity-card .entity-sid code")).toHaveText("pikeman");
});


test("legacy English anchors land below the fixed header", async ({ page }) => {
  await page.goto(
    "/docs_en/?p=reference%2F05_upgrades%2FREADME.md" +
    "#%D0%BC%D0%B0%D1%82%D0%B5%D0%BC%D0%B0%D1%82%D0%B8%D0%BA%D0%B0-" +
    "%D0%BF%D1%80%D0%B8%D0%BC%D0%B5%D0%BD%D0%B5%D0%BD%D0%B8%D1%8F-" +
    "%D0%BF%D0%BE%D1%80%D1%8F%D0%B4%D0%BE%D0%BA-%D0%B8-" +
    "%D0%BA%D0%BE%D0%BC%D0%B1%D0%B8%D0%BD%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5"
  );

  const heading = page.getByRole("heading", { name: "How upgrades combine" });
  await expect(heading).toBeVisible();
  await expect.poll(async () => {
    const header = await page.locator(".topbar").boundingBox();
    const target = await heading.boundingBox();
    return target.y - (header.y + header.height);
  }).toBeGreaterThanOrEqual(0);
});


test("build-order planner initializes and completes a simulation", async ({ page }) => {
  test.slow();
  await page.goto("/editor/");

  await expect(page.locator("#status")).toHaveClass(/ready/, { timeout: 60_000 });
  await expect(page.locator("#run_sim")).toBeEnabled();
  await page.locator("#run_sim").click();
  await expect(page.locator("#status")).toContainText("Готово", { timeout: 30_000 });
  await expect(page.locator("#summary")).not.toBeEmpty();
});


test("replay analyzer initializes its local parser", async ({ page }) => {
  test.slow();
  await page.goto("/replay-parser/");

  await expect(page.locator("#status")).toHaveClass(/ready/, { timeout: 60_000 });
  await expect(page.locator("#file_input")).toBeEnabled();
});
