#!/usr/bin/env python3
"""
Generate a side-by-side HTML visualizer for Control vs Library-RAG batch results, with optional inline evaluator annotations.

Default behavior:
  - finds the latest run under reports/control_vs_rag/run_*/
  - reads inputs.jsonl and outputs.jsonl
  - optionally reads evaluation.jsonl, if present
  - writes comparison_viewer.html into that run directory

Usage:
  .venv/bin/python tools/visualize_control_vs_rag_results.py

Specify a run:
  .venv/bin/python tools/visualize_control_vs_rag_results.py \
    --run-dir reports/control_vs_rag/run_20260924_144730

Open after generating:
  open reports/control_vs_rag/<run>/comparison_viewer.html
"""

from __future__ import annotations

import argparse
import copy
import importlib.util
from urllib.parse import quote
import html
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT_ROOT = PROJECT_ROOT / "reports" / "control_vs_rag"


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


def latest_run_dir(root: Path) -> Path:
    if not root.exists():
        raise FileNotFoundError(f"Report root not found: {root}")
    candidates = [p for p in root.iterdir() if p.is_dir() and (p / "outputs.jsonl").exists()]
    if not candidates:
        raise FileNotFoundError(f"No run directories with outputs.jsonl found under {root}")
    return max(candidates, key=lambda p: p.stat().st_mtime)


def input_id(item: Dict[str, Any], index: Optional[int] = None) -> str:
    """Use the same id priority as run_control_vs_rag.py.

    The sampled test data has both `test_item_id` and `number_key`, but the batch
    runner uses `number_key` as `input_id`. If this visualizer prefers
    `test_item_id`, every output appears missing.
    """
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


def prompt_text(item: Dict[str, Any], cleaned_prompts_by_input: Optional[Dict[str, Dict[str, Any]]] = None, index: Optional[int] = None) -> str:
    iid = input_id(item, index)
    if cleaned_prompts_by_input and iid in cleaned_prompts_by_input:
        cleaned = str(cleaned_prompts_by_input[iid].get("prompt_cleaned") or "").strip()
        if cleaned:
            return cleaned
    return "Can you prove this theorem? " + statement_text(item)


def group_outputs(outputs: List[Dict[str, Any]]) -> Dict[str, Dict[str, Dict[str, Any]]]:
    grouped: Dict[str, Dict[str, Dict[str, Any]]] = {}
    for out in outputs:
        iid = str(out.get("input_id") or "input")
        cond = str(out.get("condition") or "unknown")
        grouped.setdefault(iid, {})[cond] = out
    return grouped


def escape(value: Any) -> str:
    return html.escape(str(value if value is not None else ""))


def render_text(value: Any) -> str:
    text = escape(value)
    # Basic Markdown-ish rendering after escaping.
    text = re.sub(r"```([\s\S]*?)```", lambda m: f"<pre>{m.group(1).strip()}</pre>", text)
    text = re.sub(r"\*\*([^*\n][\s\S]*?[^*\n])\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    # Render rewrite/highlight tags and inline strategy tags if present.
    text = re.sub(
        r"\[CONTROL_SECTION:\s*([^|\]\n]+)\s*\|\s*([^\]\n]+)\]\s*([\s\S]*?)\s*\[/CONTROL_SECTION\]",
        lambda m: (
            f'<div class="proof-highlight control-ref" title="Control section {m.group(1).strip()}: {m.group(2).strip()}">'
            f'{m.group(3).strip()}'
            '</div>'
        ),
        text,
    )
    text = re.sub(
        r"\[RAG_ELABORATED_SECTION:\s*([^|\]\n]+)\s*\|\s*([^\]\n]+)\]\s*([\s\S]*?)\s*\[/RAG_ELABORATED_SECTION\]",
        lambda m: (
            f'<div class="proof-highlight elaborated" title="Elaborated RAG section {m.group(1).strip()}: {m.group(2).strip()}">'
            f'{m.group(3).strip()}'
            '</div>'
        ),
        text,
    )
    text = re.sub(
        r"\[RAG_OMITTED_SECTION:\s*([^|\]\n]+)\s*\|\s*([^\]\n]+)\]\s*([\s\S]*?)\s*\[/RAG_OMITTED_SECTION\]",
        lambda m: (
            f'<div class="proof-highlight omitted" title="Omitted/compressed RAG section {m.group(1).strip()}: {m.group(2).strip()}">'
            f'{m.group(3).strip()}'
            '</div>'
        ),
        text,
    )
    text = re.sub(
        r"\[ELABORATED_SECTION:\s*([^\]\n]+)\]\s*([\s\S]*?)\s*\[/ELABORATED_SECTION\]",
        lambda m: (
            f'<div class="proof-highlight elaborated" title="Elaborated section: {m.group(1).strip()}">'
            f'{m.group(2).strip()}'
            '</div>'
        ),
        text,
    )
    text = re.sub(
        r"\[OMITTED_SECTION:\s*([^\]\n]+)\]\s*([\s\S]*?)\s*\[/OMITTED_SECTION\]",
        lambda m: (
            f'<div class="proof-highlight omitted" title="Omitted/compressed section: {m.group(1).strip()}">'
            f'{m.group(2).strip()}'
            '</div>'
        ),
        text,
    )
    text = re.sub(
        r"\[STRATEGY:\s*([^|\]\n]+)\s*\|\s*([^\]\n]+)\]\s*([\s\S]*?)\s*\[/STRATEGY\]",
        lambda m: (
            '<div class="strategy-card">'
            '<div class="strategy-card-title">Library strategy reference</div>'
            f'<div class="strategy-card-meta">{m.group(1).strip()} · {m.group(2).strip()}</div>'
            f'<div class="strategy-card-body">{m.group(3).strip()}</div>'
            '</div>'
        ),
        text,
    )
    text = re.sub(
        r"\[NEW_STRATEGY:\s*([^\]\n]+)\]\s*([\s\S]*?)\s*\[/NEW_STRATEGY\]",
        lambda m: (
            '<div class="strategy-card new">'
            '<div class="strategy-card-title">Proposed new strategy</div>'
            f'<div class="strategy-card-meta">{m.group(1).strip()}</div>'
            f'<div class="strategy-card-body">{m.group(2).strip()}</div>'
            '</div>'
        ),
        text,
    )
    return text


def tokenize(text: str) -> set[str]:
    return {t.lower() for t in re.findall(r"[A-Za-z][A-Za-z0-9_\-]+", str(text or "")) if len(t) > 2}


def split_answer_blocks(answer: str) -> List[str]:
    """Split an answer into display blocks for localized annotations.

    Keep explicit markup blocks such as [ELABORATED_SECTION] and
    [OMITTED_SECTION] intact even when they contain many blank lines/equations.
    """
    text = str(answer or "").strip()
    if not text:
        return [""]

    tag_re = re.compile(
        r"\[(?P<tag>CONTROL_SECTION|RAG_ELABORATED_SECTION|RAG_OMITTED_SECTION|ELABORATED_SECTION|OMITTED_SECTION|STRATEGY|NEW_STRATEGY):[^\]]+\]"
        r"[\s\S]*?"
        r"\[/(?P=tag)\]"
    )
    blocks: List[str] = []
    pos = 0
    for m in tag_re.finditer(text):
        before = text[pos:m.start()].strip()
        if before:
            blocks.extend(p.strip() for p in re.split(r"\n\s*\n", before) if p.strip())
        blocks.append(m.group(0).strip())
        pos = m.end()
    tail = text[pos:].strip()
    if tail:
        blocks.extend(p.strip() for p in re.split(r"\n\s*\n", tail) if p.strip())

    if len(blocks) <= 1:
        # Fallback sentence-ish chunks for single-paragraph outputs.
        sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", text)
        chunks: List[str] = []
        current: List[str] = []
        for sent in sentences:
            current.append(sent)
            if len(" ".join(current)) > 450:
                chunks.append(" ".join(current).strip())
                current = []
        if current:
            chunks.append(" ".join(current).strip())
        return chunks or [text]
    return blocks


def best_block_index(blocks: List[str], quote: str) -> int:
    quote = str(quote or "").strip()
    if not blocks or not quote:
        return 0
    quote_lower = quote.lower()
    for i, block in enumerate(blocks):
        if quote_lower and quote_lower in block.lower():
            return i
    q_tokens = tokenize(quote)
    best_i = 0
    best_score = -1.0
    for i, block in enumerate(blocks):
        b_tokens = tokenize(block)
        if not q_tokens or not b_tokens:
            score = 0.0
        else:
            score = len(q_tokens & b_tokens) / max(1, len(q_tokens))
        if score > best_score:
            best_score = score
            best_i = i
    return best_i


def evaluation_annotations_for_rag(answer: str, evaluation: Optional[Dict[str, Any]]) -> Dict[int, List[str]]:
    """Map evaluator worked/improvement notes onto Library-RAG answer block indices."""
    blocks = split_answer_blocks(answer)
    annotations: Dict[int, List[str]] = {}
    if not evaluation:
        return annotations

    worked_items = evaluation.get("rag_worked_sections", evaluation.get("control_worked_sections", [])) or []
    for item in worked_items:
        if not isinstance(item, dict):
            continue
        quote = str(item.get("section_or_quote", ""))
        idx = best_block_index(blocks, quote)
        note = (
            '<div class="eval-note worked">'
            '<div class="eval-note-title">Evaluation: worked well</div>'
            f'<div><strong>RAG proof passage:</strong> {render_text(quote)}</div>'
            + (f'<div><strong>Related strategy block:</strong> {render_text(item.get("related_strategy_block", ""))}</div>' if item.get("related_strategy_block") else '')
            + (f'<div><strong>Corresponding control section:</strong> {render_text(item.get("corresponding_control_section", ""))}</div>' if item.get("corresponding_control_section") else '')
            + f'<div><strong>Why:</strong> {render_text(item.get("why_it_worked", ""))}</div>'
            '</div>'
        )
        annotations.setdefault(idx, []).append(note)

    improvement_items = evaluation.get("rag_needs_improvement_sections", evaluation.get("control_needs_improvement_sections", [])) or []
    for item in improvement_items:
        if not isinstance(item, dict):
            continue
        quote = str(item.get("section_or_quote", ""))
        idx = best_block_index(blocks, quote)
        note = (
            '<div class="eval-note improve">'
            '<div class="eval-note-title">Evaluation: needs improvement</div>'
            f'<div><strong>RAG proof passage:</strong> {render_text(quote)}</div>'
            + (f'<div><strong>Related strategy block:</strong> {render_text(item.get("related_strategy_block", ""))}</div>' if item.get("related_strategy_block") else '')
            + (f'<div><strong>Corresponding control section:</strong> {render_text(item.get("corresponding_control_section", ""))}</div>' if item.get("corresponding_control_section") else '')
            + f'<div><strong>Issue:</strong> {render_text(item.get("issue", ""))}</div>'
            + f'<div><strong>Suggested revision:</strong> {render_text(item.get("suggested_revision", ""))}</div>'
            '</div>'
        )
        annotations.setdefault(idx, []).append(note)
    return annotations


def extract_pairs_from_rag_markup(rag_answer: str) -> List[Dict[str, Any]]:
    """Extract paired control/RAG modification markers emitted by the new RAG prompt."""
    controls: Dict[str, Dict[str, str]] = {}
    rags: Dict[str, Dict[str, str]] = {}
    for m in re.finditer(r"\[CONTROL_SECTION:\s*([^|\]\n]+)\s*\|\s*([^\]\n]+)\]\s*([\s\S]*?)\s*\[/CONTROL_SECTION\]", rag_answer or ""):
        pid = m.group(1).strip()
        controls[pid] = {"label": m.group(2).strip(), "text": m.group(3).strip()}
    for tag, judgment in [("RAG_ELABORATED_SECTION", "worked_well"), ("RAG_OMITTED_SECTION", "needs_improvement")]:
        pattern = rf"\[{tag}:\s*([^|\]\n]+)\s*\|\s*([^\]\n]+)\]\s*([\s\S]*?)\s*\[/{tag}\]"
        for m in re.finditer(pattern, rag_answer or ""):
            pid = m.group(1).strip()
            rags[pid] = {"label": m.group(2).strip(), "text": m.group(3).strip(), "judgment": judgment}
    pairs: List[Dict[str, Any]] = []
    for pid, rag in rags.items():
        ctrl = controls.get(pid, {})
        pairs.append({
            "pair_id": pid,
            "judgment": rag.get("judgment", "linked"),
            "rag_section_or_quote": rag.get("text", ""),
            "control_section_or_quote": ctrl.get("text", ""),
            "summary": f"{rag.get('label', '')}".strip(),
            "related_strategy_block": "",
        })
    return pairs


def build_paired_annotations(
    control_answer: str,
    rag_answer: str,
    evaluation: Optional[Dict[str, Any]],
) -> tuple[Dict[int, List[Dict[str, str]]], Dict[int, List[Dict[str, str]]], List[Dict[str, Any]]]:
    """Create matched control/RAG block annotations from evaluator pairs."""
    control_blocks = split_answer_blocks(control_answer)
    rag_blocks = split_answer_blocks(rag_answer)
    control_ann: Dict[int, List[Dict[str, str]]] = {}
    rag_ann: Dict[int, List[Dict[str, str]]] = {}
    pair_links: List[Dict[str, Any]] = []

    # Prefer explicit paired tags emitted by the RAG proof itself. These should
    # work even when there is no evaluation.jsonl file.
    markup_pairs = extract_pairs_from_rag_markup(rag_answer)
    paired = evaluation.get("paired_section_links") if evaluation and isinstance(evaluation.get("paired_section_links"), list) else []

    # Backward/robust fallback: derive pairs from worked/improvement sections.
    derived: List[Dict[str, Any]] = []
    for kind, key in [("worked_well", "rag_worked_sections"), ("needs_improvement", "rag_needs_improvement_sections")]:
        for idx, item in enumerate((evaluation or {}).get(key, []) or [], start=1):
            if not isinstance(item, dict):
                continue
            derived.append({
                "pair_id": item.get("pair_id") or f"{kind}_{idx}",
                "judgment": kind,
                "rag_section_or_quote": item.get("section_or_quote", ""),
                "control_section_or_quote": item.get("corresponding_control_section", ""),
                "summary": item.get("why_it_worked") or item.get("issue") or item.get("suggested_revision") or "",
                "related_strategy_block": item.get("related_strategy_block", ""),
            })

    pairs = markup_pairs or paired or derived
    details_by_pair: Dict[str, Dict[str, Any]] = {}
    for item in ((evaluation or {}).get("rag_worked_sections", []) or []) + ((evaluation or {}).get("rag_needs_improvement_sections", []) or []):
        if isinstance(item, dict) and item.get("pair_id"):
            details_by_pair[str(item.get("pair_id"))] = item

    for n, pair in enumerate(pairs, start=1):
        if not isinstance(pair, dict):
            continue
        pair_id = re.sub(r"[^A-Za-z0-9_\-]", "_", str(pair.get("pair_id") or f"pair_{n}"))
        judgment = str(pair.get("judgment") or "linked")
        rag_quote = str(pair.get("rag_section_or_quote") or pair.get("section_or_quote") or "")
        control_quote = str(pair.get("control_section_or_quote") or pair.get("corresponding_control_section") or "")
        summary = str(pair.get("summary") or "")
        detail = details_by_pair.get(pair_id, {})
        if not summary:
            summary = str(detail.get("why_it_worked") or detail.get("issue") or detail.get("suggested_revision") or "")
        related_strategy = str(pair.get("related_strategy_block") or detail.get("related_strategy_block") or "")

        rag_idx = best_block_index(rag_blocks, rag_quote)
        control_idx = best_block_index(control_blocks, control_quote) if control_quote else 0
        note_cls = "worked" if judgment == "worked_well" else "improve" if judgment == "needs_improvement" else "linked"

        rag_note = (
            f'<div class="eval-note {note_cls}" data-pair="{escape(pair_id)}">'
            f'<div class="eval-note-title">Linked evaluation: {escape(judgment.replace("_", " "))}</div>'
            + (f'<div><strong>Related strategy block:</strong> {render_text(related_strategy)}</div>' if related_strategy else '')
            + (f'<div><strong>Corresponding control section:</strong> {render_text(control_quote)}</div>' if control_quote else '')
            + (f'<div><strong>Comparison:</strong> {render_text(summary)}</div>' if summary else '')
            + '</div>'
        )
        action = "elaborated in RAG" if judgment == "worked_well" else "compressed/omitted in RAG" if judgment == "needs_improvement" else "modified in RAG"
        control_note = (
            f'<div class="eval-note linked" data-pair="{escape(pair_id)}">'
            f'<div class="eval-note-title">Original proof section {escape(action)}</div>'
            + (f'<div><strong>RAG replacement/modification:</strong> {render_text(rag_quote)}</div>' if rag_quote else '')
            + (f'<div><strong>Reason:</strong> {render_text(summary)}</div>' if summary else '')
            + '</div>'
        )
        rag_ann.setdefault(rag_idx, []).append({"pair_id": pair_id, "html": rag_note})
        control_ann.setdefault(control_idx, []).append({"pair_id": pair_id, "html": control_note})
        pair_links.append({"pair_id": pair_id, "control_idx": control_idx, "rag_idx": rag_idx, "judgment": judgment})
    return control_ann, rag_ann, pair_links


def render_answer_blocks(answer: str, *, linked_annotations: Optional[Dict[int, List[Dict[str, str]]]] = None) -> str:
    """Render exactly the raw model answer, without highlights or annotations."""
    return f'<div class="answer-block raw-answer">{escape(str(answer or ""))}</div>'


def render_evaluation_summary(evaluation: Optional[Dict[str, Any]]) -> str:
    if not evaluation:
        return ""
    if evaluation.get("error"):
        return f'<div class="eval-summary error-box">Evaluation error: {escape(evaluation.get("error"))}</div>'
    return f"""
    <div class="eval-summary">
      <div class="small-title">AI evaluation of Library-RAG</div>
      <span class="meta-pill">control: {escape(evaluation.get('control_score_1_to_5'))}/5</span>
      <span class="meta-pill">rag: {escape(evaluation.get('rag_score_1_to_5'))}/5</span>
      <span class="meta-pill">winner: {escape(evaluation.get('winner'))}</span>
      <div class="eval-overall">{render_text(evaluation.get('rag_overall_assessment', evaluation.get('control_overall_assessment', '')))}</div>
    </div>
    """


def render_nodes(nodes: Any) -> str:
    if not isinstance(nodes, list) or not nodes:
        return "<span class='muted'>None</span>"
    parts = []
    for node in nodes:
        if not isinstance(node, dict):
            continue
        parts.append(
            f"<span class='node-chip'><code>{escape(node.get('id'))}</code> · {escape(node.get('label'))}</span>"
        )
    return "".join(parts) or "<span class='muted'>None</span>"


def output_meta(out: Optional[Dict[str, Any]]) -> str:
    if not out:
        return "<span class='muted'>Missing output</span>"
    bits = []
    for key in ["model", "reasoning_effort", "max_completion_tokens", "elapsed_seconds"]:
        if out.get(key) is not None:
            label = key.replace("_", " ")
            bits.append(f"<span class='meta-pill'>{escape(label)}: {escape(out.get(key))}</span>")
    if out.get("error"):
        bits.append(f"<span class='meta-pill error'>error</span>")
    return "".join(bits)


def library_graph_for(out):
    graph = out.get("library_graph")
    if isinstance(graph, dict) and isinstance(graph.get("nodes"), list):
        return graph
    path = PROJECT_ROOT / "data" / "train" / "general" / "strategy_hierarchy.json"
    if not path.exists():
        raise FileNotFoundError(f"Cannot resolve original library names: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_output(out):
    """Resolve library headings by ID, including results generated before this fix."""
    if not isinstance(out.get("annotated_control"), dict):
        return out
    result = copy.deepcopy(out)
    graph = library_graph_for(result)
    labels = {n["id"]: n["label"] for n in graph["nodes"]}
    for span in result["annotated_control"].get("highlights", []) + result.get("changes", []):
        if span.get("kind") == "library":
            if span.get("node_id") not in labels:
                raise ValueError(f"Unknown library strategy: {span.get('node_id')}")
            span["strategy"] = labels[span["node_id"]]
    return result


def graph_reference_link(iid):
    return "strategy_hierarchy_graph.html#proof=" + quote(str(iid), safe="")


def write_graph_reference_page(outputs, output_path):
    references = {}
    graphs = {}
    for raw in outputs:
        if not isinstance(raw.get("annotated_control"), dict):
            continue
        out = canonical_output(raw)
        graph = library_graph_for(out)
        # Keep a separate snapshot per proof if the library changed between runs.
        iid = str(out["input_id"])
        graphs[iid] = graph
        references[iid] = {"title": out.get("name") or iid, "steps": [
            {"id": h["id"], "node_id": h.get("node_id", ""), "kind": h["kind"],
             "label": h["strategy"], "annotation": h["annotation"]}
            for h in sorted(out["annotated_control"].get("highlights", []), key=lambda h: h["start"])
        ]}
    if not references:
        return
    path = PROJECT_ROOT / "workflows" / "library_hierarchy" / "visualize_strategy_hierarchy.py"
    spec = importlib.util.spec_from_file_location("proof_graph_viewer", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.render_html(next(iter(graphs.values())), output_path, proof_references=references, proof_graphs=graphs)


def render_structured_proofs(rag: Dict[str, Any], case_index: int) -> tuple[str, str]:
    """Use exact original offsets, never fuzzy quote matching, for the new pipeline."""
    proof = str(rag.get("direct_draft") or "")
    annotated = rag.get("annotated_control") or {}
    highlights = annotated.get("highlights", [])
    changes = sorted(rag.get("changes", []), key=lambda e: e["start"])
    by_id = {e["id"]: e for e in changes}
    decisions = {e["id"]: e for e in rag.get("node2_decisions", [])}
    cursor, rebuilt = 0, []
    for e in changes:
        if not (cursor <= e["start"] < e["end"] <= len(proof)):
            raise ValueError("Invalid or overlapping change offsets")
        if proof[e["start"]:e["end"]] != e["quote"]:
            raise ValueError("Change quote does not match the control proof")
        rebuilt.extend([proof[cursor:e["start"]], e["replacement"]])
        cursor = e["end"]
    rebuilt.append(proof[cursor:])
    if "".join(rebuilt) != rag.get("answer", ""):
        raise ValueError("Stored changes do not reconstruct the revised proof")

    def pane(revised):
        spans = changes if revised else sorted(
            highlights + [e for e in changes if e["stage"] == 3], key=lambda e: e["start"]
        )
        parts, cursor = [], 0
        for span in spans:
            start, end = span["start"], span["end"]
            if not (cursor <= start < end <= len(proof)) or proof[start:end] != span["quote"]:
                raise ValueError("Invalid highlight offsets")
            parts.append(render_text(proof[cursor:start]))
            pid = f"case{case_index}-" + re.sub(r"[^a-zA-Z0-9_-]", "_", str(span["id"]))
            side, other = ("rag", "control") if revised else ("control", "rag")
            edit = by_id.get(span["id"])
            action = edit["action"] if edit else "keep"
            text = span["replacement"] if revised else proof[start:end]
            body = render_text(text) if text else '<span class="omission-line" aria-label="Passage omitted"></span>'
            linked = ' linked-block' if edit else ''
            pair_attr = f' data-pairs="{pid}"' if edit else ''
            color = 'omitted' if revised and action in {'omit', 'compress'} else 'elaborated' if revised else 'control-ref'
            parts.append(f'<span class="proof-highlight answer-block {color}{linked}" id="{pid}-{side}"{pair_attr}>{body}')
            if edit:
                label = {"elaborate": "Elaborated", "compress": "Compressed", "omit": "Omitted"}[action]
                parts.append(f'<a class="pair-jump" href="#{pid}-{other}" aria-label="Go to corresponding {other} passage">{label} · {escape(span["id"])} ↔</a>')
            parts.append('</span>')
            if not revised and span.get("annotation"):
                origin = 'Library strategy' if span.get('kind') == 'library' else 'Proposed new strategy'
                decision = decisions.get(span['id'], {})
                note = span['annotation']
                if decision.get('reason'):
                    note += ' ' + decision['reason']
                parts.append('<span class="strategy-annotation"><strong>' + escape(origin + ': ' + span.get('strategy', ''))
                             + '</strong><span>' + render_text(note) + '</span></span>')
            elif revised and span.get('reason'):
                parts.append('<span class="strategy-annotation">' + render_text(span['reason']) + '</span>')
            cursor = end
        parts.append(render_text(proof[cursor:]))
        return '<div class="answer-block structured-answer">' + ''.join(parts) + '</div>'
    return pane(False), pane(True)


def render_pair(
    item: Dict[str, Any],
    idx: int,
    outputs_by_input: Dict[str, Dict[str, Dict[str, Any]]],
    evaluations_by_input: Dict[str, Dict[str, Any]],
    cleaned_prompts_by_input: Dict[str, Dict[str, Any]],
) -> str:
    iid = input_id(item, idx)
    pair = outputs_by_input.get(iid, {})
    control = pair.get("control")
    rag = pair.get("library_rag")
    prompt = prompt_text(item, cleaned_prompts_by_input, idx)
    evaluation = evaluations_by_input.get(iid)
    control_answer = control.get("answer", "") if control else "[missing]"
    rag_answer = rag.get("answer", "") if rag else "[missing]"
    structured = bool(rag and isinstance(rag.get("annotated_control"), dict) and "changes" in rag)
    rendered = {}
    if structured:
        left, right = render_structured_proofs(rag, idx)
        rendered = {"control": left, "rag": right}
        if not control:
            control = {**rag, "answer": rag["direct_draft"]}
    control_annotations: Dict[int, List[Dict[str, str]]] = {}
    rag_annotations: Dict[int, List[Dict[str, str]]] = {}
    pair_links: List[Dict[str, Any]] = []

    def result_column(label: str, out: Optional[Dict[str, Any]], css_class: str, annotations: Dict[int, List[Dict[str, str]]]) -> str:
        answer = out.get("answer", "") if out else "[missing]"
        error = out.get("error", "") if out else ""
        return f"""
        <section class="result-col {css_class}">
          <div class="col-header">
            <h3>{escape(label)}</h3>
            <button class="copy-btn" data-copy="{escape(answer)}">Copy raw</button>
          </div>
          <div class="meta-row">{output_meta(out)}</div>
          {f'<div class="error-box">{escape(error)}</div>' if error else ''}
          <div class="answer-box">{rendered.get(css_class, render_answer_blocks(answer))}</div>
        </section>
        """

    return f"""
    <article class="case" id="case-{escape(iid)}">
      <div class="case-title">
        <h2>{idx}. {escape(input_title(item))}</h2>
        <div class="case-id"><code>{escape(iid)}</code></div>
      </div>
      <div class="prompt-box global-prompt">
        <div class="small-title">Prompt</div>
        <div class="prompt-text">{render_text(prompt)}</div>
        {(f'<a class="graph-reference" href="{escape(graph_reference_link(iid))}" target="_blank" rel="noopener">Graph reference ↗</a>' if structured else '')}
      </div>
      {('<div class="comparison-toolbar"><span>Blue: original strategy steps</span><span>Green: elaborated</span><span>Grey: compressed or omitted</span><label><input class="annotation-toggle" type="checkbox" checked> Strategy annotations</label></div>' if structured else '')}
      <div class="split" data-pair-links='{escape(json.dumps(pair_links, ensure_ascii=False))}'>
        <svg class="link-layer" aria-hidden="true"></svg>
        {result_column('Control', control, 'control', control_annotations)}
        {result_column('Library-RAG', rag, 'rag', rag_annotations)}
      </div>
    </article>
    """


def make_html(
    run_dir: Path,
    inputs: List[Dict[str, Any]],
    outputs: List[Dict[str, Any]],
    evaluations: List[Dict[str, Any]],
    cleaned_prompts: List[Dict[str, Any]],
) -> str:
    grouped = group_outputs([canonical_output(out) for out in outputs])
    evaluations_by_input = {str(e.get("input_id")): e for e in evaluations if e.get("input_id")}
    cleaned_prompts_by_input = {str(e.get("input_id")): e for e in cleaned_prompts if e.get("input_id")}
    nav = []
    cases = []
    for idx, item in enumerate(inputs, start=1):
        iid = input_id(item, idx)
        title = input_title(item)
        nav.append(f"<a href='#case-{escape(iid)}'>{idx}. {escape(title)}</a>")
        cases.append(render_pair(item, idx, grouped, evaluations_by_input, cleaned_prompts_by_input))

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Control vs Library-RAG Visualizer</title>
  <script>
    window.MathJax = {{
      tex: {{ inlineMath: [['\\\\(', '\\\\)'], ['$', '$']], displayMath: [['\\\\[', '\\\\]'], ['$$', '$$']], processEscapes: true }},
      svg: {{ fontCache: 'global' }}
    }};
  </script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
  <style>
    :root {{ --bg:#f8fafc; --panel:#fff; --border:#dbe3ef; --text:#111827; --muted:#64748b; --blue:#1d4ed8; --cyan:#155e75; }}
    * {{ box-sizing: border-box; }}
    body {{ margin:0; background:var(--bg); color:var(--text); font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; }}
    header {{ position: sticky; top:0; z-index:10; background:#0f172a; color:white; padding:16px 22px; box-shadow:0 2px 10px rgba(15,23,42,.18); }}
    header h1 {{ margin:0 0 4px; font-size:22px; }}
    header .sub {{ color:#cbd5e1; font-size:13px; }}
    .layout {{ display:grid; grid-template-columns:260px 1fr; gap:0; }}
    nav {{ position:sticky; top:72px; align-self:start; height:calc(100vh - 72px); overflow:auto; padding:14px; border-right:1px solid var(--border); background:white; }}
    nav h2 {{ font-size:12px; text-transform:uppercase; letter-spacing:.05em; color:var(--muted); margin:0 0 10px; }}
    nav a {{ display:block; padding:8px 9px; border-radius:8px; color:#1e3a8a; text-decoration:none; font-size:13px; line-height:1.25; }}
    nav a:hover {{ background:#eff6ff; }}
    main {{ padding:18px; min-width:0; }}
    .case {{ margin:0 0 26px; }}
    .case-title {{ display:flex; justify-content:space-between; align-items:end; gap:10px; margin:0 0 10px; }}
    .case-title h2 {{ margin:0; font-size:20px; }}
    .case-id {{ color:var(--muted); font-size:12px; }}
    .split {{ display:grid; grid-template-columns:1fr 1fr; gap:14px; align-items:start; position:relative; }}
    .link-layer {{ position:absolute; inset:0; width:100%; height:100%; pointer-events:none; z-index:4; overflow:visible; }}
    .link-layer path {{ stroke:#94a3b8; stroke-width:2; fill:none; opacity:.28; }}
    .link-layer path.active {{ stroke:#2563eb; stroke-width:4; opacity:.92; }}
    .link-layer path.locked {{ stroke:#1d4ed8; stroke-width:5; opacity:1; }}
    .result-col {{ background:var(--panel); border:1px solid var(--border); border-radius:14px; padding:13px; min-width:0; box-shadow:0 1px 5px rgba(15,23,42,.05); position:relative; z-index:3; }}
    .result-col.control {{ border-top:5px solid #6366f1; }}
    .result-col.rag {{ border-top:5px solid #06b6d4; }}
    .col-header {{ display:flex; justify-content:space-between; align-items:center; gap:8px; }}
    .col-header h3 {{ margin:0 0 8px; color:#111827; }}
    .copy-btn {{ border:0; border-radius:999px; padding:5px 9px; background:#eef2ff; color:#3730a3; font-weight:800; cursor:pointer; }}
    .prompt-box, .nodes-box {{ border:1px solid #e2e8f0; background:#f8fafc; border-radius:10px; padding:10px; margin:8px 0; }}
    .small-title {{ font-size:11px; font-weight:900; text-transform:uppercase; letter-spacing:.05em; color:var(--muted); margin-bottom:5px; }}
    .prompt-text {{ white-space:pre-wrap; font-size:13px; line-height:1.45; max-height:220px; overflow:auto; }}
    .meta-row {{ margin:8px 0; }}
    .meta-pill {{ display:inline-block; margin:2px 4px 2px 0; padding:4px 7px; border-radius:999px; background:#e0f2fe; color:#155e75; font-size:11px; font-weight:800; }}
    .meta-pill.error {{ background:#fee2e2; color:#991b1b; }}
    .node-chip {{ display:inline-block; margin:3px 4px 0 0; padding:4px 7px; border-radius:999px; background:#ecfeff; color:#155e75; font-size:11px; }}
    .answer-box {{ line-height:1.55; font-size:14px; overflow-wrap:anywhere; }}
    .answer-block {{ white-space:pre-wrap; margin:0 0 10px; padding:6px 0; }}
    .answer-block.annotated {{ background:#fffbeb; border-left:4px solid #f59e0b; padding:9px 10px; border-radius:8px; }}
    .answer-block.link-hover {{ outline:3px solid rgba(37,99,235,.35); background:#eff6ff; }}
    .answer-block.link-locked {{ outline:4px solid rgba(37,99,235,.55); background:#dbeafe; }}
    .eval-note.link-hover {{ outline:2px solid rgba(37,99,235,.35); }}
    .eval-note.link-locked {{ outline:3px solid rgba(37,99,235,.55); }}
    .eval-summary {{ border:1px solid #c7d2fe; background:#eef2ff; color:#312e81; border-radius:10px; padding:10px; margin:8px 0; }}
    .eval-overall {{ margin-top:6px; font-size:13px; line-height:1.45; }}
    .eval-note {{ white-space:normal; border-radius:10px; padding:10px; margin:-3px 0 12px 14px; font-size:13px; line-height:1.45; }}
    .eval-note.worked {{ background:#ecfdf5; border:1px solid #bbf7d0; color:#14532d; }}
    .eval-note.improve {{ background:#fff7ed; border:1px solid #fed7aa; color:#7c2d12; }}
    .eval-note.linked {{ background:#f8fafc; border:1px solid #cbd5e1; color:#334155; }}
    .eval-note-title {{ font-size:11px; font-weight:900; text-transform:uppercase; letter-spacing:.05em; margin-bottom:5px; }}
    .error-box {{ border:1px solid #fecaca; background:#fef2f2; color:#991b1b; border-radius:9px; padding:9px; margin:8px 0; white-space:pre-wrap; }}
    code {{ background:#f1f5f9; padding:1px 4px; border-radius:4px; }}
    pre {{ background:#0f172a; color:#e5e7eb; padding:10px; border-radius:9px; overflow:auto; }}
    .strategy-card {{ white-space:normal; margin:10px 0; padding:10px 12px; border-radius:12px; border:1px solid #bfdbfe; border-left:5px solid #2563eb; background:#eff6ff; color:#1e3a8a; }}
    .strategy-card.new {{ border-color:#fed7aa; border-left-color:#f97316; background:#fff7ed; color:#7c2d12; }}
    .proof-highlight {{ white-space:pre-wrap; margin:6px 0; padding:4px 6px; border-radius:6px; border-left:4px solid transparent; }}
    .proof-highlight.elaborated {{ background:#ecfdf5; border-left-color:#16a34a; }}
    .proof-highlight.omitted {{ background:#f3f4f6; border-left-color:#6b7280; color:#374151; font-style:italic; }}
    .proof-highlight.control-ref {{ background:#eff6ff; border-left-color:#2563eb; color:#1e3a8a; }}
    .strategy-card-title {{ font-size:12px; font-weight:900; text-transform:uppercase; letter-spacing:.04em; margin-bottom:5px; }}
    .strategy-card-meta {{ font-size:12px; font-weight:800; margin-bottom:5px; }}
    .strategy-card-body {{ font-size:13px; line-height:1.45; }}
    .muted {{ color:var(--muted); }}
    .graph-reference {{ display:inline-block; margin-top:10px; padding:7px 12px; border-radius:8px; background:#e0e7ff; color:#3730a3; font-size:13px; font-weight:700; text-decoration:none; }}
    .comparison-toolbar {{ display:flex; flex-wrap:wrap; gap:14px; font-size:12px; color:#475569; margin:12px 0; align-items:center; }}
    .comparison-toolbar label {{ margin-left:auto; cursor:pointer; }}
    .structured-answer > .proof-highlight {{ display:block; margin:6px 0; font-style:normal; }}
    .strategy-annotation {{ display:block; white-space:normal; font-size:12px; line-height:1.5; color:#475569; border-left:2px solid #cbd5e1; padding:6px 10px; margin:4px 0 12px; }}
    .strategy-annotation strong, .strategy-annotation span {{ display:block; }}
    .hide-annotations .strategy-annotation {{ display:none; }}
    .pair-jump {{ display:block; width:fit-content; font:600 11px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif; color:#1d4ed8; margin-top:6px; text-decoration:none; }}
    .pair-jump:hover {{ text-decoration:underline; }}
    .omission-line {{ display:block; height:14px; border-top:3px solid #9ca3af; margin:12px 0 0; }}
    .linked-block {{ cursor:pointer; scroll-margin-top:110px; }}
    .case {{ scroll-margin-top:95px; }}
    mjx-container[display="true"] {{ overflow-x:auto; overflow-y:hidden; max-width:100%; }}
    @media (max-width: 980px) {{ .layout {{ grid-template-columns:1fr; }} nav {{ position:static; height:auto; border-right:0; border-bottom:1px solid var(--border); }} .split {{ grid-template-columns:1fr; }} }}
  </style>
</head>
<body>
  <header>
    <h1>Control vs Library-RAG Visualizer</h1>
    <div class="sub">Run: <code>{escape(run_dir.relative_to(PROJECT_ROOT) if PROJECT_ROOT in run_dir.parents else run_dir)}</code></div>
  </header>
  <div class="layout">
    <nav><h2>Cases</h2>{''.join(nav)}</nav>
    <main>{''.join(cases)}</main>
  </div>
  <script>
    document.querySelectorAll('.copy-btn').forEach((button) => {{
      button.addEventListener('click', async () => {{
        const raw = button.getAttribute('data-copy') || '';
        try {{
          await navigator.clipboard.writeText(raw);
          const old = button.textContent;
          button.textContent = 'Copied';
          setTimeout(() => button.textContent = old, 1200);
        }} catch (err) {{
          button.textContent = 'Copy failed';
          setTimeout(() => button.textContent = 'Copy raw', 1200);
        }}
      }});
    }});

    function pairsFor(el) {{
      return (el.getAttribute('data-pairs') || '').split(/\\s+/).filter(Boolean);
    }}

    function drawLinksForSplit(split) {{
      const svg = split.querySelector('.link-layer');
      if (!svg) return;
      svg.innerHTML = '';
      const splitRect = split.getBoundingClientRect();
      const blocks = Array.from(split.querySelectorAll('.linked-block'));
      const pairToBlocks = new Map();
      for (const block of blocks) {{
        for (const pair of pairsFor(block)) {{
          if (!pairToBlocks.has(pair)) pairToBlocks.set(pair, []);
          pairToBlocks.get(pair).push(block);
        }}
      }}
      for (const [pair, els] of pairToBlocks.entries()) {{
        if (els.length < 2) continue;
        const control = els.find(e => e.closest('.result-col.control')) || els[0];
        const rag = els.find(e => e.closest('.result-col.rag')) || els[1];
        if (!control || !rag || control === rag) continue;
        const a = control.getBoundingClientRect();
        const b = rag.getBoundingClientRect();
        const x1 = a.right - splitRect.left;
        const y1 = a.top + a.height / 2 - splitRect.top;
        const x2 = b.left - splitRect.left;
        const y2 = b.top + b.height / 2 - splitRect.top;
        const mid = (x1 + x2) / 2;
        const d = `M ${{x1}} ${{y1}} C ${{mid}} ${{y1}}, ${{mid}} ${{y2}}, ${{x2}} ${{y2}}`;
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.setAttribute('d', d);
        path.setAttribute('data-pair', pair);
        svg.appendChild(path);
      }}
    }}

    let lockedPair = null;

    function elementsForPair(pair) {{
      return document.querySelectorAll(`[data-pairs~="${{CSS.escape(pair)}}"], [data-pair="${{CSS.escape(pair)}}"]`);
    }}

    function setPairActive(pair, active) {{
      if (lockedPair === pair && !active) return;
      elementsForPair(pair).forEach(el => {{
        el.classList.toggle('link-hover', active);
        el.classList.toggle('active', active);
      }});
    }}

    function clearLockedPair() {{
      if (!lockedPair) return;
      elementsForPair(lockedPair).forEach(el => {{
        el.classList.remove('link-locked', 'locked', 'link-hover', 'active');
      }});
      lockedPair = null;
    }}

    function lockPair(pair) {{
      if (!pair) return;
      if (lockedPair === pair) {{
        clearLockedPair();
        return;
      }}
      clearLockedPair();
      lockedPair = pair;
      elementsForPair(pair).forEach(el => {{
        el.classList.add('link-locked', 'locked', 'link-hover', 'active');
      }});
    }}

    function setupLinkedHover() {{
      document.querySelectorAll('.split').forEach(drawLinksForSplit);
      document.querySelectorAll('.linked-block, .eval-note[data-pair]').forEach(el => {{
        const getPairs = () => el.hasAttribute('data-pair') ? [el.getAttribute('data-pair')] : pairsFor(el);
        el.addEventListener('mouseenter', () => getPairs().forEach(pair => pair && setPairActive(pair, true)));
        el.addEventListener('mouseleave', () => getPairs().forEach(pair => pair && setPairActive(pair, false)));
        el.addEventListener('click', (event) => {{
          event.stopPropagation();
          const pair = getPairs()[0];
          if (pair) lockPair(pair);
        }});
      }});
      document.addEventListener('click', () => clearLockedPair());
      document.addEventListener('keydown', (event) => {{
        if (event.key === 'Escape') clearLockedPair();
      }});
    }}

    document.querySelectorAll('.annotation-toggle').forEach(toggle => {{
      toggle.addEventListener('change', () => {{
        const article = toggle.closest('.case');
        article.classList.toggle('hide-annotations', !toggle.checked);
        article.querySelectorAll('.split').forEach(drawLinksForSplit);
      }});
    }});
    window.addEventListener('load', () => {{
      setupLinkedHover();
      if (window.MathJax && MathJax.startup && MathJax.startup.promise) {{
        MathJax.startup.promise.then(() => document.querySelectorAll('.split').forEach(drawLinksForSplit));
      }}
      const observer = new ResizeObserver(() => document.querySelectorAll('.split').forEach(drawLinksForSplit));
      document.querySelectorAll('.result-col').forEach(el => observer.observe(el));
    }});
    window.addEventListener('resize', () => {{
      document.querySelectorAll('.split').forEach(drawLinksForSplit);
      if (lockedPair) elementsForPair(lockedPair).forEach(el => el.classList.add("link-locked", "locked", "active"));
    }});
  </script>
</body>
</html>
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate side-by-side visualizer for Control vs RAG batch results.")
    parser.add_argument("--run-dir", type=Path, default=None, help="Run directory containing inputs.jsonl and outputs.jsonl. Defaults to latest under reports/control_vs_rag.")
    parser.add_argument("--output", type=Path, default=None, help="Output HTML path. Defaults to <run-dir>/comparison_viewer.html")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    run_dir = args.run_dir.resolve() if args.run_dir else latest_run_dir(DEFAULT_REPORT_ROOT)
    inputs_path = run_dir / "inputs.jsonl"
    outputs_path = run_dir / "outputs.jsonl"
    evaluations_path = run_dir / "evaluation.jsonl"
    prompt_cleaning_path = run_dir / "prompt_cleaning.jsonl"
    if not inputs_path.exists():
        raise FileNotFoundError(f"Missing inputs.jsonl in {run_dir}")
    if not outputs_path.exists():
        raise FileNotFoundError(f"Missing outputs.jsonl in {run_dir}")

    inputs = read_jsonl(inputs_path)
    outputs = read_jsonl(outputs_path)
    evaluations = read_jsonl(evaluations_path)
    cleaned_prompts = read_jsonl(prompt_cleaning_path)
    output_path = args.output or (run_dir / "comparison_viewer.html")
    write_graph_reference_page(outputs, output_path.parent / "strategy_hierarchy_graph.html")
    output_path.write_text(make_html(run_dir, inputs, outputs, evaluations, cleaned_prompts), encoding="utf-8")
    print(f"Read inputs: {len(inputs)}")
    print(f"Read outputs: {len(outputs)}")
    print(f"Read evaluations: {len(evaluations)}")
    print(f"Read cleaned prompts: {len(cleaned_prompts)}")
    print(f"Wrote visualizer: {output_path}")
    print(f"Open with: open {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
