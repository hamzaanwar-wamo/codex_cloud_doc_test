# 10. Standard vector RAG: the baseline architecture

![Standard RAG from original files to verified answers](../diagrams/10-standard.png)

## Complete path
Ingest: authorized connector -> parse/OCR -> normalize -> version -> chunk -> embed. Store original bytes, chunk text/metadata and vectors. Publish the index version. Query: authenticate -> resolve scope and date -> encode query -> filtered vector search -> fetch source chunks -> check evidence -> generate with citations -> verify -> answer/abstain. Deploy an API, ingestion workers, persistent stores and model adapters; restart processes independently from stored indexes.

The word “standard” describes the retrieval core, not permission to omit security or evidence checks. A teaching diagram often shows only embed -> retrieve -> generate; a real answer service needs the rest.

## Question A walkthrough
The model embeds “Can a Pakistan employee carry unused leave into 2027?” Semantic neighbours include leave entitlement, carry-forward and general benefits. Resolve tenant and employees-pk access before exposing text. Retain the correct policy version effective at the requested time. If the top hits contain the cap but not eligibility, retrieve related context or abstain on eligibility rather than guess.

## Benefits and limits
This architecture is easy to implement and useful for paraphrase-heavy passage questions. Weaknesses include exact IDs, incompatible query/document representation, poor chunk boundaries, restrictive filters, and multi-hop tasks where no single passage answers the question. One top chunk can be relevant without being sufficient.

Tune the model, chunking, ANN parameters and K using labeled queries. First compare exact vector search to ANN on a manageable eligible subset; then distinguish embedding quality from ANN recall loss. Add complexity only after identifying the failing stage.

**Pseudocode:** `scope = authorize(identity); hits = vector_search(embed(query), scope); evidence = validate(fetch(hits)); draft = grounded_generate(evidence); return verify(draft)`.

**Evaluation:** Candidate recall, final-context coverage, supported answer correctness, authorization, freshness, latency and cost. **Failure:** The correct passage ranks below the cutoff. Check exact vector rank, ANN recall, filters and query interpretation before increasing K blindly.

**Interview answer:** “Vector RAG is my semantic baseline. It is a retrieval choice inside a larger versioned, permission-aware evidence system.” **Follow-up:** “When do you replace it?” **Response:** “I first test adding lexical retrieval or better context selection. I do not jump directly to agents when the actual failure is exact-ID matching.”
