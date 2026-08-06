import { test, expect } from '@playwright/test';

test('Idea submission and validation flow', async ({ page }) => {
  await page.goto('/');
  await page.fill('#email', 'test@example.com');
  await page.fill('#password', 'Password123!');
  await page.click('text=Login');
  await page.fill('#title', 'Test Idea');
  await page.fill('#description', 'A test description');
  await page.click('text=Submit Idea');
  await expect(page.locator('#validation-score')).toBeVisible();
  const score = await page.locator('#validation-score').innerText();
  expect(parseFloat(score)).toBeGreaterThan(0);
});
