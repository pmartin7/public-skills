# Doc-gardening task

A periodic drift review for this repository. Run it as a recurring agent task (or paste it as a prompt) on a regular cadence — the deterministic harness catches rule breaches at edit time; this task catches the slow decay it cannot see. Findings become a PR (or a findings report when write access is unavailable), never silent fixes to `main`.

## Task

You are gardening the skills repository. Read `AGENTS.md`, `docs/golden-principles.md`, and `docs/conventions.md`, then review the full `.agents/skills/` tree and repository docs for drift. Run `python3 harness/check.py` first; anything it already flags is out of scope for you.

Look for:

1. **Semantic staleness** — instructions that no longer match how the referenced hosts, tools, or formats actually behave; claims that have quietly become wrong.
2. **Paraphrased duplication** — the same rule stated differently in two places, below the harness's exact-sentence threshold. Identify the canonical home and fold the copies into links.
3. **Checklist drift** — quality-control checklists that mention steps their workflow no longer contains, or miss steps it gained.
4. **Orphaned content** — `reference.md` sections nothing links to; role files for roles a skill no longer defines; README claims about files that moved.
5. **Point-in-time sections** — verify each clearly marked time-sensitive section still reflects reality; update or trim it, keeping the marker.
6. **Promotion candidates** — judgment rules you corrected more than once that should become mechanical harness checks; propose the check with a rule sketch rather than implementing silently.

## Output

A single report, verdict-first: number of drift findings by category, then per finding the location, evidence, and proposed fix. Apply fixes on a branch and open a PR titled `Garden: <summary>`; keep the PR reviewable in under five minutes. If nothing has drifted, say so explicitly — do not invent work.
