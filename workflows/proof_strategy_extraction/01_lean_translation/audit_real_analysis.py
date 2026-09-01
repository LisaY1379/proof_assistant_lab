#!/usr/bin/env python3
"""Audit declaration types in the ATLAS RealAnalysis subset.

Purpose
-------
Before extracting proof strategies, we need to know what kinds of Lean objects
exist in the raw RealAnalysis data: theorem, lemma, def, example, instance, etc.
This script scans .lean files, detects top-level declarations, counts their kinds,
and saves examples for inspection.

Run from project root:

    python workflows/proof_strategy_extraction/audit_real_analysis.py

Optional:

    python workflows/proof_strategy_extraction/audit_real_analysis.py --max-examples 20
    python workflows/proof_strategy_extraction/audit_real_analysis.py --include-private

Outputs:

    data/metadata/real_analysis_declaration_audit.json
    data/metadata/real_analysis_declaration_audit.md
    data/metadata/real_analysis_declarations.csv

Notes
-----
This is a lightweight text scanner, not a full Lean parser. It is intended for
project planning and data triage. It removes comments before scanning so that
commented-out declarations do not dominate the counts.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REAL_ANALYSIS_DIR = PROJECT_ROOT / "external" / "atlas-lean" / "Atlas" / "RealAnalysis"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "metadata"

# Lean declaration-ish keywords that may occur at top level.
DECL_KINDS = [
    "theorem",
    "lemma",
    "example",
    "def",
    "abbrev",
    "instance",
    "class",
    "structure",
    "inductive",
    "coinductive",
    "axiom",
    "constant",
    "opaque",
    "noncomputable def",
    "noncomputable section",  # not a declaration, but useful to count if detected
]

# Modifiers that can appear before declarations.
MODIFIERS = [
    "private",
    "protected",
    "noncomputable",
    "unsafe",
    "partial",
    "mutual",
    "scoped",
    "local",
]

# Regex for declarations. It tries to detect lines like:
#   theorem Foo ...
#   private lemma foo ...
#   noncomputable def bar ...
#   @[simp] theorem baz ...
# Attributes are handled separately by skipping preceding @[...] lines.
DECL_RE = re.compile(
    r"^\s*"
    r"(?P<modifiers>(?:(?:private|protected|noncomputable|unsafe|partial|mutual|scoped|local)\s+)*)"
    r"(?P<kind>theorem|lemma|example|def|abbrev|instance|class|structure|inductive|coinductive|axiom|constant|opaque)"
    r"(?:\s+(?P<name>[^\s:{(\[]+))?"
)

NAMESPACE_RE = re.compile(r"^\s*namespace\s+(?P<name>.+?)\s*$")
SECTION_RE = re.compile(r"^\s*section(?:\s+(?P<name>.*?))?\s*$")
END_RE = re.compile(r"^\s*end(?:\s+(?P<name>.*?))?\s*$")
IMPORT_RE = re.compile(r"^\s*import\s+(?P<module>.+?)\s*$")
OPEN_RE = re.compile(r"^\s*open\s+(?P<what>.+?)\s*$")
ATTRIBUTE_RE = re.compile(r"^\s*@\[.*\]\s*$")


@dataclass
class DeclarationRecord:
    kind: str
    name: str
    modifiers: List[str]
    source_file: str
    line_number: int
    first_line: str
    namespace_stack: List[str]
    section_stack: List[str]
    has_by: bool
    has_assign: bool
    looks_proof_like: bool


def strip_lean_comments_preserve_lines(text: str) -> str:
    """Remove Lean comments while preserving line count.

    Removes:
    - single-line comments beginning with --
    - nested-ish block comments /- ... -/

    This function is deliberately conservative. It attempts to preserve strings
    and line breaks so line numbers remain useful.
    """
    result: List[str] = []
    i = 0
    n = len(text)
    block_depth = 0
    in_string = False
    escape = False

    while i < n:
        ch = text[i]
        nxt = text[i + 1] if i + 1 < n else ""

        if block_depth > 0:
            if ch == "/" and nxt == "-":
                block_depth += 1
                i += 2
                continue
            if ch == "-" and nxt == "/":
                block_depth -= 1
                i += 2
                continue
            # Preserve newlines so line numbers remain aligned.
            if ch == "\n":
                result.append("\n")
            else:
                result.append(" ")
            i += 1
            continue

        if escape:
            result.append(ch)
            escape = False
            i += 1
            continue

        if in_string:
            result.append(ch)
            if ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            i += 1
            continue

        if ch == '"':
            in_string = True
            result.append(ch)
            i += 1
            continue

        if ch == "/" and nxt == "-":
            block_depth = 1
            result.append(" ")
            result.append(" ")
            i += 2
            continue

        if ch == "-" and nxt == "-":
            # Skip to newline, but keep newline.
            while i < n and text[i] != "\n":
                result.append(" ")
                i += 1
            continue

        result.append(ch)
        i += 1

    return "".join(result)


def normalize_kind(modifiers: List[str], kind: str) -> str:
    """Return normalized declaration kind.

    We keep `def` as `def` even if it is noncomputable, but modifiers are stored.
    """
    return kind


def extract_declarations_from_file(path: Path, root: Path, include_private: bool) -> Tuple[List[DeclarationRecord], Counter]:
    raw_text = path.read_text(encoding="utf-8", errors="replace")
    text = strip_lean_comments_preserve_lines(raw_text)
    lines = text.splitlines()

    namespace_stack: List[str] = []
    section_stack: List[str] = []
    records: List[DeclarationRecord] = []
    misc_counts: Counter = Counter()

    relative_path = str(path.relative_to(PROJECT_ROOT))

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped:
            continue

        if IMPORT_RE.match(line):
            misc_counts["import_lines"] += 1
            continue
        if OPEN_RE.match(line):
            misc_counts["open_lines"] += 1
            continue
        if ATTRIBUTE_RE.match(line):
            misc_counts["attribute_lines"] += 1
            continue

        namespace_match = NAMESPACE_RE.match(line)
        if namespace_match:
            namespace_stack.append(namespace_match.group("name").strip())
            misc_counts["namespace_lines"] += 1
            continue

        section_match = SECTION_RE.match(line)
        if section_match:
            section_name = (section_match.group("name") or "").strip()
            section_stack.append(section_name)
            misc_counts["section_lines"] += 1
            continue

        end_match = END_RE.match(line)
        if end_match:
            end_name = (end_match.group("name") or "").strip()
            # We cannot always know whether this closes section or namespace.
            # Prefer closing a section if one is open, otherwise namespace.
            if section_stack:
                section_stack.pop()
            elif namespace_stack:
                namespace_stack.pop()
            misc_counts["end_lines"] += 1
            continue

        decl_match = DECL_RE.match(line)
        if not decl_match:
            continue

        modifiers_raw = decl_match.group("modifiers") or ""
        modifiers = [m for m in modifiers_raw.split() if m]
        kind = decl_match.group("kind")
        name = decl_match.group("name") or "<anonymous>"

        if not include_private and "private" in modifiers:
            misc_counts["private_declarations_skipped"] += 1
            continue

        normalized_kind = normalize_kind(modifiers, kind)

        # Look at a small block after the declaration line for rough proof-like signs.
        following = "\n".join(lines[idx - 1 : min(idx + 20, len(lines))])
        has_by = bool(re.search(r"\bby\b", following))
        has_assign = ":=" in following
        looks_proof_like = kind in {"theorem", "lemma", "example"} and (has_by or has_assign)

        records.append(
            DeclarationRecord(
                kind=normalized_kind,
                name=name,
                modifiers=modifiers,
                source_file=relative_path,
                line_number=idx,
                first_line=stripped,
                namespace_stack=list(namespace_stack),
                section_stack=list(section_stack),
                has_by=has_by,
                has_assign=has_assign,
                looks_proof_like=looks_proof_like,
            )
        )

    return records, misc_counts


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def write_csv(path: Path, records: List[DeclarationRecord]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "kind",
                "name",
                "modifiers",
                "source_file",
                "line_number",
                "first_line",
                "namespace_stack",
                "section_stack",
                "has_by",
                "has_assign",
                "looks_proof_like",
            ],
        )
        writer.writeheader()
        for record in records:
            row = asdict(record)
            row["modifiers"] = " ".join(record.modifiers)
            row["namespace_stack"] = " :: ".join(record.namespace_stack)
            row["section_stack"] = " :: ".join(record.section_stack)
            writer.writerow(row)


def write_markdown(
    path: Path,
    *,
    real_analysis_dir: Path,
    lean_file_count: int,
    records: List[DeclarationRecord],
    misc_counts: Counter,
    max_examples: int,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    kind_counts = Counter(record.kind for record in records)
    proof_like_counts = Counter(record.kind for record in records if record.looks_proof_like)
    modifiers_counts = Counter(mod for record in records for mod in record.modifiers)
    file_counts = Counter(record.source_file for record in records)

    examples_by_kind: Dict[str, List[DeclarationRecord]] = defaultdict(list)
    for record in records:
        if len(examples_by_kind[record.kind]) < max_examples:
            examples_by_kind[record.kind].append(record)

    lines: List[str] = []
    lines.append("# RealAnalysis Declaration Audit")
    lines.append("")
    lines.append(f"Source directory: `{real_analysis_dir}`")
    lines.append(f"Lean files scanned: **{lean_file_count}**")
    lines.append(f"Declarations found: **{len(records)}**")
    lines.append("")

    lines.append("## Declaration kind counts")
    lines.append("")
    lines.append("| Kind | Count | Proof-like count |")
    lines.append("|---|---:|---:|")
    for kind, count in kind_counts.most_common():
        lines.append(f"| `{kind}` | {count} | {proof_like_counts.get(kind, 0)} |")
    lines.append("")

    lines.append("## Modifier counts")
    lines.append("")
    if modifiers_counts:
        lines.append("| Modifier | Count |")
        lines.append("|---|---:|")
        for mod, count in modifiers_counts.most_common():
            lines.append(f"| `{mod}` | {count} |")
    else:
        lines.append("No declaration modifiers detected.")
    lines.append("")

    lines.append("## Miscellaneous line counts")
    lines.append("")
    if misc_counts:
        lines.append("| Item | Count |")
        lines.append("|---|---:|")
        for item, count in misc_counts.most_common():
            lines.append(f"| `{item}` | {count} |")
    else:
        lines.append("No miscellaneous counts recorded.")
    lines.append("")

    lines.append("## Files with most declarations")
    lines.append("")
    lines.append("| File | Count |")
    lines.append("|---|---:|")
    for file, count in file_counts.most_common(20):
        lines.append(f"| `{file}` | {count} |")
    lines.append("")

    lines.append("## Examples by kind")
    lines.append("")
    for kind in sorted(examples_by_kind):
        lines.append(f"### `{kind}`")
        lines.append("")
        lines.append("| Name | File:line | First line |")
        lines.append("|---|---|---|")
        for record in examples_by_kind[kind]:
            first_line = record.first_line.replace("|", "\\|")
            lines.append(
                f"| `{record.name}` | `{record.source_file}:{record.line_number}` | `{first_line}` |"
            )
        lines.append("")

    lines.append("## Suggested filtering for proof-strategy extraction")
    lines.append("")
    lines.append("For the proof-strategy pipeline, start by processing only declaration kinds:")
    lines.append("")
    lines.append("```text")
    lines.append("theorem")
    lines.append("lemma")
    lines.append("example")
    lines.append("```")
    lines.append("")
    lines.append("Definitions such as `def`, `abbrev`, `structure`, and `class` are useful background data, but they should probably go into a separate definition-explanation workflow rather than the proof-strategy workflow.")
    lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit declaration kinds in ATLAS RealAnalysis Lean files.")
    parser.add_argument(
        "--real-analysis-dir",
        type=Path,
        default=DEFAULT_REAL_ANALYSIS_DIR,
        help=f"Path to Atlas/RealAnalysis. Default: {DEFAULT_REAL_ANALYSIS_DIR}",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory. Default: {DEFAULT_OUTPUT_DIR}",
    )
    parser.add_argument(
        "--max-examples",
        type=int,
        default=12,
        help="Maximum examples to show per declaration kind in Markdown output.",
    )
    parser.add_argument(
        "--include-private",
        action="store_true",
        help="Include private declarations instead of skipping them.",
    )
    args = parser.parse_args()

    real_analysis_dir = args.real_analysis_dir
    if not real_analysis_dir.exists():
        raise FileNotFoundError(f"RealAnalysis directory not found: {real_analysis_dir}")

    lean_files = sorted(real_analysis_dir.rglob("*.lean"))
    if not lean_files:
        raise FileNotFoundError(f"No .lean files found under: {real_analysis_dir}")

    all_records: List[DeclarationRecord] = []
    misc_counts: Counter = Counter()

    for lean_file in lean_files:
        records, file_misc_counts = extract_declarations_from_file(
            lean_file,
            real_analysis_dir,
            include_private=args.include_private,
        )
        all_records.extend(records)
        misc_counts.update(file_misc_counts)

    kind_counts = Counter(record.kind for record in all_records)
    proof_like_counts = Counter(record.kind for record in all_records if record.looks_proof_like)
    file_counts = Counter(record.source_file for record in all_records)

    summary = {
        "source_dir": str(real_analysis_dir),
        "lean_file_count": len(lean_files),
        "declaration_count": len(all_records),
        "kind_counts": dict(kind_counts.most_common()),
        "proof_like_counts": dict(proof_like_counts.most_common()),
        "modifier_counts": dict(Counter(mod for r in all_records for mod in r.modifiers).most_common()),
        "misc_counts": dict(misc_counts.most_common()),
        "top_files_by_declaration_count": dict(file_counts.most_common(30)),
        "records": [asdict(record) for record in all_records],
    }

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / "real_analysis_declaration_audit.json"
    md_path = output_dir / "real_analysis_declaration_audit.md"
    csv_path = output_dir / "real_analysis_declarations.csv"

    write_json(json_path, summary)
    write_csv(csv_path, all_records)
    write_markdown(
        md_path,
        real_analysis_dir=real_analysis_dir,
        lean_file_count=len(lean_files),
        records=all_records,
        misc_counts=misc_counts,
        max_examples=args.max_examples,
    )

    print("RealAnalysis declaration audit complete.")
    print(f"Lean files scanned: {len(lean_files)}")
    print(f"Declarations found: {len(all_records)}")
    print("Declaration kind counts:")
    for kind, count in kind_counts.most_common():
        print(f"  {kind}: {count}  proof-like: {proof_like_counts.get(kind, 0)}")
    print("Outputs:")
    print(f"  {json_path.relative_to(PROJECT_ROOT)}")
    print(f"  {md_path.relative_to(PROJECT_ROOT)}")
    print(f"  {csv_path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
