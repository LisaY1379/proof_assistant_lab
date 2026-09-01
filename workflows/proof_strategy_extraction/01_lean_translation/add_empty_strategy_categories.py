#!/usr/bin/env python3
"""
Add an empty `category` field to every strategy object inside `key_strategies`.

Expected input shape after refine_key_strategies.py:

    "key_strategies": [
      {
        "strategy_number": 1,
        "strategy": "Use compactness...",
        "original_number": 1
      }
    ]

This script updates each strategy object to:

    {
      "strategy_number": 1,
      "strategy": "Use compactness...",
      "original_number": 1,
      "category": ""
    }

It preserves existing non-empty category values by default. Use --overwrite to reset
all categories to empty strings.

Run from project root:
    .venv/bin/python workflows/proof_strategy_extraction/add_empty_strategy_categories.py

Preview without writing:
    .venv/bin/python workflows/proof_strategy_extraction/add_empty_strategy_categories.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

from run_pipeline import read_jsonl, write_jsonl

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = PROJECT_ROOT / "data" / "processed" / "proofs_with_key_strategies.jsonl"
DEFAULT_JSON_MIRROR = PROJECT_ROOT / "data" / "processed" / "proofs_with_key_strategies.json"


def make_backup(path: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = path.with_name(f"{path.name}.bak_add_empty_strategy_categories_{stamp}")
    shutil.copy2(path, backup)
    return backup


def write_json_mirror(path: Path, records: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(records, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def add_category_fields(record: Dict[str, Any], *, overwrite: bool = False) -> Tuple[Dict[str, Any], int, int, str]:
    """Return updated record, added count, overwritten count, and status."""
    updated = dict(record)
    strategies = updated.get("key_strategies")

    if not isinstance(strategies, list):
        return updated, 0, 0, "key_strategies_not_list"

    new_strategies: List[Any] = []
    added_count = 0
    overwritten_count = 0

    for item in strategies:
        if not isinstance(item, dict):
            # Keep unexpected entries but do not try to modify them.
            new_strategies.append(item)
            continue

        new_item = dict(item)
        if "category" not in new_item:
            new_item["category"] = ""
            added_count += 1
        elif overwrite:
            if new_item.get("category") != "":
                overwritten_count += 1
            new_item["category"] = ""

        new_strategies.append(new_item)

    updated["key_strategies"] = new_strategies
    if added_count or overwritten_count:
        status = "updated"
    else:
        status = "already_has_category"
    return updated, added_count, overwritten_count, status


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Add an empty category field to each key_strategies object.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help=f"Input/output proof JSONL file. Default: {DEFAULT_INPUT}")
    parser.add_argument("--json-mirror", type=Path, default=DEFAULT_JSON_MIRROR, help=f"Optional JSON array mirror. Default: {DEFAULT_JSON_MIRROR}")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing files.")
    parser.add_argument("--overwrite", action="store_true", help="Reset existing category values to empty strings.")
    parser.add_argument("--no-backup", action="store_true", help="Do not create a backup before writing. Not recommended.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    records = read_jsonl(args.input)
    if not records:
        raise SystemExit(f"No records found in {args.input}")

    updated_records: List[Dict[str, Any]] = []
    total_added = 0
    total_overwritten = 0
    status_counts: Dict[str, int] = {}

    for record in records:
        updated, added, overwritten, status = add_category_fields(record, overwrite=args.overwrite)
        updated_records.append(updated)
        total_added += added
        total_overwritten += overwritten
        status_counts[status] = status_counts.get(status, 0) + 1

    print(f"Read records: {len(records)}")
    print(f"Category fields added: {total_added}")
    print(f"Category fields overwritten/reset: {total_overwritten}")
    print("Status counts:")
    for status, count in sorted(status_counts.items()):
        print(f"  {status}: {count}")

    for record in updated_records[:3]:
        print("\n--- Preview ---")
        print(f"lean_name: {record.get('lean_name', '')}")
        print(json.dumps(record.get("key_strategies", [])[:3], ensure_ascii=False, indent=2))

    if args.dry_run:
        print("\nDry run only; no files written.")
        return

    if not args.no_backup:
        backup = make_backup(args.input)
        print(f"Backup written: {backup}")

    write_jsonl(args.input, updated_records)
    print(f"Updated: {args.input}")

    if args.json_mirror:
        write_json_mirror(args.json_mirror, updated_records)
        print(f"Updated JSON mirror: {args.json_mirror}")


if __name__ == "__main__":
    main()
