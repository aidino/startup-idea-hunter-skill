#!/usr/bin/env python3
"""
Score and reframe startup clues using the Easy-Vibe 5-Criteria & Need-Tier framework.

Evaluates raw community clues across Frequency, Pain Level, Current Workaround,
Willingness to Pay, and Market Size; classifies need tiers (pain > gratification > desire);
maps AI input-to-output architectures; and builds a 5-step validation plan.

Example:
    $ python3 scripts/score_clues.py --input clues.json --output scorecard.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple


CRITERIA_WEIGHTS: Dict[str, float] = {
    "frequency": 0.20,
    "pain_level": 0.25,
    "current_workaround": 0.20,
    "willingness_to_pay": 0.25,
    "market_size": 0.10,
}

NEED_TIER_MULTIPLIERS: Dict[str, float] = {
    "pain": 1.15,
    "gratification": 1.00,
    "desire": 0.75,
}

VALID_CHANNELS = {
    "reddit_community_pain",
    "capterra_low_star_reviews",
    "indie_hackers_product_hunt",
    "upwork_fiverr_repetitive_jobs",
    "personal_or_peer_observation",
}


def _emit_error(
    message: str,
    error_type: str = "validation",
    details: List[Dict[str, str]] | None = None,
    hint: str = "",
) -> None:
    """Print structured JSON error to stderr and exit with code 1."""
    payload: Dict[str, Any] = {
        "error": message,
        "error_type": error_type,
        "details": details or [],
        "hint": hint or "Verify that input JSON contains 'niche' and a non-empty 'clues' list with 1-5 scores.",
    }
    sys.stderr.write(json.dumps(payload, ensure_ascii=False) + "\n")
    sys.exit(1)


def infer_need_tier(clue: Dict[str, Any]) -> str:
    """
    Determine or validate the Easy-Vibe need tier ('pain', 'gratification', or 'desire').

    Args:
        clue: Clue dictionary containing optional 'need_tier', 'quote', and 'scores'.

    Returns:
        Normalized need tier string ('pain', 'gratification', or 'desire').

    Raises:
        ValueError: If an explicit need_tier is not one of the allowed values.

    Example:
        >>> infer_need_tier({"need_tier": "pain"})
        'pain'
    """
    explicit = clue.get("need_tier")
    if explicit is not None:
        normalized = str(explicit).strip().lower()
        if normalized not in NEED_TIER_MULTIPLIERS:
            raise ValueError(
                f"Invalid need_tier '{explicit}'. Must be one of: pain, gratification, desire"
            )
        return normalized

    quote_lower = str(clue.get("quote", "")).lower()
    scores = clue.get("scores", {})
    pain_score = float(scores.get("pain_level", 3))
    wtp_score = float(scores.get("willingness_to_pay", 3))

    pain_markers = ("lost $", "unpaid", "waste", "hours", "nightmare", "compliance", "4am", "overdue", "audit")
    desire_markers = ("nice to have", "aesthetic", "someday", "streak", "badge", "ideal")

    if any(marker in quote_lower for marker in desire_markers) or (pain_score <= 2 and wtp_score <= 2):
        return "desire"
    if pain_score >= 4 or wtp_score >= 4 or any(marker in quote_lower for marker in pain_markers):
        return "pain"
    return "gratification"


def infer_ai_capability(input_data: str, output_data: str) -> str:
    """
    Map input and output descriptions to a concrete AI engineering pattern.

    Args:
        input_data: Description of the raw user input data.
        output_data: Description of the desired structured output.

    Returns:
        Recommended AI engineering architecture string.

    Example:
        >>> infer_ai_capability("Scanned PDF bank statements", "Balanced CSV")
        'VLM / OCR Document Parser + Deterministic Balance Validator'
    """
    combined = f"{input_data} {output_data}".lower()
    if any(token in combined for token in ("pdf", "scan", "image", "photo", "screenshot", "handwritten", "receipt")):
        return "VLM / OCR Document Parser + Deterministic Balance Validator"
    if any(token in combined for token in ("audio", "voice", "recording", "meeting", "call", "transcript", "podcast")):
        return "ASR (Whisper) + LLM Structured Action Extractor + Webhook Sync"
    if any(token in combined for token in ("contract", "scope", "policy", "quote", "diff", "clause", "revision")):
        return "Semantic Scope/Contract Diff Engine + Contextual Response Drafter"
    return "Multi-Source Context Aggregator + Strict Schema LLM Formatter"


def score_single_clue(clue: Dict[str, Any], index: int) -> Tuple[Dict[str, Any], List[str]]:
    """
    Validate and score a single clue using the 5-Criteria Easy-Vibe model.

    Args:
        clue: Raw clue object from input JSON.
        index: 0-based clue index for error reporting.

    Returns:
        Tuple of (enriched clue dictionary, list of sanity warning strings).

    Raises:
        ValueError: If required fields are missing or scores are outside [1, 5].

    Example:
        >>> c = {"id": "c1", "title": "Test", "quote": "I waste 3 hours", "persona_context": "Dev",
        ...      "input_data": "Logs", "output_data": "Invoice", "source_url": "ref:reddit-freelance-thread",
        ...      "scores": {"frequency": 4, "pain_level": 5, "current_workaround": 4, "willingness_to_pay": 4, "market_size": 4}}
        >>> scored, warnings = score_single_clue(c, 0)
        >>> scored["verdict"]
        'BUILD_MVP_NOW'
    """
    required_str_fields = ("id", "title", "quote", "persona_context", "input_data", "output_data", "source_url")
    for field in required_str_fields:
        val = clue.get(field)
        if not isinstance(val, str) or not val.strip():
            raise ValueError(f"clues[{index}].{field} must be a non-empty string")

    raw_scores = clue.get("scores")
    if not isinstance(raw_scores, dict):
        raise ValueError(f"clues[{index}].scores must be a JSON object")

    normalized_scores: Dict[str, float] = {}
    for criterion in CRITERIA_WEIGHTS:
        if criterion not in raw_scores:
            raise ValueError(f"clues[{index}].scores.{criterion} is required")
        val = raw_scores[criterion]
        if isinstance(val, bool) or not isinstance(val, (int, float)):
            raise ValueError(f"clues[{index}].scores.{criterion} must be a number between 1 and 5")
        fval = float(val)
        if fval < 1.0 or fval > 5.0:
            raise ValueError(
                f"clues[{index}].scores.{criterion} must be between 1 and 5 (got {val})"
            )
        normalized_scores[criterion] = fval

    need_tier = infer_need_tier(clue)
    multiplier = NEED_TIER_MULTIPLIERS[need_tier]

    weighted_sum_5 = sum(
        normalized_scores[k] * weight for k, weight in CRITERIA_WEIGHTS.items()
    )
    raw_score_100 = round(weighted_sum_5 * 20.0, 2)
    adjusted_score_100 = round(min(100.0, raw_score_100 * multiplier), 2)

    warnings: List[str] = []
    if need_tier == "desire" and raw_score_100 >= 75.0:
        warnings.append(
            f"Clue '{clue['id']}' has a high raw score ({raw_score_100}) but is classified as 'desire' (vitamin); "
            "capped recommendation to avoid the Xiaoming trap."
        )
    if normalized_scores["willingness_to_pay"] <= 2.0 and adjusted_score_100 >= 70.0:
        warnings.append(
            f"Clue '{clue['id']}' has low willingness_to_pay ({normalized_scores['willingness_to_pay']}/5) despite overall score."
        )

    if need_tier == "desire" or adjusted_score_100 < 58.0 or normalized_scores["willingness_to_pay"] <= 2.0:
        verdict = "SKIP_VITAMIN" if need_tier == "desire" or adjusted_score_100 < 50.0 else "NICHE_DOWN_FIRST"
    elif adjusted_score_100 >= 76.0 and normalized_scores["pain_level"] >= 4.0 and normalized_scores["willingness_to_pay"] >= 4.0:
        verdict = "BUILD_MVP_NOW"
    else:
        verdict = "NICHE_DOWN_FIRST"

    channel = str(clue.get("channel", "reddit_community_pain")).strip()
    if channel not in VALID_CHANNELS:
        channel = "personal_or_peer_observation"

    ai_capability = str(clue.get("ai_capability") or infer_ai_capability(clue["input_data"], clue["output_data"]))

    return (
        {
            "id": clue["id"].strip(),
            "title": clue["title"].strip(),
            "channel": channel,
            "quote": clue["quote"].strip(),
            "persona_context": clue["persona_context"].strip(),
            "input_data": clue["input_data"].strip(),
            "output_data": clue["output_data"].strip(),
            "ai_capability": ai_capability,
            "source_url": clue["source_url"].strip(),
            "source_date": str(clue.get("source_date", "2026-10-27")).strip(),
            "need_tier": need_tier,
            "need_tier_multiplier": multiplier,
            "scores": normalized_scores,
            "raw_score_100": raw_score_100,
            "adjusted_score_100": adjusted_score_100,
            "verdict": verdict,
            "horizontal_segment": str(clue.get("horizontal_segment") or clue["persona_context"]).strip(),
            "vertical_trigger_moment": str(
                clue.get("vertical_trigger_moment")
                or f"When handling {clue['input_data']} to produce {clue['output_data']}"
            ).strip(),
        },
        warnings,
    )


def build_mvp_validation_plan(top_clue: Dict[str, Any], niche: str) -> Dict[str, Any]:
    """
    Construct the Easy-Vibe Reframed Concept and 5-Step Demand Validation Plan for the winning clue.

    Args:
        top_clue: Highest-ranked scored clue dictionary.
        niche: Target domain or niche name.

    Returns:
        Dictionary describing the reframed concept, horizontal/vertical focus, and 5 validation steps.

    Example:
        >>> plan = build_mvp_validation_plan({"id": "c1", "title": "Scope Guard", "horizontal_segment": "Web Freelancers",
        ...     "vertical_trigger_moment": "Client asks for extra revision", "input_data": "Contract + Email",
        ...     "output_data": "Change Order Link", "ai_capability": "Diff Engine"}, "freelance")
        >>> len(plan["five_step_validation"])
        5
    """
    return {
        "winning_clue_id": top_clue["id"],
        "winning_title": top_clue["title"],
        "reframed_positioning": (
            f"Instead of a generic {niche} platform, build a focused '{top_clue['title']}' copilot "
            f"exclusively for {top_clue['horizontal_segment']}."
        ),
        "horizontal_segment": top_clue["horizontal_segment"],
        "vertical_context_timeline": top_clue["vertical_trigger_moment"],
        "ai_workflow_contract": {
            "input": top_clue["input_data"],
            "processing_engine": top_clue["ai_capability"],
            "output": top_clue["output_data"],
        },
        "five_step_validation": [
            {
                "step": 1,
                "name": "Talk to 10 Real Target Users About Current Behavior",
                "action": (
                    f"Recruit 10 {top_clue['horizontal_segment']} and ask how they currently handle "
                    f"'{top_clue['input_data']}'. Verify they already use a manual patch (spreadsheet, scripts, or unpaid overtime)."
                ),
            },
            {
                "step": 2,
                "name": "Benchmark Against Current Workaround Friction",
                "action": (
                    f"Ensure the AI workflow produces '{top_clue['output_data']}' in <60 seconds with zero manual template setup, "
                    "beating spreadsheets and bloated incumbent tools."
                ),
            },
            {
                "step": 3,
                "name": "Run Payment / Deposit Commitment Test",
                "action": (
                    "Present a concierge demo or landing page with a paid pilot/pre-order button. "
                    "Pass threshold: >10% conversion = strong signal; 5-10% = refine segment; <5% = pivot."
                ),
            },
            {
                "step": 4,
                "name": "Bottom-Up Market Sizing",
                "action": (
                    "Multiply reachable target segment count x willingness-to-pay conversion rate x annual subscription ARPU."
                ),
            },
            {
                "step": 5,
                "name": "Lock In Non-Trivial Defensibility (Moat)",
                "action": (
                    "Accumulate domain-specific edge-case benchmarks, vertical workflow integrations, and user correction loops "
                    "so generic chat wrappers cannot replicate the reliability."
                ),
            },
        ],
    }


def evaluate_clues(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and evaluate a complete clue dataset, returning ranked ideas and MVP plan.

    Args:
        payload: Dictionary with 'niche' and 'clues' list.

    Returns:
        Dictionary with ranked clues, summary metrics, MVP validation plan, and warnings.

    Raises:
        ValueError: If payload structure or clue fields are invalid.
    """
    if not isinstance(payload, dict):
        raise ValueError("Input payload must be a JSON object")

    niche = str(payload.get("niche", "")).strip()
    if len(niche) < 2:
        raise ValueError("Field 'niche' must be a non-empty string (at least 2 chars)")

    clues = payload.get("clues")
    if not isinstance(clues, list) or len(clues) == 0:
        raise ValueError("Field 'clues' must be a non-empty list of clue objects")

    scored_clues: List[Dict[str, Any]] = []
    all_warnings: List[str] = []
    seen_ids: set[str] = set()

    for idx, raw_clue in enumerate(clues):
        if not isinstance(raw_clue, dict):
            raise ValueError(f"clues[{idx}] must be a JSON object")
        scored, warnings = score_single_clue(raw_clue, idx)
        if scored["id"] in seen_ids:
            raise ValueError(f"Duplicate clue id '{scored['id']}' at clues[{idx}]")
        seen_ids.add(scored["id"])
        scored_clues.append(scored)
        all_warnings.extend(warnings)

    ranked = sorted(
        scored_clues,
        key=lambda item: (item["adjusted_score_100"], item["scores"]["pain_level"], item["scores"]["willingness_to_pay"]),
        reverse=True,
    )
    for rank_idx, item in enumerate(ranked, start=1):
        item["rank"] = rank_idx

    if all(item["adjusted_score_100"] == ranked[0]["adjusted_score_100"] for item in ranked) and len(ranked) > 1:
        all_warnings.append("All clues received identical adjusted scores; review criteria differentiation.")

    top_clue = ranked[0]
    mvp_plan = build_mvp_validation_plan(top_clue, niche)

    tier_counts = {"pain": 0, "gratification": 0, "desire": 0}
    for item in ranked:
        tier_counts[item["need_tier"]] += 1

    result: Dict[str, Any] = {
        "niche": niche,
        "summary": {
            "total_clues": len(ranked),
            "build_mvp_now_count": sum(1 for c in ranked if c["verdict"] == "BUILD_MVP_NOW"),
            "niche_down_count": sum(1 for c in ranked if c["verdict"] == "NICHE_DOWN_FIRST"),
            "skip_vitamin_count": sum(1 for c in ranked if c["verdict"] == "SKIP_VITAMIN"),
            "need_tier_breakdown": tier_counts,
            "top_recommendation_id": top_clue["id"],
            "top_recommendation_title": top_clue["title"],
            "top_adjusted_score": top_clue["adjusted_score_100"],
        },
        "ranked_clues": ranked,
        "mvp_validation_plan": mvp_plan,
        "_warnings": all_warnings,
    }
    return result


def render_markdown_report(evaluation: Dict[str, Any], query_pack: Dict[str, Any] | None = None) -> str:
    """
    Render a human-friendly Markdown report containing the Clue Page, Scorecard, and MVP Plan.

    Args:
        evaluation: Output dictionary from evaluate_clues().
        query_pack: Optional output dictionary from generate_query_pack().

    Returns:
        Formatted Markdown document string.
    """
    lines: List[str] = []
    niche = evaluation["niche"]
    summary = evaluation["summary"]
    lines.append(f"# Easy-Vibe Startup Idea Hunter Report: {niche}")
    lines.append("")
    lines.append(
        f"**Top Recommendation**: `{summary['top_recommendation_id']}` — **{summary['top_recommendation_title']}** "
        f"(Score: **{summary['top_adjusted_score']}/100**)"
    )
    lines.append("")

    if query_pack and query_pack.get("channels"):
        lines.append("## 1. 4-Channel Hunting Query Pack")
        lines.append("")
        for ch in query_pack["channels"]:
            lines.append(f"### Step {ch['step']}: {ch['title']}")
            for q in ch["queries"]:
                lines.append(f"- `{q}`")
            lines.append("")

    lines.append("## 2. Easy-Vibe Clue Page (Source-Backed Evidence)")
    lines.append("")
    lines.append("| Rank | ID | Clue & Verbatim Quote | Persona & Context | Input -> AI -> Output | Source |")
    lines.append("|---:|---|---|---|---|---|")
    for item in evaluation["ranked_clues"]:
        short_quote = item["quote"]
        if len(short_quote) > 110:
            short_quote = short_quote[:107] + "..."
        io_chain = f"**In**: {item['input_data']}<br>**AI**: {item['ai_capability']}<br>**Out**: {item['output_data']}"
        lines.append(
            f"| {item['rank']} | `{item['id']}` | **{item['title']}**: *\"{short_quote}\"* | "
            f"{item['persona_context']} | {io_chain} | [{item['channel']}]({item['source_url']}) ({item['source_date']}) |"
        )
    lines.append("")

    lines.append("## 3. 5-Criteria Startup Idea Scorecard")
    lines.append("")
    lines.append("| Rank | ID | Need Tier | Freq (20%) | Pain (25%) | Workaround (20%) | WTP (25%) | Market (10%) | Score /100 | Verdict |")
    lines.append("|---:|---|---|---:|---:|---:|---:|---:|---:|---|")
    for item in evaluation["ranked_clues"]:
        sc = item["scores"]
        lines.append(
            f"| {item['rank']} | `{item['id']}` | `{item['need_tier']}` ({item['need_tier_multiplier']}x) | "
            f"{sc['frequency']:.1f} | {sc['pain_level']:.1f} | {sc['current_workaround']:.1f} | "
            f"{sc['willingness_to_pay']:.1f} | {sc['market_size']:.1f} | **{item['adjusted_score_100']:.2f}** | `{item['verdict']}` |"
        )
    lines.append("")

    plan = evaluation["mvp_validation_plan"]
    lines.append("## 4. Reframed AI MVP Concept & 5-Step Validation Plan")
    lines.append("")
    lines.append(f"- **Winning Concept**: **{plan['winning_title']}** (`{plan['winning_clue_id']}`)")
    lines.append(f"- **Reframed Positioning**: {plan['reframed_positioning']}")
    lines.append(f"- **Horizontal Segment**: {plan['horizontal_segment']}")
    lines.append(f"- **Vertical Trigger Moment**: {plan['vertical_context_timeline']}")
    lines.append(f"- **Input -> AI -> Output**: `{plan['ai_workflow_contract']['input']}` -> `{plan['ai_workflow_contract']['processing_engine']}` -> `{plan['ai_workflow_contract']['output']}`")
    lines.append("")
    lines.append("### 5-Step Demand Validation Checklist")
    for step in plan["five_step_validation"]:
        lines.append(f"{step['step']}. **{step['name']}**: {step['action']}")
    lines.append("")

    if evaluation.get("_warnings"):
        lines.append("## Warnings")
        for w in evaluation["_warnings"]:
            lines.append(f"- {w}")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    """CLI entry point for scoring a JSON clue file."""
    parser = argparse.ArgumentParser(
        description="Score startup clues using the Easy-Vibe 5-Criteria model."
    )
    parser.add_argument("--input", required=True, help="Path to input clue JSON file")
    parser.add_argument("--output", default="scorecard.json", help="Path to output JSON file")
    parser.add_argument("--markdown", default="", help="Optional path to output Markdown report")
    args = parser.parse_args()

    in_path = Path(args.input)
    if not in_path.is_file():
        _emit_error(
            f"Input file does not exist: {in_path}",
            error_type="validation",
            details=[{"field": "input", "error": "file_not_found"}],
        )
        return

    try:
        payload = json.loads(in_path.read_text(encoding="utf-8"))
        result = evaluate_clues(payload)
    except json.JSONDecodeError as exc:
        _emit_error(f"Malformed JSON in {in_path}: {exc}", error_type="validation")
        return
    except ValueError as exc:
        _emit_error(str(exc), error_type="validation")
        return

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if args.markdown:
        md_path = Path(args.markdown)
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(render_markdown_report(result), encoding="utf-8")

    print(f"Saved scorecard to {out_path}")


if __name__ == "__main__":
    main()
