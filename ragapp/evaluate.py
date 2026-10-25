"""Golden-set evaluation with simple deterministic metrics and a CI regression gate."""
from pathlib import Path
import json
import re
import sys
from .pipeline import answer, retrieve, tokens

ROOT = Path(__file__).resolve().parents[1]
GOLDEN = ROOT / "data" / "golden_set.json"
THRESHOLDS = ROOT / "config" / "eval_thresholds.json"
OUT = ROOT / "artifacts" / "evaluation_results.json"

def overlap_ratio(needles, haystack):
    text = haystack.lower()
    if not needles:
        return 1.0
    return sum(1 for needle in needles if needle.lower() in text) / len(needles)

def evaluate_case(case):
    retrieved = retrieve(case["question"], top_k=2)
    result = answer(case["question"])
    retrieved_ids = {d["doc_id"] for d in retrieved}
    relevant = set(case["relevant_doc_ids"])
    context_recall = len(retrieved_ids & relevant) / len(relevant) if relevant else 1.0
    context_precision = len(retrieved_ids & relevant) / len(retrieved_ids) if retrieved_ids else 0.0
    answer_relevance = overlap_ratio(tokens(case["question"]), result["answer"])
    groundedness = overlap_ratio(case["expected_facts"], result["answer"])
    return {
        "id": case["id"],
        "question": case["question"],
        "answer": result["answer"],
        "sources": result["sources"],
        "answer_relevance": round(answer_relevance, 3),
        "context_recall": round(context_recall, 3),
        "context_precision": round(context_precision, 3),
        "groundedness": round(groundedness, 3),
        "latency_ms": round(result["latency_ms"], 2)
    }

def main():
    cases = json.loads(GOLDEN.read_text(encoding="utf-8"))
    thresholds = json.loads(THRESHOLDS.read_text(encoding="utf-8"))
    rows = [evaluate_case(case) for case in cases]
    metrics = {
        key: round(sum(row[key] for row in rows) / max(1, len(rows)), 3)
        for key in ["answer_relevance", "context_recall", "context_precision", "groundedness", "latency_ms"]
    }
    # Offline demo uses a 0 USD cost estimate because no external model API is called.
    report = {"mode": "offline-deterministic-demo", "case_count": len(rows), "metrics": metrics, "cases": rows}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    failures = []
    for metric, threshold in thresholds.items():
        if metric in metrics and metric.startswith("max_"):
            metric_name = metric[4:]
            if metrics.get(metric_name, 0) > threshold:
                failures.append(f"{metric_name}={metrics[metric_name]} exceeds {threshold}")
        elif metric in metrics and metrics[metric] < threshold:
            failures.append(f"{metric}={metrics[metric]} is below {threshold}")
    if failures:
        print("\\nEVALUATION GATE FAILED:")
        for failure in failures:
            print(f"- {failure}")
        sys.exit(1)
    print("\\nEVALUATION GATE PASSED")

if __name__ == "__main__":
    main()
