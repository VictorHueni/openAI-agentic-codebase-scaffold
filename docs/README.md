# Scaffold Working Docs

This folder contains the PRDs, Execution Plans, and Design Documents used to **build the scaffold itself**.

## Structure

| Folder | Purpose |
|--------|---------|
| `product-specs/` | PRDs for scaffold features (e.g., the hire/fire CLI utility) |
| `exec-plans/active/` | Implementation plans currently being worked on |
| `exec-plans/completed/` | Archived plans for delivered scaffold features |
| `design-docs/` | Technical design documents for scaffold architecture |
| `generated/` | Auto-generated scaffold artifacts |
| `references/` | LLM-readable references specific to scaffold development |

## How this relates to `harness/`

- **`docs/`** (this folder) contains working documents for the scaffold project.
- **`harness/docs/`** contains the clean template documentation engine shipped to users.
- Skills and workforce templates point to `docs/` by default (relative to project CWD).

## Getting Started with the Template

See [`harness/README.md`](../harness/README.md) for instructions on how to use the portable template in your own project.
