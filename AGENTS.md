# AGENTS.md

Guidance for coding agents working in this repository. This file is a map, not a manual: read the pointer targets before creating or editing anything, and rely on the harness to verify your work.

## Project overview

A public collection of [Agent Skills](https://agentskills.io) for technical startup founders, covering product, marketing, and engineering workflows. There is no application code: the deliverables are `SKILL.md` files and their supporting assets. Quality bar is high — each skill must be a rigorous, self-contained workflow an agent can execute end to end without this repository's other files.

## Repository map

```
.agents/skills/<skill-name>/   # One directory per skill (cross-tool standard location)
  SKILL.md                     # Required: frontmatter + instructions
  reference.md                 # Optional: detailed material loaded on demand
  README.md                    # Optional: human-facing guidance (model selection, host setup)
  agents/                      # Optional: portable subagent role files
  scripts/                     # Optional: executable helpers
docs/
  golden-principles.md         # The rules that keep this repo coherent — read before writing
  conventions.md               # Detailed authoring rules for skills and role files
harness/
  check.py                     # Mechanical validation; run before finishing any change
  gardening-prompt.md          # Periodic drift-review task
.githooks/pre-commit           # Runs the harness on commit (git config core.hooksPath .githooks)
AGENTS.md                      # This file
README.md                      # Human-facing docs; lists every skill
```

## How to work here

1. Read [docs/golden-principles.md](docs/golden-principles.md) — the operating principles behind every rule.
2. Follow [docs/conventions.md](docs/conventions.md) when creating or editing skills and `agents/*.md` role files.
3. Before finishing **any** change, run `python3 harness/check.py` from the repository root and iterate until it passes. Every failure message contains its own remediation instructions.
4. For non-mechanical review (principle adherence, semantic drift, near-duplication), invoke the `/ai-review` skill on your change.
5. Keep the root `README.md` skill table in sync with skills in the same commit.

## Boundaries

**Always**
- Match the structure and tone of the existing skills; `product-naming` is the reference implementation.
- Run the harness before finishing; never leave it red.

**Ask first**
- Renaming or deleting an existing skill (published names are user-facing API).
- Restructuring the repository layout or moving skills out of `.agents/skills/`.
- Weakening or deleting a harness check.

**Never**
- Commit secrets, API keys, or personal data inside skills.
- Commit tool-specific trees (`.claude/`, `.codex/`, `.cursor/agents/`, `.cursorrules`, `CLAUDE.md`) duplicating skill content; `.agents/skills/` is the single source of truth.
- Pad skills with generic advice an agent already knows.
- Pin model IDs or dates outside clearly marked point-in-time sections.

## Git workflow

- Branch from `main`; one skill per PR.
- Enable the hooks once per clone: `git config core.hooksPath .githooks`.
- Commit messages: imperative mood, scoped to the skill, e.g. `Add pricing-page-audit skill` or `Fix voting tally in product-naming`.
- PR description: what the skill does, the intended trigger, and a sample invocation transcript if available.
