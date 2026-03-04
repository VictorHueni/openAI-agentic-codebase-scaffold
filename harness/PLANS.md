# PLANS.md

## Active Roadmap

[Describe the current major milestones.]

## Execution Strategy

[Explain how to move from product spec to code.]

- **Phase 1: Planning**: Define the intent in `docs/exec-plans/active/`.
- **Phase 2: The Ralph Loop**: The agent invokes `ralph-loop-runner` to execute the plan. Each iteration implements one increment in a colocated workspace (`docs/exec-plans/active/NNNN_feature-name/`), passes its test gate, and commits. Status fields (`**Status:** pending | in-progress | done`) on each increment drive progression. Use `ralph.sh` for automated multi-iteration execution.
- **Phase 3: Satisfice**: The loop terminates when `QUALITY_SCORE.md` metrics are hit.
- **Phase 4: Archiving**: Move the plan to `docs/exec-plans/completed/`.
