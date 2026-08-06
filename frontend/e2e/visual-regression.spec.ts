import { test, expect } from '@playwright/test';

test('Visual regression snapshot', async ({ page }) => {
  await page.goto('/');
  const screenshot = await page.screenshot();
  expect(screenshot).toMatchSnapshot('home.png');
});
