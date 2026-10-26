#!/usr/bin/env python3
"""
Single orchestrator entry-point for startup-idea-hunter-skill.

Wires Step 1 (4-channel query pack generation) and Step 2 (Easy-Vibe Clue Page
validation, 5-criteria scoring, need-tier classification, and MVP reframing) in code,
writes JSON and Markdown deliverables, and records privacy-preserving lifecycle events.

Example:
    $ python3 scripts/run_pipeline.py --input evals/golden/case-1/input.json --output output/scorecard.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from generate_queries import generate_query_pack  # noqa: E402
from score_clues import evaluate_clues, render_markdown_report  # noqa: E402

try:
    from success_ledger import record_event  # type: ignore
except Exception:  # pragma: no cover
    record_event = None  # type: ignore


SKILL_NAME = "startup-idea-hunter-skill"
SKILL_VERSION = "1.0.0"


def _emit_error(
    message: str,
    error_type: str = "validation",
    details: List[Dict[str, str]] | None = None,
    hint: str = "",
) -> None:
    """Emit structured JSON error to stderr and exit 1."""
    payload: Dict[str, Any] = {
        "error": message,
        "error_type": error_type,
        "details": details or [],
        "hint": hint or "Run with --input <clues.json> --output <result.json> or --check-prereqs.",
    }
    sys.stderr.write(json.dumps(payload, ensure_ascii=False) + "\n")
    sys.exit(1)


def check_prereqs() -> Dict[str, Any]:
    """
    Verify runtime prerequisites (Python >= 3.9, standard library modules, write access).

    Returns:
        Dictionary with 'ready' boolean and 'checks' list.
    """
    py_ok = sys.version_info >= (3, 9)
    checks = [
        {
            "check": "python_version",
            "required": ">=3.9",
            "found": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "ok": py_ok,
        },
        {
            "check": "config_asset",
            "required": "assets/config.json",
            "found": str((SCRIPT_DIR.parent / "assets" / "config.json").is_file()),
            "ok": (SCRIPT_DIR.parent / "assets" / "config.json").is_file(),
        },
    ]
    return {"ready": all(item["ok"] for item in checks), "checks": checks}


def diagnostics() -> Dict[str, Any]:
    """
    Return skill metadata and enabled harness capabilities.

    Returns:
        Dictionary describing skill version, commands, and harness features.
    """
    return {
        "skill": SKILL_NAME,
        "version": SKILL_VERSION,
        "harness_level": "standard-v1",
        "commands": [
            "python3 scripts/run_pipeline.py --input <file.json> --output <out.json>",
            "python3 scripts/run_pipeline.py --check-prereqs",
            "python3 scripts/run_pipeline.py --diagnostics",
            "python3 scripts/generate_queries.py --niche <domain> --output <queries.json>",
            "python3 scripts/score_clues.py --input <file.json> --output <out.json>",
        ],
        "harness_features": {
            "input_validation": True,
            "output_sanity": True,
            "structured_errors": True,
            "success_ledger": True,
        },
    }


def run_pipeline(input_path: Path, output_path: Path, markdown_path: Path | None = None) -> Dict[str, Any]:
    """
    Execute the full Easy-Vibe startup idea discovery and scoring pipeline.

    Args:
        input_path: Path to input JSON containing 'niche' and 'clues'.
        output_path: Path where the combined JSON output will be written.
        markdown_path: Optional path where the Markdown report will be written.

    Returns:
        Combined result dictionary written to output_path.

    Raises:
        ValueError: If input file is missing, malformed, or fails validation.
    """
    started = time.monotonic()
    if not input_path.is_file():
        raise ValueError(f"Input file not found: {input_path}")

    try:
        raw_payload = json.loads(input_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {input_path}: {exc}") from exc

    if not isinstance(raw_payload, dict):
        raise ValueError("Input JSON root must be an object")

    niche = str(raw_payload.get("niche", "")).strip()
    segments = raw_payload.get("target_segments") if isinstance(raw_payload.get("target_segments"), list) else []

    # Step 1: Generate 4-channel hunting query pack in code
    query_pack = generate_query_pack(niche, segments)

    # Step 2: Score clues, classify need tiers, and build reframed MVP plan in code
    evaluation = evaluate_clues(raw_payload)

    combined: Dict[str, Any] = {
        "skill": SKILL_NAME,
        "version": SKILL_VERSION,
        "niche": evaluation["niche"],
        "query_pack": query_pack,
        "summary": evaluation["summary"],
        "ranked_clues": evaluation["ranked_clues"],
        "mvp_validation_plan": evaluation["mvp_validation_plan"],
        "_warnings": evaluation["_warnings"],
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(combined, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    md_target = markdown_path or output_path.with_suffix(".md")
    md_target.parent.mkdir(parents=True, exist_ok=True)
    md_target.write_text(render_markdown_report(evaluation, query_pack), encoding="utf-8")

    if record_event is not None:
        try:
            event = os.environ.get("ASC_RUN_EVENT", "skill_run")
            record_event(
                event,
                skill=SKILL_NAME,
                run_id=os.environ.get("ASC_RUN_ID"),
                duration_seconds=time.monotonic() - started,
            )
        except (OSError, ValueError) as exc:
            sys.stderr.write(f"Warning: success_ledger recording skipped: {exc}\n")

    return combined


def main() -> None:
    """CLI entry point for the startup-idea-hunter-skill orchestrator."""
    parser = argparse.ArgumentParser(
        description="Run the end-to-end Easy-Vibe Startup Idea Hunter pipeline."
    )
    parser.add_argument("--input", help="Path to input clue JSON file")
    parser.add_argument("--output", default="output/scorecard.json", help="Path to output JSON file")
    parser.add_argument("--markdown", default="", help="Optional path to output Markdown report")
    parser.add_argument("--check-prereqs", action="store_true", help="Check runtime prerequisites and exit")
    parser.add_argument("--diagnostics", action="store_true", help="Print skill diagnostics JSON and exit")
    args = parser.parse_args()

    if args.check_prereqs:
        prereq_result = check_prereqs()
        print(json.dumps(prereq_result, indent=2))
        sys.exit(0 if prereq_result["ready"] else 1)

    if args.diagnostics:
        print(json.dumps(diagnostics(), indent=2))
        sys.exit(0)

    if not args.input:
        _emit_error(
            "Missing required argument: --input",
            error_type="validation",
            details=[{"field": "input", "error": "required"}],
        )
        return

    try:
        md_path = Path(args.markdown) if args.markdown else None
        run_pipeline(Path(args.input), Path(args.output), md_path)
    except ValueError as exc:
        _emit_error(str(exc), error_type="validation", details=[{"field": "input", "error": str(exc)}])
        return
    except OSError as exc:
        _emit_error(str(exc), error_type="runtime", details=[{"field": "io", "error": str(exc)}])
        return


if __name__ == "__main__":
    main()
