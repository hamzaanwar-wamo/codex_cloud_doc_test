# 9. Reranking, diversity and context packing

![Candidate retrieval and final context are different selection stages](../diagrams/09-reranking.png)

## Top-K is not top-N
K is how many candidates retrieval exposes to later stages. N is how many passages survive selection for evidence/context. Bigger K may improve recall but increases reranking work. Bigger N can increase coverage but also token cost and distraction. Neither should be selected by repeating a fashionable default.

A bi-encoder compares separately precomputed representations. A cross-encoder jointly reads query and candidate, allowing detailed token interactions at runtime. That is why it is often more expensive per candidate and useful after search. It cannot recover a passage retrieval never returned. Truncation inside the reranker can hide a late sentence even if the stored chunk is complete.

ColBERT-style late interaction separately encodes token vectors and aggregates token matches at query time. It is neither a single-vector embedding lookup nor a normal full cross-encoder. Its richer representation brings storage/serving trade-offs. LLM rerankers can use instructions and compare lists but add inference, order bias and prompt-injection exposure. Pairwise compares pairs; listwise ranks a set; pointwise scores each independently.

## Scores and thresholds
A relevance score measures the model's matching objective. Even a sigmoid output is not necessarily calibrated for your dataset. Select thresholds using held-out labels, inspect false positives by source/date/query slice, and monitor after upgrades. Relevance does not prove sufficiency, truth, authority or authorization.

## Context algorithm
1. Remove duplicate chunk IDs and overlapping spans.
2. Group by source/version and preserve essential qualifiers.
3. Select complementary evidence for each required fact.
4. Expand parents/neighbours only when needed and authorized.
5. Fit the model-specific token budget, including instructions, history and output reserve.
6. Attach stable citation IDs and preserve source boundaries.

MMR can select argmax of lambda*relevance(query,d) - (1-lambda)*max_similarity(d,selected). It trades relevance against redundancy. Lambda is a tunable diversity preference, not a probability. Do not discard an exception just because it resembles the main policy clause.

“Lost in the middle” describes failures to use information in long contexts. Order evidence deliberately, reduce distraction and evaluate order effects. Do not rely on one fixed placement trick for all models.

Example for A: One passage states the five-day cap; another says contractors are excluded; a third gives the effective date. A top-three list containing three paraphrases of the cap has less answer coverage than these complementary passages.

**Interview answer:** “I optimize context for sufficient, applicable facts per token. Ranking is only one input. I preserve conditions, dates and citations while removing redundant text.”

**Failure:** Great candidate recall but poor answers. **Debug:** Compare candidate -> rerank -> packed-context recall, inspect truncation and missing exceptions, then inspect generation. **Follow-up:** “Would increasing K fix it?” **Response:** “Only if the evidence was missing from candidates. It cannot repair a packing or verification bug.”
