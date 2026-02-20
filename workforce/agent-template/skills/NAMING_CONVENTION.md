# Skill Naming Convention

Use a consistent, intent-first naming format for all skills.

## Format

`<domain>-<artifact>-<role>`

- Use lowercase kebab-case only.
- Use 2-3 tokens (3 preferred for new skills).
- Keep names capability-focused, not framework/tool-focused.

## Token Meanings

- `domain`: area of work (for example: `git`, `spec`)
- `artifact`: primary object handled (for example: `implementation`, `peer`, `adr`)
- `role`: action/capability (for example: `planner`, `reviewer`, `manager`, `creator`)

## Current Examples

- `git-commit`
- `git-pr-creator`
- `git-worktrees`
- `spec-adr-manager`
- `spec-implementation-planner`
- `spec-prd-creator`
- `spec-peer-reviewer`

## Rule for Future Skills

- If the skill is product/spec/planning/review architecture work, prefer the `spec-` prefix.
- If the skill is source-control workflow, use the `git-` prefix.
- Keep folder name and `name:` in `SKILL.md` identical.
