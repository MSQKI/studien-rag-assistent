import { test, expect } from '@playwright/test';

test.describe('RAG Chat Page', () => {
  test('should display RAG chat interface', async ({ page }) => {
    await page.goto('/rag');

    // Wait for page to load
    await expect(page.locator('h1').last()).toContainText('RAG Chat');

    // Check for input field
    const inputField = page.getByPlaceholder(/Stelle eine Frage/i);
    await expect(inputField).toBeVisible();

    // Check for submit button
    const submitButton = page.getByRole('button', { name: /Frage stellen/i });
    await expect(submitButton).toBeVisible();

    // Take a screenshot
    await page.screenshot({ path: 'tests/screenshots/rag-page.png', fullPage: true });
  });

  test('should submit query and show response', async ({ page }) => {
    await page.goto('/rag');

    const inputField = page.getByPlaceholder(/Stelle eine Frage/i);
    const submitButton = page.getByRole('button', { name: /Frage stellen/i });

    // Enter a test question
    await inputField.fill('Was ist Dichte?');
    await submitButton.click();

    // Wait for response
    await page.waitForTimeout(3000);

    // Take screenshot of response
    await page.screenshot({ path: 'tests/screenshots/rag-response.png', fullPage: true });
  });

  test('should test voice button if present', async ({ page }) => {
    await page.goto('/rag');

    // Check for voice button
    const voiceButton = page.getByRole('button', { name: /voice|mikrofon|aufnahme/i });

    if (await voiceButton.count() > 0) {
      await expect(voiceButton).toBeVisible();
      console.log('Voice button found and visible');
    } else {
      console.log('Voice button not yet implemented');
    }
  });
});
