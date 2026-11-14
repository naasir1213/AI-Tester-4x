# Jira to Test Plan SOP

## Goal

Given a user request containing a Jira issue key, produce a reviewable draft test plan without inventing Jira facts.

## Navigation

1. Extract and validate one issue key from the request.
2. Fetch only the approved Jira issue fields with a read-only request.
3. Normalize Atlassian Document Format into plain text and preserve source metadata.
4. Send the normalized snapshot and the user request to Groq using the configured model.
5. Validate the JSON response for required sections, observable expected results, and traceability.
6. Render a draft plan. Never imply that the test cases were executed.

## Failure behavior

- Missing settings stop the run with an actionable configuration error.
- 401/403 responses stop the run without echoing credentials or response bodies.
- A missing issue stops the run with the issue key and no model call.
- Invalid model JSON or missing traceability rejects the plan.

## Data boundary

Tokens remain in local configuration. The model receives the normalized issue snapshot, not authorization headers, raw responses, or unrelated Jira fields.