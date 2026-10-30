# RAG Engineering Interview Handbook

A concise end-to-end RAG guide in simple language, with senior interview questions, practical examples, and production trade-offs.

- [Read the handbook](docs/RAG_Interview_Handbook.md)
- [Download PDF](docs/RAG_Interview_Handbook.pdf)
- [Download editable Word document](docs/RAG_Interview_Handbook.docx)

The handbook covers ingestion, chunking, metadata, embeddings, BM25, hybrid and vectorless retrieval, GraphRAG, agents, evidence verification, evaluation, deployment, security, and interview preparation.

## Sources and limits

Based on the supplied RAG master prompt. The linked shared conversation returned HTTP 403 and could not be read. Examples and capacity budgets are hypothetical. Code is illustrative, not a runnable production platform.

## Rebuild documents

Python 3 with `python-docx` and `reportlab` is required. Run:

```sh
python docs/build_handbook.py
```

Generated Markdown, PDF and DOCX files are written beside the generator.
