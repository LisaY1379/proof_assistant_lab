#!/usr/bin/env python3
"""
Export local workflow outputs into static JSON files for the public read-only viewer.

This exports both datasets:

    data/real_analysis/processed/proofs_with_key_strategies.jsonl
    data/high_dimensional_statistics/processed/proofs_with_key_strategies.jsonl

into:

    tools/public_viewer/data/datasets.json
    tools/public_viewer/data/real_analysis_proofs_with_key_strategies.json
    tools/public_viewer/data/real_analysis_theorem_overview.json
    tools/public_viewer/data/high_dimensional_statistics_proofs_with_key_strategies.json
    tools/public_viewer/data/high_dimensional_statistics_theorem_overview.json

Legacy names are also written for RealAnalysis compatibility:

    tools/public_viewer/data/proofs_with_key_strategies.json
    tools/public_viewer/data/theorem_overview.json
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PUBLIC_DATA_DIR = PROJECT_ROOT / "tools" / "public_viewer" / "data"

DATASETS = {
    "real_analysis": {
        "label": "RealAnalysis",
        "proofs": PROJECT_ROOT / "data" / "real_analysis" / "processed" / "proofs_with_key_strategies.jsonl",
        "legacy": True,
    },
    "high_dimensional_statistics": {
        "label": "HighDimensionalStatistics",
        "proofs": PROJECT_ROOT / "data" / "high_dimensional_statistics" / "processed" / "proofs_with_key_strategies.jsonl",
        "legacy": False,
    },
}


def read_jsonl_like(path: Path) -> List[Dict[str, Any]]:
    """Read compact JSONL, pretty-printed JSONL-like files, or JSON arrays."""
    if not path.exists():
        return []

    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []

    try:
        obj = json.loads(text)
        if isinstance(obj, list):
            return [x for x in obj if isinstance(x, dict)]
        if isinstance(obj, dict):
            return [obj]
    except json.JSONDecodeError:
        pass

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


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def make_excerpt(text: str, max_len: int = 220) -> str:
    text = " ".join(str(text or "").split())
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + "…"


def infer_lean_name(row: Dict[str, Any], idx: int) -> str:
    for key in ["lean_name", "official_lean_declaration", "book_name", "name"]:
        if row.get(key):
            return str(row[key])
    code = str(row.get("lean_original_code", ""))
    m = re.search(r"(?m)^\s*(?:theorem|lemma|def|structure|class)\s+([^\s(:]+)", code)
    return m.group(1) if m else f"item_{idx}"


def strategy_counts(row: Dict[str, Any]) -> tuple[int, int]:
    strategies = row.get("key_strategies", [])
    if isinstance(strategies, list):
        total = len([x for x in strategies if isinstance(x, dict) or str(x).strip()])
        categorized = sum(
            1
            for item in strategies
            if isinstance(item, dict) and str(item.get("category", "")).strip()
        )
        return total, categorized
    if isinstance(strategies, str) and strategies.strip():
        nums = re.findall(r"(?m)^\s*\d+[\.)]\s+", strategies)
        return (len(nums) if nums else 1), 0
    return 0, 0


def build_public_proof(row: Dict[str, Any], idx: int, dataset_id: str) -> Dict[str, Any]:
    lean_name = infer_lean_name(row, idx)
    statement = row.get("plain_english_statement_cleaned") or row.get("plain_english_statement") or ""
    proof = row.get("plain_english_proof_cleaned") or row.get("plain_english_proof") or ""
    legacy_english = row.get("textbook_explanation") or row.get("plain_english") or ""
    return {
        "dataset": dataset_id,
        "index": idx,
        "proof_id": row.get("proof_id") or row.get("report_target_id") or f"{dataset_id}.{idx}",
        "book_name": row.get("book_name", ""),
        "lean_name": lean_name,
        "official_lean_declaration": row.get("official_lean_declaration", ""),
        "official_lean_file": row.get("official_lean_file", ""),
        "kind": row.get("kind", ""),
        "location": row.get("location", ""),
        "source_file": row.get("source_file") or row.get("official_lean_file", ""),
        "start_line": row.get("start_line"),
        "end_line": row.get("end_line"),
        "comment": row.get("comment", ""),
        "formal_statement": row.get("formal_statement", ""),
        "lean_original_code": row.get("lean_original_code", ""),
        "plain_english_statement": statement,
        "plain_english_proof": proof,
        "textbook_explanation": legacy_english,
        "plain_english": legacy_english,
        "key_strategies": row.get("key_strategies", ""),
        "strategies_refined": row.get("strategies_refined", []),
        "model": row.get("model", row.get("key_strategy_model", "")),
        "annotation_status": row.get("annotation_status", row.get("key_strategy_status", "")),
    }


def build_overview(public_proofs: List[Dict[str, Any]], dataset_id: str) -> List[Dict[str, Any]]:
    overview: List[Dict[str, Any]] = []
    for idx, row in enumerate(public_proofs, start=1):
        total, categorized = strategy_counts(row)
        refined = row.get("strategies_refined", [])
        overview.append(
            {
                "dataset": dataset_id,
                "index": idx,
                "proof_id": row.get("proof_id"),
                "lean_name": row.get("lean_name"),
                "book_name": row.get("book_name", ""),
                "kind": row.get("kind"),
                "location": row.get("location", ""),
                "source_file": row.get("source_file", ""),
                "start_line": row.get("start_line"),
                "end_line": row.get("end_line"),
                "comment": row.get("comment", ""),
                "comment_excerpt": make_excerpt(row.get("comment", "")),
                "formal_statement": row.get("formal_statement", ""),
                "processed": bool(row.get("lean_original_code") or row.get("plain_english_statement") or row.get("plain_english_proof") or row.get("plain_english")),
                "strategy_count": total,
                "categorized_strategy_count": categorized,
                "category_processed": total > 0 and categorized == total,
                "refined_processed": isinstance(refined, list) and len(refined) > 0,
            }
        )
    return overview


def main() -> int:
    PUBLIC_DATA_DIR.mkdir(parents=True, exist_ok=True)
    dataset_manifest = []

    for dataset_id, cfg in DATASETS.items():
        raw_proofs = read_jsonl_like(cfg["proofs"])
        public_proofs = [build_public_proof(row, idx, dataset_id) for idx, row in enumerate(raw_proofs, start=1)]
        overview = build_overview(public_proofs, dataset_id)

        proofs_name = f"{dataset_id}_proofs_with_key_strategies.json"
        overview_name = f"{dataset_id}_theorem_overview.json"
        write_json(PUBLIC_DATA_DIR / proofs_name, public_proofs)
        write_json(PUBLIC_DATA_DIR / overview_name, overview)

        if cfg.get("legacy"):
            write_json(PUBLIC_DATA_DIR / "proofs_with_key_strategies.json", public_proofs)
            write_json(PUBLIC_DATA_DIR / "theorem_overview.json", overview)

        dataset_manifest.append(
            {
                "id": dataset_id,
                "label": cfg["label"],
                "proof_count": len(public_proofs),
                "overview_count": len(overview),
                "proofs_path": f"data/{proofs_name}",
                "overview_path": f"data/{overview_name}",
            }
        )
        print(f"Wrote {len(public_proofs)} {cfg['label']} proofs")
        print(f"Wrote {len(overview)} {cfg['label']} overview items")

    write_json(PUBLIC_DATA_DIR / "datasets.json", {"datasets": dataset_manifest, "default_dataset": "real_analysis"})
    print(f"Wrote dataset manifest to {PUBLIC_DATA_DIR / 'datasets.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
