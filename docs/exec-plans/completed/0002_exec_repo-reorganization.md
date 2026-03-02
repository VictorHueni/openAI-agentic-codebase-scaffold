# Implementation Plan: Fully Meta Reorganization — Root as Harness User

## Summary

Consolidate the repository into a two-concept structure: root (a project using the harness pattern to build itself) and `harness/` (a portable, self-contained IT department template). Eliminate `scaffold-dev/` by promoting its content to root `docs/`.

Reference: `docs/product-specs/0002_prd_repo-reorganization.md`
Architecture constraints: `ARCHITECTURE.md`

Principles:

1. **Self-Containment**: `harness/` must never reference `../` (except template AGENTS.md which deploys outside harness).
2. **True Dogfooding**: The root project follows the same structure that harness/ prescribes.
3. **Atomic Increments**: Each increment leaves the repo in a working state.
4. **History Preservation**: Use `git mv` for all file moves.

---

## Target Structure

```text
/
├── AGENTS.md                   # Scaffold-specific: how to build the scaffold
├── ARCHITECTURE.md             # Scaffold-specific: two-layer architecture
├── QUALITY_SCORE.md            # Scaffold-specific: quality bar
├── SECURITY.md, RELIABILITY.md, PLANS.md, PRODUCT_SENSE.md, DESIGN.md, FRONTEND.md
├── CLAUDE.md, GEMINI.md        # Agent entry points for scaffold work
├── README.md                   # Repo overview + meta structure explanation
├── .gitignore
│
├── docs/                       # SCAFFOLD working docs (was scaffold-dev/)
│   ├── product-specs/          (scaffold PRDs)
│   ├── exec-plans/             (scaffold plans)
│   ├── design-docs/
│   ├── generated/
│   └── references/
│
└── harness/                    # PORTABLE TEMPLATE (self-contained)
    ├── AGENTS.md               # Clean template: Ralph Loop, directives
    ├── ARCHITECTURE.md         # Clean template stub
    ├── QUALITY_SCORE.md, SECURITY.md, RELIABILITY.md, PLANS.md, etc.
    ├── README.md               # Harness usage guide for target projects
    ├── docs/                   # Clean template docs engine
    ├── workforce/              # Agent onboarding system
    │   ├── agent-template/skills/
    │   └── templates/{claude,gemini,github-copilot}/
    └── scripts/
        └── workforce.py
```

---

## Migration Map

| Current location | Destination | Notes |
|-----------------|-------------|-------|
| `docs/*` (template content) | `harness/docs/*` | Clean template docs engine |
| `scaffold-dev/product-specs/*` | `docs/product-specs/*` | Scaffold working PRDs |
| `scaffold-dev/exec-plans/*` | `docs/exec-plans/*` | Scaffold working plans |
| `scaffold-dev/README.md` | `harness/README.md` (rewritten) | Getting started guide moves to harness |
| `scaffold-dev/ARCHITECTURE.md` | Merged into root `ARCHITECTURE.md` | Scaffold architecture |
| `workforce/` | `harness/workforce/` | Agent system |
| `scripts/` | `harness/scripts/` | CLI |
| Root governance `.md` files | Stay at root, rewritten scaffold-specific | Governance for THIS project |
| Same files (template versions) | `harness/*.md` | Clean templates for target projects |

---

## Increment Plan

### Increment 01: Move `docs/` to `harness/docs/`

Scope:

1. Create `harness/` directory.
2. `git mv docs/ harness/docs/` — template docs become the harness template.

Primary files: `docs/` entire tree → `harness/docs/`

Test gate:

1. `ls harness/docs/product-specs/index.md` — exists.
2. Root `docs/` no longer exists.

### Increment 02: Move `scaffold-dev/` content to root `docs/`

Scope:

1. Create root `docs/` with required structure (`product-specs/`, `exec-plans/active/`, `exec-plans/completed/`).
2. Move `scaffold-dev/product-specs/*` → `docs/product-specs/`
3. Move `scaffold-dev/exec-plans/*` → `docs/exec-plans/`
4. Move any other scaffold-dev subdirs with content.
5. Remove `scaffold-dev/` directory.
6. Remove `scaffold-dev/` entry from `.gitignore`.
7. Remove the "Scaffold Development Mode" section from root `AGENTS.md`.

Primary files:

1. `docs/product-specs/0001_prd_onboard-agent.md` (moved)
2. `docs/product-specs/0002_prd_repo-reorganization.md` (moved)
3. `docs/exec-plans/active/0002_exec_markdownlint.md` (moved)
4. `docs/exec-plans/active/0003_exec_repo-reorganization.md` (moved)
5. `docs/exec-plans/completed/0001_exec_onboard-agent.md` (moved)
6. `.gitignore` (edited)
7. `AGENTS.md` (edited)

Test gate:

1. `ls docs/product-specs/0001_prd_onboard-agent.md` — exists.
2. `scaffold-dev/` directory no longer exists.
3. `grep scaffold-dev .gitignore` — no matches.

### Increment 03: Move `workforce/` and `scripts/` into `harness/`

Scope:

1. `git mv workforce/ harness/workforce/`
2. `git mv scripts/ harness/scripts/`

Primary files: 2 directory moves

Test gate:

1. `ls harness/workforce/templates/claude/manifest.yaml` — exists.
2. `ls harness/scripts/workforce.py` — exists.

### Increment 04: Fix `workforce.py` paths

Scope: Update `harness/scripts/workforce.py` for new location.

Changes:

- `ROOT` (line 13) now resolves to `harness/` — correct for TEMPLATES_DIR, SKILLS_SOURCE_DIR.
- Add `REPO_ROOT = ROOT.parent` — for agent context folders at project root.
- `resolve_target_dir` (line 62): `ROOT / folder` → `REPO_ROOT / folder`.
- `run_native_init` (line 71): `cwd=ROOT` → `cwd=REPO_ROOT`.

Primary files:

1. `harness/scripts/workforce.py`

Test gate:

1. `python -m py_compile harness/scripts/workforce.py` — exit 0.
2. `python harness/scripts/workforce.py hire claude --dry-run` — target `.claude/` at repo root, NOT `harness/.claude/`.

### Increment 05: Create clean governance templates in `harness/`

Scope: Create clean template versions of all governance files inside `harness/`. Strip any scaffold-specific content.

Create:

1. `harness/AGENTS.md` — Ralph Loop protocol, directives, repo navigation guide. NO scaffold-dev references.
2. `harness/ARCHITECTURE.md` — clean stub for users to fill in.
3. `harness/QUALITY_SCORE.md` — clean template with Ralph Loop exit criteria.
4. `harness/SECURITY.md`, `RELIABILITY.md`, `PLANS.md`, `PRODUCT_SENSE.md`, `DESIGN.md`, `FRONTEND.md` — clean stubs.
5. `harness/README.md` — getting started guide for target projects.

Primary files: 10 new files in `harness/`

Test gate:

1. `ls harness/AGENTS.md harness/README.md` — both exist.
2. `grep -c "scaffold-dev" harness/AGENTS.md` — returns 0.
3. `grep -c "\.\.\/" harness/AGENTS.md` — returns 0.

### Increment 06: Rewrite root governance files as scaffold-specific

Scope: Root governance files become specific to building/maintaining the scaffold.

Key content:

- **`AGENTS.md`**: Mission is building the Harness Engineering scaffold. Directives include keeping harness/ self-contained. How-to references `docs/product-specs/` and `docs/exec-plans/active/`.
- **`ARCHITECTURE.md`**: Two-layer architecture (root project + harness/ template). Invariant: harness/ never references `../`.
- **`QUALITY_SCORE.md`**: Scaffold quality bar — harness must be self-contained, templates must be clean, workforce.py must compile.
- Others: scaffold-specific or minimal stubs.

Primary files: 9 root governance `.md` files (rewritten)

Test gate:

1. Root `AGENTS.md` references `docs/product-specs/` (not scaffold-dev/).
2. Root `ARCHITECTURE.md` describes the harness/ self-containment invariant.

### Increment 07: Update template AGENTS.md pointer paths

Scope: Template AGENTS.md files (deployed into `.claude/CLAUDE.md`, etc.) need `../harness/` prefix to reach governance files.

Changes in `harness/workforce/templates/{claude,gemini,github-copilot}/AGENTS.md`:

- `../AGENTS.md` → `../harness/AGENTS.md`
- `../ARCHITECTURE.md` → `../harness/ARCHITECTURE.md`
- `../QUALITY_SCORE.md` → `../harness/QUALITY_SCORE.md`
- `../SECURITY.md` → `../harness/SECURITY.md`
- `../RELIABILITY.md` → `../harness/RELIABILITY.md`

Primary files: 3 template AGENTS.md files

Test gate:

1. `grep "harness/AGENTS.md" harness/workforce/templates/claude/AGENTS.md` — matches.

### Increment 08: Audit harness/ self-containment and fix skill paths

Scope: Ensure harness/ has zero `../` references except in template AGENTS.md.

Fix:

- `get-next-id.py` — update to use `Path.cwd()` for repo root resolution.
- Skill SKILL.md files — verify `docs/` paths work as sibling references within harness/.
- All harness/ `.md` files — verify no `../` leaks.

Primary files:

1. `harness/workforce/agent-template/skills/spec-prd-creator/scripts/get-next-id.py`
2. Skill SKILL.md files (if any need path fixes)

Test gate:

1. `grep -rn "\.\.\/" harness/ --include="*.md" --include="*.py"` — only matches in `workforce/templates/*/AGENTS.md`.

### Increment 09: Update root `README.md`, `CLAUDE.md`, `GEMINI.md`

Scope:

1. Rewrite `README.md` to explain the meta structure.
2. Verify `CLAUDE.md` and `GEMINI.md` point to root `AGENTS.md`.
3. Update all docs references in README.

Primary files:

1. `README.md`
2. `CLAUDE.md`
3. `GEMINI.md`

Test gate:

1. README describes both layers (root project + harness/ template).

### Increment 10: Update `docs/` references (scaffold working docs)

Scope: Update paths in scaffold working docs that referenced `scaffold-dev/` or old root paths.

Changes:

- `docs/product-specs/0001_prd_onboard-agent.md`: `workforce/` → `harness/workforce/`, `scripts/` → `harness/scripts/`
- `docs/exec-plans/completed/0001_exec_onboard-agent.md`: same path updates.
- `docs/exec-plans/active/0002_exec_markdownlint.md`: same path updates.
- `docs/exec-plans/active/0003_exec_repo-reorganization.md`: same path updates.

Primary files: 4 files in `docs/`

Test gate:

1. `grep -r "scripts/workforce.py" docs/ | grep -v "harness/"` — no matches.

### Increment 11: Final verification + cleanup

Scope:

1. Verify root structure.
2. Verify harness/ self-containment.
3. Verify workforce.py works.
4. Remove any leftover empty dirs.

---

## Verification Suite (Ralph Loop Exit Alignment)

1. Root `ls` → governance files + `docs/` + `harness/` + README + .gitignore + CLAUDE.md + GEMINI.md (NO scaffold-dev/)
2. `python -m py_compile harness/scripts/workforce.py` → exit 0
3. `python harness/scripts/workforce.py hire claude --dry-run` → target `.claude/` at repo root
4. `grep -rn "\.\.\/" harness/ --include="*.md" --include="*.py"` → only template AGENTS.md
5. Root `AGENTS.md` references `docs/product-specs/` (not scaffold-dev/)
6. `harness/AGENTS.md` has NO `../` references
7. `ls docs/product-specs/0001_prd_onboard-agent.md` — scaffold PRD in root docs/

## Delivery Rules

1. One increment per commit.
2. Use `git mv` for all moves to preserve history.
3. Each increment must leave the repo in a compilable/runnable state (after Increment 04).

## Milestone Chunks (Standalone Delivery Groups)

| Milestone | Increments | Coherent Outcome | Standalone Test Gate | Exit Criteria |
| :--- | :--- | :--- | :--- | :--- |
| **M-1: Physical restructure** | 01–04 | All dirs in target locations; workforce.py paths correct; scaffold-dev eliminated. | `python harness/scripts/workforce.py hire claude --dry-run` | Files moved, script compiles, dry-run passes. |
| **M-2: Content separation** | 05–06 | Harness = clean templates; root = scaffold-specific governance. | `grep -c "scaffold-dev" harness/AGENTS.md` returns 0 | Template and governance content clearly separated. |
| **M-3: Reference integrity** | 07–11 | All cross-references correct; self-containment verified. | Full verification suite (7 checks). | Zero stale references; harness self-contained. |
