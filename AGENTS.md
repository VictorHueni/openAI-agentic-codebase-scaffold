# AGENTS.md — Scaffold Development

## Mission

Build and maintain the **Harness Engineering** scaffold — a portable, self-contained template that gives any project an AI governance structure out of the box.

## Directives

- **Keep `harness/` self-contained**: No file inside `harness/` may reference `../` (except template AGENTS.md files which deploy outside harness).
- **True Dogfooding**: This repo itself uses the harness pattern — root governance for the scaffold project, `harness/` for the portable template.
- **The Ralph Loop Protocol**:
    - **Self-Correction First**: Before submitting any change, review your own work against `ARCHITECTURE.md` and `QUALITY_SCORE.md` invariants.
    - **Throw it back on the pottery wheel**: If a test fails or a linting error occurs, iterate until the local environment is green.
    - **Agent-to-Agent Review**: Simulate or request reviews from specialized sub-agents. Treat human feedback as a high-priority constraint.
    - **Context Engineering**: Use `gh`, local scripts, and repository-embedded skills to gather context. Do not guess; verify facts by reading the codebase.
    - **Small Batches**: Perform one discrete task per loop.

## How to use this repo

1. **Perceive**: Read `docs/product-specs/` and `docs/exec-plans/active/` to understand the current scaffold mission.
2. **Understand Laws**: Consult `ARCHITECTURE.md` for the two-layer structure and `QUALITY_SCORE.md` for the definition of "Done."
3. **Leverage Skills**: Check `harness/workforce/agent-template/skills/` for specialized capabilities. Each skill folder contains a `SKILL.md`.
4. **Execute**: Implement the change in small increments. One increment per commit.

## Two-Layer Structure

- **Root** (`/`): The scaffold project itself — governance, working docs, and the harness template.
- **`harness/`**: The portable template product — copy it into any project for instant AI governance.
- **`docs/`**: Scaffold working docs — PRDs, exec plans, and design docs for building the scaffold.

## Repository-Embedded Skills (/skills)

- **Convention**: Each skill is a folder containing a `SKILL.md`.
- **Two Skill Types**:
    1. **Instructional Skills**: Prompt-based strategies. Follow the rules in `SKILL.md` using your internal capabilities.
    2. **Executable Skills**: Script-based tools. Run the logic in the `scripts/` folder (if present).
- **Discovery**: Read `SKILL.md` metadata (YAML) to determine if a skill applies to your current task.
- **Verify**: Run the full verification suite (`npm test`, `lint`, etc.).
- **Close the Loop**: Once all checks pass, open a PR or update the execution plan to `completed`.
