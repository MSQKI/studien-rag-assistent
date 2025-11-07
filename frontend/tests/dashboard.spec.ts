import { test, expect } from '@playwright/test';

test.describe('Dashboard', () => {
  test('should display dashboard with all sections', async ({ page }) => {
    await page.goto('/');

    // Wait for page to load - check for welcome heading
    await expect(page.locator('h1').last().first()).toBeVisible();

    // Wait for API calls
    await page.waitForTimeout(2000);

    // Take a screenshot
    await page.screenshot({ path: 'tests/screenshots/dashboard.png', fullPage: true });

    // Check navigation links (using first() to get sidebar nav items)
    await expect(page.getByRole('link', { name: /dashboard/i }).first()).toBeVisible();
    await expect(page.getByRole('link', { name: /rag/i }).first()).toBeVisible();
    await expect(page.getByRole('link', { name: /karteikarten/i }).first()).toBeVisible();
    await expect(page.getByRole('link', { name: /graph/i }).first()).toBeVisible();
  });

  test('should navigate between pages', async ({ page }) => {
    await page.goto('/');

    // Navigate to Graph (using first() to get sidebar nav)
    await page.getByRole('link', { name: /graph/i }).first().click();
    await expect(page).toHaveURL('/graph');
    await page.waitForTimeout(1000); // Wait for page content to load

    // Navigate to Flashcards
    await page.getByRole('link', { name: /karteikarten/i }).first().click();
    await expect(page).toHaveURL('/flashcards');
    await page.waitForTimeout(1000);

    // Navigate back to Dashboard
    await page.getByRole('link', { name: /dashboard/i }).first().click();
    await expect(page).toHaveURL('/');
  });
});
