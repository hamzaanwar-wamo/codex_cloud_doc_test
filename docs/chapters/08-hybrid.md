# 8. Hybrid retrieval, rank fusion and candidate coverage

![Parallel retrieval, rank fusion and a shared evidence path](../diagrams/08-hybrid.png)

## Full data movement
Ingestion builds lexical and dense representations from version-aligned chunks. Persist identical stable IDs, tenant, permissions and source version in both indexes. Runtime resolves scope once, sends lexical and vector searches in parallel with enforced filters, fuses results, removes duplicate IDs/spans, reranks, expands authorized parents and packs evidence.

Hybrid helps when errors differ: exact policy code in BM25, paraphrased meaning in dense search. It is not guaranteed better. A noisy branch can add irrelevant candidates, and fusion may bury a rare correct result. Evaluate union recall and final ranking separately.

## RRF worked example
Reciprocal rank fusion: RRF(d)=sum_j w_j/(c+rank_j(d)). Missing results contribute zero. Rank starts at 1. With equal weights and illustrative c=60:

| Candidate | BM25 rank | Dense rank | RRF score |
|---|---|---|---|
| A | 1 | 3 | 1/61 + 1/63 = 0.03227 |
| B | 2 | 1 | 1/62 + 1/61 = 0.03252 |
| C | 3 | absent | 1/63 = 0.01587 |
| D | absent | 2 | 1/62 = 0.01613 |

Fused order is B,A,D,C. RRF uses ranks so a BM25 score of 12 is not compared directly to cosine 0.8. c controls how strongly top-rank differences matter. Choose it on validation data; it is not a confidence threshold.

Weighted score fusion can work if normalization and calibration are appropriate. Min-max scores within a tiny result list can be unstable. Calibrated relevance probabilities require labels and drift monitoring. Do not interpret an arbitrary blend as answer certainty.

## Following the candidates
Illustrative plan: lexical top 40 + dense top 40 -> 55 unique IDs -> rerank -> 6 useful passages -> expand two parents -> trim overlaps -> final context. These are tunable experiment values. Track a relevant chunk through every stage. If it disappears before generation, identify the exact stage rather than only checking the final answer.

Parallel wall time is approximately the slower retrieval branch plus overhead, subject to shared resource contention. Set branch deadlines. If one branch fails, use the other only under a tested degraded-mode policy; do not silently claim full retrieval coverage.

**Stored:** Both indexes, shared chunk IDs and model/analyzer versions. **Runtime:** Access scope, candidate lists, fusion and reranking. **Audit:** Search parameters, source IDs and rank transitions, without unnecessary sensitive text.

**Interview answer:** “I use hybrid when keyword and semantic queries coexist. I measure candidate recall before reranking and final evidence quality afterward. More candidates are useful only when they add missing relevant evidence.”

**Follow-up:** “Why not add raw scores?” **Response:** “They have different units and distributions. RRF avoids that comparison. Score fusion needs a deliberately validated normalization or calibration strategy.”
