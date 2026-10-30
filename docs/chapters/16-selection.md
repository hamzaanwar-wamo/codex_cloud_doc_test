# 16. Architecture selection and decision rules

![A practical architecture decision tree](../diagrams/16-selection.png)

## Choose from query evidence, not hype
| Need | First candidate | Escalate when |
|---|---|---|
| Known document/section/version | Exact lookup | User gives vague or ambiguous identifiers |
| Rare terms, codes, legal clauses | BM25 + exact fields | Paraphrase failures dominate |
| Semantic paraphrases | Dense baseline | Exact terms or domain misses remain |
| Mixed enterprise search | Hybrid + reranking | Multi-hop coverage remains weak |
| Explicit relation chains | Graph + passage evidence | Entities/edges cannot be extracted reliably |
| Structure-rich document navigation | Hierarchical/vectorless | Heading/summary gating misses answers |
| Variable multi-document investigation | Bounded agent over tested tools | Added calls do not improve task success |
| Exact totals/live records | Governed SQL/API | Unstructured discovery needed before querying |
| Small known authorized source set | Long-context comparison | Token cost or evidence use becomes unreliable |

## Architectural comparison
Vector search precomputes semantic representations; BM25 precomputes lexical postings; graph search precomputes relationships; vectorless trees precompute hierarchy; agents decide how to call these at runtime. These axes are not mutually exclusive. “Graph vs vector” can be the wrong question when the desired system uses graph traversal to select entities and vector search to fetch supporting passages.

Keep a baseline and ablate additions. Compare answer quality, source coverage, P95 latency, per-task cost, freshness and incident complexity. Use query slices: exact identifiers, paraphrases, temporal, multi-hop, unanswerable and restrictive access. A system can improve global averages while regressing badly for a high-risk slice.

Do not select architecture from a single demonstration. A clean question with an obvious answer tells little about noisy OCR, conflicting versions or revoked permissions. Benchmark the same source versions, user scopes and questions across candidates.

## A worked choice
Start the enterprise platform with canonical ingestion, lexical/dense baselines and shared access controls. Adopt hybrid if the union improves recall and final evidence. Add parent expansion if exceptions are split. Add graph extraction for B-like relationship questions only after showing useful path coverage. Add an agent when the needed search steps vary and a fixed graph/hybrid workflow cannot handle that variation well.

**Interview answer:** “I can explain which failure each component fixes and which metric proves the improvement. If I cannot name the failure and measurement, I probably do not need the component yet.”

**Follow-up:** “What would make you remove the graph?” **Response:** “Poor relation quality, expensive updates, or no meaningful improvement over hybrid on the target relationship slice. I retain proven exact/lexical/vector paths and simplify.”
