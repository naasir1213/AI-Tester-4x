# RICEPOT Plan — Enterprise Playwright + TypeScript + Cucumber BDD Framework

## Goal

Build a production-ready, runnable **Playwright + TypeScript + Cucumber BDD** automation framework from the RICEPOT spec in `chapter_02_Prompt_Eng/RICEPOTFramewokr_Playwright.md`, automating exactly two Salesforce login scenarios (Valid Login, Invalid Login) against `https://login.salesforce.com/?locale=in`.

**Deliverable (user-facing plan doc):** a copy of this plan saved as `chapter_02_Prompt_Eng/RICEPOT_Plan_Framework_Playwright.md` (same folder as `04_Plan_Framework.md`, the existing convention).

**Framework location:** build inside the existing empty directory `chapter_02_Prompt_Eng/RICE_POT_PlayWright_BDD/`.

## Key Architectural Decisions

| Decision | Choice | Why |
|---|---|---|
| Runner | `@cucumber/cucumber` (not Playwright Test runner) | Spec mandates Cucumber hooks, Custom World, Gherkin — the runner must be Cucumber |
| Assertions | `expect` imported from `@playwright/test` | Web-first assertions per spec; the `playwright` library alone doesn't export `expect` |
| Types/runtime | `ts-node/register` + CommonJS (`module: commonjs`) | Reliable Cucumber+TS integration; the spec's example imports from `@playwright/test` |
| Browser lifecycle | Launch once per worker (`BeforeAll`/`AfterAll`), fresh `BrowserContext` + `Page` per scenario (`Before`/`After`) | Parallel-safe isolation; per-spec requirement |
| Config | Single `src/support/config.ts` reading `process.env` via `dotenv`; zero hardcoded values | All parameters changeable without touching source (P → PARAMETERS) |
| Cross-platform scripts | `cross-env` in npm scripts | User is on Windows; `BROWSER=chromium` inline syntax fails in cmd.exe |
| HTML/JSON reports | Built-in `@cucumber/cucumber` `html:` and `json:` formatters | No extra reporter dependency; Allure can be added later without restructuring |
| `playwright.config.ts` | Minimal valid config with chromium/firefox/webkit projects | Satisfies the mandatory structure, powers `npx playwright install`, and serves future Playwright-native suites; the Cucumber run does not consume it |

**Deliverable file list (exactly the 12 files the spec's O → OUTPUT section requires):**

```
RICE_POT_PlayWright_BDD/
 ├── package.json
 ├── tsconfig.json
 ├── cucumber.js
 ├── playwright.config.ts
 ├── .env.example          (+ local .env, gitignored, empty placeholders)
 ├── .gitignore            (added — required by SECURITY: credentials must never be committed)
 ├── src/
 │   ├── pages/LoginPage.ts
 │   ├── steps/login.steps.ts
 │   ├── hooks/hooks.ts
 │   ├── support/custom-world.ts
 │   ├── support/config.ts
 │   ├── utils/test-data.ts
 │   └── features/login.feature
 └── reports/              (with .gitkeep)
```

## File-by-File Implementation Outline

### 1. `package.json`
- Dependencies: `@playwright/test` (bundles Playwright), `@cucumber/cucumber`, `dotenv`
- DevDependencies: `typescript`, `ts-node`, `@types/node`, `cross-env`
- Scripts (all `cross-env`-based for Windows):
  - `test`: `cucumber-js`
  - `test:smoke`: `cucumber-js --tags "@smoke"` · `test:login` · `test:positive` · `test:negative` (same pattern)
  - `test:chromium` / `test:firefox` / `test:webkit`: `cross-env BROWSER=... cucumber-js`
  - `test:headed`: `cross-env HEADLESS=false cucumber-js`
  - `test:parallel`: `cross-env PARALLEL_WORKERS=4 cucumber-js` (workers read in cucumber.js)
  - `typecheck`: `tsc --noEmit`

### 2. `tsconfig.json`
`strict: true`, `target: ES2022`, `module: commonjs`, `moduleResolution: node`, `esModuleInterop`, `skipLibCheck`, `noEmit: true`, `types: ["node"]`, `include: ["src"]`. No `any` anywhere.

### 3. `cucumber.js` (CommonJS config)
- `requireModule: ["ts-node/register"]`
- `require: ["src/steps/**/*.ts", "src/hooks/**/*.ts"]`
- `paths: ["src/features/**/*.feature"]`
- `parallel: Number(process.env.PARALLEL_WORKERS || 2)`
- `format`: `progress-bar` + `json:reports/cucumber-report.json` + `html:reports/cucumber-report.html`
- `publish: false`; optional `tags` from `process.env.CUCUMBER_TAGS`

### 4. `src/support/config.ts`
- `import 'dotenv/config'` at top
- Typed `Config` interface; singleton `config` built from env with defaults for every parameter in the spec's P section: `BASE_URL` (default `https://login.salesforce.com/?locale=in`), `SF_USERNAME`, `SF_PASSWORD`, `BROWSER` (default `chromium`, validated against `chromium|firefox|webkit`), `HEADLESS` (default `true`), `ENV` (default `qa`), `DEFAULT_TIMEOUT` (30000), `NAVIGATION_TIMEOUT` (60000), `CUCUMBER_TAGS`, `PARALLEL_WORKERS` (2), `SCREENSHOT_ON_FAILURE` (true), `VIDEO`, `TRACE`, `RETRIES` (0), `REPORT_PATH` (`reports`), `LOG_LEVEL` (`info`)
- Export helpers: `browserName`, `isHeadless`, `baseUrl`, `credentials` (typed), `timeouts`

### 5. `src/support/custom-world.ts`
```ts
import { setWorldConstructor, World } from '@cucumber/cucumber';
import type { Browser, BrowserContext, Page } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

export class CustomWorld extends World {
  browser!: Browser;
  context!: BrowserContext;
  page!: Page;
  loginPage!: LoginPage;
}
setWorldConstructor(CustomWorld);
```
No globals, no uncontrolled state — everything is scenario-scoped for parallel safety.

### 6. `src/utils/test-data.ts`
Separates data from code per spec:
```ts
export interface InvalidUser { username: string; password: string; }
export const invalidUser: InvalidUser = { username: 'invalid@example.com', password: 'InvalidPassword123!' };
```

### 7. `src/pages/LoginPage.ts`
Follows the spec's EXAMPLE block closely — constructor `page: Page` injection, encapsulated locators, business methods:
- Locators (Playwright-native, semantic, no XPath): `getByLabel(/username/i)`, `getByLabel(/password/i)`, `getByRole('button', { name: /log in/i })`, `getByLabel(/remember me/i)`, error via stable `#error` (falls back through `getByText` if `#error` proves unstable during verification)
- Methods: `navigate()`, `enterUsername()`, `enterPassword()`, `clickLogin()`, `login(username, password)`, `setRememberMe(enabled)`, `getLoginErrorMessage()`, and `waitForAuthenticationSuccess()` using **event-driven** `page.waitForURL(url => url.hostname !== 'login.salesforce.com')` (predicate form — no static waits, no `waitForTimeout`)
- No assertions inside the Page Object; assertions live in steps
- Zero `waitForTimeout`, zero `setTimeout`, zero static sleeps

### 8. `src/steps/login.steps.ts`
- `Given the user is on the Salesforce login page` → `loginPage.navigate(config.baseUrl)`
- `When the user logs in using valid Salesforce credentials` → `loginPage.login(config.credentials.username, config.credentials.password)` (credentials only from env — never hardcoded)
- `Then the user should be successfully authenticated` → `waitForAuthenticationSuccess()` + `expect(page).not.toHaveURL(/login\.salesforce\.com/)`
- `When the user logs in using invalid Salesforce credentials` → `loginPage.login(invalidUser.username, invalidUser.password)` (data from test-data.ts)
- `Then an authentication error message should be displayed` → `expect(errorMessage).toBeVisible()` + `expect(errorMessage).toContainText('Please check your username and password')`
- No try/catch; failures propagate. No duplicate step definitions.

### 9. `src/hooks/hooks.ts`
- Module-level `let browser: Browser` (one per worker process — safe for `parallel`)
- `BeforeAll`: `setDefaultTimeout(config.timeouts.default)`; launch via `chromium.launch` / `firefox.launch` / `webkit.launch` selected from `config.browserName` and `config.isHeadless` (centralized — single launch site)
- `Before`: `context = await browser.newContext()` → `page = await context.newPage()` → `loginPage = new LoginPage(page)`; assign into `this` (the CustomWorld)
- `After`: if `scenario.result?.status === 'FAILED'` and `SCREENSHOT_ON_FAILURE`, capture `page.screenshot({ fullPage: true })` and `this.attach(screenshot, 'image/png')`; always `await context.close()`
- `AfterAll`: `await browser.close()`
- Optional (config-gated): `context.tracing.start/stop` per scenario with trace saved to `reports/` when `TRACE=retain-on-failure`

### 10. `src/features/login.feature`
Exact spec content — Feature: Salesforce Login, `@ui @login @smoke @positive` valid scenario, `@ui @login @negative` invalid scenario, Given/When/Then as specified. No credentials anywhere in the file.

### 11. `.env.example` + `.env`
`.env.example` committed with placeholders only (`BASE_URL`, `SF_USERNAME=`, `SF_PASSWORD=`, `BROWSER=chromium`, `HEADLESS=true`, `ENV=qa`, timeouts, etc.). Local `.env` created gitignored with empty values so `dotenv` loads cleanly.

### 12. `playwright.config.ts` + `reports/`
Minimal valid config: three `projects` (chromium/firefox/webkit) reading `HEADLESS`/`REPORT_PATH` from env; `reporter` minimal. Purpose: `npx playwright install` + CI reference. Create `reports/` with `.gitkeep`.

## Implementation Phases

1. **Scaffold** — `package.json`, `tsconfig.json`, `cucumber.js`, `.env.example`, `.env`, `.gitignore`
2. **Support layer** — `src/support/config.ts`, `src/support/custom-world.ts`, `src/utils/test-data.ts`
3. **Page Object** — `src/pages/LoginPage.ts`
4. **BDD layer** — `src/features/login.feature`, `src/steps/login.steps.ts`
5. **Hooks** — `src/hooks/hooks.ts` wiring browser/context/page lifecycle
6. **Config extras** — `playwright.config.ts`, `reports/.gitkeep`
7. **Plan artifact** — save a copy of this plan as `chapter_02_Prompt_Eng/RICEPOT_Plan_Framework_Playwright.md`

## Verification

1. `npm install` then `npx playwright install chromium` — clean install
2. `npm run typecheck` — zero TypeScript errors under `strict`
3. `npm run test:negative` — invalid-login scenario passes against live Salesforce (real error message asserted); this is the runnable proof without real credentials
4. `npm run test:valid` — only with real `SF_USERNAME`/`SF_PASSWORD` set in `.env` (optional; expected to be skipped/documented as credential-gated)
5. Grep checks: no `waitForTimeout`, no `setTimeout`, no hardcoded credentials/URLs, no `any`, no XPath selectors in page object
6. Confirm `reports/cucumber-report.html` and `.json` are generated
7. If time permits, `npm run test:parallel` (2+ workers) to prove isolation

## Known Limitations / Notes

- Salesforce may serve CAPTCHA/SSO to some environments; if `test:negative` hits that, the error-message assertion needs the live DOM re-verified (locator strategy already prefers semantic `getByLabel`/`getByRole` to resist this)
- The valid-login scenario is credential-gated by design — credentials only exist in `.env`/CI secrets, never in the repo
- No platform-specific CI YAML generated (spec forbids it unless requested)
- Allure integration is left as an extension point: reports already emit JSON, so a later `allure-cucumberjs` adapter drops in without restructuring

## Out of Scope

- Selenium/Java framework (already covered by `RICE_POT_SeleniumAdvanceFramework/`)
- CI/CD pipeline YAML, Salesforce API modules, other page objects
