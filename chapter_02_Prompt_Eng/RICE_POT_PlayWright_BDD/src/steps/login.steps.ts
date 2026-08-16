import { Given, When, Then } from '@cucumber/cucumber';
import { expect } from '@playwright/test';
import type { CustomWorld } from '../support/custom-world';
import { testData } from '../utils/test-data';

Given('the user is on the Salesforce login page', async function (this: CustomWorld) {
  await this.loginPage.navigate();
});

When('the user logs in using valid Salesforce credentials', async function (this: CustomWorld) {
  const { username, password } = testData.validUser;
  await this.loginPage.login(username, password);
});

When('the user logs in using invalid Salesforce credentials', async function (this: CustomWorld) {
  const { username, password } = testData.invalidUser;
  await this.loginPage.login(username, password);
  this.loginErrorText = await this.loginPage.getLoginErrorMessage();
});

Then('the user should be successfully authenticated', async function (this: CustomWorld) {
  await this.page.waitForURL(/(lightning|home|setup)/, { timeout: 60000 });
  expect(this.page.url()).not.toContain('/login');
});

Then('an authentication error message should be displayed', async function (this: CustomWorld) {
  expect(this.loginErrorText).toContain('check your username and password');
});
