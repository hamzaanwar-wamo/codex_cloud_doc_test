# 21. Answer, evidence and safety evaluation

![Independent answer dimensions and calibrated release gates](../diagrams/21-answer-metrics.png)

## Score dimensions separately
Correctness asks whether the answer matches the expected facts and calculations. Faithfulness asks whether supplied evidence supports its claims. A faithful answer can still be wrong if the source is wrong. Relevance asks whether the response addresses the question. Completeness checks required facts and exceptions. Citation validity checks that cited sources exist and are accessible; citation support checks that they actually substantiate claims.

Define citation precision as correctly supported/attributed cited claims divided by cited claims, and citation recall as material claims with adequate supporting citations divided by material claims requiring citations. Choose a consistent claim/citation unit; multiple citations on one claim require an explicit attribution policy. Do not silently mix document-level and claim-level metrics.

## Example rubric
| Dimension | Strong answer | Failure example |
|---|---|---|
| Correctness | Cap, group and date match truth | Right cap, wrong employee group |
| Support | Each material statement is entailed | Plausible rationale not stated in sources |
| Completeness | Includes exceptions and missing information | Leaves out contractor exclusion |
| Citation | Resolves to supporting applicable span | Real document, unrelated paragraph |
| Abstention | Answers supported parts, flags gaps | Guesses when evidence is absent |
| Authorization | No out-of-scope exposure anywhere | Tenant text in output, cache or logs |

For risk-weighted release gates, define tolerances before the experiment and justify them by harm and label uncertainty. Do not propose one universal “faithfulness above 0.8” rule. A single critical access breach can block release even if average language quality is high.

## Judges and calibration
Use deterministic checks for schema, IDs, dates, arithmetic and citation membership. Use calibrated LLM/NLI judges for semantic support, plus human review for difficult or high-risk cases. Control judge model/prompt versions and avoid feeding confidential evidence to an unauthorized evaluator. Test disagreement rates and false approvals. RAGAS, DeepEval, TruLens and LangSmith can help organize scoring/traces; their metric names and semantics are not automatically equivalent.

Answerability calibration compares model/system signals to held-out correct/incorrect labels. Reliability plots and risk-coverage curves help choose where to abstain. Confidence from a generator or a cosine score is not enough.

**Interview answer:** “I never compress correctness, support, completeness and authorization into one number without also reporting the underlying dimensions and critical failures.”

**Follow-up:** “What if the judge says supported but experts disagree?” **Response:** “Adjudicate, inspect the judge rubric, record the failure mode and recalibrate. The judge is a measurement instrument, not the ground truth.”
