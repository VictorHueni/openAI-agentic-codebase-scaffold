# PRD: Agent Onboarding Utility (`onboard-agent`)

**Date:** 2026-02-14  
**Status:** Draft  
**Target:** Developers & AI Agents  

---

## 1. Problem Statement
When a developer or an AI agent joins a new project, they often lack the specific "Rules of the Road" (architectural invariants, coding standards, and local workflows like the Ralph Loop). While many AI tools have native `init` commands, they generate generic configurations that do not capture the unique intent of a "Harness Engineering" repository. 

Manually setting up these hidden context folders (`.gemini`, `.claude`, etc.) is error-prone, leads to stale documentation, and creates friction for multi-agent interoperability.

---

## 2. Goals
- **Full-Spectrum Provisioning**: Act as an environment architect that goes beyond native `init` to set up folders and custom rules.
- **Decoupled Sync Strategy**: Separate the *Onboarding* (creation) from the *Synchronization* (updating). 
- **Summary + Pointer Model**: Maintain agent-specific "Primary Files" (e.g., `GEMINI.md`) with lean summaries of root laws and mandatory pointers to the full root files.
- **YAML-Driven Configs**: Use token-efficient YAML manifests to define the relationship between agents and root laws.
- **Skills Discovery**: Make all repo skills avaible to the agent  as its primary library of capabilities. A copy paste of the master skills folder to the agent folder. 
- **Multi-Agent Interoperability**: Support Gemini, Claude, Copilot, and OSS-Agents via standardized YAML templates.

---

## 3. Non-Goals
- **API Key Management**: The script will not handle LLM provider authentication or billing.
- **Agent Execution**: The script configures the environment but does not "run" the agents.

---

## 4. User Stories

manifest.yaml:
```yaml
    agent_name: gemini
    context_folder: .gemini
    primary_file: GEMINI.md
    native_init: "gemini /init"
    skills_library_sync: "symlink" # or "copy"
```


### US-001: Initialize Agent Onboarding
**Description:** As a developer, I want to run a command `hire gemini` so that the agent's "Brain" (System Prompt) is created according to the agent's template and the `/skills` library is made available in the agent folder (symlink or copy as per agent template)

**Acceptance Criteria:**
- [ ] Script calls native `init` if applicable.
- [ ] Script populate the system prompt with the agent's identity and role based on a template `AGENTS.md`.
- [ ] Script prepends `AUTO-GENERATED` headers to all managed sections.
- [ ] Script creates a symlink or copy of the `/skills` folder in the agent

### US-002: Interactive Conflict Resolution
**Description:** As a developer, I want to be prompted if an agent folder already exists upon creation so that I don't accidentally wipe my custom configurations or local-only state.

**Acceptance Criteria:**
- [ ] Script detects an existing `.agent-folder` during the onboarding phase.
- [ ] User is presented with a clear menu: `[R]eset (Wipe & Rebuild)`,  or `[S]kip` .
- [ ] **Reset**: Deletes the entire target folder before re-provisioning.
- [ ] **Skip**: Terminates the script without making any changes.

### US-001: Standardize Agent Offboarding
**Description:** As a developer, I want to run a command `fire gemini` so that the agent's folder is removed.

**Acceptance Criteria:**
- [ ] Script checks for the existence of the agent's folder.
- [ ] If the folder exists, iskip is deleted along with all its contents.
- [ ] If the folder does not exist, the script outputs a message indicating that the agent is not currently onboarded.

---

## 5. Technical Considerations
- **Templates**: All master instructions (Identity, Pointers) and manifest templates live in `/workforce/templates/`.
- **Manifests**: Use YAML for agent-specific configurations (Agent Name, Primary File...).
- **Header Protection**: Prepend `<!-- AUTO-GENERATED: DO NOT EDIT -->` to managed system promt.
- 
---

## 6. Success Metrics
- **Zero-Drift**: 100% of onboarded agents use the exact same system prompt and the exact same set of skills as the source of truth in the root folder.
- **Onboarding Speed**: New agents are ready to work with the full repository context in under 10 seconds.

---

## 7. Resolved Decisions
- **Scope**: The utility will stick strictly to project-local configurations (e.g., `./.gemini/`) to ensure repository portability and avoid side effects in the user's home directory.
- **OSS-Agent Strategy**: Generic open-source contributor agents will be supported via a standardized `.agent/` folder and `AGENTS.md` template, following the emerging open standard for repo-embedded context.
