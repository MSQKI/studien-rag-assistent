import { test, expect } from '@playwright/test';

/**
 * Complete E2E workflow test
 * Tests the entire user journey through the platform
 */
test.describe('Complete User Workflow', () => {
  test('should complete full user journey', async ({ page }) => {
    // 1. Start at Dashboard
    await page.goto('/');
    await expect(page.locator('h1').last()).toContainText('Dashboard');
    await page.waitForTimeout(1000);
    await page.screenshot({ path: 'tests/screenshots/workflow-1-dashboard.png', fullPage: true });

    // 2. Navigate to RAG and ask a question
    await page.getByRole('link', { name: /rag/i }).click();
    await expect(page).toHaveURL('/rag');

    const inputField = page.getByPlaceholder(/Stelle eine Frage/i);
    if (await inputField.count() > 0) {
      await inputField.fill('Erkläre mir Dichte');
      const submitButton = page.getByRole('button', { name: /frage stellen/i });
      if (await submitButton.count() > 0) {
        await submitButton.click();
        await page.waitForTimeout(2000);
      }
    }
    await page.screenshot({ path: 'tests/screenshots/workflow-2-rag.png', fullPage: true });

    // 3. Navigate to Flashcards and try "Erneut prüfen"
    await page.getByRole('link', { name: /karteikarten/i }).click();
    await expect(page).toHaveURL('/flashcards');
    await page.waitForTimeout(1000);

    const refreshButton = page.getByRole('button', { name: /erneut prüfen/i });
    if (await refreshButton.count() > 0) {
      await refreshButton.click();
      await page.waitForTimeout(1000);
    }
    await page.screenshot({ path: 'tests/screenshots/workflow-3-flashcards.png', fullPage: true });

    // 4. Navigate to Graph
    await page.getByRole('link', { name: /graph/i }).click();
    await expect(page).toHaveURL('/graph');
    await page.waitForTimeout(2000);

    // Try zoom buttons
    const zoomInButton = page.getByRole('button', { name: /zoom in|\+/i });
    if (await zoomInButton.count() > 0) {
      await zoomInButton.click();
    }
    await page.screenshot({ path: 'tests/screenshots/workflow-4-graph.png', fullPage: true });

    // 5. Navigate to Data Management
    await page.getByRole('link', { name: /datenverwaltung|data/i }).click();
    await expect(page).toHaveURL('/data');
    await page.waitForTimeout(1000);
    await page.screenshot({ path: 'tests/screenshots/workflow-5-data.png', fullPage: true });

    // 6. Return to Dashboard
    await page.getByRole('link', { name: /dashboard/i }).click();
    await expect(page).toHaveURL('/');
    await page.screenshot({ path: 'tests/screenshots/workflow-6-back-home.png', fullPage: true });

    console.log('✅ Complete workflow test passed!');
  });

  test('should test all critical buttons', async ({ page }) => {
    const buttonTests = [];

    // Test RAG submit button
    await page.goto('/rag');
    const submitButton = page.getByRole('button', { name: /frage stellen/i });
    if (await submitButton.count() > 0) {
      buttonTests.push('RAG submit button: ✅');
    } else {
      buttonTests.push('RAG submit button: ❌ NOT FOUND');
    }

    // Test Flashcards "Erneut prüfen" button
    await page.goto('/flashcards');
    await page.waitForTimeout(1000);
    const refreshButton = page.getByRole('button', { name: /erneut prüfen/i });
    if (await refreshButton.count() > 0) {
      buttonTests.push('Flashcards refresh button: ✅');
    } else {
      buttonTests.push('Flashcards refresh button: ❌ NOT FOUND');
    }

    // Test Graph zoom buttons
    await page.goto('/graph');
    await page.waitForTimeout(1000);
    const zoomInButton = page.getByRole('button', { name: /zoom in|\+/i });
    const zoomOutButton = page.getByRole('button', { name: /zoom out|-/i });
    if (await zoomInButton.count() > 0 && await zoomOutButton.count() > 0) {
      buttonTests.push('Graph zoom buttons: ✅');
    } else {
      buttonTests.push('Graph zoom buttons: ⚠️ PARTIAL');
    }

    // Print results
    console.log('\n=== Button Test Results ===');
    buttonTests.forEach(result => console.log(result));
    console.log('===========================\n');

    // All tests should pass
    expect(buttonTests.filter(r => r.includes('❌')).length).toBe(0);
  });
});
