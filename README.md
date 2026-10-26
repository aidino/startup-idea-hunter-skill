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

## Usage Examples

### 1. Run End-to-End Scoring & MVP Reframing on Collected Clues

```bash
python3 scripts/run_pipeline.py \
  --input evals/golden/case-1/input.json \
  --output output/freelance-scorecard.json \
  --markdown output/freelance-scorecard.md
```

### 2. Generate 4-Channel Hunting Queries for a New Niche

```bash
python3 scripts/generate_queries.py \
  --niche "property management" \
  --segment "independent landlords with 5-30 units" \
  --output output/queries.json
```

### 3. Run Bundled Evaluations & Self-Maintenance

```bash
python3 scripts/run_evals.py --validate
python3 scripts/run_evals.py --rollout
python3 scripts/evolve.py
```

## Verification

See [VERIFICATION.md](VERIFICATION.md) for recorded gate results and rollout evidence.
