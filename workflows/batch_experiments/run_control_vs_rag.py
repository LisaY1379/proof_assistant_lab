#!/usr/bin/env python3
"""
Batch experiment: compare Control vs Library-RAG proof-agent responses.

This reuses the interactive agent logic from `main/agent_server.py`:
  - API call wrapper
  - .env loading
  - strategy hierarchy retrieval
  - control vs library_rag prompt construction

Inputs are JSONL theorem/problem records. For each record, this script runs both:
  1. control mode
  2. library_rag mode

Outputs are stored in a timestamped run directory:
  data/experiments/control_vs_rag/run_YYYYMMDD_HHMMSS/
    metadata.json
    inputs.jsonl
    outputs.jsonl
    report.md
    report.html

Example:
  .venv/bin/python workflows/batch_experiments/run_control_vs_rag.py \
    --inputs workflows/batch_experiments/theorem_inputs.example.jsonl \
    --limit 3
"""

from __future__ import annotations

import argparse
import html
import importlib.util
import json
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parents[2]
AGENT_SERVER = PROJECT_ROOT / "main" / "agent_server.py"
DEFAULT_OUTPUT_ROOT = PROJECT_ROOT / "reports" / "control_vs_rag"
DEFAULT_MODEL = "gpt-5.6-sol"
DEFAULT_REASONING_EFFORT = "high"
DEFAULT_MAX_COMPLETION_TOKENS = 4000
DEFAULT_TEMPERATURE = 1.0


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def run_id() -> str:
    return "run_" + datetime.now().strftime("%Y%m%d_%H%M%S")


def load_agent() -> Any:
    spec = importlib.util.spec_from_file_location("batch_agent_server", AGENT_SERVER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load interactive agent from {AGENT_SERVER}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    """Read batch inputs in several convenient formats.

    Supported formats:
      1. JSONL: one object per line.
      2. JSON array: [{...}, {...}].
      3. One pretty-printed JSON object, like the PDF-unit record format:
           {"pdf_unit_id": ..., "statement": ..., "proof_text": ...}
      4. Multiple pretty-printed JSON objects concatenated, optionally separated
         by commas, as often happens when copying objects from a JSON array.
    """
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []

    # First try normal JSON: either an array or a single object.
    try:
        obj = json.loads(text)
        if isinstance(obj, list):
            return [x for x in obj if isinstance(x, dict)]
        if isinstance(obj, dict):
            # Support test datasets shaped like:
            # {"metadata": {...}, "records": [{...}, ...]}
            if isinstance(obj.get("records"), list):
                return [x for x in obj["records"] if isinstance(x, dict)]
            return [obj]
    except json.JSONDecodeError:
        pass

    # Then try line-oriented JSONL.
    records: List[Dict[str, Any]] = []
    jsonl_ok = True
    for line_no, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip().rstrip(",")
        if not stripped or stripped.startswith("#"):
            continue
        try:
            obj = json.loads(stripped)
        except json.JSONDecodeError:
            jsonl_ok = False
            break
        if not isinstance(obj, dict):
            raise ValueError(f"Expected JSON object on {path}:{line_no}")
        records.append(obj)
    if jsonl_ok and records:
        return records

    # Finally parse a stream of pretty JSON objects. This also tolerates commas
    # between objects or one trailing comma after a single copied object.
    records = []
    decoder = json.JSONDecoder()
    idx = 0
    n = len(text)
    while idx < n:
        while idx < n and (text[idx].isspace() or text[idx] == ","):
            idx += 1
        if idx >= n:
            break
        try:
            obj, end = decoder.raw_decode(text, idx)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Could not parse JSON object stream near character {idx} in {path}: {exc}") from exc
        if isinstance(obj, dict):
            records.append(obj)
        elif isinstance(obj, list):
            records.extend(x for x in obj if isinstance(x, dict))
        elif isinstance(obj, dict) and isinstance(obj.get("records"), list):
            records.extend(x for x in obj["records"] if isinstance(x, dict))
        else:
            raise ValueError(f"Expected JSON object or list near character {idx} in {path}")
        idx = end
    return records


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def append_jsonl(path: Path, obj: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False, sort_keys=True) + "\n")


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def input_id(item: Dict[str, Any], index: Optional[int] = None) -> str:
    return str(
        item.get("id")
        or item.get("number_key")
        or item.get("pdf_unit_id")
        or item.get("proof_id")
        or item.get("report_target_id")
        or (f"input_{index}" if index is not None else "input")
    )


def input_title(item: Dict[str, Any]) -> str:
    return str(
        item.get("name")
        or item.get("lean_name")
        or item.get("book_name")
        or item.get("number_key")
        or item.get("id")
        or item.get("pdf_unit_id")
        or "unnamed"
    )


def input_dataset(item: Dict[str, Any]) -> str:
    return str(item.get("dataset") or item.get("source_dataset") or "high_dimensional_statistics")


def build_user_message(item: Dict[str, Any]) -> str:
    """Build the exact theorem-proving prompt for the batch experiment.

    Per the current experiment design, the model should receive only a direct
    theorem-proving request followed by the object's `statement` field.
    """
    statement = str(item.get("statement", "")).strip()
    return "Can you prove this theorem? " + statement


def call_condition(
    *,
    agent: Any,
    condition: str,
    item: Dict[str, Any],
    model: str,
    reasoning_effort: Optional[str],
    max_completion_tokens: int,
    temperature: float,
    sleep_seconds: float,
) -> Dict[str, Any]:
    message = build_user_message(item)
    messages, selected_nodes = agent.build_messages(condition, message, history=[])
    started = time.time()
    answer = agent.call_openai_chat(
        api_key=agent.os.environ.get("OPENAI_API_KEY", "").strip(),
        model=model,
        messages=messages,
        api_base=agent.DEFAULT_API_BASE,
        temperature=temperature,
        max_completion_tokens=max_completion_tokens,
        reasoning_effort=reasoning_effort,
    )
    elapsed = time.time() - started
    if not answer.strip():
        retry_tokens = max(max_completion_tokens * 2, 6000)
        started_retry = time.time()
        answer = agent.call_openai_chat(
            api_key=agent.os.environ.get("OPENAI_API_KEY", "").strip(),
            model=model,
            messages=messages,
            api_base=agent.DEFAULT_API_BASE,
            temperature=temperature,
            max_completion_tokens=retry_tokens,
            reasoning_effort=reasoning_effort,
        )
        elapsed += time.time() - started_retry
    if sleep_seconds > 0:
        time.sleep(sleep_seconds)
    return {
        "input_id": input_id(item),
        "dataset": input_dataset(item),
        "name": input_title(item),
        "condition": condition,
        "model": model,
        "temperature": temperature,
        "reasoning_effort": reasoning_effort or "none",
        "max_completion_tokens": max_completion_tokens,
        "created_at": now_iso(),
        "elapsed_seconds": round(elapsed, 3),
        "answer": answer,
        "retrieved_nodes": [
            {
                "id": n.get("id"),
                "label": n.get("label"),
                "level": n.get("level"),
                "description": n.get("description"),
            }
            for n in selected_nodes
        ],
    }


def markdown_escape_code(text: str) -> str:
    return str(text or "").replace("```", "` ` `")


def make_report_md(inputs: List[Dict[str, Any]], outputs: List[Dict[str, Any]], metadata: Dict[str, Any]) -> str:
    by_input: Dict[str, Dict[str, Dict[str, Any]]] = {}
    for out in outputs:
        iid = str(out.get("input_id"))
        by_input.setdefault(iid, {})[str(out.get("condition"))] = out

    lines: List[str] = []
    lines.append("# Control vs Library-RAG Batch Experiment")
    lines.append("")
    lines.append("## Metadata")
    lines.append("")
    for key, value in metadata.items():
        lines.append(f"- **{key}**: `{value}`")
    lines.append("")

    for item in inputs:
        iid = input_id(item)
        title = input_title(item)
        lines.append(f"## {iid} — {title}")
        lines.append("")
        if input_dataset(item):
            lines.append(f"Dataset: `{input_dataset(item)}`")
            lines.append("")
        if item.get("statement") or item.get("formal_statement") or item.get("plain_english_statement") or item.get("plain_english_statement_cleaned"):
            statement = item.get("statement") or item.get("formal_statement") or item.get("plain_english_statement") or item.get("plain_english_statement_cleaned")
            lines.append("### Input statement")
            lines.append("")
            lines.append(str(statement).strip())
            lines.append("")
        if item.get("task"):
            lines.append("### Task")
            lines.append("")
            lines.append(str(item.get("task")).strip())
            lines.append("")

        pair = by_input.get(iid, {})
        control = pair.get("control")
        rag = pair.get("library_rag")

        lines.append("### Control output")
        lines.append("")
        lines.append(control.get("answer", "[missing]") if control else "[missing]")
        lines.append("")

        lines.append("### Library-RAG output")
        lines.append("")
        lines.append(rag.get("answer", "[missing]") if rag else "[missing]")
        lines.append("")

        lines.append("### Retrieved strategy nodes")
        lines.append("")
        if rag and rag.get("retrieved_nodes"):
            for node in rag["retrieved_nodes"]:
                lines.append(f"- `{node.get('id')}` — **{node.get('label')}**: {node.get('description', '')}")
        else:
            lines.append("None retrieved.")
        lines.append("")

        lines.append("---")
        lines.append("")
    return "\n".join(lines)


def markdown_to_simple_html(md: str) -> str:
    # Minimal report renderer; keeps Markdown-ish text readable without external deps.
    escaped = html.escape(md)
    escaped = escaped.replace("\n", "<br>\n")
    escaped = escaped.replace("# ", "<h1>").replace("<br>\n## ", "</h1>\n<h2>").replace("<br>\n### ", "</h2>\n<h3>")
    return f"""<!doctype html>
<html><head><meta charset='utf-8'><title>Control vs RAG Report</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; line-height: 1.55; max-width: 1100px; margin: 32px auto; padding: 0 18px; color: #111827; }}
code {{ background: #f1f5f9; padding: 2px 4px; border-radius: 4px; }}
h1,h2,h3 {{ color: #1e3a8a; }}
</style></head><body>{escaped}</body></html>"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run control vs Library-RAG proof-agent batch experiment.")
    parser.add_argument("--inputs", type=Path, required=True, help="Input theorem/problem JSONL file.")
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--run-name", default=None, help="Optional run directory name. Defaults to timestamp.")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--reasoning-effort", choices=["none", "low", "medium", "high"], default=DEFAULT_REASONING_EFFORT)
    parser.add_argument("--max-completion-tokens", type=int, default=DEFAULT_MAX_COMPLETION_TOKENS)
    parser.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE)
    parser.add_argument("--sleep", type=float, default=0.0)
    parser.add_argument("--conditions", nargs="+", choices=["control", "library_rag"], default=["control", "library_rag"])
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    agent = load_agent()
    agent.load_dotenv()
    api_key = agent.os.environ.get("OPENAI_API_KEY", "").strip()
    if not args.dry_run and (not api_key or api_key == "your-openai-api-key-here"):
        raise RuntimeError("OPENAI_API_KEY missing or placeholder. Set .env or export it before running.")

    inputs = read_jsonl(args.inputs)
    if args.limit is not None:
        inputs = inputs[: args.limit]
    if not inputs:
        raise RuntimeError("No input records to process.")

    run_dir = args.output_root / (args.run_name or run_id())
    run_dir.mkdir(parents=True, exist_ok=True)
    outputs_path = run_dir / "outputs.jsonl"
    report_md_path = run_dir / "report.md"
    report_html_path = run_dir / "report.html"
    metadata_path = run_dir / "metadata.json"
    inputs_copy_path = run_dir / "inputs.jsonl"

    metadata = {
        "created_at": now_iso(),
        "input_path": str(args.inputs),
        "input_count": len(inputs),
        "conditions": args.conditions,
        "model": args.model,
        "temperature": args.temperature,
        "reasoning_effort": args.reasoning_effort,
        "max_completion_tokens": args.max_completion_tokens,
        "strategy_graph": str(agent.GRAPH_PATH.relative_to(PROJECT_ROOT)) if agent.GRAPH_PATH.exists() else str(agent.GRAPH_PATH),
    }
    write_json(metadata_path, metadata)
    write_jsonl(inputs_copy_path, inputs)

    print(f"Run directory: {run_dir}")
    print(f"Inputs: {len(inputs)}")
    print(f"Conditions: {', '.join(args.conditions)}")
    print(f"Model: {args.model}")

    if args.dry_run:
        print("Dry run: no API calls.")
        for item in inputs[:5]:
            print(f"- {input_id(item)}: {input_title(item)}")
        return 0

    reasoning_effort = None if args.reasoning_effort == "none" else args.reasoning_effort
    all_outputs: List[Dict[str, Any]] = []

    for idx, item in enumerate(inputs, start=1):
        print(f"[{idx}/{len(inputs)}] {input_id(item, idx)} — {input_title(item)}")
        for condition in args.conditions:
            print(f"  - {condition}", flush=True)
            try:
                out = call_condition(
                    agent=agent,
                    condition=condition,
                    item=item,
                    model=args.model,
                    reasoning_effort=reasoning_effort,
                    max_completion_tokens=args.max_completion_tokens,
                    temperature=args.temperature,
                    sleep_seconds=args.sleep,
                )
            except Exception as exc:  # noqa: BLE001
                out = {
                    "input_id": input_id(item),
                    "dataset": input_dataset(item),
                    "name": input_title(item),
                    "condition": condition,
                    "model": args.model,
                    "temperature": args.temperature,
                    "reasoning_effort": args.reasoning_effort,
                    "max_completion_tokens": args.max_completion_tokens,
                    "created_at": now_iso(),
                    "error": str(exc),
                    "answer": "",
                    "retrieved_nodes": [],
                }
            append_jsonl(outputs_path, out)
            all_outputs.append(out)

    report_md = make_report_md(inputs, all_outputs, metadata)
    report_md_path.write_text(report_md, encoding="utf-8")
    report_html_path.write_text(markdown_to_simple_html(report_md), encoding="utf-8")
    print(f"Wrote outputs: {outputs_path}")
    print(f"Wrote Markdown report: {report_md_path}")
    print(f"Wrote HTML report: {report_html_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
