# Public Skills

A curated collection of [Agent Skills](https://agentskills.io) for **technical startup founders**, covering the key operations of building a new product: product, marketing, and engineering. Each skill packages a rigorous, repeatable workflow that AI coding agents (Cursor, Claude Code, Codex, and any tool supporting the Agent Skills open standard) can load and execute.

## About the author

Curated by **[Pierre Martin](https://pierre-martin.com)** — CTO of [Gavel](https://www.gavel.io), mentor at [Neo](https://neo.com) and AI House, formerly CTO of Beacon and founding Head of Engineering of Amazon Live Sports. Full bio at [pierre-martin.com](https://pierre-martin.com) and [LinkedIn](https://www.linkedin.com/in/pierremartin7/).

## Skills in this repository

| Skill | Category | What it does |
|-------|----------|--------------|
| [`product-naming`](.agents/skills/product-naming/SKILL.md) | Product & Marketing | A multi-agent naming workflow: 8 persona-driven ideators generate and refine hundreds of associations from your product description and five desired customer feelings, then produce brand-name candidates, blind-vote a shortlist, and run lightweight, severity-graded web and domain-use checks on the top 12. Includes a [model and settings guide](.agents/skills/product-naming/README.md). Invoke with `/product-naming`. |
| [`ai-review`](.agents/skills/ai-review/SKILL.md) | Engineering | Reviews skills, agent role files, and repo docs against harness-engineering best practices and this repo's golden principles: runs the mechanical harness, then a judgment pass, and delivers a verdict-first report with located, remediable findings. Invoke with `/ai-review`. |

More skills are on the way. Watch or star the repo to follow along.

## What are Agent Skills?

A skill is a folder containing a `SKILL.md` file: YAML frontmatter (name, description) plus Markdown instructions. Compatible agents discover skills automatically, read the description to decide when a skill is relevant, and load the full instructions only when needed. The format is an open standard adopted by Cursor, Claude Code, OpenAI Codex, GitHub Copilot, Gemini CLI, and a growing list of tools.

Skills in this repo live under `.agents/skills/`, the cross-tool standard location.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/pmartin7/public-skills.git
```

### 2. Make the skills available to your agent

Prefer symlinks over copies: symlinked installs stay current with `git pull`, while copies silently go stale. Use `cp -R` only when your host does not follow symlinks.

**Cursor** — reads `.agents/skills/` natively. Either open this repo directly, or install skills globally for all your projects:

```bash
ln -s "$(pwd)/public-skills/.agents/skills"/* ~/.cursor/skills/
```

**Claude Code** — link skills into your personal skills directory (all projects), or into a specific project:

```bash
# Personal (all projects)
ln -s "$(pwd)/public-skills/.agents/skills"/* ~/.claude/skills/

# Or per-project
ln -s /path/to/public-skills/.agents/skills your-project/.claude/skills
```

**Codex** — reads `.agents/skills/` natively in a project, or install globally:

```bash
ln -s "$(pwd)/public-skills/.agents/skills"/* ~/.agents/skills/
```

**Other tools** — any agent supporting the Agent Skills standard will pick these up from its documented skills directory; symlink (or copy) the skill folders there.

### 3. Optional: install subagent role files

Some skills ship portable subagent role definitions in an `agents/` subfolder (e.g. `product-naming/agents/`). Installing them lets multi-agent workflows run each role on an appropriate model tier; skipping them is fine — every skill works without them.

```bash
# Cursor
ln -s "$(pwd)"/public-skills/.agents/skills/*/agents/*.md .cursor/agents/ 2>/dev/null

# Claude Code
ln -s "$(pwd)"/public-skills/.agents/skills/*/agents/*.md .claude/agents/ 2>/dev/null
```

The files use `model: inherit` by default; each skill's own `README.md` explains how to pin model tiers per role (and how to convert the files to Codex's `.codex/agents/*.toml` format).

### 4. Use a skill

Invoke a skill explicitly with a slash command (e.g. `/product-naming`), or simply describe the task — the agent matches your request against skill descriptions and applies the relevant one. For example:

> /product-naming
> Product: a scheduling tool for indie fitness coaches.
> Feelings: in control, professional, energized, trusted, unburdened.

## Contributing

New skills follow [AGENTS.md](AGENTS.md) and the detailed rules in [docs/conventions.md](docs/conventions.md), guided by [docs/golden-principles.md](docs/golden-principles.md). Before opening a PR:

```bash
git config core.hooksPath .githooks   # once per clone: runs the harness on every commit
python3 harness/check.py              # the same mechanical checks, on demand
```

CI runs the identical harness on every pull request. For judgment-level review beyond the mechanical checks, invoke the `/ai-review` skill on your change. One skill per PR.

## License

[MIT](LICENSE) © Pierre Martin
