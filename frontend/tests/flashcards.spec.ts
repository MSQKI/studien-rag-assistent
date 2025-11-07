import { test, expect } from '@playwright/test';

test.describe('Flashcards Page', () => {
  test('should display flashcards page', async ({ page }) => {
    await page.goto('/flashcards');

    // Wait for page to load - use last() to get content h1, not header h1
    await expect(page.locator('h1').last().last()).toContainText('Karteikarten');

    // Wait for API calls
    await page.waitForTimeout(2000);

    // Take a screenshot
    await page.screenshot({ path: 'tests/screenshots/flashcards-page.png', fullPage: true });

    // Check for stats
    const hasStats = await page.locator('.stat-card').count() > 0;
    expect(hasStats).toBeTruthy();
  });

  test('should handle "Erneut prüfen" button', async ({ page }) => {
    await page.goto('/flashcards');

    await page.waitForTimeout(2000);

    // Look for the refresh button
    const refreshButton = page.getByRole('button', { name: /erneut prüfen/i });

    if (await refreshButton.count() > 0) {
      await refreshButton.click();

      // Wait for any changes
      await page.waitForTimeout(1000);

      // Take a screenshot after clicking
      await page.screenshot({ path: 'tests/screenshots/flashcards-refresh.png', fullPage: true });
    }
  });
});
