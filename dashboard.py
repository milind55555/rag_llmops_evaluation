"""Streamlit dashboard for evaluation quality and request telemetry."""
from pathlib import Path
import json
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
EVAL_FILE = ROOT / "artifacts" / "evaluation_results.json"
TRACE_FILE = ROOT / "artifacts" / "traces.jsonl"

st.set_page_config(page_title="RAG LLMOps Dashboard", layout="wide")
st.title("RAG Evaluation & LLMOps")
st.caption("Offline demo telemetry. Cost is zero because no paid model API is called.")

if EVAL_FILE.exists():
    report = json.loads(EVAL_FILE.read_text(encoding="utf-8"))
    metrics = report.get("metrics", {})
    cols = st.columns(4)
    cols[0].metric("Answer relevance", metrics.get("answer_relevance", "—"))
    cols[1].metric("Context recall", metrics.get("context_recall", "—"))
    cols[2].metric("Groundedness", metrics.get("groundedness", "—"))
    cols[3].metric("Avg latency (ms)", metrics.get("latency_ms", "—"))
    st.subheader("Golden-set cases")
    st.dataframe(pd.DataFrame(report.get("cases", [])), use_container_width=True)
else:
    st.info("No evaluation report yet. Run `python -m ragapp.evaluate`.")

st.subheader("Request traces")
if TRACE_FILE.exists():
    events = []
    for line in TRACE_FILE.read_text(encoding="utf-8").splitlines():
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    if events:
        df = pd.DataFrame(events)
        a, b, c = st.columns(3)
        a.metric("Requests traced", len(df))
        b.metric("Mean latency (ms)", round(df["latency_ms"].mean(), 2))
        c.metric("Estimated cost (USD)", round(df["estimated_cost_usd"].sum(), 6))
        st.line_chart(df[["latency_ms"]].reset_index(drop=True))
        st.dataframe(df, use_container_width=True)
    else:
        st.caption("Trace file is empty.")
else:
    st.caption("No traces yet. Ask a question with `python -m ragapp.cli \"your question\"`.")
