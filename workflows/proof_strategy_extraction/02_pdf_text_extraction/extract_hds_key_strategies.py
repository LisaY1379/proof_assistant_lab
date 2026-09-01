#!/usr/bin/env python3
"""
Extract key proof strategies for the HighDimensionalStatistics PDF-aligned library.

This is a focused workflow derived from Step 4 of the Lean translation pipeline:

    For each full proof, call the API to identify the key proof strategies / key
    ideas that make the proof work.

Unlike the Lean-to-English workflow, this script does NOT translate Lean code into
natural language. It assumes the HighDimensionalStatistics library already contains
book-side natural-language fields:

    plain_english_statement
    plain_english_proof

or cleaned variants:

    plain_english_statement_cleaned
    plain_english_proof_cleaned

It reads:

    data/high_dimensional_statistics/processed/proofs_with_key_strategies.jsonl

and writes plain enumerated key-strategy text back into each record under:

    key_strategies

Example usage from repository root:

    .venv/bin/python workflows/proof_strategy_extraction/02_pdf_text_extraction/extract_hds_key_strategies.py --until 10

Dry run:

    .venv/bin/python workflows/proof_strategy_extraction/02_pdf_text_extraction/extract_hds_key_strategies.py --until 3 --dry-run
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import shutil
import ssl
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


DEFAULT_LIBRARY_PATH = Path("data/high_dimensional_statistics/processed/proofs_with_key_strategies.jsonl")
DEFAULT_JSON_MIRROR_PATH = Path("data/high_dimensional_statistics/processed/proofs_with_key_strategies.json")
DEFAULT_API_BASE = "https://api.openai.com/v1"
DEFAULT_MODEL = "gpt-5.6-sol"

KEY_STRATEGY_SYSTEM_PROMPT = (
    "You are a careful mathematical proof analyst. Your job is to identify the key "
    "proof ideas in natural-language mathematics proofs. Focus on mathematical ideas, "
    "not superficial formatting. Do not invent claims not supported by the statement/proof."
)

KEY_STRATEGY_USER_INSTRUCTION = """\
Read the theorem statement and the original textbook proof.

Identify the key proof strategies / key ideas that make the proof work.
Focus on ideas without which the proof would fail, such as:
- choosing the right theorem or definition;
- reducing the goal to a known principle;
- compactness, concentration, covering, symmetrization, union bounds, epsilon-net arguments, decomposition, conditioning, comparison, or optimization tricks;
- constructing a useful object or witness;
- splitting the proof into essential cases;
- controlling an error term or probability tail by the decisive estimate.

Do NOT list routine algebra, notation changes, or purely mechanical simplifications as key strategies unless they are genuinely the central idea.

Return only an enumerated plain-text list of key ideas, in this format:

1. <One sentence stating the key idea.>
2. <One sentence stating the key idea.>

If useful, include a short evidence phrase after the sentence, but keep each item concise.
Do not return JSON, Markdown tables, code fences, or explanatory text outside the enumerated list.

If the proof text is missing or too incomplete, return an empty string.
"""


# -----------------------------------------------------------------------------
# Basic utilities
# -----------------------------------------------------------------------------


def now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat()


def load_project_env(env_path: Path = Path(".env"), override: bool = True) -> None:
    """Load simple KEY=VALUE lines from a project .env file."""
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and (override or key not in os.environ):
            os.environ[key] = value


def format_json_record(row: Dict[str, Any]) -> str:
    return json.dumps(row, ensure_ascii=False, sort_keys=True, indent=2)


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            if count:
                f.write("\n")
            f.write(format_json_record(row) + "\n")
            count += 1
    return count


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    """Read compact JSONL or pretty-printed JSONL-like records."""
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []

    rows: List[Dict[str, Any]] = []
    jsonl_ok = True
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        try:
            rows.append(json.loads(stripped))
        except json.JSONDecodeError:
            jsonl_ok = False
            break
    if jsonl_ok:
        return rows

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
                    rows.append(json.loads(record_text))
                buffer = []
    trailing = "".join(buffer).strip()
    if trailing:
        raise ValueError(f"Could not parse trailing JSON content in {path}")
    return rows


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def make_backup(path: Path, label: str = "hds_key_strategies") -> Optional[Path]:
    if not path.exists():
        return None
    stamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = path.with_name(path.name + f".bak_{label}_{stamp}")
    shutil.copy2(path, backup)
    return backup


# -----------------------------------------------------------------------------
# OpenAI-compatible API call
# -----------------------------------------------------------------------------


def call_openai_chat(
    *,
    api_key: str,
    model: str,
    system_prompt: str,
    user_prompt: str,
    api_base: str = DEFAULT_API_BASE,
    temperature: float = 1.0,
    max_tokens: int = 700,
    reasoning_effort: Optional[str] = "high",
    timeout: int = 180,
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
        "max_completion_tokens": max_tokens,
    }
    if reasoning_effort:
        payload["reasoning_effort"] = reasoning_effort

    data = json.dumps(payload).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        import certifi  # type: ignore
        ssl_context = ssl.create_default_context(cafile=certifi.where())
    except Exception:
        ssl_context = ssl.create_default_context()

    last_error: Optional[Exception] = None
    for attempt in range(1, max_retries + 1):
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=ssl_context) as response:
                body = response.read().decode("utf-8")
                obj = json.loads(body)
                return obj["choices"][0]["message"]["content"].strip()
        except urllib.error.HTTPError as e:
            last_error = e
            error_body = e.read().decode("utf-8", errors="replace")
            if attempt == max_retries:
                raise RuntimeError(f"OpenAI API HTTP error {e.code}: {error_body}") from e
        except Exception as e:
            last_error = e
            if attempt == max_retries:
                raise
        sleep_for = retry_sleep * attempt
        print(f"API call failed on attempt {attempt}; retrying in {sleep_for:.1f}s...", file=sys.stderr)
        time.sleep(sleep_for)
    raise RuntimeError(f"OpenAI API call failed: {last_error}")


# -----------------------------------------------------------------------------
# Strategy extraction
# -----------------------------------------------------------------------------


def get_statement(record: Dict[str, Any]) -> str:
    return str(
        record.get("plain_english_statement_cleaned")
        or record.get("plain_english_statement")
        or record.get("comment")
        or ""
    ).strip()


def get_proof_text(record: Dict[str, Any]) -> str:
    return str(record.get("plain_english_proof_cleaned") or record.get("plain_english_proof") or "").strip()


def has_existing_key_strategies(record: Dict[str, Any]) -> bool:
    value = record.get("key_strategies")
    if isinstance(value, list):
        return len(value) > 0
    if isinstance(value, str):
        return bool(value.strip())
    return False


def normalize_enumerated_text(text: str) -> str:
    """Clean a plain-text enumerated key-strategy response.

    This mirrors the original Lean workflow behavior: the LLM output is treated as
    text, not parsed as JSON. We only remove surrounding code fences or leading
    labels if they appear accidentally.
    """
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:text|markdown|md)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned).strip()
    cleaned = re.sub(r"^Key (?:proof )?(?:strategies|ideas)\s*:?\s*", "", cleaned, flags=re.IGNORECASE)
    return cleaned.strip()


def identify_key_strategies_from_book_proof(
    *,
    record: Dict[str, Any],
    api_key: str,
    model: str,
    api_base: str,
    temperature: float,
    reasoning_effort: Optional[str],
    max_tokens: int,
) -> str:
    statement = get_statement(record)
    proof_text = get_proof_text(record)
    lean_code = str(record.get("lean_original_code", "")).strip()
    comment = str(record.get("comment", "")).strip()

    if not proof_text:
        return ""

    user_prompt = (
        f"Lean declaration name, if available: {record.get('lean_name') or '[unknown]'}\n\n"
        f"Lean-side comment / description, if available:\n{comment or '[No comment]'}\n\n"
        f"Book theorem statement:\n{statement or '[No statement available]'}\n\n"
        f"Original textbook proof:\n{proof_text}\n\n"
        "Lean code is provided only as optional formal context; do not base the strategy analysis primarily on Lean syntax:\n"
        f"{lean_code or '[No Lean code]'}\n\n"
        f"{KEY_STRATEGY_USER_INSTRUCTION}"
    )
    raw = call_openai_chat(
        api_key=api_key,
        model=model,
        api_base=api_base,
        system_prompt=KEY_STRATEGY_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        reasoning_effort=reasoning_effort,
    )
    return normalize_enumerated_text(raw)


def write_library(records: List[Dict[str, Any]], library_path: Path, json_mirror_path: Optional[Path]) -> None:
    write_jsonl(library_path, records)
    if json_mirror_path:
        write_json(json_mirror_path, records)


def process_records(
    *,
    records: List[Dict[str, Any]],
    until: Optional[int],
    api_key: str,
    model: str,
    api_base: str,
    temperature: float,
    reasoning_effort: Optional[str],
    max_tokens: int,
    sleep_seconds: float,
    resume: bool,
    dry_run: bool,
    library_path: Path,
    json_mirror_path: Optional[Path],
) -> None:
    selected = records[:until] if until is not None else records
    pending_indices: List[int] = []
    skipped_existing = 0
    skipped_no_proof = 0

    for i, record in enumerate(selected):
        if resume and has_existing_key_strategies(record):
            skipped_existing += 1
            continue
        if not get_proof_text(record):
            skipped_no_proof += 1
            if not has_existing_key_strategies(record) and not dry_run:
                record["key_strategies"] = ""
                record["key_strategy_status"] = "no_book_proof_text"
            continue
        pending_indices.append(i)

    print(f"Loaded records: {len(records)}")
    print(f"Selected records: {len(selected)}")
    print(f"Already with key_strategies skipped: {skipped_existing}")
    print(f"No book proof text skipped: {skipped_no_proof}")
    print(f"Pending API strategy extraction: {len(pending_indices)}")

    if dry_run:
        for idx in pending_indices[:10]:
            rec = records[idx]
            print(f"DRY RUN would process #{idx + 1}: {rec.get('lean_name') or '(unnamed)'}")
        return

    backup = make_backup(library_path)
    if backup:
        print(f"Backup created: {backup}")

    # Persist no-proof statuses before API work, if any were added.
    write_library(records, library_path, json_mirror_path)

    for n, idx in enumerate(pending_indices, start=1):
        record = records[idx]
        name = record.get("lean_name") or record.get("book_name") or "(unnamed)"
        print(f"[{n}/{len(pending_indices)}] Identifying key strategies for proof #{idx + 1}: {name}", flush=True)

        key_strategies = ""
        empty_attempts = 2
        for attempt in range(1, empty_attempts + 1):
            key_strategies = identify_key_strategies_from_book_proof(
                record=record,
                api_key=api_key,
                model=model,
                api_base=api_base,
                temperature=temperature,
                reasoning_effort=reasoning_effort,
                max_tokens=max_tokens,
            )
            if key_strategies.strip():
                break
            print(
                f"  Empty key-strategy output on attempt {attempt}/{empty_attempts}; "
                "retrying..." if attempt < empty_attempts else "  Empty output after retries; marking failed.",
                flush=True,
            )
            if attempt < empty_attempts and sleep_seconds > 0:
                time.sleep(sleep_seconds)

        if key_strategies.strip():
            record["key_strategies"] = key_strategies
            record["key_strategy_status"] = "llm_generated_unreviewed"
            record["key_strategy_model"] = model
            record["key_strategy_extracted_at"] = now_iso()
            record.pop("key_strategy_error", None)
        else:
            record["key_strategies"] = ""
            record["key_strategy_status"] = "empty_llm_output"
            record["key_strategy_model"] = model
            record["key_strategy_extracted_at"] = now_iso()
            record["key_strategy_error"] = "LLM returned empty key-strategy text after retries."

        write_library(records, library_path, json_mirror_path)
        if sleep_seconds > 0:
            time.sleep(sleep_seconds)


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------


def parse_reasoning_effort(value: str) -> Optional[str]:
    value = (value or "none").strip().lower()
    if value == "none":
        return None
    if value not in {"low", "medium", "high"}:
        raise argparse.ArgumentTypeError("reasoning effort must be one of: none, low, medium, high")
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract key strategies from the HDS PDF-aligned natural-language proof library."
    )
    parser.add_argument("--library", type=Path, default=DEFAULT_LIBRARY_PATH, help=f"Input/output JSONL library. Default: {DEFAULT_LIBRARY_PATH}")
    parser.add_argument("--json-mirror", type=Path, default=DEFAULT_JSON_MIRROR_PATH, help=f"Optional JSON mirror. Default: {DEFAULT_JSON_MIRROR_PATH}")
    parser.add_argument("--until", type=int, default=None, help="Process records from the beginning through this item number.")
    parser.add_argument("--limit", type=int, default=None, help="Alias for --until.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"OpenAI model. Default: {DEFAULT_MODEL}")
    parser.add_argument("--api-base", default=DEFAULT_API_BASE, help=f"OpenAI-compatible API base. Default: {DEFAULT_API_BASE}")
    parser.add_argument("--temperature", type=float, default=1.0, help="API temperature. Default: 1.0")
    parser.add_argument("--max-tokens", type=int, default=700, help="Maximum completion tokens. Default: 700")
    parser.add_argument("--reasoning-effort", type=parse_reasoning_effort, default="high", help="Reasoning effort if supported by model: none, low, medium, high. Default: high")
    parser.add_argument("--sleep", type=float, default=0.0, help="Seconds to sleep between API calls. Default: 0")
    parser.add_argument("--no-resume", action="store_true", help="Recompute even if key_strategies already exists.")
    parser.add_argument("--dry-run", action="store_true", help="Preview work without API calls or file writes.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    until = args.until if args.until is not None else args.limit
    if until is not None and until <= 0:
        raise SystemExit("--until/--limit must be a positive integer")

    load_project_env(override=True)
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key and not args.dry_run:
        raise SystemExit("OPENAI_API_KEY is not set. Add it to .env or export it before running.")

    records = read_jsonl(args.library)
    if not records:
        raise SystemExit(f"No records found in {args.library}")

    process_records(
        records=records,
        until=until,
        api_key=api_key,
        model=args.model,
        api_base=args.api_base,
        temperature=args.temperature,
        reasoning_effort=args.reasoning_effort,
        max_tokens=args.max_tokens,
        sleep_seconds=args.sleep,
        resume=not args.no_resume,
        dry_run=args.dry_run,
        library_path=args.library,
        json_mirror_path=args.json_mirror,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
