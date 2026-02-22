# PRD: Agent Onboarding Utility (`onboard-agent`)

**Date:** 2026-02-14  
**Status:** Complete  
**Target:** Developers and AI Agents

---

## 1. Problem Statement
When a developer or AI agent joins a new project, they often miss repo-specific rules (architecture invariants, quality bars, local workflow). Native `init` commands are generic and do not capture this scaffold's operating model.

Manual setup of hidden context folders (`.gemini`, `.claude`, etc.) creates drift, stale prompts, and inconsistent multi-agent behavior.

---

## 2. Goals
- **Full-Spectrum Provisioning**: Build a local environment that goes beyond native `init`.
- **Decoupled Lifecycle**: Keep onboarding (`hire`) separate from synchronization workflows.
- **Summary + Pointer Model**: Generate lean agent primary files (`GEMINI.md`, `CLAUDE.md`, etc.) that point to root laws.
- **YAML-Driven Configs**: Define agent setup via template-local `manifest.yaml`.
- **Skills Availability**: Make `harness/workforce/agent-template/skills` available inside each onboarded agent folder (copy or symlink, per manifest).
- **Multi-Agent Interoperability**: Support Gemini, Claude, Copilot, and OSS-style agent setups.

---

## 3. Non-Goals
- **API Key Management**: No provider auth/billing setup.
- **Agent Execution**: The utility configures environments only; it does not run agents.

---

## 4. User Stories

Manifest example:
```yaml
agent_name: gemini
context_folder: .gemini
primary_file: GEMINI.md
native_init: gemini /init
skills_library_sync: copy
```

### US-001: Initialize Agent Onboarding
**Description:** As a developer, I run `hire gemini` so the agent context folder is provisioned with identity rules and skills.

**Acceptance Criteria:**
- [x] Script calls native `init` when defined in the manifest.
- [x] Script writes the primary file from the template `AGENTS.md`.
- [x] Script prepends `AUTO-GENERATED` headers to managed output.
- [x] Script syncs `harness/workforce/agent-template/skills` into the onboarded agent folder.

### US-002: Interactive Conflict Resolution
**Description:** As a developer, I get prompted when a target agent folder already exists, so I do not lose local state accidentally.

**Acceptance Criteria:**
- [x] Script detects existing target folder during `hire`.
- [x] User is prompted with `[R]eset` or `[S]kip`.
- [x] **Reset** deletes and rebuilds the target folder.
- [x] **Skip** exits without changes.

### US-003: Standardize Agent Offboarding
**Description:** As a developer, I run `fire gemini` so the agent folder is removed cleanly.

**Acceptance Criteria:**
- [x] Script checks whether the target folder exists.
- [x] If the folder exists, it is deleted recursively.
- [x] If the folder does not exist, script prints an explicit "not onboarded" message.

---

## 5. Technical Considerations
- **Template Source**: Agent manifests and per-agent overlays live in `harness/workforce/templates/`.
- **Skills Source**: Skills source of truth is `harness/workforce/agent-template/skills/`.
- **Header Protection**: Managed files include `<!-- AUTO-GENERATED: DO NOT EDIT -->`.
- **CLI Entry Point**: `harness/scripts/workforce.py` provides `hire` and `fire`.

---

## 6. Success Metrics
- **Zero Drift**: Onboarded agents are reproducible from templates and source skills.
- **Onboarding Speed**: New agent setup completes in under 10 seconds on local runs.

---

## 7. Resolved Decisions
- **Scope**: Keep everything project-local (for example `./.gemini/`), no user-home side effects.
- **OSS-Agent Compatibility**: Keep template model generic enough for standardized `.agent/` style contexts.
