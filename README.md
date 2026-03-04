# Harness Engineering Scaffold

A portable **Agent-First Engineering** template based on [Harness Engineering](https://openai.com/index/harness-engineering/) by OpenAI and the [Ralph Loop](https://ghuntley.com/loop/) by Geoffrey Huntley.

## Repository Structure

This repository has two layers:

| Layer                 | Path       | Purpose                                                                   |
| --------------------- | ---------- | ------------------------------------------------------------------------- |
| **Scaffold project**  | Root (`/`) | Governance and working docs for building the scaffold itself              |
| **Portable template** | `harness/` | Self-contained template — copy into any project for instant AI governance |

### Root — Scaffold Development

- **Governance files** (`AGENTS.md`, `ARCHITECTURE.md`, `QUALITY_SCORE.md`, etc.) — scaffold-specific rules and mission
- **`docs/`** — scaffold working docs: PRDs, exec plans, design docs
- **`CLAUDE.md`**, **`GEMINI.md`** — agent entry points for scaffold work

### `harness/` — Portable Template

- **Governance templates** — clean stubs for users to fill in
- **`docs/`** — documentation engine (specs, plans, design docs, references)
- **`workforce/`** — agent onboarding system (templates, skills, manifests)
- **`scripts/`** — CLI tools (`workforce.py` for hire/fire commands)

See [`harness/README.md`](harness/README.md) for the getting started guide.

### Scaffold Working Docs

This folder contains the PRDs, Execution Plans, and Design Documents used to **build the scaffold itself**.

#### Structure

| Folder                  | Purpose                                                      |
| ----------------------- | ------------------------------------------------------------ |
| `product-specs/`        | PRDs for scaffold features (e.g., the hire/fire CLI utility) |
| `exec-plans/active/`    | Implementation plans currently being worked on               |
| `exec-plans/completed/` | Archived plans for delivered scaffold features               |
| `design-docs/`          | Technical design documents for scaffold architecture         |
| `generated/`            | Auto-generated scaffold artifacts                            |
| `references/`           | LLM-readable references specific to scaffold development     |

#### How this relates to `harness/`

- **`docs/`** (this folder) contains working documents for the scaffold project.
- **`harness/docs/`** contains the clean template documentation engine shipped to users.
- Skills and workforce templates point to `docs/` by default (relative to project CWD).

## Getting Started with the Template

See [`harness/README.md`](../harness/README.md) for instructions on how to use the portable template in your own project.

## Using the Template

```bash
# Copy harness/ into your project
cp -r harness/ /path/to/my-project/harness/

# Fill in governance files, then onboard agents
python harness/scripts/workforce.py hire claude
python harness/scripts/workforce.py hire gemini
```

## Harness Engineering — Portable Template

This folder is a self-contained **Agent-First Engineering** template based on [Harness Engineering](https://openai.com/index/harness-engineering/) by OpenAI and the [Ralph Loop](https://ghuntley.com/loop/) by Geoffrey Huntley.

Copy `harness/` into any project root to get an instant AI governance structure.

## Quick Start

### 1. Copy into your project

```bash
cp -r harness/ /path/to/my-project/harness/
```

### 2. Define your mission

Fill in the governance files with your project's specifics:

| File               | What to fill in                                           | Priority      |
| ------------------ | --------------------------------------------------------- | ------------- |
| `AGENTS.md`        | High-level mission, directives, and repo navigation guide | Required      |
| `ARCHITECTURE.md`  | Dependency layers, invariants, module boundaries          | Required      |
| `QUALITY_SCORE.md` | Definition of "Done", test coverage bar, lint standards   | Required      |
| `PRODUCT_SENSE.md` | Target audience, value proposition, success metrics       | Recommended   |
| `PLANS.md`         | Roadmap, current priorities, milestones                   | Recommended   |
| `SECURITY.md`      | Auth model, secrets handling, OWASP considerations        | Recommended   |
| `RELIABILITY.md`   | Error budgets, monitoring, tech debt strategy             | Recommended   |
| `DESIGN.md`        | Design system, component library, visual language         | If applicable |
| `FRONTEND.md`      | UI stack, frameworks, rendering strategy                  | If applicable |

### 3. Onboard your AI agents

```bash
# Preview what will be created (no changes made)
python harness/scripts/workforce.py hire claude --dry-run

# Onboard agents
python harness/scripts/workforce.py hire claude
python harness/scripts/workforce.py hire gemini
python harness/scripts/workforce.py hire github-copilot
```

What `hire` does for each agent:

| Agent            | Context folder           | Primary file | Native init    | Skills sync |
| ---------------- | ------------------------ | ------------ | -------------- | ----------- |
| `claude`         | `.claude/`               | `CLAUDE.md`  | none           | copy        |
| `gemini`         | `.gemini/`               | `GEMINI.md`  | `gemini /init` | copy        |
| `github-copilot` | `.copilot-instructions/` | `AGENTS.md`  | none           | copy        |

To remove an agent: `python harness/scripts/workforce.py fire gemini`

### 4. Write your first product spec

```bash
touch harness/docs/product-specs/0001_prd_my-feature.md
touch harness/docs/exec-plans/active/0001_exec_my-feature.md
```

### 5. Start the Ralph Loop

#### Manual (agent-guided)

1. **Write a product spec**: Use the `spec-prd-creator` skill to generate a PRD in `docs/product-specs/`.
2. **Create an exec plan**: Use the `spec-implementation-planner` skill to break the PRD into increments in `docs/exec-plans/active/`.
3. **Peer review**: Use `spec-peer-reviewer` to validate the plan has status fields, test gates, and acceptance criteria.
4. **Execute**: Invoke the `ralph-loop-runner` skill. The agent sets up a workspace, iterates through increments one at a time, and self-reviews against `ARCHITECTURE.md` and `QUALITY_SCORE.md`.
5. **Archive**: On completion, the runner moves the PRD and exec plan to their final locations.

#### Automated (script-driven)

For hands-off execution, use the `ralph.sh` script to spawn a fresh agent per increment:

```bash
bash skills/ralph-loop-runner/scripts/ralph.sh docs/exec-plans/active/NNNN_feature-name/
```

The script detects completion by checking for remaining `**Status:** pending` increments and stops when all are done or the max iteration limit is reached.

## Contents

| Path               | Purpose                                                              |
| ------------------ | -------------------------------------------------------------------- |
| `AGENTS.md`        | Primary agent entry point — mission, directives, Ralph Loop protocol |
| `ARCHITECTURE.md`  | Dependency layers and structural invariants                          |
| `QUALITY_SCORE.md` | Definition of "Done" and exit criteria                               |
| `SECURITY.md`      | Security invariants and compliance references                        |
| `RELIABILITY.md`   | Monitoring, alerting, and error handling policy                      |
| `PLANS.md`         | Active roadmap and execution strategy                                |
| `PRODUCT_SENSE.md` | Target audience and core value proposition                           |
| `DESIGN.md`        | Aesthetic and design system principles                               |
| `FRONTEND.md`      | Technical stack and component guidelines                             |
| `docs/`            | Documentation engine (specs, plans, design docs, references)         |
| `workforce/`       | Agent onboarding system (templates, skills, manifests)               |
| `scripts/`         | CLI tools (workforce.py)                                             |

## Available Skills

Skills live in `workforce/agent-template/skills/` and are synced into each agent's context folder on `hire`.

| Skill                         | Type          | Purpose                                         |
| ----------------------------- | ------------- | ----------------------------------------------- |
| `git-commit`                  | Instructional | Conventional commit messages                    |
| `git-pr-creator`              | Instructional | Structured PR creation                          |
| `git-worktrees`               | Instructional | Git worktree workflow for parallel tasks        |
| `spec-prd-creator`            | Instructional | Generate PRDs from intent                       |
| `spec-implementation-planner` | Instructional | Break PRDs into incremental exec plans          |
| `spec-adr-manager`            | Instructional | Create and manage Architecture Decision Records |
| `spec-peer-reviewer`          | Instructional | Agent-to-agent peer review                      |
| `ralph-loop-runner`           | Instructional | Autonomous Ralph Loop execution                 |

## The Ralph Loop

1. **Set Intent**: Write a product spec in `docs/product-specs/`
2. **Start Loop**: Agent takes the task and iterates autonomously
3. **Monitor Satisfice**: Agent implements, self-reviews, responds to feedback
4. **Completion**: Loop terminates when `QUALITY_SCORE.md` metrics are satisfied

The goal is to maximize **Agent Legibility** — ensuring that an AI agent can understand the entire domain, architecture, and intent of the project directly from the repository.

### Legibility & Autonomy Stack

#### 1. Sensory Input (The "Eyes")

- **Chrome DevTools Bridge**: Use Playwright or Puppeteer to allow the agent to inspect the UI, capture screenshots, and read console logs.
- **Observability (OpenTelemetry)**: Integrate traces and logs that the agent can query to debug complex failures autonomously.
- **Log Aggregation**: Provide a standardized way for agents to tail and parse application logs in real-time.

#### 2. Mechanical Control (The "Hands")

- **CLI Integration**: Ensure all core tasks (database migrations, deployments, tests) are executable via clean, documented CLI commands.
- **Isolated Previews**: Automate the creation of sandbox environments where agents can verify their changes before opening a PR.
- **Snapshot Verification**: Implement visual and data regression testing that agents can run locally to satisfy quality invariants.

#### 3. Intellectual Context (The "Mind")

- **Dependency Mapping**: Provide scripts that generate visual or text-based dependency graphs to help agents map the architecture.
- **Schema Reflection**: Automatically maintain up-to-date documentation of database schemas, API contracts, and state machines in `docs/generated/`.

### Knowledge Base & Mechanical Enforcement

1. **Documentation Linters**: Implement CI jobs that validate your markdown using `markdownlint` or custom scripts.
2. **Architectural Unit Tests**: Create tests that ensure the code follows the "Laws" in `ARCHITECTURE.md`.
3. **The "Doc-Gardening" Agent**: Schedule a recurring background task that scans for stale tasks and documentation drift.
4. **Remediation Instructions**: When a linter fails, include the exact command the agent needs to run to fix it.
5. **Elevate to Code**: If a documentation rule is repeatedly ignored, enforce it in code or a custom linter.

## Contributing

This repo dogfoods the harness pattern — root governance files describe how to build the scaffold, while `harness/` contains the template product. See `docs/` for scaffold PRDs and exec plans.
