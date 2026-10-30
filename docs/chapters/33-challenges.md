# 33. Architecture challenges and design responses

![Challenge handling: identify constraint, change one layer, prove the result](../diagrams/33-challenges.png)

## 1. Ten million documents
Estimate chunks, bytes, update rate, shard distribution and rebuild time. Separate storage from serving capacity; benchmark filtered search. Use incremental ingestion, partition only where justified, batch background work and test backup/restore. Failure to prepare temporary rebuild capacity can block safe model migrations.

## 2. Healthcare knowledge assistant
Use approved, applicable sources with strict access and audit. Identify patient/clinical scope explicitly, protect PII and define escalation for uncertainty. Evaluate contraindication, temporal and unanswerable cases. Do not interpret retrieval similarity as medical confidence or claim that RAG makes autonomous clinical use safe.

## 3. Financial tables
Preserve headers, units, currencies and periods. Use layout-aware parsing and deterministic calculations or governed SQL. Cite cells/rows and assumptions. Validate that a number belongs to the requested entity and accounting period; matching digits alone is insufficient.

## 4. Multi-tenant enterprise
Derive scope from authenticated identity. Test every retrieval/graph/parent/cache/source-link path. Choose shared indexes versus dedicated resources based on isolation, scale and cost. Revalidate cache hits and propagate revocation promptly. Test near-identical cross-tenant records to expose accidental scope leakage.

## 5. Graph multi-hop
Define ontology and canonical IDs first. Store independent source assertions for edges. Restrict relation types/hops, fetch evidence for every join, and compare complete-path coverage against hybrid. Bad entity resolution can make a beautifully connected graph incorrect.

## 6. Low-latency agentic RAG
Keep simple questions on a deterministic route. Parallelize independent tool reads, cap calls/results, checkpoint progress and stop on no progress. Compare task success and P95/cost against a fixed workflow. If deadlines prevent sufficient research, return supported partial findings with gaps.

## 7. Vector-to-hybrid migration
Build a version-aligned lexical index, shadow queries and compare exact-ID/paraphrase slices. Tune fusion/reranking, test ACL/delete parity, canary and retain rollback. Do not copy arbitrary score weights from another corpus.

## 8. Low recall
Confirm relevant source exists and parsing is correct. Check restrictive filters, analyzer/tokenizer, chunk boundaries, embedding domain fit, truncation and ANN loss against exact search. Increase K only if the relevant source ranks just below cutoff and added work is justified. A corrupted source needs ingestion repair.

## 9. Forty-percent cost reduction
Set a measured baseline per successful task. Inspect model tokens, retrieval/rerank depth, agent retries and infrastructure. Test route simplification, context deduplication, safe caching and model tiering. Maintain critical quality and access gates. Report the observed reduction with uncertainty, not the target as an achievement.

## 10. Evaluation without golden data
Build a small representative expert-labeled set, add high-risk negatives, adjudicate ambiguity and version sources. Use judge-assisted labeling and production signals as supplements. Expand slices according to observed failure/uncertainty. Avoid declaring readiness from synthetic easy questions only.

**Interview pattern:** State constraints -> draw the changed data path -> name the failure mode -> define evidence of success -> describe rollback. The answer is stronger when it admits what remains unmeasured.
