#!/usr/bin/env python3
"""
Randomly sample proof units from a PDF-units JSON file to create a small testing dataset.

Default input:
  data/test/high_dimensional_probability/pdf_units.json

Default output:
  data/test/high_dimensional_probability/test_01/data.json

By default, this samples only units with non-empty `proof_text`, because the batch
proof-agent experiment needs an actual proof context.

Run from project root:
  .venv/bin/python workflows/testing_data_preparation/random_fetch_testing_data.py

For reproducibility:
  .venv/bin/python workflows/testing_data_preparation/random_fetch_testing_data.py --seed 42
"""

from __future__ import annotations

import argparse
import json
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = PROJECT_ROOT / "data" / "test" / "high_dimensional_probability" / "pdf_units.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "test" / "high_dimensional_probability" / "test_01" / "data.json"


def read_units(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Input PDF units file not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"Expected a JSON array in {path}")
    return [item for item in data if isinstance(item, dict)]


def has_proof(unit: Dict[str, Any]) -> bool:
    return bool(str(unit.get("proof_text", "")).strip())


def make_test_record(unit: Dict[str, Any], sample_index: int) -> Dict[str, Any]:
    """Normalize a PDF unit into the batch experiment's accepted input format.

    The batch workflow can also read raw PDF-unit records directly, but this adds
    explicit test metadata and a default task.
    """
    return {
        "test_item_id": f"test_01_{sample_index:02d}",
        "source_pdf_unit_id": unit.get("pdf_unit_id", ""),
        "source_index": unit.get("index"),
        "dataset": "high_dimensional_probability",
        "kind": unit.get("kind", ""),
        "name": unit.get("name", ""),
        "number_key": unit.get("number_key", ""),
        "statement": unit.get("statement", ""),
        "proof_text": unit.get("proof_text", ""),
        "raw_text": unit.get("raw_text", ""),
        "task": "Explain the proof strategy and give a proof plan. Identify the main mathematical methods used.",
    }


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Randomly sample 5 proof units into a testing dataset.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--seed", type=int, default=None, help="Optional random seed for reproducibility.")
    parser.add_argument("--allow-no-proof", action="store_true", help="Allow sampling units without proof_text.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite output if it already exists.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.count <= 0:
        raise ValueError("--count must be positive")
    if args.output.exists() and not args.overwrite:
        raise FileExistsError(f"Output already exists: {args.output}. Use --overwrite to replace it.")

    units = read_units(args.input)
    candidates = units if args.allow_no_proof else [unit for unit in units if has_proof(unit)]
    if len(candidates) < args.count:
        raise RuntimeError(
            f"Not enough candidate units to sample {args.count}. "
            f"Candidates={len(candidates)}, total units={len(units)}. "
            "Use --allow-no-proof if you intentionally want statement-only units."
        )

    rng = random.Random(args.seed)
    sampled = rng.sample(candidates, args.count)
    records = [make_test_record(unit, idx) for idx, unit in enumerate(sampled, start=1)]

    output = {
        "metadata": {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "source_file": str(args.input.relative_to(PROJECT_ROOT) if args.input.is_absolute() and PROJECT_ROOT in args.input.parents else args.input),
            "sample_count": args.count,
            "seed": args.seed,
            "proof_required": not args.allow_no_proof,
            "total_units": len(units),
            "candidate_units": len(candidates),
        },
        "records": records,
    }
    write_json(args.output, output)

    print(f"Read units: {len(units)}")
    print(f"Candidate units: {len(candidates)}")
    print(f"Sampled records: {len(records)}")
    print(f"Wrote: {args.output}")
    for record in records:
        print(f"  - {record['test_item_id']}: {record['name']} [{record['number_key']}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
