# Findings: Jira ID to Test Plan Creator

## Protocol 0 boundary

The requested product decisions are now explicit: Jira Cloud is the source of truth, Groq is the model provider, and the local Streamlit UI is the delivery surface. Live API handshakes remain environment-dependent; the app exposes safe connection tests for both services.

## Confirmed from `BLAST.md`

- Protocol 0 requires project memory before tools or scripts are written.
- The project must define data schemas before coding.
- Discovery must cover the North Star, integrations, source of truth, delivery payload, and behavioral rules.
- Connectivity must be verified before full logic is built.
- The architecture separates SOPs, navigation/decision-making, and deterministic tools.
- The initial business objective is to create a test plan from a Jira ID.

## Initial solution interpretation

The Jira issue is the source document. The issue key is an identifier, not enough content by itself. The workflow therefore needs to fetch the issue, normalize the fields that contain requirements, identify gaps, and generate a test plan with traceability back to the source text.

The LLM should propose and organize test coverage, but it must not become the system of record for Jira facts. Jira retrieval, field normalization, schema validation, redaction, and output checks should remain deterministic.

## Jira API discovery

### Jira Cloud REST API: issue lookup

For Jira Cloud, the standard read request is:

```bash
curl --request GET \
  --url "https://YOUR-DOMAIN.atlassian.net/rest/api/3/issue/PROJ-123?fields=summary,description,issuetype,status,priority,labels,components,assignee,reporter,project,created,updated" \
  --user "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  --header "Accept: application/json"
```

The base URL must be the user's Jira site. `JIRA_EMAIL` and `JIRA_API_TOKEN` must come from the environment or a secret manager, never from source files, prompts, logs, or generated test plans.

A minimal request can be used during connectivity verification:

```bash
curl --fail-with-body --silent --show-error \
  --request GET \
  --url "$JIRA_BASE_URL/rest/api/3/issue/$JIRA_ISSUE_KEY?fields=summary,description" \
  --user "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  --header "Accept: application/json"
```

### Jira Cloud REST API: JQL search when lookup is insufficient

The preferred path is a direct issue lookup by key. JQL should only be used when the workflow needs related issues or a controlled discovery query:

```bash
curl --request POST \
  --url "$JIRA_BASE_URL/rest/api/3/search" \
  --user "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  --header "Accept: application/json" \
  --header "Content-Type: application/json" \
  --data '{
    "jql": "project = PROJ AND key = PROJ-123",
    "startAt": 0,
    "maxResults": 1,
    "fields": ["summary", "description", "issuetype", "status", "priority", "labels", "components"]
  }'
```

The exact search endpoint and payload can vary by Jira deployment and API version. The deployment type must be confirmed before treating this request as executable.

### Jira Cloud REST API: comments and links

Comments and linked issues may contain acceptance criteria or constraints, but they should not be fetched automatically until the user approves them as part of the source of truth. If approved, they should be requested explicitly and labeled by origin:

```bash
curl --request GET \
  --url "$JIRA_BASE_URL/rest/api/3/issue/$JIRA_ISSUE_KEY/comment" \
  --user "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  --header "Accept: application/json"
```

Possible follow-up endpoints include issue links, remote links, attachments, and changelog. Each adds permission, privacy, latency, and interpretation risk, so each should be enabled deliberately.

## Expected Jira response data

Jira Cloud descriptions and comments may use Atlassian Document Format (ADF), not plain text. The normalizer must support ADF nodes and preserve enough structure to identify headings, paragraphs, lists, tables, code blocks, and links. Custom fields are instance-specific and must be mapped through configuration rather than guessed.

Potentially useful fields:

- `key`: canonical issue identifier.
- `fields.summary`: short requirement title.
- `fields.description`: primary requirement text, often ADF.
- `fields.issuetype`: issue category.
- `fields.status`: current lifecycle state.
- `fields.priority`: planning priority.
- `fields.labels` and `fields.components`: scope hints.
- `fields.project`: project context.
- `fields.created` and `fields.updated`: source snapshot metadata.
- A configured custom acceptance-criteria field, if the project uses one.
- Approved comments or linked issues, if the discovery decision includes them.

## Key risks and constraints

- A valid issue key can still return 401, 403, 404, or incomplete data.
- Jira permissions may hide fields or linked artifacts.
- Acceptance criteria may be in a custom field, description, comments, or an attached document.
- ADF parsing errors can erase requirement details if handled as plain text only.
- Field names and custom field IDs differ between Jira instances.
- Rate limits and transient 5xx responses require bounded retries and clear diagnostics.
- Jira text may contain secrets or personal data; outputs need redaction rules.
- LLM output can invent expected results unless every case is validated for traceability.
- Generated plans should identify uncertainty instead of presenting assumptions as confirmed behavior.

## Discovery questions still open

1. What exact output makes the test plan acceptable: manual cases, automation-ready cases, or both?
2. Is the integration Jira Cloud, Jira Data Center, or Jira Server? What is the base URL and API version?
3. Are Jira API credentials available, and may they be stored as environment variables?
4. Should comments, linked issues, attachments, or only the target issue be part of the source of truth?
5. Where should the final JSON and Markdown plan be delivered?
6. Which fields contain acceptance criteria in this Jira project?
7. What coverage policy, priority scale, and test-case format should be used?
8. Which LLM/provider constraints apply, including data residency or prohibited data handling?

## Implemented checks

- Jira and Groq connection checks are available from `pages/settings.py`.
- Jira issue retrieval uses API v3 and requests only the approved fields.
- The Groq response is JSON-decoded and rejected if required sections, steps, expected results, or traceability are missing.
- Authentication errors never include tokens or response bodies.

## Remaining live checks

Before implementation, these checks can disconfirm the current assumptions:

- `GET /rest/api/3/issue/{key}?fields=summary,description` verifies that the account can read the target issue.
- Inspecting the returned `description` verifies whether ADF parsing is required.
- Comparing the response fields with the project's configured custom fields reveals where acceptance criteria actually live.
- Fetching an issue that the account should not access confirms that permission failures are surfaced without leaking response content.
