# ARCHITECTURE.md — Scaffold Architecture

## Two-Layer Structure

This repository has two conceptual layers:

1. **Root Layer** (this project): Governance files, working docs (`docs/`), and the harness template. Mission: build the scaffold.
2. **`harness/` Layer** (the product): A portable, self-contained template. Copy it into any project for instant AI governance.

## Harness Internal Layers

1. **Policy Layer**: Governance files (`harness/AGENTS.md`, `harness/QUALITY_SCORE.md`, `harness/SECURITY.md`, `harness/RELIABILITY.md`).
2. **Template Layer**: Static onboarding assets (`harness/workforce/templates/**`, `harness/workforce/agent-template/skills/**`).
3. **Automation Layer**: Executable onboarding logic (`harness/scripts/workforce.py`).
4. **Generated Runtime Layer**: Created at execution time (`.gemini/`, `.claude/`, `.copilot-instructions/`).

## Dependency Rules

1. Template Layer must stay data-only — no runtime code under template folders.
2. Automation Layer may read Policy and Template layers, but Policy/Template must not import runtime output.
3. Generated Runtime Layer is disposable and must remain gitignored.
4. `docs/**` describes implementation intent and must not be runtime dependencies.

## Invariants

- **Self-Containment**: `harness/` must never reference `../` except in `workforce/templates/*/AGENTS.md` (which deploy outside harness).
- No circular dependencies between script modules.
- Onboarding is deterministic from manifests and templates.
- Skills source of truth remains `harness/workforce/agent-template/skills`.
- `hire`/`fire` operations are idempotent where possible.
