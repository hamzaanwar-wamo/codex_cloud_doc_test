# Diagram gallery and editable sources

All figures appear inline in the handbook and are embedded in PDF/Word. Most are flows, trees or schema relationships; figure 36 is a participant sequence; figures 39 and 40 are quantitative charts.

Edit `specs.json` for Graphviz/Mermaid flow definitions. Edit `../render_visuals.py` for the sequence/charts. Rebuild with `python docs/build_handbook.py` from the repository root. Exports are generated, so editing only a PNG or MMD will not persist through a rebuild.

| Figure | Preview | Editable / vector sources |
|---|---|---|
| 01-lifecycle | [PNG](01-lifecycle.png) | [mmd](01-lifecycle.mmd), [dot](01-lifecycle.dot), [svg](01-lifecycle.svg) |
| 02-sizing | [PNG](02-sizing.png) | [mmd](02-sizing.mmd), [dot](02-sizing.dot), [svg](02-sizing.svg) |
| 03-ingestion | [PNG](03-ingestion.png) | [mmd](03-ingestion.mmd), [dot](03-ingestion.dot), [svg](03-ingestion.svg) |
| 04-chunking | [PNG](04-chunking.png) | [mmd](04-chunking.mmd), [dot](04-chunking.dot), [svg](04-chunking.svg) |
| 05-metadata | [PNG](05-metadata.png) | [mmd](05-metadata.mmd), [dot](05-metadata.dot), [svg](05-metadata.svg) |
| 06-vectors | [PNG](06-vectors.png) | [mmd](06-vectors.mmd), [dot](06-vectors.dot), [svg](06-vectors.svg) |
| 07-bm25 | [PNG](07-bm25.png) | [mmd](07-bm25.mmd), [dot](07-bm25.dot), [svg](07-bm25.svg) |
| 08-hybrid | [PNG](08-hybrid.png) | [mmd](08-hybrid.mmd), [dot](08-hybrid.dot), [svg](08-hybrid.svg) |
| 09-reranking | [PNG](09-reranking.png) | [mmd](09-reranking.mmd), [dot](09-reranking.dot), [svg](09-reranking.svg) |
| 10-standard | [PNG](10-standard.png) | [mmd](10-standard.mmd), [dot](10-standard.dot), [svg](10-standard.svg) |
| 11-production-hybrid | [PNG](11-production-hybrid.png) | [mmd](11-production-hybrid.mmd), [dot](11-production-hybrid.dot), [svg](11-production-hybrid.svg) |
| 12-vectorless | [PNG](12-vectorless.png) | [mmd](12-vectorless.mmd), [dot](12-vectorless.dot), [svg](12-vectorless.svg) |
| 13-graph | [PNG](13-graph.png) | [mmd](13-graph.mmd), [dot](13-graph.dot), [svg](13-graph.svg) |
| 14-agent | [PNG](14-agent.png) | [mmd](14-agent.mmd), [dot](14-agent.dot), [svg](14-agent.svg) |
| 15-variants | [PNG](15-variants.png) | [mmd](15-variants.mmd), [dot](15-variants.dot), [svg](15-variants.svg) |
| 16-selection | [PNG](16-selection.png) | [mmd](16-selection.mmd), [dot](16-selection.dot), [svg](16-selection.svg) |
| 17-evidence | [PNG](17-evidence.png) | [mmd](17-evidence.mmd), [dot](17-evidence.dot), [svg](17-evidence.svg) |
| 18-generation | [PNG](18-generation.png) | [mmd](18-generation.mmd), [dot](18-generation.dot), [svg](18-generation.svg) |
| 19-dataset | [PNG](19-dataset.png) | [mmd](19-dataset.mmd), [dot](19-dataset.dot), [svg](19-dataset.svg) |
| 20-retrieval-metrics | [PNG](20-retrieval-metrics.png) | [mmd](20-retrieval-metrics.mmd), [dot](20-retrieval-metrics.dot), [svg](20-retrieval-metrics.svg) |
| 21-answer-metrics | [PNG](21-answer-metrics.png) | [mmd](21-answer-metrics.mmd), [dot](21-answer-metrics.dot), [svg](21-answer-metrics.svg) |
| 22-agent-eval | [PNG](22-agent-eval.png) | [mmd](22-agent-eval.mmd), [dot](22-agent-eval.dot), [svg](22-agent-eval.svg) |
| 23-experiments | [PNG](23-experiments.png) | [mmd](23-experiments.mmd), [dot](23-experiments.dot), [svg](23-experiments.svg) |
| 24-deployment | [PNG](24-deployment.png) | [mmd](24-deployment.mmd), [dot](24-deployment.dot), [svg](24-deployment.svg) |
| 25-latency | [PNG](25-latency.png) | [mmd](25-latency.mmd), [dot](25-latency.dot), [svg](25-latency.svg) |
| 26-security | [PNG](26-security.png) | [mmd](26-security.mmd), [dot](26-security.dot), [svg](26-security.svg) |
| 27-observability | [PNG](27-observability.png) | [mmd](27-observability.mmd), [dot](27-observability.dot), [svg](27-observability.svg) |
| 28-debugging | [PNG](28-debugging.png) | [mmd](28-debugging.mmd), [dot](28-debugging.dot), [svg](28-debugging.svg) |
| 29-implementation | [PNG](29-implementation.png) | [mmd](29-implementation.mmd), [dot](29-implementation.dot), [svg](29-implementation.svg) |
| 30-walkthroughs | [PNG](30-walkthroughs.png) | [mmd](30-walkthroughs.mmd), [dot](30-walkthroughs.dot), [svg](30-walkthroughs.svg) |
| 31-interview | [PNG](31-interview.png) | [mmd](31-interview.mmd), [dot](31-interview.dot), [svg](31-interview.svg) |
| 32-questions | [PNG](32-questions.png) | [mmd](32-questions.mmd), [dot](32-questions.dot), [svg](32-questions.svg) |
| 33-challenges | [PNG](33-challenges.png) | [mmd](33-challenges.mmd), [dot](33-challenges.dot), [svg](33-challenges.svg) |
| 34-revision | [PNG](34-revision.png) | [mmd](34-revision.mmd), [dot](34-revision.dot), [svg](34-revision.svg) |
| 35-schema | [PNG](35-schema.png) | [mmd](35-schema.mmd), [dot](35-schema.dot), [svg](35-schema.svg) |
| 36-query-sequence | [PNG](36-query-sequence.png) | [mmd](36-query-sequence.mmd), [dot](36-query-sequence.dot), [svg](36-query-sequence.svg) |
| 37-chunk-tree | [PNG](37-chunk-tree.png) | [mmd](37-chunk-tree.mmd), [dot](37-chunk-tree.dot), [svg](37-chunk-tree.svg) |
| 38-graph-example | [PNG](38-graph-example.png) | [mmd](38-graph-example.mmd), [dot](38-graph-example.dot), [svg](38-graph-example.svg) |
| 39-storage-chart | [PNG](39-storage-chart.png) | [svg](39-storage-chart.svg), [json](39-storage-chart.json) |
| 40-latency-chart | [PNG](40-latency-chart.png) | [svg](40-latency-chart.svg), [json](40-latency-chart.json) |

The DOT export for figure 36 is a flow projection; the PNG/SVG and Mermaid export use a participant sequence. Chart values are hypothetical arithmetic/budgets, not measurements.
