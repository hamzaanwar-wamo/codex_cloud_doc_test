# 5. Metadata, enrichment and query understanding

![Document metadata prepared offline and query scope resolved online](../diagrams/05-metadata.png)

## Three different metadata layers
Document metadata identifies owner, source, authority, language, version, effective dates and access policy. Chunk metadata adds heading path, page/span, parent, entities and indexed representation version. Query metadata describes authenticated identity, allowed scope, requested time, language, intent and extracted identifiers. These layers have different trust levels.

```json
{
  "chunk_id": "hr42:v3:s7:c2", "doc_id": "hr42", "version": 3,
  "tenant_id": "t1", "allowed_groups": ["employees-pk"],
  "parent_id": "hr42:v3:s7", "heading_path": ["Leave", "Carry forward"],
  "text": "Up to five days ...", "page": 8,
  "source_uri": "object://t1/hr42/v3.pdf",
  "effective_from": "2027-01-01", "effective_to": null,
  "content_hash": "sha256:...", "pipeline_version": "parse4-chunk2",
  "embedding_model": "model-A-v1", "authority": "approved-policy"
}
```

Source references must resolve to access-checked content; a citation URL must not bypass storage authorization. Store exact spans when feasible, not just page numbers. Generated enrichment belongs in a separate field from original evidence.

## Enrichment methods
Rules extract stable IDs, dates and known patterns cheaply. NER finds candidate people, organizations and locations. LLMs can infer topics and relations, but require schema validation, source grounding and error sampling. Store extraction method, version, source span and uncertainty. A model-supplied confidence value is not automatically calibrated.

Contextual prefixes explain where a chunk belongs, such as “HR-42, 2027 Pakistan leave policy, carry-forward section.” Build prefixes from reliable headings/metadata where possible. If generated, verify they do not change meaning. Index the prefix but cite original text.

## Query transformations and risks
Rewriting resolves shorthand or conversation references: “What about contractors?” becomes a search question linked to the previous policy topic. Keep the original query for auditing; a rewrite can change intent. Expansion adds synonyms or related terms. Multi-query retrieves several reformulations and merges results. Decomposition makes dependent subquestions for a multi-hop task. Each raises recall potential and query cost.

HyDE generates a hypothetical answer/document, embeds it, then retrieves real evidence. The hypothetical text is a search aid, never evidence. It may steer toward plausible but wrong assumptions. Compare against simpler query expansion.

Routing chooses exact lookup, lexical, vector, hybrid, graph or SQL based on task and measured performance. A classifier should have a fallback route. A wrongly predicted topic should usually be a soft boost, not an irreversible exclusion.

Hard filters enforce tenant, access, explicit version/date and other certain requirements. Soft filters boost likely topic/source preferences. Resolve access from the server identity, never from generated query text. Date filters must distinguish publication, ingestion and effective dates.

**Interview answer:** “Metadata is not just tags. It connects retrieval, versioning, provenance and authorization. I separate trusted scope from model-inferred hints.”

**Follow-up:** “Can the model choose filters?” **Response:** “It can propose business filters through a schema. The server validates them and always adds non-negotiable access constraints.”
