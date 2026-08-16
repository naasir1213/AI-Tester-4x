RICEPOT PROMPT — ENTERPRISE PLAYWRIGHT + TYPESCRIPT + CUCUMBER BDD AUTOMATION FRAMEWORK

R → ROLE

You are a Senior QA Automation Architect with 15+ years of experience designing enterprise-level test automation frameworks.

You have deep expertise in:

- Playwright
- TypeScript
- Cucumber BDD
- Node.js / npm
- Page Object Model
- REST API automation
- Cross-browser automation
- CI/CD integration
- Test reporting
- Environment configuration
- CRM applications such as Salesforce
- Enterprise SaaS applications
- Scalable and maintainable automation architecture
Your responsibility is to design and generate a production-ready Playwright + TypeScript + Cucumber BDD automation framework following enterprise-level architecture and coding standards.

The framework must be:

- Scalable
- Modular
- Maintainable
- Reusable
- Configuration-driven
- Environment-independent
- CI/CD ready
- Cross-browser compatible
- Parallel-execution ready
- Suitable for large enterprise automation suites
I → INSTRUCTIONS

Generate a complete Playwright + TypeScript + Cucumber BDD automation implementation for validating the Salesforce login page:

https://login.salesforce.com/?locale=in

Automate and verify exactly these scenarios:

1. Valid Login
2. Invalid Login
FRAMEWORK REQUIREMENTS

Use:

- Playwright
- TypeScript
- @cucumber/cucumber
- Node.js
- npm
- Page Object Model
- Gherkin Feature Files
- Step Definitions
- Hooks
- Custom World
- Environment Configuration
- Cucumber Configuration
- Playwright Configuration
MANDATORY PROJECT STRUCTURE

playwright-bdd-framework/
 │
 ├── package.json
 ├── tsconfig.json
 ├── cucumber.js
 ├── playwright.config.ts
 ├── .env
 ├── .env.example
 │
 ├── src/
 │  ├── pages/
 │  │  └── LoginPage.ts
 │  │
 │  ├── steps/
 │  │  └── login.steps.ts
 │  │
 │  ├── hooks/
 │  │  └── hooks.ts
 │  │
 │  ├── support/
 │  │  ├── custom-world.ts
 │  │  └── config.ts
 │  │
 │  ├── utils/
 │  │  └── test-data.ts
 │  │
 │  └── features/
 │  └── login.feature
 │
 └── reports/

BDD REQUIREMENTS

Use proper Gherkin syntax with:

- Feature
- Background where appropriate
- Scenario
- Given
- When
- Then
- And
Use meaningful tags such as:

@ui
 @login
 @smoke
 @positive
 @negative

Avoid duplicate step definitions and unnecessary repetition.

SCENARIO 1 — VALID LOGIN

Validate login using valid Salesforce credentials supplied through environment variables.

The username and password must never be hardcoded inside:

- Feature files
- Step definitions
- Page Objects
- Configuration source files
SCENARIO 2 — INVALID LOGIN

Attempt login using invalid credentials and verify the appropriate Salesforce login error message.

Invalid credentials should come from reusable test data configuration.

PAGE OBJECT MODEL REQUIREMENTS

Create:

LoginPage.ts

The Page Object must:

- Receive Playwright Page through constructor injection
- Encapsulate all Salesforce login-page locators
- Encapsulate reusable login-page actions
- Keep locators out of step definitions
- Expose meaningful business/action methods
- Avoid unnecessarily exposing raw locators
- Keep assertions outside Page Objects wherever practical
Expected reusable methods may include:

async navigate(): Promise

async enterUsername(username: string): Promise

async enterPassword(password: string): Promise

async clickLogin(): Promise

async login(username: string, password: string): Promise

async setRememberMe(enabled: boolean): Promise

async getLoginErrorMessage(): Promise

LOCATOR STRATEGY

Follow Playwright-native locator best practices.

Preferred locator strategy:

1. getByRole()
2. getByLabel()
3. getByPlaceholder()
4. getByText()
5. data-testid or another stable test attribute
6. CSS locator only when required
7. XPath only as the final fallback
Do not force XPath when a reliable semantic Playwright locator is available.

Locators must be:

- Stable
- Unique
- Readable
- Maintainable
- Resistant to UI changes
Avoid:

- Absolute XPath
- Indexed XPath
- Deep DOM chaining
- Dynamic generated classes
- Brittle selectors
PLAYWRIGHT AUTO-WAIT REQUIREMENTS

Do not use:

page.waitForTimeout()

Do not use:

setTimeout()

Do not add arbitrary/static waits.

Use:
-authenticate once via API and reuse storageState, do not log in through the UI in every test. 
- use Playwright fixtures for setup, not BeforeEach with manual browser launch
- Playwright auto-waiting
- Web-first assertions
- locator.waitFor() only when genuinely required
- page.waitForURL() for navigation validation
- Event-driven waits where appropriate
ASSERTION REQUIREMENTS

Use Playwright assertions such as:

expect(locator).toBeVisible()

expect(locator).toHaveText()

expect(locator).toContainText()

expect(page).toHaveURL()

Prefer web-first assertions rather than manually polling DOM elements.

CUCUMBER HOOKS

Create proper Cucumber hooks.

Use where appropriate:

Before
 After
 BeforeAll
 AfterAll

The framework must:

- Initialize browser execution correctly
- Create a BrowserContext per scenario
- Create a Page per scenario
- Initialize required Page Objects
- Dispose BrowserContext after each scenario
- Close browser resources correctly
- Capture screenshot when a scenario fails
- Attach the failure screenshot to the Cucumber report
CUSTOM WORLD REQUIREMENTS

Create a strongly typed Cucumber Custom World.

The World should expose scenario-specific objects such as:

browser
 context
 page
 loginPage

Do not use uncontrolled global variables for scenario state.

Scenario-level resources must remain isolated to support parallel execution.

BROWSER CONFIGURATION

Support browser selection through environment variables.

Example:

BROWSER=chromium

Supported values:

chromium
 firefox
 webkit

Default:

chromium

Browser-launch logic must exist in a reusable centralized location.

HEADLESS CONFIGURATION

Support:

HEADLESS=true
 HEADLESS=false

Default:

HEADLESS=true

The framework must work correctly in headless CI/CD execution.

ENVIRONMENT CONFIGURATION

Use dotenv or equivalent environment configuration.

Expected variables:

BASE_URL=https://login.salesforce.com/?locale=in

SF_USERNAME=

SF_PASSWORD=

BROWSER=chromium

HEADLESS=true

ENV=qa

Credentials must never be committed to source control.

Create an:

.env.example

file containing placeholders only.

TEST DATA MANAGEMENT

Separate test data from automation code.

Example structure:

invalidUser: {
 username: “invalid@example.com”,
 password: “InvalidPassword123!”
 }

Do not scatter test data across Step Definition files.

ERROR HANDLING

Do not wrap every Playwright action in unnecessary try-catch blocks.

Allow Playwright, assertions and Cucumber failures to propagate naturally.

Use contextual exception handling only when it genuinely improves diagnostics.

Use try/finally where resource cleanup requires it.

Never:

- Swallow exceptions
- Catch errors and continue silently
- Replace assertion failures with console logs
- Hide original Playwright errors
TYPESCRIPT REQUIREMENTS

Use strict TypeScript.

Enable:

“strict”: true

Avoid using:

any

unless technically unavoidable.

Use:

- Explicit typing
- Interfaces where useful
- Strongly typed Custom World
- Async/await
- Consistent module imports
- Explicit return types where appropriate
CODING STANDARDS

Follow:

- SOLID principles
- DRY principles
- Separation of concerns
- Single Responsibility Principle
- Reusability
- Meaningful naming conventions
- Clean-code standards
Do not create:

- Giant Step Definition files
- Duplicate locators
- Duplicate browser setup
- Hardcoded URLs
- Hardcoded credentials
- Static waits
- Unnecessary inheritance
- Unnecessary utility classes
FEATURE FILE REQUIREMENT

Create:

src/features/login.feature

Expected business intent:

Feature: Salesforce Login

As a Salesforce user
 I want to authenticate through the login page
 So that access is granted only with valid credentials

@ui @login @smoke @positive
 Scenario: Login using valid Salesforce credentials
 Given the user is on the Salesforce login page
 When the user logs in using valid Salesforce credentials
 Then the user should be successfully authenticated

@ui @login @negative
 Scenario: Login using invalid Salesforce credentials
 Given the user is on the Salesforce login page
 When the user logs in using invalid Salesforce credentials
 Then an authentication error message should be displayed

CUCUMBER CONFIGURATION

Configure Cucumber to support:

- TypeScript
- Feature discovery
- Step Definition discovery
- Hooks
- Tags
- Parallel execution
- HTML reporting
- JSON reporting
NPM SCRIPTS

Provide useful scripts such as:

“test”: “cucumber-js”

“test:smoke”: “cucumber-js –tags ‘@smoke’”

“test:login”: “cucumber-js –tags ‘@login’”

“test:positive”: “cucumber-js –tags ‘@positive’”

“test:negative”: “cucumber-js –tags ‘@negative’”

“test:chromium”: “…”

“test:firefox”: “…”

“test:webkit”: “…”

“test:headed”: “…”

“test:parallel”: “…”

The scripts must work with the selected framework architecture without unnecessary duplication.

CROSS-BROWSER REQUIREMENTS

Support execution on:

- Chromium
- Firefox
- WebKit
Changing browsers must not require source-code modification.

PARALLEL EXECUTION

Design the framework to support safe parallel Cucumber scenario execution.

Do not share the following across scenarios:

- Page
- BrowserContext
- Scenario-specific Page Objects
- Mutable test data
Parallel workers should be configurable.

REPORTING

Configure at least:

- Cucumber HTML report
- Cucumber JSON report
On scenario failure:

- Capture screenshot
- Attach screenshot to Cucumber result/report
Keep the architecture extensible for future Allure integration.

LOGGING

Use meaningful runtime logging only where genuinely required.

Avoid excessive:

console.log()

Do not use logs as a replacement for assertions.

SECURITY REQUIREMENTS

Never expose:

- Salesforce usernames
- Salesforce passwords
- Access tokens
- Refresh tokens
- Secrets
- Session cookies
inside:

- Logs
- Reports
- Source code
- Feature files
- Git repository
Use environment variables or CI/CD secrets.

CI/CD READINESS

The framework must be executable from:

- GitHub Actions
- Azure DevOps
- Jenkins
Do not generate platform-specific pipeline YAML unless explicitly requested.

The framework must support non-interactive execution such as:

npm ci

npx playwright install –with-deps

npm test

FORBIDDEN PRACTICES

Do not use:

page.waitForTimeout()

Do not use:

setTimeout()

Do not:

- Hardcode credentials
- Hardcode browser selection
- Use uncontrolled global variables
- Duplicate locators
- Use brittle absolute XPath
- Add arbitrary sleeps
- Suppress failed assertions
- Add unnecessary try-catch blocks
- Mix browser setup with test business logic
- Put the complete framework inside one file
- Add excessive comments
- Use bad coding practices
C → CONTEXT

The application under test is Salesforce Login:

https://login.salesforce.com/?locale=in

The login page includes:

- Username / Email
- Password
- Login button
- Remember Me checkbox
- Forgot Password functionality
- Validation/error messages
The application may contain UI variations due to:

- Salesforce releases
- Localization
- A/B testing
- Environment-specific configuration
Therefore, use stable accessibility-based Playwright locators instead of DOM-position-dependent selectors.

The immediate scope is Salesforce login automation.

However, the framework architecture should support future automation modules such as:

- Accounts
- Contacts
- Leads
- Opportunities
- Campaigns
- Dashboards
- Salesforce APIs
E → EXAMPLE

Expected Page Object style:

import { Locator, Page } from ‘@playwright/test’;

export class LoginPage {

```
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

    this.loginButton = page.getByRole(
        'button',
        { name: /log in/i }
    );

    this.rememberMeCheckbox =
        page.getByLabel(/remember me/i);

    this.errorMessage =
        page.locator('#error');
}

async navigate(baseUrl: string): Promise<void> {

    await this.page.goto(baseUrl);
}

async login(
    username: string,
    password: string
): Promise<void> {

    await this.usernameInput.fill(username);

    await this.passwordInput.fill(password);

    await this.loginButton.click();
}
```
}

Expected BDD style:

@ui @login
 Feature: Salesforce Login

As a Salesforce user
 I want to authenticate through the login page
 So that only authorized users can access Salesforce

@smoke @positive
 Scenario: Login using valid Salesforce credentials
 Given the user is on the Salesforce login page
 When the user logs in using valid Salesforce credentials
 Then the user should be successfully authenticated

@negative
 Scenario: Login using invalid Salesforce credentials
 Given the user is on the Salesforce login page
 When the user logs in using invalid Salesforce credentials
 Then an authentication error message should be displayed

P → PARAMETERS

Generate the solution with production-level automation standards and minimal bad coding practices.

Use configurable parameters:

BASE_URL=<Salesforce QA/Staging URL>

SF_USERNAME=

SF_PASSWORD=

BROWSER=chromium|firefox|webkit

HEADLESS=true|false

ENV=qa|staging|uat|prod

DEFAULT_TIMEOUT=30000

NAVIGATION_TIMEOUT=60000

CUCUMBER_TAGS=@smoke

PARALLEL_WORKERS=2

SCREENSHOT_ON_FAILURE=true

VIDEO=off|retain-on-failure

TRACE=off|retain-on-failure|on-first-retry

RETRIES=0

REPORT_PATH=reports

LOG_LEVEL=info

All parameters must be changeable without modifying test-source files.

External credentials must be consumed securely through environment variables.

O → OUTPUT

Generate a complete runnable Playwright + TypeScript + Cucumber BDD project.

Provide exactly these files:

package.json

tsconfig.json

cucumber.js

playwright.config.ts

.env.example

src/features/login.feature

src/pages/LoginPage.ts

src/steps/login.steps.ts

src/hooks/hooks.ts

src/support/custom-world.ts

src/support/config.ts

src/utils/test-data.ts

Generate automation for:

1. Valid Login
2. Invalid Login
The generated project must run using:

npm install

npx playwright install

npm test

The output must contain:

- Complete file contents
- Correct imports
- Correct dependencies
- Runnable scripts
- Consistent project structure
- Proper TypeScript configuration
- Working BDD implementation
Do not provide conceptual explanations outside the generated project unless explicitly requested.

T → TONE

Technical, precise, enterprise-grade and implementation-focused.

Behave as a QA Automation Architect reviewing production-ready automation code.

Prioritize:

- Correctness
- Maintainability
- Reliability
- Scalability
- Playwright-native practices
- BDD readability
- Security
- CI/CD compatibility
- Cross-browser support
- Parallel execution readiness
Avoid:

- Generic explanations
- Beginner-level tutorials
- Excessive comments
- Unnecessary verbosity
- Bad coding practices
