"""Small offline RAG pipeline. Swap lexical retrieval/generation for production models as needed."""
from pathlib import Path
import json
import re
import time
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "data" / "docs"
TRACE_FILE = ROOT / "artifacts" / "traces.jsonl"

def load_documents():
    docs = []
    for path in sorted(DOCS.glob("*.md")):
        body = path.read_text(encoding="utf-8")
        docs.append({"doc_id": path.stem, "text": body})
    return docs

def tokens(text):
    return re.findall(r"[a-z0-9]+", text.lower())

def retrieve(question, docs=None, top_k=2):
    docs = docs if docs is not None else load_documents()
    q = Counter(tokens(question))
    ranked = []
    for doc in docs:
        d = Counter(tokens(doc["text"]))
        score = sum(min(count, d[t]) for t, count in q.items())
        ranked.append((score, doc))
    ranked.sort(key=lambda x: (-x[0], x[1]["doc_id"]))
    return [doc for score, doc in ranked[:top_k] if score > 0]

def generate_answer(question, contexts):
    """Deterministic extractive response for evaluation plumbing; not an LLM."""
    if not contexts:
        return "I could not find enough information in the supplied documents.", []
    snippets = []
    for doc in contexts:
        lines = [line.strip() for line in doc["text"].splitlines() if line.strip() and not line.startswith("#")]
        snippets.extend(lines)
    answer = " ".join(snippets[:3])
    return answer, [d["doc_id"] for d in contexts]

def log_trace(question, answer, source_ids, latency_ms):
    TRACE_FILE.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "timestamp": time.time(),
        "question": question,
        "answer_preview": answer[:240],
        "source_ids": source_ids,
        "latency_ms": round(latency_ms, 2),
        "input_tokens_est": max(1, len(tokens(question))),
        "output_tokens_est": max(1, len(tokens(answer))),
        "estimated_cost_usd": 0.0,
        "provider": "offline-demo"
    }
    with TRACE_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\\n")

def answer(question):
    start = time.perf_counter()
    contexts = retrieve(question)
    response, source_ids = generate_answer(question, contexts)
    latency_ms = (time.perf_counter() - start) * 1000
    log_trace(question, response, source_ids, latency_ms)
    return {"question": question, "answer": response, "sources": source_ids, "latency_ms": latency_ms}
