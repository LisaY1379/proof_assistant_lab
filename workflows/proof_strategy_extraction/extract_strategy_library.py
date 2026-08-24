#!/usr/bin/env python3
"""
Extract a standalone library of proof strategies from proofs_with_key_strategies.jsonl.

The input records contain a field like:

    "key_strategies": "1. First key idea...\n2. Second key idea..."

This script splits multiple strategies from each proof into separate items, removes the
local numbering, and enumerates the whole strategy library globally.

Default input:
    data/processed/proofs_with_key_strategies.jsonl

Default outputs:
    data/processed/strategy_library.json
    data/processed/strategy_library.md
    data/processed/strategy_library.csv

Run from project root:
    python workflows/proof_strategy_extraction/extract_strategy_library.py
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = PROJECT_ROOT / "data" / "processed" / "proofs_with_key_strategies.jsonl"
DEFAULT_JSON_OUTPUT = PROJECT_ROOT / "data" / "processed" / "strategy_library.json"
DEFAULT_MD_OUTPUT = PROJECT_ROOT / "data" / "processed" / "strategy_library.md"
DEFAULT_CSV_OUTPUT = PROJECT_ROOT / "data" / "processed" / "strategy_library.csv"

# Matches numbered strategy items such as:
#   1. Use compactness...
#   2) Rewrite the metric...
#   ③ Some unicode-like formats are not targeted here.
NUMBERED_ITEM_RE = re.compile(r"(?ms)^\s*(\d+)[\.)]\s+(.*?)(?=^\s*\d+[\.)]\s+|\Z)")


def read_records(path: Path) -> List[Dict[str, Any]]:
    """Read records from either normal JSON array, strict JSONL, or pretty JSONL.

    Earlier versions of the pipeline wrote one compact JSON object per line. Later
    versions may write pretty-printed multi-line JSON objects separated by newlines.
    This function tries all useful formats.
    """
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []

    # 1. JSON array or single JSON object.
    try:
        parsed = json.loads(text)
        if isinstance(parsed, list):
            return [x for x in parsed if isinstance(x, dict)]
        if isinstance(parsed, dict):
            return [parsed]
    except json.JSONDecodeError:
        pass

    # 2. Strict JSONL: one JSON object per line.
    records: List[Dict[str, Any]] = []
    strict_failed = False
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            if isinstance(obj, dict):
                records.append(obj)
        except json.JSONDecodeError:
            strict_failed = True
            break
    if records and not strict_failed:
        return records

    # 3. Pretty JSONL: multiple top-level JSON objects concatenated.
    decoder = json.JSONDecoder()
    idx = 0
    records = []
    length = len(text)
    while idx < length:
        while idx < length and text[idx].isspace():
            idx += 1
        if idx >= length:
            break
        obj, end = decoder.raw_decode(text, idx)
        if isinstance(obj, dict):
            records.append(obj)
        elif isinstance(obj, list):
            records.extend(x for x in obj if isinstance(x, dict))
        idx = end
    return records


def split_key_strategies(raw: str) -> List[str]:
    """Split a key_strategies string into individual unnumbered strategies."""
    if not raw or not raw.strip():
        return []

    raw = raw.strip()
    matches = list(NUMBERED_ITEM_RE.finditer(raw))
    if matches:
        items = [m.group(2).strip() for m in matches]
    else:
        # Fallback: split on non-empty lines if the model did not enumerate properly.
        items = [line.strip() for line in raw.splitlines() if line.strip()]

    cleaned: List[str] = []
    for item in items:
        # Remove accidental remaining leading numbering/bullets.
        item = re.sub(r"^\s*\d+[\.)]\s+", "", item).strip()
        item = re.sub(r"^\s*[-*•]\s+", "", item).strip()
        # Collapse internal whitespace but preserve readable math text.
        item = re.sub(r"[ \t]+", " ", item)
        if item:
            cleaned.append(item)
    return cleaned


def build_strategy_library(records: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    library: List[Dict[str, Any]] = []

    for record in records:
        strategies = split_key_strategies(str(record.get("key_strategies", "")))
        proof_id = record.get("proof_id", "")
        lean_name = record.get("lean_name", "")
        source_file = record.get("source_file", "")
        formal_statement = record.get("formal_statement", "")
        comment = record.get("comment", "")

        for local_index, strategy in enumerate(strategies, start=1):
            library.append(
                {
                    "strategy_id": len(library) + 1,
                    "strategy": strategy,
                    "source_proof_id": proof_id,
                    "source_lean_name": lean_name,
                    "source_strategy_number": local_index,
                    "source_file": source_file,
                    "formal_statement": formal_statement,
                    "comment": comment,
                }
            )

    return library


def write_json(path: Path, library: List[Dict[str, Any]], source_path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_file": str(source_path.relative_to(PROJECT_ROOT) if source_path.is_relative_to(PROJECT_ROOT) else source_path),
        "strategy_count": len(library),
        "strategies": library,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_markdown(path: Path, library: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: List[str] = []
    lines.append("# Proof Strategy Library")
    lines.append("")
    lines.append(f"Generated at: {datetime.now(timezone.utc).isoformat()}")
    lines.append(f"Total strategies: {len(library)}")
    lines.append("")

    for item in library:
        lines.append(f"## {item['strategy_id']}. {item['strategy']}")
        lines.append("")
        lines.append(f"- Source theorem/lemma: `{item.get('source_lean_name', '')}`")
        lines.append(f"- Source proof id: `{item.get('source_proof_id', '')}`")
        lines.append(f"- Source strategy number in proof: {item.get('source_strategy_number', '')}")
        if item.get("source_file"):
            lines.append(f"- Source file: `{item['source_file']}`")
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def write_csv(path: Path, library: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "strategy_id",
        "strategy",
        "source_proof_id",
        "source_lean_name",
        "source_strategy_number",
        "source_file",
        "formal_statement",
        "comment",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in library:
            writer.writerow(item)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract a standalone library of key proof strategies.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help=f"Input processed proofs file. Default: {DEFAULT_INPUT}")
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON_OUTPUT, help=f"JSON output. Default: {DEFAULT_JSON_OUTPUT}")
    parser.add_argument("--md-output", type=Path, default=DEFAULT_MD_OUTPUT, help=f"Markdown output. Default: {DEFAULT_MD_OUTPUT}")
    parser.add_argument("--csv-output", type=Path, default=DEFAULT_CSV_OUTPUT, help=f"CSV output. Default: {DEFAULT_CSV_OUTPUT}")
    args = parser.parse_args()

    records = read_records(args.input)
    library = build_strategy_library(records)

    write_json(args.json_output, library, args.input)
    write_markdown(args.md_output, library)
    write_csv(args.csv_output, library)

    print(f"Read {len(records)} proof records from {args.input}")
    print(f"Extracted {len(library)} individual strategies")
    print(f"Wrote JSON: {args.json_output}")
    print(f"Wrote Markdown: {args.md_output}")
    print(f"Wrote CSV: {args.csv_output}")


if __name__ == "__main__":
    main()
