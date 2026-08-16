import { defineConfig } from '@playwright/test';
import dotenv from 'dotenv';
import path from 'path';

dotenv.config({ path: path.resolve(process.cwd(), '.env') });

const reportPath = process.env.REPORT_PATH ?? 'reports';
const browserType = process.env.BROWSER ?? 'chromium';
const defaultTimeout = parseInt(process.env.DEFAULT_TIMEOUT ?? '30000', 10);
const supportedBrowsers = ['chromium', 'firefox', 'webkit'] as const;

const selectedBrowsers = (supportedBrowsers as readonly string[]).includes(browserType)
  ? [browserType as (typeof supportedBrowsers)[number]]
  : [...supportedBrowsers];

export default defineConfig({
  testDir: './src/features',
  testIgnore: ['**/*.feature'],
  timeout: defaultTimeout,
  expect: { timeout: defaultTimeout },
  retries: parseInt(process.env.RETRIES ?? '0', 10),
  workers: parseInt(process.env.PARALLEL_WORKERS ?? '1', 10),
  reporter: [['html', { outputFolder: path.join(reportPath, 'playwright-report') }]],
  use: {
    baseURL: process.env.BASE_URL ?? 'https://login.salesforce.com/?locale=in',
    headless: (process.env.HEADLESS ?? 'true') !== 'false',
    screenshot: 'only-on-failure',
    video: (process.env.VIDEO ?? 'off') as 'off' | 'on' | 'retain-on-failure',
    trace: (process.env.TRACE ?? 'off') as 'off' | 'on' | 'retain-on-failure' | 'on-first-retry',
  },
  projects: selectedBrowsers.map((name) => ({ name, use: { browserName: name } })),
});
