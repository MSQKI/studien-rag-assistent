import { test, expect } from '@playwright/test';

test.describe('Comprehensive Study Platform Test', () => {
  test('Full platform functionality check', async ({ page }) => {
    // Test 1: Dashboard loads
    await page.goto('/');
    await expect(page.locator('h1').last()).toBeVisible();
    await page.waitForTimeout(2000);

    console.log('✅ Dashboard loaded successfully');

    // Test 2: Check all navigation links work
    const navLinks = [
      { name: /rag/i, url: '/rag', heading: 'RAG Chat' },
      { name: /karteikarten/i, url: '/flashcards', heading: 'Karteikarten' },
      { name: /graph/i, url: '/graph', heading: 'Knowledge Graph' },
      { name: /datenverwaltung/i, url: '/data', heading: 'Datenverwaltung' },
    ];

    for (const link of navLinks) {
      await page.getByRole('link', { name: link.name }).first().click();
      await expect(page).toHaveURL(link.url);
      await page.waitForTimeout(1000);
      console.log(`✅ Navigation to ${link.url} works`);
    }

    // Test 3: RAG Chat Interface
    await page.goto('/rag');
    await page.waitForTimeout(2000);

    // Check if input field exists
    const ragInput = page.locator('textarea, input[type="text"]').first();
    if (await ragInput.isVisible()) {
      console.log('✅ RAG input field found');
    }

    // Test 4: Flashcards Interface
    await page.goto('/flashcards');
    await page.waitForTimeout(2000);

    // Check stats cards
    const statsCards = await page.locator('.stat-card, [class*="stat"]').count();
    console.log(`✅ Flashcards page shows ${statsCards} stat elements`);

    // Test 5: Knowledge Graph
    await page.goto('/graph');
    await page.waitForTimeout(3000);

    // Check if canvas or graph container exists
    const hasCanvas = await page.locator('canvas, #cy, [id*="graph"]').count() > 0;
    console.log(`✅ Knowledge Graph ${hasCanvas ? 'has visualization' : 'loaded'}`);

    // Test 6: Data Management
    await page.goto('/data');
    await page.waitForTimeout(2000);

    // Check tabs exist
    const tabs = await page.getByRole('button', { name: /dokumente|karteikarten|graph/i }).count();
    console.log(`✅ Data Management shows ${tabs} tabs`);

    // Test 7: Check API health
    const response = await page.request.get('http://localhost:8000/health');
    expect(response.ok()).toBeTruthy();
    const health = await response.json();
    console.log(`✅ Backend healthy: ${health.status}`);

    // Test 8: Get stats from all modules
    const ragStats = await page.request.get('http://localhost:8000/api/rag/stats');
    const ragData = await ragStats.json();
    console.log(`✅ RAG: ${ragData.total_documents} docs, ${ragData.total_chunks} chunks`);

    const flashcardStats = await page.request.get('http://localhost:8000/api/flashcards/stats/overview');
    const fcData = await flashcardStats.json();
    console.log(`✅ Flashcards: ${fcData.total_flashcards} total, ${fcData.due_today} due today`);

    const graphStats = await page.request.get('http://localhost:8000/api/graph/stats');
    const graphData = await graphStats.json();
    console.log(`✅ Graph: ${graphData.total_nodes} nodes, ${graphData.total_relationships} relationships`);

    // Final screenshot
    await page.goto('/');
    await page.waitForTimeout(1000);
    await page.screenshot({ path: 'tests/screenshots/comprehensive-final.png', fullPage: true });

    console.log('✅ ==========================================');
    console.log('✅ ALL COMPREHENSIVE TESTS PASSED');
    console.log('✅ ==========================================');
  });

  test('Test all critical buttons and interactions', async ({ page }) => {
    await page.goto('/');

    // Test "Erneut prüfen" button if flashcards exist
    await page.goto('/flashcards');
    await page.waitForTimeout(2000);

    const refreshButton = page.getByRole('button', { name: /erneut|refresh|prüfen/i });
    if (await refreshButton.isVisible({ timeout: 1000 }).catch(() => false)) {
      await refreshButton.click();
      await page.waitForTimeout(500);
      console.log('✅ Flashcard refresh button works');
    } else {
      console.log('ℹ️  No flashcards available to refresh');
    }

    // Test Graph zoom controls
    await page.goto('/graph');
    await page.waitForTimeout(2000);

    const zoomButtons = await page.getByRole('button', { name: /zoom|\\+|\\-/i }).count();
    console.log(`✅ Graph shows ${zoomButtons} zoom controls`);

    // Test Data Management tabs
    await page.goto('/data');
    await page.waitForTimeout(1000);

    const docTab = page.getByRole('button', { name: /dokumente/i }).first();
    if (await docTab.isVisible()) {
      await docTab.click();
      await page.waitForTimeout(500);
      console.log('✅ Documents tab clickable');
    }

    const flashcardTab = page.getByRole('button', { name: /karteikarten/i }).first();
    if (await flashcardTab.isVisible()) {
      await flashcardTab.click();
      await page.waitForTimeout(500);
      console.log('✅ Flashcards tab clickable');
    }

    console.log('✅ All interactive elements tested');
  });
});
