# QUALITY_SCORE.md — Scaffold Quality Bar

## Definition of Quality

A scaffold change is "Done" when:
- `harness/` remains self-contained (`grep -rn "\.\.\/" harness/` only matches template AGENTS.md files).
- Templates are clean stubs with no scaffold-specific content.
- `workforce.py` compiles and dry-run passes.
- All governance files exist in both root (scaffold-specific) and `harness/` (clean templates).

## Metrics

- `python -m py_compile harness/scripts/workforce.py` exits 0.
- `python harness/scripts/workforce.py hire claude --dry-run` targets `.claude/` at repo root.
- `grep -rn "\.\.\/" harness/ --include="*.md" --include="*.py"` only matches `workforce/templates/*/AGENTS.md`.
- No file references `scaffold-dev/` anywhere.

## Ralph Loop Satisfice (Exit Criteria)

An agent may only consider a task "Done" when:
1. **Self-Review Passes**: The agent has explicitly checked the diff against `ARCHITECTURE.md`.
2. **Automated Verifiers are Green**: All tests, linters, and type-checkers pass in the local environment.
3. **Agent-Legibility maintained**: Any new logic is documented in the code or `docs/` such that another agent could maintain it.
4. **Pottery Wheel Iteration**: If the initial solution was rejected by a verifier, the agent has performed at least one cycle of self-correction before reporting status.
