import { setWorldConstructor, World } from '@cucumber/cucumber';
import type { Browser, BrowserContext, Page } from '@playwright/test';
import type { LoginPage } from '../pages/LoginPage';

export interface WorldOptions {
  parameters?: Record<string, unknown>;
}

export class CustomWorld extends World {
  browser!: Browser;
  context!: BrowserContext;
  page!: Page;
  loginPage!: LoginPage;
  loginErrorText = '';

  constructor(options: WorldOptions) {
    super(options);
  }
}

setWorldConstructor(CustomWorld);
