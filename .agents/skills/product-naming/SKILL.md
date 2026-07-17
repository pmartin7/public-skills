---
name: product-naming
description: Generate, refine, rank, and lightly research memorable product or company names from a short product description and five desired customer feelings. Use when the user invokes /product-naming or asks for a rigorous multi-agent naming process with lightweight web and domain checks.
---

# Product Naming

A multi-agent naming workflow that moves from emotional associations to a voted shortlist, then performs lightweight point-in-time web and domain checks.

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

## Roles

The orchestrator creates the following agents or emulates them as isolated passes when true subagents are unavailable:

- **8 Ideators** — each receives a distinct socio-economic and decision-making persona
- **1 Curator** — deduplicates and organizes association pools after rounds 1 and 2
- **1 Ballot Manager** — anonymizes, randomizes, tallies, and resolves ties
- **1 Web Checker** — runs lightweight web searches for obvious name conflicts and domain use
- **1 Orchestrator** — validates inputs, manages state, enforces schemas, and writes the final report

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
5. Creates eight non-overlapping personas.

### Persona design

Personas should create genuinely different semantic instincts. Vary at least four of these dimensions:

- Budget sensitivity
- Individual versus institutional buyer
- Technical expertise
- Status orientation
- Risk tolerance
- Time pressure
- Urban, suburban, rural, or distributed work context
- Frontline, operator, manager, executive, creator, or specialist role
- Preference for plain language versus symbolic language
- Familiarity with literature, science, sports, games, internet culture, craft, or industry jargon

Default persona examples, to be adapted rather than copied mechanically:

1. A budget-conscious early-career customer who values clarity and usefulness
2. An independent small-business operator focused on trust and immediate payoff
3. A skeptical enterprise buyer concerned with risk, credibility, and longevity
4. A technically sophisticated builder attracted to precision and elegant systems
5. A culture-forward creative who notices rhythm, imagery, and distinctiveness
6. A practical household or community decision-maker who values warmth and ease
7. A frontline practitioner or craftsperson who prefers concrete, tactile language
8. A prestige-aware leader who wants confidence, aspiration, and category authority

### Persona record

```json
{
  "persona_id": "P1",
  "label": "short neutral label",
  "context": "2-4 sentences",
  "naming_lens": ["3-5 distinctive lenses"],
  "reference_territories": ["literature", "industrial design", "sports", "etc."],
  "avoidances": ["stereotypes or overlaps with other personas"]
}
```

Exit criterion: eight personas are meaningfully distinct and all required input fields are canonicalized.

## Stage 1 — Independent association generation

Run eight ideators independently. They must not see one another's output.

Each ideator generates **10 associations for each of the five values**, for **50 associations per ideator** and **400 raw associations total**.

Associations may be:

- Direct synonyms or antonyms used constructively
- Concrete objects, materials, tools, places, animals, or natural phenomena
- Verbs and sensory words
- Industry concepts or jargon
- Scientific, mathematical, architectural, or engineering references
- Mythological or public-domain figures
- Literary or historical references
- Famous characters or popular-culture references used only as inspiration
- Humor, wordplay, idioms, or unexpected social associations
- Sounds, phonemes, roots, prefixes, or suffixes

Each set of 10 for a value should contain variety. Aim for at least:

- 2 direct or literal associations
- 2 metaphorical or sensory associations
- 2 cultural, literary, historical, or mythic associations
- 2 industry, scientific, or craft associations
- 2 playful, phonetic, or surprising associations

Do not force weak items merely to satisfy a category; quality and diversity come first.

### Association schema

```json
{
  "association_id": "P1-R1-V3-07",
  "persona_id": "P1",
  "round": 1,
  "value_id": "V3",
  "term": "string",
  "association_type": "literal | metaphor | cultural | literary | historical | mythic | industry | scientific | sensory | playful | phonetic | other",
  "connection": "one concise sentence explaining the link",
  "energy": "serious | warm | bold | playful | strange | premium | technical | other",
  "direct_reuse_risk": "low | medium | high",
  "notes": "optional"
}
```

Mark existing character names, franchise names, celebrity names, and well-known brands as `direct_reuse_risk: high` even when they are useful creative seeds.

Exit criterion: each ideator has exactly 10 valid associations per value.

## Stage 2 — First curation and deduplication

The Curator receives all 400 raw associations.

Deduplicate both **within each ideator** and **across all ideators** while preserving provenance.

### Normalization

Normalize for comparison only:

- Lowercase
- Trim punctuation and whitespace
- Singularize obvious plurals
- Normalize possessives
- Compare unaccented forms while preserving original spelling
- Compare common spelling variants
- Compare phonetic similarity

### Duplicate classes

1. **Exact duplicate** — same normalized term
2. **Morphological duplicate** — e.g. `forge`, `forged`, `forging`
3. **Near-phonetic duplicate** — names or terms that sound materially the same
4. **Semantic duplicate** — effectively identical meaning with no useful distinction
5. **Reference duplicate** — multiple labels for the same character, object, or concept

Do not collapse useful semantic neighbors such as `harbor`, `anchor`, and `lighthouse`. The goal is to remove redundancy, not richness.

For every merged cluster:

- Select the clearest canonical term
- Preserve alternate forms
- Preserve all contributing persona IDs and value IDs
- Combine the best non-redundant explanations
- Keep high-risk inspiration markers

### Curated association schema

```json
{
  "canonical_id": "A-0017",
  "term": "string",
  "alternate_forms": ["string"],
  "value_ids": ["V1", "V4"],
  "persona_ids": ["P2", "P6"],
  "association_types": ["metaphor", "industry"],
  "connections": ["concise distinct explanations"],
  "direct_reuse_risk": "low | medium | high",
  "novelty_signal": "common | distinctive | unusual",
  "curator_note": "why merged or preserved"
}
```

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

Useful expansion methods:

- Opposite-to-asset transformation
- Object → action → result chains
- Material → property → feeling chains
- Character trait → symbol → sound chains
- Industry concept → everyday metaphor chains
- Cross-value bridges linking two or more values
- Etymological roots and multilingual fragments that remain pronounceable in the target market
- Comedic or strange lateral jumps that still have an explainable connection

### Round-2 schema

Use the Stage-1 association schema and add:

```json
{
  "inspired_by": ["A-0017", "A-0094"],
  "novelty_explanation": "how this extends rather than repeats the source"
}
```

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

Each ideator generates **20 brand-name candidates**, for **160 raw names total**.

### Candidate requirements

A candidate should:

- Be simple and memorable
- Prefer two or three syllables
- Never exceed four syllables unless the user explicitly allows it
- Be pronounceable on first sight for the primary target market
- Be easy to say aloud and reasonably easy to spell after hearing it
- Work in a sentence such as “We use ___” or “Open ___”
- Connect to at least one core value; stronger candidates connect to two or more
- Avoid direct copies of famous characters, franchises, existing brands, or obvious category leaders
- Avoid gratuitous misspellings, hard-to-type punctuation, and unexplained numbers
- Avoid names whose only merit is an available-looking domain

Memorability devices may include:

- Alliteration
- Assonance or consonance
- Internal rhyme
- Strong stress pattern
- Compact compounds
- Familiar roots in a new combination
- Evocative concrete words
- Light semantic tension or surprise
- Short invented words with intuitive phonetics

### Portfolio diversity per ideator

Across 20 candidates, target roughly:

- 4 recognizable standalone words used in a distinctive way
- 5 compounds or clipped compounds
- 4 blends or portmanteaus
- 4 invented or root-derived names
- 3 mythic, literary, scientific, craft, or cultural transformations that do not directly reuse protected names

Do not force a weak category to hit the quota.

### Candidate schema

```json
{
  "candidate_id": "P3-N-014",
  "creator_persona_id": "P3",
  "name": "string",
  "pronunciation": "simple phonetic guide",
  "syllables": 2,
  "construction_type": "word | compound | blend | invented | transformed_reference | other",
  "source_association_ids": ["A-0017", "A-0132"],
  "linked_value_ids": ["V1", "V2", "V5"],
  "rationale": "1-3 concise sentences",
  "memory_device": "alliteration | rhythm | imagery | contrast | familiarity | other",
  "tone": ["warm", "precise"],
  "possible_risks": ["category generic", "spelling ambiguity", "reference risk"],
  "self_score": {
    "memorability": 1,
    "pronounceability": 1,
    "value_resonance": 1,
    "distinctiveness": 1,
    "category_fit": 1
  }
}
```

Scores are 1-5 and are advisory only. Ideators should not run web or domain checks yet; early searching causes convergence toward mediocre domain-driven names.

### Pre-ballot cleanup

The Curator deduplicates the 160 names before voting:

- Exact spelling duplicates
- Case and punctuation variants
- Singular/plural variants
- Near-identical compounds
- Confusingly similar pronunciation
- Same invented stem with trivial suffix changes

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

- Memorability — 25%
- Pronounceability and spelling — 15%
- Resonance with the five values — 20%
- Distinctiveness — 20%
- Product/category fit without being overly narrow — 10%
- Emotional and tonal fit — 10%

Availability is not scored because it has not yet been researched.

### Ballot schema

```json
{
  "voter_persona_id": "P5",
  "ranked_candidate_ids": ["N-041", "N-118", "N-007", "... exactly 12"],
  "top_three_reasons": {
    "N-041": "string",
    "N-118": "string",
    "N-007": "string"
  },
  "risk_notes": {
    "N-118": "optional concise concern"
  }
}
```

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

Run lightweight checks on the top 12 only. The purpose is to catch obvious conflicts and signs of domain use without turning naming into a trademark or domain-clearance project.

### Research date and scope

Every result must record:

- Research date
- Exact web queries used
- Domain names searched
- Sources supporting any identified conflict

Search results change quickly. Phrase findings as point-in-time proxies.

### Brand-conflict research

For each top-12 name, run at most these searches:

1. Exact quoted name
2. Exact name plus industry/category keywords

Classify:

- **No obvious conflict found** — the limited searches found no meaningful exact use in the target category
- **Crowded** — multiple unrelated uses make the name difficult to own or discover
- **Potential conflict** — a meaningful exact use exists in the same or adjacent category
- **Uncertain** — results are incomplete, ambiguous, or unavailable

Do not search USPTO, WIPO, EUIPO, other trademark databases, corporate registries, or professional directories by default. Do not expand into close spelling or phonetic variants unless an obvious result makes one directly relevant. Never label a name “available,” “trademark-safe,” or “cleared.”

### Domain research

For each name, search the web for:

- The exact-name `.com`
- One preferred extension supplied by the user, when applicable
- At most one sensible modified `.com` if the exact `.com` appears used

Use search-engine results and visible website use only. Do not query registrars, WHOIS, registry services, aftermarket listings, DNS, or bulk domain tools by default.

Classify each domain:

- **In active use**
- **No active use found**
- **Uncertain**

`No active use found` does not mean the domain is unregistered or available to register. Do not recommend awkward domain hacks merely to manufacture an option.

### Obvious reputation checks

Record only risks surfaced by the same searches, such as:

- Obvious negative meanings or vulgar homophones
- Strong political, extremist, medical, financial, or adult associations that would surprise the user

Do not run separate exhaustive linguistic or reputation research.

### Research schema

```json
{
  "candidate_id": "N-041",
  "name": "string",
  "researched_on": "YYYY-MM-DD",
  "queries": ["exact searches used"],
  "brand_signal": "no_obvious_conflict_found | crowded | potential_conflict | uncertain",
  "conflicts": [
    {
      "entity": "string",
      "category": "string",
      "why_relevant": "string",
      "source": "URL"
    }
  ],
  "domains": [
    {
      "domain": "example.com",
      "status": "active_use | no_active_use_found | uncertain",
      "source": "URL or search query"
    }
  ],
  "best_domain_lead": "string or null",
  "obvious_reputation_risks": ["string"],
  "notes": "limitations and follow-up needed"
}
```

Exit criterion: every top-12 name has two name-search results, an exact-domain search, and explicit limitations; no default authoritative-database research was performed.

## Stage 8 — Final synthesis

The Orchestrator produces a decision-oriented report.

Do not bury the result under the creative process. Start with the shortlist.

### Presentation format

When the environment supports a standalone rich report or canvas, create one. Otherwise use the same section order in Markdown. The report must be a single scrollable decision page; do not hide the top 12, top 30, evidence, or method behind tabs.

Render sections in this exact order:

1. **Report header** — `PRODUCT NAMING DECISION REPORT`, product/category title, and one-sentence naming brief.
2. **Decision callout** — state whether any candidate is ready for deeper consideration and name the recommended next action.
3. **Three decision cards** — quality leader, premium/serious option, and warm/playful option. Each card states the name, vote evidence, and material caveat.
4. **Method statistics** — four prominent counts: personas, raw associations, raw names, and final blind-ballot pool.
5. **Top-12 vote chart** — horizontal bars in frozen vote order, labeled with Borda points; include axis meaning, source, and research date. If charts are unavailable, use a compact ranked score list.
6. **Official shortlist table** — compact columns for rank, name with pronunciation and syllables, points/voters, conflict signal, exact `.com` use, best domain lead, and key risk.
7. **Expandable evidence and rationale** — one disclosure per top-12 name containing rationale, linked values, key risk, and citations. In Markdown, use `<details>` blocks when supported or level-three headings otherwise.
8. **Top-30 table** — show all ranks 1-30 directly on the page with name, points, voters, conflict screen, and one-line value link. Never make the user select a tab to discover ranks 13-30.
9. **Naming brief and method** — place side by side when layout permits; otherwise render consecutively.
10. **Preliminary-research callout** — end with the required availability disclaimer.

Use flat, restrained styling with one visually dominant decision. Avoid decorative gradients, shadows, emojis, and a wall of identical cards. Every factual conflict and domain-use claim must link to its source.

### Required final structure

#### 1. Naming brief

A compact recap of:

- Product and customer
- Five values
- Tone and constraints
- Material assumptions

#### 2. Top 12 checked shortlist

Use a table with these columns:

| Rank | Name | Pronunciation | Syllables | Why it works | Values | Vote points / voters | Web conflict signal | Exact .com use | Best domain lead | Key risk |
|---|---|---:|---:|---|---|---:|---|---|---|---|

Keep each rationale concise but specific.

After the table, identify:

- **Best overall naming candidate** based on name quality and lightweight checks, clearly distinguishing this judgment from vote rank
- **Best domain lead**
- **Best premium/serious option**
- **Best warm/playful option** when relevant
- Any top-voted name that should probably be rejected because of a potential conflict

Do not silently reorder the official top 12. You may provide a separate recommended decision order after research.

#### 3. Top 30 by vote

List ranks 1-30 with:

- Name
- Vote points
- Unique voters
- One-line rationale or value link
- Obvious conflict flag when discovered

#### 4. Method summary

Report counts:

- 8 personas
- 400 round-1 associations before deduplication
- 320 round-2 associations before deduplication
- 160 raw name candidates before deduplication
- Final candidate-pool size
- 8 ballots of 12 ranked names

Mention any deviations from the specified counts and why.

#### 5. Availability disclaimer

Use language equivalent to:

> These web and domain-use checks are preliminary point-in-time proxies, not trademark or registration clearance. A qualified trademark attorney and a registrar should verify finalists before launch or material investment.

Also state that web searches are only proxies: `no obvious conflict found` is not proof of trademark clearance, and `no active use found` is not proof that a domain can be registered.

### Citation requirements

When web research is performed:

- Cite every factual conflict or domain-use claim
- Use ordinary web search results and directly discovered company or product sites
- Separate inference from confirmed facts
- Include the research date

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
- [ ] Candidate names respect the four-syllable maximum
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
- [ ] Domain results describe visible use, not registration availability
- [ ] The final answer clearly states that web search is a proxy, not legal or domain clearance

## Failure handling

- **Subagent unavailable:** emulate isolated passes sequentially and disclose the method accurately.
- **Malformed agent output:** repair once against the schema; rerun the stage if counts remain wrong.
- **Too many duplicates:** instruct the affected ideator to regenerate only rejected slots using underexplored territories.
- **Candidate pool too small after dedupe:** run a focused supplemental name-generation pass, then include the new names in the same blind ballot.
- **Web search unavailable:** mark the result `uncertain`, list what could not be checked, and do not infer clearance.
- **Domain-use results contradictory:** mark `uncertain`, cite both signals, and recommend manual confirmation for finalists.
- **Potential conflict among top 12:** preserve its official vote rank, flag it prominently, and recommend the strongest viable alternative separately.

## User-facing progress updates

Because this workflow is long, provide compact updates at major milestones rather than exposing raw chain-of-thought:

1. Inputs and personas finalized
2. Association rounds curated
3. Candidate pool ready and voting complete
4. Lightweight web and domain checks complete

Do not overwhelm the user with hundreds of raw associations unless they request the working set. The final report should be useful on its own, while structured artifacts preserve the detailed audit trail.
