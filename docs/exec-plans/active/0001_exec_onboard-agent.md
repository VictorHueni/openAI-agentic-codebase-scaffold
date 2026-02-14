# Implementation Plan: Agent Onboarding Utility (`hire` & `fire`)

## Summary
The `onboard-agent` feature (delivered via `hire` and `fire` commands) automates the lifecycle of AI agent environments. It ensures that any "hired" agent is equipped with the repository's identity, laws, and the full `/skills` library, while providing a clean way to "fire" (remove) them.

Reference: `docs/product-specs/0001_prd_onboard-agent.md`

Principles:
1. **Source of Truth**: The `/workforce/templates/` and `/skills/` folders are the absolute masters.
2. **Atomic Onboarding**: An agent is either fully "hired" or not at all.
3. **Mechanical Safety**: Headers protect managed files from accidental manual edits.

---

## Increment Plan

### Increment 01: Workforce Templates Scaffolding
Scope:
1. Create `/workforce/templates/` directory.
2. Create subfolders for `gemini`, `claude`, and `github-copilot`.
3. Add a base `manifest.yaml` and `AGENTS.md` template for each.

Primary files:
1. `workforce/templates/gemini/manifest.yaml`
2. `workforce/templates/gemini/AGENTS.md`

Test gate:
1. `ls workforce/templates` verifies the structure.

### Increment 02: CLI Entry Points (`hire` & `fire`)
Scope:
1. Create `scripts/workforce.py` to handle both commands.
2. Implement argument parsing for `hire <agent>` and `fire <agent>`.
3. Validate that the requested agent exists in templates.

Primary files:
1. `scripts/workforce.py`

Test gate:
1. `python scripts/workforce.py hire gemini --dry-run`
2. `python scripts/workforce.py fire gemini --dry-run`

### Increment 03: The `fire` Command Implementation
Scope:
1. Implement the deletion logic: check for folder existence and perform `shutil.rmtree`.
2. Add a confirmation message for the user.

Primary files:
1. `scripts/workforce.py`

Test gate:
1. Create a dummy `.test-agent` folder and run `fire test-agent`.

### Increment 04: `hire` - Folder Setup & Native Init
Scope:
1. Implement the initial `hire` logic: folder creation and calling native `init` (e.g., `gemini /init`).
2. Implement the basic `[R]eset` and `[S]kip` logic for existing folders.

Primary files:
1. `scripts/workforce.py`

Test gate:
1. `python scripts/workforce.py hire gemini` creates the `.gemini/` folder.

### Increment 05: `hire` - Identity & Header Injection
Scope:
1. Implement logic to read the `AGENTS.md` template and the agent's identity rules.
2. Inject the content into the `primary_file` (e.g., `GEMINI.md`) with `AUTO-GENERATED` headers.

Primary files:
1. `scripts/workforce.py`

Test gate:
1. Verify `.gemini/GEMINI.md` contains the correct identity and headers.

### Increment 06: `hire` - Skills Library Sync
Scope:
1. Implement the "Copy" or "Symlink" logic for the `/skills` folder as defined in the `manifest.yaml`.
2. Ensure the sync is a clean mirror of the root `/skills` folder.

Primary files:
1. `scripts/workforce.py`

Test gate:
1. Verify that `.gemini/skills/` matches the root `/skills/` folder.

---

## Delivery Rules
1. One increment per commit.
2. `hire` and `fire` must be idempotent where possible.
3. No environment variables should be required for the scripts to run.

## Milestone Chunks (Standalone Delivery Groups)

| Milestone | Increments | Coherent Outcome | Standalone Test Gate | Exit Criteria |
| :--- | :--- | :--- | :--- | :--- |
| **M-1: Workforce Foundation** | 01-03 | Templates and `fire` command ready. | `python scripts/workforce.py fire` | Cleanup and template structure functional. |
| **M-2: Full Hiring Cycle** | 04-06 | Agents can be "hired" with full context. | `python scripts/workforce.py hire gemini` | Agent context is complete with identity and skills. |
