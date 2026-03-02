# RELIABILITY.md

## Monitoring & Alerting

[Define how we know if the system is healthy.]

## Error Handling Policy

[Standards for retry logic and fallback mechanisms.]

## Continuous Reliability (The Ralph Loop)

- **Garbage Collection**: Recurring background tasks should scan for architectural deviations or stale documentation and open "Cleanup" loops.
- **Agent Drift Detection**: Agents should periodically verify that the current codebase still adheres to the "Laws" in `ARCHITECTURE.md`.
- **Debt Pay-down**: Use the `docs/exec-plans/tech-debt-tracker.md` as a backlog for background agents to refactor in the Ralph Loop.
