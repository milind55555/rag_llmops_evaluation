"""Validate and index the local markdown corpus into a lightweight JSONL chunk store."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "data" / "docs"
OUT = ROOT / "artifacts" / "chunks.jsonl"

def chunk_text(text: str, max_words: int = 180):
    words = text.split()
    for start in range(0, len(words), max_words):
        yield " ".join(words[start:start + max_words])

def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for path in sorted(DOCS.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        text = re.sub(r"^# .*\\n", "", text)
        for i, chunk in enumerate(chunk_text(text)):
            rows.append({"doc_id": path.stem, "chunk_id": f"{path.stem}-{i}", "text": chunk})
    OUT.write_text("".join(json.dumps(r) + "\\n" for r in rows), encoding="utf-8")
    print(f"Indexed {len(rows)} chunks into {OUT.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
