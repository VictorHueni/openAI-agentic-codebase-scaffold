# Scaffold Architecture

## Purpose
This file defines architecture constraints for scaffold-development work only.
It does not replace the root `ARCHITECTURE.md` shipped to end users.

## Layers
1. **Policy Layer**: root governance files (`AGENTS.md`, `QUALITY_SCORE.md`, `SECURITY.md`, `RELIABILITY.md`).
2. **Template Layer**: static onboarding assets (`workforce/templates/**`, `workforce/agent-template/skills/**`).
3. **Automation Layer**: executable onboarding logic (`scripts/workforce.py`).
4. **Generated Runtime Layer**: created at execution time (`.gemini/`, `.claude/`, `.copilot-instructions/`).

## Dependency Rules
1. Template Layer must stay data-only; no runtime code under template folders.
2. Automation Layer may read Policy and Template layers, but Policy/Template must not import runtime output.
3. Generated Runtime Layer is disposable and must remain gitignored.
4. `scaffold-dev/**` docs describe implementation intent and must not be runtime dependencies.

## Invariants
1. No circular dependencies between script modules.
2. Onboarding is deterministic from manifests and templates.
3. Skills source of truth remains `workforce/agent-template/skills`.
4. `hire`/`fire` operations are idempotent where possible.
