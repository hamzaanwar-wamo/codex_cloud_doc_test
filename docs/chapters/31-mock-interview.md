# 31. A 60-minute senior system-design mock

![Interview progression: clarify, design, challenge, measure](../diagrams/31-interview.png)

## Minutes 0-5: clarify
Interviewer: “Design an enterprise knowledge assistant.”

My answer: “I need users, access boundaries, query types, source formats, update rate, citation requirements and expected latency/cost. Are answers advisory or high-risk? Can we abstain? I will assume the hypothetical million-document, 100K-query/day platform, but I will validate chunks and peak traffic before sizing.”

Interruption: “Just use the newest policy.” Response: “Newest upload and currently effective policy can differ. I need explicit authority and temporal rules.”

## Minutes 5-10: estimate
My answer: “Average traffic is 1.16 QPS. I need peak distribution. At assumed 20 QPS and three-second mean, about 60 requests are in flight. If documents average 20 chunks, we have 20M vectors, or 61.44 GB raw at 768 float32 dimensions, excluding indexes/replicas. I sample before using this for provisioning.”

Interruption: “Why not one shard per tenant?” Response: “That simplifies some isolation but may create many tiny shards and overhead. I compare shared scope-enforced indexes with dedicated resources for heavy or regulated tenants.”

## Minutes 10-20: ingestion
My answer: “Connectors capture revisions, workers parse/OCR, preserve structure and provenance, normalize, chunk and enrich. Idempotent jobs write versioned lexical/vector indexes. Validation precedes a manifest switch. Deletion and revocation block access promptly and remove derived artifacts.”

Interruption: “The worker crashes after only vector writes.” Response: “The version remains unpublished. A durable job/reconciler completes or cleans the partial state.”

## Minutes 20-35: query and evidence
My answer: “Resolve access/date, route exact lookups, run lexical/dense in parallel for mixed search, fuse, rerank and pack complementary evidence. Generate with source IDs and verify material claims. Add graph retrieval for explicit relationships and bounded agents only for variable research tasks.”

Interruption: “Reranker confidence is 0.99.” Response: “That does not establish applicable, sufficient evidence or calibrated answer correctness. I check required facts and source validity.”

## Minutes 35-45: evaluation and cost
My answer: “Versioned golden sets include exact-ID, paraphrase, multi-hop, temporal, unanswerable and unauthorized slices. Measure candidate/context recall, support/correctness, citation quality, risk-coverage, latency and cost. Use controlled ablations and held-out thresholds. Inspect actual stage traces before optimizing.”

Interruption: “No labels.” Response: “Start with a privacy-reviewed representative sample and expert edge cases; adjudicate labels. Synthetic questions and model judges can assist, but do not replace calibration.”

## Minutes 45-55: failures and security
My answer: “Apply server-side access across every store/cache/tool/source link. Retrieved instructions are untrusted. Use read-only tools and bounded execution. Timeouts, backpressure, circuit breakers and validated degraded paths protect availability. Trace source IDs and versions safely. Test restore, revocation and index rollback.”

Interruption: “Vector DB is down.” Response: “Use scoped lexical fallback only where evaluated; otherwise explain missing evidence. Never claim the same coverage silently.”

## Minutes 55-60: decision and trade-offs
My answer: “My initial candidate is permission-aware hybrid RAG with versioned ingestion and evidence checks. The key risks are parsing quality, exact/semantic coverage, missing exceptions and access consistency. Graphs/agents are additions justified by target-slice gains. I would first validate source parsing, labeled retrieval and authorization before expanding scope.”
