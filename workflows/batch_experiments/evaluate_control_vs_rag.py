#!/usr/bin/env python3
"""
AI-judge workflow for Control vs Library-RAG batch experiment outputs.

For each theorem/problem in a run directory, this script asks a judge model to
review the two generated proofs/responses and evaluate whether they achieve:

    "elaborate on critical steps, omit trivial steps"

It explicitly asks the judge to highlight:
  - sections where the Library-RAG response worked well;
  - sections where the Library-RAG response needs improvement;
  - comparison notes against the control response.

Inputs:
  reports/control_vs_rag/<run>/inputs.jsonl
  reports/control_vs_rag/<run>/outputs.jsonl

Outputs:
  reports/control_vs_rag/<run>/evaluation.jsonl
  reports/control_vs_rag/<run>/evaluation_report.md
  reports/control_vs_rag/<run>/evaluation_report.html

Example:
  .venv/bin/python workflows/batch_experiments/evaluate_control_vs_rag.py \
    --run-dir reports/control_vs_rag/run_20260924_144730
"""

from __future__ import annotations

import argparse
import html
import importlib.util
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parents[2]
AGENT_SERVER = PROJECT_ROOT / "main" / "agent_server.py"
DEFAULT_REPORT_ROOT = PROJECT_ROOT / "reports" / "control_vs_rag"
DEFAULT_MODEL = "gpt-5.6-sol"
DEFAULT_REASONING_EFFORT = "high"
DEFAULT_MAX_COMPLETION_TOKENS = 3000
DEFAULT_TEMPERATURE = 1.0

CRITERION = "elaborate on critical steps, omit trivial steps"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_agent() -> Any:
    spec = importlib.util.spec_from_file_location("batch_eval_agent_server", AGENT_SERVER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load interactive agent from {AGENT_SERVER}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def latest_run_dir(root: Path) -> Path:
    if not root.exists():
        raise FileNotFoundError(f"Report root not found: {root}")
    candidates = [p for p in root.iterdir() if p.is_dir() and (p / "outputs.jsonl").exists()]
    if not candidates:
        raise FileNotFoundError(f"No run directories with outputs.jsonl found under {root}")
    return max(candidates, key=lambda p: p.stat().st_mtime)


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    rows: List[Dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSONL at {path}:{line_no}: {exc}") from exc
        if isinstance(obj, dict):
            rows.append(obj)
    return rows


def append_jsonl(path: Path, obj: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False, sort_keys=True) + "\n")


def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
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
        or item.get("test_item_id")
        or (f"input_{index}" if index is not None else "input")
    )


def input_title(item: Dict[str, Any]) -> str:
    return str(
        item.get("name")
        or item.get("lean_name")
        or item.get("book_name")
        or item.get("number_key")
        or item.get("id")
        or item.get("test_item_id")
        or item.get("pdf_unit_id")
        or "unnamed"
    )


def statement_text(item: Dict[str, Any]) -> str:
    return str(
        item.get("statement")
        or item.get("formal_statement")
        or item.get("plain_english_statement")
        or item.get("plain_english_statement_cleaned")
        or ""
    ).strip()


def group_outputs(outputs: List[Dict[str, Any]]) -> Dict[str, Dict[str, Dict[str, Any]]]:
    grouped: Dict[str, Dict[str, Dict[str, Any]]] = {}
    for out in outputs:
        iid = str(out.get("input_id") or "input")
        condition = str(out.get("condition") or "unknown")
        grouped.setdefault(iid, {})[condition] = out
    return grouped


def strip_json_fence(text: str) -> str:
    text = str(text or "").strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    return text.strip()


def parse_judge_json(raw: str) -> Dict[str, Any]:
    cleaned = strip_json_fence(raw)
    try:
        obj = json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise
        obj = json.loads(cleaned[start : end + 1])
    if not isinstance(obj, dict):
        raise ValueError("Judge response must be a JSON object")
    return obj


def build_judge_prompt(item: Dict[str, Any], control: Dict[str, Any], rag: Dict[str, Any]) -> str:
    retrieved_nodes = rag.get("retrieved_nodes", []) if rag else []
    return f"""
You are evaluating proof explanations/proof plans generated by two systems.

Evaluation criterion:
"{CRITERION}"

Meaning of the criterion:
- Critical steps are mathematical moves without which the proof would not work: the decisive inequality, transformation, theorem selection, construction, reduction, decomposition, estimate, or limiting argument.
- Trivial steps are routine algebra, purely mechanical rewriting, restating assumptions, or filler text unless those steps are genuinely the conceptual key.
- A good answer should spend more detail on critical steps and less space on routine mechanics.

Important treatment of Library-RAG strategy blocks:
- The Library-RAG response may contain inline blocks like [STRATEGY: ...] ... [/STRATEGY] or [NEW_STRATEGY: ...] ... [/NEW_STRATEGY].
- Treat these strategy blocks as annotations, NOT as part of the proof explanation itself.
- Do not reward or penalize the RAG response merely for including these blocks.
- Use each strategy block only as a pointer to the nearby proof passage it annotates.

Your task:
1. Read the theorem statement.
2. Read the CONTROL response and Library-RAG response.
3. Ignore the strategy blocks as proof text, but use them to identify which RAG proof passage they are related to.
4. Evaluate whether the RAG proof passage related to each strategy block becomes better or worse than the corresponding part of the CONTROL response with respect to the criterion.
5. Highlight where the RAG proof passage improved over control and where it became worse or still needs improvement.
6. For every worked-well or needs-improvement judgment, explicitly identify BOTH:
   - the RAG proof passage being judged, and
   - the corresponding passage in the CONTROL response.
   These paired passages will be highlighted and linked in the visualizer.
7. Judge by mathematical explanatory quality: did RAG better elaborate critical steps and omit/compress trivial steps?
8. Return strict JSON only.

THEOREM / PROBLEM:
ID: {input_id(item)}
Name: {input_title(item)}
Statement:
{statement_text(item) or '[No statement provided]'}

CONTROL RESPONSE:
{control.get('answer') or '[Missing control answer]'}

LIBRARY-RAG RESPONSE:
{rag.get('answer') if rag else '[Missing Library-RAG answer]'}

RAG RETRIEVED NODES:
{json.dumps(retrieved_nodes, ensure_ascii=False, indent=2)}

Return strict JSON in this exact shape:
{{
  "input_id": "{input_id(item)}",
  "criterion": "{CRITERION}",
  "control_score_1_to_5": <integer>,
  "rag_score_1_to_5": <integer>,
  "winner": "control|library_rag|tie",
  "rag_overall_assessment": "<short assessment of the Library-RAG response>",
  "rag_worked_sections": [
    {{
      "pair_id": "pair_1",
      "section_or_quote": "<quote/paraphrase from the RAG proof passage, not from the strategy block>",
      "related_strategy_block": "<strategy node/card label if one points to this passage, otherwise empty>",
      "corresponding_control_section": "<quote/paraphrase of the analogous control passage>",
      "why_it_worked": "<why the RAG passage improves on control or better satisfies the criterion>"
    }}
  ],
  "rag_needs_improvement_sections": [
    {{
      "pair_id": "pair_2",
      "section_or_quote": "<quote/paraphrase from the RAG proof passage, not from the strategy block>",
      "related_strategy_block": "<strategy node/card label if one points to this passage, otherwise empty>",
      "corresponding_control_section": "<quote/paraphrase of the analogous control passage>",
      "issue": "<what is worse than control, still missing, too trivial, or too compressed>",
      "suggested_revision": "<how to improve the RAG proof passage>"
    }}
  ],
  "paired_section_links": [
    {{
      "pair_id": "pair_1",
      "judgment": "worked_well|needs_improvement",
      "rag_section_or_quote": "<same RAG proof passage>",
      "control_section_or_quote": "<corresponding control passage>",
      "summary": "<one-sentence comparison>"
    }}
  ],
  "critical_steps_that_should_be_elaborated": ["<step 1>", "<step 2>"],
  "trivial_steps_that_should_be_omitted_or_compressed": ["<step 1>", "<step 2>"],
  "control_comparison_notes": "<brief comparison to control>",
  "evaluator_confidence": "high|medium|low"
}}
""".strip()


def call_judge(
    *,
    agent: Any,
    item: Dict[str, Any],
    control: Dict[str, Any],
    rag: Dict[str, Any],
    model: str,
    reasoning_effort: Optional[str],
    max_completion_tokens: int,
    temperature: float,
) -> Dict[str, Any]:
    prompt = build_judge_prompt(item, control, rag)
    messages = [
        {
            "role": "system",
            "content": (
                "You are a rigorous but fair mathematical proof-explanation evaluator. "
                "Return only valid JSON. Do not add prose outside JSON."
            ),
        },
        {"role": "user", "content": prompt},
    ]
    raw = agent.call_openai_chat(
        api_key=agent.os.environ.get("OPENAI_API_KEY", "").strip(),
        model=model,
        messages=messages,
        api_base=agent.DEFAULT_API_BASE,
        temperature=temperature,
        max_completion_tokens=max_completion_tokens,
        reasoning_effort=reasoning_effort,
    )
    try:
        parsed = parse_judge_json(raw)
    except Exception as first_exc:
        # Reasoning models can return empty visible content or malformed JSON when
        # the first token budget is too small. Retry once with a stricter prompt
        # and larger budget before giving up.
        retry_prompt = build_judge_prompt(item, control, rag) + """

IMPORTANT RETRY INSTRUCTION:
Your previous response was empty or invalid JSON. Return ONLY a valid JSON object matching the requested schema. Keep every string concise. Do not use Markdown fences. Do not include prose outside JSON.
"""
        raw_retry = agent.call_openai_chat(
            api_key=agent.os.environ.get("OPENAI_API_KEY", "").strip(),
            model=model,
            messages=[messages[0], {"role": "user", "content": retry_prompt}],
            api_base=agent.DEFAULT_API_BASE,
            temperature=temperature,
            max_completion_tokens=max(max_completion_tokens, 5000),
            reasoning_effort=reasoning_effort,
        )
        try:
            parsed = parse_judge_json(raw_retry)
            raw = raw_retry
        except Exception as second_exc:
            return {
                "input_id": input_id(item),
                "criterion": CRITERION,
                "error": f"Judge returned invalid JSON after retry: {second_exc}",
                "first_parse_error": str(first_exc),
                "raw_judge_response": raw,
                "raw_judge_retry_response": raw_retry,
                "evaluated_at": now_iso(),
                "judge_model": model,
            }
    parsed["raw_judge_response"] = raw
    parsed["evaluated_at"] = now_iso()
    parsed["judge_model"] = model
    return parsed


def make_report_md(inputs: List[Dict[str, Any]], evaluations: List[Dict[str, Any]]) -> str:
    by_id = {str(e.get("input_id")): e for e in evaluations}
    lines: List[str] = []
    lines.append("# Evaluation Report: Elaborate Critical Steps, Omit Trivial Steps")
    lines.append("")
    lines.append(f"Criterion: **{CRITERION}**")
    lines.append("")

    scores = [e for e in evaluations if isinstance(e.get("control_score_1_to_5"), int)]
    if scores:
        avg_control = sum(e.get("control_score_1_to_5", 0) for e in scores) / len(scores)
        avg_rag = sum(e.get("rag_score_1_to_5", 0) for e in scores) / len(scores)
        winners: Dict[str, int] = {}
        for e in scores:
            winners[str(e.get("winner", "unknown"))] = winners.get(str(e.get("winner", "unknown")), 0) + 1
        lines.append("## Summary")
        lines.append("")
        lines.append(f"- Evaluated items: {len(scores)}")
        lines.append(f"- Average control score: {avg_control:.2f}/5")
        lines.append(f"- Average Library-RAG score: {avg_rag:.2f}/5")
        lines.append(f"- Winners: {winners}")
        lines.append("")

    for idx, item in enumerate(inputs, start=1):
        iid = input_id(item, idx)
        ev = by_id.get(iid)
        lines.append(f"## {idx}. {input_title(item)}")
        lines.append("")
        lines.append(f"ID: `{iid}`")
        lines.append("")
        if statement_text(item):
            lines.append("### Statement")
            lines.append("")
            lines.append(statement_text(item))
            lines.append("")
        if not ev:
            lines.append("No evaluation found.")
            lines.append("")
            continue

        lines.append("### Scores")
        lines.append("")
        lines.append(f"- Control: **{ev.get('control_score_1_to_5')} / 5**")
        lines.append(f"- Library-RAG: **{ev.get('rag_score_1_to_5')} / 5**")
        lines.append(f"- Winner: **{ev.get('winner')}**")
        lines.append(f"- Confidence: `{ev.get('evaluator_confidence')}`")
        lines.append("")

        lines.append("### Library-RAG overall assessment")
        lines.append("")
        lines.append(str(ev.get("rag_overall_assessment", ev.get("control_overall_assessment", ""))))
        lines.append("")

        lines.append("### Where the Library-RAG response worked")
        lines.append("")
        worked = ev.get("rag_worked_sections", ev.get("control_worked_sections", []))
        if worked:
            for item2 in worked:
                if isinstance(item2, dict):
                    lines.append(f"- **Section/quote:** {item2.get('section_or_quote', '')}")
                    lines.append(f"  - Why it worked: {item2.get('why_it_worked', '')}")
        else:
            lines.append("None identified.")
        lines.append("")

        lines.append("### Where the Library-RAG response needs improvement")
        lines.append("")
        bad = ev.get("rag_needs_improvement_sections", ev.get("control_needs_improvement_sections", []))
        if bad:
            for item2 in bad:
                if isinstance(item2, dict):
                    lines.append(f"- **Section/quote:** {item2.get('section_or_quote', '')}")
                    lines.append(f"  - Issue: {item2.get('issue', '')}")
                    lines.append(f"  - Suggested revision: {item2.get('suggested_revision', '')}")
        else:
            lines.append("None identified.")
        lines.append("")

        lines.append("### Critical steps to elaborate")
        lines.append("")
        for step in ev.get("critical_steps_that_should_be_elaborated", []) or []:
            lines.append(f"- {step}")
        lines.append("")

        lines.append("### Trivial steps to omit/compress")
        lines.append("")
        for step in ev.get("trivial_steps_that_should_be_omitted_or_compressed", []) or []:
            lines.append(f"- {step}")
        lines.append("")

        lines.append("### Control comparison notes")
        lines.append("")
        lines.append(str(ev.get("control_comparison_notes", ev.get("rag_comparison_notes", ""))))
        lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines)


def markdown_to_html(md: str) -> str:
    escaped = html.escape(md)
    escaped = re.sub(r"^# (.*?)$", r"<h1>\1</h1>", escaped, flags=re.M)
    escaped = re.sub(r"^## (.*?)$", r"<h2>\1</h2>", escaped, flags=re.M)
    escaped = re.sub(r"^### (.*?)$", r"<h3>\1</h3>", escaped, flags=re.M)
    escaped = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = escaped.replace("\n", "<br>\n")
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Evaluation Report</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 1100px; margin: 32px auto; padding: 0 18px; line-height: 1.55; color: #111827; }}
h1,h2,h3 {{ color: #1e3a8a; }}
code {{ background: #f1f5f9; padding: 2px 4px; border-radius: 4px; }}
strong {{ color: #111827; }}
</style></head><body>{escaped}</body></html>"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate control vs RAG proof outputs using an AI judge.")
    parser.add_argument("--run-dir", type=Path, default=None, help="Run directory under reports/control_vs_rag. Defaults to latest run.")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--reasoning-effort", choices=["none", "low", "medium", "high"], default=DEFAULT_REASONING_EFFORT)
    parser.add_argument("--max-completion-tokens", type=int, default=DEFAULT_MAX_COMPLETION_TOKENS)
    parser.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--redo", action="store_true", help="Recompute existing evaluation.jsonl instead of resuming.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    agent = load_agent()
    agent.load_dotenv()
    api_key = agent.os.environ.get("OPENAI_API_KEY", "").strip()
    if not args.dry_run and (not api_key or api_key == "your-openai-api-key-here"):
        raise RuntimeError("OPENAI_API_KEY missing or placeholder. Set .env or export it before running.")

    run_dir = args.run_dir.resolve() if args.run_dir else latest_run_dir(DEFAULT_REPORT_ROOT)
    inputs = read_jsonl(run_dir / "inputs.jsonl")
    outputs = read_jsonl(run_dir / "outputs.jsonl")
    if args.limit is not None:
        inputs = inputs[: args.limit]

    grouped = group_outputs(outputs)
    eval_path = run_dir / "evaluation.jsonl"
    report_md_path = run_dir / "evaluation_report.md"
    report_html_path = run_dir / "evaluation_report.html"

    existing: Dict[str, Dict[str, Any]] = {}
    if eval_path.exists() and not args.redo:
        for row in read_jsonl(eval_path):
            if row.get("input_id"):
                existing[str(row["input_id"])] = row

    print(f"Run directory: {run_dir}")
    print(f"Inputs selected: {len(inputs)}")
    print(f"Existing evaluations: {len(existing)}")
    print(f"Criterion: {CRITERION}")

    if args.dry_run:
        for item in inputs:
            iid = input_id(item)
            pair = grouped.get(iid, {})
            print(f"- {iid}: control={'yes' if pair.get('control') else 'no'}, rag={'yes' if pair.get('library_rag') else 'no'}")
        print("Dry run: no API calls.")
        return 0

    reasoning_effort = None if args.reasoning_effort == "none" else args.reasoning_effort
    evaluations: List[Dict[str, Any]] = []
    if eval_path.exists() and args.redo:
        eval_path.unlink()

    for idx, item in enumerate(inputs, start=1):
        iid = input_id(item, idx)
        if iid in existing and not args.redo:
            print(f"[{idx}/{len(inputs)}] {iid}: already evaluated")
            evaluations.append(existing[iid])
            continue
        pair = grouped.get(iid, {})
        control = pair.get("control")
        rag = pair.get("library_rag")
        if not control or not rag:
            evaluation = {
                "input_id": iid,
                "error": "missing control or library_rag output",
                "has_control": bool(control),
                "has_library_rag": bool(rag),
                "evaluated_at": now_iso(),
            }
            append_jsonl(eval_path, evaluation)
            evaluations.append(evaluation)
            continue

        print(f"[{idx}/{len(inputs)}] evaluating {iid} — {input_title(item)}", flush=True)
        try:
            evaluation = call_judge(
                agent=agent,
                item=item,
                control=control,
                rag=rag,
                model=args.model,
                reasoning_effort=reasoning_effort,
                max_completion_tokens=args.max_completion_tokens,
                temperature=args.temperature,
            )
        except Exception as exc:  # noqa: BLE001
            evaluation = {
                "input_id": iid,
                "error": str(exc),
                "evaluated_at": now_iso(),
                "judge_model": args.model,
            }
        append_jsonl(eval_path, evaluation)
        evaluations.append(evaluation)

    # Include any existing rows not in this selected subset only if not redo.
    if not args.redo:
        selected_ids = {input_id(item, idx) for idx, item in enumerate(inputs, start=1)}
        for iid, row in existing.items():
            if iid not in selected_ids:
                evaluations.append(row)

    report_md = make_report_md(inputs, evaluations)
    report_md_path.write_text(report_md, encoding="utf-8")
    report_html_path.write_text(markdown_to_html(report_md), encoding="utf-8")
    print(f"Wrote evaluations: {eval_path}")
    print(f"Wrote Markdown report: {report_md_path}")
    print(f"Wrote HTML report: {report_html_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
