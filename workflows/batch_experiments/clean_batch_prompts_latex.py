#!/usr/bin/env python3
"""
Clean batch experiment theorem prompts/statements into readable Markdown + LaTeX.

This is a patch workflow for reports/control_vs_rag/<run>/inputs.jsonl.
It calls an LLM to convert the raw `statement` field into clean LaTeX formatting,
then writes:

  reports/control_vs_rag/<run>/prompt_cleaning.jsonl

The comparison visualizer can then display the cleaned prompt instead of the raw
PDF-extracted text.

Run:
  .venv/bin/python workflows/batch_experiments/clean_batch_prompts_latex.py \
    --run-dir reports/control_vs_rag/run_20260924_144730_new_arch
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parents[2]
AGENT_PATH = PROJECT_ROOT / "main" / "agent_server.py"
DEFAULT_REPORT_ROOT = PROJECT_ROOT / "reports" / "control_vs_rag"


def load_agent() -> Any:
    spec = importlib.util.spec_from_file_location("agent_server", AGENT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load agent_server.py from {AGENT_PATH}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["agent_server"] = mod
    spec.loader.exec_module(mod)
    return mod


def latest_run_dir() -> Path:
    runs = sorted(DEFAULT_REPORT_ROOT.glob("run_*"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not runs:
        raise FileNotFoundError(f"No runs found under {DEFAULT_REPORT_ROOT}")
    return runs[0]


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        obj = json.loads(line)
        if isinstance(obj, dict):
            records.append(obj)
    return records


def append_jsonl(path: Path, obj: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False, sort_keys=True) + "\n")


def input_id(item: Dict[str, Any], index: Optional[int] = None) -> str:
    return str(
        item.get("id")
        or item.get("number_key")
        or item.get("pdf_unit_id")
        or item.get("proof_id")
        or item.get("report_target_id")
        or item.get("test_item_id")
        or (f"input_{index}" if index is not None else "input")
    )


def statement_text(item: Dict[str, Any]) -> str:
    return str(
        item.get("statement")
        or item.get("formal_statement")
        or item.get("plain_english_statement")
        or item.get("plain_english_statement_cleaned")
        or ""
    ).strip()


SYSTEM_PROMPT = r"""You are a careful mathematical editor.
Your job is to clean a theorem statement extracted from a PDF into readable Markdown + LaTeX.

Rules:
- Preserve the mathematical meaning exactly.
- Do not prove the theorem.
- Do not add new assumptions or remove assumptions.
- Convert mathematical notation into valid LaTeX.
- Use \( ... \) for inline math and \[ ... \] for displayed equations if needed.
- Fix obvious PDF extraction artifacts, such as:
  - Rn or IRn -> \mathbb{R}^n
  - ||x|| -> \|x\|
  - X1, ..., Xn -> X_1, \ldots, X_n
  - <= -> \le, >= -> \ge
- Keep the result concise and only return the cleaned theorem statement.
"""


def clean_statement(agent: Any, *, raw_statement: str, model: str, reasoning_effort: Optional[str], max_tokens: int, temperature: float) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Raw theorem statement:\n{raw_statement}"},
    ]
    return agent.call_openai_chat(
        api_key=os.environ.get("OPENAI_API_KEY", "").strip(),
        model=model,
        messages=messages,
        api_base=agent.DEFAULT_API_BASE,
        temperature=temperature,
        max_completion_tokens=max_tokens,
        reasoning_effort=reasoning_effort,
    ).strip()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, default=None, help="Run directory. Defaults to latest reports/control_vs_rag/run_*.")
    parser.add_argument("--model", default="gpt-5.6-sol")
    parser.add_argument("--reasoning-effort", default="high", choices=["none", "low", "medium", "high"])
    parser.add_argument("--max-tokens", type=int, default=1200)
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--redo", action="store_true", help="Recompute even if prompt_cleaning.jsonl already has an entry.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    run_dir = args.run_dir or latest_run_dir()
    inputs_path = run_dir / "inputs.jsonl"
    output_path = run_dir / "prompt_cleaning.jsonl"
    if not inputs_path.exists():
        raise FileNotFoundError(f"Missing inputs file: {inputs_path}")

    inputs = read_jsonl(inputs_path)
    existing: Dict[str, Dict[str, Any]] = {}
    if output_path.exists() and not args.redo:
        for rec in read_jsonl(output_path):
            if rec.get("input_id"):
                existing[str(rec["input_id"])] = rec

    print(f"Run dir: {run_dir}")
    print(f"Inputs: {len(inputs)}")
    print(f"Existing cleaned prompts: {len(existing)}")
    if args.dry_run:
        for i, item in enumerate(inputs, start=1):
            iid = input_id(item, i)
            status = "skip-existing" if iid in existing else "would-clean"
            print(f"- {iid}: {status}; raw_len={len(statement_text(item))}")
        return

    agent = load_agent()
    if hasattr(agent, "load_dotenv"):
        agent.load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("OPENAI_API_KEY is not set. Add it to .env or export it.")

    if args.redo and output_path.exists():
        output_path.unlink()
        existing = {}

    reasoning_effort = None if args.reasoning_effort == "none" else args.reasoning_effort
    for i, item in enumerate(inputs, start=1):
        iid = input_id(item, i)
        if iid in existing:
            continue
        raw = statement_text(item)
        print(f"[{i}/{len(inputs)}] Cleaning prompt {iid}", flush=True)
        cleaned = clean_statement(
            agent,
            raw_statement=raw,
            model=args.model,
            reasoning_effort=reasoning_effort,
            max_tokens=args.max_tokens,
            temperature=args.temperature,
        )
        rec = {
            "input_id": iid,
            "raw_statement": raw,
            "cleaned_statement_latex": cleaned,
            "prompt_cleaned": "Can you prove this theorem? " + cleaned,
            "model": args.model,
            "reasoning_effort": args.reasoning_effort,
        }
        append_jsonl(output_path, rec)
    print(f"Wrote: {output_path}")


if __name__ == "__main__":
    main()
