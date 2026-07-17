# Public Skills

A curated collection of [Agent Skills](https://agentskills.io) for **technical startup founders**, covering the key operations of building a new product: product, marketing, and engineering. Each skill packages a rigorous, repeatable workflow that AI coding agents (Cursor, Claude Code, Codex, and any tool supporting the Agent Skills open standard) can load and execute.

## About the author

Curated by **[Pierre Martin](https://pierre-martin.com)** — CTO of [Gavel](https://www.gavel.io), mentor at [Neo](https://neo.com) and AI House, formerly CTO of Beacon and founding Head of Engineering of Amazon Live Sports. Full bio at [pierre-martin.com](https://pierre-martin.com) and [LinkedIn](https://www.linkedin.com/in/pierremartin7/).

## Skills in this repository

| Skill | Category | What it does |
|-------|----------|--------------|
| [`product-naming`](.agents/skills/product-naming/SKILL.md) | Product & Marketing | A multi-agent naming workflow: 8 persona-driven ideators generate and refine hundreds of associations from your product description and five desired customer feelings, then produce brand-name candidates, blind-vote a shortlist, and run lightweight web and domain-use checks on the top 12. Invoke with `/product-naming`. |

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

**Cursor** — reads `.agents/skills/` natively. Either open this repo directly, or install skills globally for all your projects:

```bash
cp -R public-skills/.agents/skills/* ~/.cursor/skills/
```

**Claude Code** — copy skills into your personal skills directory (all projects), or symlink into a specific project:

```bash
# Personal (all projects)
cp -R public-skills/.agents/skills/* ~/.claude/skills/

# Or per-project
ln -s /path/to/public-skills/.agents/skills your-project/.claude/skills
```

**Codex** — reads `.agents/skills/` natively in a project, or install globally:

```bash
cp -R public-skills/.agents/skills/* ~/.agents/skills/
```

**Other tools** — any agent supporting the Agent Skills standard will pick these up from its documented skills directory; copy or symlink the skill folders there.

### 3. Use a skill

Invoke a skill explicitly with a slash command (e.g. `/product-naming`), or simply describe the task — the agent matches your request against skill descriptions and applies the relevant one. For example:

> /product-naming
> Product: a scheduling tool for indie fitness coaches.
> Feelings: in control, professional, energized, trusted, unburdened.

## Contributing

New skills follow the conventions in [AGENTS.md](AGENTS.md), which gives coding agents (and humans) everything needed to author a skill consistent with this repository. Open a PR with a single skill per change.

## License

[MIT](LICENSE) © Pierre Martin
