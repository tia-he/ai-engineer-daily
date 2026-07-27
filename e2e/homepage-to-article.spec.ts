import { expect, test } from "@playwright/test";

// Relies on the deterministic seed data from backend/init_db.py.
// The backend must already be running and seeded before this test
// starts (see README's "Getting Started" and the CI workflow's e2e job).

test("homepage links to an article and back", async ({ page }) => {
  await page.goto("/");

  await expect(
    page.getByRole("heading", { name: "AI Engineer Daily", level: 1 }),
  ).toBeVisible();

  // NewsCard wraps a heading inside an <article> inside the <a>; the
  // nested <article> role breaks "name from content" computation for
  // the outer link, so target the heading directly instead — clicking
  // it still bubbles to the enclosing link.
  const articleHeading = page.getByRole("heading", {
    name: "OpenAI Releases New Coding Model",
  });
  await expect(articleHeading).toBeVisible();
  await articleHeading.click();

  await expect(page).toHaveURL(/\/news\/openai-coding-model$/);
  await expect(
    page.getByRole("heading", { name: "OpenAI Releases New Coding Model" }),
  ).toBeVisible();
  await expect(
    page.getByText(
      "AI coding assistants are evolving from code completion toward repository-level software engineering.",
    ),
  ).toBeVisible();

  await page.getByRole("link", { name: /Back to the brief/i }).click();
  await expect(page).toHaveURL("http://localhost:3000/");
});
