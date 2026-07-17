---
name: ai-review
description: Review skills, agent role files, and repository docs for adoption of AI/harness engineering best practices and adherence to the repository's golden principles. Runs the mechanical harness first, then a judgment-level review, and delivers a verdict-first report with located, remediable findings. Use when the user invokes /ai-review, asks to review a skill or agent change against best practices, or before merging any skill change.
---

# AI Review

A two-layer review of changes to skills, agent role files, and repository documentation: a deterministic harness pass for everything mechanically checkable, then a judgment pass against the golden principles for everything that is not. Produces a verdict-first report whose every finding names a location, cites evidence, and prescribes a fix.

## Invocation

`/ai-review` — optionally followed by a scope: a skill name, a file path, or `all`.

## Required input

Nothing beyond an optional scope. Infer the review target from repository state, in this order:

1. A scope supplied with the invocation.
2. Uncommitted changes (staged and unstaged), when any exist.
3. The current branch's diff against `main`, when it differs.
4. Otherwise the entire `.agents/skills/` tree.

Do not ask clarifying questions; state the inferred scope in the report header.

## Outcome

- A **verdict**: `approve`, `approve with advisories`, or `request changes`.
- A **findings list**, each finding with principle, severity, location, evidence, and remediation.
- A **promotion list**: recurring judgment findings that should become new mechanical harness checks.
- An honest statement of anything that could not be checked and why.

## Operating principles

1. **Mechanical first.** Never hand-review what `harness/check.py` already checks; run it and import its failures. The judgment pass covers only what determinism cannot.
2. **Every finding is actionable.** A finding without a location and a concrete fix is an opinion; drop it.
3. **Review against the principles, not personal taste.** Style preferences that no principle backs are out of scope. If a real problem has no covering principle, flag it as a proposed principle, clearly labeled.
4. **Severity is about consequences.** `violation` = will degrade future agent runs or mislead users (blocks approval). `advisory` = worth fixing, does not block. `note` = observation, no action required.
5. **Propose promotions.** When the same judgment finding appears more than once — in this review or across reviews — recommend encoding it as a harness check, with a sketch of the rule.
6. **Verdict first.** The report leads with the verdict and finding counts; detail follows.

## Workflow

### Stage 1 — Scope and mechanical baseline

1. Resolve the review scope per Required input and list the files in scope.
2. From the repository root, run `python3 harness/check.py`. Convert each failure that touches in-scope files into a finding with `severity: violation` and `source: harness`. Out-of-scope harness failures are reported in one summary line, not as findings.
3. Read `docs/golden-principles.md` and `docs/conventions.md`; they are the review standard.

Exit criterion: scope stated, harness executed (or its unavailability recorded), standards loaded.

### Stage 2 — Judgment review

A portable reviewer role definition ships in this skill's `agents/` folder. When the host has it installed as a project subagent, run this stage as that role so it executes on a strong reasoning tier; otherwise perform the stage as a single disciplined pass and say so in the report.

Review the in-scope files against each golden principle, looking specifically for what the harness cannot see:

- **Progressive disclosure** — Is `SKILL.md` genuinely a workflow, or padded with background a capable agent already knows? Is `reference.md` content actually referenced from the body? Would an agent reading only the entry point know where to look next?
- **Future-proofing** — Semantic claims that will rot without matching the harness regexes: product feature assumptions, host-behavior claims, pricing implications, or benchmarks stated as timeless facts.
- **Single source of truth** — Paraphrased duplication below the harness's exact-sentence threshold; the same rule stated differently in two files; role files containing instructions that exist nowhere in the skill (a graceful-degradation breach).
- **Graceful degradation** — Walk each workflow stage asking: what happens with no subagents, no web access, no installed role files? Failure handling must cover every tool the workflow invokes.
- **Exact numbers** — Adjectives where counts belong; rubric weights that do not sum to 100%; schemas missing fields the workflow later relies on.
- **Lead with the deliverable** — Reports or skills that bury the answer under process.
- **Point-in-time honesty** — Research or availability language that overclaims; any wording resembling clearance.
- **Structural soundness** — Stages without real exit criteria; hand-offs without schemas; quality-control checklists that no longer match the workflow they check.

Record each finding in the schema below.

```json
{
  "finding_id": "F-01",
  "source": "harness | judgment",
  "principle": "progressive-disclosure | future-proofing | single-source-of-truth | graceful-degradation | mechanical-enforcement | symlink-over-copy | exact-numbers | lead-with-deliverable | repo-as-record | point-in-time-honesty | structure | proposed-principle",
  "severity": "violation | advisory | note",
  "location": "relative/path.md:line or relative/path.md#heading",
  "evidence": "quoted text or concrete observation",
  "remediation": "the specific change that resolves the finding"
}
```

Exit criterion: every in-scope file reviewed against every principle; every finding schema-complete.

### Stage 3 — Verdict and report

1. Verdict: `request changes` when any `violation` exists; `approve with advisories` when only advisories; `approve` when neither.
2. Render the report in this order: verdict and counts; findings grouped by severity (table: id, principle, location, evidence, remediation); promotion list (proposed harness checks with rule sketches); anything not checked and why.
3. When the environment supports it, offer to apply the remediations; never apply them silently as part of the review.

Exit criterion: report delivered, verdict consistent with findings, unchecked areas disclosed.

## Quality controls

Before delivering, verify:

- [ ] The harness was executed, or its unavailability is stated in the report
- [ ] Every finding has principle, severity, location, evidence, and remediation
- [ ] No finding is a style preference without a backing principle
- [ ] The verdict follows mechanically from the severity counts
- [ ] Recurring judgment findings produced promotion proposals
- [ ] The report leads with the verdict, not the method

## Failure handling

- **Harness missing or errors:** record it as a `violation` against mechanical-enforcement, proceed with the judgment pass, and state that mechanical coverage is absent.
- **Git unavailable or no diff resolvable:** fall back to reviewing the whole `.agents/skills/` tree and say so.
- **Scope names a nonexistent skill or path:** report the mismatch and list available skills; do not guess.
- **Standards files missing:** review against the principle names embedded in the finding schema and flag the missing files as a `violation`.
- **Subagent support absent:** perform the review as a single pass; do not claim an isolated reviewer was used.
