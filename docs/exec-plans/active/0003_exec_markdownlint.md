# Implementation Plan: Markdownlint Full Setup

## Summary

Deliver markdownlint infrastructure across the scaffold: CLI scripts, GitHub Actions CI, and a pre-commit hook via husky/lint-staged.

Reference: `docs/product-specs/` (no standalone PRD — originated from `README.md` section "Knowledge Base & Mechanical Enforcement" item 1, and `QUALITY_SCORE.md` linting standards)
Architecture constraints: `ARCHITECTURE.md`

Principles:

1. **Tool Choice**: `markdownlint-cli2` — newer, recommended by the markdownlint author, supports JSONC config with comments (ideal for a template repo where rule rationale matters).
2. **Minimal Footprint**: All tooling is devDependencies only; `"private": true` prevents accidental npm publish.
3. **Convention Over Configuration**: Sensible defaults with targeted overrides based on codebase analysis of 44+ tracked markdown files.

## Non-Goals

1. **Shipping markdownlint as part of `harness/`**: The template product does not include lint tooling; users bring their own.
2. **Linting non-markdown files**: No prose linting, spell-check, or link validation in this plan.
3. **Custom markdownlint rules**: Only built-in rules with config overrides; no custom plugins.

---

## Increment Plan

### Increment 01: Create markdownlint config (`.markdownlint-cli2.jsonc`)

Scope:

1. Create the JSONC rule configuration file with comments explaining each rule decision.
2. Configure glob patterns and ignores.
3. Configure `ignores` array to exclude all gitignored directories that may contain `.md` files on disk: `node_modules/`, `.gemini/`, `.claude/`, `.cursor/`, `.aider/`, `.bolt/`, `.copilot-instructions/`.

Primary files:

1. `.markdownlint-cli2.jsonc`

Key rule decisions (based on codebase analysis):

| Rule | Setting | Rationale |
|------|---------|-----------|
| MD013 (line length) | **disabled** | Prose-heavy docs; 66+ lines already exceed 120 chars |
| MD024 (duplicate headings) | `siblings_only: true` | Exec plans reuse headings under different parents |
| MD026 (trailing punctuation) | `punctuation` excludes `:()` | Headings like `## Types (required)` are common |
| MD033 (inline HTML) | **disabled** | Template users may need `<details>`, badges, etc. |
| MD036 (emphasis as heading) | **disabled** | Bold text used as visual separators in SKILL.md files |
| MD041 (first-line heading) | **disabled** | All 7 SKILL.md files (14 including `.claude/` copies) start with YAML front matter |
| All others | **default (enabled)** | Existing files largely conform already |

Test gate:

1. File is valid JSONC.
2. Config loads successfully when used by `markdownlint-cli2` (verified in Increment 02).

### Increment 02: Create `package.json`, pin Node version, and install dependencies

Scope:

1. Create minimal `package.json` with `markdownlint-cli2`, `husky`, and `lint-staged` as devDependencies. Include `"private": true` and `engines` field matching `.nvmrc`.
2. Create `.nvmrc` with pinned Node LTS version (e.g., `22`).
3. Define scripts: `"lint:md": "markdownlint-cli2"`, `"lint:md:fix": "markdownlint-cli2 --fix"`. Globs are defined in the config file, not repeated in scripts.
4. Run `npm install` to generate `package-lock.json`. Commit the lock file (best practice for non-library projects).
5. Verify `.gitignore` already includes `node_modules/`.

Primary files:

1. `package.json`
2. `.nvmrc`
3. `package-lock.json` (generated, committed)

Rollback: If `npm install` fails, delete `package.json`, `package-lock.json`, and `node_modules/`.

Test gate:

1. `npm run lint:md` runs, loads config, and reports violations (expected non-zero exit at this stage — Increment 03 fixes them).

### Increment 03: Fix existing markdown lint violations

Scope:

1. Run `npm run lint:md:fix` to auto-fix what can be auto-fixed.
2. Manually fix any remaining violations.
3. Verify zero violations.

Note: `harness/` markdown files are in-scope. Lint fixes improve template quality and do not violate self-containment (no scaffold-specific content is added). Verify with `grep -rn "\.\.\/" harness/` after fixes.

Primary files:

1. Various `*.md` files across the repo (root and `harness/`).

Test gate:

1. `npm run lint:md` exits with code 0.
2. `grep -rn "\.\.\/" harness/ --include="*.md"` — only matches in `workforce/templates/*/AGENTS.md` (self-containment preserved).

### Increment 04: GitHub Actions workflow

Scope:

1. Create `.github/workflows/` directory.
2. Create CI workflow that lints markdown on PRs and pushes to `main`.
3. Use `paths` filter so workflow only runs when `*.md`, `.markdownlint-cli2.jsonc`, or `package.json` change.
4. Runner: `ubuntu-latest`. Node version: from `.nvmrc` via `actions/setup-node` with `node-version-file`. Cache: `actions/setup-node` with `cache: 'npm'`.
5. Steps: checkout, setup-node, `npm ci`, `npm run lint:md`.

Primary files:

1. `.github/workflows/lint-markdown.yml`

Test gate:

1. YAML is valid (`actionlint` or manual review).
2. Full verification on first PR.

### Increment 05: Husky pre-commit hook

Scope:

1. Run `npx husky init` to create `.husky/` directory.
2. Set `.husky/pre-commit` to run `npx lint-staged`.
3. Add `lint-staged` config block to the existing `package.json`: runs `markdownlint-cli2` on staged `*.md` files.

Primary files:

1. `.husky/pre-commit`
2. `package.json` (add `lint-staged` config block)

Rollback: If `npx husky init` fails or writes unexpected files, delete `.husky/` and retry.

Test gate:

1. Stage a `.md` file with a violation, attempt commit — pre-commit hook blocks it.
2. Fix violation, re-stage, commit succeeds.
3. Hook executes correctly on Windows (Git Bash — husky v9+ requirement).

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
4. Commit `package-lock.json` (best practice for non-library projects).
5. Node.js version pinned in `.nvmrc` and referenced by CI and `engines` field.

## Milestone Chunks (Standalone Delivery Groups)

| Milestone | Increments | Coherent Outcome | Standalone Test Gate | Exit Criteria |
| :--- | :--- | :--- | :--- | :--- |
| **M-1: Local Linting** | 01-03 | markdownlint runs locally with zero violations. | `npm run lint:md` exits 0 | All .md files pass lint. |
| **M-2: Automated Guards** | 04-05 | CI and pre-commit hooks enforce lint on every change. | Commit hook blocks bad .md; CI passes on PR | Full pipeline verified. |
