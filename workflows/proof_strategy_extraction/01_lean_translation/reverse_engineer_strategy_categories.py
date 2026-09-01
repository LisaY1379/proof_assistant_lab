#!/usr/bin/env python3
"""
Reverse-engineer proof strategy categories directly from each processed proof.

This workflow reads processed proof records from:
    data/processed/proofs_with_key_strategies.jsonl

For each proof through a requested proof number, it gives the LLM:
    - formal_statement
    - comment
    - plain_english / textbook_explanation
    - the existing strategy category taxonomy from strategy_categories.txt

The LLM chooses which category/categories likely appear in the proof and explains
where in the proof each category appears. The result is stored in each proof record
under:
    strategies_refined

Example output shape per proof:
    "strategies_refined": [
      {
        "category": "By definition / standard characterization",
        "evidence": "The proof rewrites ContinuousWithinAt using Metric.continuousWithinAt_iff.",
        "explanation": "The proof succeeds by replacing the abstract continuity predicate with its standard epsilon-delta characterization.",
        "confidence": "high",
        "category_name_match": true
      }
    ]

Run from project root:
    .venv/bin/python workflows/proof_strategy_extraction/reverse_engineer_strategy_categories.py --until-proof 10

Dry run:
    .venv/bin/python workflows/proof_strategy_extraction/reverse_engineer_strategy_categories.py --until-proof 10 --dry-run

Force recomputation:
    .venv/bin/python workflows/proof_strategy_extraction/reverse_engineer_strategy_categories.py --until-proof 10 --no-resume
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from run_pipeline import read_jsonl, write_jsonl
from categorize_strategy_library import (
    DEFAULT_CATEGORIES_OUTPUT,
    call_openai_chat,
    load_dotenv,
    parse_category_names,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PROOFS_JSONL = PROJECT_ROOT / "data" / "processed" / "proofs_with_key_strategies.jsonl"
DEFAULT_PROOFS_JSON = PROJECT_ROOT / "data" / "processed" / "proofs_with_key_strategies.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def make_backup(path: Path, label: str = "reverse_engineer_strategies") -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = path.with_name(f"{path.name}.bak_{label}_{stamp}")
    shutil.copy2(path, backup)
    return backup


def write_json_mirror(path: Path, records: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(records, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def strip_json_fence(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped)
        stripped = re.sub(r"\s*```$", "", stripped)
    return stripped.strip()


def normalize_category(category: str, category_names: List[str]) -> tuple[str, bool]:
    """Return an exact category name if possible, plus exact-match flag."""
    category = str(category or "").strip()
    if not category_names:
        return category, False
    if category in category_names:
        return category, True

    lower_map = {name.lower(): name for name in category_names}
    if category.lower() in lower_map:
        return lower_map[category.lower()], True

    # Try prefix/contains matching only as a soft repair for minor model formatting.
    for name in category_names:
        if category.lower() in name.lower() or name.lower() in category.lower():
            return name, False

    return category, False


def parse_refined_response(raw: str, category_names: List[str]) -> List[Dict[str, Any]]:
    text = strip_json_fence(raw)
    try:
        parsed = json.loads(text)
    except Exception:
        return [
            {
                "category": "UNPARSED_RESPONSE",
                "evidence": "The LLM response could not be parsed as JSON.",
                "explanation": raw.strip(),
                "confidence": "low",
                "category_name_match": False,
                "raw_response": raw,
            }
        ]

    if isinstance(parsed, dict):
        if isinstance(parsed.get("strategies_refined"), list):
            items = parsed["strategies_refined"]
        elif isinstance(parsed.get("categories"), list):
            items = parsed["categories"]
        else:
            items = [parsed]
    elif isinstance(parsed, list):
        items = parsed
    else:
        items = []

    results: List[Dict[str, Any]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        category, exact = normalize_category(str(item.get("category", "")), category_names)
        results.append(
            {
                "category": category,
                "evidence": str(item.get("evidence", item.get("where", ""))).strip(),
                "explanation": str(item.get("explanation", item.get("reason", ""))).strip(),
                "confidence": str(item.get("confidence", "medium")).strip().lower(),
                "category_name_match": exact,
                "raw_category": str(item.get("category", "")).strip(),
            }
        )

    if not results:
        return [
            {
                "category": "EMPTY_RESPONSE",
                "evidence": "No strategy category objects were found in the parsed response.",
                "explanation": raw.strip(),
                "confidence": "low",
                "category_name_match": False,
                "raw_response": raw,
            }
        ]
    return results


def format_category_list(categories_text: str) -> str:
    return categories_text.strip()


def reverse_engineer_one_proof(
    *,
    proof: Dict[str, Any],
    categories_text: str,
    category_names: List[str],
    api_key: str,
    model: str,
    api_base: str,
    temperature: float,
    reasoning_effort: Optional[str],
    max_tokens: int,
) -> List[Dict[str, Any]]:
    system_prompt = (
        "You are a careful real-analysis proof analyst. Your task is to reverse-engineer "
        "which proof-strategy categories appear in a proof, using only the provided category taxonomy. "
        "Choose categories because they explain the mathematical proof, not because of superficial wording."
    )

    allowed_categories = "\n".join(f"- {name}" for name in category_names)
    plain_english = proof.get("textbook_explanation") or proof.get("plain_english") or ""

    user_prompt = f"""
You are given one processed Lean theorem/lemma and a fixed strategy category taxonomy.

Your job:
1. Read the theorem comment, formal statement, and textbook-style English proof explanation.
2. Pick the strategy category/categories from the taxonomy that likely appear in this proof.
3. For each chosen category, explain which step or part of the proof corresponds to that category.
4. Use exact category names from the allowed list whenever possible.
5. Do not invent new categories unless no listed category fits; if you must invent one, make confidence low.
6. Do not over-classify routine wording: only include categories that genuinely help explain how the proof works.

CATEGORY TAXONOMY:
{format_category_list(categories_text)}

ALLOWED CATEGORY NAMES:
{allowed_categories}

PROOF RECORD:
Lean name: {proof.get('lean_name')}
Proof id: {proof.get('proof_id')}

Comment before theorem:
{proof.get('comment') or '[No comment provided]'}

Formal statement:
{proof.get('formal_statement') or '[No formal statement provided]'}

Textbook-style English proof explanation:
{plain_english or '[No textbook explanation provided]'}

Return strict JSON only in this exact shape:
{{
  "strategies_refined": [
    {{
      "category": "<exact category name from allowed list>",
      "evidence": "<which step/part of the proof shows this category>",
      "explanation": "<why this category is relevant to the proof>",
      "confidence": "high|medium|low"
    }}
  ]
}}
""".strip()

    raw = call_openai_chat(
        api_key=api_key,
        model=model,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        api_base=api_base,
        temperature=temperature,
        max_completion_tokens=max_tokens,
        reasoning_effort=reasoning_effort,
    )
    return parse_refined_response(raw, category_names)


def needs_refinement(proof: Dict[str, Any]) -> bool:
    value = proof.get("strategies_refined")
    return not (isinstance(value, list) and len(value) > 0)


def run_workflow(
    *,
    proofs_jsonl: Path,
    proofs_json: Path,
    categories_path: Path,
    until_proof: int,
    api_key: str,
    model: str,
    api_base: str,
    temperature: float,
    reasoning_effort: Optional[str],
    max_tokens: int,
    resume: bool,
    dry_run: bool,
) -> None:
    proofs = read_jsonl(proofs_jsonl)
    if not proofs:
        raise RuntimeError(f"No proof records found in {proofs_jsonl}")
    if until_proof <= 0:
        raise ValueError("--until-proof must be positive")
    if until_proof > len(proofs):
        raise ValueError(f"--until-proof={until_proof} exceeds available proof records: {len(proofs)}")
    if not categories_path.exists():
        raise FileNotFoundError(
            f"Category taxonomy not found: {categories_path}\n"
            "Run Stage 1 first: .venv/bin/python workflows/proof_strategy_extraction/categorize_strategy_library.py"
        )

    categories_text = categories_path.read_text(encoding="utf-8")
    category_names = parse_category_names(categories_text)
    selected = proofs[:until_proof]
    pending = [p for p in selected if (needs_refinement(p) or not resume)]

    print(f"Loaded {len(proofs)} proof records from {proofs_jsonl}")
    print(f"Loaded category taxonomy from {categories_path}")
    print(f"Parsed {len(category_names)} category names")
    print(f"Selected proofs: 1..{until_proof}")
    print(f"Pending refinements: {len(pending)}")

    if dry_run:
        for i, proof in enumerate(selected, start=1):
            status = "pending" if (needs_refinement(proof) or not resume) else "already refined"
            print(f"  proof #{i}: {proof.get('lean_name')} — {status}")
        print("Dry run: no API calls and no file writes.")
        return

    if not pending:
        print("No pending proofs to refine in selected range; nothing to do.")
        return

    backup = make_backup(proofs_jsonl)
    print(f"Backup written: {backup}")

    total = len(pending)
    processed = 0
    for proof_index, proof in enumerate(selected, start=1):
        if resume and not needs_refinement(proof):
            print(f"Skipping proof #{proof_index}: {proof.get('lean_name')} already has strategies_refined")
            continue

        processed += 1
        print(f"[{processed}/{total}] Reverse-engineering strategies for proof #{proof_index}: {proof.get('lean_name')}")
        refined = reverse_engineer_one_proof(
            proof=proof,
            categories_text=categories_text,
            category_names=category_names,
            api_key=api_key,
            model=model,
            api_base=api_base,
            temperature=temperature,
            reasoning_effort=reasoning_effort,
            max_tokens=max_tokens,
        )
        proof["strategies_refined"] = refined
        proof["strategies_refined_model"] = model
        proof["strategies_refined_at"] = now_iso()
        proof["strategies_refined_source"] = "reverse_engineered_from_formal_statement_comment_plain_english"

        # Save after each proof so the workflow can resume safely.
        write_jsonl(proofs_jsonl, proofs)
        write_json_mirror(proofs_json, proofs)

    write_jsonl(proofs_jsonl, proofs)
    write_json_mirror(proofs_json, proofs)
    print(f"Done. Updated {processed} proof records with strategies_refined.")
    print(f"Updated JSONL: {proofs_jsonl}")
    print(f"Updated JSON mirror: {proofs_json}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Reverse-engineer likely strategy categories for each proof and store them as strategies_refined."
    )
    parser.add_argument(
        "--until-proof",
        type=int,
        required=True,
        help="Process/refine proofs from item #1 through this proof number.",
    )
    parser.add_argument("--proofs-jsonl", type=Path, default=DEFAULT_PROOFS_JSONL)
    parser.add_argument("--proofs-json", type=Path, default=DEFAULT_PROOFS_JSON)
    parser.add_argument("--categories", type=Path, default=DEFAULT_CATEGORIES_OUTPUT)
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
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()

    if not args.dry_run and (not api_key or api_key == "your-openai-api-key-here"):
        raise RuntimeError("OPENAI_API_KEY is missing or still set to the placeholder. Put a real key in .env or export it.")

    run_workflow(
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
