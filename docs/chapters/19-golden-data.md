# 19. Golden datasets and annotation

![Building a versioned evaluation set without circular labels](../diagrams/19-dataset.png)

## Define the unit of evaluation
A question alone is incomplete. Store question, authenticated test identity/scope, requested date, corpus version, expected answer or rubric, required facts, supporting source/chunk IDs, acceptable abstention and failure category. Evidence labels should refer to versioned source text. A source update can legitimately change the answer.

Include factual, explanatory, exact-ID, multi-document, multi-hop, temporal, conflicting, unanswerable, unauthorized, adversarial, conversational, OCR, tables and agent-research cases. Include negatives that look relevant but are outdated or inapplicable. Test restrictive permissions rather than only all-access admin users.

Example label: question A; scope=employees-pk; valid_at=2027-01-01; required facts=[cap, eligibility, expiry]; acceptable source versions=[hr42:v3]; expected abstention if the expiry source is absent. Do not label an invented company policy as real ground truth; construct a synthetic corpus explicitly for that exercise.

## Annotation process
Sample from real workloads after privacy review. Add expert-designed edge cases and synthetic cases for gaps. Have annotators independently label difficult examples, adjudicate disagreements and record ambiguous questions. Distinguish missing labels from truly irrelevant passages. Human relevance labels can be incomplete; retrieval metrics should state that limitation.

Keep tuning and final test sets separate. Avoid writing synthetic questions directly from only one system's retrieved chunks, which biases evaluation toward that retriever. Avoid allowing the answer-generating model to be the only judge of its own success. LLM assistance can speed labeling, but human calibration is needed for meaningful quality claims.

Version data, corpus manifests, label guidelines and scoring code together. Use held-out customer/tenant/source/time slices where appropriate to test generalization. Protect sensitive examples and keep retention consistent with policy.

**Interview answer:** “My golden set is a versioned contract for the task, identity and evidence, not just question-answer text. It includes unanswerable and unauthorized cases.”

**Follow-up:** “How much data is enough?” **Response:** “Enough to estimate the important slice error rates with useful uncertainty. I start with a manageable expert-labeled set, inspect failures, expand underrepresented slices and report confidence intervals instead of claiming certainty from a small sample.”
