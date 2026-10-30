# 22. Agent evaluation: outcomes and trajectories

![Score both the final answer and the path taken](../diagrams/22-agent-eval.png)

## What to measure
Task success, correct tool selection, valid arguments, permission compliance, evidence acquisition, recovery, termination, final claim support, elapsed time, tokens and cost. Track unnecessary calls and repeated no-progress steps. A correct final answer can hide an unauthorized intermediate lookup or an unsustainable cost.

Do not require one exact action sequence when several safe paths can solve the task. Evaluate required evidence and constraints, then compare efficiency. For deterministic tools, keep replayable fixtures and fault injection. For model choices, pin versions/configuration and repeat where nondeterminism materially affects conclusions.

## A concrete trace
Task: Find Atlas vendors and compare old/new retention obligations. Step 1: Resolve Atlas and retrieve service/vendor relationships. Step 2: Fetch new policy. Evidence checker finds no historical baseline. Step 3: Fetch historical policy by version. Step 4: Verify affected vendors and changed values. Finish with supported claims and citations.

The trace succeeds only if every relation and both policy versions are supported, tool calls remain authorized, and budgets are respected. If Step 3 returns no historical source, “could not establish the previous obligation” may be the correct bounded outcome. A fabricated comparison is not success.

## Fault and adversarial testing
Inject a timeout, empty results, malformed tool output, irrelevant high-score text, prompt injection, stale cache, revoked permission and contradictory evidence. Confirm safe recovery or bounded failure. Tool descriptions and retrieved documents cannot grant new capabilities. Store structured action outcomes and evidence references; do not require access to private reasoning traces.

Compare against a fixed workflow using the same tools. Added autonomy should improve the target query slice enough to justify extra latency, spend and debugging difficulty. Report distributions and failure categories, not only average success.

**Interview answer:** “I score whether the task was solved safely and with sufficient evidence, then whether the chosen actions were efficient and recoverable.”

**Follow-up:** “Can a shorter trace score better?” **Response:** “Yes, when it meets the same evidence and safety requirements. More steps are not more intelligence.”
