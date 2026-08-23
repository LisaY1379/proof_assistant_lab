#!/usr/bin/env python3
"""
Export local workflow outputs into static JSON files for the public read-only viewer.

Run from the project root:

    python tools/public_viewer/export_public_data.py

It creates:

    tools/public_viewer/data/proofs_with_key_strategies.json
    tools/public_viewer/data/theorem_overview.json

The public viewer reads only those static files and does not need the Python backend.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_PROOFS = PROJECT_ROOT / "data" / "processed" / "proofs_with_key_strategies.jsonl"
ATLAS_REAL_ANALYSIS_DIR = PROJECT_ROOT / "external" / "atlas-lean" / "Atlas" / "RealAnalysis"
ATLAS_REPO_ROOT = PROJECT_ROOT / "external" / "atlas-lean"
PIPELINE_DIR = PROJECT_ROOT / "workflows" / "proof_strategy_extraction"
PUBLIC_DATA_DIR = PROJECT_ROOT / "tools" / "public_viewer" / "data"
PUBLIC_PROOFS = PUBLIC_DATA_DIR / "proofs_with_key_strategies.json"
PUBLIC_OVERVIEW = PUBLIC_DATA_DIR / "theorem_overview.json"


def read_jsonl_like(path: Path) -> List[Dict[str, Any]]:
    """Read compact JSONL or this project's pretty-printed JSONL-like files."""
    if not path.exists():
        return []

    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []

    # Try standard JSON first.
    try:
        obj = json.loads(text)
        if isinstance(obj, list):
            return [x for x in obj if isinstance(x, dict)]
        if isinstance(obj, dict):
            return [obj]
    except json.JSONDecodeError:
        pass

    # Try compact JSONL.
    rows: List[Dict[str, Any]] = []
    ok = True
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        try:
            obj = json.loads(stripped)
            if isinstance(obj, dict):
                rows.append(obj)
        except json.JSONDecodeError:
            ok = False
            break
    if ok:
        return rows

    # Parse pretty-printed JSON objects separated by blank lines.
    rows = []
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
                record_text = "".join(buffer).strip()
                if record_text:
                    obj = json.loads(record_text)
                    if isinstance(obj, dict):
                        rows.append(obj)
                buffer = []

    trailing = "".join(buffer).strip()
    if trailing:
        raise ValueError(f"Could not parse trailing JSON in {path}")

    return rows


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def make_excerpt(text: str, max_len: int = 220) -> str:
    text = " ".join(str(text or "").split())
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + "…"


def load_all_theorem_lemma_records() -> List[Dict[str, Any]]:
    """Scan the ATLAS RealAnalysis source directly for the complete overview."""
    if not ATLAS_REAL_ANALYSIS_DIR.exists():
        raise FileNotFoundError(
            f"ATLAS RealAnalysis directory not found: {ATLAS_REAL_ANALYSIS_DIR}\n"
            "Run scripts/setup_atlas_real_analysis.sh or sparse-clone ATLAS first."
        )

    sys.path.insert(0, str(PIPELINE_DIR))
    from run_pipeline import extract_proofs  # type: ignore

    return extract_proofs(ATLAS_REAL_ANALYSIS_DIR, ATLAS_REPO_ROOT, limit=None)


def main() -> int:
    processed = read_jsonl_like(PROCESSED_PROOFS)
    extracted = load_all_theorem_lemma_records()

    processed_ids = {row.get("proof_id") for row in processed if row.get("proof_id")}

    overview: List[Dict[str, Any]] = []
    for idx, row in enumerate(extracted, start=1):
        proof_id = row.get("proof_id")
        overview.append(
            {
                "index": idx,
                "proof_id": proof_id,
                "lean_name": row.get("lean_name"),
                "kind": row.get("kind"),
                "source_file": row.get("source_file"),
                "start_line": row.get("start_line"),
                "end_line": row.get("end_line"),
                "comment": row.get("comment", ""),
                "comment_excerpt": make_excerpt(row.get("comment", "")),
                "formal_statement": row.get("formal_statement", ""),
                "processed": proof_id in processed_ids,
            }
        )

    public_proofs = []
    for row in processed:
        public_proofs.append(
            {
                "proof_id": row.get("proof_id"),
                "lean_name": row.get("lean_name"),
                "kind": row.get("kind"),
                "source_file": row.get("source_file"),
                "start_line": row.get("start_line"),
                "end_line": row.get("end_line"),
                "comment": row.get("comment", ""),
                "formal_statement": row.get("formal_statement", ""),
                "lean_original_code": row.get("lean_original_code", ""),
                "textbook_explanation": row.get("textbook_explanation") or row.get("plain_english", ""),
                "plain_english": row.get("plain_english") or row.get("textbook_explanation", ""),
                "key_strategies": row.get("key_strategies", ""),
                "model": row.get("model", ""),
                "annotation_status": row.get("annotation_status", ""),
            }
        )

    write_json(PUBLIC_PROOFS, public_proofs)
    write_json(PUBLIC_OVERVIEW, overview)

    print(f"Wrote {len(public_proofs)} processed proofs to {PUBLIC_PROOFS}")
    print(f"Wrote {len(overview)} overview items to {PUBLIC_OVERVIEW}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
