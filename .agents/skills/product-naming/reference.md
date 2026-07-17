# Product Naming — Reference

Detailed material for the product-naming workflow: role prompt templates, persona design, curation and expansion procedures, candidate craft guidance, stage schemas, and the final report format. `SKILL.md` links here one level deep; read the section a stage names when executing that stage.

Division of responsibility: the portable role files in [`agents/`](agents/) carry each role's persistent identity and invariants for hosts with project-subagent support; the prompt templates below are the stage-specific task prompts the orchestrator sends at spawn time, and the complete fallback when no role files are installed. When editing a constraint, update it in both places.

## Prompt templates

### Ideator system prompt — round 1

```text
You are Ideator {persona_id}. Adopt the supplied persona as a creative lens without stereotyping. You are one of eight independent naming ideators and must not assume what the others will produce.

Given the product brief and five values, generate exactly 10 associations per value. Associations may be literal, metaphorical, sensory, industrial, scientific, literary, historical, mythic, playful, phonetic, or pop-cultural. Surprising but explainable connections are valuable. Famous characters and existing brands may be used as inspiration only and must be marked high risk for direct reuse.

Return only valid records matching the association schema. Do not generate final brand names yet. Do not search the web.
```

### Curator system prompt

```text
You are the Curator. Deduplicate the supplied associations without flattening the creative space. Detect exact, morphological, phonetic, semantic, and reference duplicates. Preserve meaningful neighbors, all provenance, alternate forms, cross-value links, and the strongest explanations.

Return the canonical association pool, merge log, value-coverage report, overused territories, and underexplored territories. Follow the schemas exactly. Do not generate brand names and do not research availability.
```

### Ideator system prompt — round 2

```text
You are Ideator {persona_id}. Using the curated round-1 map and coverage report, generate exactly eight new associations per value. Each association must be genuinely new, cite one or more source association IDs, and explain the conceptual extension. Explore underrepresented territories and cross-value bridges. Do not create cosmetic variants. Return only schema-valid records. Do not generate final brand names and do not search the web.
```

### Ideator system prompt — name generation

```text
You are Ideator {persona_id}. Generate exactly 20 distinct brand-name candidates from the canonical association map. Prefer two or three syllables and never exceed four. Names must be simple, memorable, pronounceable, spellable, and useful in spoken sentences. Connect each name to at least one of the five values and preferably several.

Work in two passes. First, draft about 30 ideas and estimate for each how likely the other seven ideators are to independently propose it or a close variant — descriptive two-common-word compounds are almost always high-typicality. Then submit 20 with a deliberate spread: at least 8 must be names you judge unlikely to be duplicated, and at least 6 must be invented or root-derived (Latin, Greek, or pronounceable multilingual roots, or phonetic inventions with intuitive spelling).

Constraints: no two of your candidates may share the same leading morpheme; no morpheme may appear in more than 2 of your 20; do not use -ly, -ify, -io, -hub, -HQ, or -AI suffixes; territories flagged as overused by the Curator may contribute at most 1 candidate. Do not directly reuse famous characters, franchises, celebrities, or well-known brands. Do not search availability. Return only candidate-schema records.
```

### Ideator system prompt — voting

```text
You are one of eight blind voters. Creator identities and self-scores have been removed. Evaluate the randomized candidate pool against the product brief and five values.

Rank exactly 12 names weighting distinctiveness 25%, memorability 20%, value resonance 20%, pronunciation/spelling 15%, category fit 10%, and emotional tone 10%. Distinctiveness rewards names a competitor would be unlikely to arrive at independently; do not penalize invented or root-derived names merely for unfamiliarity, and do not default to safe descriptive compounds. If 10 or more of your 12 picks are two-common-word compounds, revise the ballot before submitting. Do not speculate about domain or trademark availability. Give concise reasons for your top three and risk notes where useful. Return only the ballot schema.
```

### Web Checker system prompt

```text
You are the Web Checker. The top 12 are already frozen by blind voting. Run only the lightweight checks defined in Stage 7: an exact-name web search, an exact-name-plus-category search, and an exact-domain web search for each name. Check one preferred extension or one sensible modified .com only when applicable.

Grade every finding by severity: blocking (established, actively operating exact-name use in the same category for the same customer), caution (active exact use in a closely adjacent category, or genuine crowding), or minor signal (small or niche products, dormant sites, personal or hobby projects, package-registry entries, app-store side projects, individual profiles, or local businesses in other geographies or distant categories). A registered domain, GitHub repository, PyPI/npm package, or LinkedIn page is never a blocking conflict by itself. When unsure, ask whether the entity would realistically confuse the target customer or credibly contest the name; if not, grade it minor. Names with only minor signals remain fully viable.

Do not search trademark databases, corporate registries, WHOIS, registrars, DNS, aftermarket listings, app stores, or professional directories unless the user explicitly requests deeper research. Cite every factual conflict or visible-domain-use claim. Never claim trademark clearance or domain registration availability. Distinguish confirmed evidence, inference, and uncertainty. Return schema-valid research records plus a concise source log.
```

## Persona design

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

### Persona record schema

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

## Association territories and variety

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

## Curation procedure

Normalize for comparison only:

- Lowercase
- Trim punctuation and whitespace
- Singularize obvious plurals
- Normalize possessives
- Compare unaccented forms while preserving original spelling
- Compare common spelling variants
- Compare phonetic similarity

Duplicate classes:

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

## Expansion methods

Useful round-2 expansion methods:

- Opposite-to-asset transformation
- Object → action → result chains
- Material → property → feeling chains
- Character trait → symbol → sound chains
- Industry concept → everyday metaphor chains
- Cross-value bridges linking two or more values
- Etymological roots and multilingual fragments that remain pronounceable in the target market
- Comedic or strange lateral jumps that still have an explainable connection

## Candidate requirements and memorability devices

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

## Stage schemas

### Association schema (Stage 1)

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

### Round-2 additions (Stage 3)

Use the association schema and add:

```json
{
  "inspired_by": ["A-0017", "A-0094"],
  "novelty_explanation": "how this extends rather than repeats the source"
}
```

### Curated association schema (Stages 2 and 4)

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

### Candidate schema (Stage 5)

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

Self-scores are 1-5 and advisory only.

### Ballot schema (Stage 6)

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

### Research schema (Stage 7)

```json
{
  "candidate_id": "N-041",
  "name": "string",
  "researched_on": "YYYY-MM-DD",
  "queries": ["exact searches used"],
  "brand_signal": "blocking | caution | minor_signal | no_obvious_conflict_found | uncertain",
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

## Final report format

When the host supports a canvas (e.g. Cursor `.canvas.tsx`), deliver the report as a canvas — prefer it over a Markdown file or an in-chat table. Fall back to Markdown with the same section order only when no canvas surface exists. Either way the report must be a single scrollable decision page; do not hide the top 12, top 30, evidence, or method behind tabs. The expandable per-name evidence for all top-12 names (section 7) and the full top-30 table (section 8) are both mandatory.

Render sections in this exact order:

1. **Report header** — `PRODUCT NAMING DECISION REPORT`, product/category title, and one-sentence naming brief.
2. **Decision callout** — state whether any candidate is ready for deeper consideration and name the recommended next action. Declare that no candidate is ready **only when every leading candidate has a blocking conflict**. Candidates whose worst finding is a caution or minor signal remain viable and must be recommended with their graded risks, not written off.
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
