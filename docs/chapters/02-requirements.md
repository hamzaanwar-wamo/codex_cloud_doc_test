# 2. Requirements, capacity and system design

## Clarify the workload
Ask who uses the system, what they can access, which answers need citations, what freshness means, what languages/file types exist, and which actions are allowed. Define availability and latency targets separately for interactive answers and research tasks. Define whether uncertain cases should abstain or escalate. Agree on source authority and effective-date semantics.

![Sizing from workload to capacity rather than document count alone](../diagrams/02-sizing.png)

Functional requirements: ingest/update/delete; retrieve within permission scope; answer with applicable citations; handle follow-ups and multi-document questions. Nonfunctional requirements: isolation, recoverability, freshness, bounded spend, observable failures and measurable answer quality.

## Capacity calculations
Average QPS = 100,000 / 86,400 = 1.16. Peak QPS cannot be inferred from that average. Suppose a measured or explicitly assumed peak is 20 QPS and mean request duration is 3 seconds. Little's law gives about 60 requests in flight in a stable interval: concurrency = arrival rate x mean duration. This is not a tail-latency guarantee. Retries, bursts and model limits require headroom.

Suppose 1 million documents average 20 chunks: 20 million vectors. At 768 dimensions, float32 raw vector bytes = 20,000,000 x 768 x 4 = 61.44 GB, about 57.2 GiB. Add index structures, metadata, text, lexical postings, replicas, temporary rebuild space and backups. Sample pages and chunk counts before committing to this estimate. Scanned-page OCR throughput may dominate ingestion more than embeddings.

For an ingestion deadline, workers needed approximately equal total processing seconds / deadline seconds / effective utilization. Measure file-type distributions, provider quotas and memory requirements. More workers do not help if one embedding endpoint is throttled.

## Architecture and storage ownership
Object storage retains original bytes and parsed layout. PostgreSQL tracks documents, versions, chunks, ACLs, jobs and publication state. Search indexes hold retrievable representations. An optional graph store holds source-backed relationships. A cache stores replaceable results, never the only copy of authoritative data.

An SLO must specify the denominator and window. Example, not a recommendation: “99% of successful interactive requests complete within the agreed deadline over a month.” Track errors and abstentions separately so rejecting hard requests cannot fake good latency or quality.

**Interview answer:** “I size from chunks, bytes, query mix, peak traffic and update rate. I choose the simplest pipeline that meets measured quality and isolation requirements. The first design is a hypothesis, not a benchmark.”

**Follow-up:** “What do you build first?” **Response:** “Representative ingestion, permission-aware lexical and dense baselines, and a labeled evaluation set. I postpone graphs and agents until their target query slices justify them.”

**Failure:** A design meets average QPS but collapses at office opening. **Debug:** Inspect request arrival distribution, queue wait and provider rate limits. **Prevention:** Load-test realistic bursts, apply backpressure, set admission limits and protect the interactive path from bulk ingestion.


## Additional visual walkthrough

![Logical database schema and source-to-claim references](../diagrams/35-schema.png)

## Quantitative storage visual

![Raw vector storage under explicit dimension and precision assumptions](../diagrams/39-storage-chart.png)

Only the vector payload is counted. Compression may change retrieval quality and add codebook/scale metadata. Lower raw bytes do not prove lower total system cost. Text, graph, replicas and index structures remain outside these bars.
