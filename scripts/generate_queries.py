#!/usr/bin/env python3
"""
Generate 4-channel startup clue hunting queries following the Easy-Vibe methodology.

Builds targeted search queries across Reddit/communities, Capterra/G2 low-star
software reviews, Indie Hackers/Product Hunt launches, and Upwork/Fiverr repetitive
freelance jobs, paired with an AI Engineer input-to-output inspection lens.

Example:
    $ python3 scripts/generate_queries.py --niche "freelance workflows" --output queries.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


DEFAULT_CHANNELS: List[str] = [
    "reddit_community_pain",
    "capterra_low_star_reviews",
    "indie_hackers_product_hunt",
    "upwork_fiverr_repetitive_jobs",
]


def _emit_error(message: str, error_type: str = "validation", details: List[Dict[str, str]] | None = None, hint: str = "") -> None:
    """Print structured JSON error to stderr and exit with code 1."""
    payload: Dict[str, Any] = {
        "error": message,
        "error_type": error_type,
        "details": details or [],
        "hint": hint or "Provide a non-empty --niche string (2-120 characters).",
    }
    sys.stderr.write(json.dumps(payload, ensure_ascii=False) + "\n")
    sys.exit(1)


def generate_query_pack(niche: str, target_segments: List[str] | None = None) -> Dict[str, Any]:
    """
    Generate a 4-channel search query pack for a given domain or niche.

    Args:
        niche: Target domain or workflow niche (e.g., "freelance workflows").
        target_segments: Optional list of narrower horizontal user segments.

    Returns:
        Dictionary containing normalized niche, channels with search queries,
        and AI Engineer inspection lenses.

    Raises:
        ValueError: If niche is empty or exceeds 120 characters.

    Example:
        >>> pack = generate_query_pack("freelance workflows")
        >>> len(pack["channels"])
        4
    """
    cleaned = " ".join((niche or "").strip().split())
    if len(cleaned) < 2:
        raise ValueError("niche must be at least 2 characters long")
    if len(cleaned) > 120:
        raise ValueError("niche must not exceed 120 characters")

    segments = [s.strip() for s in (target_segments or []) if isinstance(s, str) and s.strip()]
    primary_term = cleaned.lower()

    channels: List[Dict[str, Any]] = [
        {
            "channel_id": "reddit_community_pain",
            "step": 1,
            "title": "Reddit & Community Manual Workflow Pain",
            "objective": "Catch users describing repetitive copy-paste, spreadsheet glue, or hours wasted.",
            "queries": [
                f'site:reddit.com "{primary_term}" ("is there a tool" OR "i spend hours" OR "manually")',
                f'site:reddit.com "{primary_term}" ("tedious" OR "nightmare" OR "waste of time" OR "spreadsheet")',
                f'site:reddit.com "{primary_term}" ("how do you automate" OR "copy paste" OR "every week")',
            ],
            "what_to_save": "Verbatim complaint quote, user role/context, trigger frequency, and link with date.",
        },
        {
            "channel_id": "capterra_low_star_reviews",
            "step": 2,
            "title": "Capterra & G2 1-to-3 Star Software Reviews",
            "objective": "Find paying software users frustrated by clunky UX, manual imports, or missing smart automation.",
            "queries": [
                f'site:capterra.com "{primary_term}" ("Cons" OR "clunky" OR "manual" OR "frustrating")',
                f'site:capterra.com "{primary_term}" ("import" OR "formatting" OR "template" OR "too many clicks")',
                f'site:g2.com "{primary_term}" ("What do you dislike" OR "manual entry" OR "export")',
            ],
            "what_to_save": "Incumbent software name, exact 'Cons' quote, and the manual workaround users are forced to do.",
        },
        {
            "channel_id": "indie_hackers_product_hunt",
            "step": 3,
            "title": "Indie Hackers Revenue Proofs & Product Hunt Launch Comments",
            "objective": "Verify solo-founder willingness-to-pay ($500-$5,000/mo) and unserved edge cases in launch comments.",
            "queries": [
                f'site:indiehackers.com "{primary_term}" ("problem" OR "revenue" OR "customers" OR "launched")',
                f'site:producthunt.com "{primary_term}" ("does it support" OR "can it handle" OR "alternative")',
                f'site:trends.google.com "{primary_term}"',
            ],
            "what_to_save": "One-line value proposition, pricing tier, first customer acquisition channel, and unmet comment requests.",
        },
        {
            "channel_id": "upwork_fiverr_repetitive_jobs",
            "step": 4,
            "title": "Upwork & Fiverr Paid Repetitive Human Tasks",
            "objective": "Spot recurring manual data processing tasks where clients already pay humans per batch.",
            "queries": [
                f'site:upwork.com/freelance-jobs "{primary_term}" ("convert" OR "extract" OR "format" OR "transcribe")',
                f'site:upwork.com/services "{primary_term}" ("clean" OR "spreadsheet" OR "PDF" OR "automation")',
                f'site:fiverr.com "{primary_term}" ("data entry" OR "formatting" OR "summary" OR "audit")',
            ],
            "what_to_save": "Exact raw input files provided by the client and the exact deliverable format expected back.",
        },
    ]

    ai_engineer_lenses: List[Dict[str, str]] = [
        {
            "pattern": "Messy Document / Screenshot -> Structured Table",
            "ai_stack": "Vision-Language Model (VLM) + Strict JSON Schema Validator",
            "signal": "Users re-typing PDFs, receipts, schedules, or WhatsApp/Zalo screenshots into Excel/CSV.",
        },
        {
            "pattern": "Voice / Meeting / Call Recording -> Actionable System Tasks",
            "ai_stack": "ASR (Whisper) + LLM Action Extractor + Task API Webhook",
            "signal": "Users re-listening to client calls to write proposals, scope changes, or Trello/ClickUp tickets.",
        },
        {
            "pattern": "Incoming Request vs. Baseline Contract / Policy Diffing",
            "ai_stack": "Embedding Retrieval + Structured Semantic Diff + Draft Response Generator",
            "signal": "Users losing money or time to scope creep, compliance checks, or vendor quote comparisons.",
        },
        {
            "pattern": "Multi-App Context Glue -> Ready-to-Send Artifact",
            "ai_stack": "Deterministic Connector Script + Few-Shot LLM Formatter",
            "signal": "Users opening 3+ tabs every week to piece together timesheets, invoices, or multi-format posts.",
        },
    ]

    return {
        "niche": cleaned,
        "target_segments": segments,
        "channel_count": len(channels),
        "channels": channels,
        "ai_engineer_lenses": ai_engineer_lenses,
    }


def main() -> None:
    """CLI entry point for generating a 4-channel hunting query pack."""
    parser = argparse.ArgumentParser(
        description="Generate 4-channel Easy-Vibe startup clue hunting queries."
    )
    parser.add_argument("--niche", required=True, help="Target domain or niche to hunt clues in")
    parser.add_argument(
        "--segment",
        action="append",
        default=[],
        help="Optional horizontal user sub-segment (repeatable)",
    )
    parser.add_argument("--output", default="queries.json", help="Output JSON file path")
    args = parser.parse_args()

    try:
        result = generate_query_pack(args.niche, args.segment)
    except ValueError as exc:
        _emit_error(str(exc), error_type="validation", details=[{"field": "niche", "error": str(exc)}])
        return

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Saved query pack to {out_path}")


if __name__ == "__main__":
    main()
