#!/usr/bin/env python3
"""
Visualize the hierarchical proof-strategy graph produced by build_strategy_hierarchy.py.

Input:
  data/general/strategy_hierarchy.json

Outputs:
  data/general/strategy_hierarchy_graph.html
  data/general/strategy_hierarchy_graph.mmd

The HTML output is standalone and dependency-free: it uses absolutely-positioned
HTML cards plus an inline SVG edge layer. The Mermaid output is useful if you want
to paste the graph into Mermaid-compatible tools.
"""

from __future__ import annotations

import argparse
import html
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = PROJECT_ROOT / "data" / "general" / "strategy_hierarchy.json"
DEFAULT_HTML = PROJECT_ROOT / "data" / "general" / "strategy_hierarchy_graph.html"
DEFAULT_MERMAID = PROJECT_ROOT / "data" / "general" / "strategy_hierarchy_graph.mmd"

CARD_W = 330
CARD_H = 150
COL_GAP = 130
ROW_GAP = 34
MARGIN_X = 48
MARGIN_Y = 48


def read_graph(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(
            f"Missing hierarchy JSON: {path}\n"
            "Run first:\n"
            "  .venv/bin/python workflows/library_hierarchy/build_strategy_hierarchy.py"
        )
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object in {path}")
    return data


def safe_id(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_]+", "_", str(value or "node")).strip("_")
    return cleaned or "node"


def node_label(node: Dict[str, Any]) -> str:
    return str(node.get("label") or node.get("name") or node.get("id") or "Unnamed node")


def node_level(node: Dict[str, Any]) -> str:
    level = node.get("level", "unknown")
    return str(level)


def sort_level_key(level: str) -> Tuple[int, str]:
    try:
        return (0, f"{int(level):04d}")
    except Exception:
        return (1, level)


def source_summary(node: Dict[str, Any], max_items: int = 4) -> str:
    srcs = node.get("source_categories", [])
    if not isinstance(srcs, list) or not srcs:
        return ""
    parts: List[str] = []
    for src in srcs[:max_items]:
        if not isinstance(src, dict):
            continue
        sid = src.get("id", "")
        name = src.get("name", "")
        dataset = src.get("dataset", "")
        parts.append(f"{dataset}:{sid} {name}".strip())
    if len(srcs) > max_items:
        parts.append(f"+{len(srcs) - max_items} more")
    return "; ".join(parts)


def layout_nodes(nodes: List[Dict[str, Any]]) -> Tuple[Dict[str, Dict[str, Any]], int, int, List[str]]:
    levels: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for node in nodes:
        levels[node_level(node)].append(node)

    ordered_levels = sorted(levels.keys(), key=sort_level_key)
    positioned: Dict[str, Dict[str, Any]] = {}

    for col, level in enumerate(ordered_levels):
        level_nodes = levels[level]
        level_nodes.sort(key=lambda n: node_label(n).lower())
        x = MARGIN_X + col * (CARD_W + COL_GAP)
        for row, node in enumerate(level_nodes):
            y = MARGIN_Y + row * (CARD_H + ROW_GAP)
            nid = str(node.get("id") or safe_id(node_label(node)))
            positioned[nid] = {
                "node": node,
                "x": x,
                "y": y,
                "w": CARD_W,
                "h": CARD_H,
                "level": level,
            }

    width = MARGIN_X * 2 + max(1, len(ordered_levels)) * CARD_W + max(0, len(ordered_levels) - 1) * COL_GAP
    max_rows = max((len(v) for v in levels.values()), default=1)
    height = MARGIN_Y * 2 + max_rows * CARD_H + max(0, max_rows - 1) * ROW_GAP
    return positioned, width, height, ordered_levels


def edge_path(src: Dict[str, Any], tgt: Dict[str, Any]) -> str:
    x1 = src["x"] + src["w"]
    y1 = src["y"] + src["h"] / 2
    x2 = tgt["x"]
    y2 = tgt["y"] + tgt["h"] / 2
    mid = (x1 + x2) / 2
    return f"M{x1:.1f},{y1:.1f} C{mid:.1f},{y1:.1f} {mid:.1f},{y2:.1f} {x2:.1f},{y2:.1f}"


def edge_color(relation: str) -> str:
    relation = str(relation or "").lower()
    if relation == "parent_of":
        return "#2563eb"
    if relation in {"related_to", "cross_link", "overlaps_with"}:
        return "#9333ea"
    if relation in {"equivalent_to", "same_as"}:
        return "#059669"
    return "#64748b"


def render_html(graph: Dict[str, Any], output: Path) -> None:
    metadata = graph.get("metadata", {}) if isinstance(graph.get("metadata"), dict) else {}
    nodes = [n for n in graph.get("nodes", []) if isinstance(n, dict)]
    edges = [e for e in graph.get("edges", []) if isinstance(e, dict)]
    positioned, width, height, ordered_levels = layout_nodes(nodes)

    valid_edges = []
    for edge in edges:
        src = str(edge.get("source", ""))
        tgt = str(edge.get("target", ""))
        if src in positioned and tgt in positioned:
            valid_edges.append(edge)

    title = str(metadata.get("title") or "Hierarchical Proof Strategy Library")
    description = str(metadata.get("description") or "")

    svg_paths = []
    for edge in valid_edges:
        src_id = str(edge.get("source"))
        tgt_id = str(edge.get("target"))
        relation = str(edge.get("relation", "related_to"))
        color = edge_color(relation)
        rationale = html.escape(str(edge.get("rationale", "")))
        svg_paths.append(
            f'<path class="edge-path" data-source="{html.escape(src_id)}" data-target="{html.escape(tgt_id)}" '
            f'd="{edge_path(positioned[src_id], positioned[tgt_id])}" '
            f'stroke="{color}" stroke-width="2" fill="none" marker-end="url(#arrow)" '
            f'opacity="0.72"><title>{html.escape(relation)}: {rationale}</title></path>'
        )

    cards = []
    for nid, info in positioned.items():
        node = info["node"]
        label = html.escape(node_label(node))
        desc = html.escape(str(node.get("description", "")))
        sources = html.escape(source_summary(node))
        level = html.escape(info["level"])
        cards.append(
            f'''
            <div class="node-card" data-node-id="{html.escape(nid)}" style="left:{info['x']}px; top:{info['y']}px; width:{info['w']}px; height:{info['h']}px;">
              <div class="node-level">Level {level}</div>
              <div class="node-label">{label}</div>
              <div class="node-desc">{desc}</div>
              <div class="node-sources">{sources}</div>
              <div class="node-id">{html.escape(nid)}</div>
            </div>
            '''
        )

    level_legend = "".join(f'<span class="pill">Level {html.escape(level)}</span>' for level in ordered_levels)

    page = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      --bg: #f8fafc;
      --panel: #ffffff;
      --text: #111827;
      --muted: #64748b;
      --border: #dbe3ef;
      --blue: #2563eb;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: var(--bg); color: var(--text); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }}
    header {{ padding: 24px 28px; background: #0f172a; color: white; }}
    h1 {{ margin: 0 0 8px; font-size: 24px; }}
    .subtitle {{ color: #cbd5e1; max-width: 1100px; line-height: 1.45; }}
    .summary {{ display: flex; flex-wrap: wrap; gap: 10px; padding: 14px 28px; background: white; border-bottom: 1px solid var(--border); align-items: center; }}
    .pill {{ display: inline-block; padding: 5px 9px; border-radius: 999px; background: #e0f2fe; color: #075985; font-size: 12px; font-weight: 750; }}
    .graph-wrap {{ overflow: auto; padding: 24px; }}
    .graph-canvas {{ position: relative; width: {width}px; height: {height}px; min-width: {width}px; min-height: {height}px; }}
    svg.edge-layer {{ position: absolute; left: 0; top: 0; width: {width}px; height: {height}px; pointer-events: none; }}
    .edge-path {{ transition: opacity .12s ease, stroke-width .12s ease, filter .12s ease; }}
    .graph-canvas.dimmed .edge-path {{ opacity: 0.06; }}
    .graph-canvas.dimmed .edge-path.edge-active {{ opacity: 1; stroke-width: 5; filter: drop-shadow(0 0 3px rgba(37, 99, 235, .45)); }}
    .node-card {{ position: absolute; background: var(--panel); border: 1px solid var(--border); border-left: 5px solid var(--blue); border-radius: 12px; padding: 12px; box-shadow: 0 3px 10px rgba(15, 23, 42, 0.08); overflow: hidden; transition: opacity .12s ease, transform .12s ease, box-shadow .12s ease, border-color .12s ease; cursor: default; }}
    .graph-canvas.dimmed .node-card {{ opacity: 0.18; }}
    .graph-canvas.dimmed .node-card.node-active {{ opacity: 1; transform: translateY(-2px); box-shadow: 0 8px 22px rgba(37,99,235,.22); border-color: #2563eb; z-index: 5; }}
    .graph-canvas.dimmed .node-card.node-locked {{ outline: 3px solid rgba(37,99,235,.35); outline-offset: 2px; }}
    .graph-canvas.dimmed .node-card.node-parent {{ opacity: 1; border-left-color: #059669; box-shadow: 0 8px 22px rgba(5,150,105,.20); z-index: 4; }}
    .graph-canvas.dimmed .node-card.node-child {{ opacity: 1; border-left-color: #f59e0b; box-shadow: 0 8px 22px rgba(245,158,11,.20); z-index: 4; }}
    .node-level {{ color: var(--muted); font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: .04em; margin-bottom: 4px; }}
    .node-label {{ font-weight: 850; color: #1d4ed8; font-size: 14px; line-height: 1.25; margin-bottom: 6px; }}
    .node-desc {{ color: #334155; font-size: 12px; line-height: 1.35; max-height: 48px; overflow: hidden; }}
    .node-sources {{ color: #64748b; font-size: 10px; line-height: 1.25; margin-top: 7px; max-height: 25px; overflow: hidden; }}
    .node-id {{ position: absolute; right: 10px; bottom: 7px; color: #94a3b8; font-size: 9px; }}
    .legend-note {{ color: var(--muted); font-size: 12px; }}
  </style>
</head>
<body>
  <header>
    <h1>{html.escape(title)}</h1>
    <div class="subtitle">{html.escape(description)}</div>
  </header>
  <div class="summary">
    <span class="pill">Nodes: {len(nodes)}</span>
    <span class="pill">Edges: {len(valid_edges)}</span>
    {level_legend}
    <span class="legend-note">Hover a node to preview relations. Click a node to freeze/highlight its relations; click it again or press Escape to clear. Green border = parent; orange border = child.</span>
  </div>
  <div class="graph-wrap">
    <div class="graph-canvas">
      <svg class="edge-layer" viewBox="0 0 {width} {height}" aria-hidden="true">
        <defs>
          <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#64748b"></path>
          </marker>
        </defs>
        {''.join(svg_paths)}
      </svg>
      {''.join(cards)}
    </div>
  </div>
  <script>
    (function () {{
      const canvas = document.querySelector('.graph-canvas');
      const nodes = Array.from(document.querySelectorAll('.node-card'));
      const edges = Array.from(document.querySelectorAll('.edge-path'));
      const nodeById = new Map(nodes.map((node) => [node.dataset.nodeId, node]));
      let lockedNodeId = null;

      function clearHighlight() {{
        canvas.classList.remove('dimmed', 'locked');
        nodes.forEach((node) => node.classList.remove('node-active', 'node-parent', 'node-child', 'node-locked'));
        edges.forEach((edge) => edge.classList.remove('edge-active'));
      }}

      function highlight(nodeId, locked = false) {{
        clearHighlight();
        canvas.classList.add('dimmed');
        if (locked) canvas.classList.add('locked');
        const active = nodeById.get(nodeId);
        if (active) {{
          active.classList.add('node-active');
          if (locked) active.classList.add('node-locked');
        }}

        edges.forEach((edge) => {{
          const source = edge.dataset.source;
          const target = edge.dataset.target;
          if (source === nodeId || target === nodeId) {{
            edge.classList.add('edge-active');
            if (source === nodeId && nodeById.has(target)) {{
              nodeById.get(target).classList.add('node-child');
            }}
            if (target === nodeId && nodeById.has(source)) {{
              nodeById.get(source).classList.add('node-parent');
            }}
          }}
        }});
      }}

      function lockNode(nodeId) {{
        if (lockedNodeId === nodeId) {{
          lockedNodeId = null;
          clearHighlight();
          return;
        }}
        lockedNodeId = nodeId;
        highlight(nodeId, true);
      }}

      nodes.forEach((node) => {{
        node.addEventListener('mouseenter', () => {{
          if (!lockedNodeId) highlight(node.dataset.nodeId, false);
        }});
        node.addEventListener('mouseleave', () => {{
          if (!lockedNodeId) clearHighlight();
        }});
        node.addEventListener('focus', () => {{
          if (!lockedNodeId) highlight(node.dataset.nodeId, false);
        }});
        node.addEventListener('blur', () => {{
          if (!lockedNodeId) clearHighlight();
        }});
        node.addEventListener('click', (event) => {{
          event.stopPropagation();
          lockNode(node.dataset.nodeId);
        }});
        node.tabIndex = 0;
      }});

      canvas.addEventListener('click', () => {{
        if (lockedNodeId) {{
          lockedNodeId = null;
          clearHighlight();
        }}
      }});

      document.addEventListener('keydown', (event) => {{
        if (event.key === 'Escape' && lockedNodeId) {{
          lockedNodeId = null;
          clearHighlight();
        }}
      }});
    }})();
  </script>
</body>
</html>
'''
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(page, encoding="utf-8")


def mermaid_label(text: str) -> str:
    text = str(text or "")
    text = text.replace('"', "'")
    text = re.sub(r"[\r\n]+", " ", text)
    return text[:80]


def render_mermaid(graph: Dict[str, Any], output: Path) -> None:
    nodes = [n for n in graph.get("nodes", []) if isinstance(n, dict)]
    edges = [e for e in graph.get("edges", []) if isinstance(e, dict)]
    node_ids = {str(n.get("id")) for n in nodes if n.get("id")}

    lines = ["flowchart LR"]
    for node in nodes:
        nid = safe_id(str(node.get("id") or node_label(node)))
        label = mermaid_label(node_label(node))
        lines.append(f'  {nid}["{label}"]')
    for edge in edges:
        src = str(edge.get("source", ""))
        tgt = str(edge.get("target", ""))
        if src not in node_ids or tgt not in node_ids:
            continue
        relation = mermaid_label(edge.get("relation", "related_to"))
        lines.append(f"  {safe_id(src)} -- {relation} --> {safe_id(tgt)}")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Visualize data/general/strategy_hierarchy.json as HTML and Mermaid.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-html", type=Path, default=DEFAULT_HTML)
    parser.add_argument("--output-mermaid", type=Path, default=DEFAULT_MERMAID)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    graph = read_graph(args.input)
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    if not isinstance(nodes, list) or not isinstance(edges, list):
        raise ValueError("Hierarchy JSON must contain list fields `nodes` and `edges`.")

    render_html(graph, args.output_html)
    render_mermaid(graph, args.output_mermaid)

    print(f"Read graph: {args.input}")
    print(f"Nodes: {len(nodes)}")
    print(f"Edges: {len(edges)}")
    print(f"Wrote HTML visualization: {args.output_html}")
    print(f"Wrote Mermaid graph: {args.output_mermaid}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
