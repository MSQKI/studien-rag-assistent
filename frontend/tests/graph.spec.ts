import { test, expect } from '@playwright/test';

test.describe('Graph Page', () => {
  test('should display graph page and load concepts', async ({ page }) => {
    await page.goto('/graph');

    // Wait for page to load
    await expect(page.locator('h1').last()).toContainText('Knowledge Graph');

    // Wait for API call to complete
    await page.waitForTimeout(2000);

    // Take a screenshot
    await page.screenshot({ path: 'tests/screenshots/graph-page.png', fullPage: true });

    // Check if there are any console errors
    const errors: string[] = [];
    page.on('console', msg => {
      if (msg.type() === 'error') {
        errors.push(msg.text());
      }
    });

    // Check if graph is loaded or shows empty state
    const hasGraph = await page.locator('canvas').count() > 0;
    const hasEmptyState = await page.getByText('Noch keine Konzepte').count() > 0;

    expect(hasGraph || hasEmptyState).toBeTruthy();

    console.log('Graph page console errors:', errors);
  });

  test('should allow searching for concepts', async ({ page }) => {
    await page.goto('/graph');

    // Find and use search input
    const searchInput = page.getByPlaceholder('Konzept suchen...');
    await expect(searchInput).toBeVisible();

    await searchInput.fill('Dichte');

    // Take a screenshot after search
    await page.screenshot({ path: 'tests/screenshots/graph-search.png', fullPage: true });
  });
});
