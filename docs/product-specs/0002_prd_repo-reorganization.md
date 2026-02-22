# PRD: Repository Reorganization — Fully Meta Harness Structure

**Date:** 2026-02-22
**Status:** Draft
**Target:** Scaffold Maintainers and AI Agents

---

## 1. Problem Statement

The repository currently mixes template content (meant for end users who clone the scaffold) with scaffold development governance (meant for building the scaffold itself) at root level. Twelve governance files, three directories (`docs/`, `workforce/`, `scripts/`), and a gitignored `scaffold-dev/` folder create an unclear boundary between "the product" and "the project that builds the product."

Users who clone the repo cannot easily extract just the portable template. Contributors cannot easily see the scaffold's own working docs (hidden in gitignored `scaffold-dev/`).

---

## 2. Goals

- **Self-Contained Portable Template**: Consolidate all template content into a single `harness/` folder that can be dropped into any new project with zero `../` references.
- **True Dogfooding**: The scaffold repo itself uses the harness pattern — root governance files + `docs/` for working specs and plans.
- **Eliminate scaffold-dev/**: Move its content into root `docs/`, un-gitignore it, making scaffold build docs visible to collaborators.
- **Two-Concept Mental Model**: Root = a project using the harness; `harness/` = the portable IT department template.

---

## 3. Non-Goals

- **Changing the workforce CLI behavior**: `hire`/`fire` commands stay the same; only internal paths update.
- **Changing skill content**: Skill instructions stay the same; only file path references update.
- **Adding new features**: This is a structural reorganization only.

---

## 4. User Stories

### US-001: Extract Portable Template

**Description:** As a developer starting a new project, I copy `harness/` from this repo into my project root and it works immediately without editing any internal paths.

**Acceptance Criteria:**
- [ ] `harness/` contains all governance templates, docs engine, workforce system, and scripts.
- [ ] `grep -rn "\.\.\/" harness/` only matches `workforce/templates/*/AGENTS.md` (intentional deploy-outside references).
- [ ] `python harness/scripts/workforce.py hire claude --dry-run` works from one directory above harness/.

### US-002: Scaffold Dogfooding

**Description:** As a scaffold contributor, I see the repo itself following the harness pattern — root governance files reference `docs/` for working specs and plans.

**Acceptance Criteria:**
- [ ] Root `AGENTS.md` is scaffold-specific (mission: build the harness).
- [ ] Root `docs/` contains scaffold PRDs and exec plans (visible in git, not gitignored).
- [ ] `scaffold-dev/` no longer exists.
- [ ] `.gitignore` no longer lists `scaffold-dev/`.

### US-003: Clean Separation

**Description:** As a contributor, I can clearly distinguish scaffold governance (root) from the template product (harness/).

**Acceptance Criteria:**
- [ ] Root governance files have scaffold-specific content (not template stubs).
- [ ] `harness/` governance files are clean templates for end users to fill in.
- [ ] `README.md` explains the two-layer structure.

---

## 5. Technical Considerations

- **Agent Entry Points**: `CLAUDE.md` and `GEMINI.md` must stay at root (agent discovery). They point to root `AGENTS.md` for scaffold work.
- **workforce.py Path Split**: After moving to `harness/scripts/`, needs `ROOT` (harness/) for templates/skills and `REPO_ROOT` (parent) for agent context folders.
- **Template AGENTS.md**: Written into `.claude/CLAUDE.md` etc. at project root. Must reference `../harness/AGENTS.md` (the one intentional `../` reference in harness/).
- **Existing Agent Folders**: If `.claude/`, `.gemini/`, `.copilot-instructions/` exist from prior `hire`, they'll have stale pointers. Users must re-run `hire --reset`.

---

## 6. Success Metrics

- **Self-Containment**: `grep -rn "\.\.\/" harness/` returns only template AGENTS.md matches.
- **Functional**: `python harness/scripts/workforce.py hire claude --dry-run` succeeds with correct paths.
- **Zero Stale References**: No file references `scaffold-dev/` after migration.

---

## 7. Resolved Decisions

- **Folder name**: `harness/` — ties to "Harness Engineering" from OpenAI methodology.
- **Dogfooding approach**: Root IS a harness user (Option B), not a separate governance layer.
- **scaffold-dev/ elimination**: Content moves to root `docs/`, un-gitignored for visibility.
