# Skill and agent-file conventions

The detailed authoring rules for this repository. `AGENTS.md` is the map; this file is the reference. `harness/check.py` enforces the mechanical subset; `docs/golden-principles.md` explains the reasoning.

## Creating a new skill

1. Create `.agents/skills/<skill-name>/SKILL.md`. The directory name must match the frontmatter `name`: lowercase letters, numbers, and hyphens only, max 64 chars, verb-first and specific (`product-naming`, `pricing-page-audit` — never `helper`, `utils`).
2. Write the frontmatter:

```yaml
---
name: skill-name
description: What the skill does and when to use it. Third person, specific, max 1024 chars. Include trigger phrases, e.g. "Use when the user invokes /skill-name or asks to ...".
---
```

3. Write the body following the structure below.
4. Add a row to the "Skills in this repository" table in the root `README.md` (skill link, category, one-sentence description, invocation).
5. Run `python3 harness/check.py` and iterate until it passes.

## Skill body structure

Every skill contains these sections, in this order (harness-enforced):

1. **Title + one-paragraph summary** of what the workflow produces.
2. **Invocation** — the slash command.
3. **Required input** — what the user must provide; what to infer versus ask about. Bias toward starting work: ask at most one clarifying question, and only when research or output would otherwise be useless.
4. **Outcome** — the concrete deliverables, listed up front.
5. **Operating principles** — numbered rules that resolve judgment calls during execution.
6. **Workflow** — numbered stages, each with an explicit exit criterion. Define JSON schemas for any structured data passed between stages (schemas may live in `reference.md` when the stage summary links them).
7. **Quality controls** — a final checklist the agent verifies before delivering.
8. **Failure handling** — what to do when tools, subagents, or data are unavailable.

## Writing rules

- Assume a capable agent. Include only knowledge it lacks: the workflow, the constraints, the schemas, the domain judgment. Cut background explanations.
- `SKILL.md` under 500 lines; overflow moves to `reference.md`, linked one level deep (no deeper nesting).
- One term per concept, used consistently throughout.
- POSIX paths only. Scripts must document their dependencies and state whether the agent should execute or read them.
- Everything in `docs/golden-principles.md` applies: exact numbers, no time-sensitive content outside marked sections, lead with the deliverable, honest degradation, no clearance claims.

## Cross-tool subagent roles

Skills with multi-agent workflows may ship role definitions in `<skill-name>/agents/*.md`. These let hosts with project-subagent support (Cursor, Claude Code) run each role on an appropriate model tier. They are an optimization layer, never a dependency: every skill must be fully executable from `SKILL.md` and `reference.md` alone, and role files only repackage instructions the skill already contains.

**File format** — use only the frontmatter intersection that Cursor (`.cursor/agents/*.md`) and Claude Code (`.claude/agents/*.md`) both accept:

```yaml
---
name: <skill-name>-<role>      # prefix with the skill name to avoid collisions
description: What the role does and when the orchestrator should spawn it. Third person.
model: inherit                 # always `inherit` in committed files
---
Model tier: <semantic tier and reasoning-effort hint — first body line, harness-enforced>

Body = the role's system prompt: identity, invariants, and constraints.
The orchestrator supplies stage-specific prompts, schemas, and inputs at spawn time.
```

Do not commit tool-specific fields (`tools:` is Claude Code-only; `readonly:` and `is_background:` are Cursor-only). Document them as optional post-install additions in the skill's `README.md`, so one committed file loads cleanly in every host. Never pin model IDs anywhere in role files — declare tiers semantically and let users resolve them at install or spawn time.

**Installation mapping** (document in the skill's `README.md`):

- Cursor — symlink or copy `agents/*.md` into `.cursor/agents/` (project) or `~/.cursor/agents/` (global).
- Claude Code — symlink or copy into `.claude/agents/` or `~/.claude/agents/`.
- Codex — convert each file to `.codex/agents/<name>.toml`: frontmatter `name` and `description` map directly, the Markdown body becomes `developer_instructions`, and the tier hint may be expressed as `model_reasoning_effort`. Leave `model` unset so Codex auto-routes. Codex also honors per-spawn model requests made directly in skill instructions, so conversion is optional.

**SKILL.md wiring** — the skill's roles section states: use the shipped role definitions when the host has them installed or supports registering them; otherwise emulate each role as an isolated pass using the prompts in `reference.md`, and disclose the method.

## Validation

`python3 harness/check.py` from the repository root is the authoritative check; run it before finishing any change and iterate until green. It verifies frontmatter, naming, line budgets, section order, link depth, dead links, time-sensitive content, role-file format, duplication, README sync, and enforcement plumbing — each failure prints its own remediation instructions.

Judgment-level review beyond the mechanical checks (principle adherence, duplication below the detection threshold, semantic drift) is the job of the `/ai-review` skill.
