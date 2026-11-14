import json

import requests


class GroqError(Exception):
    pass


BASE_URL = "https://api.groq.com/openai/v1"


def test_connection(config: dict) -> str:
    if not config.get("groq_api_key"):
        raise GroqError("Add a Groq API key before testing the connection.")
    try:
        response = requests.get(
            f"{BASE_URL}/models",
            headers={"Authorization": f"Bearer {config['groq_api_key']}"},
            timeout=15,
        )
    except requests.RequestException as exc:
        raise GroqError("Groq could not be reached. Check the network connection.") from exc
    if response.status_code in (401, 403):
        raise GroqError("Groq rejected the API key.")
    if not response.ok:
        raise GroqError(f"Groq returned HTTP {response.status_code}.")
    return "Connected"


def generate_plan(config: dict, snapshot: dict, user_prompt: str) -> dict:
    if not config.get("groq_api_key"):
        raise GroqError("Add a Groq API key in Settings before generating a plan.")
    system_prompt = """You are a senior software test architect. Return only valid JSON matching this shape:
{"summary":"string","questions":["string"],"assumptions":["string"],"risks":["string"],"test_cases":[{"id":"TC-001","title":"string","type":"positive|negative|boundary|security|integration|regression","priority":"high|medium|low","preconditions":["string"],"test_data":["string"],"steps":[{"step":1,"action":"string","expected_result":"string","source_refs":["string"]}],"expected_result":"string","automation_candidate":true,"source_refs":["string"],"assumption_refs":[]}]}.
Use only the Jira snapshot as factual source. Make missing details questions or explicit assumptions. Every case and step must have observable expected results and source_refs, unless assumption_refs explain the gap. Do not claim tests were executed."""
    payload = {"user_prompt": user_prompt, "jira_snapshot": snapshot}
    try:
        response = requests.post(
            f"{BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {config['groq_api_key']}", "Content-Type": "application/json"},
            json={
                "model": config.get("groq_model") or "openai/gpt-oss-120b",
                "temperature": 0.1,
                "response_format": {"type": "json_object"},
                "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": json.dumps(payload)}],
            },
            timeout=90,
        )
    except requests.RequestException as exc:
        raise GroqError("Groq could not be reached. Check the network connection.") from exc
    if response.status_code in (401, 403):
        raise GroqError("Groq rejected the API key.")
    if not response.ok:
        raise GroqError(f"Groq returned HTTP {response.status_code}.")
    try:
        content = response.json()["choices"][0]["message"]["content"]
        plan = json.loads(content)
    except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
        raise GroqError("Groq returned an invalid test-plan JSON response.") from exc
    return validate_plan(plan, snapshot)


def validate_plan(plan: dict, snapshot: dict) -> dict:
    required = {"summary", "questions", "assumptions", "risks", "test_cases"}
    if not isinstance(plan, dict) or not required.issubset(plan):
        raise GroqError("The generated plan is missing required sections.")
    for index, case in enumerate(plan["test_cases"], start=1):
        case.setdefault("id", f"TC-{index:03d}")
        if not case.get("source_refs") and not case.get("assumption_refs"):
            raise GroqError(f"Test case {case['id']} has no traceability reference.")
        if not case.get("steps") or not case.get("expected_result"):
            raise GroqError(f"Test case {case['id']} is missing steps or an expected result.")
    plan["metadata"] = {
        "source_issue_key": snapshot["source"]["issue_key"],
        "source_updated_at": snapshot["source"].get("updated_at"),
        "generator_version": "1.0.0",
        "generation_status": "draft",
    }
    return plan