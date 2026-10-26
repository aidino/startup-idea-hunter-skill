# startup-idea-hunter-skill

Hunt, structure, and score startup, micro-SaaS, and AI product ideas using the **Easy-Vibe Stage 1** methodology (`appendix-idea-sources` + `finding-great-idea`).

Instead of guessing product features or building generic AI wrappers, this skill guides coding agents through:
1. **4-Channel Community & Market Clue Hunting**: Targeted search query packs across Reddit/forums, Capterra/G2 1-to-3 star reviews, Indie Hackers/Product Hunt launches, and Upwork/Fiverr repetitive jobs.
2. **Easy-Vibe Clue Page Structuring**: Preserves verbatim complaints, persona context, source links, and maps `Unstructured Input -> AI Capability -> Structured Output`.
3. **5-Criteria Startup Idea Scorecard & Need-Tier Classifier**: Evaluates `frequency` (20%), `pain_level` (25%), `current_workaround` (20%), `willingness_to_pay` (25%), and `market_size` (10%) with need-tier multipliers (`pain` 1.15x, `gratification` 1.0x, `desire` 0.75x).
4. **Value Reframing & 5-Step Validation Plan**: Narrows broad ideas horizontally, maps the vertical context timeline, and outputs a concrete 10-user + >10% pre-order validation plan.

## Installation

### Universal Path (works with 6+ tools)

```bash
git clone https://github.com/aidino/startup-idea-hunter-skill.git ~/.agents/skills/startup-idea-hunter-skill
```

Works with Codex CLI, Gemini CLI, Kiro, OpenCode, Goose, Antigravity, and other tools that read `~/.agents/skills/`.

### Claude Code (plugin — recommended)

```
/plugin marketplace add aidino/startup-idea-hunter-skill
/plugin install startup-idea-hunter-skill@startup-idea-hunter-skill
```

### Using install.sh (Recommended for all 17 platforms)

```bash
chmod +x install.sh
./install.sh                          # Auto-detect platform
./install.sh --platform claude-code   # Claude Code
./install.sh --platform cursor        # Cursor (auto-generates .mdc)
./install.sh --all                    # All detected platforms
./install.sh --dry-run                # Preview without installing
```

### Alternative: npx

```bash
npx skills add https://github.com/aidino/startup-idea-hunter-skill
```

### Manual Installation

| Platform | Copy to |
|---|---|
| Universal | `~/.agents/skills/startup-idea-hunter-skill/` |
| Claude Code | `~/.claude/skills/startup-idea-hunter-skill/` |
| GitHub Copilot | `.github/skills/startup-idea-hunter-skill/` |
| Cursor | `.cursor/rules/startup-idea-hunter-skill/` |
| Windsurf | `.windsurf/rules/startup-idea-hunter-skill/` |
| Cline | `.clinerules/startup-idea-hunter-skill/` |
| Codex CLI | `~/.agents/skills/startup-idea-hunter-skill/` |
| Gemini CLI | `~/.gemini/skills/startup-idea-hunter-skill/` |
| Kiro | `.kiro/skills/startup-idea-hunter-skill/` |
| Trae | `.trae/rules/startup-idea-hunter-skill/` |
| Goose | `~/.config/goose/skills/startup-idea-hunter-skill/` |
| OpenCode | `~/.config/opencode/skills/startup-idea-hunter-skill/` |
| Roo Code | `.roo/rules/startup-idea-hunter-skill/` |
| Antigravity | `~/.agents/skills/startup-idea-hunter-skill/` |

## Prerequisites

- Python 3.9+ (uses standard library only; no third-party pip packages required).

```bash
python3 scripts/run_pipeline.py --check-prereqs
```

## How to Use in Your Coding Agent

Once installed, you **do not need to run Python scripts manually**. Invoke the skill directly inside your Coding Agent chat (Claude Code, Cursor, Codex, GitHub Copilot, OpenCode, Gemini CLI, etc.) using `/startup-idea-hunter-skill` or natural language. The Coding Agent will automatically respond in the language you use.

### 1. Hunt Startup Ideas from Scratch in Any Niche
Prompt your Coding Agent:

```text
/startup-idea-hunter-skill Hunt AI micro-SaaS startup ideas in the freelance workflow niche using the 4-step Easy-Vibe methodology, with verbatim quotes and source links.
```

**What the Coding Agent does automatically:**
1. Generates a **4-channel search query pack** across Reddit/forums, Capterra/G2 1-to-3 star reviews, Indie Hackers/Product Hunt launches, and Upwork/Fiverr repetitive jobs.
2. Uses the agent's built-in web search to harvest verbatim user complaints, persona context, and source URLs.
3. Maps each clue through an AI Engineer lens: **Unstructured Input $\rightarrow$ AI Capability $\rightarrow$ Structured Output**.
4. Scores and ranks every candidate on the **5-Criteria Easy-Vibe Scorecard** (`Frequency`, `Pain Level`, `Current Workaround`, `Willingness to Pay`, `Market Size`), classifies the need tier (`pain` > `gratification` > `desire`), and outputs a **Clue Page + 5-Step MVP Validation Plan**.

---

### 2. Score & Filter Existing Clues or Notes You Collected
When you already have user complaints, forum links, or raw notes:

```text
/startup-idea-hunter-skill Score the raw complaints in clues.json using the Easy-Vibe 5-criteria scorecard. Tell me which one is a real painkiller worth building an MVP for and which ones are vitamin ideas to skip.
```

---

### 3. Reframe a Broad Idea into a High-Willingness-to-Pay Niche
When you have a broad product idea (e.g., *"an AI meeting notes app"* or *"a fitness tracker"*):

```text
/startup-idea-hunter-skill I want to build an AI meeting notes tool. Apply Easy-Vibe horizontal user segmentation and vertical context timeline analysis to reframe it into a narrow niche with strong willingness to pay.
```

---

### 4. Teach & Refine the Skill Over Time (`--correct`)
When you disagree with a ranking or want the skill to remember a domain rule on future runs, tell your agent:

```text
Record a correction for startup-idea-hunter-skill: "Prioritize B2B PDF/spreadsheet automation workflows over B2C habit trackers"
```
*(The agent runs `scripts/evolve.py --correct` under the hood to update `## Gotchas` and add a permanent regression check).*

---

## Under the Hood (Deterministic CLI for Agents & CI)

Behind the conversational interface, the Coding Agent invokes these deterministic scripts in `scripts/` so scoring and validation remain reproducible:

```bash
# Run the end-to-end scoring & MVP reframing pipeline:
python3 scripts/run_pipeline.py \
  --input evals/golden/case-1/input.json \
  --output output/freelance-scorecard.json \
  --markdown output/freelance-scorecard.md

# Generate 4-channel hunting queries for a domain:
python3 scripts/generate_queries.py --niche "property management" --output output/queries.json

# Validate evals and run self-maintenance:
python3 scripts/run_evals.py --validate
python3 scripts/run_evals.py --rollout
python3 scripts/evolve.py
```
## Verification

See [VERIFICATION.md](VERIFICATION.md) for recorded gate results and rollout evidence.
