import streamlit as st

from config_store import load_config, mask_secret, save_config
from groq_client import GroqError, test_connection as test_groq_connection
from jira_client import JiraError, test_connection as test_jira_connection


st.set_page_config(page_title="Settings | Jira Test Plan Studio", page_icon="ST", layout="wide")
st.title("Connection settings")
st.caption("Credentials are stored locally in git-ignored config.json. They are never sent to Groq or included in plans.")

config = load_config()
left, right = st.columns(2, gap="large")

with left:
    st.subheader("Jira")
    jira_url = st.text_input("Jira URL", config.get("jira_url", ""), placeholder="https://your-org.atlassian.net")
    jira_email = st.text_input("Email", config.get("jira_email", ""), placeholder="you@example.com")
    jira_token = st.text_input("API token", config.get("jira_api_token", ""), type="password")
    st.caption("Current token: " + mask_secret(config.get("jira_api_token", "")))
    if st.button("Test Jira connection"):
        try:
            name = test_jira_connection({"jira_url": jira_url, "jira_email": jira_email, "jira_api_token": jira_token})
            st.success(f"Connected as {name}.")
        except JiraError as exc:
            st.error(str(exc))

with right:
    st.subheader("Groq")
    groq_key = st.text_input("API key", config.get("groq_api_key", ""), type="password")
    groq_model = st.text_input("Model", config.get("groq_model", "openai/gpt-oss-120b"))
    st.caption("Current key: " + mask_secret(config.get("groq_api_key", "")))
    if st.button("Test Groq connection"):
        try:
            test_groq_connection({"groq_api_key": groq_key})
            st.success("Groq is reachable and the key was accepted.")
        except GroqError as exc:
            st.error(str(exc))

st.markdown("---")
if st.button("Save settings", type="primary"):
    save_config({"jira_url": jira_url, "jira_email": jira_email, "jira_api_token": jira_token, "groq_api_key": groq_key, "groq_model": groq_model})
    st.success("Settings saved.")