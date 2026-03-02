# QUALITY_SCORE.md

## Definition of Quality

[Define what a 10/10 PR looks like.]

## Metrics

- [Requirement 1]
- [Requirement 2]
- Test coverage requirements.
- Linting standards.

## Ralph Loop Satisfice (Exit Criteria)

An agent may only consider a task "Done" when:

1. **Self-Review Passes**: The agent has explicitly checked the diff against `ARCHITECTURE.md`.
2. **Automated Verifiers are Green**: All tests, linters, and type-checkers pass in the local environment.
3. **Agent-Legibility maintained**: Any new logic is documented in the code or `/docs` such that another agent could maintain it.
4. **Pottery Wheel Iteration**: If the initial solution was rejected by a verifier, the agent has performed at least one cycle of self-correction before reporting status.
