# Implementation Plan: Agent Onboarding Utility (`hire` and `fire`)

## Summary
Deliver a deterministic onboarding CLI that provisions local agent folders from templates and safely removes them when offboarded.

Reference: `docs/product-specs/0001_prd_onboard-agent.md`  
Architecture constraints: `ARCHITECTURE.md`

Principles:
1. **Source of Truth**: `harness/workforce/templates/` for agent templates and `harness/workforce/agent-template/skills/` for skills.
2. **Atomic Onboarding**: An agent is either fully provisioned or unchanged.
3. **Mechanical Safety**: Managed output is explicitly header-tagged.
4. **Idempotence**: Repeated `hire`/`fire` runs should converge safely.

---

## Increment Plan

### Increment 01: Workforce Templates Scaffolding
Scope:
1. Ensure `harness/workforce/templates/` exists.
2. Create `gemini`, `claude`, and `github-copilot` template folders.
3. Add `manifest.yaml` and `AGENTS.md` to each folder.

Primary files:
1. `harness/workforce/templates/gemini/manifest.yaml`
2. `harness/workforce/templates/gemini/AGENTS.md`
3. `harness/workforce/templates/claude/manifest.yaml`
4. `harness/workforce/templates/claude/AGENTS.md`
5. `harness/workforce/templates/github-copilot/manifest.yaml`
6. `harness/workforce/templates/github-copilot/AGENTS.md`

Test gate:
1. `Get-ChildItem harness/workforce/templates -Recurse -File`

### Increment 02: CLI Entry Points (`hire` and `fire`)
Scope:
1. Create `harness/scripts/workforce.py`.
2. Implement argument parsing for `hire <agent>` and `fire <agent>`.
3. Validate agent template existence and required manifest keys.
4. Support `--dry-run`.

Primary files:
1. `harness/scripts/workforce.py`

Test gate:
1. `python -m py_compile harness/scripts/workforce.py`
2. `python harness/scripts/workforce.py hire gemini --dry-run`
3. `python harness/scripts/workforce.py fire gemini --dry-run`

### Increment 03: `fire` Command Behavior
Scope:
1. Resolve target folder from manifest.
2. If missing, print explicit not-onboarded message and exit 0.
3. If present, remove recursively (or log action in dry-run).

Primary files:
1. `harness/scripts/workforce.py`

Test gate:
1. `python harness/scripts/workforce.py fire gemini --dry-run`

### Increment 04: `hire` Folder Setup and Conflict Handling
Scope:
1. Create target context folder from manifest.
2. Support existing-folder behavior: `[R]eset` or `[S]kip`.
3. Provide non-interactive controls (`--reset`, `--skip-existing`).
4. Run manifest-defined native init command when configured.

Primary files:
1. `harness/scripts/workforce.py`

Test gate:
1. `python harness/scripts/workforce.py hire gemini --dry-run`

### Increment 05: Identity Injection and Managed Header
Scope:
1. Read per-agent template `AGENTS.md`.
2. Write to manifest `primary_file` under target folder.
3. Prepend `<!-- AUTO-GENERATED: DO NOT EDIT -->`.

Primary files:
1. `harness/scripts/workforce.py`
2. `harness/workforce/templates/*/AGENTS.md`

Test gate:
1. `python harness/scripts/workforce.py hire gemini --dry-run`

### Increment 06: Skills Sync
Scope:
1. Sync `harness/workforce/agent-template/skills/` into `<context_folder>/skills`.
2. Honor `skills_library_sync` strategy (`copy` or `symlink` with copy fallback).
3. Ensure sync step runs after target folder setup.

Primary files:
1. `harness/scripts/workforce.py`
2. `harness/workforce/agent-template/skills/*`

Test gate:
1. `python harness/scripts/workforce.py hire gemini --dry-run`

---

## Verification Suite (Ralph Loop Exit Alignment)
1. `python -m py_compile harness/scripts/workforce.py`
2. `python harness/scripts/workforce.py hire gemini --dry-run`
3. `python harness/scripts/workforce.py fire gemini --dry-run`
4. `python harness/scripts/workforce.py hire claude --dry-run`
5. `python harness/scripts/workforce.py hire github-copilot --dry-run`

## Delivery Rules
1. One increment per commit.
2. Keep runtime behavior deterministic from template manifests.
3. Keep scaffold docs and executable paths synchronized.

## Milestone Chunks (Standalone Delivery Groups)

| Milestone | Increments | Coherent Outcome | Standalone Test Gate | Exit Criteria |
| :--- | :--- | :--- | :--- | :--- |
| **M-1: Workforce Foundation** | 01-03 | Templates exist and `fire` behavior is safe/idempotent. | `python harness/scripts/workforce.py fire gemini --dry-run` | Template validity and offboarding behavior confirmed. |
| **M-2: Full Hiring Cycle** | 04-06 | `hire` provisions identity and skills from source-of-truth folders. | `python harness/scripts/workforce.py hire gemini --dry-run` | Provisioning flow and sync logic validated. |
