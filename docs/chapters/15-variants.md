# 15. Other RAG patterns and what each changes

![Route by information need instead of accumulating every architecture](../diagrams/15-variants.png)

All variants keep the same obligations: authorized ingestion -> versioned index/storage -> scoped retrieval -> evidence checks -> grounded answer -> verification -> deploy/observe. The table states what changes, rather than implying these obligations disappear.

| Pattern | Ingestion/storage change | Runtime change and main trade-off |
|---|---|---|
| Self-RAG | Specific research versions use a model trained with reflection tokens | Model signals guide retrieval/critique; a generic self-check prompt is not the full research method |
| Corrective RAG | Retain reliable fallback sources | Detect weak retrieval and correct it; an incorrect detector can trigger unnecessary searches |
| Adaptive RAG | Store route/evaluation configuration | Choose path complexity by query; routing errors need fallbacks |
| Multi-hop | Preserve entities, source links and join evidence | Retrieve dependent facts; measure support for every hop |
| Hierarchical | Document/section/chunk tree | Coarse-to-fine selection; early-gate misses propagate |
| Parent-document | Small indexed children, larger parents | Fetch surrounding context; expansion adds tokens |
| Contextual | Add source-backed context to indexed passages | Retrieve using richer text; generated prefixes may distort meaning |
| Long-context | Retain complete source structure | Feed more selected content; costly and still vulnerable to distraction |
| Multimodal | Store images/regions/tables and compatible representations | Retrieve/interpret modalities; measure OCR/layout and citation accuracy |
| SQL/Text-to-SQL | Schema, semantic definitions, governed database access | Generate validated read-only query; exact calculations need execution, not prose guesses |
| Temporal | Effective intervals, versions, transaction times | Answer “as of” a date; latest upload is not always applicable truth |
| Conversational | Store scoped session context with retention limits | Resolve references, then retrieve fresh evidence; history can contain errors |
| Federated | Source registry and per-source access capabilities | Query multiple stores, normalize outputs and handle partial outages |
| Multi-agent | Tool and state contracts plus coordination metadata | Delegate independent subtasks; duplicates and inconsistent evidence need resolution |
| RAPTOR | Recursively cluster passages and create tree summaries | Retrieve across abstraction levels; summaries must link to source leaves |
| KG-enhanced | Extract source-backed relations | Combine path retrieval with passage search; extraction errors matter |
| Cached/speculative | Store reusable work with scope/version keys | Reuse/prefetch likely results; wrong predictions waste cost or become stale |

## SQL safety in more detail
Use parameterized values where applicable, schema/statement validation, read-only roles, row-level restrictions, execution deadlines and row/byte limits. Never let the model choose arbitrary databases or weaken tenant constraints. A syntactically valid query can still ask the wrong business question. Validate the reporting period, units, joins and aggregation definition. Cite the data source and query interpretation, not a fabricated paragraph.

## Temporal and conversational example
User asks A, then “What about contractors?” Resolve “what” to carry-forward, preserve the requested 2027 date, and retrieve the contractor policy. Do not reuse an employee answer because the wording is similar. If current identity or access changed, reevaluate scope even within the same session.

**Interview answer:** “These patterns solve different gaps and can be combined. I name the changed ingestion/runtime step and the new failure mode, rather than treating each label as a completely separate product.”

**Follow-up:** “Which is the best RAG?” **Response:** “The one that meets the workload's quality, isolation, freshness, latency and cost constraints with the least unnecessary complexity.”
