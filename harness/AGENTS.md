# AGENTS.md

## Mission

[Define the high-level mission for the AI agents in this repository.]
Operate autonomously within the **Ralph Loop** to drive tasks from intent to completion with zero architectural drift and maximum quality.

## Directives

- [Instruction 1]
- [Instruction 2]
- **The Ralph Loop Protocol**:
    - **Self-Correction First**: Before submitting any change, you MUST review your own work against the `ARCHITECTURE.md` and `QUALITY_SCORE.md` invariants.
    - **Throw it back on the pottery wheel**: If a test fails or a linting error occurs, do not ask for help immediately. Iterate on the solution until the local environment is green.
    - **Agent-to-Agent Review**: Simulate or request reviews from specialized sub-agents. Treat human feedback as a high-priority constraint to be integrated into the next iteration of the loop.
    - **Context Engineering**: Use `gh`, local scripts, and repository-embedded skills to gather context. Do not guess; verify facts by reading the codebase.
    - **Small Batches**: Perform one discrete task per loop.

## How to use this repo

[Guide the agent on where to find types, logic, and tests.]
1. **Perceive**: Read `docs/product-specs/` and `docs/exec-plans/active/` to understand the current mission.
2. **Understand Laws**: Consult `ARCHITECTURE.md` for dependency rules and `QUALITY_SCORE.md` for the definition of "Done."
3. **Leverage Skills**: Check the `/skills` directory for specialized capabilities. Each skill folder contains a `SKILL.md` (metadata & instructions) and a `scripts/` folder (logic).
4. **Execute**: Implement the change in small increments.

## Repository-Embedded Skills (/skills)

- **Convention**: Each skill is a folder containing a `SKILL.md`.
- **Two Skill Types**:
    1. **Instructional Skills**: Prompt-based strategies. Follow the rules in `SKILL.md` using your internal capabilities (e.g., `prd-creator`).
    2. **Executable Skills**: Script-based tools. Run the logic in the `scripts/` folder (if present).
- **Discovery**: Read `SKILL.md` metadata (YAML) to determine if a skill applies to your current task.
4. **Verify**: Run the full verification suite (`npm test`, `lint`, etc.).
5. **Close the Loop**: Once all checks pass and the agent-review is satisfied, open a PR or update the execution plan to `completed`.
