---
name: startup-idea-hunter-skill
description: >-
  Hunt, structure, and score startup, micro-SaaS, and AI product ideas using the
  Easy-Vibe Stage 1 methodology. Activates when users ask to find startup ideas,
  discover user pain points, mine Reddit complaints, analyze Capterra 1-to-3 star
  reviews, research Indie Hackers or Product Hunt launches, inspect Upwork or Fiverr
  repetitive jobs, build a Clue Page, or evaluate product ideas on Frequency, Pain
  Level, Current Workaround, Willingness to Pay, and Market Size. Supports 4-channel
  search query generation, AI input-to-output workflow mapping, need-tier
  classification (pain vs gratification vs desire), horizontal user segmentation,
  vertical context timeline analysis, and MVP validation planning.
activation: /startup-idea-hunter-skill
license: MIT
metadata:
  author: aidino
  version: 1.0.0
  created: 2026-10-27
  last_reviewed: 2026-10-27
  review_interval_days: 90
provenance:
  maintainer: aidino
  version: 1.0.0
  created: 2026-10-27
  source_references:
    - https://raw.githubusercontent.com/datawhalechina/easy-vibe/main/docs/vi-vn/stage-1/appendix-idea-sources/index.md
    - https://raw.githubusercontent.com/datawhalechina/easy-vibe/main/docs/vi-vn/stage-1/finding-great-idea/index.md
---

# /startup-idea-hunter-skill

Turn vague domain curiosity or raw community complaints into an evidence-backed **Easy-Vibe Clue Page**, a **5-Criteria Startup Idea Scorecard**, and a **Reframed AI MVP Validation Plan**.

Instead of "holding an AI hammer looking for a nail," this skill enforces the two-stage Easy-Vibe discovery discipline:
1. **Clue Hunting (Stage 1A)**: Collect verbatim complaints, manual spreadsheet/copy-paste workflows, low-star software reviews, indie revenue proofs, and paid repetitive freelance jobs with source links and `Input -> AI Capability -> Output` mappings.
2. **Demand Scoring & Value Reframing (Stage 1B)**: Filter clues by behavioral evidence, classify need tiers (`pain` > `gratification` > `desire`), score across 5 criteria (`frequency`, `pain_level`, `current_workaround`, `willingness_to_pay`, `market_size`), narrow the target segment horizontally, map the vertical context timeline, and produce a 5-step validation plan.

## When to Use This Skill

Invoke `/startup-idea-hunter-skill` when you want to:
- Generate a 4-channel hunting query pack (Reddit/forums, Capterra/G2 low-star reviews, Indie Hackers/Product Hunt launches, Upwork/Fiverr repetitive jobs) for any niche.
- Transform raw search snippets or user complaints into a structured Clue Page with explicit AI input-to-output mappings.
- Score and rank candidate startup ideas using the Easy-Vibe 5-Criteria Scorecard and Need-Tier Classifier.
- Reframe a broad feature idea into a focused, high-willingness-to-pay AI micro-SaaS MVP concept.

**Language adaptability**:
- Always respond in the language used by the user (or the language configured in the host Coding Agent), while keeping JSON keys and verdict enums in canonical English.

**Anti-goals**:
- Do NOT activate on general coding, deployment, or model-training queries — wait for explicit `/startup-idea-hunter-skill` invocation or clear startup/product idea discovery requests.
- Never fabricate user quotes or URLs when live search is requested; every clue must preserve its verbatim wording and source link.
## Prerequisites

- **Runtime**: Python 3.9+ (uses standard library only; zero external pip packages required).
- **Permissions**: Read access to local clue JSON files and write access to local output directory.
- **Network**: Deterministic scoring and query generation run 100% offline. Live community clue harvesting uses the host coding agent's web search tool when requested.

Check environment readiness anytime:

```bash
python3 scripts/run_pipeline.py --check-prereqs
python3 scripts/run_pipeline.py --diagnostics
```

## Workflows

### Workflow 1: End-to-End Clue Hunting & Idea Scoring (Deterministic Happy Path)

Run `python3 scripts/run_pipeline.py` on a structured clue JSON file (containing a target `niche` and collected `clues`) to generate the 4-channel query pack, Clue Page, 5-Criteria Startup Idea Scorecard, and Reframed MVP Validation Plan in one command:

```bash
python3 scripts/run_pipeline.py \
  --input evals/golden/case-1/input.json \
  --output output/freelance-scorecard.json \
  --markdown output/freelance-scorecard.md
```

### Workflow 2: Starting Without Clues (Live 4-Channel Hunting via Agent Web Search)

When the user only names a domain or niche (for example, *"Hunt AI startup ideas in property management"* or *"Find micro-SaaS pain points in freelance workflows"*):

1. Run `python3 scripts/generate_queries.py` to generate the 4-channel search queries for the niche:
   ```bash
   python3 scripts/generate_queries.py --niche "freelance workflows" --output /tmp/queries.json
   ```
2. Execute the generated queries using the agent's web search tool across:
   - **Step 1 (Reddit/Forums)**: Manual copy-paste, spreadsheet friction, tedious workflows.
   - **Step 2 (Capterra/G2)**: 1-to-3 star reviews mentioning `"Cons"`, `"clunky"`, `"manual"`, `"import"`, `"formatting"`.
   - **Step 3 (Indie Hackers/Product Hunt)**: Validated micro-SaaS revenue threads and launch comment gaps.
   - **Step 4 (Upwork/Fiverr)**: Repetitive data entry, transcription, extraction, and formatting jobs clients already pay humans to do.
3. Save the harvested verbatim clues (with exact `quote`, `persona_context`, `input_data`, `output_data`, `source_url`, `channel`, and 1–5 criteria ratings) into a JSON file matching the schema in `assets/config.json`.
4. Run `python3 scripts/run_pipeline.py` on that JSON file to score, rank, and reframe the clues into an inspectable JSON and Markdown report.

## Available Scripts

- **Run** `python3 scripts/run_pipeline.py --input <clues.json> --output <result.json> [--markdown <report.md>]` — single orchestrator that validates inputs, generates the 4-channel query pack, scores all clues using the Easy-Vibe 5-criteria model, classifies need tiers, checks output sanity bounds, and writes the complete JSON and Markdown deliverables.
- **Run** `python3 scripts/generate_queries.py --niche "<domain>" --output <queries.json>` — standalone generator for 4-channel community, review, indie-launch, and freelance-marketplace search queries.
- **Run** `python3 scripts/score_clues.py --input <clues.json> --output <scored.json>` — standalone evaluator that computes weighted Easy-Vibe scores, classifies `pain` vs `gratification` vs `desire`, maps AI architectures, and builds the MVP validation plan.
- **Run** `python3 scripts/run_evals.py --validate` — validates the bundled evaluation specification and golden cases.
- **Run** `python3 scripts/evolve.py --correct "<what the result got wrong>"` — records a domain correction into `EVOLUTION.md`, `## Gotchas`, and regression tests.

## Available Analyses

Read `references/analysis-methods.md` for the full mathematical formulas and rubrics behind each analysis:

1. **4-Channel Search Query Synthesis**: Builds targeted search dorks for Reddit/communities, Capterra low-star reviews, Indie Hackers/Product Hunt, and Upwork/Fiverr.
2. **Easy-Vibe Clue Page Structuring**: Preserves verbatim quotes, context, source links, and maps `Unstructured Input -> AI Capability -> Structured Output`.
3. **Need-Tier Classification**: Categorizes each clue into `pain` (fear/loss-driven, 1.15x multiplier), `gratification` (instant relief, 1.0x multiplier), or `desire` (ideal self/vitamin, 0.75x penalty multiplier).
4. **5-Criteria Weighted Startup Scorecard**: Scores `frequency` (20%), `pain_level` (25%), `current_workaround` (20%), `willingness_to_pay` (25%), and `market_size` (10%) on a 0–100 scale with actionable verdicts (`BUILD_MVP_NOW`, `NICHE_DOWN_FIRST`, `SKIP_VITAMIN`).
5. **Value Reframing & 5-Step Validation Plan**: Produces horizontal segmentation, vertical timeline friction points, and the 10-user interview + >10% pre-order validation checklist.

## Error Handling

All scripts emit structured JSON errors to `stderr` with `"error"`, `"error_type"` (`"validation"`, `"runtime"`, or `"network"`), `"details"`, and `"hint"`, then exit with code `1`. Read `references/troubleshooting.md` for recovery steps.

## Gotchas

- **Desire ("vitamin") ideas often score high on surface market size but fail willingness to pay**: running `scripts/score_clues.py` applies a `0.75` need-tier multiplier when `need_tier` is `"desire"` and caps the recommendation at `"NICHE_DOWN_FIRST"` or `"SKIP_VITAMIN"` even if raw criteria scores look high.
- **Direct HTTP fetches to `reddit.com` from headless scripts frequently return HTTP 403 network blocks**: When harvesting live Reddit clues, use the agent's web search tool or `https://arctic-shift.photon-reddit.com/api/posts/ids?ids=<post_id>` rather than scraping `www.reddit.com` directly.
- **Low-star software reviews (2–3 stars) carry higher product signal than 1-star billing rants or 5-star praise**: Filter Capterra/G2 queries for workflow friction terms (`"clunky"`, `"manual"`, `"import"`, `"formatting"`, `"too many clicks"`) rather than generic `"worst"` or `"scam"` keywords.

## Keywords for Automatic Detection

**Entities**: startup idea, micro-SaaS, AI product, Easy-Vibe, Clue Page, Reddit, Product Hunt, Indie Hackers, Capterra, Upwork, Fiverr, scope creep, manual workflow
**Metrics**: frequency, pain level, current workaround, willingness to pay, market size, need tier, pain vs desire, pre-order conversion rate
**Actions**: hunt clues, find startup ideas, mine reviews, score ideas, validate demand, reframe value, segment users

**Activation examples**:
- `/startup-idea-hunter-skill Hunt startup ideas in the freelance workflow niche`
- `/startup-idea-hunter-skill --input clues.json --output scorecard.json`
- "Use Easy-Vibe to hunt community pain points and score AI micro-SaaS startup ideas"
**Does NOT activate for**:
- "Write a Python web scraper to download images from Instagram"
- "Optimize my PostgreSQL database indexes"

## References

| File | When to read this |
|---|---|
| `references/easy-vibe-playbook.md` | Read when conducting live 4-channel community hunting or explaining the Easy-Vibe Stage 1 methodology |
| `references/analysis-methods.md` | Read when interpreting the 5-Criteria Scorecard math, Need-Tier multipliers, AI capability mapping, or Value Reframing rules |
| `references/troubleshooting.md` | Read when diagnosing input validation errors, empty clue sets, or Reddit/Capterra search blocks |
