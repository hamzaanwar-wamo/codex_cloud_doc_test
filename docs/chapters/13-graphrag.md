# 13. GraphRAG: entities, paths and source-backed reasoning

## Two related but different designs
Knowledge-graph RAG retrieves explicit entities/relations and paths. Community-summary GraphRAG clusters related graph areas and summarizes communities for broad corpus-level questions. A relationship query and “What themes connect our major incidents?” need different retrieval patterns. A summary is a derived artifact, not automatically primary evidence.

![Graph construction, bounded traversal and verification against source chunks](../diagrams/13-graph.png)

## Ingestion and graph schema
Parse/chunk documents -> extract candidate entities and relations -> canonicalize aliases -> validate ontology/types -> attach source spans, tenant, access, effective times and extractor version -> write assertions -> optionally cluster and summarize -> validate/publish. Store original text outside or alongside the graph so paths can resolve back to evidence. Deploy graph query workers/API plus graph store, source store and optional lexical/vector retrieval.

Example: Team Atlas --USES--> Service Ledger --SUPPLIED_BY--> Vendor Orion --SUBJECT_TO--> Policy R7. Every relationship needs a source assertion. Distinguish the canonical relation from assertions supporting it. If two documents support an edge, deleting one should remove that assertion, not necessarily the still-supported relation. If the last valid assertion disappears, do not keep the edge as truth.

Entity resolution uses source IDs, aliases, type constraints and sometimes similarity. “Atlas” may be a team, product or outside company. Merge only with sufficient evidence and retain reversible resolution history. An erroneous merge creates plausible but false multi-hop answers.

## What the database computes
A graph query engine executes patterns, joins, adjacency expansion, aggregations or algorithms over stored data. It does not establish that extracted relations are true. Shortest path is a graph property, not a proof that a path answers the question. Community detection groups strongly related nodes under an algorithm/objective; it does not identify authoritative policy on its own.

For B: Resolve the team entity -> traverse only relevant relation types -> restrict dates and access on nodes/edges -> bound depth/fan-out -> rank eligible paths -> fetch source chunks for every material edge -> verify joins, relation meaning and policy applicability -> synthesize with citations.

```cypher
// Simplified pattern; production requires access/date predicates on all parts.
MATCH (t:Team {id:$team_id, tenant_id:$tenant})
      -[u:USES]->(s:Service)-[p:SUPPLIED_BY]->(v:Vendor)
RETURN s.id, v.id, u.source_chunk_ids, p.source_chunk_ids
```

Use parameter binding and read-only credentials. A predicate on the starting node alone is not complete graph authorization. An application must validate every returned node/edge and evidence fetch, or enforce equivalent access in a tested query layer.

## Path ranking and global summaries
Rank by query-entity match, allowed relation semantics, source authority, temporal applicability and complete edge support. Arbitrary hop penalties or confidence products require validation; extraction scores are not independent probabilities. For broad questions, retrieve relevant community summaries, map partial answers and reduce them, preserving drill-down provenance. Rebuild affected summaries when underlying assertions change.

## Costs and evaluation
Extraction and entity resolution can dominate ingestion cost. Traversal can explode with high-degree nodes. Use relation-type restrictions, bounded hops, query timeouts, eligible subgraphs and candidate pruning. Evaluate entity-resolution quality, edge precision/recall, source-backed path coverage and final answer correctness against a hybrid baseline.

**Interview answer:** “The graph finds relationship chains. The evidence store proves what sources actually support those chains. I need both.” **Follow-up:** “Can the model infer a missing edge?” **Response:** “It can propose a hypothesis for further retrieval. I do not present it as an established relation without supporting evidence.”


## Additional visual walkthrough

![The Atlas relationship chain and independent source evidence](../diagrams/38-graph-example.png)

## A deeper path-selection example
For B, imagine three candidate paths. Path P1 connects Atlas to Orion through Ledger and current policy R7. P2 connects an unrelated team also named Atlas. P3 connects the correct team/vendor but uses an expired policy assertion. All three can be short and lexically plausible. Entity resolution rejects P2; temporal applicability rejects P3; only P1 moves to source verification. If one P1 edge has no permitted source, its answer remains unconfirmed.

A transparent ranking feature set can include exact entity identity, allowed relation sequence, requested-time overlap, source authority, query relevance and number of supported required relations. Learn or tune the combination using labeled paths. Do not hide an unsupported edge behind a large aggregate score. Hard validity constraints precede soft ranking preferences.

For temporal relationships, an entire path must be applicable at the requested time or over the explicitly defined interval. Independent current-looking edges may refer to incompatible periods. Store assertion validity separately from ingestion timestamp. For an “as of” query, intersect valid intervals and reject paths with an empty relevant intersection.

## Local/global queries and updates
Local search starts from particular entities and expands relevant neighbourhoods. Global search retrieves or processes community summaries to answer corpus-level themes, then combines supported partial results. Summaries can lose minority facts and qualifiers. Keep the source hierarchy so high-risk statements can drill back to originals. Recompute affected summaries after relation updates rather than assuming a summary remains valid because its text embedding still exists.

Incremental graph maintenance requires mapping source revision -> extracted assertions -> canonical relations -> affected communities/summaries. Deleting one document can invalidate several derived artifacts. A publication manifest should prevent mixed graph/source versions from silently answering together.
