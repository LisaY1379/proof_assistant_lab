#!/usr/bin/env python3
"""
Clean HighDimensionalStatistics PDF-extracted statement/proof text into readable
Markdown + LaTeX.

Input:
  data/high_dimensional_statistics/processed/proofs_with_key_strategies.jsonl

Output fields added to each record:
  - plain_english_statement_cleaned
  - plain_english_proof_cleaned

The raw fields are preserved:
  - plain_english_statement
  - plain_english_proof

The script deduplicates identical raw statement/proof pairs before calling the LLM,
so declarations aligned to the same textbook unit reuse the same cleaned text.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import ssl
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATASET_ROOT = PROJECT_ROOT / "data" / "high_dimensional_statistics"
PROCESSED_DIR = DATASET_ROOT / "processed"
INPUT_JSONL = PROCESSED_DIR / "proofs_with_key_strategies.jsonl"
INPUT_JSON = PROCESSED_DIR / "proofs_with_key_strategies.json"
CACHE_JSON = PROCESSED_DIR / "pdf_text_cleaning_cache.json"

WORKFLOW_NAME = "02_pdf_text_extraction/clean_hds_pdf_text.py"
WORKFLOW_VERSION = "0.1.0"
PROMPT_VERSION = "hds_pdf_clean_markdown_latex_v1"

SYSTEM_PROMPT = r"""You are a careful mathematical editor cleaning text extracted from a PDF of a high-dimensional statistics textbook.

Your job is not to invent new mathematics. Your job is to preserve the original meaning while fixing PDF-extraction artifacts and formatting the result as clean Markdown with LaTeX.

Rules:
- Preserve all assumptions, constants, quantifiers, inequalities, and probability statements.
- Convert mathematical expressions into valid LaTeX.
- Use \( ... \) for inline mathematics.
- Use \[ ... \] for displayed equations when appropriate.
- Fix obvious extraction artifacts, for example IRd -> \mathbb{R}^d, . . . -> \ldots, c⊤x -> c^\top x, X1 -> X_1 when clearly indexed.
- Keep paragraph breaks when they help readability.
- Do not add explanations beyond what the text says.
- If text is empty, return an empty string.
- Return only the cleaned text, with no preamble and no markdown fence.
"""


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_dotenv(path: Path) -> None:
    """Load project .env. Project-local values override the current shell."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ[key] = value


def read_json_records(path: Path) -> List[Dict[str, Any]]:
    """Read either a JSON array or pretty/multiline JSONL object stream."""
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []
    try:
        obj = json.loads(text)
        if isinstance(obj, list):
            return obj
        if isinstance(obj, dict):
            return [obj]
    except json.JSONDecodeError:
        pass

    decoder = json.JSONDecoder()
    records: List[Dict[str, Any]] = []
    idx = 0
    n = len(text)
    while idx < n:
        while idx < n and text[idx].isspace():
            idx += 1
        if idx >= n:
            break
        obj, end = decoder.raw_decode(text, idx)
        if not isinstance(obj, dict):
            raise ValueError(f"Expected JSON object at character {idx}, got {type(obj).__name__}")
        records.append(obj)
        idx = end
    return records


def write_jsonl(path: Path, records: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False, indent=2))
            f.write("\n")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def call_openai_chat(
    *,
    api_key: str,
    model: str,
    system_prompt: str,
    user_prompt: str,
    api_base: str = "https://api.openai.com/v1",
    temperature: float = 1.0,
    max_tokens: int = 1600,
    reasoning_effort: Optional[str] = None,
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


def normalize_blank_lines(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def make_cleanup_prompt(kind: str, raw_text: str, context: Dict[str, str]) -> str:
    return f"""Clean the following PDF-extracted {kind} into readable Markdown + LaTeX.

Context, for disambiguation only:
Lean-side comment:
{context.get('comment') or '[none]'}

Lean declaration/proof code:
{context.get('lean_original_code') or '[none]'}

Raw PDF-extracted {kind}:
{raw_text or ''}

Return only the cleaned {kind}. If the raw text is empty, return an empty string."""


def load_cache(path: Path) -> Dict[str, str]:
    if not path.exists():
        return {}
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(obj, dict):
            # Do not reuse empty cached cleanups for non-empty raw text. An empty
            # cleaned output is almost always a failed API response/formatting run.
            return {str(k): str(v) for k, v in obj.items() if str(v).strip()}
    except Exception:
        pass
    return {}


def save_cache(path: Path, cache: Dict[str, str]) -> None:
    write_json(path, cache)


def cache_key(kind: str, raw_text: str) -> str:
    return f"{kind}\n---\n{raw_text.strip()}"


def clean_one_text(
    *,
    kind: str,
    raw_text: str,
    context: Dict[str, str],
    cache: Dict[str, str],
    api_key: str,
    model: str,
    api_base: str,
    temperature: float,
    reasoning_effort: Optional[str],
    max_tokens: int,
    dry_run: bool,
) -> str:
    raw_text = normalize_blank_lines(raw_text or "")
    if not raw_text:
        return ""
    key = cache_key(kind, raw_text)
    if key in cache and str(cache[key]).strip():
        return cache[key]
    if key in cache and not str(cache[key]).strip():
        # Remove bad cache entries so interrupted/failed runs can recover.
        del cache[key]
        save_cache(CACHE_JSON, cache)
    if dry_run:
        return f"[DRY RUN: would clean {kind}; raw length={len(raw_text)}]"

    prompt = make_cleanup_prompt(kind, raw_text, context)
    cleaned = call_openai_chat(
        api_key=api_key,
        model=model,
        api_base=api_base,
        system_prompt=SYSTEM_PROMPT,
        user_prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        reasoning_effort=reasoning_effort,
    )
    cleaned = normalize_blank_lines(cleaned)

    if not cleaned:
        # Retry once with a stronger, shorter instruction. This prevents cases
        # where a model returns an empty string for a non-empty proof and that
        # empty value then gets cached forever.
        retry_prompt = f"""The previous cleanup returned empty text, but the raw {kind} is non-empty.

Rewrite the raw {kind} below as clean Markdown with valid LaTeX. Preserve the mathematical meaning. Return only the cleaned {kind}; do not return an empty response.

Raw {kind}:
{raw_text}
"""
        cleaned = call_openai_chat(
            api_key=api_key,
            model=model,
            api_base=api_base,
            system_prompt=SYSTEM_PROMPT,
            user_prompt=retry_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            reasoning_effort=reasoning_effort,
        )
        cleaned = normalize_blank_lines(cleaned)

    if not cleaned:
        raise RuntimeError(f"LLM returned empty cleaned {kind} for non-empty raw text; not caching failed output.")

    cache[key] = cleaned
    save_cache(CACHE_JSON, cache)
    return cleaned


def has_cleaned_fields(record: Dict[str, Any]) -> bool:
    raw_statement = str(record.get("plain_english_statement", "")).strip()
    raw_proof = str(record.get("plain_english_proof", "")).strip()
    if raw_statement and not str(record.get("plain_english_statement_cleaned", "")).strip():
        return False
    if raw_proof and not str(record.get("plain_english_proof_cleaned", "")).strip():
        return False
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean HDS PDF-extracted statement/proof text into Markdown + LaTeX.")
    parser.add_argument("--until", "--until-proof", dest="until", type=int, default=None, help="Clean records through this 1-based proof index.")
    parser.add_argument("--limit", type=int, default=None, help="Clean only first N records after applying --until, useful for testing.")
    parser.add_argument("--model", default="gpt-4.1-mini", help="OpenAI model. Default: gpt-4.1-mini")
    parser.add_argument("--api-base", default="https://api.openai.com/v1", help="OpenAI-compatible API base URL.")
    parser.add_argument("--temperature", type=float, default=1.0, help="Temperature. Default: 1.0")
    parser.add_argument("--reasoning-effort", choices=["low", "medium", "high", "none"], default="none", help="Reasoning effort. Use 'none' to omit the parameter. Default: none.")
    parser.add_argument("--max-tokens", type=int, default=1800, help="Max completion tokens per cleanup call.")
    parser.add_argument("--no-resume", action="store_true", help="Re-clean records even if cleaned fields already exist.")
    parser.add_argument("--dry-run", action="store_true", help="Preview work without API calls or file writes.")
    args = parser.parse_args()

    load_dotenv(PROJECT_ROOT / ".env")
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key and not args.dry_run:
        raise RuntimeError("OPENAI_API_KEY is not set. Put it in .env or export it before running.")

    records = read_json_records(INPUT_JSONL)
    total_records = len(records)
    selected = records[: args.until] if args.until is not None else records
    if args.limit is not None:
        selected = selected[: args.limit]

    pending_indices: List[int] = []
    for i, rec in enumerate(selected):
        raw_statement = str(rec.get("plain_english_statement", "")).strip()
        raw_proof = str(rec.get("plain_english_proof", "")).strip()
        if not raw_statement and not raw_proof:
            continue
        if args.no_resume or not has_cleaned_fields(rec):
            pending_indices.append(i)

    unique_texts = set()
    for i in pending_indices:
        rec = records[i]
        if str(rec.get("plain_english_statement", "")).strip():
            unique_texts.add(cache_key("statement", str(rec.get("plain_english_statement", ""))))
        if str(rec.get("plain_english_proof", "")).strip():
            unique_texts.add(cache_key("proof", str(rec.get("plain_english_proof", ""))))

    print(f"Loaded records: {total_records}")
    print(f"Selected records: {len(selected)}")
    print(f"Pending records needing cleanup: {len(pending_indices)}")
    print(f"Unique raw statement/proof texts needing or using cache: {len(unique_texts)}")

    if args.dry_run:
        for i in pending_indices[:10]:
            rec = records[i]
            print(f"  would clean record #{i + 1}: statement_len={len(str(rec.get('plain_english_statement', '')))}, proof_len={len(str(rec.get('plain_english_proof', '')))}")
        print("Dry run: no API calls and no files written.")
        return

    cache = load_cache(CACHE_JSON)
    reasoning_effort = None if args.reasoning_effort == "none" else args.reasoning_effort

    if pending_indices:
        backup = INPUT_JSONL.with_name(INPUT_JSONL.name + f".bak_before_clean_hds_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        shutil.copy2(INPUT_JSONL, backup)
        print(f"Backup written before cleanup: {backup.relative_to(PROJECT_ROOT)}")

    for count, i in enumerate(pending_indices, start=1):
        rec = records[i]
        context = {
            "comment": str(rec.get("comment", "")),
            "lean_original_code": str(rec.get("lean_original_code", "")),
        }
        print(f"[{count}/{len(pending_indices)}] Cleaning record #{i + 1}")

        raw_statement = str(rec.get("plain_english_statement", ""))
        raw_proof = str(rec.get("plain_english_proof", ""))

        if raw_statement.strip():
            rec["plain_english_statement_cleaned"] = clean_one_text(
                kind="statement",
                raw_text=raw_statement,
                context=context,
                cache=cache,
                api_key=api_key,
                model=args.model,
                api_base=args.api_base,
                temperature=args.temperature,
                reasoning_effort=reasoning_effort,
                max_tokens=args.max_tokens,
                dry_run=False,
            )
        else:
            rec["plain_english_statement_cleaned"] = ""

        if raw_proof.strip():
            rec["plain_english_proof_cleaned"] = clean_one_text(
                kind="proof",
                raw_text=raw_proof,
                context=context,
                cache=cache,
                api_key=api_key,
                model=args.model,
                api_base=args.api_base,
                temperature=args.temperature,
                reasoning_effort=reasoning_effort,
                max_tokens=args.max_tokens,
                dry_run=False,
            )
        else:
            rec["plain_english_proof_cleaned"] = ""

        rec["pdf_text_cleaning_workflow"] = WORKFLOW_NAME
        rec["pdf_text_cleaning_workflow_version"] = WORKFLOW_VERSION
        rec["pdf_text_cleaning_prompt_version"] = PROMPT_VERSION
        rec["pdf_text_cleaning_model"] = args.model
        rec["pdf_text_cleaned_at"] = now_iso()

        # Save after every record so long jobs can be resumed safely.
        write_jsonl(INPUT_JSONL, records)
        write_json(INPUT_JSON, records)

    print("Done.")
    print(f"Updated: {INPUT_JSONL.relative_to(PROJECT_ROOT)}")
    print(f"Updated: {INPUT_JSON.relative_to(PROJECT_ROOT)}")
    print(f"Cache:   {CACHE_JSON.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
