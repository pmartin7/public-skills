---
name: product-naming
description: Generate, refine, rank, and lightly research memorable product or company names from a short product description and five desired customer feelings. Use when the user invokes /product-naming or asks for a rigorous multi-agent naming process with lightweight web and domain checks.
---

# Product Naming

A multi-agent naming workflow that moves from emotional associations to a voted shortlist, then performs lightweight point-in-time web and domain checks. Detailed procedures, prompt templates, stage schemas, and the report format live in [reference.md](reference.md).

## Invocation

`/product-naming`

## Required input

The user should provide:

1. **Product description** — a short description of what the product does, who it serves, and the category it competes in.
2. **Five core values or feelings** — exactly five things the customer should feel while using or thinking about the product.

Optional but useful:

- Target customer or buyer
- Industry and product category
- Target countries or languages
- Desired tone: serious, warm, technical, premium, playful, etc.
- Words, sounds, themes, or competitors to avoid
- Preferred domain extensions
- Whether the name must work as a company name, product name, or both

If the two required inputs are present, begin without asking unnecessary follow-up questions. Infer missing optional details from the product description and state material assumptions. Ask one concise question only when the category, customer, or intended meaning is too ambiguous to perform useful web checks.

## Outcome

Produce:

- A researched **top 12** selected strictly from ideator voting
- Lightweight web-presence and domain-use signals for every top-12 name
- The **top 30 names overall** by vote score
- Concise rationales connecting each shortlisted name to the product and values
- A clear statement that the checks are proxies, not trademark or registration clearance

## Operating principles

1. **Diverge before converging.** Ideators work independently in the first round.
2. **Use personas as creative lenses, not stereotypes.** Vary economic context, role, expertise, risk tolerance, and cultural reference style. Never caricature protected classes or infer tastes from race, ethnicity, religion, disability, sexuality, or similar traits.
3. **Preserve surprising associations.** Serious, literal, funny, indirect, literary, industrial, mythological, scientific, and popular-culture connections are all welcome.
4. **Do not confuse inspiration with permission.** Famous characters, franchises, and existing brands may inspire associations, but direct reuse should normally be excluded from final candidates.
5. **Prefer memorable speech.** Two to three syllables is ideal; four is the maximum unless the user explicitly relaxes the rule.
6. **Blind the vote.** Remove ideator identity and randomize candidate order before voting.
7. **Keep checks lightweight and honest.** Use simple web searches as proxies for obvious conflicts and domain use. Do not perform trademark-database, corporate-registry, or exhaustive domain research unless the user explicitly asks.
8. **Keep provenance.** Every association and name should retain its source persona, linked values, and generation round until the blind-voting stage.
9. **Make the workflow resumable.** Save the structured result of every stage when the environment supports files or persistent state.
10. **Fight convergence deliberately.** Aligned language models drift toward the same safe descriptive compounds — which are exactly the names adjacent products have already chosen. Enforce the stem caps, invented-name quotas, and typicality self-checks defined in Stages 5 and 6; a shortlist dominated by two-common-word compounds is a process failure, not a taste preference.
11. **Grade conflicts by severity.** A small, niche, dormant, or adjacent-category use is a risk signal, not a veto. Only an established, actively operating same-category use blocks a recommendation. Report everything else as graded risk and leave the judgment to the user.

## Model selection

Ideation and voting quality depend heavily on which model runs each role. See [README.md](README.md) in this skill folder for role-by-role model-class and sampling guidance, including how to compensate when temperature is not adjustable.

## Roles

The orchestrator creates the following agents or emulates them as isolated passes when true subagents are unavailable:

- **8 Ideators** — each receives a distinct socio-economic and decision-making persona
- **1 Curator** — deduplicates and organizes association pools after rounds 1 and 2
- **1 Ballot Manager** — anonymizes, randomizes, tallies, and resolves ties
- **1 Web Checker** — runs lightweight web searches for obvious name conflicts and domain use
- **1 Orchestrator** — validates inputs, manages state, enforces schemas, and writes the final report

Portable role definitions for the ideator, curator, voter, and web checker ship in this skill's `agents/` folder. When the host has them installed as project subagents (or supports registering them), spawn those roles by name so each runs on its configured model tier. Otherwise, emulate each role as an isolated pass using the prompts in [reference.md](reference.md) — the workflow is identical either way. The Ballot Manager's tally is arithmetic; prefer a short script over a model.

Never claim that parallel subagents were used when the environment does not provide them. In that case, perform eight deliberately isolated ideation passes and label the method accurately.

## State and artifacts

When possible, maintain these artifacts:

```text
product-naming/
  00-intake.json
  01-personas.json
  02-round1-associations.jsonl
  03-round1-deduped.json
  04-round2-associations.jsonl
  05-round2-deduped.json
  06-name-candidates.jsonl
  07-ballots.jsonl
  08-ranked-names.json
  09-web-domain-checks.json
  10-final-report.md
```

Each stage reads the prior canonical artifact rather than informal conversation summaries.

## Canonical input schema

```json
{
  "product_description": "string",
  "core_values": ["value 1", "value 2", "value 3", "value 4", "value 5"],
  "target_customer": "string or inferred",
  "industry": "string or inferred",
  "category": "string or inferred",
  "target_markets": ["country or language"],
  "tone": ["optional descriptors"],
  "avoid": ["optional words, sounds, themes, competitors"],
  "domain_preferences": [".com", "optional alternatives"],
  "name_scope": "product | company | both",
  "assumptions": ["material inferred assumptions"]
}
```

Reject or repair inputs with fewer or more than five core values. Preserve the user's wording, but the orchestrator may add a one-line operational interpretation for each value.

---

# Workflow

## Stage 0 — Intake and value interpretation

The orchestrator:

1. Parses the product description and exactly five core values.
2. Infers the target buyer, industry, category, and likely markets when omitted.
3. Converts each value into a naming brief containing:
   - What the value means in this product context
   - What it should not be confused with
   - Useful emotional, functional, sensory, and social directions
4. Records exclusions and naming constraints.
5. Creates eight non-overlapping personas following the [persona design guide](reference.md#persona-design): each persona varies at least four design dimensions, and the record uses the persona schema defined there.

Exit criterion: eight personas are meaningfully distinct and all required input fields are canonicalized.

## Stage 1 — Independent association generation

Run eight ideators independently. They must not see one another's output.

Each ideator generates **10 associations for each of the five values**, for **50 associations per ideator** and **400 raw associations total**.

Each set of 10 per value must spread across the five territory groups (literal, metaphorical/sensory, cultural/literary/mythic, industry/scientific, playful/phonetic) with at least 2 from each, quality permitting — the full territory list and variety quotas are in [Association territories and variety](reference.md#association-territories-and-variety). Records follow the [association schema](reference.md#association-schema-stage-1).

Mark existing character names, franchise names, celebrity names, and well-known brands as `direct_reuse_risk: high` even when they are useful creative seeds.

Exit criterion: each ideator has exactly 10 valid associations per value.

## Stage 2 — First curation and deduplication

The Curator receives all 400 raw associations.

Deduplicate both **within each ideator** and **across all ideators** while preserving provenance. Apply the normalization steps, five duplicate classes, and merged-cluster rules in the [curation procedure](reference.md#curation-procedure); output uses the [curated association schema](reference.md#curated-association-schema-stages-2-and-4). Redundancy goes; richness stays — meaningful semantic neighbors are never collapsed.

Also produce a coverage report per value and identify underexplored semantic territories for round 2.

Exit criterion: no obvious exact or near duplicates remain, provenance is preserved, and each value still has broad semantic coverage.

## Stage 3 — Inspired expansion

Return the deduplicated round-1 pool and coverage report to all eight ideators.

Each ideator generates **8 new associations for each value**, for **40 new associations per ideator** and **320 raw round-2 associations total**.

Round-2 associations must:

- Be genuinely new, not cosmetic variants
- Be inspired by paths in the curated pool
- Explore underrepresented territories identified by the Curator
- Extend associations one or two conceptual steps rather than simply restating them
- Include a short `inspired_by` list of canonical association IDs

Productive techniques (chains, bridges, transformations, etymological roots) are listed under [Expansion methods](reference.md#expansion-methods); records use the association schema plus the [round-2 additions](reference.md#round-2-additions-stage-3).

Exit criterion: each ideator produces exactly eight valid new associations per value, with traceable inspiration.

## Stage 4 — Second curation and deduplication

The Curator combines the round-1 canonical pool with all round-2 associations and repeats the Stage-2 process.

Additional requirements:

- Detect round-2 paraphrases of round-1 ideas
- Preserve cross-value bridge associations
- Flag overused naming territories such as generic speed, generic intelligence, generic trust, or generic Greek mythology when they dominate
- Identify the strongest 15-30 source associations per value for name generation
- Create an `underused_gems` list of unusual but productive associations

Exit criterion: a clean, well-covered canonical association map exists for all five values.

## Stage 5 — Brand-name generation

Each of the eight ideators receives:

- Canonical input
- Final deduplicated association map
- Strong source associations per value
- Underused gems
- Constraints and exclusions

Each ideator generates **20 brand-name candidates**, for **160 raw names total**. Candidates must satisfy the craft bar in [Candidate requirements and memorability devices](reference.md#candidate-requirements-and-memorability-devices): two-to-three syllables preferred (four maximum), pronounceable and spellable on first contact, linked to at least one core value, free of famous-name reuse and gimmick spellings. Records use the [candidate schema](reference.md#candidate-schema-stage-5).

### Anti-convergence rules

Descriptive two-common-word compounds (`Threadlight`, `Proofloop`, `Signalcraft`) are the names every AI-assisted team generates for the same category, so they are simultaneously the least distinctive and the most likely to already be in use. Each ideator must:

1. **Sample verbally before selecting.** Internally draft roughly 30 name ideas and estimate for each how likely the other seven ideators are to independently propose it or a close variant. Submit 20 with a deliberate spread: at least 8 of the 20 must be ideas the ideator judges unlikely to be duplicated.
2. **Cap stems.** No two of an ideator's 20 candidates may share the same leading morpheme, and no morpheme (prefix, root, or suffix) may appear in more than 2 of the 20.
3. **Avoid stock affixes.** Do not use `-ly`, `-ify`, `-io`, `-hub`, `-HQ`, or `-AI` suffixes, and avoid compound halves that merely restate the category (`mail`, `inbox`, `ad`, `task`) unless the other half is genuinely surprising.
4. **Honor overused-territory flags.** Any semantic territory the Curator flagged as overused may contribute at most 1 candidate.

### Portfolio diversity per ideator

Across 20 candidates, target roughly:

- 3 recognizable standalone words used in a distinctive way
- 4 compounds or clipped compounds
- 4 blends or portmanteaus
- 6 invented or root-derived names — Latin, Greek, or pronounceable multilingual roots, and phonetic inventions with intuitive spelling
- 3 mythic, literary, scientific, craft, or cultural transformations that do not directly reuse protected names

Do not force a weak category to hit the quota, but an ideator returning fewer than 4 invented or root-derived candidates must regenerate the shortfall before submitting.

Ideators should not run web or domain checks yet; early searching causes convergence toward mediocre domain-driven names.

### Pre-ballot cleanup

The Curator deduplicates the 160 names before voting:

- Exact spelling duplicates
- Case and punctuation variants
- Singular/plural variants
- Near-identical compounds
- Confusingly similar pronunciation
- Same invented stem with trivial suffix changes

Then enforce a pool-level stem cap: when more than 2 surviving candidates share a leading morpheme or the same suffix pattern (for example five `Thread-` names or three `-wise` names), keep the strongest 2 and cut the rest, crediting all creators of the retained forms.

For a name family, retain the strongest form and preserve all credited creators. Do not perform market or domain research at this stage.

Exit criterion: a blind-ready set of distinct candidate names exists with creator metadata stored separately.

## Stage 6 — Blind voting

The Ballot Manager:

1. Removes creator identity and self-scores.
2. Randomizes name order independently for each ideator.
3. Gives every ideator the product brief, five values, and the full deduplicated candidate pool.
4. Requires each ideator to rank exactly **12 names**.
5. Collects a concise reason for the top three and one risk note for any selected name that has a meaningful weakness.

### Voting rubric

Ideators should consider:

- Memorability — 20%
- Pronounceability and spelling — 15%
- Resonance with the five values — 20%
- Distinctiveness — 25%
- Product/category fit without being overly narrow — 10%
- Emotional and tonal fit — 10%

Distinctiveness rewards names a competitor is unlikely to arrive at independently. Voters must not penalize invented or root-derived names merely for unfamiliarity — `Kodak`, `Spotify`, and `Sonos` were unfamiliar once. A ballot in which 10 or more of the 12 ranked names are descriptive two-common-word compounds signals convergence; the Ballot Manager returns it once for revision with that observation.

Availability is not scored because it has not yet been researched. Ballots use the [ballot schema](reference.md#ballot-schema-stage-6).

### Tally

Use Borda scoring:

- Rank 1 = 12 points
- Rank 2 = 11 points
- ...
- Rank 12 = 1 point

For each name, calculate:

- Total points
- Number of unique voters
- Number of first-place votes
- Median rank among voters who selected it
- Distribution across persona types

Retain the **12 names with the highest point totals**. Do not replace a top-12 name merely because preliminary research later finds a conflict.

### Tie-breakers

Apply in order:

1. More unique voters
2. More first-place votes
3. Better median rank
4. Broader persona distribution
5. Fewer pre-research naming risks
6. Fewer syllables, provided quality is not reduced
7. Orchestrator judgment, documented in one sentence

Also retain the **top 30 names overall** by the same ranking.

Exit criterion: top 12 and top 30 are frozen before lightweight web and domain checks begin.

## Stage 7 — Lightweight web and domain checks

The Web Checker investigates only after voting is complete.

Run lightweight checks on the top 12 only. The purpose is to catch obvious conflicts and signs of domain use without turning naming into a trademark or domain-clearance project. Every result records the research date, exact queries, domains searched, and sources; findings are phrased as point-in-time proxies. Results use the [research schema](reference.md#research-schema-stage-7).

### Brand-conflict research

For each top-12 name, run at most these searches:

1. Exact quoted name
2. Exact name plus industry/category keywords

Classify with graded severity:

- **Blocking** — an established, actively operating product or company uses the exact name (or an indistinguishable form) in the same category for the same customer
- **Caution** — an active exact use exists in a closely adjacent category, or multiple unrelated active uses crowd the name enough to hurt discoverability
- **Minor signal** — the only findings are small or niche products, dormant or inactive sites, personal or hobby projects, package-registry entries (PyPI, npm, GitHub repositories), app-store side projects, individual profiles, or local businesses in other geographies or distant categories
- **No obvious conflict found** — the limited searches found no meaningful exact use
- **Uncertain** — results are incomplete, ambiguous, or unavailable

Severity rules:

- A name with only minor signals is **contested but plausibly winnable** and stays fully viable for recommendation; report the evidence and let the user judge.
- Only a blocking conflict disqualifies a name from recommendation. Caution downgrades but does not disqualify.
- A registered domain, by itself, is never a conflict. Nor is a GitHub repository, a package-registry entry, or a LinkedIn page.
- When grading is borderline, ask: would this entity realistically confuse the target customer or credibly contest the name? If not, grade it minor.

Do not search USPTO, WIPO, EUIPO, other trademark databases, corporate registries, or professional directories by default. Do not expand into close spelling or phonetic variants unless an obvious result makes one directly relevant. Never label a name “available,” “trademark-safe,” or “cleared.”

### Domain research

For each name, search the web for:

- The exact-name `.com`
- One preferred extension supplied by the user, when applicable
- At most one sensible modified `.com` if the exact `.com` appears used

Use search-engine results and visible website use only. Do not query registrars, WHOIS, registry services, aftermarket listings, DNS, or bulk domain tools by default.

Classify each domain as **in active use**, **no active use found**, or **uncertain**. `No active use found` does not mean the domain is unregistered or available to register. Do not recommend awkward domain hacks merely to manufacture an option.

### Obvious reputation checks

Record only risks surfaced by the same searches, such as obvious negative meanings, vulgar homophones, or strong political, extremist, medical, financial, or adult associations that would surprise the user. Do not run separate exhaustive linguistic or reputation research.

Exit criterion: every top-12 name has two name-search results, an exact-domain search, and explicit limitations; no default authoritative-database research was performed.

## Stage 8 — Final synthesis

The Orchestrator produces a decision-oriented report. Do not bury the result under the creative process: start with the shortlist.

Follow the [final report format](reference.md#final-report-format) exactly. Its non-negotiables:

- **Deliver as a canvas when the host supports one** (e.g. Cursor). Prefer a single `.canvas.tsx` decision page over a Markdown file or an in-chat table; fall back to Markdown (same sections, same order) only when no canvas surface is available. Either way it is one scrollable page — never hide content behind tabs.
- The report — canvas or Markdown — renders, in order: report header, decision callout, three decision cards, method statistics, top-12 vote chart, official shortlist table, **expandable per-name evidence and rationale for all top-12 names (what each name means, why it fits the brief, and its graded conflict evidence)**, the full top-30 table, naming brief and method, and the preliminary-research callout. The top-12 analysis and the top-30 list are both mandatory and both visible on the one page.
- The decision callout declares that no candidate is ready **only when every leading candidate has a blocking conflict**; candidates whose worst finding is a caution or minor signal are recommended with their graded risks.
- The official top 12 keep their frozen vote order; any recommended decision order after research is presented separately.
- All 30 ranked names visible without tabs; every factual conflict and domain-use claim linked to its source with the research date.
- The availability disclaimer (verbatim template in the report format) closes the report.

Exit criterion: the report follows the required section order, every claim is cited, and the disclaimer is present.

---

# Agent prompt templates

Role-specific system prompts for the Ideators, Curator, Ballot Manager voters, and Web Checker are in [reference.md](reference.md). Read it when instantiating agents at each stage.

---

# Quality controls

Before finalizing, verify:

- [ ] Exactly five values were used throughout
- [ ] Eight distinct personas were created
- [ ] Round 1 produced 10 associations × 5 values × 8 ideators
- [ ] First dedupe preserved provenance
- [ ] Round 2 produced 8 new associations × 5 values × 8 ideators
- [ ] Second dedupe removed near-duplicates and surfaced underused gems
- [ ] Name generation produced 20 names × 8 ideators before cleanup
- [ ] Each ideator submitted at least 4 invented or root-derived candidates
- [ ] Candidate names respect the four-syllable maximum
- [ ] No more than 2 ballot candidates share a leading morpheme or suffix pattern
- [ ] Direct famous-character and brand reuse was excluded from finalists
- [ ] Voting was blind and candidate order randomized
- [ ] Every ideator ranked exactly 12 names
- [ ] Borda scores and tie-breakers were calculated correctly
- [ ] Official top 12 were frozen before research
- [ ] Top 30 were retained
- [ ] The final report follows the required single-page presentation order
- [ ] All 30 ranked names are visible without opening a tab or requesting another artifact
- [ ] The top-12 vote chart or score-list fallback is labeled with metric, source, and research date
- [ ] Every top-12 factual conflict or domain-use claim is cited
- [ ] Checks stayed within the Stage-7 query budget
- [ ] Conflict severity was graded; minor signals were not treated as blockers
- [ ] The decision callout is consistent with the severity grades
- [ ] Domain results describe visible use, not registration availability
- [ ] The final answer clearly states that web search is a proxy, not legal or domain clearance

## Failure handling

- **Subagent unavailable:** emulate isolated passes sequentially and disclose the method accurately.
- **Malformed agent output:** repair once against the schema; rerun the stage if counts remain wrong.
- **Too many duplicates:** instruct the affected ideator to regenerate only rejected slots using underexplored territories.
- **Candidate pool too small after dedupe:** run a focused supplemental name-generation pass, then include the new names in the same blind ballot.
- **Web search unavailable:** mark the result `uncertain`, list what could not be checked, and do not infer clearance.
- **Domain-use results contradictory:** mark `uncertain`, cite both signals, and recommend manual confirmation for finalists.
- **Blocking conflict among top 12:** preserve its official vote rank, flag it prominently, and recommend the strongest viable alternative separately. Do not escalate caution or minor signals into blockers to simplify the recommendation.
- **Convergent candidate pool:** if the pre-ballot pool is dominated by descriptive compounds despite the Stage-5 rules, rerun name generation for the worst-offending ideators with explicit low-typicality instructions rather than voting on a weak pool.

## User-facing progress updates

Because this workflow is long, provide compact updates at major milestones rather than exposing raw chain-of-thought:

1. Inputs and personas finalized
2. Association rounds curated
3. Candidate pool ready and voting complete
4. Lightweight web and domain checks complete

Do not overwhelm the user with hundreds of raw associations unless they request the working set. The final report should be useful on its own, while structured artifacts preserve the detailed audit trail.
