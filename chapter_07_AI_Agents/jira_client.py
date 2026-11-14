import re
from datetime import datetime, timezone

import requests
from requests.auth import HTTPBasicAuth


class JiraError(Exception):
    pass


class JiraAuthError(JiraError):
    pass


class JiraNotFoundError(JiraError):
    pass


ISSUE_KEY_PATTERN = re.compile(r"\b[A-Z][A-Z0-9_]+-\d+\b")


def extract_issue_key(text: str) -> str | None:
    match = ISSUE_KEY_PATTERN.search(text.upper())
    return match.group(0) if match else None


def _text_from_adf(node: object) -> str:
    if isinstance(node, str):
        return node
    if not isinstance(node, dict):
        return ""
    parts = []
    if node.get("type") == "text":
        parts.append(str(node.get("text", "")))
    for child in node.get("content", []):
        child_text = _text_from_adf(child)
        if child_text:
            parts.append(child_text)
    separator = "\n" if node.get("type") in {"paragraph", "heading", "listItem", "codeBlock"} else ""
    return separator.join(parts)


def _field_name(field: object) -> str:
    if isinstance(field, dict):
        return str(field.get("name") or field.get("displayName") or "")
    return str(field or "")


def fetch_issue(config: dict, issue_key: str) -> dict:
    if not config.get("jira_url") or not config.get("jira_email") or not config.get("jira_api_token"):
        raise JiraAuthError("Jira URL, email, and API token are required in Settings.")
    if not ISSUE_KEY_PATTERN.fullmatch(issue_key.upper()):
        raise JiraError("Use a Jira issue key such as PROJ-123 in the prompt.")

    url = f"{config['jira_url'].rstrip('/')}/rest/api/3/issue/{issue_key.upper()}"
    params = {"fields": "summary,description,issuetype,status,priority,labels,components,project,created,updated"}
    try:
        response = requests.get(
            url,
            params=params,
            auth=HTTPBasicAuth(config["jira_email"], config["jira_api_token"]),
            headers={"Accept": "application/json"},
            timeout=20,
        )
    except requests.RequestException as exc:
        raise JiraError("Jira could not be reached. Check the URL and network connection.") from exc

    if response.status_code in (401, 403):
        raise JiraAuthError("Jira rejected the credentials or the account lacks issue access.")
    if response.status_code == 404:
        raise JiraNotFoundError(f"Jira issue {issue_key.upper()} was not found.")
    if not response.ok:
        raise JiraError(f"Jira returned HTTP {response.status_code}.")

    fields = response.json().get("fields", {})
    description = _text_from_adf(fields.get("description", "")).strip()
    acceptance = []
    for line in description.splitlines():
        if re.match(r"\s*(?:[-*]|\d+[.)])\s+", line):
            acceptance.append(re.sub(r"^\s*(?:[-*]|\d+[.)])\s+", "", line).strip())

    return {
        "schema_version": "1.0",
        "source": {
            "system": "jira",
            "base_url": config["jira_url"].rstrip("/"),
            "issue_key": response.json().get("key", issue_key.upper()),
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": fields.get("updated"),
        },
        "issue": {
            "summary": fields.get("summary", ""),
            "description": description,
            "issue_type": _field_name(fields.get("issuetype")),
            "status": _field_name(fields.get("status")),
            "priority": _field_name(fields.get("priority")),
            "labels": fields.get("labels", []),
            "components": [_field_name(value) for value in fields.get("components", [])],
            "acceptance_criteria": acceptance,
        },
    }


def test_connection(config: dict) -> str:
    if not config.get("jira_url") or not config.get("jira_email") or not config.get("jira_api_token"):
        raise JiraAuthError("Complete all Jira settings before testing the connection.")
    try:
        response = requests.get(
            f"{config['jira_url'].rstrip('/')}/rest/api/3/myself",
            auth=HTTPBasicAuth(config["jira_email"], config["jira_api_token"]),
            headers={"Accept": "application/json"},
            timeout=15,
        )
    except requests.RequestException as exc:
        raise JiraError("Jira could not be reached. Check the URL and network connection.") from exc
    if response.status_code in (401, 403):
        raise JiraAuthError("Jira rejected the credentials.")
    if not response.ok:
        raise JiraError(f"Jira returned HTTP {response.status_code}.")
    return response.json().get("displayName") or response.json().get("emailAddress") or "Connected"