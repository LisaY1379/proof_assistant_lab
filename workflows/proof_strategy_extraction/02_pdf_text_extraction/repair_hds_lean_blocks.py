#!/usr/bin/env python3
"""Repair HDS library Lean blocks after declaration-boundary extraction fixes.

This updates only Lean-side metadata in
`data/high_dimensional_statistics/processed/proofs_with_key_strategies.jsonl`:

- comment
- lean_original_code
- formal_statement, if present in the library
- source/start/end/name fields, if present

It preserves PDF text, cleaned text, key strategies, and all other downstream
annotations.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import shutil
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from build_hds_library import (
    OUTPUT_JSON,
    OUTPUT_JSONL,
    extract_lean_declarations,
)


def format_json_record(row: Dict[str, Any]) -> str:
    return json.dumps(row, ensure_ascii=False, sort_keys=True, indent=2)


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            if count:
                f.write("\n")
            f.write(format_json_record(row) + "\n")
            count += 1
    return count


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []
    rows: List[Dict[str, Any]] = []
    buffer: List[str] = []
    depth = 0
    in_string = False
    escape = False
    for ch in text:
        buffer.append(ch)
        if escape:
            escape = False
            continue
        if ch == "\\" and in_string:
            escape = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                rec = "".join(buffer).strip()
                if rec:
                    rows.append(json.loads(rec))
                buffer = []
    return rows


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def make_backup(path: Path) -> Optional[Path]:
    if not path.exists():
        return None
    stamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = path.with_name(path.name + f".bak_repair_lean_blocks_{stamp}")
    shutil.copy2(path, backup)
    return backup


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Repair HDS Lean declaration blocks in the processed library.")
    p.add_argument("--library", type=Path, default=OUTPUT_JSONL)
    p.add_argument("--json-mirror", type=Path, default=OUTPUT_JSON)
    p.add_argument("--limit", type=int, default=None, help="Only compare/update first N records.")
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    records = read_jsonl(args.library)
    lean_decls = extract_lean_declarations(limit=args.limit)

    selected_count = min(len(records), len(lean_decls))
    if args.limit:
        selected_count = min(selected_count, args.limit)

    changed = 0
    trailing_comment_before = 0
    trailing_comment_after = 0

    for i in range(selected_count):
        rec = records[i]
        decl = lean_decls[i]
        old_code = str(rec.get("lean_original_code", ""))
        new_code = decl.lean_original_code
        if "/--" in old_code:
            trailing_comment_before += 1
        if "/--" in new_code:
            trailing_comment_after += 1
        if old_code != new_code or rec.get("comment", "") != decl.comment:
            changed += 1
            if not args.dry_run:
                rec["comment"] = decl.comment
                rec["lean_original_code"] = decl.lean_original_code
                if "formal_statement" in rec:
                    rec["formal_statement"] = decl.formal_statement
                if "lean_name" in rec:
                    rec["lean_name"] = decl.lean_name
                if "source_file" in rec:
                    rec["source_file"] = decl.source_file
                if "start_line" in rec:
                    rec["start_line"] = decl.start_line
                if "end_line" in rec:
                    rec["end_line"] = decl.end_line
                rec["lean_block_repaired_at"] = _dt.datetime.now(_dt.timezone.utc).isoformat()
                rec["lean_block_repair_note"] = "Removed trailing top-level context/doc comments from Lean declaration block."

    print(f"Library records: {len(records)}")
    print(f"Fresh Lean declarations: {len(lean_decls)}")
    print(f"Compared records: {selected_count}")
    print(f"Records whose old lean_original_code contained /--: {trailing_comment_before}")
    print(f"Records whose fresh lean_original_code contains /--: {trailing_comment_after}")
    print(f"Records to update: {changed}")

    if args.dry_run:
        print("Dry run: no files written.")
        return 0

    backup = make_backup(args.library)
    if backup:
        print(f"Backup created: {backup}")
    write_jsonl(args.library, records)
    if args.json_mirror:
        write_json(args.json_mirror, records)
    print(f"Updated {args.library}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
