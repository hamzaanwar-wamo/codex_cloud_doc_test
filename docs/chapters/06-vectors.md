# 6. Embeddings and vector search internals

## Representations
Dense embeddings encode text into fixed-length vectors. Sparse learned representations assign weights to vocabulary features. Multi-vector/token representations retain several vectors per passage for more detailed matching. Do not treat these as interchangeable storage or scoring formats.

A bi-encoder embeds queries and documents separately, allowing document representations to be precomputed. A cross-encoder reads the pair together at runtime and is normally used after candidate retrieval. Follow the model's required prefixes, tokenizer, maximum input length and pooling method. Silent truncation can drop the answer before indexing.

![Offline encoding, online ANN search and exact recall checks](../diagrams/06-vectors.png)

## Geometry and worked math
dot(q,d) = sum_i q_i*d_i. cosine(q,d) = dot(q,d)/(norm(q)*norm(d)). For q=(1,0) and d=(1,1), dot=1 and cosine=0.707. Euclidean distance=sqrt(sum_i(q_i-d_i)^2)=1. With unit-normalized vectors, squared Euclidean distance=2-2*cosine. These rankings can agree under normalization, but raw dot products also reward magnitude. A cosine score is not a probability of truth. Handle zero vectors explicitly.

## Approximate nearest neighbours
Exact search compares against all eligible vectors; useful as an evaluation reference on manageable samples. ANN skips much of that work and trades recall for speed.

HNSW builds a layered proximity graph. Search starts at sparse upper layers, descends toward neighbours, then explores a candidate frontier. Construction connectivity and construction effort affect memory/build quality; search effort affects runtime recall. Parameter names differ by implementation.

IVF clusters vectors into cells. At query time, probe selected cells, then rank vectors within them. More probed cells usually improve recall and increase work. Poor training data or embedding drift can make partitions uneven. PQ approximates vectors by codebook entries for subvectors, reducing memory at a possible accuracy cost. Scalar quantization lowers per-dimension precision. Evaluate both ANN recall and downstream answer quality.

## Filtering and model migrations
Post-filtering a small global candidate set can lose all permitted hits for a restrictive tenant. Use supported filter-aware search, appropriate partitioning or exact search for tiny eligible sets. Test realistic high- and low-selectivity ACLs; unfiltered recall is insufficient.

When changing model/dimensions/normalization, build a new versioned index and query with its matching model. Never mix incompatible spaces just because dimensions match. Dual-run evaluation, publish the new manifest, then retire the old index. Track language/domain drift and changed score distributions.

| Option | Useful starting context | Operational question |
|---|---|---|
| FAISS | Embedded/local search library | Who supplies persistence, access control, serving and recovery? |
| pgvector | PostgreSQL-centric application | How do filtered ANN, SQL load and index growth interact? |
| Qdrant / Milvus | Dedicated vector workloads | How do filtering, partitioning, replication and updates behave? |
| Pinecone | Managed vector service | What are current cost, isolation, limits and residency options? |
| Weaviate | Schema/object-oriented search needs | Which search modules and deployment guarantees are required? |
| OpenSearch | Lexical and vector in one search platform | How do shard layout and hybrid features behave at the chosen version? |

**Interview answer:** “I select the embedding on representative multilingual/domain queries, then select ANN parameters against an exact-search baseline. I choose a database on filters, operations and recovery as well as recall/latency.”

**Failure:** A model upgrade reduces exact-ID retrieval. **Action:** Slice evaluation by query type, retain lexical search, and compare tokenization/truncation and domain representation before blaming ANN.
