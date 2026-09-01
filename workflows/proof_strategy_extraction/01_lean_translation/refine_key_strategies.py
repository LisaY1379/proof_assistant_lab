#!/usr/bin/env python3
"""
Refine `key_strategies` inside proofs_with_key_strategies.jsonl.

Goal:
    Convert a numbered text block like:

        "key_strategies": "1. Use compactness...\n2. Rewrite the metric..."

    into a structured list of independent strategy objects:

        "key_strategies": [
          {"strategy_number": 1, "strategy": "Use compactness..."},
          {"strategy_number": 2, "strategy": "Rewrite the metric..."}
        ]

The script preserves the original text in `key_strategies_original_text` by default.
It also makes a timestamped backup before overwriting the input file.

Run from project root:
    .venv/bin/python workflows/proof_strategy_extraction/refine_key_strategies.py

Preview without writing:
    .venv/bin/python workflows/proof_strategy_extraction/refine_key_strategies.py --dry-run

Force conversion even if `key_strategies` is already a list:
    .venv/bin/python workflows/proof_strategy_extraction/refine_key_strategies.py --force
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

# Reuse the pipeline's robust pretty-JSONL reader/writer.
from run_pipeline import read_jsonl, write_jsonl

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = PROJECT_ROOT / "data" / "processed" / "proofs_with_key_strategies.jsonl"
DEFAULT_JSON_MIRROR = PROJECT_ROOT / "data" / "processed" / "proofs_with_key_strategies.json"

# Matches numbered items such as:
#   1. First strategy
#   2) Second strategy
# and captures multi-line bodies until the next numbered item.
NUMBERED_ITEM_RE = re.compile(r"(?ms)^\s*(\d+)[\.)]\s+(.*?)(?=^\s*\d+[\.)]\s+|\Z)")

# Removes accidental numbering/bullet leftovers after splitting.
LEADING_MARKER_RE = re.compile(r"^\s*(?:\d+[\.)]|[-*•])\s+")


def clean_strategy_text(text: str) -> str:
    """Normalize one strategy item's text without destroying mathematical content."""
    text = text.strip()
    text = LEADING_MARKER_RE.sub("", text).strip()
    # Collapse spaces/tabs while preserving line breaks if the strategy has displayed math.
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.splitlines()]
    # Remove empty edge lines, but keep intentional internal non-empty lines.
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines).strip()


def split_key_strategies(raw: str) -> List[Dict[str, Any]]:
    """Split a numbered key_strategies string into structured strategy objects."""
    if not raw or not raw.strip():
        return []

    raw = raw.strip()
    matches = list(NUMBERED_ITEM_RE.finditer(raw))

    items: List[Tuple[int, str]] = []
    if matches:
        for fallback_index, match in enumerate(matches, start=1):
            try:
                original_number = int(match.group(1))
            except ValueError:
                original_number = fallback_index
            items.append((original_number, match.group(2)))
    else:
        # Fallback for non-numbered output: each non-empty line becomes a strategy.
        for fallback_index, line in enumerate(raw.splitlines(), start=1):
            if line.strip():
                items.append((fallback_index, line))

    strategies: List[Dict[str, Any]] = []
    for global_index, (original_number, item_text) in enumerate(items, start=1):
        cleaned = clean_strategy_text(item_text)
        if not cleaned:
            continue
        strategies.append(
            {
                "strategy_number": len(strategies) + 1,
                "strategy": cleaned,
                "original_number": original_number,
            }
        )

    return strategies


def refine_record(record: Dict[str, Any], *, force: bool = False, keep_original: bool = True) -> Tuple[Dict[str, Any], bool, str]:
    """Return refined record, changed flag, and a short status string."""
    refined = dict(record)
    value = refined.get("key_strategies")

    if isinstance(value, list):
        if not force:
            return refined, False, "already_structured"
        # If forcing, reconstruct from original text if available; otherwise normalize list items.
        original_text = refined.get("key_strategies_original_text")
        if isinstance(original_text, str) and original_text.strip():
            strategies = split_key_strategies(original_text)
        else:
            strategies = []
            for idx, item in enumerate(value, start=1):
                if isinstance(item, dict):
                    text = str(item.get("strategy", "")).strip()
                    original_number = item.get("original_number", item.get("strategy_number", idx))
                else:
                    text = str(item).strip()
                    original_number = idx
                if text:
                    strategies.append(
                        {
                            "strategy_number": len(strategies) + 1,
                            "strategy": clean_strategy_text(text),
                            "original_number": original_number,
                        }
                    )
    elif isinstance(value, str):
        original_text = value
        strategies = split_key_strategies(value)
        if keep_original and "key_strategies_original_text" not in refined:
            refined["key_strategies_original_text"] = original_text
    elif value is None:
        strategies = []
    else:
        original_text = str(value)
        strategies = split_key_strategies(original_text)
        if keep_original and "key_strategies_original_text" not in refined:
            refined["key_strategies_original_text"] = original_text

    refined["key_strategies"] = strategies
    refined["key_strategies_refined_at"] = datetime.now(timezone.utc).isoformat()
    refined["key_strategies_schema"] = "list[{strategy_number:int,strategy:str,original_number:int}]"

    return refined, True, f"structured_{len(strategies)}"


def write_json_mirror(path: Path, records: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(records, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def make_backup(path: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = path.with_name(f"{path.name}.bak_refine_key_strategies_{stamp}")
    shutil.copy2(path, backup)
    return backup


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert numbered key_strategies text into structured strategy objects.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help=f"Input/output proof JSONL file. Default: {DEFAULT_INPUT}")
    parser.add_argument("--json-mirror", type=Path, default=DEFAULT_JSON_MIRROR, help=f"Optional JSON array mirror. Default: {DEFAULT_JSON_MIRROR}")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing files.")
    parser.add_argument("--force", action="store_true", help="Rebuild key_strategies even if already structured as a list.")
    parser.add_argument("--no-backup", action="store_true", help="Do not create a backup before writing. Not recommended.")
    parser.add_argument("--no-original", action="store_true", help="Do not preserve the old string in key_strategies_original_text.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = args.input

    records = read_jsonl(input_path)
    if not records:
        raise SystemExit(f"No records found in {input_path}")

    refined_records: List[Dict[str, Any]] = []
    changed_count = 0
    total_strategy_objects = 0
    status_counts: Dict[str, int] = {}

    for record in records:
        refined, changed, status = refine_record(
            record,
            force=args.force,
            keep_original=not args.no_original,
        )
        refined_records.append(refined)
        if changed:
            changed_count += 1
        status_counts[status] = status_counts.get(status, 0) + 1
        ks = refined.get("key_strategies")
        if isinstance(ks, list):
            total_strategy_objects += len(ks)

    print(f"Read records: {len(records)}")
    print(f"Records changed: {changed_count}")
    print(f"Total strategy objects after refinement: {total_strategy_objects}")
    print("Status counts:")
    for status, count in sorted(status_counts.items()):
        print(f"  {status}: {count}")

    # Show a small preview.
    for record in refined_records[:3]:
        print("\n--- Preview ---")
        print(f"lean_name: {record.get('lean_name', '')}")
        print(json.dumps(record.get("key_strategies", []), ensure_ascii=False, indent=2))

    if args.dry_run:
        print("\nDry run only; no files written.")
        return

    if not args.no_backup:
        backup = make_backup(input_path)
        print(f"Backup written: {backup}")

    write_jsonl(input_path, refined_records)
    print(f"Updated: {input_path}")

    if args.json_mirror:
        write_json_mirror(args.json_mirror, refined_records)
        print(f"Updated JSON mirror: {args.json_mirror}")


if __name__ == "__main__":
    main()
