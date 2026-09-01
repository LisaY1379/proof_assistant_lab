#!/usr/bin/env python3
"""Inspect HighDimensionalStatistics records missing book proof text.

This script separates records into:
  1. statement present but proof missing
  2. both statement and proof missing
  3. proof present but statement missing (rare diagnostic)
  4. both statement and proof present

It reads the HDS processed library and writes a JSON/Markdown/CSV report.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Dict, List

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_LIBRARY = PROJECT_ROOT / "data/high_dimensional_statistics/processed/proofs_with_key_strategies.jsonl"
DEFAULT_REPORT_JSON = PROJECT_ROOT / "data/high_dimensional_statistics/metadata/missing_book_text_report.json"
DEFAULT_REPORT_MD = PROJECT_ROOT / "data/high_dimensional_statistics/metadata/missing_book_text_report.md"
DEFAULT_REPORT_CSV = PROJECT_ROOT / "data/high_dimensional_statistics/metadata/missing_book_text_report.csv"


def read_json_records(path: Path) -> List[Dict[str, Any]]:
    """Read either strict JSONL, pretty-printed JSON objects, or JSON arrays."""
    if not path.exists():
        raise FileNotFoundError(f"Library file not found: {path}")
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []

    if text.startswith("["):
        data = json.loads(text)
        if not isinstance(data, list):
            raise ValueError(f"Expected JSON array in {path}")
        return [x for x in data if isinstance(x, dict)]

    records: List[Dict[str, Any]] = []
    decoder = json.JSONDecoder()
    idx = 0
    n = len(text)
    while idx < n:
        while idx < n and text[idx].isspace():
            idx += 1
        if idx >= n:
            break
        obj, end = decoder.raw_decode(text, idx)
        if isinstance(obj, dict):
            records.append(obj)
        idx = end
    return records


def has_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def first_text(record: Dict[str, Any], keys: List[str]) -> str:
    for key in keys:
        value = record.get(key)
        if has_text(value):
            return str(value).strip()
    return ""


def get_statement(record: Dict[str, Any]) -> str:
    return first_text(record, [
        "plain_english_statement_cleaned",
        "plain_english_statement",
        "plain_english",
    ])


def get_proof(record: Dict[str, Any]) -> str:
    return first_text(record, [
        "plain_english_proof_cleaned",
        "plain_english_proof",
    ])


def lean_name(record: Dict[str, Any]) -> str:
    value = record.get("lean_name") or record.get("official_lean_declaration") or record.get("book_name")
    if value:
        return str(value)
    code = str(record.get("lean_original_code", ""))
    # Small fallback: parse a declaration name from Lean code.
    import re
    m = re.search(r"\b(?:theorem|lemma|proposition|corollary)\s+([A-Za-z0-9_'.]+)", code)
    return m.group(1) if m else "(unnamed)"


def summarize_record(index: int, record: Dict[str, Any], category: str) -> Dict[str, Any]:
    statement = get_statement(record)
    proof = get_proof(record)
    return {
        "index": index,
        "category": category,
        "lean_name": lean_name(record),
        "book_name": record.get("book_name", ""),
        "kind": record.get("kind", ""),
        "location": record.get("location", ""),
        "source_file": record.get("source_file", ""),
        "official_lean_declaration": record.get("official_lean_declaration", ""),
        "plain_english_statement_len": len(statement),
        "plain_english_proof_len": len(proof),
        "statement_excerpt": statement[:240].replace("\n", " "),
        "comment_excerpt": str(record.get("comment", ""))[:240].replace("\n", " "),
    }


def write_reports(records: List[Dict[str, Any]], report_json: Path, report_md: Path, report_csv: Path) -> None:
    buckets = {
        "statement_but_no_proof": [],
        "neither_statement_nor_proof": [],
        "proof_but_no_statement": [],
        "both_statement_and_proof": [],
    }

    for i, record in enumerate(records, start=1):
        statement = get_statement(record)
        proof = get_proof(record)
        if statement and proof:
            category = "both_statement_and_proof"
        elif statement and not proof:
            category = "statement_but_no_proof"
        elif proof and not statement:
            category = "proof_but_no_statement"
        else:
            category = "neither_statement_nor_proof"
        buckets[category].append(summarize_record(i, record, category))

    summary = {
        "total_records": len(records),
        "both_statement_and_proof": len(buckets["both_statement_and_proof"]),
        "statement_but_no_proof": len(buckets["statement_but_no_proof"]),
        "proof_but_no_statement": len(buckets["proof_but_no_statement"]),
        "neither_statement_nor_proof": len(buckets["neither_statement_nor_proof"]),
    }

    payload = {"summary": summary, "records": buckets}
    report_json.parent.mkdir(parents=True, exist_ok=True)
    report_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# Missing HDS Book Text Report",
        "",
        "## Summary",
        "",
        f"- Total records: {summary['total_records']}",
        f"- Both statement and proof: {summary['both_statement_and_proof']}",
        f"- Statement but no proof: {summary['statement_but_no_proof']}",
        f"- Proof but no statement: {summary['proof_but_no_statement']}",
        f"- Neither statement nor proof: {summary['neither_statement_nor_proof']}",
        "",
    ]
    for category in ["statement_but_no_proof", "neither_statement_nor_proof", "proof_but_no_statement"]:
        items = buckets[category]
        lines.extend([f"## {category}", "", f"Count: {len(items)}", ""])
        if not items:
            lines.append("None.\n")
            continue
        for item in items:
            lines.extend([
                f"### {item['index']}. {item['lean_name']}",
                "",
                f"- Book name: {item['book_name'] or '—'}",
                f"- Kind: {item['kind'] or '—'}",
                f"- Location: {item['location'] or '—'}",
                f"- Official Lean declaration: {item['official_lean_declaration'] or '—'}",
                f"- Source file: `{item['source_file'] or '—'}`",
                f"- Statement length: {item['plain_english_statement_len']}",
                f"- Proof length: {item['plain_english_proof_len']}",
                f"- Statement excerpt: {item['statement_excerpt'] or '—'}",
                f"- Comment excerpt: {item['comment_excerpt'] or '—'}",
                "",
            ])
    report_md.write_text("\n".join(lines), encoding="utf-8")

    all_rows = []
    for items in buckets.values():
        all_rows.extend(items)
    with report_csv.open("w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "index", "category", "lean_name", "book_name", "kind", "location",
            "official_lean_declaration", "source_file",
            "plain_english_statement_len", "plain_english_proof_len",
            "statement_excerpt", "comment_excerpt",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in all_rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})

    print("Summary:")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    print(f"Wrote JSON report: {report_json}")
    print(f"Wrote Markdown report: {report_md}")
    print(f"Wrote CSV report: {report_csv}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect HDS records with missing book statement/proof text.")
    parser.add_argument("--library", type=Path, default=DEFAULT_LIBRARY, help="HDS proofs_with_key_strategies JSONL file.")
    parser.add_argument("--report-json", type=Path, default=DEFAULT_REPORT_JSON)
    parser.add_argument("--report-md", type=Path, default=DEFAULT_REPORT_MD)
    parser.add_argument("--report-csv", type=Path, default=DEFAULT_REPORT_CSV)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    records = read_json_records(args.library)
    write_reports(records, args.report_json, args.report_md, args.report_csv)


if __name__ == "__main__":
    main()
