# 28. Debugging: symptom to cause to prevention

![Follow the evidence through stage boundaries before changing parameters](../diagrams/28-debugging.png)

Use a failing query with its identity, requested time and corpus version. Find the expected source. Ask where it first disappears or becomes corrupted: source -> parser -> chunk -> index -> candidate -> rank -> context -> claim. Change the failing stage, not every parameter at once.

| Symptom | Likely causes and diagnostic check | Fix / prevention |
|---|---|---|
| Wrong document | Query rewrite changed meaning; analyzer lost ID; filter overrestricted | Preserve original query; exact fields; test route/filter recall |
| Right document, wrong chunk | Broken reading order, poor boundaries, truncated text | Inspect source/parse/chunk spans; structure-aware splitting; parent expansion |
| High reranker score, weak evidence | Topical relevance without eligibility/date/authority | Separate applicability and sufficiency checks; calibrated answerability |
| Hallucinated explanation | Generator added unstated rationale | Claim checks; source-only factual contract; abstain on missing rationale |
| Conflicting versions | Active alias mismatch; effective date confused with upload date | Version manifest; explicit temporal semantics; contradiction tests |
| DB outage | Dependency failure or timeout | Tested scoped fallback; circuit breaker; fail clearly if evidence unavailable |
| Graph explosion | Broad relation patterns or high-degree nodes | Bound hops/types/fan-out/time; inspect eligible path counts |
| Infinite agent loop | No gap state or no-progress detection | Budget/deadline/repeated-result stopping; bounded recovery tests |
| ACL leakage | Post-filter too late; parent/cache/graph path omitted checks | Stop affected path; invalidate caches; audit; enforce every hop |
| Embedding migration regression | Query and index model mismatch or truncation changed | Versioned namespaces; exact baseline; shadow evaluation and rollback |
| Index corruption/orphans | Partial writes, failed publication, mismatched stores | Reconcile IDs/manifests; rebuild from source; restore drill |
| Latency spike | Queue wait, provider throttle, large K/context, hot shard | Trace critical path; cap work; scale measured bottleneck |
| Cost spike | Long outputs, duplicate retries, unbounded agents | Per-task usage budgets; no-progress stop; regression gates |
| OCR numbers wrong | Bad scan, column order or character confusion | Inspect original region; OCR quality checks; review high-risk values |
| Stale answers | Cache missing version/date key; delayed ingestion | Version-aware invalidation; source-change-to-searchable metrics |

## Two deeper examples
Recall appears high, answer misses contractor exclusion: Check what relevance labels mean. A “related leave passage” label can hide fact incompleteness. Label required facts, inspect packed context and reranker truncation, then preserve the exception passage.

Tenant filter produces no vector hits: Check whether search globally retrieved a small K and only then discarded unauthorized records. Increasing global K may hide the design flaw. Use tested filter-aware retrieval or exact search on the small eligible subset.

**Interview answer:** “I debug by tracing one expected fact through the pipeline. I distinguish missing source, missing retrieval, lost context and unsupported generation.”

**Follow-up:** “Would a larger model fix it?” **Response:** “Not if the source is absent, corrupt or unauthorized. Better reasoning cannot recover an excluded fact safely.”
