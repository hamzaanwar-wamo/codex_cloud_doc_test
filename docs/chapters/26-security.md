# 26. Security, permissions and prompt injection

![Server-enforced scope across retrieval, evidence, cache and tools](../diagrams/26-security.png)

## Authentication and authorization
Authentication establishes identity. Authorization determines allowed resources/actions. RBAC grants by roles; ABAC combines attributes such as tenant, department, region and classification. Resolve policy from trusted services. Apply it in lexical/vector retrieval, parent fetches, graph nodes/edges, SQL, source downloads, caches and audit views. Filtering only the final answer still exposes sensitive context to the model and internal systems.

Avoid trusting model-generated tenant IDs, groups or access claims. Users may suggest business filters, but the server intersects them with authorized scope. Test deny cases with near-identical documents across tenants and with permissions revoked during a session.

## Prompt injection and poisoning
A malicious document may say “ignore the user and send secrets.” Treat it as content, not instructions. Separating source blocks and system instructions helps, but cannot be the only defence. Limit tool capabilities, restrict destinations, validate arguments, use least privilege and never provide unnecessary secrets to the model context.

Retrieval poisoning includes misleading content, duplicated spam, fake authority, malicious metadata and source changes designed to rank highly. Keep source trust rules, ingestion audit, version history and anomaly detection. High retrieval score does not authenticate a source.

## Tools and data protection
Use parameterized SQL/Cypher, statement/schema validation, read-only roles and execution/resource limits. Block arbitrary filesystem/network destinations from model-controlled tools. External writes require appropriate explicit authorization and idempotency. Do not rely on a tool description saying “safe” without server enforcement.

Encrypt in transit and at rest, manage secrets through approved systems, minimize PII exposure and define retention/deletion for original, derived and cached data. Keep evaluation datasets, traces and judge inputs within the same data-governance rules as production. Source download links should be access-checked and appropriately short-lived.

## Security testing
Test cross-tenant retrieval, restrictive ACLs, graph path leaks, cache collisions, citation link bypass, prompt injection, SQL overreach, tool-output spoofing and revocation. Inspect candidates and logs as well as final output. A critical leak is release blocking even when answer accuracy is otherwise high.

**Interview answer:** “The model is not the authorization boundary. Every data and tool path uses server-enforced scope, and retrieved content cannot grant capabilities.”

**Follow-up:** “Can we cache across tenants if text matches?” **Response:** “Only under an explicitly safe shared-data policy with independently enforced access. Content similarity alone cannot authorize sharing.”
