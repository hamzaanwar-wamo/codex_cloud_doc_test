# The Complete RAG Engineering Handbook

A detailed visual guide in simple language, from fundamentals to production architecture and senior interview preparation.

- [Read the handbook](docs/RAG_Interview_Handbook.md)
- [Download PDF](docs/RAG_Interview_Handbook.pdf)
- [Download editable Word document](docs/RAG_Interview_Handbook.docx)
- [Browse the 34 chapter sources](docs/chapters)
- [Browse diagrams and editable sources](docs/diagrams)
- [Run the offline retrieval lab](examples/rag_lab.py)

The expanded edition includes **34 chapters, 40 rendered figures, 150 interview revision questions**, worked math, five execution walkthroughs and a runnable offline retrieval lab. PDF and Word contain the actual figures, not just diagram code. GitHub Markdown displays the same figures inline.

Topics include parsing/OCR, chunking families, metadata and query rewriting, embeddings and ANN, BM25, hybrid fusion, reranking, vectorless search, GraphRAG traversal/provenance, bounded agents, claim verification, evaluation, production deployment, cost, security, observability and debugging. Each major chapter includes interview answers, follow-ups or design challenges.

Start with Chapters 1–9 for the core pipeline. Continue through architecture choices (10–16), evidence/evaluation (17–23), production/implementation (24–30), and interviews/revision (31–34).

## Sources and limits

Based on the supplied RAG master prompt. The linked shared conversation returned HTTP 403 on both attempts and could not be read. The guide does not claim to reproduce that unseen discussion. Examples, score calculations and capacity/latency budgets are hypothetical, not benchmarks. Architecture code is labeled pseudocode. The runnable lab uses hashed **lexical** vectors and source excerpts; it is not neural semantic search, an LLM app or a deployed production platform.

## Rebuild documents

Python 3.10+ is required, plus Graphviz (`dot`) and DejaVu Sans/Mono fonts. On Debian/Ubuntu, the system packages are `graphviz` and `fonts-dejavu-core`. Install Python packages in your preferred virtual environment:

```sh
python -m pip install -r docs/requirements.txt
python docs/build_handbook.py
```

Edit files in `docs/chapters/`, then rebuild. The combined Markdown, PDF and DOCX are generated artifacts and should not be edited independently. The build reads the same chapter sources for all three formats. The PDF includes a generated page-numbered contents list and bookmarks.

Edit `docs/diagrams/specs.json` for flow/tree/schema diagrams. The builder exports DOT, Mermaid, PNG and SVG. `docs/render_visuals.py` draws the sequence and quantitative figures; the sequence also has Mermaid source, and charts have JSON data. These exports are regenerated during the build.

## Run and test the offline lab

No extra packages or network access are required for the lab:

```sh
python examples/rag_lab.py --question "unused leave carry forward" --group employees-pk
python examples/rag_lab.py --question "carry forward" --date 2026-06-01
python -m unittest discover -s examples -p 'test_*.py' -v
```

Tests cover ranking math, scope isolation, permission denial, temporal selection, required-source retrieval, empty queries and metric calculations. Passing these tests validates the teaching lab, not external production services.
