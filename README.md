# ScamShield — Online Scam Awareness Wiki

Educational project. Six summarized source documents are in `wiki/`; each contains its source URL. Verify facts against official sources before publication.

## Actual ingest and retrieval

Requires Python 3.9+; no external packages or API key:

```bash
python3 ingest.py
python3 retrieve.py "如何辨識釣魚郵件？"
```

The first command creates `index.json` from the source documents. The second performs TF-IDF cosine similarity retrieval and prints supporting source chunks. This is a real local **ingest + retrieval** pipeline, **not** an LLM by itself. An LLM must consume retrieved chunks to generate slide text, and its output must be reviewed and logged before claiming a complete LLM Wiki workflow.

See `workflow/graph.md` and `workflow/execution_log.md`.
