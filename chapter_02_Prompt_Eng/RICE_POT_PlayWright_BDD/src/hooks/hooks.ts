import { Before, After, BeforeAll, AfterAll } from '@cucumber/cucumber';
import { chromium, firefox, webkit } from '@playwright/test';
import type { Browser, BrowserContext, Page } from '@playwright/test';
import type { CustomWorld } from '../support/custom-world';
import { config } from '../support/config';
import { LoginPage } from '../pages/LoginPage';

const browsers: Record<'chromium' | 'firefox' | 'webkit', typeof chromium> = {
  chromium,
  firefox,
  webkit,
};

let browser: Browser;

BeforeAll(async function () {
  const launcher = browsers[config.browser];
  browser = await launcher.launch({ headless: config.headless });
});

Before(async function (this: CustomWorld) {
  this.context = await browser.newContext({
    baseURL: config.baseUrl,
    viewport: { width: 1280, height: 720 },
    acceptDownloads: true,
    video: config.video === 'on' || config.video === 'retain-on-failure' ? 'retain-on-failure' : 'off',
    recordVideo: config.video === 'on' ? { dir: 'reports/videos' } : undefined,
  });
  this.page = await this.context.newPage();
  this.page.setDefaultTimeout(config.defaultTimeout);
  this.loginPage = new LoginPage(this.page);
});

After(async function (this: CustomWorld, scenario) {
  if (config.screenshotOnFailure && scenario.result?.status === 'FAILED' && this.page) {
    const screenshot = await this.page.screenshot({ fullPage: true });
    await this.attach(screenshot, 'image/png');
  }
  await this.context?.close();
});

AfterAll(async function () {
  await browser?.close();
});
