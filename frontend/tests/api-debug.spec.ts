import { test, expect } from '@playwright/test';

test('Debug API calls and Graph loading', async ({ page }) => {
  // Capture console logs
  const consoleLogs: string[] = [];
  page.on('console', msg => {
    consoleLogs.push(`[${msg.type()}] ${msg.text()}`);
  });

  // Capture network requests
  const apiCalls: { url: string; status: number; response?: any }[] = [];
  page.on('response', async response => {
    const url = response.url();
    if (url.includes('/api/')) {
      try {
        const text = await response.text();
        apiCalls.push({
          url,
          status: response.status(),
          response: text.substring(0, 200), // First 200 chars
        });
      } catch (e) {
        apiCalls.push({ url, status: response.status() });
      }
    }
  });

  // Navigate to graph page
  await page.goto('/graph');

  // Wait for network to be idle
  await page.waitForLoadState('networkidle');

  // Wait a bit more
  await page.waitForTimeout(3000);

  // Take screenshot
  await page.screenshot({ path: 'tests/screenshots/graph-debug.png', fullPage: true });

  // Log everything
  console.log('\n=== CONSOLE LOGS ===');
  consoleLogs.forEach(log => console.log(log));

  console.log('\n=== API CALLS ===');
  apiCalls.forEach(call => {
    console.log(`${call.status} ${call.url}`);
    if (call.response) {
      console.log(`Response: ${call.response}`);
    }
  });

  // Check if concepts were fetched
  const conceptsCall = apiCalls.find(c => c.url.includes('/api/graph/concepts'));
  if (conceptsCall) {
    console.log('\n=== CONCEPTS API CALL ===');
    console.log(`Status: ${conceptsCall.status}`);
    console.log(`Response: ${conceptsCall.response}`);
  }

  // Check page state
  const isLoading = await page.locator('text=Lade Graph...').count();
  const hasEmptyState = await page.locator('text=Noch keine Konzepte').count();
  const hasCanvas = await page.locator('canvas').count();

  console.log('\n=== PAGE STATE ===');
  console.log(`Loading indicator: ${isLoading > 0 ? 'YES' : 'NO'}`);
  console.log(`Empty state: ${hasEmptyState > 0 ? 'YES' : 'NO'}`);
  console.log(`Has canvas: ${hasCanvas > 0 ? 'YES' : 'NO'}`);
});
