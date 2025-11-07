import { test, expect } from '@playwright/test';

test.describe('Data Management Page', () => {
  test('should display data management interface', async ({ page }) => {
    await page.goto('/data');

    // Wait for page to load
    await expect(page.locator('h1').last()).toContainText('Datenverwaltung');

    // Wait for tabs to load
    await page.waitForTimeout(1000);

    // Check for tabs
    const documentTab = page.getByRole('tab', { name: /dokumente/i });
    const flashcardsTab = page.getByRole('tab', { name: /karteikarten/i });
    const graphTab = page.getByRole('tab', { name: /graph/i });

    await expect(documentTab).toBeVisible();
    await expect(flashcardsTab).toBeVisible();
    await expect(graphTab).toBeVisible();

    // Take a screenshot
    await page.screenshot({ path: 'tests/screenshots/data-management.png', fullPage: true });
  });

  test('should test document upload button', async ({ page }) => {
    await page.goto('/data');

    // Click documents tab
    const documentTab = page.getByRole('tab', { name: /dokumente/i });
    await documentTab.click();

    await page.waitForTimeout(500);

    // Look for upload button
    const uploadButton = page.getByRole('button', { name: /hochladen|upload/i });

    if (await uploadButton.count() > 0) {
      await expect(uploadButton).toBeVisible();
      console.log('Upload button found');
    }

    await page.screenshot({ path: 'tests/screenshots/documents-tab.png', fullPage: true });
  });

  test('should test flashcards tab CRUD buttons', async ({ page }) => {
    await page.goto('/data');

    // Click flashcards tab
    const flashcardsTab = page.getByRole('tab', { name: /karteikarten/i });
    await flashcardsTab.click();

    await page.waitForTimeout(1000);

    // Check for edit/delete buttons (should appear when there are flashcards)
    const editButtons = page.getByRole('button', { name: /bearbeiten|edit/i });
    const deleteButtons = page.getByRole('button', { name: /löschen|delete/i });

    console.log(`Found ${await editButtons.count()} edit buttons`);
    console.log(`Found ${await deleteButtons.count()} delete buttons`);

    await page.screenshot({ path: 'tests/screenshots/flashcards-tab.png', fullPage: true });
  });

  test('should test graph tab clear button', async ({ page }) => {
    await page.goto('/data');

    // Click graph tab
    const graphTab = page.getByRole('tab', { name: /graph/i });
    await graphTab.click();

    await page.waitForTimeout(1000);

    // Look for clear button
    const clearButton = page.getByRole('button', { name: /löschen|leeren|clear/i });

    if (await clearButton.count() > 0) {
      await expect(clearButton).toBeVisible();
      console.log('Clear graph button found');
    }

    await page.screenshot({ path: 'tests/screenshots/graph-tab.png', fullPage: true });
  });
});
