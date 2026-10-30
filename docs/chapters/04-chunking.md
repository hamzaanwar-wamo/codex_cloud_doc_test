# 4. Chunking: boundaries, meaning and retrieval units

## What chunking actually changes
A chunk is a retrievable unit, not necessarily the final context unit. Its size changes term statistics, semantic specificity, number of vectors, reranking cost and citation granularity. The right boundary keeps a fact with its conditions: “five days” without “eligible permanent staff only” is incomplete evidence.

![Chunking decision tree and parent-child expansion](../diagrams/04-chunking.png)

## Families and internal working
| Technique | How boundaries are chosen | Cost and main failure |
|---|---|---|
| Fixed characters | Cut every n characters | Cheap; token length varies and sentences break |
| Fixed tokens | Tokenize, take bounded windows | Predictable budget; semantic boundaries ignored |
| Sliding window | Advance by size minus overlap | Repeated facts raise storage and duplicate context |
| Sentence/paragraph | Detect language-aware boundaries, then pack | Natural units; abbreviations and long paragraphs need handling |
| Recursive | Try heading, paragraph, sentence, then token splits | Strong baseline; quality depends on parser/separators |
| Heading/Markdown | Preserve heading paths and blocks | Good structure; weak or fake headings mislead |
| HTML/DOM | Traverse meaningful content nodes | Navigation/ads can pollute text; reading order matters |
| JSON | Split by records or key subtrees; retain key paths | Splitting values from keys destroys interpretation |
| Table-aware | Keep headers/units with row groups | Repeated headers add tokens; huge tables need SQL |
| AST/code | Function/class/symbol boundaries plus file context | A function may depend on imports or another file |
| Semantic | Split where adjacent text embedding similarity falls | Extra inference; topic change is not always a safe fact boundary |
| Proposition | Extract atomic factual statements | Precise matching; extraction may omit conditions or invent facts |
| Parent-child | Index small children and link to larger parents | Better recall/reading balance; expansion needs a budget |
| Sentence-window | Index sentence; fetch nearby sentences | Context can cross headings or authorization boundaries |
| Hierarchical | Store document -> section -> chunk relationships | Multiple levels help routing but create update complexity |
| Contextual | Prefix chunk with document/section explanation | Generated prefix can be false; preserve original source |
| Late chunking | Encode long text, then pool token vectors by span | Requires suitable model/token representations; not ordinary post-embedding splitting |
| LLM/agentic | Ask model to identify coherent units | Cost, repeatability and provenance validation required |
| Multimodal | Link text, image regions and table areas | Need modality-compatible encoders and location metadata |
| Adaptive/query-aware | Select or reshape passages after query arrives | More runtime latency and no single fixed index unit |
| Document/section | Index a larger logical unit directly | Useful for short content/routing; mixed topics reduce precision |

## Semantic breakpoints, precisely
Encode adjacent sentences or small sentence windows, then compute distance d_i = 1 - cosine(e_i, e_(i+1)). A high distance suggests a topic change. A percentile method splits above a selected distance percentile. A standard-deviation method splits above mean(d) + a x std(d). Neither threshold guarantees meaningful boundaries. Percentiles can force splits in a uniform document; standard-deviation rules can produce none. Enforce minimum/maximum sizes and preserve tables or clauses as protected spans.

## Size and overlap experiment
Compare 128, 256, 400, 512, 800 and 1024 tokens using the actual tokenizer. Those are experimental candidates, not default recommendations. For each, measure candidate recall, required-fact coverage, final answer quality, context tokens, index size and P95 latency. Evaluate exact IDs, explanations, tables and multi-hop questions separately.

Approximate window count for L tokens, size s and overlap o is ceil((L-s)/(s-o))+1 when L>s and 0<=o<s. A 2,000-token text with size 500 and overlap 100 produces 5 windows: starts 0,400,800,1200,1600. The final one may be shorter. Exact counts vary when structure changes boundaries.

```python
# Illustrative token-window primitive; tokenizer supplied by caller.
def windows(tokens, size, overlap):
    if not 0 <= overlap < size:
        raise ValueError("Require 0 <= overlap < size")
    start = 0
    while start < len(tokens):
        yield tokens[start:start + size]
        if start + size >= len(tokens):
            break
        start += size - overlap
```

## Stored vs runtime
Persist chunk ID, original text, token count, source/page offsets, parent ID, heading path, version and access metadata. Precompute embeddings for the indexed representation. At runtime retrieve small children, authorize parent access, expand only useful context, then deduplicate overlapping spans. Do not send every retrieved parent in full.

**Interview answer:** “I start with structure-aware recursive chunking, test sizes and overlap, then add parent expansion for observed boundary failures. Parent-child and recursive are compatible: one defines retrieval/context levels, the other defines boundaries.”

**Follow-up:** “Why not semantic chunking everywhere?” **Response:** “It adds processing and threshold sensitivity. I need evidence that it improves full-fact retrieval over the simpler baseline, including exceptions and tables.”


## Additional visual walkthrough

![A chunk tree separates retrieval children from context parents](../diagrams/37-chunk-tree.png)

## Boundary algorithms in practical detail

### Fixed, recursive and structure-aware example
Suppose a source says: heading “Carry forward”; paragraph “Eligible permanent employees may carry five days”; paragraph “Contractors are excluded”; a table lists expiry dates. A fixed window may cut before the exception. A recursive splitter first keeps the section, then packs paragraphs while under its limit. A structure-aware variant treats the table as protected and repeats its header in each row group. Store the heading path on every child so a hit can expand to the right context.

For a recursive implementation, represent parsed blocks as `(type, text, source_span, heading_path)`. Try to pack whole blocks. If one block exceeds the limit, choose a type-specific split: sentences for prose, row groups for a table, statements/symbol blocks for code. Only fall back to raw token cuts when no safe structural boundary exists. Every derived span needs a valid source mapping. This is why parsing quality precedes clever chunking.

### Sentence, paragraph and window example
Sentence splitting needs language-aware handling for abbreviations, initials and decimal values. A naive split on `.` can break “Dr. Khan,” “U.S.” and “3.5%.” Pack sentences until the token cap, then optionally retain a short trailing overlap. Sentence-window retrieval stores a sentence ID and neighbours rather than permanently duplicating every window. At query time fetch neighbour spans within the same permitted section/version and merge overlapping windows.

### Semantic example
For adjacent window similarities [0.92, 0.90, 0.41, 0.88], distances are [0.08, 0.10, 0.59, 0.12]. The large 0.59 suggests a possible boundary. It is not proof: the second passage might contain an exception using different vocabulary. Evaluate complete clause coverage and not only perceived topic coherence. Percentile thresholds depend on available distances; a very short document provides poor distribution estimates.

### Proposition and contextual example
Original: “Permanent Pakistan staff may carry five days, unless their contract states otherwise.” A safe proposition preserves subject, region, cap and exception. “All staff may carry five days” is an extraction error. Contextual enrichment might prefix “HR-42 v3, Pakistan leave rules, effective 2027.” If this prefix comes from a wrong summary, the indexed meaning becomes misleading even though the source passage was correct. Persist original and enrichment separately, with provenance.

### Late chunking example
Ordinary chunking encodes `[paragraph A]` and `[paragraph B]` separately. Late chunking encodes the longer combined text first so contextual token representations for B can reflect an entity named in A, then pools token spans into chunk vectors. This requires access to appropriate token-level model outputs and a pooling method consistent with the model. It is limited by the encoder's context window and may not work through a simple hosted endpoint that returns only one vector per input.

### Code, JSON and table examples
An AST splitter identifies a function/class and retains symbol/file metadata. If a function exceeds the limit, split along syntax blocks while retaining signature and necessary context; do not execute source code during parsing. A JSON splitter emits records with key paths such as `employees[17].leave_policy`, preserving units and object identity. A table splitter repeats column labels like `Region | Employee type | Cap (days) | Effective date`; keep a row's values together and cite original cells/coordinates.

### Multimodal and adaptive example
An image chunk may include a page crop, caption, OCR text and bounding box. A multimodal encoder matches visual content while the answer cites the original region. Validate visual facts with the appropriate model/tool; an OCR-only route cannot see a chart's unlabeled trend reliably. Adaptive chunking may retrieve a coarse section, then choose query-relevant spans at runtime. It saves final context tokens at the cost of another processing step; cache only under correct query/scope/version semantics.

### How to compare all methods fairly
Keep the same document versions and golden questions. Count required facts, not just relevant chunk IDs, because changing boundaries changes IDs. Report indexing/model calls, raw and derived storage, candidate token totals, final context size and answer metrics. A method that produces more labeled chunks can look better under raw chunk recall while adding no new supported facts. Include answer-spans that cross boundaries, long exceptions, tables, multilingual content and malformed structure.
