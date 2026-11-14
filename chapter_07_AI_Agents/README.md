# Jira Test Plan Studio

This is the Phase 1-4 BLAST implementation for the Jira-to-test-plan workflow.

## Run locally

```powershell
cd chapter_07_AI_Agents
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local URL printed by Streamlit, configure Jira and Groq in Settings, then enter a request containing a Jira key, for example:

`Fetch PROJ-123 and create a test plan with negative and boundary coverage.`

Credentials can be loaded from `.env` using `.env.example` as a template or entered through the Settings page. Local `config.json` and `.env` are git-ignored. The app performs read-only Jira calls and labels every result as a draft plan; it does not execute tests or write back to Jira.