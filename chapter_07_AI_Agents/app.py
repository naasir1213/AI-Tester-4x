import json
import re

import streamlit as st

from config_store import load_config
from groq_client import GroqError, generate_plan
from jira_client import JiraError, extract_issue_key, fetch_issue


st.set_page_config(page_title="Jira Test Plan Studio", page_icon="JT", layout="wide")

st.markdown(
    """
    <style>
    .stApp { background: #f4f0e8; color: #1d2926; }
    [data-testid="stSidebar"] { background: #1d2926; }
    [data-testid="stSidebar"] * { color: #f4f0e8 !important; }
    .eyebrow { color: #ad4b31; font-size: .78rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; }
    h1 { font-family: Georgia, serif; font-size: 3.2rem !important; letter-spacing: 0 !important; }
    .lede { color: #52625d; font-size: 1.08rem; max-width: 700px; }
    .step { border-top: 3px solid #d7c9b2; padding-top: .7rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

config = load_config()
st.sidebar.markdown("## Jira Test Plan Studio")
st.sidebar.caption("BLAST workflow: retrieve, reason, validate")
st.sidebar.markdown("---")
st.sidebar.markdown("**Jira**  " + ("Connected" if config["jira_url"] and config["jira_api_token"] else "Needs setup"))
st.sidebar.markdown("**Groq**  " + ("Ready" if config["groq_api_key"] else "Needs setup"))
st.sidebar.markdown("[Open Settings](./settings)")

st.markdown('<div class="eyebrow">Phase 4 / Delivery</div>', unsafe_allow_html=True)
st.title("Turn a Jira issue into a test plan.")
st.markdown(
    '<p class="lede">Describe what you need in plain language. The studio retrieves the Jira source, sends only the normalized requirement to Groq, and keeps assumptions visible.</p>',
    unsafe_allow_html=True,
)

prompt = st.text_area(
    "Request",
    placeholder='Fetch PROJ-123 from Jira and create a test plan with negative and boundary coverage.',
    height=120,
    label_visibility="collapsed",
)
run = st.button("Generate test plan", type="primary", use_container_width=False)

if run:
    if not prompt.strip():
        st.warning("Enter a request containing a Jira issue key, such as PROJ-123.")
    else:
        issue_key = extract_issue_key(prompt)
        if not issue_key:
            st.error("I could not find a Jira issue key. Include a key like PROJ-123 in your request.")
        else:
            try:
                with st.status(f"Working on {issue_key}...", expanded=True) as status:
                    st.write("Fetching the approved Jira fields")
                    snapshot = fetch_issue(config, issue_key)
                    st.write("Generating a traceable draft with Groq")
                    plan = generate_plan(config, snapshot, prompt)
                    status.update(label=f"Draft ready for {issue_key}", state="complete", expanded=False)

                issue = snapshot["issue"]
                st.markdown(f'<div class="eyebrow">{issue_key} / Draft plan</div>', unsafe_allow_html=True)
                st.header(issue.get("summary") or "Untitled Jira issue")
                st.caption(f"Source updated: {snapshot['source'].get('updated_at') or 'not provided'}")
                st.markdown(plan.get("summary", ""))
                col1, col2, col3 = st.columns(3)
                col1.metric("Test cases", len(plan.get("test_cases", [])))
                col2.metric("Questions", len(plan.get("questions", [])))
                col3.metric("Risks", len(plan.get("risks", [])))

                for case in plan.get("test_cases", []):
                    with st.expander(f"{case.get('id', 'TC')}  |  {case.get('title', 'Untitled')}"):
                        st.caption(f"{case.get('type', 'coverage')} / {case.get('priority', 'medium')} priority")
                        if case.get("preconditions"):
                            st.markdown("**Preconditions**\n\n" + "\n".join(f"- {item}" for item in case["preconditions"]))
                        st.markdown("**Steps**")
                        for step in case.get("steps", []):
                            st.markdown(f"{step.get('step', '')}. {step.get('action', '')}  \nExpected: {step.get('expected_result', '')}")
                        st.caption("Trace: " + ", ".join(case.get("source_refs", []) + case.get("assumption_refs", [])))

                if plan.get("questions") or plan.get("assumptions"):
                    st.markdown("### Review before execution")
                    if plan.get("questions"):
                        st.markdown("**Questions**\n\n" + "\n".join(f"- {item}" for item in plan["questions"]))
                    if plan.get("assumptions"):
                        st.markdown("**Assumptions**\n\n" + "\n".join(f"- {item}" for item in plan["assumptions"]))
                st.download_button("Download JSON", json.dumps(plan, indent=2), f"{issue_key}-test-plan.json", "application/json")
            except (JiraError, GroqError) as exc:
                st.error(str(exc))
            except Exception:
                st.error("The workflow failed unexpectedly. Check the configured connections and application logs.")

st.markdown("---")
st.markdown('<div class="step"><strong>Source first.</strong> Jira facts stay separate from model suggestions. Every generated case must retain traceability.</div>', unsafe_allow_html=True)