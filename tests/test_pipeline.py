from ragapp.pipeline import retrieve, generate_answer

def test_retrieval_finds_api_key_document():
    docs = [{"doc_id": "api_key_management", "text": "Rotate API key by creating a replacement key."},
            {"doc_id": "deployment_health", "text": "Monitor deployment latency and error rate."}]
    results = retrieve("How to rotate API key?", docs=docs, top_k=1)
    assert results
    assert results[0]["doc_id"] == "api_key_management"

def test_generation_returns_source_ids():
    answer, sources = generate_answer("question", [{"doc_id": "doc1", "text": "# title\nA useful sentence."}])
    assert "A useful sentence" in answer
    assert sources == ["doc1"]

def test_empty_context_is_safe():
    answer, sources = generate_answer("question", [])
    assert "could not find enough information" in answer
    assert sources == []
