# Senior Full-Stack Engineer Take-Home: Production Change Exercise

## Purpose

This exercise evaluates how you understand and improve an unfamiliar application under a realistic time constraint.

It is not a test of Gaia product knowledge, algorithm memorization, visual polish, or how much code you can generate. We are looking for evidence of senior full-stack judgment: identifying important risks, changing the smallest appropriate surface, preserving data integrity, handling frontend and backend failure states, testing critical behavior, and explaining tradeoffs.

## Timebox

Spend no more than **3 hours of active work**. Stop when the timebox expires, even if your implementation is incomplete. Record your approximate active time and explain what you completed, deliberately deferred, and would do next.

A safe, well-tested partial implementation can score better than a broad implementation that introduces uncertain behavior.

## AI Tool Policy

You may use coding agents, LLMs, documentation, search, and normal development tools.

Include a short `AI_USE.md` stating:

- the tools and models you used;
- what work you delegated;
- at least one suggestion or output you rejected, corrected, or independently verified;
- the validation commands you ran;
- any AI-generated behavior you did not have time to verify.

Do not include private chain-of-thought. We evaluate decisions, understanding, and verification evidence—not prompt-writing style or generated-code volume.

## Scenario

RequestFlow lets employees submit operational change requests and lets assigned reviewers approve or reject them. The basic flow exists, but users have reported stale UI state, duplicate decisions, and inconsistent history.

Improve the request-decision path within the timebox. Treat the code as an application you inherited; do not replace the stack or rebuild the project.

## Business Rules

1. The backend derives the current actor and team membership from the server-owned simulated session.
2. The request body must not be trusted to declare the actor, role, team, or authorization result.
3. Only an assigned reviewer or a member of the assigned reviewer team may decide a request.
4. A requester may not decide their own request, even if they are also a reviewer.
5. Only a `pending` request may transition to `approved` or `rejected`.
6. `approved` and `rejected` are terminal states for this exercise.
7. A rejection requires a non-empty reason. An approval note is optional.
8. Retrying the same logical command must not create another decision or history event.
9. If two different decisions race, exactly one may win. The other caller receives a typed conflict containing the safe current state.
10. The request transition and decision-history event commit atomically.
11. The UI reconciles with server truth after success, denial, conflict, timeout, or unexpected error.

## Required Work

### Diagnose And Prioritize

Inspect the existing path before changing it. Prioritize the failures presenting the greatest correctness, authorization, or data-integrity risk. Document important findings you leave unresolved.

### Backend Decision Path

Implement or repair the approve/reject path so the server enforces the business rules. Provide server-owned authorization, typed outcomes, safe retries, a clear concurrency strategy, atomic persistence, and a response contract the frontend can use without inventing state.

Keep `POST /api/requests/{request_id}/decision` as the decision operation. The target request must contain:

```json
{
  "decision": "approved",
  "reason": "optional for approval, required for rejection",
  "idempotency_key": "candidate-generated-command-id",
  "expected_version": 1
}
```

The actor is supplied only through the existing `X-Session-Token` development-session boundary.

You may evolve response schemas and the data model when justified, but document compatibility tradeoffs.

### Frontend Decision Experience

Handle an authorized pending request, decision progress, success, authorization denial, a stale or conflicting decision, timeout, and unexpected failure. A conflict must show current server state and a clear recovery path. Disabling a button is useful UX but is not a correctness boundary.

Preserve basic keyboard access, focus behavior, and understandable errors.

### Decision History

Record one durable history event for the winning terminal decision with request ID, actor ID, decision, note or rejection reason, timestamp, idempotency reference, and resulting version. A failed, unauthorized, or losing attempt must not create a successful terminal-decision event.

### Required Tests

Add or update tests for:

- authorized approval;
- authorized rejection and missing rejection reason;
- self-approval and unauthorized review;
- an idempotent retry;
- competing decisions where only one wins;
- atomic agreement between final state and history;
- frontend denial or conflict without false success.

Test observable invariants, not only implementation details or status codes.

### Engineering Judgment Note

Add `DECISIONS.md`, maximum one page, covering the request path, important risks, authorization/retry/concurrency approach, deliberate deferrals, and next production validation step.

## Out Of Scope

Do not implement real authentication, notifications, integrations, configurable approval chains, terminal-state reopening, deployment infrastructure, a visual redesign, or a framework migration.

## Deliverables

Submit your implementation, backend and frontend tests, updated run instructions if needed, `DECISIONS.md`, `AI_USE.md`, and approximate active time. No demo video or slides are required.

## Evaluation

| Area | Weight |
| --- | ---: |
| Correctness and data integrity | 25% |
| Backend, API, and authorization | 20% |
| Frontend and product behavior | 20% |
| Tests and debugging evidence | 15% |
| Scope and engineering judgment | 15% |
| AI-use discipline and communication | 5% |

## Automatic Failure Conditions

A submission does not pass if verified behavior shows that the backend trusts browser-supplied identity or authorization, an unauthorized user can decide a request, contradictory terminal states can commit, state and successful history disagree, the UI presents false success, negative tests were weakened merely to pass, or critical failing behavior is knowingly presented as complete.

An incomplete feature is not an automatic failure when the implemented path is correct, testable, and honestly described.

## Follow-Up Discussion

Candidates passing the screen will trace a decision end to end, discuss a remaining risk, respond to a small retry/permission/concurrency change, and improve a bounded part of their submission. The goal is to evaluate understanding, verification habits, and safe adaptation—not typing speed.
