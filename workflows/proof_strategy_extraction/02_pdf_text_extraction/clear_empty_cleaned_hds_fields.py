#!/usr/bin/env python3
"""Clear empty HDS cleaned-text fields so cleanup workflow retries them."""

from __future__ import annotations

import argparse
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from clean_hds_pdf_text import INPUT_JSON, INPUT_JSONL, PROJECT_ROOT, read_json_records, write_json, write_jsonl


def main() -> None:
    parser = argparse.ArgumentParser(description="Clear empty cleaned HDS text fields so they can be regenerated.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    records = read_json_records(INPUT_JSONL)
    changed = 0
    cleared_fields = 0
    for rec in records:
        rec_changed = False
        raw_statement = str(rec.get("plain_english_statement", "")).strip()
        raw_proof = str(rec.get("plain_english_proof", "")).strip()

        if raw_statement and "plain_english_statement_cleaned" in rec and not str(rec.get("plain_english_statement_cleaned", "")).strip():
            del rec["plain_english_statement_cleaned"]
            rec_changed = True
            cleared_fields += 1
        if raw_proof and "plain_english_proof_cleaned" in rec and not str(rec.get("plain_english_proof_cleaned", "")).strip():
            del rec["plain_english_proof_cleaned"]
            rec_changed = True
            cleared_fields += 1

        if rec_changed:
            changed += 1

    print(f"Records read: {len(records)}")
    print(f"Records changed: {changed}")
    print(f"Empty cleaned fields cleared: {cleared_fields}")

    if args.dry_run:
        print("Dry run: no files written.")
        return

    if changed:
        backup = INPUT_JSONL.with_name(INPUT_JSONL.name + f".bak_clear_empty_cleaned_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        shutil.copy2(INPUT_JSONL, backup)
        print(f"Backup written: {backup.relative_to(PROJECT_ROOT)}")
        write_jsonl(INPUT_JSONL, records)
        write_json(INPUT_JSON, records)
        print(f"Updated: {INPUT_JSONL.relative_to(PROJECT_ROOT)}")
        print(f"Updated: {INPUT_JSON.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
