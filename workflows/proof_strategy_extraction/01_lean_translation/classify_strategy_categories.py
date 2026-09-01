#!/usr/bin/env python3
"""
Stage 2: classify extracted proof strategies into an existing category taxonomy.

This script assumes Stage 1 has already been run by:

    python workflows/proof_strategy_extraction/categorize_strategy_library.py

Stage 1 produces:
    data/processed/strategy_category_notes.txt
    data/processed/strategy_categories.txt
    data/processed/strategy_categories_raw.txt

This script reads:
    data/processed/strategy_library.json
    data/processed/strategy_category_notes.txt
    data/processed/strategy_categories.txt

and writes:
    data/processed/strategy_category_assignments.json
    data/processed/strategy_category_assignments.csv
    data/processed/strategy_category_assignments.md

Run from project root:
    python workflows/proof_strategy_extraction/classify_strategy_categories.py

Useful test run:
    python workflows/proof_strategy_extraction/classify_strategy_categories.py --limit 10

Redo classifications without regenerating the category taxonomy:
    python workflows/proof_strategy_extraction/classify_strategy_categories.py --redo-assignments
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from run_pipeline import read_jsonl, write_jsonl

from categorize_strategy_library import (
    DEFAULT_ASSIGNMENTS_CSV,
    DEFAULT_ASSIGNMENTS_JSON,
    DEFAULT_ASSIGNMENTS_MD,
    DEFAULT_CATEGORIES_OUTPUT,
    DEFAULT_INPUT,
    DEFAULT_NOTES_OUTPUT,
    call_openai_chat,  # imported so this file documents its dependency path; classify_strategy uses it internally
    classify_strategy,
    load_dotenv,
    parse_category_names,
    read_existing_assignments,
    read_strategy_library,
    write_assignments_csv,
    write_assignments_json,
    write_assignments_md,
)

# Silence linters about the imported API helper being intentionally available through this module.
_ = call_openai_chat

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PROOFS_JSONL = PROJECT_ROOT / "data" / "processed" / "proofs_with_key_strategies.jsonl"
DEFAULT_PROOFS_JSON = PROJECT_ROOT / "data" / "processed" / "proofs_with_key_strategies.json"


def make_backup(path: Path, label: str = "classify_strategy_categories") -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = path.with_name(f"{path.name}.bak_{label}_{stamp}")
    shutil.copy2(path, backup)
    return backup


def write_json_mirror(path: Path, records: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(records, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def strategy_needs_category(strategy_obj: Any) -> bool:
    return isinstance(strategy_obj, dict) and not str(strategy_obj.get("category", "")).strip()


def split_enumerated_strategy_text(text: str) -> List[Dict[str, Any]]:
    """Convert numbered strategy text into structured strategy objects.

    Supports lines like:
      1. Strategy text
      2) Strategy text
    and keeps continuation lines attached to the current item.
    """
    raw = str(text or "").strip()
    if not raw:
        return []
    items: List[Dict[str, Any]] = []
    current_number: Optional[int] = None
    current_lines: List[str] = []

    def flush() -> None:
        nonlocal current_number, current_lines
        strategy = "\n".join(line.strip() for line in current_lines).strip()
        if strategy:
            n = current_number if current_number is not None else len(items) + 1
            items.append({
                "strategy_number": n,
                "strategy": strategy,
                "original_number": n,
                "category": "",
            })
        current_number = None
        current_lines = []

    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        m = re.match(r"^(\d+)\s*[\.)]\s+(.*)$", stripped)
        if m:
            flush()
            current_number = int(m.group(1))
            current_lines = [m.group(2)]
        else:
            current_lines.append(stripped)
    flush()

    if not items:
        items.append({
            "strategy_number": 1,
            "strategy": raw,
            "original_number": 1,
            "category": "",
        })
    return items


def normalize_proof_key_strategy_objects(proofs: List[Dict[str, Any]], until_proof: Optional[int]) -> int:
    """Ensure selected proofs store key_strategies as list objects.

    Returns number of proof records converted from plain text to list objects.
    """
    selected_count = until_proof if until_proof is not None else len(proofs)
    converted = 0
    for proof in proofs[:selected_count]:
        strategies = proof.get("key_strategies")
        if isinstance(strategies, list):
            continue
        if isinstance(strategies, str) and strategies.strip():
            proof["key_strategies_original_text"] = strategies
            proof["key_strategies"] = split_enumerated_strategy_text(strategies)
            proof["key_strategies_schema"] = "list[{strategy_number:int,strategy:str,original_number:int,category:str}]"
            converted += 1
    return converted


def count_strategy_categories_in_proofs(proofs: List[Dict[str, Any]], until_proof: Optional[int] = None) -> Dict[str, int]:
    selected = proofs[:until_proof] if until_proof is not None else proofs
    total = 0
    categorized = 0
    pending = 0
    for proof in selected:
        strategies = proof.get("key_strategies")
        if not isinstance(strategies, list):
            continue
        for strategy_obj in strategies:
            if not isinstance(strategy_obj, dict):
                continue
            total += 1
            if str(strategy_obj.get("category", "")).strip():
                categorized += 1
            else:
                pending += 1
    return {"total": total, "categorized": categorized, "pending": pending}


def classify_proof_strategy_objects(
    *,
    proofs_jsonl: Path,
    proofs_json: Path,
    until_proof: int,
    categories_text: str,
    category_names: List[str],
    notes: str,
    api_key: str,
    model: str,
    api_base: str,
    temperature: float,
    reasoning_effort: Optional[str],
    max_tokens: int,
    dry_run: bool = False,
) -> None:
    """Classify empty `category` fields in proof key_strategy objects through proof #until_proof."""
    proofs = read_jsonl(proofs_jsonl)
    if not proofs:
        raise RuntimeError(f"No proof records found in {proofs_jsonl}")
    if until_proof <= 0:
        raise ValueError("until_proof must be positive")
    if until_proof > len(proofs):
        raise ValueError(f"until_proof={until_proof} exceeds available processed proofs: {len(proofs)}")

    converted = normalize_proof_key_strategy_objects(proofs, until_proof)
    counts = count_strategy_categories_in_proofs(proofs, until_proof)
    print(
        f"Proof-category mode: selected proofs 1..{until_proof}; "
        f"strategies={counts['total']}, categorized={counts['categorized']}, pending={counts['pending']}, "
        f"converted_from_text={converted}"
    )

    if dry_run:
        for proof_index, proof in enumerate(proofs[:until_proof], start=1):
            pending_here = sum(1 for s in proof.get("key_strategies", []) if strategy_needs_category(s)) if isinstance(proof.get("key_strategies"), list) else 0
            print(f"  proof #{proof_index}: {proof.get('lean_name')} pending strategies={pending_here}")
        print("Dry run: no API calls and no proof file writes.")
        return

    if counts["pending"] == 0:
        print("No pending strategy categories in selected proof range; nothing to do.")
        return

    backup = make_backup(proofs_jsonl, "proof_strategy_category_classification")
    print(f"Backup written: {backup}")
    if converted:
        write_jsonl(proofs_jsonl, proofs)
        write_json_mirror(proofs_json, proofs)
        print(f"Converted {converted} proof records from numbered strategy text to structured strategy objects.")

    total_pending = counts["pending"]
    done = 0
    synthetic_id = 0
    for prior_proof in proofs:
        strategies = prior_proof.get("key_strategies")
        if isinstance(strategies, list):
            synthetic_id += len([s for s in strategies if isinstance(s, dict)])

    # Use stable synthetic ids based on proof index and strategy number for prompts/traceability.
    for proof_index, proof in enumerate(proofs[:until_proof], start=1):
        strategies = proof.get("key_strategies")
        if not isinstance(strategies, list):
            continue
        for strategy_obj in strategies:
            if not strategy_needs_category(strategy_obj):
                continue
            done += 1
            strategy_number = strategy_obj.get("strategy_number") or strategy_obj.get("original_number") or done
            strategy_id = int(f"{proof_index}{int(strategy_number):03d}") if str(strategy_number).isdigit() else done
            print(f"[{done}/{total_pending}] Classifying proof #{proof_index} {proof.get('lean_name')} strategy {strategy_number}...")
            strategy_record = {
                "strategy_id": strategy_id,
                "strategy": strategy_obj.get("strategy", ""),
                "source_proof_id": proof.get("proof_id"),
                "source_lean_name": proof.get("lean_name"),
                "source_strategy_number": strategy_number,
                "source_file": proof.get("source_file"),
                "formal_statement": proof.get("formal_statement"),
            }
            assignment = classify_strategy(
                strategy=strategy_record,
                categories_text=categories_text,
                category_names=category_names,
                notes=notes,
                api_key=api_key,
                model=model,
                api_base=api_base,
                temperature=temperature,
                reasoning_effort=reasoning_effort,
                max_tokens=max_tokens,
            )
            strategy_obj["category"] = str(assignment.get("category") or "").strip()
            strategy_obj["category_reason"] = assignment.get("reason")
            strategy_obj["category_name_match"] = assignment.get("category_name_match")
            strategy_obj["category_classified_at"] = datetime.utcnow().isoformat() + "Z"
            # Save after every strategy so this can resume safely.
            write_jsonl(proofs_jsonl, proofs)
            write_json_mirror(proofs_json, proofs)

    write_jsonl(proofs_jsonl, proofs)
    write_json_mirror(proofs_json, proofs)
    final_counts = count_strategy_categories_in_proofs(proofs, until_proof)
    print(
        f"Done updating proof strategy categories through proof #{until_proof}. "
        f"categorized={final_counts['categorized']}/{final_counts['total']}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Stage 2 only: classify each extracted strategy into an existing category taxonomy."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help=f"Input strategy library JSON. Default: {DEFAULT_INPUT}")
    parser.add_argument("--model", default="gpt-5.6-sol", help="OpenAI model. Default: gpt-5.6-sol")
    parser.add_argument("--api-base", default="https://api.openai.com/v1", help="OpenAI-compatible API base URL.")
    parser.add_argument("--temperature", type=float, default=1.0, help="Sampling temperature. Some models only support 1.0.")
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
        help="Max completion tokens for each classification call.",
    )
    parser.add_argument("--limit", type=int, default=None, help="For testing: classify only the first N strategies in standalone strategy-library mode.")
    parser.add_argument(
        "--until-proof",
        type=int,
        default=None,
        help="Proof-record mode: classify empty category fields for all key_strategies through proof item N in proofs_with_key_strategies.jsonl.",
    )
    parser.add_argument("--proofs-jsonl", type=Path, default=DEFAULT_PROOFS_JSONL, help=f"Proof records JSONL. Default: {DEFAULT_PROOFS_JSONL}")
    parser.add_argument("--proofs-json", type=Path, default=DEFAULT_PROOFS_JSON, help=f"Proof records JSON mirror. Default: {DEFAULT_PROOFS_JSON}")
    parser.add_argument(
        "--redo-assignments",
        action="store_true",
        help="Ignore existing assignment outputs and redo classification, while keeping the existing category taxonomy.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Load inputs and print what would happen, but do not call the API.")
    parser.add_argument("--notes", type=Path, default=DEFAULT_NOTES_OUTPUT, help="Stage 1 notes file.")
    parser.add_argument("--categories", type=Path, default=DEFAULT_CATEGORIES_OUTPUT, help="Stage 1 category list file.")
    parser.add_argument("--assignments-json", type=Path, default=DEFAULT_ASSIGNMENTS_JSON)
    parser.add_argument("--assignments-csv", type=Path, default=DEFAULT_ASSIGNMENTS_CSV)
    parser.add_argument("--assignments-md", type=Path, default=DEFAULT_ASSIGNMENTS_MD)
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()

    strategies: List[Dict[str, Any]] = []
    strategies_to_classify: List[Dict[str, Any]] = []
    if args.until_proof is None:
        strategies = read_strategy_library(args.input)
        if args.limit is not None:
            strategies_to_classify = strategies[: args.limit]
        else:
            strategies_to_classify = strategies

    if not args.categories.exists():
        raise FileNotFoundError(
            f"Category list not found: {args.categories}\n"
            "Run Stage 1 first: python workflows/proof_strategy_extraction/categorize_strategy_library.py"
        )
    categories_text = args.categories.read_text(encoding="utf-8")
    notes = args.notes.read_text(encoding="utf-8") if args.notes.exists() else ""
    category_names = parse_category_names(categories_text)

    if args.until_proof is None:
        print(f"Loaded {len(strategies)} strategies from {args.input}")
    else:
        print("Proof-record mode: using key_strategies objects from proofs_with_key_strategies.jsonl")
    print(f"Loaded category taxonomy from {args.categories}")
    print(f"Parsed {len(category_names)} category names")

    if args.until_proof is not None:
        print(f"Proof-record mode: will classify strategy objects through proof #{args.until_proof}")
        if args.dry_run:
            classify_proof_strategy_objects(
                proofs_jsonl=args.proofs_jsonl,
                proofs_json=args.proofs_json,
                until_proof=args.until_proof,
                categories_text=categories_text,
                category_names=category_names,
                notes=notes,
                api_key=api_key,
                model=args.model,
                api_base=args.api_base,
                temperature=args.temperature,
                reasoning_effort=args.reasoning_effort,
                max_tokens=args.classification_max_tokens,
                dry_run=True,
            )
            return
        if not api_key or api_key == "your-openai-api-key-here":
            raise RuntimeError("OPENAI_API_KEY is missing or still set to the placeholder. Put a real key in .env or export it.")
        classify_proof_strategy_objects(
            proofs_jsonl=args.proofs_jsonl,
            proofs_json=args.proofs_json,
            until_proof=args.until_proof,
            categories_text=categories_text,
            category_names=category_names,
            notes=notes,
            api_key=api_key,
            model=args.model,
            api_base=args.api_base,
            temperature=args.temperature,
            reasoning_effort=args.reasoning_effort,
            max_tokens=args.classification_max_tokens,
            dry_run=False,
        )
        return

    print(f"Will classify {len(strategies_to_classify)} strategies")

    if args.dry_run:
        print("Dry run: no API calls will be made and no assignment files will be written.")
        print("First few categories:")
        for name in category_names[:10]:
            print(f"  - {name}")
        print("First few strategies:")
        for item in strategies_to_classify[:5]:
            print(f"  {item.get('strategy_id')}. {item.get('strategy')}")
        return

    if not api_key or api_key == "your-openai-api-key-here":
        raise RuntimeError("OPENAI_API_KEY is missing or still set to the placeholder. Put a real key in .env or export it.")

    if not category_names:
        print("Warning: could not parse category names from category list. Classification may not match names exactly.")

    existing = {} if args.redo_assignments else read_existing_assignments(args.assignments_json)
    assignments_by_id: Dict[int, Dict[str, Any]] = dict(existing)

    for idx, strategy in enumerate(strategies_to_classify, start=1):
        sid = int(strategy.get("strategy_id"))
        if sid in assignments_by_id:
            print(
                f"[{idx}/{len(strategies_to_classify)}] Strategy {sid}: "
                f"already classified as {assignments_by_id[sid].get('category')}"
            )
            continue

        print(f"[{idx}/{len(strategies_to_classify)}] Classifying strategy {sid}...")
        assignment = classify_strategy(
            strategy=strategy,
            categories_text=categories_text,
            category_names=category_names,
            notes=notes,
            api_key=api_key,
            model=args.model,
            api_base=args.api_base,
            temperature=args.temperature,
            reasoning_effort=args.reasoning_effort,
            max_tokens=args.classification_max_tokens,
        )
        assignments_by_id[sid] = assignment

        # Save after every strategy so the script can resume safely.
        sorted_assignments = [assignments_by_id[k] for k in sorted(assignments_by_id)]
        write_assignments_json(args.assignments_json, sorted_assignments, categories_text, notes)
        write_assignments_csv(args.assignments_csv, sorted_assignments)
        write_assignments_md(args.assignments_md, sorted_assignments, categories_text, notes)

    final_assignments = [assignments_by_id[k] for k in sorted(assignments_by_id)]
    write_assignments_json(args.assignments_json, final_assignments, categories_text, notes)
    write_assignments_csv(args.assignments_csv, final_assignments)
    write_assignments_md(args.assignments_md, final_assignments, categories_text, notes)

    print("Done.")
    print(f"Assignments JSON: {args.assignments_json}")
    print(f"Assignments CSV: {args.assignments_csv}")
    print(f"Assignments Markdown: {args.assignments_md}")


if __name__ == "__main__":
    main()
