# AGENTS.md

Guidance for coding agents working in this repository. Read this before creating or editing anything.

## Project overview

A public collection of [Agent Skills](https://agentskills.io) for technical startup founders, covering product, marketing, and engineering workflows. There is no application code: the deliverables are `SKILL.md` files and their supporting assets. Quality bar is high — each skill must be a rigorous, self-contained workflow an agent can execute end to end without this repository's other files.

## Repository structure

```
.agents/skills/<skill-name>/   # One directory per skill (cross-tool standard location)
  SKILL.md                     # Required: frontmatter + instructions
  reference.md                 # Optional: detailed material loaded on demand
  README.md                    # Optional: human-facing guidance (model selection, host setup)
  agents/                      # Optional: portable subagent role files (see "Cross-tool subagent roles")
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

## Cross-tool subagent roles

Skills with multi-agent workflows may ship role definitions in `<skill-name>/agents/*.md`. These files let hosts that support project subagents (Cursor, Claude Code) run each role on an appropriate model tier. They are an optimization layer, never a dependency.

**Hard rule — graceful degradation:** every skill must be fully executable from `SKILL.md` (plus `reference.md`) alone, with zero agent files installed. Role files repackage instructions the skill already contains; they never hold instructions that exist nowhere else in the skill.

**File format.** Use only the frontmatter intersection that Cursor (`.cursor/agents/*.md`) and Claude Code (`.claude/agents/*.md`) both accept:

```yaml
---
name: <skill-name>-<role>      # prefix with the skill name to avoid collisions
description: What the role does and when the orchestrator should spawn it. Third person.
model: inherit                 # always `inherit` in committed files — see future-proofing
---
Body = the role's system prompt: identity, invariants, and constraints.
The orchestrator supplies stage-specific prompts, schemas, and inputs at spawn time.
```

Do not commit tool-specific fields (`tools:` is Claude Code-only; `readonly:` and `is_background:` are Cursor-only). Document them as optional post-install additions in the skill's `README.md` instead, so one committed file loads cleanly in every host.

**Future-proofing — never pin models.** Committed files must not contain model IDs, vendor aliases, or version numbers; they rot as new models ship. Instead, the first body line of each role declares its tier semantically ("Model tier: strongest creative model available" / "fastest inexpensive model available") plus a reasoning-effort hint (`low`/`medium`/`high` level names are durable across model generations). Hosts and users resolve tiers at install or spawn time. Concrete model names belong only in a skill `README.md` section clearly marked as point-in-time.

**Installation mapping** (document in the skill's `README.md`):

- Cursor — copy `agents/*.md` to `.cursor/agents/` (project) or `~/.cursor/agents/` (global).
- Claude Code — copy `agents/*.md` to `.claude/agents/` or `~/.claude/agents/`.
- Codex — convert each file to `.codex/agents/<name>.toml`: frontmatter `name` and `description` map directly, the Markdown body becomes `developer_instructions`, and the tier hint may be expressed as `model_reasoning_effort`. Leave `model` unset so Codex auto-routes by task. Codex also honors per-spawn model requests made directly in skill instructions, so conversion is optional.

**SKILL.md wiring.** The skill's roles section should state: use the shipped role definitions when the host has them installed or supports registering them; otherwise emulate each role as an isolated pass using the prompts in `reference.md`, and disclose the method.

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
- [ ] Any `agents/*.md` role files use only the shared frontmatter fields (`name`, `description`, `model: inherit`), contain no model IDs, and duplicate no instructions that are absent from the skill itself
- [ ] The skill runs end to end with no agent files installed (graceful degradation)

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
