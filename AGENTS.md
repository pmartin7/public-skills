# AGENTS.md

Guidance for coding agents working in this repository. Read this before creating or editing anything.

## Project overview

A public collection of [Agent Skills](https://agentskills.io) for technical startup founders, covering product, marketing, and engineering workflows. There is no application code: the deliverables are `SKILL.md` files and their supporting assets. Quality bar is high — each skill must be a rigorous, self-contained workflow an agent can execute end to end without this repository's other files.

## Repository structure

```
.agents/skills/<skill-name>/   # One directory per skill (cross-tool standard location)
  SKILL.md                     # Required: frontmatter + instructions
  reference.md                 # Optional: detailed material loaded on demand
  scripts/                     # Optional: executable helpers
AGENTS.md                      # This file
README.md                      # Human-facing docs; lists every skill
LICENSE                        # MIT
```

## Creating a new skill

1. Create `.agents/skills/<skill-name>/SKILL.md`. The directory name must match the frontmatter `name`: lowercase letters, numbers, and hyphens only, max 64 chars, verb-first and specific (`product-naming`, `pricing-page-audit` — never `helper`, `utils`).
2. Write the frontmatter:

```yaml
---
name: skill-name
description: What the skill does and when to use it. Third person, specific, max 1024 chars. Include trigger phrases, e.g. "Use when the user invokes /skill-name or asks to ...".
---
```

3. Write the body following the conventions below.
4. Add a row to the "Skills in this repository" table in `README.md` (skill link, category, one-sentence description, invocation).

## Skill body conventions

Structure every skill in this order:

1. **Title + one-paragraph summary** of what the workflow produces.
2. **Invocation** — the slash command.
3. **Required input** — what the user must provide; what to infer versus ask about. Bias toward starting work: ask at most one clarifying question, and only when research or output would otherwise be useless.
4. **Outcome** — the concrete deliverables, listed up front.
5. **Operating principles** — numbered rules that resolve judgment calls during execution.
6. **Workflow** — numbered stages, each with an explicit exit criterion. Define JSON schemas for any structured data passed between stages.
7. **Quality controls** — a final checklist the agent verifies before delivering.
8. **Failure handling** — what to do when tools, subagents, or data are unavailable. Degrade honestly; never fabricate capabilities or results.

Writing rules:

- Assume a capable agent. Include only knowledge it lacks: the workflow, the constraints, the schemas, the domain judgment. Cut background explanations.
- Target under 500 lines for `SKILL.md`. Move prompt templates and other reusable detail to a `reference.md` linked one level deep from `SKILL.md` (no deeper nesting).
- Prefer exact numbers over adjectives ("generate exactly 20 candidates", not "several candidates").
- One term per concept, used consistently throughout.
- Lead with the deliverable: final reports start with the answer, not the process.
- Skills must not claim legal, medical, or financial clearance. Research results are point-in-time signals; say so explicitly.
- Never claim parallel subagents were used when the environment lacks them; emulate isolated passes and disclose the method.
- No time-sensitive content (dates, versions, "as of ..."). If unavoidable, isolate it in a clearly marked section.
- POSIX paths only. Scripts must document their dependencies and state whether the agent should execute or read them.

## Validation checklist

Before finishing any skill change, verify:

- [ ] Directory name matches frontmatter `name`
- [ ] Description states WHAT and WHEN in third person, with trigger phrases
- [ ] Body targets under 500 lines; overflow moved to `reference.md`
- [ ] Every workflow stage has an exit criterion
- [ ] Structured hand-offs between stages have schemas
- [ ] Failure handling covers missing tools, malformed output, and unavailable data
- [ ] `README.md` skill table is updated
- [ ] Frontmatter starts and ends with `---` and contains valid `name:` and `description:` keys

## Boundaries

**Always**
- Match the structure and tone of the existing skills before writing a new one; `product-naming` is the reference implementation.
- Keep `README.md` and the skills in sync in the same commit.

**Ask first**
- Renaming or deleting an existing skill (published names are user-facing API).
- Restructuring the repository layout or moving skills out of `.agents/skills/`.

**Never**
- Commit secrets, API keys, or personal data inside skills.
- Add tool-specific config duplicating a skill (`.cursorrules`, `CLAUDE.md`); skills are the single source of truth.
- Pad skills with generic advice an agent already knows.

## Git workflow

- Branch from `main`; one skill per PR.
- Commit messages: imperative mood, scoped to the skill, e.g. `Add pricing-page-audit skill` or `Fix voting tally in product-naming`.
- PR description: what the skill does, the intended trigger, and a sample invocation transcript if available.
