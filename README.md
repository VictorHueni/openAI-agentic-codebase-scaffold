# Harness Engineering Scaffold Guide

This repository follows the **Agent-First Engineering** principles outlined by OpenAI in [Harness Engineering](https://openai.com/index/harness-engineering/). The core engine of this workflow is the **Ralph Loop** (or "Ralph Wiggum Loop").

## Root Level Guidance
- **AGENTS.md**: The primary entry point for AI. Define the mission, specific tool directives, and a "how-to" for the codebase.
- **skills/**: Folder-based capabilities. Each skill (e.g., `researcher/`) contains a `SKILL.md` for metadata and a `scripts/` folder for logic.
- **ARCHITECTURE.md**: Define the structural "laws" (e.g., dependency layers). Agents use this to prevent architectural drift.
- **DESIGN.md / FRONTEND.md**: Document the "taste" and technical stack of the UI.
- **QUALITY_SCORE.md**: Define what constitutes "good" code. Agents will use this as a checklist for PRs.
- **SECURITY.md / RELIABILITY.md**: Define the non-negotiable invariants for safety and uptime.
- **PLANS.md / PRODUCT_SENSE.md**: High-level context on *what* we are building and *why*.

## Documentation Engine (`/docs`)
- **design-docs/**: Store technical design documents (TDDs) and "Core Beliefs."
- **exec-plans/**: 
    - `active/`: Ongoing tasks.
    - `completed/`: Historical record of decisions and implementations.
    - `tech-debt-tracker.md`: A live list of technical debt identified by agents or humans.
- **product-specs/**: Business requirements. Start here before writing any code.
- **generated/**: Store artifacts that are automatically updated (e.g., DB schemas, API docs).
- **references/**: `.txt` files specifically formatted for LLMs to explain complex external systems (Nixpacks, Design Systems, etc.).

### The Ralph Loop
Humans interact with this system primarily through prompts and architectural constraints. Instead of writing code line-by-line, the developer:
1. **Sets the Intent**: Describes a task via a product spec or issue.
2. **Starts the Loop**: The agent takes the task and iterates autonomously.
3. **Monitors the Satisfice**: The agent implements code, performs local and cloud-based self-reviews, and responds to feedback from other agents or humans.
4. **Completion**: The loop terminates only when all agent reviewers and quality checks (defined in `QUALITY_SCORE.md`) are satisfied.

The goal is to maximize **Agent Legibility**—ensuring that an AI agent can understand the entire domain, architecture, and intent of the project directly from the repository.

## Developer Instructions
1. **Initialize the Mission**: Fill out `AGENTS.md` with your project's specific goals.
2. **Set the Laws**: Define your dependency layers in `ARCHITECTURE.md`.
3. **Plan First**: Before implementing a feature, create a file in `docs/product-specs/` and a corresponding plan in `docs/exec-plans/active/`.
4. **Mechanical Enforcement**: Use the principles in `QUALITY_SCORE.md` to guide your automated tests and linters.
