#!/usr/bin/env python3
"""
Build a graph-like hierarchical strategy library from the RealAnalysis and
HighDimensionalStatistics strategy category lists.

Inputs:
  data/real_analysis/processed/strategy_categories.txt
  data/high_dimensional_statistics/processed/strategy_categories.txt

Output directory:
  data/general/

Main outputs:
  data/general/strategy_hierarchy.json
  data/general/strategy_hierarchy.md
  data/general/strategy_hierarchy_raw.txt

The workflow asks an LLM to identify cross-library granularity relations, e.g.
RealAnalysis fine-grained calculus categories as children of a broader HDS-style
"Integration methods" category.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import ssl
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parents[2]
REAL_CATEGORIES = PROJECT_ROOT / "data" / "real_analysis" / "processed" / "strategy_categories.txt"
HDS_CATEGORIES = PROJECT_ROOT / "data" / "high_dimensional_statistics" / "processed" / "strategy_categories.txt"
OUTPUT_DIR = PROJECT_ROOT / "data" / "general"
OUTPUT_JSON = OUTPUT_DIR / "strategy_hierarchy.json"
OUTPUT_MD = OUTPUT_DIR / "strategy_hierarchy.md"
OUTPUT_RAW = OUTPUT_DIR / "strategy_hierarchy_raw.txt"

DEFAULT_MODEL = "gpt-5.6-sol"
DEFAULT_API_BASE = "https://api.openai.com/v1"

SYSTEM_PROMPT = """You are a mathematical proof-strategy librarian.

Your job is to merge and organize category taxonomies from two proof datasets into a graph-like hierarchical library. You understand that different libraries may use different granularities: one category may be a broad parent of several finer categories in another library.

Be precise and conservative. Do not collapse categories merely because words overlap. Identify parent-child relations only when the child is genuinely a more specific instance, technique, or sub-branch of the parent. Allow cross-links when a strategy belongs naturally under more than one parent.
"""


def load_dotenv(path: Path = PROJECT_ROOT / ".env") -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ[key] = value


def make_ssl_context() -> ssl.SSLContext:
    try:
        import certifi  # type: ignore
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return ssl.create_default_context()


def call_openai_chat(
    *,
    api_key: str,
    model: str,
    system_prompt: str,
    user_prompt: str,
    api_base: str,
    temperature: float,
    max_completion_tokens: int,
    reasoning_effort: Optional[str],
    timeout: int = 240,
    max_retries: int = 3,
    retry_sleep: float = 2.0,
) -> str:
    url = api_base.rstrip("/") + "/chat/completions"
    payload: Dict[str, Any] = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
        "max_completion_tokens": max_completion_tokens,
    }
    if reasoning_effort:
        payload["reasoning_effort"] = reasoning_effort

    body = json.dumps(payload).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    context = make_ssl_context()

    last_error: Optional[BaseException] = None
    for attempt in range(1, max_retries + 1):
        req = urllib.request.Request(url, data=body, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=context) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"].strip()
        except urllib.error.HTTPError as e:
            error_text = e.read().decode("utf-8", errors="replace")
            if e.code in {429, 500, 502, 503, 504} and attempt < max_retries:
                last_error = RuntimeError(f"OpenAI HTTP {e.code}: {error_text}")
                time.sleep(retry_sleep * attempt)
                continue
            raise RuntimeError(f"OpenAI API HTTP error {e.code}: {error_text}") from e
        except Exception as e:
            last_error = e
            if attempt < max_retries:
                time.sleep(retry_sleep * attempt)
                continue
            raise RuntimeError(f"OpenAI API call failed after {max_retries} attempts: {last_error}") from e
    raise RuntimeError(f"OpenAI API call failed: {last_error}")


def read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Missing category file: {path}")
    return path.read_text(encoding="utf-8").strip()


def parse_numbered_categories(text: str, dataset: str) -> List[Dict[str, str]]:
    categories: List[Dict[str, str]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        m = re.match(r"^(\d+)\s*[\.)]\s*(.*)$", line)
        if not m:
            continue
        num = m.group(1)
        body = m.group(2).strip()
        if ":" in body:
            name, desc = body.split(":", 1)
        else:
            name, desc = body, ""
        categories.append(
            {
                "id": f"{dataset}_{num}",
                "dataset": dataset,
                "number": num,
                "name": name.strip(),
                "description": desc.strip(),
                "raw": line,
            }
        )
    return categories


def strip_json_fence(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    return text.strip()


def parse_llm_json(raw: str) -> Dict[str, Any]:
    cleaned = strip_json_fence(raw)
    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise
        parsed = json.loads(cleaned[start : end + 1])
    if not isinstance(parsed, dict):
        raise ValueError("Expected top-level JSON object from LLM")
    return parsed


def build_prompt(real_text: str, hds_text: str, real_items: List[Dict[str, str]], hds_items: List[Dict[str, str]]) -> str:
    return f"""
You are given two proof-strategy category libraries.

Goal: build a graph-like hierarchical strategy library that organizes both libraries together.

Important: The two libraries differ in granularity. RealAnalysis often has fine-grained categories, especially calculus/integration/series/limit categories. HighDimensionalStatistics often has broader categories such as concentration, error decomposition, covering-net arguments, and integration/moment methods. Discover parent-child relations where one category is a more detailed sub-branch of another.

Requirements:
1. Read BOTH category lists completely.
2. Create a hierarchy with at least two layers when appropriate:
   - broad parent strategy families;
   - child strategy categories or sub-branches.
3. If a category naturally belongs under multiple parents, include cross-links in `edges`.
4. Preserve source provenance: every node should list which source categories it covers, using ids such as `real_analysis_24` or `high_dimensional_statistics_11`.
5. Do not force every relation into a tree if a graph is more accurate.
6. Distinguish different granularities explicitly. For example, if one library has separate integration-by-parts/substitution/FTC categories and another has a broader integration-calculus category, make the broad one a parent and the detailed ones children.
7. Include categories that are dataset-specific but still important.
8. Prefer mathematically standard names for parent families.

Return strict JSON only. Use this schema:
{{
  "metadata": {{
    "title": "Hierarchical Proof Strategy Library",
    "description": "...",
    "source_libraries": ["real_analysis", "high_dimensional_statistics"]
  }},
  "nodes": [
    {{
      "id": "family_calculus_methods",
      "label": "Calculus methods",
      "level": 1,
      "description": "Broad parent family description.",
      "source_categories": [
        {{"dataset": "real_analysis", "id": "real_analysis_22", "name": "Fundamental Theorem of Calculus"}},
        {{"dataset": "high_dimensional_statistics", "id": "high_dimensional_statistics_11", "name": "Integral-calculus arguments"}}
      ]
    }},
    {{
      "id": "sub_integration_by_parts_substitution",
      "label": "Integration by parts and substitution",
      "level": 2,
      "description": "More specific sub-branch description.",
      "source_categories": [...]
    }}
  ],
  "edges": [
    {{
      "source": "family_calculus_methods",
      "target": "sub_integration_by_parts_substitution",
      "relation": "parent_of",
      "rationale": "The target is a more specific integration technique under the broader calculus/integration family."
    }}
  ],
  "unmapped_source_categories": [
    {{"dataset": "real_analysis", "id": "real_analysis_99", "name": "...", "reason": "..."}}
  ]
}}

RealAnalysis parsed category ids:
{json.dumps(real_items, ensure_ascii=False, indent=2)}

HighDimensionalStatistics parsed category ids:
{json.dumps(hds_items, ensure_ascii=False, indent=2)}

RealAnalysis raw strategy_categories.txt:
{real_text}

HighDimensionalStatistics raw strategy_categories.txt:
{hds_text}
""".strip()


def write_markdown(path: Path, graph: Dict[str, Any], raw: str) -> None:
    lines: List[str] = []
    metadata = graph.get("metadata", {}) if isinstance(graph, dict) else {}
    lines.append(f"# {metadata.get('title', 'Hierarchical Proof Strategy Library')}")
    lines.append("")
    if metadata.get("description"):
        lines.append(str(metadata["description"]))
        lines.append("")

    nodes = graph.get("nodes", []) if isinstance(graph, dict) else []
    edges = graph.get("edges", []) if isinstance(graph, dict) else []
    by_level: Dict[Any, List[Dict[str, Any]]] = {}
    for node in nodes:
        if isinstance(node, dict):
            by_level.setdefault(node.get("level", "unknown"), []).append(node)

    lines.append("## Nodes by level")
    lines.append("")
    for level in sorted(by_level, key=lambda x: str(x)):
        lines.append(f"### Level {level}")
        lines.append("")
        for node in by_level[level]:
            lines.append(f"- **{node.get('label', node.get('id'))}** (`{node.get('id')}`): {node.get('description', '')}")
            srcs = node.get("source_categories", [])
            if srcs:
                src_text = "; ".join(
                    f"{s.get('id')} {s.get('name', '')}" for s in srcs if isinstance(s, dict)
                )
                lines.append(f"  - Sources: {src_text}")
        lines.append("")

    lines.append("## Edges")
    lines.append("")
    for edge in edges:
        if not isinstance(edge, dict):
            continue
        lines.append(
            f"- `{edge.get('source')}` → `{edge.get('target')}` "
            f"({edge.get('relation', 'related_to')}): {edge.get('rationale', '')}"
        )
    lines.append("")

    unmapped = graph.get("unmapped_source_categories", []) if isinstance(graph, dict) else []
    if unmapped:
        lines.append("## Unmapped source categories")
        lines.append("")
        for item in unmapped:
            if isinstance(item, dict):
                lines.append(f"- {item.get('dataset')} `{item.get('id')}` {item.get('name')}: {item.get('reason', '')}")
        lines.append("")

    lines.append("## Raw LLM response")
    lines.append("")
    lines.append("```json")
    lines.append(raw.strip())
    lines.append("```")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_reasoning_effort(value: str) -> Optional[str]:
    value = (value or "none").strip().lower()
    if value == "none":
        return None
    if value not in {"low", "medium", "high"}:
        raise argparse.ArgumentTypeError("reasoning effort must be one of: none, low, medium, high")
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a hierarchical graph library from RealAnalysis and HDS strategy category lists.")
    parser.add_argument("--real-categories", type=Path, default=REAL_CATEGORIES)
    parser.add_argument("--hds-categories", type=Path, default=HDS_CATEGORIES)
    parser.add_argument("--output-json", type=Path, default=OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=OUTPUT_MD)
    parser.add_argument("--output-raw", type=Path, default=OUTPUT_RAW)
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"OpenAI model. Default: {DEFAULT_MODEL}")
    parser.add_argument("--api-base", default=DEFAULT_API_BASE)
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--reasoning-effort", type=parse_reasoning_effort, default=None, help="Reasoning effort if supported: none, low, medium, high. Default: none")
    parser.add_argument("--max-tokens", type=int, default=12000)
    parser.add_argument("--dry-run", action="store_true", help="Load inputs and print prompt summary without calling the API.")
    parser.add_argument("--no-parse", action="store_true", help="Write raw output even if JSON parsing fails.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    load_dotenv()

    real_text = read_text(args.real_categories)
    hds_text = read_text(args.hds_categories)
    real_items = parse_numbered_categories(real_text, "real_analysis")
    hds_items = parse_numbered_categories(hds_text, "high_dimensional_statistics")
    prompt = build_prompt(real_text, hds_text, real_items, hds_items)

    print(f"Loaded RealAnalysis categories: {len(real_items)} from {args.real_categories}")
    print(f"Loaded HDS categories: {len(hds_items)} from {args.hds_categories}")
    print(f"Output JSON: {args.output_json}")
    print(f"Output Markdown: {args.output_md}")
    print(f"Model: {args.model}")

    if args.dry_run:
        print("Dry run: no API call will be made.")
        print(f"Prompt characters: {len(prompt)}")
        print("First RealAnalysis categories:")
        for item in real_items[:5]:
            print(f"  {item['id']}: {item['name']}")
        print("First HDS categories:")
        for item in hds_items[:5]:
            print(f"  {item['id']}: {item['name']}")
        return 0

    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key or api_key == "your-openai-api-key-here":
        raise RuntimeError("OPENAI_API_KEY is missing or still set to the placeholder. Put a real key in .env or export it.")

    raw = call_openai_chat(
        api_key=api_key,
        model=args.model,
        system_prompt=SYSTEM_PROMPT,
        user_prompt=prompt,
        api_base=args.api_base,
        temperature=args.temperature,
        max_completion_tokens=args.max_tokens,
        reasoning_effort=args.reasoning_effort,
    )

    args.output_raw.parent.mkdir(parents=True, exist_ok=True)
    args.output_raw.write_text(raw + "\n", encoding="utf-8")

    try:
        graph = parse_llm_json(raw)
    except Exception as exc:
        if not args.no_parse:
            raise RuntimeError(f"LLM output could not be parsed as JSON. Raw response saved to {args.output_raw}") from exc
        graph = {
            "metadata": {
                "title": "Hierarchical Proof Strategy Library",
                "description": "Raw LLM output could not be parsed as JSON.",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "model": args.model,
                "parse_error": str(exc),
            },
            "nodes": [],
            "edges": [],
            "unmapped_source_categories": [],
            "raw_response": raw,
        }

    graph.setdefault("metadata", {})
    graph["metadata"].update(
        {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "model": args.model,
            "real_analysis_category_count": len(real_items),
            "high_dimensional_statistics_category_count": len(hds_items),
            "real_analysis_source": str(args.real_categories.relative_to(PROJECT_ROOT) if args.real_categories.is_absolute() and PROJECT_ROOT in args.real_categories.parents else args.real_categories),
            "high_dimensional_statistics_source": str(args.hds_categories.relative_to(PROJECT_ROOT) if args.hds_categories.is_absolute() and PROJECT_ROOT in args.hds_categories.parents else args.hds_categories),
        }
    )

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(args.output_md, graph, raw)

    print(f"Wrote raw response: {args.output_raw}")
    print(f"Wrote hierarchy JSON: {args.output_json}")
    print(f"Wrote hierarchy Markdown: {args.output_md}")
    print(f"Nodes: {len(graph.get('nodes', []))}; Edges: {len(graph.get('edges', []))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
