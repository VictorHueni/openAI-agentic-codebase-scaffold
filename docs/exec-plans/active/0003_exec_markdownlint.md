# Implementation Plan: Markdownlint Full Setup

## Summary

Deliver markdownlint infrastructure across the scaffold: CLI scripts, GitHub Actions CI, and a pre-commit hook via husky/lint-staged.

Reference: `docs/product-specs/` (no standalone PRD — originated from `README.md` line 53 recommendation and `QUALITY_SCORE.md` linting standards)
Architecture constraints: `ARCHITECTURE.md`

Principles:
1. **Tool Choice**: `markdownlint-cli2` — newer, recommended by the markdownlint author, supports JSONC config with comments (ideal for a template repo where rule rationale matters).
2. **Minimal Footprint**: All tooling is devDependencies only; `"private": true` prevents accidental npm publish.
3. **Convention Over Configuration**: Sensible defaults with targeted overrides based on codebase analysis of 28+ markdown files.

---

## Increment Plan

### Increment 01: Create markdownlint config (`.markdownlint-cli2.jsonc`)

Scope:
1. Create the JSONC rule configuration file with comments explaining each rule decision.
2. Configure glob patterns and ignores.

Primary files:
1. `.markdownlint-cli2.jsonc`

Key rule decisions (based on codebase analysis):

| Rule | Setting | Rationale |
|------|---------|-----------|
| MD013 (line length) | **disabled** | Prose-heavy docs; 66+ lines already exceed 120 chars |
| MD024 (duplicate headings) | `siblings_only: true` | Exec plans reuse headings under different parents |
| MD026 (trailing punctuation) | exclude `:()` | Headings like `## Types (required)` are common |
| MD033 (inline HTML) | **disabled** | Template users may need `<details>`, badges, etc. |
| MD036 (emphasis as heading) | **disabled** | Bold text used as visual separators in SKILL.md files |
| MD041 (first-line heading) | **disabled** | 5 SKILL.md files start with YAML front matter |
| All others | **default (enabled)** | Existing files largely conform already |

Test gate:
1. File is valid JSONC.

### Increment 02: Create `package.json` and install dependencies

Scope:
1. Create minimal `package.json` with `markdownlint-cli2`, `husky`, and `lint-staged` as devDependencies.
2. Run `npm install` to generate `package-lock.json`.
3. Verify `.gitignore` already includes `node_modules/`.

Primary files:
1. `package.json`
2. `package-lock.json` (generated)

Test gate:
1. `npm run lint:md` executes without crashing.

### Increment 03: Fix existing markdown lint violations

Scope:
1. Run `npm run lint:md:fix` to auto-fix what can be auto-fixed.
2. Manually fix any remaining violations.
3. Verify zero violations.

Primary files:
1. Various `*.md` files across the repo.

Test gate:
1. `npm run lint:md` exits with code 0.

### Increment 04: GitHub Actions workflow

Scope:
1. Create `.github/workflows/` directory.
2. Create CI workflow that lints markdown on PRs and pushes to `main`.
3. Use `paths` filter so workflow only runs when `*.md` or lint config changes.

Primary files:
1. `.github/workflows/lint-markdown.yml`

Test gate:
1. YAML is valid.
2. Full verification on first PR.

### Increment 05: Husky pre-commit hook

Scope:
1. Run `npx husky init` to create `.husky/` directory.
2. Set `.husky/pre-commit` to run `npx lint-staged`.
3. `lint-staged` config (in `package.json`) runs `markdownlint-cli2` on staged `*.md` files.

Primary files:
1. `.husky/pre-commit`

Test gate:
1. Stage a `.md` file with a violation, attempt commit — pre-commit hook blocks it.
2. Fix violation, re-stage, commit succeeds.

---

## Verification Suite

1. `npm run lint:md` — exits 0 (all markdown clean)
2. `npm run lint:md:fix` — auto-fix works on a dirty file
3. Stage a `.md` file with a violation, attempt commit — pre-commit hook blocks it
4. Push to a branch, open PR — GitHub Actions workflow runs and passes

## Delivery Rules
1. One increment per commit.
2. Keep config documented with JSONC comments for template users.
3. Minimal Node.js footprint — devDependencies only, no runtime code.

## Milestone Chunks (Standalone Delivery Groups)

| Milestone | Increments | Coherent Outcome | Standalone Test Gate | Exit Criteria |
| :--- | :--- | :--- | :--- | :--- |
| **M-1: Local Linting** | 01-03 | markdownlint runs locally with zero violations. | `npm run lint:md` exits 0 | All .md files pass lint. |
| **M-2: Automated Guards** | 04-05 | CI and pre-commit hooks enforce lint on every change. | Commit hook blocks bad .md; CI passes on PR | Full pipeline verified. |
