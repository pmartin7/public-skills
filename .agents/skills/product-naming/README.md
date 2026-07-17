# Product Naming — Model and Settings Guide

How to choose models and sampling settings when running the [`product-naming`](SKILL.md) workflow. The skill itself is model-agnostic; this guide explains how to get the most creativity and quality per token from whatever models are available.

## Why model choice matters here

Post-training alignment makes language models converge on the most typical answer — a phenomenon known as mode collapse, driven by typicality bias in preference data ([Verbalized Sampling, arXiv:2510.01171](https://arxiv.org/abs/2510.01171)). In naming, the typical answer is a descriptive two-common-word compound (`Threadlight`, `Proofloop`), which is exactly what every other AI-assisted team in the category also generates — so those names are both less distinctive and more likely to already be in use. The workflow's anti-convergence rules (stem caps, invented-name quotas, typicality self-checks) fight this at the prompt level; the model and settings choices below fight it at the sampling level.

## Role-by-role recommendations

These are stated by model class, not product name, so they stay valid as model lineups change.

| Role | Model class | Temperature | Why |
|---|---|---|---|
| Ideators (association rounds 1–2) | Strongest available creative/frontier model | 0.9–1.1 | Diversity is the whole point of these stages; capable models benefit most from verbalized sampling |
| Ideators (name generation) | Same frontier creative model | 0.9–1.0 | High enough for novel combinations, low enough for pronounceable phonetics |
| Curator (dedupe, coverage) | Fast mid-tier or budget model | 0–0.2 | Mechanical classification; determinism beats flair |
| Ballot Manager (tally) | Script it, or a budget model | 0 | Borda arithmetic must be exact — prefer a short script over a model |
| Voters (blind ballots) | Frontier model | 0.3–0.5 | Judgment should be stable but not identical across the eight ballots |
| Web Checker | Fast model with web-search tooling | 0 | Factual retrieval and severity grading; creativity is a liability |

Rules of thumb for the sampling parameters:

- **Tune temperature or top-p, not both.** Leave top-p at the provider default (0.9–1.0) and move temperature. Their interaction is unpredictable and hard to debug.
- **Never run high temperature without a nucleus filter.** Above roughly 1.2, most models degrade into incoherent phonetics; 0.9–1.1 with default top-p is the sweet spot for name ideation.
- **Multiple moderate samples beat one hot sample.** Eight ideators at temperature ~1.0 produce more usable diversity than one ideator at 1.5. This is why the workflow uses eight isolated passes.
- **A light frequency penalty (~0.3–0.5) helps name generation** when the provider supports it: it discourages the model from reusing the same root across candidates (`Datashield`, then `Dataguard`, then `Datakeep`).

## When you cannot set temperature

Many agent environments (Claude, Codex, Cursor) and most reasoning models do not expose sampling parameters — reasoning models largely flatten the temperature lever anyway, because deliberation, not sampling, shapes the output. Compensate at the prompt level; the skill already builds these in:

1. **Verbalized sampling.** Ask for a set of candidates with self-assessed typicality and require a share of low-typicality picks. This recovers 1.6–2.1× diversity over direct prompting without retraining ([arXiv:2510.01171](https://arxiv.org/abs/2510.01171)).
2. **Isolated persona passes.** Distinct personas with different reference territories shift the semantic prior of each pass, which parallel samples at one temperature cannot do.
3. **Hard negative constraints.** Explicit stem caps and banned stock affixes (`-ly`, `-ify`, `-io`, `-hub`, `-AI`) remove the modal outputs from the space entirely.
4. **Lower reasoning effort for ideation.** If the model exposes a reasoning-effort control, use a low or medium setting for association and name generation — extended deliberation pushes reasoning models toward the safest answer. Reserve high effort for the Curator's dedupe judgment and the Web Checker's severity grading, where correctness matters more than surprise.

## Enforcing tiers per host

This skill ships portable role definitions in [`agents/`](agents/) — ideator, curator, voter, and web checker — as Markdown files using only the frontmatter fields Cursor and Claude Code both accept (`name`, `description`, `model`). The committed files set `model: inherit` and declare their tier semantically in the body, so they never go stale as model lineups change; you resolve tiers to concrete models at install time if you want hard pinning. The skill remains fully functional with none of these installed — the orchestrator then emulates the roles as isolated passes.

To install:

- **Cursor** — copy `agents/*.md` to `.cursor/agents/` (project) or `~/.cursor/agents/` (global). To pin a tier, replace `inherit` with a model ID from your enabled models, optionally with bracket parameters (e.g. `model: <id>[effort=low]`). You may also add the Cursor-only fields `readonly: true` (curator, voter, checker) and `is_background: true` (ideators). Without pinning, the orchestrator can still pass a model per spawn via the subagent tool's `model` parameter.
- **Claude Code** — copy `agents/*.md` to `.claude/agents/` or `~/.claude/agents/`. Tier aliases (`haiku`, `sonnet`, `opus`) track the latest model in each tier, which is the most future-proof pinning available: set `model: haiku` on the curator and web checker, keep the ideators and voters on a top tier or `inherit`. You may add a Claude-only `tools:` field to restrict roles. `CLAUDE_CODE_SUBAGENT_MODEL` overrides everything for cheap dry runs.
- **Codex** — convert each file to `.codex/agents/<name>.toml`: `name` and `description` map directly, the body becomes `developer_instructions`, and the tier hint becomes `model_reasoning_effort` (`low` for curator, `medium` for ideators/voters, `high` for the checker). Leave `model` unset so Codex auto-routes by task — its router already favors cheaper models for light work. Conversion is optional: Codex applies per-spawn model and effort overrides when skill instructions request them explicitly.

No agent host currently exposes temperature or top-p. Where tiering is unavailable or sampling control matters, fall back to the prompt-level techniques in the previous section, or drive the stages as a script against model APIs directly — the per-stage JSONL artifacts make the workflow scriptable without changing the process.

## Token efficiency

The workflow generates 720 raw associations and 160 raw names per run, so token discipline matters:

- **Split model tiers.** Ideation and voting deserve the frontier model; curation, tallying, and web checks run fine on a model a tier or two cheaper. In a typical run, the mechanical stages are more than half the tokens.
- **Pass artifacts, not transcripts.** Each stage should read the prior stage's JSON/JSONL artifact, never the conversation history. This keeps every subagent context small and prevents cross-contamination between ideators.
- **Keep schemas terse.** JSONL with the short field names in the skill's schemas; no prose wrappers around records.
- **Script the arithmetic.** The Borda tally, tie-breakers, and dedupe normalization (lowercasing, plural folding) are a few lines of code — spending model tokens on them risks errors and wastes budget.
- **Cap the ballot context.** Voters need the brief, the values, and the candidate list — not the association map or the curation logs.

## Point-in-time model notes

> **Time-sensitive section.** Model names, capabilities, and prices below reflect the landscape when this guide was last revised. Verify against current benchmarks before relying on them.

- **Claude (Opus / Fable class)** — strongest instruction following plus top-tier creative output; the safest default for ideators and voters, where the workflow's counting and schema constraints must be followed exactly while staying inventive.
- **GPT (frontier class)** — fastest high-volume ideation and the strongest structured-output adherence; a good ideator choice when run cost or latency matters, and a natural fit for the Curator.
- **Gemini (Pro class)** — leads creative-writing arena scores at a materially lower price; the value pick for ideation rounds, and its large context helps if you run curation over the full association pool in one pass.
- Any small fast model from these families is adequate for the Web Checker and Ballot Manager.
