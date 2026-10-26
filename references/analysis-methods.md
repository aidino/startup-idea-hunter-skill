# Analysis Methods: 5-Criteria Scoring, Need-Tier Math, and AI Mapping

This document specifies the exact mathematical formulas, scoring rubrics, classification rules, and validation thresholds implemented in `scripts/score_clues.py` and `scripts/run_pipeline.py`.

---

## 1. The 5-Criteria Easy-Vibe Scorecard

Every clue is rated on a continuous or integer scale from `1.0` to `5.0` across five orthogonal dimensions:

| Criterion Key | Weight | 1 (Weak) | 3 (Moderate) | 5 (Strong) |
|---|---:|---|---|---|
| `frequency` | **20%** (`0.20`) | Yearly or one-time event | Monthly workflow | Daily or multiple times per week |
| `pain_level` | **25%** (`0.25`) | Minor annoyance, easily ignored | Wastes 1–2 hours or causes frustration | Direct revenue loss ($1,000+), severe anxiety, or compliance penalty |
| `current_workaround` | **20%** (`0.20`) | Users do nothing and don't care | Users cobble together manual spreadsheets/copy-paste | Users pay freelancers, buy clunky tools, or spend hours every week |
| `willingness_to_pay` | **25%** (`0.25`) | Expects 100% free tool; no budget | Would pay $5–$15/mo if frictionless | Already paying for inferior software/services or saves >$500/mo in billable time |
| `market_size` | **10%** (`0.10`) | Tiny hyper-local niche (<1,000 users) | Specialized professional niche (10k–100k users) | Large global professional or consumer segment (>500k users) |

### Raw Score Formula (0–100 Scale)

Let $s_i \in [1, 5]$ be the score for criterion $i$ and $w_i$ be its weight ($\sum w_i = 1.00$):

$$\text{WeightedSum}_5 = 0.20 \cdot s_{\text{freq}} + 0.25 \cdot s_{\text{pain}} + 0.20 \cdot s_{\text{workaround}} + 0.25 \cdot s_{\text{wtp}} + 0.10 \cdot s_{\text{market}}$$

$$\text{RawScore}_{100} = \text{round}(\text{WeightedSum}_5 \times 20.0, 2)$$

---

## 2. Need-Tier Multiplier (`pain` vs `gratification` vs `desire`)

To enforce the Easy-Vibe rule that **fear/pain drives payment while desire leads to procrastination**, the raw score is adjusted by a Need-Tier Multiplier $M_{\text{tier}}$:

- **`pain`** ($M = 1.15$): Fear, direct financial loss, or severe operational bottleneck.
- **`gratification`** ($M = 1.00$): Instant convenience or speed reward.
- **`desire`** ($M = 0.75$): Ideal self-image ("vitamin").

$$\text{AdjustedScore}_{100} = \min\left(100.0, \text{round}(\text{RawScore}_{100} \times M_{\text{tier}}, 2)\right)$$

### Verdict Decision Rules

1. **`BUILD_MVP_NOW`**:
   - $\text{AdjustedScore}_{100} \ge 76.0$
   - $s_{\text{pain}} \ge 4.0$
   - $s_{\text{wtp}} \ge 4.0$
   - `need_tier` $\neq$ `"desire"`
2. **`SKIP_VITAMIN`**:
   - `need_tier` == `"desire"` OR $\text{AdjustedScore}_{100} < 50.0$
3. **`NICHE_DOWN_FIRST`**:
   - All intermediate candidates ($50.0 \le \text{AdjustedScore}_{100} < 76.0$, or high score with $s_{\text{pain}} < 4.0$ or $s_{\text{wtp}} < 4.0$). Must undergo horizontal segmentation and context reframing before building.

### Numerical Example

Suppose Clue `c1` (*Scope Creep Guard for Freelancers*) has:
- `frequency` = 4.0, `pain_level` = 5.0, `current_workaround` = 4.0, `willingness_to_pay` = 5.0, `market_size` = 4.0
- `need_tier` = `"pain"` ($M = 1.15$)

Calculation:
- $\text{WeightedSum}_5 = 0.20(4) + 0.25(5) + 0.20(4) + 0.25(5) + 0.10(4) = 0.80 + 1.25 + 0.80 + 1.25 + 0.40 = 4.50$
- $\text{RawScore}_{100} = 4.50 \times 20 = 90.00$
- $\text{AdjustedScore}_{100} = \min(100.0, 90.00 \times 1.15) = 100.00$
- Verdict: `BUILD_MVP_NOW`

Suppose Clue `c5` (*Aesthetic Freelance Desk Mood Tracker*) has:
- `frequency` = 5.0, `pain_level` = 2.0, `current_workaround` = 2.0, `willingness_to_pay` = 1.5, `market_size` = 5.0
- `need_tier` = `"desire"` ($M = 0.75$)
- $\text{WeightedSum}_5 = 0.20(5) + 0.25(2) + 0.20(2) + 0.25(1.5) + 0.10(5) = 1.00 + 0.50 + 0.40 + 0.375 + 0.50 = 2.775$
- $\text{RawScore}_{100} = 55.50$
- $\text{AdjustedScore}_{100} = 55.50 \times 0.75 = 41.62$
- Verdict: `SKIP_VITAMIN`

---

## 3. AI Capability Mapping Rules

When `ai_capability` is not explicitly provided on a clue, `infer_ai_capability()` inspects `input_data` and `output_data`:

1. **Visual / Document Inputs** (`pdf`, `scan`, `image`, `photo`, `screenshot`, `handwritten`, `receipt`):
   - Maps to: `VLM / OCR Document Parser + Deterministic Balance Validator`
2. **Audio / Speech Inputs** (`audio`, `voice`, `recording`, `meeting`, `call`, `transcript`, `podcast`):
   - Maps to: `ASR (Whisper) + LLM Structured Action Extractor + Webhook Sync`
3. **Contract / Policy / Scope Comparison** (`contract`, `scope`, `policy`, `quote`, `diff`, `clause`, `revision`):
   - Maps to: `Semantic Scope/Contract Diff Engine + Contextual Response Drafter`
4. **General Multi-Source Text / Logs**:
   - Maps to: `Multi-Source Context Aggregator + Strict Schema LLM Formatter`

---

## 4. The 5-Step Demand Validation Thresholds

Before writing production application code, validate the top-ranked concept against five empirical gates:
1. **10-User Behavioral Check**: At least 7 of 10 interviewed target users must already use an active workaround (spreadsheets, manual copy-paste, or paid help).
2. **10x Friction Reduction**: Deliver the target output artifact in under 60 seconds with zero template setup.
3. **Pre-Order / Deposit Gate**:
   - **>10% conversion**: Strong paid demand — build MVP immediately.
   - **5%–10% conversion**: Moderate demand — narrow the horizontal persona or sharpen positioning.
   - **<5% conversion**: Weak demand — invalidate hypothesis and test the next clue.
4. **Bottom-Up Market Calculation**: $\text{TAM}_{\text{initial}} = \text{Reachable Niche Users} \times \text{Paid Conversion \%} \times \text{Annual ARPU}$.
5. **Defensibility (Moat) Check**: Identify proprietary workflow integrations, vertical edge-case datasets, or correction loops that prevent generic chat wrappers from substituting the tool.
