# 18. Grounded answer generation and safe release

![Prompt construction, answer validation and verified release](../diagrams/18-generation.png)

## Prompt construction
Separate trusted instructions, user question, optional conversation context and untrusted source blocks. Give each source a stable citation ID, source/version, effective date and relevant text. Tell the model to use only supplied evidence for factual source-dependent claims, preserve qualifiers and cite supported claims. Document instructions such as “ignore all previous rules” are data, not authority.

Prompting is one defence. The server must enforce access, tool capability and output constraints. Do not depend on the model to avoid retrieving another tenant's data after it has already been exposed.

Example context block: `SOURCE E1 | HR-42 v3 | effective 2027-01-01 | page 8 | [original passage]`. The answer cites E1; a server resolves E1 to the authorized document version. Never accept a model-invented source ID just because it looks well formatted.

## Numerical and temporal reasoning
For finance, preserve units, reporting period, row/column labels and currency. Use a deterministic tool for arithmetic, then explain inputs and assumptions. “Retention changed from 30 to 90 days” requires evidence for both old and new values and correct effective dates. A valid 2027 policy may not answer a question about 2026.

For multi-document synthesis, make the joins explicit. If one source says Atlas uses Ledger and another says Orion supplies Ledger, check that identifiers and dates refer to the same service. Shared names alone are weak join evidence.

## Structured output and revision
Use a schema for answer text, citation references, supported claims and unresolved gaps. Validate types and citation membership. Then verify factual claims. Schema-valid is not factually correct. If verification fails, revise using the identified gap or abstain. Do not keep regenerating until one judge happens to approve.

Conversation summaries should preserve uncertainty. A prior assistant statement can be wrong and should not become a new authoritative source. Retrieve current evidence for follow-ups and re-check permissions.

## Streaming and release
Streaming tokens improves perceived latency but can expose unverified content. For high-risk use, verify before release or release only independently verified segments. A later correction cannot make an already exposed secret or false claim disappear. Measure first-token time, verified-first-content time and total completion separately.

**Interview answer:** “I treat generation as a source-constrained drafting step, followed by deterministic validation and claim support checks. The output contract includes what cannot be established.”

**Follow-up:** “Can stronger prompting replace a verifier?” **Response:** “It can improve behaviour, but it is not an independent measurement. I still test and verify important claims according to the risk profile.”


## Additional visual walkthrough

![An ordered request/response sequence across system boundaries](../diagrams/36-query-sequence.png)
