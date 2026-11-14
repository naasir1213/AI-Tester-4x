# Task Plan: Jira ID to Test Plan Creator

## Protocol 0 status

- [x] Read and adopt the local `BLAST.md` protocol.
- [x] Define the initial objective: create a test plan from one Jira issue ID.
- [x] Create project memory files before writing automation code.
- [x] Record the initial Jira research and request shapes in `findings.md`.
- [x] Record the initial architecture, schemas, and invariants in `LLM.md`.
- [x] Record this initialization event in `progress.md`.
- [x] Convert the north star into a product contract: Jira Cloud read, Groq generation, local review UI.
- [x] Confirm authentication method: Jira API token and Groq API key from `.env` or Settings.
- [x] Confirm delivery: local Streamlit UI with JSON download and visible review questions.
- [x] Review and approve the input/output schemas in `LLM.md`.
- [x] Approve the implementation boundary in `architecture/jira_to_test_plan.md`.

## North-star goal

Given a Jira issue ID, retrieve the authoritative issue data, normalize its requirements and acceptance criteria, identify testable behavior, and produce a structured, reviewable test plan. The first version should be deterministic at the integration and validation boundaries, auditable, and safe to rerun.

## Scope for the first version

### In scope

- Accept one Jira issue key such as `PROJ-123`.
- Fetch the issue and only the fields required for test planning.
- Preserve the raw Jira response for traceability without exposing credentials.
- Normalize summary, description, issue type, status, labels, components, and acceptance criteria.
- Generate test-plan cases with positive, negative, boundary, permission, integration, and regression coverage where the issue supports them.
- Validate that every generated test case traces back to an issue requirement or is explicitly marked as an assumption.
- Return a machine-readable JSON result and a human-readable Markdown rendering.
- Fail clearly when the issue is missing, inaccessible, incomplete, or ambiguous.

### Out of scope for this version

- Writing files under `tools/`.
- Creating or modifying Jira issues.
- Automatically transitioning, commenting on, or attaching artifacts to Jira.
- Executing browser/API tests.
- Guessing missing acceptance criteria or inventing product behavior.
- Selecting an LLM provider, model, or prompt contract without approval.

## Phases and checklists

### Phase 0: Initialization and discovery

- [x] North Star: fetch a Jira issue from a natural-language request and create a traceable draft test plan.
- [x] Integrations: Jira Cloud and Groq; no Jira writes, comments, links, or attachments.
- [x] Source of truth: summary, description, status, priority, labels, components, and timestamps.
- [x] Delivery payload: local Streamlit review screen plus downloadable JSON.
- [x] Behavioral rules: facts stay grounded in Jira; gaps become questions or assumptions.
- [x] Jira API v3 and token authentication are implemented; live verification remains environment-dependent.
- [x] Secrets are excluded from logs, plans, and source control through `.gitignore`.

### Phase 1: Blueprint approval

- [x] Freeze the input, normalized Jira, and output test-plan shapes.
- [x] Define acceptance criteria for traceability and failure behavior.
- [x] Approve the architecture in `LLM.md` and the Jira SOP.

### Phase 2: Link verification

- [x] Store credentials in `.env` or local git-ignored `config.json`.
- [x] Add Jira and Groq connection checks to Settings.
- [x] Add request timeouts and safe error classification.
- [ ] Run live authenticated checks with a non-sensitive issue when network verification is desired.

### Phase 3: Architect and implement

- [x] Write the Jira retrieval SOP before implementation.
- [x] Implement issue-key validation, ADF normalization, and deterministic retrieval.
- [x] Implement Groq generation behind a versioned JSON contract.
- [x] Implement traceability and assumption validation.
- [x] Implement JSON download and review rendering.
- [ ] Add a fixture-based test suite in the next iteration.

### Phase 4: Review and delivery

- [ ] Review a live generated plan against a representative Jira issue.
- [x] Verify no secrets or unnecessary private fields appear in output.
- [ ] Verify reruns are stable for the same source snapshot and configuration.
- [x] Document setup, commands, environment variables, and known limitations.
- [ ] Obtain user feedback on coverage and presentation.

## Definition of done

- A user can provide a valid Jira issue key and receive a validated test plan.
- The source issue and retrieval time are recorded in metadata.
- Each test case has an ID, objective, preconditions, steps, expected result, priority, type, and traceability reference.
- Missing or ambiguous requirements are visible as questions or assumptions, never silently fabricated.
- Authentication uses environment variables and is absent from logs and artifacts.
- Automated checks cover the schema and the main failure paths.
- The blueprint and discovery answers are approved before implementation begins.
