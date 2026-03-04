# Documentation Index

This is the knowledge layer of the harness. Everything an agent (or human) needs to understand *what* to build, *how* to build it, and *what happened* lives here.

## Folder Map

| Folder                  | Purpose                                                                                                 | Skill                         | Key Files                                            |
| ----------------------- | ------------------------------------------------------------------------------------------------------- | ----------------------------- | ---------------------------------------------------- |
| `product-specs/`        | **What to build.** PRDs that define user problems, goals, stories, and acceptance criteria.             | `spec-prd-creator`            |                                                      |
| `exec-plans/active/`    | **How to build it.** Incremental implementation plans with test gates, currently in progress.           | `spec-implementation-planner` |                                                      |
| `exec-plans/completed/` | **What was built.** Archived plans that have passed all increments — the delivery history.              | --                            |                                                      |
| `exec-plans/`           | Shared tracking artifacts                                                                               | --                            | [Tech Debt Tracker](exec-plans/tech-debt-tracker.md) |
| `design-docs/`          | **Why we build it this way.** Technical design documents, ADRs, and non-negotiable engineering beliefs. | `spec-adr-manager`            | [Core Beliefs](design-docs/core-beliefs.md)          |
| `references/`           | **External context.** LLM-friendly documentation snapshots for frameworks, tools, and design systems.   | --                            |                                                      |
| `generated/`            | **Machine-maintained artifacts.** Auto-generated or manually updated files (schemas, API docs).         | --                            |                                                      |
