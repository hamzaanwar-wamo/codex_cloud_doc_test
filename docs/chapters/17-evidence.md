# 17. Evidence verification: relevance is only the beginning

![Claim-to-source verification with conflict and abstention branches](../diagrams/17-evidence.png)

## Five independent checks
Relevance: Is this about the question? Applicability: Correct tenant, person group, jurisdiction and effective date? Authority: Is this an approved source or an informal note? Sufficiency: Are all required facts and exceptions present? Support: Does the evidence actually entail each material claim? A source can pass one and fail another.

For A, “Leave policy” is relevant. A 2025 policy is not necessarily applicable in 2027. An unofficial Slack explanation is not necessarily authoritative. A cap alone may not establish eligibility. A correct citation ID does not prove the cited passage supports the sentence.

## Data and workflow
Precompute source provenance, versions, effective dates, authority labels, hashes, source spans and optionally extracted facts. At runtime identify required facts, select applicable evidence, detect contradictions, generate a draft, extract material claims, map them to source spans and verify. Store claim verdicts and source references with verifier/prompt/index versions. A previous verdict is invalid when source, scope or claim changes.

```json
{
  "claim_id":"c1", "claim":"Eligible staff may carry five days",
  "evidence":[{"chunk_id":"hr42:v3:s7:c2","page":8,"span":[50,110]}],
  "valid_at":"2027-01-01", "verdict":"supported",
  "checks":["date","eligibility","entailment"],
  "verifier_version":"rules-judge-v1", "request_id":"r17"
}
```

The fact and offsets are illustrative. Production offsets must map to actual stored source text and remain stable for that version. Avoid retaining sensitive claim text unnecessarily in audit systems.

## Algorithms and limitations
Rules verify citation membership, identifiers, dates, units and arithmetic. NLI models estimate entailment/contradiction for premise-hypothesis pairs. LLM judges can evaluate multi-passage support with a strict schema. Both can miss negation, tables, temporal assumptions and invalid joins. Judge output needs validation and comparison to human labels. Self-consistency across several generated answers is not external evidence of correctness.

Weighted evidence coverage can be sum of weights of supported required facts / sum of weights of all required facts. Define facts and weights before scoring. If the required list is wrong, high coverage is misleading. For three equally weighted facts—cap, eligibility, expiry—supporting two gives 2/3, even if many duplicate passages repeat the cap.

Do not multiply retrieval and verifier scores as if they were independent calibrated probabilities. Build a held-out answerability dataset, compare score combinations to human judgments and select an operating point for wrong-answer risk versus coverage.

## Conflict and abstention
Resolve conflicts using explicit authority, applicable scope and effective dates. A newer upload does not always supersede an approved policy. If authority remains unresolved, show the conflict with citations or abstain. If one subquestion is supported, return it separately from the unsupported part. “I could not establish contractor eligibility from the available sources” is better than an invented condition.

**Interview answer:** “I verify material claims against applicable original sources, not just that a passage has a high retrieval score.” **Follow-up:** “What is the latency cost?” **Response:** “It depends on claim count and verifier choice. I batch checks, use deterministic checks where possible, measure the critical path and verify before releasing high-risk claims.”

## Worked claim audit
Draft: “Every Pakistan worker can carry five days into 2027 because management wants to reduce burnout.” Evidence: approved text says “eligible permanent employees may carry up to five days,” with a contractor exclusion; no rationale is provided. Break the draft into claims: all workers eligible; cap five; applies to 2027; burnout rationale. The first overgeneralizes, the second may be supported with “up to,” the third requires effective-date evidence, and the fourth is unsupported. The repair is a narrower answer with eligibility conditions and no invented rationale, not merely another citation.

Verification pseudocode:
```python
# Illustration: each adapter requires its own validation and calibration.
for claim in material_claims(draft):
    spans = map_to_original_sources(claim, authorized_context)
    if not spans or not applicable(spans, question_time, scope):
        mark_unsupported(claim)
    elif deterministic_check_available(claim):
        record(rule_check(claim, spans))
    else:
        record(calibrated_entailment_check(claim, spans))
if unresolved_conflict() or missing_required_fact():
    revise_supported_parts_or_abstain()
```
A claim extractor can miss claims, and a mapping model can pick the wrong span. Evaluate those substeps too. Report unsupported-claim rates under a declared claim segmentation policy, rather than treating the verifier's own count as perfect truth.
