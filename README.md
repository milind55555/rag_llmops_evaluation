# RAG Evaluation & LLMOps Pipeline

A portfolio-ready starter project demonstrating how to build a Retrieval-Augmented Generation (RAG) application and measure whether it works. It includes a small document corpus, a deterministic local demo, a golden evaluation set, CI regression gates, optional RAGAS evaluation, tracing hooks, and a cost/latency/quality dashboard.

> **Important:** The included local demo is intentionally deterministic so it runs without API keys and is suitable for demonstrating evaluation mechanics. It is not a production-grade semantic retriever or a claim of measured model quality. Connect a real embedding model and LLM before reporting real-world RAGAS scores.

## Features

- RAG pipeline with chunking, lexical retrieval, context-grounded response generation, and source references
- Golden test set with expected answer facts and relevant document IDs
- Automated evaluation for answer relevance, context precision/recall proxies, and groundedness
- CI gate that fails when metrics fall below configured thresholds
- Optional RAGAS adapter for model-based evaluation
- OpenTelemetry-compatible tracing hooks (optional) and local JSONL traces
- Streamlit dashboard for quality, latency, token estimates, and cost estimates
- Dockerfile and GitHub Actions workflow

## Architecture

```text
Documents -> Chunking -> Retriever -> Context -> Generator -> Answer + Sources
                                  |                       |
                                  +---- Trace / Metrics --+
                                                            |
Golden dataset -> Eval runner -> Threshold gate -> GitHub Actions CI
                                                            |
                                                  JSONL metrics -> Dashboard
```

## Quick start (Python 3.11 recommended)

```bash
python -m venv .venv
# Windows PowerShell:
.venv\\Scripts\\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python -m ragapp.ingest
python -m ragapp.cli "How do I rotate an API key?"
python -m ragapp.evaluate
streamlit run dashboard.py
```

The baseline evaluation is offline and deterministic. It should pass in a clean checkout. CI runs the same command and blocks regressions.

## Optional RAGAS evaluation

Install the optional dependencies:

```bash
pip install -r requirements-ragas.txt
```

Set up your provider credentials and model integration before enabling RAGAS. See `ragapp/ragas_eval.py` for the adapter entry point. Do not commit API keys.

## Tracing

By default, request traces are written to `artifacts/traces.jsonl`. To export spans with OpenTelemetry, install `requirements-otel.txt` and set `OTEL_EXPORTER_OTLP_ENDPOINT` to your collector endpoint. Keep secrets in GitHub Actions secrets or environment variables.

## Dashboard

```bash
streamlit run dashboard.py
```

The dashboard reads `artifacts/evaluation_results.json` and `artifacts/traces.jsonl`. Run the evaluation and send a few CLI queries first to populate these files.

## CI quality gate

The GitHub Actions workflow runs tests and evaluation on pushes and pull requests. Thresholds are configured in `config/eval_thresholds.json`. A regression exits with a non-zero code and blocks the workflow.

## Repository layout

```text
rag-llmops-evaluation/
├── .github/workflows/ci.yml
├── config/
├── data/
├── ragapp/
├── tests/
├── artifacts/
├── dashboard.py
├── Dockerfile
├── requirements.txt
└── README.md
```

## Resume bullets (edit to reflect what you actually run)

- Built a RAG evaluation and LLMOps starter platform with a golden QA set, automated regression gates, retrieval/groundedness metrics, and source attribution.
- Integrated CI evaluation with GitHub Actions so changes fail the pipeline when configured quality thresholds are missed.
- Added request tracing and a Streamlit dashboard for latency, estimated token usage, cost, and evaluation quality.

**Be honest in interviews:** describe the provided evaluation as a deterministic baseline until you have connected a real LLM/embedding stack and generated real benchmark results.
