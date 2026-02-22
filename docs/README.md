# Scaffold Development Docs

This folder contains the PRDs, Execution Plans, and Design Documents used to **build this scaffold itself**. It is gitignored and will not ship to users who clone this template.

## Getting Started — New Project Setup

Follow these steps when you clone this scaffold to start a new project.

### 1. Clone and clean

```bash
git clone https://github.com/<your-org>/openAI-agentic-codebase-scaffold.git my-project
cd my-project

# Remove the scaffold-dev folder (it's for scaffold maintainers, not end users)
rm -rf scaffold-dev/

# Reset git history to start fresh
rm -rf .git
git init
git add -A
git commit -m "feat: initialize project from Harness Engineering scaffold"
```

### 2. Define your mission

Fill in the placeholder files with your project's specifics. These are the files agents read first — they are the "brain" of your repo.

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

The scaffold ships with a workforce CLI to provision agent context folders. Supported agents: `claude`, `gemini`, `github-copilot`.

```bash
# Preview what will be created (no changes made)
python scripts/workforce.py hire claude --dry-run
python scripts/workforce.py hire gemini --dry-run
python scripts/workforce.py hire github-copilot --dry-run

# Onboard the agents you use
python scripts/workforce.py hire claude
python scripts/workforce.py hire gemini
python scripts/workforce.py hire github-copilot
```

What `hire` does for each agent:

| Agent | Context folder | Primary file | Native init | Skills sync |
|-------|---------------|-------------|-------------|-------------|
| `claude` | `.claude/` | `CLAUDE.md` | none | copy |
| `gemini` | `.gemini/` | `GEMINI.md` | `gemini /init` | copy |
| `github-copilot` | `.copilot-instructions/` | `AGENTS.md` | none | copy |

Each `hire` command:
1. Creates the agent's context folder
2. Writes the primary file with an `<!-- AUTO-GENERATED: DO NOT EDIT -->` header
3. Copies the skills library (`workforce/agent-template/skills/`) into the context folder
4. Runs the agent's native init command (if defined in the manifest)

To remove an agent later:

```bash
python scripts/workforce.py fire gemini
```

If the context folder already exists, the CLI prompts you to `[R]eset` or `[S]kip`. Use `--reset` or `--skip-existing` for non-interactive mode.

### 4. Write your first product spec

Before writing any code, create a product spec and an execution plan.

```bash
# Create your first PRD
# (or use the spec-prd-creator skill via your AI agent)
touch docs/product-specs/0001_prd_my-feature.md

# Create the corresponding execution plan
touch docs/exec-plans/active/0001_exec_my-feature.md
```

Use the naming convention: `NNNN_type_slug.md` (e.g., `0001_prd_user-auth.md`).

### 5. Start the Ralph Loop

With your mission defined and agents onboarded, the workflow is:

1. **Write a product spec** in `docs/product-specs/`
2. **Create an exec plan** in `docs/exec-plans/active/`
3. **Hand it to your agent** — the agent reads the spec, follows the plan, and iterates autonomously
4. **Agent self-reviews** against `ARCHITECTURE.md` and `QUALITY_SCORE.md`
5. **Move completed plans** from `docs/exec-plans/active/` to `docs/exec-plans/completed/`

### 6. Set up linting (recommended)

Install markdownlint to enforce documentation quality (see `README.md` line 53):

```bash
npm install
npm run lint:md        # Check all markdown files
npm run lint:md:fix    # Auto-fix issues
```

This also sets up a pre-commit hook via husky that lints staged `.md` files automatically.

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
| `spec-peer-reviewer` | Instructional | Agent-to-agent code review |

## Structure

This folder mirrors `/docs/` exactly:

| Folder | Purpose |
|--------|---------|
| `product-specs/` | PRDs for scaffold features (e.g., the hire/fire CLI utility) |
| `exec-plans/active/` | Implementation plans currently being worked on |
| `exec-plans/completed/` | Archived plans for delivered scaffold features |
| `design-docs/` | Technical design documents for scaffold architecture |
| `generated/` | Auto-generated scaffold artifacts |
| `references/` | LLM-readable references specific to scaffold development |

## Relationship to /docs/

- `/docs/` is the **clean template** that ships to users.
- `/scaffold-dev/` is the **private workspace** for building the scaffold.
- Skills (`prd-creator`, `spec-implementation-planner`) point to `/docs/` by default because they are designed for the end user's workflow. When working on the scaffold itself, save outputs to `/scaffold-dev/` instead.
