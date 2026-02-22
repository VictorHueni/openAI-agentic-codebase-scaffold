# Harness Engineering — Portable Template

This folder is a self-contained **Agent-First Engineering** template based on [Harness Engineering](https://openai.com/index/harness-engineering/) by OpenAI and the [Ralph Loop](https://ghuntley.com/loop/) by Geoffrey Huntley.

Copy `harness/` into any project root to get an instant AI governance structure.

## Quick Start

### 1. Copy into your project

```bash
cp -r harness/ /path/to/my-project/harness/
```

### 2. Define your mission

Fill in the governance files with your project's specifics:

| File | What to fill in | Priority |
|------|----------------|----------|
| `AGENTS.md` | High-level mission, directives, and repo navigation guide | Required |
| `ARCHITECTURE.md` | Dependency layers, invariants, module boundaries | Required |
| `QUALITY_SCORE.md` | Definition of "Done", test coverage bar, lint standards | Required |
| `PRODUCT_SENSE.md` | Target audience, value proposition, success metrics | Recommended |
| `PLANS.md` | Roadmap, current priorities, milestones | Recommended |
| `SECURITY.md` | Auth model, secrets handling, OWASP considerations | Recommended |
| `RELIABILITY.md` | Error budgets, monitoring, tech debt strategy | Recommended |
| `DESIGN.md` | Design system, component library, visual language | If applicable |
| `FRONTEND.md` | UI stack, frameworks, rendering strategy | If applicable |

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

| Agent | Context folder | Primary file | Native init | Skills sync |
|-------|---------------|-------------|-------------|-------------|
| `claude` | `.claude/` | `CLAUDE.md` | none | copy |
| `gemini` | `.gemini/` | `GEMINI.md` | `gemini /init` | copy |
| `github-copilot` | `.copilot-instructions/` | `AGENTS.md` | none | copy |

To remove an agent: `python harness/scripts/workforce.py fire gemini`

### 4. Write your first product spec

```bash
touch harness/docs/product-specs/0001_prd_my-feature.md
touch harness/docs/exec-plans/active/0001_exec_my-feature.md
```

### 5. Start the Ralph Loop

1. **Write a product spec** in `docs/product-specs/`
2. **Create an exec plan** in `docs/exec-plans/active/`
3. **Hand it to your agent** — the agent reads the spec, follows the plan, and iterates autonomously
4. **Agent self-reviews** against `ARCHITECTURE.md` and `QUALITY_SCORE.md`
5. **Move completed plans** to `docs/exec-plans/completed/`

## Contents

| Path | Purpose |
|------|---------|
| `AGENTS.md` | Primary agent entry point — mission, directives, Ralph Loop protocol |
| `ARCHITECTURE.md` | Dependency layers and structural invariants |
| `QUALITY_SCORE.md` | Definition of "Done" and exit criteria |
| `SECURITY.md` | Security invariants and compliance references |
| `RELIABILITY.md` | Monitoring, alerting, and error handling policy |
| `PLANS.md` | Active roadmap and execution strategy |
| `PRODUCT_SENSE.md` | Target audience and core value proposition |
| `DESIGN.md` | Aesthetic and design system principles |
| `FRONTEND.md` | Technical stack and component guidelines |
| `docs/` | Documentation engine (specs, plans, design docs, references) |
| `workforce/` | Agent onboarding system (templates, skills, manifests) |
| `scripts/` | CLI tools (workforce.py) |

## Available Skills

Skills live in `workforce/agent-template/skills/` and are synced into each agent's context folder on `hire`.

| Skill | Type | Purpose |
|-------|------|---------|
| `git-commit` | Instructional | Conventional commit messages |
| `git-pr-creator` | Instructional | Structured PR creation |
| `git-worktrees` | Instructional | Git worktree workflow for parallel tasks |
| `spec-prd-creator` | Instructional | Generate PRDs from intent |
| `spec-implementation-planner` | Instructional | Break PRDs into incremental exec plans |
| `spec-adr-manager` | Instructional | Create and manage Architecture Decision Records |
| `spec-peer-reviewer` | Instructional | Agent-to-agent peer review |
