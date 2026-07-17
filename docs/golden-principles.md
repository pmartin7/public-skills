# Golden principles

Opinionated, mostly mechanical rules that keep this repository legible and consistent for every future agent run. When a principle can be checked deterministically, it is enforced by `harness/check.py`; the rest are verified by the `/ai-review` skill and human judgment. When you find yourself repeatedly correcting the same problem, promote the correction into a harness check rather than re-explaining it.

1. **Progressive disclosure.** Entry points are maps, not manuals. `AGENTS.md` stays under 120 lines and points to deeper sources of truth. `SKILL.md` stays under 500 lines; prompt templates, report formats, and procedural detail live in `reference.md`, linked exactly one level deep. A reader (human or agent) should always start small and be told where to look next. *(Enforced: line limits, link depth.)*

2. **Future-proof by default.** No model IDs, version numbers, dates, or "as of" claims anywhere in a skill — they rot within months. Express capability needs as semantic tiers ("strongest creative model available", "fastest inexpensive model") and durable level names (`low`/`medium`/`high` reasoning effort). Concrete model names are allowed only inside a section whose heading is marked "Point-in-time" or "Time-sensitive". *(Enforced: time-sensitivity scan.)*

3. **Single source of truth, no duplication.** Each piece of content has one canonical home: workflow rules in `SKILL.md`, stage prompts and reusable detail in `reference.md`, human guidance in a skill `README.md`, role identity in `agents/*.md`. Everything else links to the canonical copy. The one sanctioned exception: `agents/*.md` role files repackage invariants the skill already contains, because hosts load them standalone. *(Enforced: duplicate-sentence scan across SKILL/reference/README.)*

4. **Graceful degradation.** Every skill must run end to end from `SKILL.md` and `reference.md` alone — with no role files installed, no subagent support, no web access assumptions beyond what failure handling covers. Optional infrastructure improves execution; it never gates it. Degrade honestly: never fabricate capabilities, results, or parallel subagents that were not used.

5. **Mechanical enforcement over prose.** A rule that matters becomes a harness check; a rule that stays prose is a suggestion. Harness error messages are written as remediation instructions for the agent that will fix them — state what is wrong, where, and exactly what to do.

6. **Symlink over copy.** Installation instructions prefer `ln -s` so installed skills and role files stay current with `git pull`; copying is the fallback for hosts that do not follow symlinks. Never maintain two copies of the same content in the repository. *(Enforced: no committed tool-specific trees; README must offer symlinks.)*

7. **Exact numbers over adjectives.** "Generate exactly 20 candidates", never "several candidates". Ambiguity in a skill multiplies across every future run.

8. **Lead with the deliverable.** Final reports start with the answer; skills state their outcome before their process; findings come before methodology.

9. **Repository knowledge is the system of record.** Anything an agent needs must be discoverable inside the repository — not in chat history, external docs, or anyone's head. Decisions worth keeping become files.

10. **Point-in-time honesty.** Research results (web checks, domain signals, benchmarks) are proxies at a moment in time. Skills must say so and must never claim legal, medical, financial, or trademark clearance.
