# 30. Five complete execution walkthroughs

![The common execution spine and five retrieval routes](../diagrams/30-walkthroughs.png)

All records and policy facts below are synthetic. Each trace should record identity/scope, source/index version, requested date, route, candidates, ranking transitions, final evidence, verifier result, stage timings and token/tool cost. These are worked designs, not measured production executions.

## 1. Factual vector route: question A
Ingestion stores HR-42 v3 carry-forward and eligibility chunks with page spans and effective date. Runtime resolves tenant t1, group employees-pk and 2027 applicability. Query embedding retrieves leave passages. Fetch/expand the cap and exception sources. Evidence checklist: cap, eligible group, effective date and any expiry condition. Generate “Up to five days for eligible staff, subject to the cited conditions.” Verify each material claim. If expiry is absent, say it was not established. Store citations/verdict references, not invented certainty. Deployment uses the common API/search/model path.

## 2. Hybrid explanation: “Why does HR-42 limit carry-forward?”
Ingestion publishes lexical/vector representations from the same source versions. BM25 ranks policy-code matches; dense search ranks semantic rationale passages. Suppose ranks are BM25 A,B,C and dense B,D,A. RRF with illustrative c=60 produces B,A,D,C. Rerank and deduplicate. If B states the rule and A states an approved rationale, answer both with distinct citations. If no source states a rationale, explain only the rule and flag the missing explanation. A model's plausible HR rationale is not evidence.

## 3. Vectorless exact lookup: question C
Ingestion stores document/version/section exact fields and original section text. Runtime authorizes t1 and requested HR-42 v3, section 7. Exact lookup resolves directly to the section. Check applicability if the user expects current policy; do not silently replace an explicitly historical version. Return the excerpt with source location. No embedding or multi-step navigation is needed. Cache only under scope/version keys. Deployment can omit a vector service for this route.

## 4. Graph multi-hop: question B
Ingestion stores canonical Atlas, Ledger, Orion and R7 entities plus independently source-backed relationship assertions. Runtime resolves Atlas, traverses USES/SUPPLIED_BY/SUBJECT_TO under access/date constraints, ranks candidate paths and fetches every edge's evidence. Exclude expired or unsupported relationships. Verify that Ledger refers to the same service across sources. Answer only supported affected vendors and cite original sources, not just a graph visualization. Persist path/source IDs and unresolved gaps. Deploy a graph adapter plus the shared evidence pipeline.

## 5. Agentic comparison: B plus “compare old and new obligations”
Ingestion retains versioned policies and source-backed vendor links. Runtime plan: discover vendors, fetch current policy, fetch historical policy, compare obligations. Evidence check after the current policy identifies the missing historical baseline. A permitted tool retrieves it. If successful, calculate changes deterministically and verify sources. If absent or budget exhausted, return confirmed affected vendors and state that the old obligation was not established. The state machine stops rather than searching forever. Checkpoints store permitted progress; the orchestrator enforces deadlines and call budgets.

## Reading latency and cost
For each route, add actual serial stage durations, account for parallel overlap, and record total request duration directly. Compute input/output/tool cost from actual usage and current pricing. Do not infer a system benchmark from the example ranks or hypothetical budgets in this book.

**Interview answer:** “The route changes, but authorization, versions, provenance, sufficiency and claim verification remain common. I can show every intermediate record that led to the final answer.”
