#!/usr/bin/env python3
"""
Stage 1: generate a global category taxonomy for extracted proof strategies.

Input:
    data/processed/strategy_library.json

This script gives the LLM the full collection of strategies and asks it to summarize
recurring real-analysis proof-strategy categories.

Default outputs:
    data/processed/strategy_categories.txt
    data/processed/strategy_categories_raw.txt

Run from project root:
    python workflows/proof_strategy_extraction/categorize_strategy_library.py

Force regeneration of the category taxonomy:
    python workflows/proof_strategy_extraction/categorize_strategy_library.py --no-resume

Stage 2 classification has been separated into:
    python workflows/proof_strategy_extraction/classify_strategy_categories.py
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import ssl
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = PROJECT_ROOT / "data" / "processed" / "strategy_library.json"
DEFAULT_NOTES_OUTPUT = PROJECT_ROOT / "data" / "processed" / "strategy_category_notes.txt"
DEFAULT_CATEGORIES_OUTPUT = PROJECT_ROOT / "data" / "processed" / "strategy_categories.txt"
DEFAULT_RAW_OUTPUT = PROJECT_ROOT / "data" / "processed" / "strategy_categories_raw.txt"
DEFAULT_ASSIGNMENTS_JSON = PROJECT_ROOT / "data" / "processed" / "strategy_category_assignments.json"
DEFAULT_ASSIGNMENTS_CSV = PROJECT_ROOT / "data" / "processed" / "strategy_category_assignments.csv"
DEFAULT_ASSIGNMENTS_MD = PROJECT_ROOT / "data" / "processed" / "strategy_category_assignments.md"

CATEGORY_LINE_RE = re.compile(r"^\s*(\d+)[\.)]\s+(.*)\s*$")


def load_dotenv(path: Path = PROJECT_ROOT / ".env") -> None:
    """Load simple KEY=VALUE lines from .env without overriding existing env vars."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def make_ssl_context() -> ssl.SSLContext:
    """Use certifi if available; otherwise fall back to the default SSL context."""
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
    api_base: str = "https://api.openai.com/v1",
    temperature: float = 1.0,
    max_completion_tokens: int = 4000,
    reasoning_effort: Optional[str] = "high",
    timeout: int = 180,
    max_retries: int = 3,
    retry_sleep: float = 2.0,
) -> str:
    """Minimal OpenAI chat-completions call using stdlib urllib."""
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
                response_text = resp.read().decode("utf-8")
            data = json.loads(response_text)
            return data["choices"][0]["message"]["content"].strip()
        except urllib.error.HTTPError as e:
            error_text = e.read().decode("utf-8", errors="replace")
            # Retry only transient server/rate-limit errors.
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


def read_strategy_library(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Strategy library not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and isinstance(data.get("strategies"), list):
        return [x for x in data["strategies"] if isinstance(x, dict)]
    if isinstance(data, list):
        return [x for x in data if isinstance(x, dict)]
    raise ValueError(f"Unexpected strategy library format: {path}")


def format_strategy_collection(strategies: List[Dict[str, Any]]) -> str:
    lines: List[str] = []
    for item in strategies:
        sid = item.get("strategy_id", "")
        strategy = str(item.get("strategy", "")).strip()
        source_name = item.get("source_lean_name", "")
        if source_name:
            lines.append(f"{sid}. {strategy} [source: {source_name}]")
        else:
            lines.append(f"{sid}. {strategy}")
    return "\n".join(lines)


def normalize_categories_text(raw: str) -> str:
    """Extract the category list from a model response.

    The current prompt asks for only the final category list. This function also
    tolerates older responses containing headings such as FINAL CATEGORY LIST:.
    """
    text = raw.strip()
    upper = text.upper()
    marker_candidates = [
        "FINAL CATEGORY LIST:",
        "FINAL CATEGORIES:",
        "CATEGORY LIST:",
        "FINAL LIST:",
    ]
    for marker in marker_candidates:
        idx = upper.find(marker)
        if idx != -1:
            return text[idx + len(marker) :].strip()
    return text


def parse_category_names(categories_text: str) -> List[str]:
    names: List[str] = []
    for line in categories_text.splitlines():
        line = line.strip()
        if not line:
            continue
        m = CATEGORY_LINE_RE.match(line)
        if m:
            item = m.group(2).strip()
            # If the line is like "Compactness and extrema: key point...",
            # use the category heading before ':' or an em dash as the category name.
            # Do NOT split on ordinary hyphens, because category names may contain
            # hyphenated phrases such as "Abstract-to-concrete reformulation".
            heading = re.split(r"\s*(?::|—)\s*", item, maxsplit=1)[0].strip()
            names.append(heading or item)
    return names


def generate_categories(
    *,
    strategies: List[Dict[str, Any]],
    api_key: str,
    model: str,
    api_base: str,
    temperature: float,
    reasoning_effort: Optional[str],
    max_tokens: int,
) -> Tuple[str, str, str, List[str]]:
    system_prompt = (
        "You are a mathematical proof-analysis assistant specializing in real analysis and Lean proofs. "
        "You identify recurring mathematical proof strategies accurately and avoid vague categories."
    )

    user_prompt = f"""
Here is a collection of proof strategies used in real analysis proofs. You need to go over all the strategies and summarize them into a finite number of categories of strategies.

SUMMARIZE THE CATEGORIES LIKE WHAT A MATHEMATICIAN WOULD DO AND USE THE TERMS WE USUALLY CALL THEM. For example: by definition/by algebra/by some theorem. IMPORTANT: YOU MUST NOT BE LIMITED TO THE EXAMPLES PROVIDED, but your summaries should share a SIMILAR GRANULARITY as the examples.

Also pay attention to:
- Are there strategies that are similar to each other that appear a lot? If so, they belong to the same category.
- Summarize the KEY POINT of each category ACCURATELY.
- Prefer mathematically meaningful categories, not superficial wording categories.
- Categories should be broad enough to group repeated patterns, but specific enough to be useful for proof search/explanation.

Return only the final category list in exactly this format:

1. <Category name>: <one or two sentences accurately summarizing the key point of this category>
2. <Category name>: <one or two sentences accurately summarizing the key point of this category>
...

Collection of strategies:
{format_strategy_collection(strategies)}
""".strip()

    raw = call_openai_chat(
        api_key=api_key,
        model=model,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        api_base=api_base,
        temperature=temperature,
        max_completion_tokens=max_tokens,
        reasoning_effort=reasoning_effort,
    )
    categories_text = normalize_categories_text(raw)
    category_names = parse_category_names(categories_text)
    return raw, "", categories_text, category_names


def classify_strategy(
    *,
    strategy: Dict[str, Any],
    categories_text: str,
    category_names: List[str],
    notes: str,
    api_key: str,
    model: str,
    api_base: str,
    temperature: float,
    reasoning_effort: Optional[str],
    max_tokens: int,
) -> Dict[str, Any]:
    system_prompt = (
        "You are classifying individual real-analysis proof strategies into an existing taxonomy. "
        "Choose the closest listed category; do not invent a new category unless absolutely necessary."
    )
    allowed_categories = "\n".join(f"- {name}" for name in category_names)
    user_prompt = f"""
You previously summarized a collection of proof strategies into categories. Your notes and category list are below.

NOTES FROM INITIAL CATEGORIZATION:
{notes}

CATEGORY LIST:
{categories_text}

ALLOWED CATEGORY NAMES:
{allowed_categories}

Now classify this individual strategy into exactly one category from the allowed category names.

Strategy id: {strategy.get('strategy_id')}
Strategy text: {strategy.get('strategy')}
Source theorem/lemma: {strategy.get('source_lean_name')}
Source formal statement: {strategy.get('formal_statement')}

Return strict JSON only, with this shape:
{{
  "strategy_id": {strategy.get('strategy_id')},
  "category": "<one allowed category name>",
  "reason": "<one concise sentence explaining why it belongs there>"
}}
""".strip()

    raw = call_openai_chat(
        api_key=api_key,
        model=model,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        api_base=api_base,
        temperature=temperature,
        max_completion_tokens=max_tokens,
        reasoning_effort=reasoning_effort,
    )

    try:
        parsed = json.loads(raw)
        if not isinstance(parsed, dict):
            raise ValueError("LLM JSON response is not an object")
    except Exception:
        parsed = {
            "strategy_id": strategy.get("strategy_id"),
            "category": "UNPARSED_RESPONSE",
            "reason": raw,
        }

    category = str(parsed.get("category", "")).strip()
    if category_names and category not in category_names:
        # Keep the model output, but flag that it did not match exactly.
        parsed["category_name_match"] = False
    else:
        parsed["category_name_match"] = True

    return {
        "strategy_id": strategy.get("strategy_id"),
        "strategy": strategy.get("strategy"),
        "source_proof_id": strategy.get("source_proof_id"),
        "source_lean_name": strategy.get("source_lean_name"),
        "source_strategy_number": strategy.get("source_strategy_number"),
        "source_file": strategy.get("source_file"),
        "category": parsed.get("category"),
        "category_name_match": parsed.get("category_name_match"),
        "reason": parsed.get("reason"),
        "raw_classification_response": raw,
    }


def read_existing_assignments(path: Path) -> Dict[int, Dict[str, Any]]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        assignments = data.get("assignments", []) if isinstance(data, dict) else data
        result: Dict[int, Dict[str, Any]] = {}
        for item in assignments:
            if isinstance(item, dict) and item.get("strategy_id") is not None:
                result[int(item["strategy_id"])] = item
        return result
    except Exception:
        return {}


def write_assignments_json(path: Path, assignments: List[Dict[str, Any]], categories_text: str, notes: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "assignment_count": len(assignments),
        "category_notes": notes,
        "categories": categories_text,
        "assignments": assignments,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_assignments_csv(path: Path, assignments: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "strategy_id",
        "strategy",
        "category",
        "category_name_match",
        "reason",
        "source_lean_name",
        "source_strategy_number",
        "source_file",
        "source_proof_id",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for item in assignments:
            writer.writerow(item)


def write_assignments_md(path: Path, assignments: List[Dict[str, Any]], categories_text: str, notes: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: List[str] = []
    lines.append("# Strategy Category Assignments")
    lines.append("")
    lines.append(f"Generated at: {datetime.now(timezone.utc).isoformat()}")
    lines.append(f"Total assignments: {len(assignments)}")
    lines.append("")
    lines.append("## Category Notes")
    lines.append("")
    lines.append(notes or "_No notes captured._")
    lines.append("")
    lines.append("## Category List")
    lines.append("")
    lines.append(categories_text)
    lines.append("")
    lines.append("## Assignments")
    lines.append("")
    for item in assignments:
        lines.append(f"### {item.get('strategy_id')}. {item.get('category')}")
        lines.append("")
        lines.append(f"**Strategy:** {item.get('strategy')}")
        lines.append("")
        lines.append(f"**Reason:** {item.get('reason')}")
        lines.append("")
        lines.append(f"**Source:** `{item.get('source_lean_name')}`")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Stage 1 only: generate a category taxonomy for extracted proof strategies with an LLM.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help=f"Input strategy library JSON. Default: {DEFAULT_INPUT}")
    parser.add_argument("--model", default="gpt-5.6-sol", help="OpenAI model. Default: gpt-5.6-sol")
    parser.add_argument("--api-base", default="https://api.openai.com/v1", help="OpenAI-compatible API base URL.")
    parser.add_argument("--temperature", type=float, default=1.0, help="Sampling temperature. Some models only support 1.0.")
    parser.add_argument("--reasoning-effort", choices=["low", "medium", "high"], default="high", help="Reasoning effort for supported models. Default: high")
    parser.add_argument("--category-max-tokens", type=int, default=8000, help="Max completion tokens for global category generation.")
    parser.add_argument("--limit", type=int, default=None, help="For testing Stage 1 only: generate categories from only the first N strategies.")
    parser.add_argument("--no-resume", action="store_true", help="Regenerate the category taxonomy even if output files already exist.")
    parser.add_argument("--dry-run", action="store_true", help="Load inputs and print what would happen, but do not call the API.")
    parser.add_argument("--notes-output", type=Path, default=DEFAULT_NOTES_OUTPUT)
    parser.add_argument("--categories-output", type=Path, default=DEFAULT_CATEGORIES_OUTPUT)
    parser.add_argument("--raw-output", type=Path, default=DEFAULT_RAW_OUTPUT)
    parser.add_argument("--assignments-json", type=Path, default=DEFAULT_ASSIGNMENTS_JSON)
    parser.add_argument("--assignments-csv", type=Path, default=DEFAULT_ASSIGNMENTS_CSV)
    parser.add_argument("--assignments-md", type=Path, default=DEFAULT_ASSIGNMENTS_MD)
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()

    strategies = read_strategy_library(args.input)
    if args.limit is not None:
        strategies_for_categories = strategies[: args.limit]
    else:
        strategies_for_categories = strategies

    print(f"Loaded {len(strategies)} strategies from {args.input}")
    print(f"Will generate categories from {len(strategies_for_categories)} strategies")

    if args.dry_run:
        print("Dry run: no API calls will be made.")
        print("First few strategies:")
        for item in strategies_for_categories[:5]:
            print(f"  {item.get('strategy_id')}. {item.get('strategy')}")
        return

    if not api_key or api_key == "your-openai-api-key-here":
        raise RuntimeError("OPENAI_API_KEY is missing or still set to the placeholder. Put a real key in .env or export it.")

    # Stage 1: global categorization.
    if not args.no_resume and args.categories_output.exists() and args.raw_output.exists():
        print(f"Reusing existing categories from {args.categories_output}")
        raw_categories = args.raw_output.read_text(encoding="utf-8")
        notes = ""
        categories_text = args.categories_output.read_text(encoding="utf-8")
        category_names = parse_category_names(categories_text)
    else:
        print("Generating global strategy categories...")
        raw_categories, notes, categories_text, category_names = generate_categories(
            strategies=strategies_for_categories,
            api_key=api_key,
            model=args.model,
            api_base=args.api_base,
            temperature=args.temperature,
            reasoning_effort=args.reasoning_effort,
            max_tokens=args.category_max_tokens,
        )
        args.raw_output.parent.mkdir(parents=True, exist_ok=True)
        args.raw_output.write_text(raw_categories + "\n", encoding="utf-8")
        args.categories_output.write_text(categories_text + "\n", encoding="utf-8")
        print(f"Wrote category list: {args.categories_output}")

    if not category_names:
        print("Warning: could not parse category names from category list.")
    else:
        print(f"Parsed {len(category_names)} category names.")

    print("Done with Stage 1 category generation.")
    print(f"Category list: {args.categories_output}")
    print(f"Raw category response: {args.raw_output}")
    print("")
    print("To run Stage 2 classification without regenerating this taxonomy, run:")
    print("  .venv/bin/python workflows/proof_strategy_extraction/classify_strategy_categories.py")


if __name__ == "__main__":
    main()
