#!/usr/bin/env python3
"""
Build an initial HighDimensionalStatistics proof library by aligning ATLAS Lean
statements with original natural-language proof text extracted from a textbook PDF.

Output:
  data/high_dimensional_statistics/processed/proofs_with_key_strategies.jsonl

Each output record contains the core aligned variables:
  - comment: Lean doc comment immediately before the declaration
  - lean_original_code: original Lean declaration/proof block
  - plain_english_statement: corresponding original theorem/lemma statement from the book, if aligned
  - plain_english_proof: corresponding original proof text from the book, if aligned

The script also writes an alignment report under metadata for inspection.

Alignment logic, v0.2:
  1. Parse official ATLAS target records from report.json.
  2. Use report.json's `lean_declaration` and `lean_file` fields as the authoritative
     textbook-target ↔ Lean mapping.
  3. Extract theorem/lemma/proposition/corollary-style units from PDF text.
  4. Align official report targets to PDF units primarily by theorem numbering,
     with fallback text similarity.

This deliberately avoids treating every helper Lean lemma as a textbook-level record.
The output library is one record per official proof-like report target by default.

Notes:
  - PDF extraction uses the external `pdftotext` command if available.
  - If no PDF is available, the script can still build records with empty plain_english.
  - This is an initial simple workflow; it is designed for inspection and refinement.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATASET_ROOT = PROJECT_ROOT / "data" / "high_dimensional_statistics"
ATLAS_ROOT = PROJECT_ROOT / "external" / "atlas-lean" / "Atlas" / "HighDimensionalStatistics"
LEAN_CODE_ROOT = ATLAS_ROOT / "code"
REPORT_PATH = ATLAS_ROOT / "report.json"

RAW_DIR = DATASET_ROOT / "raw"
EXTRACTED_DIR = DATASET_ROOT / "extracted"
PROCESSED_DIR = DATASET_ROOT / "processed"
METADATA_DIR = DATASET_ROOT / "metadata"

ATLAS_ORIGINAL_ROOT = PROJECT_ROOT / "external" / "atlas-original"
HDS_ORIGINAL_ROOT = ATLAS_ORIGINAL_ROOT / "HighDimensionalStatistics"

DEFAULT_PDF_PATHS = [
    HDS_ORIGINAL_ROOT / "original.pdf",
    HDS_ORIGINAL_ROOT / "high_dimensional_statistics.pdf",
    ATLAS_ORIGINAL_ROOT / "HighDimensionalStatistics.pdf",
    ATLAS_ORIGINAL_ROOT / "high_dimensional_statistics.pdf",
]

OUTPUT_JSONL = PROCESSED_DIR / "proofs_with_key_strategies.jsonl"
OUTPUT_JSON = PROCESSED_DIR / "proofs_with_key_strategies.json"
ALIGNMENT_REPORT_JSON = METADATA_DIR / "hds_pdf_lean_alignment_report.json"
ALIGNMENT_REPORT_MD = METADATA_DIR / "hds_pdf_lean_alignment_report.md"
PDF_TEXT_PATH = EXTRACTED_DIR / "pdf_text.txt"
PDF_UNITS_JSON = EXTRACTED_DIR / "pdf_units.json"
TARGETS_JSON = METADATA_DIR / "atlas_report_targets.json"
LEAN_DECLS_JSON = PROCESSED_DIR / "lean_declarations.json"

DECL_BOUNDARY_RE = re.compile(
    r"^(?P<prefix>\s*)(?:noncomputable\s+)?(?:private\s+|protected\s+)?"
    r"(?P<kind>theorem|lemma|def|structure|class|instance|abbrev|example)\b\s*"
    r"(?P<name>[^\s:(]+)?"
)
TOP_LEVEL_NON_DECL_RE = re.compile(
    r"^\s*(?:variable|namespace|section|end|open|local|noncomputable\s+section)\b"
)
ALLOWED_LEAN_KINDS = {"theorem", "lemma", "def", "structure", "class", "instance", "abbrev", "example"}
BOOK_UNIT_KINDS = {"theorem", "lemma", "proposition", "corollary"}


@dataclass
class LeanDecl:
    lean_id: str
    kind: str
    lean_name: str
    comment: str
    lean_original_code: str
    formal_statement: str
    source_file: str
    start_line: int
    end_line: int
    number_key: str


@dataclass
class ReportTarget:
    target_id: str
    index: int
    kind: str
    name: str
    location: str
    description: str
    number_key: str
    official_lean_declaration: str
    official_lean_file: str
    passed: bool
    match_confidence: str
    scores: Dict[str, Any]


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


def ensure_dirs() -> None:
    for path in [RAW_DIR, EXTRACTED_DIR, PROCESSED_DIR, METADATA_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def stable_id(prefix: str, text: str) -> str:
    return f"{prefix}.{hashlib.sha1(text.encode('utf-8')).hexdigest()[:12]}"


def strip_block_comment_markers(comment: str) -> str:
    s = comment.strip()
    if s.startswith("/--"):
        s = s[3:]
    elif s.startswith("/-"):
        s = s[2:]
    if s.endswith("-/"):
        s = s[:-2]
    lines = []
    for line in s.splitlines():
        line = re.sub(r"^\s*\*\s?", "", line).rstrip()
        lines.append(line)
    return "\n".join(lines).strip()


def remove_initial_license_comment(text: str) -> str:
    # Keep doc comments later, but remove leading copyright block from consideration.
    return text


def find_doc_comment_before(lines: List[str], decl_start_idx: int) -> str:
    """Find a Lean doc comment /-- ... -/ immediately above declaration."""
    j = decl_start_idx - 1
    while j >= 0 and lines[j].strip() == "":
        j -= 1
    if j < 0:
        return ""

    # Single-line or ending line of multi-line doc comment.
    if "-/" not in lines[j]:
        return ""

    block: List[str] = []
    while j >= 0:
        block.append(lines[j])
        if "/--" in lines[j]:
            block.reverse()
            return strip_block_comment_markers("\n".join(block))
        # Stop if this is a non-doc block comment.
        if "/-" in lines[j] and "/--" not in lines[j]:
            return ""
        j -= 1
    return ""


def find_block_end_before_next_context(lines: List[str], start_i: int, next_decl_i: int) -> int:
    """Trim a declaration block before following doc comments/top-level setup.

    ATLAS files often look like:

        theorem foo ... := proof_term

        variable ...

        /-- doc comment for the next theorem -/
        theorem bar ...

    A naive declaration-to-next-declaration slice would attach `variable ...` and
    the next doc comment to `foo`.  This function trims such trailing context.
    It is deliberately conservative: it only trims after the current declaration
    body has started, i.e. after seeing `:=`.
    """
    seen_body = False
    i = start_i
    while i < next_decl_i:
        line = lines[i]
        stripped = line.strip()
        if ":=" in line:
            seen_body = True
        if seen_body and i > start_i:
            if stripped.startswith("/--"):
                return i
            if TOP_LEVEL_NON_DECL_RE.match(line):
                return i
            if stripped == "":
                j = i + 1
                while j < next_decl_i and lines[j].strip() == "":
                    j += 1
                if j < next_decl_i:
                    nxt = lines[j]
                    nxt_stripped = nxt.strip()
                    if nxt_stripped.startswith("/--") or TOP_LEVEL_NON_DECL_RE.match(nxt) or DECL_BOUNDARY_RE.match(nxt):
                        return i
        i += 1
    return next_decl_i


def iter_declaration_blocks(text: str) -> Iterable[Tuple[int, int, str, str, str, str]]:
    """Yield start/end/kind/name/comment/block for top-level declarations."""
    lines = text.splitlines()
    starts: List[Tuple[int, re.Match[str]]] = []
    for i, line in enumerate(lines):
        m = DECL_BOUNDARY_RE.match(line)
        if m and len(m.group("prefix")) == 0:
            starts.append((i, m))

    for idx, (start_i, m) in enumerate(starts):
        next_decl_i = starts[idx + 1][0] if idx + 1 < len(starts) else len(lines)
        end_i = find_block_end_before_next_context(lines, start_i, next_decl_i)
        kind = m.group("kind")
        name = m.group("name") or "anonymous"
        comment = find_doc_comment_before(lines, start_i)
        block = "\n".join(lines[start_i:end_i]).rstrip()
        yield start_i + 1, end_i, kind, name, comment, block


def extract_formal_statement(block: str) -> str:
    if ":= by" in block:
        return block.split(":= by", 1)[0].strip()
    if ":=" in block:
        return block.split(":=", 1)[0].strip()
    return block.splitlines()[0].strip() if block.splitlines() else ""


def infer_number_key_from_text(text: str) -> str:
    """Infer canonical number key such as theorem_1_9 or lemma_1_4."""
    if not text:
        return ""
    patterns = [
        r"\b(Theorem|Lemma|Proposition|Prop\.?|Corollary|Cor\.?|Problem)\s+([0-9]+(?:\.[0-9]+)+|[0-9]+)\b",
        r"\b(Thm|Thm\.|Lemma|Prop|Cor|Def|Definition)_?\s*([0-9]+(?:[_\.][0-9]+)+|[0-9]+)\b",
    ]
    for pat in patterns:
        m = re.search(pat, text, flags=re.IGNORECASE)
        if m:
            kind_raw = m.group(1).lower().replace(".", "")
            num = m.group(2).replace("_", ".")
            if kind_raw in {"thm", "theorem"}:
                kind = "theorem"
            elif kind_raw == "lemma":
                kind = "lemma"
            elif kind_raw in {"prop", "proposition"}:
                kind = "proposition"
            elif kind_raw in {"cor", "corollary"}:
                kind = "corollary"
            elif kind_raw in {"def", "definition"}:
                kind = "definition"
            else:
                kind = kind_raw
            return f"{kind}_{num.replace('.', '_')}"

    # File/name convention fallback: Thm_1_9, Lemma_1_4, Cor_1_7, Prop_1_1.
    m = re.search(r"\b(Thm|Theorem|Lemma|Prop|Proposition|Cor|Corollary)[_\s-]+([0-9]+(?:[_\.][0-9]+)*)", text, re.I)
    if m:
        kind_raw = m.group(1).lower()
        num = m.group(2).replace("_", ".")
        kind = {
            "thm": "theorem",
            "theorem": "theorem",
            "lemma": "lemma",
            "prop": "proposition",
            "proposition": "proposition",
            "cor": "corollary",
            "corollary": "corollary",
        }[kind_raw]
        return f"{kind}_{num.replace('.', '_')}"
    return ""


def extract_lean_declarations(limit: Optional[int] = None) -> List[LeanDecl]:
    """Extract Lean declarations for lookup by report.json's official names.

    We extract broad declaration kinds here because official report targets can be
    definitions when `--include-definitions` is requested.  The output library is
    still controlled by `report.json`, not by this raw declaration list.
    """
    records: List[LeanDecl] = []
    if not LEAN_CODE_ROOT.exists():
        raise FileNotFoundError(f"Lean code root not found: {LEAN_CODE_ROOT}")

    for path in sorted(LEAN_CODE_ROOT.rglob("*.lean")):
        text = path.read_text(encoding="utf-8")
        for start_line, end_line, kind, name, comment, block in iter_declaration_blocks(text):
            if kind not in ALLOWED_LEAN_KINDS:
                continue
            rel = path.relative_to(PROJECT_ROOT).as_posix()
            number_key = infer_number_key_from_text(" ".join([rel, name, comment, block[:500]]))
            formal_statement = extract_formal_statement(block)
            records.append(
                LeanDecl(
                    lean_id=stable_id("hds.lean", f"{rel}:{start_line}:{name}"),
                    kind=kind,
                    lean_name=name,
                    comment=comment,
                    lean_original_code=block,
                    formal_statement=formal_statement,
                    source_file=rel,
                    start_line=start_line,
                    end_line=end_line,
                    number_key=number_key,
                )
            )
            if limit and len(records) >= limit:
                return records
    return records


def normalize_decl_name(name: str) -> str:
    return (name or "").split(".")[-1].strip()


def atlas_relative_file_key(path: str) -> str:
    """Normalize Lean paths to the `Atlas/...` form used by report.json."""
    p = (path or "").replace("\\", "/").strip()
    marker = "Atlas/HighDimensionalStatistics/"
    idx = p.find(marker)
    if idx >= 0:
        return p[idx:]
    return p


def build_lean_lookup(lean_decls: List[LeanDecl]) -> Dict[Tuple[str, str], LeanDecl]:
    """Build lookup keyed by `(source_file, full_or_short_declaration_name)`.

    The extractor stores source files relative to the project root, e.g.
    `external/atlas-lean/Atlas/...`, while report.json stores `Atlas/...` paths.
    We index both forms.
    """
    lookup: Dict[Tuple[str, str], LeanDecl] = {}
    for decl in lean_decls:
        name_keys = {
            decl.lean_name,
            normalize_decl_name(decl.lean_name),
        }
        file_keys = {
            decl.source_file,
            atlas_relative_file_key(decl.source_file),
        }
        for file_key in file_keys:
            for name_key in name_keys:
                if file_key and name_key:
                    lookup[(file_key, name_key)] = decl
    return lookup


def find_official_lean_decl(target: ReportTarget, lookup: Dict[Tuple[str, str], LeanDecl]) -> Optional[LeanDecl]:
    """Find the official Lean declaration named by report.json."""
    lean_file = target.official_lean_file
    lean_decl = target.official_lean_declaration
    if not lean_file or not lean_decl:
        return None

    for key in [lean_decl, normalize_decl_name(lean_decl)]:
        found = lookup.get((lean_file, key))
        if found:
            return found

    # Conservative fallback: same file and declaration suffix match.
    suffix = normalize_decl_name(lean_decl)
    candidates = [d for (file, _), d in lookup.items() if file == lean_file and d.lean_name == suffix]
    return candidates[0] if candidates else None


def parse_report_targets(path: Path = REPORT_PATH, *, include_definitions: bool = False) -> List[ReportTarget]:
    """Parse official ATLAS target mappings from report.json.

    `report.json` is authoritative for the textbook-target ↔ Lean mapping because
    each statement detail includes `name`, `description`, `kind`, `lean_file`, and
    `lean_declaration`.  This function intentionally filters to proof-like book
    targets by default, rather than all helper Lean declarations.
    """
    if not path.exists():
        raise FileNotFoundError(f"ATLAS report.json not found: {path}")

    raw = json.loads(path.read_text(encoding="utf-8"))
    details = raw.get("statements", {}).get("details", [])
    targets: List[ReportTarget] = []
    allowed_kinds = set(BOOK_UNIT_KINDS)
    if include_definitions:
        allowed_kinds.add("definition")

    for fallback_i, item in enumerate(details, start=1):
        kind = str(item.get("kind", "")).strip().lower()
        if kind not in allowed_kinds:
            continue
        name = str(item.get("name", "")).strip()
        location = str(item.get("location", "")).strip()
        description = str(item.get("description", "")).strip()
        index = int(item.get("idx", fallback_i))
        lean_decl = str(item.get("lean_declaration", "")).strip()
        lean_file = str(item.get("lean_file", "")).strip()
        number_key = infer_number_key_from_text(name) or infer_number_key_from_text(location + " " + description[:300])
        targets.append(
            ReportTarget(
                target_id=str(item.get("id", "")).strip() or stable_id("hds.report_target", f"{index}:{name}:{lean_decl}"),
                index=index,
                kind=kind,
                name=name,
                location=location,
                description=description,
                number_key=number_key,
                official_lean_declaration=lean_decl,
                official_lean_file=lean_file,
                passed=bool(item.get("passed", False)),
                match_confidence=str(item.get("match_confidence", "")).strip(),
                scores=dict(item.get("scores", {})),
            )
        )
    targets.sort(key=lambda t: t.index)
    return targets


def find_pdf_path(user_pdf: Optional[str]) -> Optional[Path]:
    candidates: List[Path] = []
    if user_pdf:
        candidates.append(Path(user_pdf).expanduser())
    candidates.extend(DEFAULT_PDF_PATHS)
    candidates.extend(sorted(HDS_ORIGINAL_ROOT.rglob("*.pdf")) if HDS_ORIGINAL_ROOT.exists() else [])
    candidates.extend(sorted(ATLAS_ORIGINAL_ROOT.rglob("*.pdf")) if ATLAS_ORIGINAL_ROOT.exists() else [])
    for p in candidates:
        if p.exists() and p.is_file():
            return p
    return None


def extract_pdf_text(pdf_path: Path, force: bool = False) -> str:
    if PDF_TEXT_PATH.exists() and not force:
        return PDF_TEXT_PATH.read_text(encoding="utf-8")
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    if not shutil.which("pdftotext"):
        raise RuntimeError(
            "Cannot extract PDF text because `pdftotext` is not installed. "
            "Install poppler or manually save extracted text to "
            f"{PDF_TEXT_PATH}."
        )
    PDF_TEXT_PATH.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["pdftotext", "-layout", str(pdf_path), str(PDF_TEXT_PATH)]
    subprocess.run(cmd, check=True)
    return PDF_TEXT_PATH.read_text(encoding="utf-8", errors="replace")


def normalize_space(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def parse_pdf_units(text: str) -> List[PdfUnit]:
    """Extract rough theorem/lemma units and following proof text from PDF text.

    This is intentionally heuristic. It looks for headings such as "Theorem 1.9",
    "Lemma 1.4", etc., then captures until the next such heading. Proof text is the
    substring after the first occurrence of "Proof" if present.
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
        num = m.group(2)
        title = normalize_space(m.group(3) or m.group(4) or "")
        name = f"{kind.title()} {num}" + (f" ({title})" if title else "")
        number_key = f"{kind}_{num.replace('.', '_')}"

        proof_match = re.search(r"(?i)\bProof\b\s*[:.]?", raw)
        if proof_match:
            statement = raw[: proof_match.start()].strip()
            proof_text = raw[proof_match.end() :].strip()
            # Stop proof at common terminal markers only if they are clearly present.
            proof_text = re.split(r"(?im)^\s*(?:□|QED|Bibliographical notes|Exercises)\s*$", proof_text)[0].strip()
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


def token_set(s: str) -> set[str]:
    return {t.lower() for t in re.findall(r"[A-Za-z][A-Za-z0-9_]+", s or "") if len(t) > 2}


def jaccard(a: str, b: str) -> float:
    ta, tb = token_set(a), token_set(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def choose_alignment(target: ReportTarget, pdf_units: List[PdfUnit]) -> Dict[str, Any]:
    """Align one official report target to a PDF theorem/proof unit."""
    pdf_unit: Optional[PdfUnit] = None
    confidence = 0.0
    method = "none"
    reason = "No matching PDF unit found."

    if target.number_key:
        same_pdf = [u for u in pdf_units if u.number_key == target.number_key]
        if same_pdf:
            pdf_unit = same_pdf[0]
            confidence = 0.95
            method = "report_number_key_to_pdf"
            reason = f"Official report target matched PDF unit by number key {target.number_key}."

    if not pdf_unit and pdf_units:
        source = "\n".join([target.name, target.location, target.description])
        scored_p = [(jaccard(source, u.statement), u) for u in pdf_units]
        scored_p.sort(reverse=True, key=lambda x: x[0])
        if scored_p and scored_p[0][0] >= 0.15:
            pdf_unit = scored_p[0][1]
            confidence = 0.55
            method = "report_target_to_pdf_similarity"
            reason = f"Official report target matched PDF by statement similarity {scored_p[0][0]:.3f}."

    return {
        "target_id": target.target_id,
        "target_index": target.index,
        "target_kind": target.kind,
        "target_name": target.name,
        "target_location": target.location,
        "target_number_key": target.number_key,
        "official_lean_declaration": target.official_lean_declaration,
        "official_lean_file": target.official_lean_file,
        "report_match_confidence": target.match_confidence,
        "report_passed": target.passed,
        "pdf_unit_id": pdf_unit.pdf_unit_id if pdf_unit else "",
        "pdf_name": pdf_unit.name if pdf_unit else "",
        "pdf_number_key": pdf_unit.number_key if pdf_unit else "",
        "alignment_method": method,
        "alignment_confidence": confidence,
        "alignment_reason": normalize_space(reason),
        "plain_english_statement": pdf_unit.statement if pdf_unit else target.description,
        "plain_english_proof": pdf_unit.proof_text if pdf_unit else "",
    }


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, records: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False, indent=2))
            f.write("\n")


def write_alignment_md(path: Path, report: Dict[str, Any], alignments: List[Dict[str, Any]]) -> None:
    lines = [
        "# HighDimensionalStatistics PDF ↔ Lean Alignment Report",
        "",
        f"Created: {report['created_at']}",
        "",
        "## Summary",
        "",
        f"- Raw Lean declarations indexed: {report['lean_declaration_count']}",
        f"- Official report targets: {report['target_count']}",
        f"- PDF units: {report['pdf_unit_count']}",
        f"- Output records: {report['output_record_count']}",
        f"- Records with statement: {report['records_with_plain_english_statement']}",
        f"- Records with proof: {report['records_with_plain_english_proof']}",
        "",
        "## Alignments",
        "",
        "| # | Book target | Official Lean declaration | Official file | PDF unit | Method | Confidence |",
        "|---:|---|---|---|---|---|---:|",
    ]
    for i, a in enumerate(alignments, start=1):
        lines.append(
            f"| {i} | {a['target_name'] or '—'} | `{a['official_lean_declaration'] or '—'}` | "
            f"`{a['official_lean_file'] or '—'}` | {a['pdf_name'] or '—'} | "
            f"{a['alignment_method']} | {a['alignment_confidence']:.2f} |"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build initial HDS PDF/Lean aligned proof library.")
    parser.add_argument("--pdf", default=None, help="Path to textbook PDF. Defaults to external/atlas-original locations if present.")
    parser.add_argument("--limit", type=int, default=None, help="Only process first N official report targets.")
    parser.add_argument("--include-definitions", action="store_true", help="Also include official definition targets from report.json. Default: proof-like targets only.")
    parser.add_argument("--force-pdf-extract", action="store_true", help="Re-extract PDF text even if extracted/pdf_text.txt exists.")
    parser.add_argument("--allow-empty-pdf", action="store_true", help="Build framework even if no PDF/text is available; plain_english will be empty.")
    parser.add_argument("--dry-run", action="store_true", help="Preview counts and alignments without writing output library.")
    args = parser.parse_args()

    ensure_dirs()

    print("Indexing Lean declarations for official report targets...")
    lean_decls = extract_lean_declarations(limit=None)
    lean_lookup = build_lean_lookup(lean_decls)
    print(f"  Raw Lean declarations indexed: {len(lean_decls)}")

    print("Parsing official ATLAS report.json targets...")
    targets = parse_report_targets(include_definitions=args.include_definitions)
    if args.limit:
        targets = targets[: args.limit]
    print(f"  Official report targets: {len(targets)}")

    pdf_text = ""
    pdf_units: List[PdfUnit] = []
    pdf_path = find_pdf_path(args.pdf)
    if pdf_path:
        print(f"Using PDF: {pdf_path}")
        try:
            pdf_text = extract_pdf_text(pdf_path, force=args.force_pdf_extract)
        except Exception as exc:
            if not args.allow_empty_pdf:
                raise
            print(f"WARNING: PDF extraction failed, continuing with empty PDF units: {exc}")
    elif PDF_TEXT_PATH.exists():
        print(f"Using existing extracted PDF text: {PDF_TEXT_PATH}")
        pdf_text = PDF_TEXT_PATH.read_text(encoding="utf-8")
    elif args.allow_empty_pdf:
        print("WARNING: No PDF or extracted text found; building empty plain_english framework.")
    else:
        raise FileNotFoundError(
            "No PDF found. Put the book at external/atlas-original/HighDimensionalStatistics/original.pdf "
            "or external/atlas-original/HighDimensionalStatistics.pdf, "
            "or pass --pdf /path/to/book.pdf, or use --allow-empty-pdf."
        )

    if pdf_text:
        print("Parsing theorem/lemma/proposition/corollary units from PDF text...")
        pdf_units = parse_pdf_units(pdf_text)
    print(f"  PDF units: {len(pdf_units)}")

    alignments: List[Dict[str, Any]] = []
    output_records: List[Dict[str, Any]] = []
    official_missing_lean = 0
    for target in targets:
        lean = find_official_lean_decl(target, lean_lookup)
        if lean is None:
            official_missing_lean += 1
        alignment = choose_alignment(target, pdf_units)
        alignments.append(alignment)
        output_records.append(
            {
                "book_name": target.name,
                "kind": target.kind,
                "location": target.location,
                "official_lean_declaration": target.official_lean_declaration,
                "official_lean_file": target.official_lean_file,
                "report_target_id": target.target_id,
                "report_passed": target.passed,
                "report_match_confidence": target.match_confidence,
                "comment": lean.comment if lean else target.description,
                "lean_original_code": lean.lean_original_code if lean else "",
                "plain_english_statement": alignment.get("plain_english_statement", ""),
                "plain_english_proof": alignment.get("plain_english_proof", ""),
            }
        )

    records_with_plain = sum(1 for r in output_records if r.get("plain_english_proof", "").strip())
    records_with_statement = sum(1 for r in output_records if r.get("plain_english_statement", "").strip())
    report = {
        "created_at": now_iso(),
        "workflow": "02_pdf_text_extraction/build_hds_library.py",
        "dataset": "high_dimensional_statistics",
        "atlas_root": ATLAS_ROOT.relative_to(PROJECT_ROOT).as_posix(),
        "pdf_path": str(pdf_path) if pdf_path else "",
        "pdf_text_path": PDF_TEXT_PATH.relative_to(PROJECT_ROOT).as_posix(),
        "lean_declaration_count": len(lean_decls),
        "target_count": len(targets),
        "official_targets_missing_lean_declaration": official_missing_lean,
        "pdf_unit_count": len(pdf_units),
        "output_record_count": len(output_records),
        "records_with_plain_english_statement": records_with_statement,
        "records_with_plain_english_proof": records_with_plain,
        "records_with_plain_english": records_with_plain,
        "notes": "Official-target alignment. Output library is one record per proof-like report.json target and stores comment, lean_original_code, plain_english_statement, and plain_english_proof.",
    }

    print("\nSummary:")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("\nFirst alignments:")
    for i, a in enumerate(alignments[:10], start=1):
        print(f"  {i}. {a['target_name']} -> lean={a['official_lean_declaration'] or '—'}; pdf={a['pdf_name'] or '—'}; method={a['alignment_method']}; conf={a['alignment_confidence']:.2f}")

    if args.dry_run:
        print("\nDry run: no files written.")
        return

    write_json(LEAN_DECLS_JSON, [asdict(d) for d in lean_decls])
    write_json(TARGETS_JSON, [asdict(t) for t in targets])
    write_json(PDF_UNITS_JSON, [asdict(u) for u in pdf_units])
    write_jsonl(OUTPUT_JSONL, output_records)
    write_json(OUTPUT_JSON, output_records)
    write_json(ALIGNMENT_REPORT_JSON, {"summary": report, "alignments": alignments})
    write_alignment_md(ALIGNMENT_REPORT_MD, report, alignments)

    print("\nWrote:")
    for p in [OUTPUT_JSONL, OUTPUT_JSON, LEAN_DECLS_JSON, TARGETS_JSON, PDF_UNITS_JSON, ALIGNMENT_REPORT_JSON, ALIGNMENT_REPORT_MD]:
        print(f"  - {p.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
