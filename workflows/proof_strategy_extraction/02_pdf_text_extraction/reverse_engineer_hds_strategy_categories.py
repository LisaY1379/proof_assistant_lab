#!/usr/bin/env python3
"""
Thin wrapper: reverse-engineer HighDimensionalStatistics strategy categories using
cleaned LaTeX textbook text.

This delegates to the existing shared reverse-engineering workflow in
01_lean_translation/reverse_engineer_strategy_categories.py, but changes one input
behavior for HDS:

  When the shared workflow asks for the plain-English proof explanation, this
  wrapper supplies:

    plain_english_statement_cleaned / plain_english_statement
    +
    plain_english_proof_cleaned / plain_english_proof

  as `textbook_explanation`.

It does not duplicate the reverse-engineering logic.

Run from project root:

  .venv/bin/python workflows/proof_strategy_extraction/02_pdf_text_extraction/reverse_engineer_hds_strategy_categories.py --until-proof 58

Dry run:

  .venv/bin/python workflows/proof_strategy_extraction/02_pdf_text_extraction/reverse_engineer_hds_strategy_categories.py --until-proof 5 --dry-run
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import sys
from pathlib import Path
from typing import Any, Dict

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SHARED_REVERSE = PROJECT_ROOT / "workflows" / "proof_strategy_extraction" / "01_lean_translation" / "reverse_engineer_strategy_categories.py"
HDS_PROCESSED = PROJECT_ROOT / "data" / "high_dimensional_statistics" / "processed"
HDS_PROOFS_JSONL = HDS_PROCESSED / "proofs_with_key_strategies.jsonl"
HDS_PROOFS_JSON = HDS_PROCESSED / "proofs_with_key_strategies.json"
HDS_CATEGORIES = HDS_PROCESSED / "strategy_categories.txt"


def load_shared_reverse() -> Any:
    # The shared reverse script imports sibling modules (`run_pipeline`,
    # `categorize_strategy_library`) by bare name, so put its directory on sys.path.
    shared_dir = SHARED_REVERSE.parent
    if str(shared_dir) not in sys.path:
        sys.path.insert(0, str(shared_dir))

    spec = importlib.util.spec_from_file_location("hds_shared_reverse_engineer", SHARED_REVERSE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not import shared reverse workflow: {SHARED_REVERSE}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def cleaned_hds_textbook_explanation(proof: Dict[str, Any]) -> str:
    statement = str(
        proof.get("plain_english_statement_cleaned")
        or proof.get("plain_english_statement")
        or proof.get("plain_english")
        or ""
    ).strip()
    proof_text = str(
        proof.get("plain_english_proof_cleaned")
        or proof.get("plain_english_proof")
        or ""
    ).strip()

    parts = []
    if statement:
        parts.append("Statement:\n" + statement)
    if proof_text:
        parts.append("Proof:\n" + proof_text)
    return "\n\n---\n\n".join(parts)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="HDS wrapper for reverse-engineering strategy categories from cleaned LaTeX book text."
    )
    parser.add_argument(
        "--until-proof",
        type=int,
        required=True,
        help="Process/refine HDS proofs from item #1 through this proof number.",
    )
    parser.add_argument("--proofs-jsonl", type=Path, default=HDS_PROOFS_JSONL)
    parser.add_argument("--proofs-json", type=Path, default=HDS_PROOFS_JSON)
    parser.add_argument("--categories", type=Path, default=HDS_CATEGORIES)
    parser.add_argument("--model", default="gpt-5.6-sol", help="OpenAI model. Default: gpt-5.6-sol")
    parser.add_argument("--api-base", default="https://api.openai.com/v1")
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument(
        "--reasoning-effort",
        choices=["low", "medium", "high"],
        default="high",
        help="Reasoning effort for supported models. Default: high",
    )
    parser.add_argument("--max-tokens", type=int, default=1800, help="Max completion tokens per proof.")
    parser.add_argument("--no-resume", action="store_true", help="Recompute strategies_refined even if already present.")
    parser.add_argument("--dry-run", action="store_true", help="Preview work without API calls or file writes.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    shared = load_shared_reverse()

    if not args.proofs_jsonl.exists():
        raise FileNotFoundError(f"HDS proof library not found: {args.proofs_jsonl}")
    if not args.categories.exists():
        raise FileNotFoundError(
            f"HDS category taxonomy not found: {args.categories}\n"
            "Run first:\n"
            "  .venv/bin/python workflows/proof_strategy_extraction/02_pdf_text_extraction/categorize_strategy_library.py --no-resume"
        )

    # Monkeypatch only the single HDS-specific behavior: what plain-English proof
    # text is sent to the LLM. The original function already prefers
    # `textbook_explanation`, so pass a copied proof with that field populated by
    # the cleaned HDS LaTeX statement/proof.
    original_reverse_one = shared.reverse_engineer_one_proof

    def reverse_one_with_cleaned_hds_text(*, proof: Dict[str, Any], **kwargs: Any) -> Any:
        proof_for_prompt = dict(proof)
        proof_for_prompt["textbook_explanation"] = cleaned_hds_textbook_explanation(proof)
        proof_for_prompt["plain_english"] = proof_for_prompt["textbook_explanation"]
        return original_reverse_one(proof=proof_for_prompt, **kwargs)

    shared.reverse_engineer_one_proof = reverse_one_with_cleaned_hds_text

    shared.load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not args.dry_run and (not api_key or api_key == "your-openai-api-key-here"):
        raise RuntimeError("OPENAI_API_KEY is missing or still set to the placeholder. Put a real key in .env or export it.")

    shared.run_workflow(
        proofs_jsonl=args.proofs_jsonl,
        proofs_json=args.proofs_json,
        categories_path=args.categories,
        until_proof=args.until_proof,
        api_key=api_key,
        model=args.model,
        api_base=args.api_base,
        temperature=args.temperature,
        reasoning_effort=args.reasoning_effort,
        max_tokens=args.max_tokens,
        resume=not args.no_resume,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
