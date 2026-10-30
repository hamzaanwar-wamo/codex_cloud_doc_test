# 29. Implementation blueprint and runnable offline lab

![The runnable teaching slice and the production adapters it deliberately omits](../diagrams/29-implementation.png)

## Repository layout
```text
docs/chapters/           editable chapter sources
docs/diagrams/           PNG/SVG plus DOT/Mermaid source and specs
docs/build_handbook.py   build Markdown, PDF and Word from chapters
examples/rag_lab.py      runnable standard-library retrieval exercise
examples/test_rag_lab.py tests for ranking, access and evidence behaviour
```

The lab is a deterministic, offline learning system. It implements tokenization, BM25, hashed term-vector cosine search, RRF, scoped version/date filtering, source-backed extractive output and a small retrieval evaluation. Hashed lexical vectors are not semantic neural embeddings. Extractive output is not LLM generation, and selected excerpts are not an entailment proof. The lab exists to inspect intermediate data without requiring credentials or paid models.

From the repository root:
```sh
python examples/rag_lab.py --question "unused leave carry forward" --group employees-pk
python -m unittest discover -s examples -p 'test_*.py' -v
```
The command prints query scope, lexical/vector ranks, fused ranks, authorized evidence and evaluation results. Review the two source versions and another-tenant record in the synthetic corpus. Changing group/date demonstrates why relevance and applicability differ. Run the command with `--date 2026-06-01` to inspect historical policy selection.

## Production project design
A production application can split into API, ingestion, retrieval, evidence, agent, storage and observability modules. Define typed request/response schemas with FastAPI/Pydantic or equivalents. Integrate real parsing/OCR, object storage, PostgreSQL, lexical/vector stores, optional graph store, reranker and model gateway behind explicit adapters. Enforce permissions in adapters and source fetches, not only orchestration.

Schema relationships: documents 1:N versions; versions 1:N chunks; chunks N:M source-backed graph assertions; query runs 1:N candidate records and claim-verdict records. Keep publication state distinct from index-write success. Store model/pipeline versions so source and output artifacts are reproducible.

```python
# Production architecture pseudocode, not the offline lab.
async def answer(request, identity):
    scope = await authorization.resolve(identity)
    query = understand_preserving_original(request)
    lexical, dense = await parallel_search(query, scope)
    candidates = fuse_and_deduplicate(lexical, dense)
    ranked = await rerank(query, candidates)
    context = await authorized_expand_and_pack(ranked, scope)
    if not enough_applicable_evidence(query, context):
        return abstain("Missing required evidence")
    draft = await generate_grounded(query, context)
    verdict = await verify_claims_and_citations(draft, context)
    return draft if verdict.supported else revise_or_abstain(verdict)
```

## What must be tested beyond the lab
Real ingestion -> published index -> permitted query -> cited answer integration; delete/revoke propagation; source-coordinate citations; model/reranker truncation; graph edge authorization; bounded agents; provider outages; restore and migration. A passing mock or offline lab cannot establish that those external services work. This handbook provides the design and a runnable retrieval slice, not a fully deployed enterprise implementation.

**Interview answer:** “I separate orchestration contracts from provider adapters and test access at every boundary. My small lab teaches ranking; production readiness needs actual integration and fault tests.”
