# Project Constitution: Jira ID to Test Plan Creator

## Purpose

This document is the working constitution for the Jira-to-test-plan project. It defines the data contracts, behavioral rules, and architecture that must be approved before implementation. It uses `LLM.md` as the requested name for the Protocol 0 constitution described in `BLAST.md`.

## Current design position

The system should be a controlled pipeline, not a free-form chatbot. Jira is the source of factual requirements. Deterministic code retrieves, normalizes, validates, redacts, and renders data. The LLM may synthesize candidate coverage from a bounded, labeled input and must return a strict schema. A validator rejects unsupported claims, malformed cases, missing traceability, and unmarked assumptions.

This is a design position, not a claim that the final behavior is approved. Discovery answers may change it.

## Schemas

The following JSON shapes are the initial proposal. They are intentionally versioned and should be finalized during Blueprint approval.

### Input: `TestPlanRequest`

```json
{
  "schema_version": "1.0",
  "jira_issue_key": "PROJ-123",
  "options": {
    "include_comments": false,
    "include_linked_issues": false,
    "include_attachments": false,
    "output_formats": ["json", "markdown"]
  },
  "requested_by": "optional-user-id",
  "correlation_id": "optional-run-id"
}
```

Rules for input:

- `jira_issue_key` is required and must match the configured Jira key pattern.
- Options default to the least-privileged source: target issue fields only.
- Optional expansions require explicit approval and separate traceability.
- `requested_by` and `correlation_id` are metadata, not requirement content.
- Secrets, tokens, and passwords are never valid input fields.

### Normalized source: `JiraRequirementSnapshot`

```json
{
  "schema_version": "1.0",
  "source": {
    "system": "jira",
    "base_url": "https://example.atlassian.net",
    "issue_key": "PROJ-123",
    "retrieved_at": "2026-09-05T00:00:00Z",
    "updated_at": "2026-09-04T12:00:00Z"
  },
  "issue": {
    "summary": "Short requirement title",
    "description": {
      "text": "Normalized description",
      "blocks": []
    },
    "issue_type": "Story",
    "status": "To Do",
    "priority": "High",
    "labels": [],
    "components": [],
    "acceptance_criteria": [],
    "custom_fields": {}
  },
  "approved_related_sources": [],
  "gaps": [],
  "redactions": []
}
```

Rules for the source snapshot:

- Preserve the issue key and retrieval metadata.
- Preserve provenance for each normalized requirement block.
- Parse Atlassian Document Format without silently dropping unsupported nodes.
- Keep unknown custom fields only when configured and permitted.
- Represent absent, inaccessible, and empty fields differently where possible.
- Never include the authorization header, API token, cookies, or raw credentials.

### Output: `TestPlan`

```json
{
  "schema_version": "1.0",
  "metadata": {
    "source_issue_key": "PROJ-123",
    "source_updated_at": "2026-09-04T12:00:00Z",
    "generated_at": "2026-09-05T00:00:00Z",
    "generator_version": "0.1.0",
    "generation_status": "draft"
  },
  "summary": "Test-plan scope and risk summary",
  "questions": [],
  "assumptions": [],
  "risks": [],
  "test_cases": [
    {
      "id": "TC-001",
      "title": "Case title",
      "type": "positive",
      "priority": "high",
      "preconditions": [],
      "test_data": [],
      "steps": [
        {
          "step": 1,
          "action": "Action grounded in a requirement",
          "expected_result": "Observable result",
          "source_refs": ["jira:PROJ-123/description/block-1"]
        }
      ],
      "expected_result": "Overall expected result",
      "automation_candidate": true,
      "source_refs": ["jira:PROJ-123/acceptance-criteria/1"],
      "assumption_refs": []
    }
  ]
}
```

Required output invariants:

- Every test case has at least one `source_refs` entry or an `assumption_refs` entry.
- An assumption must be visible in the top-level `assumptions` list and cannot be disguised as a fact.
- Every step has an observable expected result.
- Test-case IDs are stable within one generated plan.
- `generation_status` is `draft` until validation passes and a reviewer accepts it.
- Questions are retained when the issue lacks enough information to define reliable coverage.
- The output must never claim that a test was executed; it is a plan unless execution evidence exists separately.

## Behavioral rules

1. Do not guess business logic. Ask a question or record an explicit assumption.
2. Treat Jira as the factual source for the retrieved snapshot, not the LLM's memory.
3. Use least-privileged reads and request only approved fields.
4. Keep raw source, normalized source, model input, model output, and final output distinguishable.
5. Redact secrets and sensitive personal data from logs and rendered artifacts.
6. Prefer complete, traceable coverage over a large number of repetitive cases.
7. Consider positive, negative, boundary, validation, authorization, integration, and regression coverage when supported by the issue.
8. Do not create, update, transition, comment on, or attach anything to Jira without a separate explicit workflow.
9. Fail closed on schema violations, missing required source data, invalid Jira identifiers, and unbounded model output.
10. Make retries bounded and idempotent; never duplicate a delivery because of a retry.
11. Preserve uncertainty and provenance through every transformation.
12. Never log authentication headers, API tokens, cookies, or full sensitive response bodies.

## Architecture: B.L.A.S.T. plus A.N.T.

### Blueprint

- `task_plan.md` is the phase plan and approval checklist.
- `findings.md` records research, constraints, endpoint decisions, and unresolved questions.
- `LLM.md` is the data and behavior constitution.
- No scripts in `tools/` are created until discovery and schema approval are complete.

### Link

A deterministic Jira client will:

- Validate and encode the issue key.
- Build the configured read-only endpoint.
- Authenticate using environment variables or an approved secret manager.
- Apply timeouts, bounded retries for transient failures, and safe error classification.
- Return a source snapshot plus response metadata without credentials.

### Architect

The implementation should follow three layers:

1. **Architecture/SOPs:** Markdown contracts for Jira retrieval, ADF normalization, traceability, generation, validation, and rendering.
2. **Navigation:** A small coordinator that validates the request, selects the approved source expansions, calls tools in order, and stops on unsafe or incomplete input.
3. **Tools:** Atomic deterministic modules for Jira HTTP, ADF parsing, normalization, redaction, schema validation, and output rendering.

The LLM adapter belongs behind a narrow interface. It receives a versioned normalized snapshot, a versioned instruction contract, and explicit output constraints. It does not call Jira directly and does not decide which private fields may be fetched.

### Stylize

The first delivery should support JSON for downstream systems and Markdown for human review. Formatting must not change factual content. The Markdown renderer should display source metadata, questions, assumptions, risks, traceability, and test cases clearly.

### Trigger

The initial trigger is a direct request containing one Jira issue key in the Streamlit UI. n8n may later provide the orchestration trigger, but the first delivery is intentionally local and read-only.

## Failure model

- `400`: invalid request or issue key; report a correctable input error.
- `401`: authentication failure; report configuration failure without echoing credentials.
- `403`: permission failure; report inaccessible source and stop.
- `404`: issue or endpoint not found; distinguish deployment/configuration from missing issue when possible.
- `429`: rate limit; retry only according to bounded backoff and server guidance.
- `5xx` or network timeout: bounded retry, then a clear unavailable-source error.
- Invalid or incomplete Jira data: produce a blocked/draft result with questions; do not invent requirements.
- Invalid LLM JSON or unsupported claims: reject and record validation errors; do not silently repair factual content.

## Approval gates

The first implementation satisfies these gates:

- The north star, integrations, source, delivery, and behavioral rules are recorded in `task_plan.md`.
- Jira Cloud API v3, base URL configuration, and token authentication are implemented.
- The initial authoritative fields are summary, description, status, priority, labels, and components; custom acceptance fields remain a documented follow-up.
- The input, normalized source, and output schemas are implemented and validated at runtime.
- The initial delivery destination is the local Streamlit UI and a downloadable JSON artifact.
- Live connection checks remain user-triggered because they use external credentials.
