# startup-idea-hunter-skill

> Hunt, structure, and score startup, micro-SaaS, and AI product ideas using the Easy-Vibe Stage 1 methodology.

## Purpose

`startup-idea-hunter-skill` turns raw domain curiosity or community complaints into an evidence-backed **Easy-Vibe Clue Page**, a **5-Criteria Startup Idea Scorecard**, and a **Reframed AI MVP Validation Plan**. It prevents engineers from building unvalidated AI wrappers by enforcing source-linked clue harvesting across Reddit, Capterra, Indie Hackers/Product Hunt, and Upwork/Fiverr before scoring and reframing ideas.

## Activation

This skill activates when users ask about finding startup ideas, hunting user pain points, mining low-star software reviews, structuring an Easy-Vibe Clue Page, or scoring AI micro-SaaS concepts. Invoke with `/startup-idea-hunter-skill` on platforms that support slash commands, or ask naturally.

**Example queries:**
- `/startup-idea-hunter-skill --input evals/golden/case-1/input.json --output output/freelance-scorecard.json`
- `/startup-idea-hunter-skill Hunt startup ideas in the freelance workflow niche for an AI Engineer`
- "Theo hướng dẫn Easy-Vibe, hãy giúp tôi truy lùng manh mối từ cộng đồng và chấm điểm ý tưởng AI startup"

## Usage

Run the deterministic pipeline on a JSON clue file:

```bash
python3 scripts/run_pipeline.py \
  --input evals/golden/case-1/input.json \
  --output output/scorecard.json \
  --markdown output/scorecard.md
```

Or generate a 4-channel hunting query pack for any niche:

```bash
python3 scripts/generate_queries.py --niche "property management" --output /tmp/queries.json
```

## Gotchas

- **Desire ("vitamin") ideas often score high on surface market size but fail willingness to pay**: running `scripts/score_clues.py` applies a `0.75` need-tier multiplier when `need_tier` is `"desire"` and caps the recommendation at `"NICHE_DOWN_FIRST"` or `"SKIP_VITAMIN"` even if raw criteria scores look high.
- **Direct HTTP fetches to `reddit.com` from headless scripts frequently return HTTP 403 network blocks**: When harvesting live Reddit clues, use the agent's web search tool or `https://arctic-shift.photon-reddit.com/api/posts/ids?ids=<post_id>` rather than scraping `www.reddit.com` directly.
- **Low-star software reviews (2–3 stars) carry higher product signal than 1-star billing rants or 5-star praise**: Filter Capterra/G2 queries for workflow friction terms (`"clunky"`, `"manual"`, `"import"`, `"formatting"`, `"too many clicks"`) rather than generic `"worst"` or `"scam"` keywords.

## Implementation

Full skill definition, scripts, and references are in the `SKILL.md` file and accompanying directories. Read `SKILL.md` for complete instructions.

## Files

- `SKILL.md` — Full skill definition (agentskills.io format), including the `## Gotchas` section
- `scripts/` — Executable code (`run_pipeline.py` orchestrator, `generate_queries.py`, `score_clues.py`, `run_evals.py` eval runner, `evolve.py` maintenance runner)
- `references/` — Detailed documentation (`easy-vibe-playbook.md`, `analysis-methods.md`, `troubleshooting.md`)
- `assets/` — Configuration and scoring weights (`config.json`)
- `evals/` — Bundled eval spec: binary checks + golden cases; `evals/caliper/` holds the agent-run (Caliper) spec
- `install.sh` / `install.ps1` — Cross-platform installers
