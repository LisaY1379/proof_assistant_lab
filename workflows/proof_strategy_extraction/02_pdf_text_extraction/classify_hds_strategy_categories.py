#!/usr/bin/env python3
"""
Thin wrapper: classify HighDimensionalStatistics key strategies using the shared
classifier from 01_lean_translation.

This intentionally does NOT duplicate the classifier logic. It only supplies HDS
input/output paths:

  proofs:     data/high_dimensional_statistics/processed/proofs_with_key_strategies.jsonl
  mirror:     data/high_dimensional_statistics/processed/proofs_with_key_strategies.json
  categories: data/high_dimensional_statistics/processed/strategy_categories.txt

Run from project root:

  .venv/bin/python workflows/proof_strategy_extraction/02_pdf_text_extraction/classify_hds_strategy_categories.py --until-proof 58

Dry run:

  .venv/bin/python workflows/proof_strategy_extraction/02_pdf_text_extraction/classify_hds_strategy_categories.py --until-proof 5 --dry-run
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SHARED_CLASSIFIER = PROJECT_ROOT / "workflows" / "proof_strategy_extraction" / "01_lean_translation" / "classify_strategy_categories.py"
HDS_PROCESSED = PROJECT_ROOT / "data" / "high_dimensional_statistics" / "processed"
HDS_PROOFS_JSONL = HDS_PROCESSED / "proofs_with_key_strategies.jsonl"
HDS_PROOFS_JSON = HDS_PROCESSED / "proofs_with_key_strategies.json"
HDS_CATEGORIES = HDS_PROCESSED / "strategy_categories.txt"
HDS_ASSIGNMENTS_JSON = HDS_PROCESSED / "strategy_category_assignments.json"
HDS_ASSIGNMENTS_CSV = HDS_PROCESSED / "strategy_category_assignments.csv"
HDS_ASSIGNMENTS_MD = HDS_PROCESSED / "strategy_category_assignments.md"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Wrapper for classifying HDS proof strategy objects using the shared classifier."
    )
    parser.add_argument(
        "--until-proof",
        type=int,
        default=58,
        help="Classify strategy categories through HDS proof item N. Default: 58",
    )
    parser.add_argument("--model", default="gpt-5.6-sol", help="OpenAI model. Default: gpt-5.6-sol")
    parser.add_argument("--api-base", default="https://api.openai.com/v1", help="OpenAI-compatible API base URL.")
    parser.add_argument("--temperature", type=float, default=1.0, help="Sampling temperature. Default: 1.0")
    parser.add_argument(
        "--reasoning-effort",
        choices=["low", "medium", "high"],
        default="high",
        help="Reasoning effort for supported models. Default: high",
    )
    parser.add_argument(
        "--classification-max-tokens",
        type=int,
        default=1000,
        help="Max completion tokens for each classification call. Default: 1000",
    )
    parser.add_argument(
        "--redo-assignments",
        action="store_true",
        help="Redo proof-strategy category assignment while keeping the existing HDS category taxonomy.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print what would happen, but do not call the API.")
    args = parser.parse_args()

    if not SHARED_CLASSIFIER.exists():
        raise FileNotFoundError(f"Shared classifier not found: {SHARED_CLASSIFIER}")
    if not HDS_PROOFS_JSONL.exists():
        raise FileNotFoundError(f"HDS proof library not found: {HDS_PROOFS_JSONL}")
    if not HDS_CATEGORIES.exists():
        raise FileNotFoundError(
            f"HDS category taxonomy not found: {HDS_CATEGORIES}\n"
            "Run first:\n"
            "  .venv/bin/python workflows/proof_strategy_extraction/02_pdf_text_extraction/categorize_strategy_library.py --no-resume"
        )

    cmd = [
        sys.executable,
        str(SHARED_CLASSIFIER),
        "--until-proof",
        str(args.until_proof),
        "--proofs-jsonl",
        str(HDS_PROOFS_JSONL),
        "--proofs-json",
        str(HDS_PROOFS_JSON),
        "--categories",
        str(HDS_CATEGORIES),
        "--assignments-json",
        str(HDS_ASSIGNMENTS_JSON),
        "--assignments-csv",
        str(HDS_ASSIGNMENTS_CSV),
        "--assignments-md",
        str(HDS_ASSIGNMENTS_MD),
        "--model",
        args.model,
        "--api-base",
        args.api_base,
        "--temperature",
        str(args.temperature),
        "--reasoning-effort",
        args.reasoning_effort,
        "--classification-max-tokens",
        str(args.classification_max_tokens),
    ]
    if args.redo_assignments:
        cmd.append("--redo-assignments")
    if args.dry_run:
        cmd.append("--dry-run")

    print("Delegating to shared classifier:")
    print(" ".join(cmd))
    raise SystemExit(subprocess.call(cmd, cwd=PROJECT_ROOT))


if __name__ == "__main__":
    main()
