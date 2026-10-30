# 32. 150 interview questions and first-person answers

These concise revision cards supplement the deeper explanations and challenging follow-ups in Chapters 1-31. Use them for recall, then expand each answer with a diagram, example, failure mode and evaluation plan. They are not a claim that every topic has only one valid answer.

![Turn a short answer into a defensible senior-level explanation](../diagrams/32-questions.png)

## Foundations and requirements

### Q001. What does RAG add to an LLM?
I add selected external evidence at answer time. I still need to measure retrieval errors and unsupported generation.

### Q002. Why can a retrieved answer still be wrong?
I may retrieve an outdated or inapplicable source, miss an exception, or generate a claim the evidence does not support.

### Q003. When would you fine-tune instead?
I use fine-tuning for behaviour, style or repeated task patterns. I keep freshness and citations in the evidence pipeline.

### Q004. Can long context replace retrieval?
For a small known source set, sometimes. At enterprise scale I still need authorization, source selection and manageable cost.

### Q005. What is parametric knowledge?
It is information encoded in model parameters, without a dependable per-fact source/version lookup.

### Q006. Retrieval versus reasoning?
I retrieve facts, then reason or compute over them. Neither step automatically validates the other.

### Q007. What is modular RAG?
I separate ingestion, routing, retrieval, ranking, generation and verification behind explicit contracts.

### Q008. Which requirements do you clarify first?
I ask about users, access, query types, authority, freshness, citations, latency, cost and acceptable abstention.

### Q009. Why is document count insufficient for sizing?
I need bytes, pages, chunk distribution, vector dimensions, update rate, replicas and peak query behaviour.

### Q010. How do you estimate mean concurrency?
I multiply arrival rate by mean duration in a stable interval, then separately plan for bursts and tail behaviour.

### Q011. What makes an SLO meaningful?
I define the population, time window, outcome and threshold, including how errors and timeouts are counted.

### Q012. What is a good first baseline?
I build representative ingestion, exact/lexical and dense retrieval, access checks and a labeled query set.

### Q013. What is the difference between a source and an index?
The source contains authoritative content. The index is a derived search representation that can be rebuilt.

### Q014. What is a token budget?
I budget instructions, history, evidence and output using the target tokenizer and model limits.

### Q015. What does production-ready mean here?
I require real integration, access/freshness checks, fault handling, observability and recovery evidence, not just a fluent demo.

## Ingestion and lifecycle

### Q016. Why keep original files?
I need reproducibility, source verification, improved reparsing and reliable citations back to original content.

### Q017. How do you parse scanned PDFs?
I use OCR plus layout handling and preserve page/region coordinates. I inspect numerical and column-order errors.

### Q018. What is ingestion idempotency?
Repeated delivery of one source revision should produce the same intended version without duplicate active chunks.

### Q019. What belongs in an idempotency key?
I include tenant, stable source identity, revision and pipeline version, matching the actual update semantics.

### Q020. Why at-least-once queues matter?
I expect duplicate deliveries and make writes/retries safe rather than assume each event happens exactly once.

### Q021. What goes to a DLQ?
I move permanently invalid or repeatedly failing jobs with safe diagnostics, source pointers and a defined repair path.

### Q022. How do you publish an index?
I validate the required versioned artifacts and switch a manifest or alias only when the complete version is ready.

### Q023. What about partial cross-store writes?
I leave the version unpublished and use durable job state plus reconciliation to complete or clean it.

### Q024. Content hash versus source identity?
A hash detects byte/content equality; source identity tracks ownership and lifecycle. Neither replaces tenant/access semantics.

### Q025. When must you re-embed?
I re-embed changed content or rebuild when the model/representation contract changes. Matching dimensions do not imply compatible spaces.

### Q026. How do you delete a document?
I block access promptly, remove original/derived/index/cache records under policy and track deletion completion.

### Q027. How do you handle ACL revocation?
I enforce current scope or tombstones immediately enough for the security requirement, independently of slow reindexing.

### Q028. Upload time versus effective time?
Upload time says when we received content. Effective time says when the policy or fact applies.

### Q029. How do you test freshness?
I measure source-change-to-searchable delay and verify the published revision, including update/delete/revocation cases.

### Q030. What do you preserve for tables?
I retain column/row labels, units, period, caption and coordinates, then use structured computation for exact aggregation.

## Chunking

### Q031. Why not embed the whole document?
Long documents mix topics, may truncate and give coarse citations. I compare document routing with local evidence chunks.

### Q032. Character versus token chunks?
Character count is cheap but does not control model input size. Token count uses the chosen tokenizer.

### Q033. How does recursive splitting work?
I try meaningful separators in order, then use finer boundaries until the maximum token size is met.

### Q034. How do you pick overlap?
I test boundary-failure cases and compare against zero overlap. Duplicate storage/context is a real cost.

### Q035. Is a 512-token chunk always good?
No. I test candidate sizes on required-fact coverage, answer quality, index cost and latency for the actual corpus.

### Q036. What is semantic chunking?
I split near changes in adjacent semantic representations, while enforcing size limits and protected structural spans.

### Q037. Percentile versus deviation breakpoints?
Percentiles select relative distance extremes; deviation rules compare to the distribution mean. Both need corpus-specific testing.

### Q038. What is parent-child retrieval?
I index small children for matching, then fetch larger authorized parents when extra context is needed.

### Q039. Can parent-child use recursive chunks?
Yes. Recursive defines boundaries; parent-child defines relationships between retrieval and context units.

### Q040. What is sentence-window retrieval?
I retrieve a sentence and expand nearby sentences, respecting section boundaries, permissions and context budget.

### Q041. What is proposition chunking?
I extract atomic factual statements, but I retain provenance and check that qualifiers were not lost.

### Q042. What is contextual enrichment?
I add source context before indexing, separating generated explanation from original evidence and validating it.

### Q043. What is late chunking?
I encode longer text first and pool token representations over selected spans, using a compatible model.

### Q044. Why AST chunking for code?
Symbols and syntax are meaningful boundaries. I still retain imports, file context and cross-file dependencies.

### Q045. When use LLM chunking?
Only when difficult structure benefits enough to justify cost, nondeterminism and source-boundary validation.

## Metadata and embeddings

### Q046. Which metadata is mandatory?
I need stable IDs, tenant/access scope, source/version, location, parent links, effective dates and representation versions.

### Q047. Hard filter versus soft boost?
Hard filters exclude results and need reliable constraints. Soft boosts express uncertain preferences without irreversibly hiding evidence.

### Q048. Can an LLM set access filters?
It can propose business intent. The server always resolves and enforces identity, tenant and access independently.

### Q049. Why store enrichment confidence?
It helps inspection and calibration, but I do not interpret an unvalidated generated number as a probability.

### Q050. What can query rewriting break?
It can change entities, requested dates or user intent. I preserve the original query and test rewrite effects.

### Q051. What is HyDE?
I generate hypothetical search text to embed, then retrieve real sources. The generated text is not evidence.

### Q052. When use multi-query retrieval?
When diverse formulations improve recall enough to justify added search cost and candidate noise.

### Q053. What is a bi-encoder?
It encodes query and document separately so document vectors can be prepared before queries arrive.

### Q054. What does cosine measure?
Vector angle similarity after accounting for magnitudes. It is not calibrated answer correctness.

### Q055. When do dot and cosine rankings agree?
For consistently unit-normalized vectors. Without normalization, vector magnitude also affects dot product.

### Q056. Why does embedding truncation matter?
A model can silently omit the answer-bearing end of a chunk before any vector search occurs.

### Q057. How do you choose embedding dimensions?
I compare quality and memory/latency trade-offs supported by the model, rather than assume more dimensions always help.

### Q058. How do you handle multilingual queries?
I evaluate cross-language retrieval and domain terminology, including code-switching, using representative labels.

### Q059. Why version the tokenizer/model?
Representation and truncation can change across versions, affecting reproducibility and compatibility.

### Q060. How do you migrate embedding models?
I build a separate compatible index, shadow/evaluate, publish by manifest and retain rollback without mixing spaces.

## Search internals and vectorless RAG

### Q061. What is an inverted index?
It maps terms to postings of matching document/chunk IDs and statistics, avoiding a full PDF scan at query time.

### Q062. How does BM25 use IDF?
Rarer query terms usually contribute more, subject to the implementation's IDF formula and tokenization.

### Q063. Why term-frequency saturation?
Repeated mentions should not increase relevance without bound, so BM25 gives diminishing returns.

### Q064. What does BM25 length normalization do?
It adjusts for longer indexed units containing more terms. I tune it against the chosen chunk/document granularity.

### Q065. Why keep exact keyword fields?
I need identifiers and versions to survive punctuation, stemming and analyzer transformations.

### Q066. Document versus chunk BM25?
Documents provide coarse topic context; chunks provide local evidence. I evaluate any document gate for missed relevant sources.

### Q067. What is vectorless RAG?
It retrieves using exact lookup, lexical indexes or hierarchy without dense embeddings, then grounds generation in sources.

### Q068. Is LLM tree navigation free?
No. It can add several model calls and miss branches due to misleading headings or summaries.

### Q069. How does HNSW search work?
It navigates a layered neighbour graph, then explores nearby candidates with a recall/latency search-effort trade-off.

### Q070. How does IVF work?
It searches selected vector clusters/cells rather than all vectors, trading probe effort against recall.

### Q071. What is PQ?
It compresses subvectors using learned codebooks, reducing storage with possible ranking accuracy loss.

### Q072. Why evaluate ANN against exact search?
I want to isolate approximate-index loss from embedding quality, filters or missing sources.

### Q073. Why can post-filtering fail?
A small global candidate list may contain no authorized items even when good eligible matches exist.

### Q074. Is FAISS a full database?
No. I must supply serving, persistence, metadata, authorization and recovery around the index library.

### Q075. How do you select a vector database?
I test filtered recall, updates, persistence, recovery, scale, operational burden and cost under the actual workload.

## Hybrid, reranking and context

### Q076. Why hybrid retrieval?
Keyword and semantic retrieval fail differently; I test whether their union improves relevant evidence coverage.

### Q077. Why not add BM25 and cosine scores?
Their scales and meanings differ. I use rank fusion or a validated normalization/calibration method.

### Q078. What is RRF?
I sum weighted reciprocal shifted ranks for each candidate. Missing results contribute zero.

### Q079. How do you choose the RRF constant?
I tune it on held-out ranking/answer metrics because it controls sensitivity to rank differences.

### Q080. Candidate K versus final N?
K sets retrieval/reranking coverage; N sets evidence/context selection. They have different costs and failure modes.

### Q081. Can reranking fix missing retrieval?
No. It can only reorder candidates already returned, so I measure candidate recall first.

### Q082. Why is a cross-encoder more expensive?
It jointly reads each query-document pair at runtime instead of reusing one stored document vector.

### Q083. What is ColBERT late interaction?
It matches separately encoded token vectors and aggregates their similarities, with richer storage/serving needs.

### Q084. Pointwise versus listwise reranking?
Pointwise scores each candidate; listwise compares a set and can introduce order/context-budget sensitivity.

### Q085. Is reranker score a probability?
Only if appropriately calibrated for the task and distribution. A high relevance score still does not prove support.

### Q086. Why deduplicate before generation?
Repeated spans waste tokens and can falsely look like independent corroboration.

### Q087. What does MMR optimize?
A balance of query relevance and novelty relative to selected results, under a tunable trade-off.

### Q088. How do you pack context?
I prioritize complete required facts, source boundaries and qualifiers, then fit the full prompt/output budget.

### Q089. What is lost-in-the-middle risk?
The model may underuse evidence in long contexts depending on placement and distraction, so I test ordering.

### Q090. When expand parents?
When small hits lack conditions or surrounding meaning, while enforcing scope and final token limits.

## Graphs and agents

### Q091. Why use a knowledge graph?
Explicit relationships help queries requiring joins or multi-hop paths across entities, when extraction quality is sufficient.

### Q092. Does a graph path prove a claim?
No. It proves stored connectivity. I verify entity identity, relation semantics, dates and original source support.

### Q093. What is entity resolution?
I map aliases and mentions to canonical identities, retaining uncertainty and reversible merge history.

### Q094. What belongs on graph assertions?
I store source spans/IDs, tenant/access, effective dates, extractor version and relation provenance.

### Q095. Why separate relations and assertions?
Several sources can support one relation; deleting one assertion should not wrongly erase or perpetuate the fact.

### Q096. How do you choose traversal paths?
I restrict relation types and scope, then rank paths by query relevance, applicability and complete source support.

### Q097. Is shortest path best evidence?
Not necessarily. Graph distance is not the same as semantic relevance or authoritative support.

### Q098. Community GraphRAG versus KG retrieval?
Community summaries support broad themes; entity-path retrieval supports explicit relation questions. Both need provenance.

### Q099. How do you avoid graph explosion?
I bound hops, fan-out, relation types, execution time and eligible subgraphs, then monitor path counts.

### Q100. Agent versus workflow?
A workflow follows defined transitions; an agent chooses actions from observations. Both need scoped tools and budgets.

### Q101. What belongs in agent state?
I store task plan, evidence references, gaps, safe action outcomes, progress and budgets, with trusted identity outside model control.

### Q102. What makes an agent retry useful?
It addresses a specific evidence gap with a changed query/tool or follows a meaningful state change.

### Q103. How do you stop loops?
I enforce deadline, spend/call limits and no-progress/repeated-result detection in server logic.

### Q104. When use human approval?
For consequential external actions or unresolved high-risk decisions under the task's authorization policy, not every read-only search.

### Q105. How do you evaluate multi-agent systems?
I compare task success, evidence consistency, duplicated work, safety and cost against a simpler single-orchestrator baseline.

## Evidence and generation

### Q106. Relevance versus sufficiency?
A passage may be topical while missing a condition. I test whether all required facts are supported.

### Q107. What is provenance?
The trace from a claim or chunk back to source version, location and processing steps.

### Q108. What is precomputed evidence metadata?
Source spans, hashes, authority labels, dates and extracted facts can be prepared before queries.

### Q109. What is runtime evidence verification?
I check whether applicable sources support the specific question and each generated material claim.

### Q110. How do you represent a claim verdict?
I store claim/source references, source versions, check type, verdict and verifier version under retention/access rules.

### Q111. What can deterministic checks verify?
Citation membership, IDs, types, dates, units and arithmetic, when the rule and data are reliable.

### Q112. What can NLI or LLM judges miss?
Negation, tables, temporal assumptions, invalid joins, hidden exceptions and ambiguous source authority.

### Q113. How do you handle conflicting sources?
I apply explicit authority/scope/time rules, then disclose or abstain on unresolved conflicts instead of silently merging.

### Q114. What is evidence coverage?
The supported share of predefined required facts, optionally weighted; duplicates do not create new coverage.

### Q115. Why not multiply all confidence scores?
They are often correlated, uncalibrated and measuring different objectives, so the product is not a justified probability.

### Q116. How do you calibrate answerability?
I compare signals to held-out correctness labels and choose a risk/coverage operating point by task slice.

### Q117. What makes a citation valid?
It resolves to an accessible source version and location; support additionally requires that the passage substantiates the claim.

### Q118. How should prompts handle retrieved instructions?
I mark them as untrusted source content, while server-side controls prevent capability or access escalation.

### Q119. When should the system abstain?
When required applicable evidence is missing, authority is unresolved or claim support fails under the defined policy.

### Q120. Should answers stream before verification?
Only under an explicit risk policy. For high-risk claims I verify before release or release verified segments.

## Evaluation and experiments

### Q121. What belongs in a golden example?
Question, identity/scope, date, corpus version, required facts, sources, acceptable answer/abstention and rubric.

### Q122. Why include unauthorized questions?
I need to verify no leakage across candidates, output, citations, caches or logs, not just answer correctness.

### Q123. Precision@K versus Recall@K?
Precision measures relevant share of returned results; recall measures share of all labeled relevant evidence found.

### Q124. What does MRR emphasize?
The position of the first relevant result, not complete evidence coverage for multi-fact questions.

### Q125. Why use nDCG?
It evaluates placement with graded relevance against the ideal ordering, under stated label/zero-relevance conventions.

### Q126. What is MAP?
Mean average precision over queries, sensitive to the positions of relevant items under an explicit cutoff denominator.

### Q127. How do you evaluate graph retrieval?
I test entity resolution, edge accuracy, complete supported path coverage and final answer quality.

### Q128. Correctness versus faithfulness?
Correctness compares to truth/expected facts; faithfulness compares claims to supplied evidence, which itself may be wrong.

### Q129. Citation precision versus recall?
Precision checks cited-claim support/attribution; recall checks coverage of material claims needing citations.

### Q130. How do you assess abstention?
I report wrong-answer risk against answer coverage and detect unnecessary refusal when evidence is sufficient.

### Q131. Can the same model generate and judge?
It can assist, but shared biases require human calibration, independent checks and versioned judge prompts.

### Q132. What is an ablation?
I remove or vary one component to identify which change produced the measured benefit or regression.

### Q133. Why paired evaluation?
The same queries reduce workload confounding, allowing more meaningful differences and uncertainty estimates.

### Q134. How do you avoid test-set leakage?
I separate tuning/test sets, version labels and avoid repeatedly selecting parameters on the final holdout.

### Q135. Offline versus online evaluation?
Offline labels diagnose quality and safety; controlled online tests measure real behaviour with monitoring and stop criteria.

## Production, security and debugging

### Q136. Why separate ingestion and queries?
Bulk parsing/indexing throughput should not consume resources needed for interactive latency.

### Q137. Which versions belong in traces?
I include corpus/index, parser/chunker, analyzer/embedding, reranker, generator/prompt and verifier versions where relevant.

### Q138. Why not sum stage P95 values?
Stage tail events may not coincide. I measure request P95 directly from complete traces.

### Q139. How do you calculate model cost?
I multiply actual input/output usage by current unit prices, then add tool, retrieval and infrastructure costs.

### Q140. Retrieval cache versus KV cache?
Retrieval cache stores search results; KV cache reuses model attention computation. Neither alone establishes current access or truth.

### Q141. What makes a cache key safe?
I include tenant, effective permissions, date, source/index version and relevant model/prompt versions, and revalidate access.

### Q142. Where must authorization apply?
Every lexical/vector, graph, parent, SQL, source-link, cache and audit path—not only the final answer.

### Q143. How do you defend prompt injection?
I treat documents as untrusted, constrain tools/destinations and enforce scope server-side, rather than rely only on prompts.

### Q144. What should not go in logs?
I avoid secrets, unnecessary raw sensitive text, unauthorized content and private reasoning; logs need access/retention controls.

### Q145. How do you handle dependency outages?
I use deadlines, bounded retries, circuit breakers and validated scoped fallback; otherwise I fail or abstain clearly.

### Q146. How do you debug low recall?
I trace expected sources through parsing, filtering, indexing and search, and compare ANN with exact eligible search.

### Q147. How do you debug good recall but bad answers?
I inspect rerank/packing losses, missing qualifiers, applicability, generation and verification before changing the model.

### Q148. What must deletion invalidate?
Original/derived/index/graph/summary/cache records under retention rules, with prompt access blocking and tracked completion.

### Q149. How do you prove disaster recovery?
I run restore drills and measure recovery objectives instead of assuming that having backups is enough.

### Q150. What is the strongest interview habit?
I state assumptions, draw the data path, explain trade-offs, name failure modes and propose measurable evidence of success.
