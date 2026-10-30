# 12. Vectorless RAG: retrieval without dense embeddings

![Exact, lexical and hierarchical routes without a vector index](../diagrams/12-vectorless.png)

## What replaces embeddings
Vectorless RAG can use exact metadata lookup, BM25, document trees, rule-based routing or LLM navigation. It is not “search without an index.” A tree is a navigation structure; an inverted index is a lexical retrieval structure. These can coexist and still feed grounded generation.

Ingest: Parse structure and preserve heading paths -> build document/section/chunk records -> create lexical and exact-field indexes -> link tree parents -> retain page evidence and access metadata -> validate/publish. Persist JSON hierarchy and original text. Runtime: authenticate -> classify exact versus exploratory intent -> lookup/search -> navigate or expand -> verify source evidence -> generate/cite. Deploy an API and ingestion workers with object/relational/lexical stores; no dense service is required.

## How the right document is found
For C, use keyword fields `(doc_id=HR-42, version=3, section=7)` under tenant scope. No LLM selection is needed. For A, BM25 retrieves carry-forward passages or first ranks documents by title/body, then searches their sections. Query rewriting can add “unused annual leave,” but generated synonyms are not evidence.

A document-level index uses whole-document length and term statistics. A chunk-level index scores local passages. In two-stage document -> chunk search, measure document-gate recall: a missed document cannot be recovered by its unsearched children. A mixed strategy can merge direct chunk hits with hierarchical candidates.

## LLM tree navigation
Store nodes with heading, summary, children and source spans. A model selects likely branches, reads children and repeats until reaching evidence. This can work for structure-rich documents and preserve organizational context. It can fail on misleading headings or incomplete summaries. Each navigation step adds model latency; bound branches, depth and total spend. Keep summaries distinct from original evidence and validate final claims against leaf sources.

Example tree record: `{"id":"hr42:v3:s7","title":"Carry forward","parent":"hr42:v3","children":["s7:c1","s7:c2"],"source_pages":[8]}`. Source/tenant/version fields remain mandatory even when omitted from this short example.

**Interview answer:** “Vectorless systems retrieve through exact fields, lexical postings or hierarchy. They can be better for known IDs and structured policies, but semantic paraphrases may need expansion or another route.”

**Follow-up:** “Is vectorless always cheaper?” **Response:** “No. Avoiding embeddings saves one cost, but repeated LLM navigation can cost more than vector search. I compare end-to-end latency and answer quality, not one component.”
