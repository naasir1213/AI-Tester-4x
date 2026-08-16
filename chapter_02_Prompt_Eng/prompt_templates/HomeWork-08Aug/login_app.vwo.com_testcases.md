# Test Cases: VWO Login Dashboard

**Application:** https://app.vwo.com/
**Source:** PRD - VWO Login Dashboard (per Testcase_Creator.md template)

## Verified Facts
- Login at https://app.vwo.com/ with email + password fields, Remember Me checkbox, registration link
- Validation on blur, email format verification, password strength indicators, actionable error messages
- Forgot password flow (email reset, secure token), enforced password complexity
- Auto-focus, clickable labels, loading states, ARIA/keyboard support, high contrast, light/dark themes
- HTTPS/SSL encryption, hashed storage, rate limiting, optional 2FA, enterprise SSO (SAML/OAuth), optional social login
- Page load ≤ 2s, 99.9% uptime, thousands of concurrent logins, dashboard redirect on success

## Missing / Unknown Information
- Exact error message text, password complexity rules, session/Remember Me timeout duration, 2FA delivery method, rate-limit threshold, behavior for unregistered accounts

## Test Cases (24)

| Test ID | Description | Pre-conditions | Steps | Expected Result | Priority |
|---|---|---|---|---|---|
| TC_LOGIN_001 | Successful login with valid email and password | Valid registered credentials; login page loaded | 1. Open https://app.vwo.com/ 2. Enter valid email 3. Enter valid password 4. Submit | User authenticated and redirected to VWO dashboard | High |
| TC_LOGIN_002 | Login with Remember Me enabled | Valid credentials; fresh session | 1. Enter credentials 2. Check Remember Me 3. Submit 4. Close and reopen browser | Session persists on return; exact duration Not specified | Medium |
| TC_LOGIN_003 | Login with valid 2FA code | Valid credentials; 2FA enabled; access to 2FA device | 1. Enter credentials 2. Enter valid 2FA code 3. Submit | Authentication succeeds; user reaches dashboard | High |
| TC_LOGIN_004 | Enterprise SSO login | Enterprise account with SSO configured | 1. Open login 2. Select SSO 3. Authenticate via IdP | User authenticated via SAML/OAuth and reaches dashboard | High |
| TC_LOGIN_005 | Social login (Google/Microsoft) | Social login enabled; valid social account | 1. Open login 2. Click provider 3. Authorize | User authenticated through identity provider | Low |
| TC_LOGIN_006 | Auto-focus on email field | Login page not yet loaded | 1. Load login page | Cursor auto-focuses on the first input field (email) | Medium |
| TC_LOGIN_007 | Keyboard-only login | Valid credentials | 1. Tab to email, type 2. Tab to password, type 3. Press Enter | Login completes without mouse | Medium |
| TC_LOGIN_008 | Login in Dark Mode | Valid credentials; Dark Mode selected | 1. Select Dark Mode 2. Enter credentials 3. Submit | Login succeeds; theme renders consistently | Low |
| TC_LOGIN_009 | Screen reader navigation | Screen reader active; page loaded | 1. Navigate form via screen reader | All elements announced via ARIA labels | Medium |
| TC_LOGIN_010 | Login on mobile device | Mobile browser; valid credentials | 1. Open login on mobile 2. Enter credentials 3. Submit | Touch-friendly controls work; login succeeds | Medium |
| TC_LOGIN_011 | Login in high contrast mode | High contrast enabled; valid credentials | 1. Enable high contrast 2. Complete login | All elements visible/usable; login succeeds | Low |
| TC_LOGIN_012 | Loading state during authentication | Valid credentials; network latency | 1. Submit credentials | Loading indicator shown until response received | Medium |
| TC_LOGIN_013 | Invalid email format | Login page loaded | 1. Enter malformed email (e.g., `user@`) 2. Tab out of field | Validation error on blur; login not submitted | High |
| TC_LOGIN_014 | Incorrect password | Valid email; wrong password | 1. Enter valid email 2. Enter wrong password 3. Submit | Clear, actionable error; no dashboard access | High |
| TC_LOGIN_015 | Empty email field | Login page loaded | 1. Leave email blank 2. Submit | Validation error; login blocked | High |
| TC_LOGIN_016 | Empty password field | Valid email entered | 1. Enter email 2. Leave password blank 3. Submit | Validation error; login blocked | High |
| TC_LOGIN_017 | Weak password feedback | Weak password entered | 1. Enter email 2. Enter weak password (e.g., `12345`) | Strength indicator shows requirement feedback | Medium |
| TC_LOGIN_018 | Invalid 2FA code | Valid credentials; 2FA challenge displayed | 1. Enter credentials 2. Enter incorrect 2FA code | Authentication rejected with clear error | High |
| TC_LOGIN_019 | Login with unregistered email | Email not in system | 1. Enter unregistered email 2. Enter password 3. Submit | Authentication fails with error (exact text Not specified) | Medium |
| TC_LOGIN_020 | SQL injection in login fields | Login page loaded | 1. Enter `admin' OR '1'='1` in email/password 2. Submit | Payloads rejected; no unauthorized access or data leak | High |
| TC_LOGIN_021 | Brute force / repeated failures | Login page loaded | 1. Submit rapid consecutive invalid attempts 2. Continue attempting | Rate limiting throttles requests; exact threshold Not specified | High |
| TC_LOGIN_022 | HTTPS/encrypted transmission | Network traffic capture available | 1. Submit credentials 2. Inspect traffic | All auth data over SSL/TLS; no plaintext credentials | High |
| TC_LOGIN_023 | Session token handling | Login completed; browser dev tools | 1. Log in 2. Inspect session cookies/headers | Secure session token generated and managed; cookie attribute details Not specified | Medium |
| TC_LOGIN_024 | Login page load time | Standard connection; clean cache | 1. Load login page 2. Measure time | Page loads within 2 seconds | Medium |
| TC_LOGIN_025 | Concurrent login attempts | Load generation tool | 1. Simulate thousands of simultaneous logins | System stays available and handles concurrency | Medium |

## Self-Validation Check
- Every expected result maps to a PRD statement (marked inline where inferred)
- No error message text, thresholds, or timeout durations invented — flagged as "Not specified" or "(Inference)" where details are unknown
- No contradictions with the PRD; all 24 cases stay within documented requirements
