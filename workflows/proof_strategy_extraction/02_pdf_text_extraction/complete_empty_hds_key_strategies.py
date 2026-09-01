#!/usr/bin/env python3
"""
Complete missing/empty key strategies in the HighDimensionalStatistics library.

This is a repair workflow for records where:
  - there is book proof text, but
  - key_strategies is missing or empty.

It reuses the existing HDS key-strategy extraction engine in:
  extract_hds_key_strategies.py

It does NOT overwrite non-empty key_strategies unless --no-resume is passed.
Records with no book proof text are skipped and marked no_book_proof_text by the
underlying engine.

Example usage from repository root:

  .venv/bin/python workflows/proof_strategy_extraction/02_pdf_text_extraction/complete_empty_hds_key_strategies.py --until 58

Dry run:

  .venv/bin/python workflows/proof_strategy_extraction/02_pdf_text_extraction/complete_empty_hds_key_strategies.py --until 58 --dry-run
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import sys
from pathlib import Path
from typing import Any, List, Optional

HERE = Path(__file__).resolve().parent
ENGINE_PATH = HERE / "extract_hds_key_strategies.py"


def load_engine() -> Any:
    spec = importlib.util.spec_from_file_location("extract_hds_key_strategies", ENGINE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load engine from {ENGINE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def parse_args() -> argparse.Namespace:
    engine = load_engine()
    parser = argparse.ArgumentParser(
        description="Repair empty HDS key_strategies entries using the existing HDS key-strategy extraction engine."
    )
    parser.add_argument(
        "--library",
        type=Path,
        default=engine.DEFAULT_LIBRARY_PATH,
        help=f"Input/output HDS library JSONL. Default: {engine.DEFAULT_LIBRARY_PATH}",
    )
    parser.add_argument(
        "--json-mirror",
        type=Path,
        default=engine.DEFAULT_JSON_MIRROR_PATH,
        help=f"Optional JSON mirror path. Default: {engine.DEFAULT_JSON_MIRROR_PATH}",
    )
    parser.add_argument(
        "--until",
        type=int,
        default=None,
        help="Process records from the start through this 1-based record number. Default: all records.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Alias for --until.",
    )
    parser.add_argument("--model", default=engine.DEFAULT_MODEL, help=f"OpenAI model. Default: {engine.DEFAULT_MODEL}")
    parser.add_argument("--api-base", default=engine.DEFAULT_API_BASE, help=f"OpenAI API base. Default: {engine.DEFAULT_API_BASE}")
    parser.add_argument("--temperature", type=float, default=1.0, help="Temperature. Default: 1.0")
    parser.add_argument(
        "--reasoning-effort",
        default="high",
        type=engine.parse_reasoning_effort,
        help="Reasoning effort: none, low, medium, high. Default: high",
    )
    parser.add_argument("--max-tokens", type=int, default=700, help="max_completion_tokens. Default: 700")
    parser.add_argument("--sleep", type=float, default=0.0, help="Seconds to sleep between API calls.")
    parser.add_argument(
        "--no-resume",
        action="store_true",
        help="Overwrite non-empty key_strategies too. Normally this repair workflow only fills empty entries.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Inspect pending empty entries without API calls or writes.")
    return parser.parse_args()


def main() -> None:
    engine = load_engine()
    args = parse_args()
    until = args.until if args.until is not None else args.limit

    engine.load_project_env(override=True)
    api_key = "" if args.dry_run else os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key and not args.dry_run:
        raise SystemExit("OPENAI_API_KEY is not set. Add it to .env or export it before running.")
    records = engine.read_jsonl(args.library)

    # The underlying engine already treats non-empty key_strategies as complete
    # when resume=True, and treats empty/missing key_strategies as pending if a
    # book proof exists. That is exactly the repair behavior we need here.
    engine.process_records(
        records=records,
        until=until,
        api_key=api_key or "",
        model=args.model,
        api_base=args.api_base,
        temperature=args.temperature,
        reasoning_effort=args.reasoning_effort,
        max_tokens=args.max_tokens,
        sleep_seconds=args.sleep,
        resume=not args.no_resume,
        dry_run=args.dry_run,
        library_path=args.library,
        json_mirror_path=args.json_mirror,
    )


if __name__ == "__main__":
    main()
