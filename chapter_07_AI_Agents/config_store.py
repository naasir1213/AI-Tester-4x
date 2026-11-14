import json
import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).parent
CONFIG_PATH = BASE_DIR / "config.json"

DEFAULTS = {
    "jira_url": "",
    "jira_email": "",
    "jira_api_token": "",
    "groq_api_key": "",
    "groq_model": "openai/gpt-oss-120b",
}


def load_config() -> dict:
    load_dotenv(BASE_DIR / ".env")
    config = {}
    if CONFIG_PATH.exists():
        try:
            config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            config = {}

    env_map = {
        "jira_url": "JIRA_URL",
        "jira_email": "JIRA_EMAIL",
        "jira_api_token": "JIRA_API_TOKEN",
        "groq_api_key": "GROQ_API_KEY",
        "groq_model": "GROQ_MODEL",
    }
    for key, env_name in env_map.items():
        if not config.get(key):
            config[key] = os.getenv(env_name, DEFAULTS[key])
    return {**DEFAULTS, **config}


def save_config(config: dict) -> None:
    safe_config = {key: str(config.get(key, "")).strip() for key in DEFAULTS}
    CONFIG_PATH.write_text(json.dumps(safe_config, indent=2), encoding="utf-8")


def mask_secret(value: str) -> str:
    if not value:
        return "Not configured"
    return f"{value[:4]}...{value[-4:]}" if len(value) > 8 else "Configured"