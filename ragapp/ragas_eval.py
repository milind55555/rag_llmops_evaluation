"""Optional RAGAS integration scaffold.

Use a real LLM/embedding provider and build a RAGAS Dataset before invoking metrics.
Kept separate from the offline CI gate so the repository works without API credentials.
See https://docs.ragas.io/ for the API matching your installed RAGAS version.
"""
def main():
    raise SystemExit(
        "RAGAS scaffold only: connect a real LLM/embedding provider, map golden-set "
        "questions/answers/contexts/reference answers to the RAGAS dataset schema, "
        "then run version-appropriate metrics. The offline gate is `python -m ragapp.evaluate`."
    )

if __name__ == "__main__":
    main()
