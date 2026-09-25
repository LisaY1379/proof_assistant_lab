#!/usr/bin/env python3
"""
PDF-only extraction workflow for HighDimensionalStatistics.

This test-data-cleaning copy intentionally removes all Lean/report-alignment logic
from the original HDS library builder. It only does:

  PDF -> extracted text -> theorem/proof units JSON

Inputs:
  external/pdf_files/HDP-2.pdf
  or a path passed with --pdf

Outputs by default:
  data/test/high_dimensional_probability/pdf_text.txt
  data/test/high_dimensional_probability/pdf_units.json

No LLM calls. No Lean scanning. No report.json parsing. No processed proof library.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, List, Optional


# This file lives at workflows/test_data_cleasing/build_hds_library.py
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_ROOT = PROJECT_ROOT / "data" / "test" / "high_dimensional_probability"
PDF_FILES_ROOT = PROJECT_ROOT / "external" / "pdf_files"
DEFAULT_PDF_PATHS = [
    PDF_FILES_ROOT / "HDP-2.pdf",
]

DEFAULT_PDF_TEXT_PATH = DATASET_ROOT / "pdf_text.txt"
DEFAULT_PDF_UNITS_JSON = DATASET_ROOT / "pdf_units.json"


@dataclass
class PdfUnit:
    pdf_unit_id: str
    index: int
    kind: str
    name: str
    location_hint: str
    statement: str
    proof_text: str
    raw_text: str
    number_key: str


def stable_id(prefix: str, text: str) -> str:
    return f"{prefix}.{hashlib.sha1(text.encode('utf-8')).hexdigest()[:12]}"


def ensure_dirs(*paths: Path) -> None:
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def find_pdf_path(user_pdf: Optional[str]) -> Optional[Path]:
    candidates: List[Path] = []
    if user_pdf:
        candidates.append(Path(user_pdf).expanduser())
    candidates.extend(DEFAULT_PDF_PATHS)
    candidates.extend(sorted(PDF_FILES_ROOT.rglob("*.pdf")) if PDF_FILES_ROOT.exists() else [])
    seen = set()
    for p in candidates:
        try:
            key = p.resolve()
        except Exception:
            key = p
        if key in seen:
            continue
        seen.add(key)
        if p.exists() and p.is_file():
            return p
    return None


def extract_pdf_text(pdf_path: Path, output_text_path: Path, force: bool = False) -> str:
    if output_text_path.exists() and not force:
        return output_text_path.read_text(encoding="utf-8")
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    if not shutil.which("pdftotext"):
        raise RuntimeError(
            "Cannot extract PDF text because `pdftotext` is not installed. "
            "Install poppler, or manually place extracted text at "
            f"{output_text_path}."
        )
    output_text_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["pdftotext", "-layout", str(pdf_path), str(output_text_path)], check=True)
    return output_text_path.read_text(encoding="utf-8", errors="replace")


def normalize_space(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def infer_number_key(kind: str, number: str) -> str:
    kind = kind.lower().strip()
    return f"{kind}_{number.replace('.', '_')}"


def parse_pdf_units(text: str) -> List[PdfUnit]:
    """Extract rough theorem/lemma/proposition/corollary units from PDF text.

    This parser is intentionally PDF-only and heuristic. It detects headings such
    as `Theorem 1.9`, `Lemma 1.4`, `Proposition 1.1`, `Corollary 2.8`, then
    captures text until the next detected heading. If a `Proof` marker appears,
    text before it is the statement and text after it is proof_text.
    """
    if not text.strip():
        return []

    heading_re = re.compile(
        r"(?im)^\s*(Theorem|Lemma|Proposition|Corollary)\s+([0-9]+(?:\.[0-9]+)+|[0-9]+)"
        r"(?:\s*\(([^\n]+)\)|\s*[:.\-–—]?\s*([^\n]*))"
    )
    matches = list(heading_re.finditer(text))
    units: List[PdfUnit] = []

    for idx, m in enumerate(matches):
        start = m.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        raw = text[start:end].strip()

        kind = m.group(1).lower()
        number = m.group(2)
        title = normalize_space(m.group(3) or m.group(4) or "")
        name = f"{kind.title()} {number}" + (f" ({title})" if title else "")
        number_key = infer_number_key(kind, number)

        proof_match = re.search(r"(?i)\bProof\b\s*[:.]?", raw)
        if proof_match:
            statement = raw[: proof_match.start()].strip()
            proof_text = raw[proof_match.end() :].strip()
            # Trim some common non-proof trailers if they appear as standalone headings.
            proof_text = re.split(
                r"(?im)^\s*(?:□|QED|Bibliographical notes|Exercises|Notes|Problems)\s*$",
                proof_text,
            )[0].strip()
        else:
            statement = raw
            proof_text = ""

        units.append(
            PdfUnit(
                pdf_unit_id=stable_id("hds.pdf", f"{idx + 1}:{name}:{raw[:200]}"),
                index=idx + 1,
                kind=kind,
                name=name,
                location_hint="",
                statement=statement,
                proof_text=proof_text,
                raw_text=raw,
                number_key=number_key,
            )
        )
    return units


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="PDF-only HDS extraction: PDF -> pdf_text.txt + pdf_units.json")
    parser.add_argument("--pdf", default=None, help="Path to textbook PDF. Defaults to external/atlas-original locations.")
    parser.add_argument("--output-text", type=Path, default=DEFAULT_PDF_TEXT_PATH)
    parser.add_argument("--output-units", type=Path, default=DEFAULT_PDF_UNITS_JSON)
    parser.add_argument("--force-pdf-extract", action="store_true", help="Re-run pdftotext even if output text already exists.")
    parser.add_argument("--dry-run", action="store_true", help="Parse and print counts without writing pdf_units.json.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ensure_dirs(args.output_text.parent, args.output_units.parent)

    pdf_path = find_pdf_path(args.pdf)
    if pdf_path:
        print(f"Using PDF: {pdf_path}")
        text = extract_pdf_text(pdf_path, args.output_text, force=args.force_pdf_extract)
    elif args.output_text.exists():
        print(f"No PDF found; using existing extracted text: {args.output_text}")
        text = args.output_text.read_text(encoding="utf-8")
    else:
        raise FileNotFoundError(
            "No PDF found. Put the book at external/pdf_files/HDP-2.pdf "
            "or pass --pdf /path/to/book.pdf."
        )

    units = parse_pdf_units(text)
    print(f"Extracted PDF text characters: {len(text)}")
    print(f"Parsed PDF units: {len(units)}")
    with_proof = sum(1 for u in units if u.proof_text.strip())
    print(f"PDF units with proof text: {with_proof}")
    print("First units:")
    for unit in units[:10]:
        print(f"  {unit.index}. {unit.name} [{unit.number_key}] proof_len={len(unit.proof_text)}")

    if args.dry_run:
        print("Dry run: not writing pdf_units.json.")
        return 0

    write_json(args.output_units, [asdict(unit) for unit in units])
    print(f"Wrote extracted text: {args.output_text}")
    print(f"Wrote PDF units: {args.output_units}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
