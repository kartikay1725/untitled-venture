import { test, expect } from '@playwright/test';

test('Chaos: random API failure', async ({ page }) => {
  // Simulate backend returning 500 randomly
  await page.route('**/api/**', async route => {
    if (Math.random() < 0.3) {
      await route.fulfill({ status: 500, body: 'Internal Server Error' });
    } else {
      await route.continue();
    }
  });
  await page.goto('/');
  await page.fill('#title', 'Chaos Idea');
  await page.fill('#description', 'Testing chaos');
  await page.click('text=Submit Idea');
  const error = await page.locator('.error').first();
  if (await error.isVisible()) {
    expect(await error.innerText()).toContain('Error');
  }
});
