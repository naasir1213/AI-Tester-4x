import type { Locator, Page } from '@playwright/test';
import { config } from '../support/config';

export class LoginPage {
  readonly page: Page;
  readonly usernameInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;
  readonly rememberMeCheckbox: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.usernameInput = page.getByLabel(/username/i);
    this.passwordInput = page.getByLabel(/password/i);
    this.loginButton = page.getByRole('button', { name: /log in/i });
    this.rememberMeCheckbox = page.getByLabel(/remember me/i);
    this.errorMessage = page.locator('#error');
  }

  async navigate(): Promise<void> {
    await this.page.goto(config.baseUrl, {
      waitUntil: 'domcontentloaded',
      timeout: config.navigationTimeout,
    });
  }

  async enterUsername(username: string): Promise<void> {
    await this.usernameInput.fill(username);
  }

  async enterPassword(password: string): Promise<void> {
    await this.passwordInput.fill(password);
  }

  async clickLogin(): Promise<void> {
    await this.loginButton.click();
  }

  async login(username: string, password: string): Promise<void> {
    await this.enterUsername(username);
    await this.enterPassword(password);
    await this.clickLogin();
  }

  async setRememberMe(enabled: boolean): Promise<void> {
    if (enabled) {
      await this.rememberMeCheckbox.check();
    } else {
      await this.rememberMeCheckbox.uncheck();
    }
  }

  async getLoginErrorMessage(): Promise<string> {
    await this.errorMessage.waitFor({ state: 'visible' });
    return this.errorMessage.innerText();
  }
}
