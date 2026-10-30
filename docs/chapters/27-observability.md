# 27. Observability, reliability and incident response

![A trace follows stage decisions while metrics and audits serve different needs](../diagrams/27-observability.png)

## What to record
A trace spans request intake, authorization, query understanding, retrieval branches, fusion, reranking, parent fetch, generation and verification. Include trace/request IDs, source/index/model versions, safe candidate IDs, rank changes, stage latency, token/cost usage, tool outcomes, final citations and abstention reason. Avoid default raw document/prompt logging, secrets and private reasoning. Apply access and retention controls to traces.

Metrics summarize rates and distributions; traces explain individual requests; audit logs record accountable access/actions. They are related but not interchangeable. Tools such as OpenTelemetry, Langfuse or LangSmith can help; configure their data handling deliberately.

## Quality and operational signals
Monitor empty retrieval rate, no-evidence abstention, unsupported claims on reviewed samples, source freshness lag, index version mismatch, queue age, DLQ volume, provider throttling, timeout rates, P95/P99 latency and cost per task. Changes in query mix can explain metric shifts; segment by query class and access selectivity. Avoid unbounded labels containing queries or user IDs in metric systems.

Retries should be bounded and limited to transient failures. Circuit breakers prevent a failing dependency from consuming all resources. Set deadlines per stage and propagate cancellation. Load shedding and admission control protect the rest of the system. Return a defined degraded response when a safe fallback exists; otherwise fail/abstain clearly.

## Recovery and drift
Run restore drills. Reconcile missing or orphaned chunks across stores. Check index manifests and source counts. Monitor distribution changes after source/model updates: vocabulary, score ranges, languages, document lengths and error slices. Drift is a prompt for evaluation, not automatic proof that retraining is required.

During an incident, establish affected scope/time/version, preserve safe evidence, stop harmful paths, communicate impact, restore verified service and add regression coverage. For access incidents, invalidate relevant caches and check source-link exposure as well as answer text.

**Interview answer:** “I need enough structured evidence to explain why a source entered or left the answer context, while minimizing sensitive logging. Reliability includes quality and freshness, not only uptime.”

**Follow-up:** “An alert says answer quality fell. What first?” **Response:** “Check corpus/model/index changes and query slices, reproduce affected traces, then locate the failing stage. I do not immediately rewrite the prompt.”
