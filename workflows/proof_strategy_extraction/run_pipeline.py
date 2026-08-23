#!/usr/bin/env python3
"""
Proof Strategy Extraction Pipeline for ATLAS RealAnalysis

This workflow processes raw Lean proofs from ATLAS RealAnalysis in three major stages:

1. Extract Lean proof/declaration blocks from raw `.lean` files.
2. Split each proof into enumerated Lean steps.
3. For each Lean step, call an OpenAI-compatible API and translate the step into
   plain English.
4. For each full proof, call the API again to identify the key proof strategies / key
   ideas that make the proof work.
5. Save the final proof records with:
      - proof_id
      - lean_name
      - enumerated Lean original code
      - enumerated plain-English step translations
      - key_strategies

This script is intentionally dependency-light and uses only the Python standard library.
It expects the API key in the environment variable:

    OPENAI_API_KEY

Example usage from repository root:

    python workflows/proof_strategy_extraction/run_pipeline.py --limit 5

Full run:

    python workflows/proof_strategy_extraction/run_pipeline.py

Dry run without API calls:

    python workflows/proof_strategy_extraction/run_pipeline.py --limit 5 --dry-run

Outputs:

    data/processed/real_analysis_extracted_proofs.jsonl
    data/processed/translated_proofs.jsonl
    data/annotations/key_strategy_labels.jsonl
    data/processed/proofs_with_key_strategies.jsonl
    data/metadata/proof_strategy_pipeline_run.json

Important limitations:
- This is a heuristic extractor, not a full Lean parser.
- Step splitting is line-based by default, so some Lean steps may be too coarse or too fine.
- LLM outputs should be reviewed before being treated as reliable mathematical annotations.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import re
import subprocess
import ssl
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


# Proof-strategy extraction should only process declarations that actually
# contain proofs. In the RealAnalysis subset, these are `theorem` and `lemma`.
# Definitions/classes/structures should be handled by a separate concept-
# explanation workflow, not by this proof-strategy workflow.
ALLOWED_PROOF_KINDS = {"theorem", "lemma"}

# Use a broad declaration regex for block boundaries, but only process
# ALLOWED_PROOF_KINDS below. This prevents a theorem block from swallowing a
# following def/class/structure/comment before the next theorem.
DECL_START_RE = re.compile(
    r"^(?P<prefix>\s*)(?P<visibility>private\s+|protected\s+)?"
    r"(?P<kind>theorem|lemma|def|structure|class|instance|abbrev|example)\b(?P<rest>.*)$"
)

IMPORT_RE = re.compile(r"^\s*import\s+(.+?)\s*$")


TEXTBOOK_PROOF_PROMPT = (
    "You are translating a Lean proof into a textbook-style mathematical proof explanation. "
    "Do NOT merely translate symbols literally. Explain the mathematical role of the Lean proof as "
    "a human real-analysis textbook would. Use the theorem comment and formal statement as context. "
    "Mention the core theorems, reductions, rewrites, constructions, or compactness/continuity ideas "
    "being used. Avoid Lean-specific phrasing unless it is essential. Return a coherent textbook-style "
    "proof explanation, not a line-by-line syntax gloss."
)

KEY_STRATEGY_PROMPT = (
    "THINK HARD and identify THE KEYS to this proof "
    "(hint: what is THE GENIUS IDEAS where the proof could not work without it?) "
    "Summarize EACH KEY in one sentence. ENUMERATE EACH sentence and put a number before it."
)


# -----------------------------------------------------------------------------
# Basic utilities
# -----------------------------------------------------------------------------


def now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat()


def stable_hash(text: str, length: int = 12) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:length]


def ensure_dirs(out_dir: Path) -> Dict[str, Path]:
    paths = {
        "processed": out_dir / "processed",
        "annotations": out_dir / "annotations",
        "metadata": out_dir / "metadata",
    }
    for p in paths.values():
        p.mkdir(parents=True, exist_ok=True)
    return paths


def format_json_record(row: Dict[str, Any]) -> str:
    """Return a human-readable JSON representation for one output record."""
    return json.dumps(row, ensure_ascii=False, sort_keys=True, indent=2)


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> int:
    """
    Write records in a readable JSONL-like format.

    Each record is pretty-printed with indentation, then separated by a blank line.
    This is easier to inspect by hand than compact one-line JSON. The matching
    read_jsonl function below can read this multi-line format back in.
    """
    count = 0
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            if count:
                f.write("\n")
            f.write(format_json_record(row) + "\n")
            count += 1
    return count


def append_jsonl(path: Path, row: Dict[str, Any]) -> None:
    """Append one pretty-printed record to a JSONL-like output file."""
    needs_separator = path.exists() and path.stat().st_size > 0
    with path.open("a", encoding="utf-8") as f:
        if needs_separator:
            f.write("\n")
        f.write(format_json_record(row) + "\n")


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    """
    Read either compact JSONL or this pipeline's pretty-printed JSONL-like format.

    The writer stores one pretty-printed JSON object per record, separated by a
    blank line. For backward compatibility, this reader also accepts traditional
    one-object-per-line JSONL files.
    """
    if not path.exists():
        return []

    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []

    # First try ordinary JSONL, for compatibility with older outputs.
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

    # Then parse pretty-printed records by tracking balanced braces.
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
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def get_git_commit(repo_root: Path) -> Optional[str]:
    """Return git commit hash for the external ATLAS repo if available."""
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except Exception:
        return None


def find_lean_files(atlas_dir: Path) -> List[Path]:
    return sorted(p for p in atlas_dir.rglob("*.lean") if p.is_file())


def file_imports(text: str) -> List[str]:
    imports: List[str] = []
    for line in text.splitlines():
        m = IMPORT_RE.match(line)
        if m:
            imports.append(m.group(1).strip())
    return imports


# -----------------------------------------------------------------------------
# Stage 1: Extract proof blocks from Lean files
# -----------------------------------------------------------------------------


def extract_decl_name(kind: str, rest: str, fallback: str) -> str:
    """Extract a likely Lean declaration name from the declaration line."""
    if kind == "example":
        return fallback

    rest = rest.strip()
    if not rest:
        return fallback

    token = re.split(r"[\s(:=]", rest, maxsplit=1)[0].strip()
    if token and token not in {":", ":=", "by"}:
        return token
    return fallback


def clean_lean_doc_comment(raw: str) -> str:
    """Convert a Lean doc/comment block into readable text."""
    text = raw.strip()
    if text.startswith("/--"):
        text = text[3:]
    elif text.startswith("/-"):
        text = text[2:]
    if text.endswith("-/"):
        text = text[:-2]

    cleaned_lines: List[str] = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("--"):
            line = line[2:].strip()
        if line.startswith("*"):
            line = line[1:].strip()
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines).strip()


def extract_preceding_comment(lines: List[str], decl_start_i: int) -> str:
    """Return the doc/comment immediately preceding a declaration, if present.

    Supports Lean doc comments `/-- ... -/`, ordinary block comments `/- ... -/`,
    and consecutive single-line comments `-- ...` directly above the declaration.
    """
    j = decl_start_i - 1
    while j >= 0 and not lines[j].strip():
        j -= 1
    if j < 0:
        return ""

    stripped = lines[j].strip()

    # Block/doc comment ending immediately before the theorem/lemma.
    if stripped.endswith("-/"):
        end_j = j
        while j >= 0 and "/-" not in lines[j]:
            j -= 1
        if j >= 0:
            raw = "\n".join(lines[j : end_j + 1])
            return clean_lean_doc_comment(raw)
        return ""

    # Consecutive single-line comments immediately above the theorem/lemma.
    if stripped.startswith("--"):
        comment_lines: List[str] = []
        while j >= 0 and lines[j].strip().startswith("--"):
            comment_lines.append(lines[j])
            j -= 1
        comment_lines.reverse()
        return clean_lean_doc_comment("\n".join(comment_lines))

    return ""


def iter_declaration_blocks(text: str) -> Iterable[Tuple[int, int, str, str, str, str]]:
    """Yield rough top-level declaration blocks.

    Returns:
        (start_line, end_line, kind, first_line, block_text, preceding_comment)

    This is heuristic: it finds top-level declaration lines and treats everything
    up to the next top-level declaration as part of the block. It uses all common
    Lean declaration types as boundaries, but callers can filter which kinds to
    process.
    """
    lines = text.splitlines()
    starts: List[Tuple[int, re.Match[str]]] = []

    for i, line in enumerate(lines):
        m = DECL_START_RE.match(line)
        if m and len(m.group("prefix")) == 0:
            starts.append((i, m))

    for idx, (start_i, match) in enumerate(starts):
        end_i = starts[idx + 1][0] if idx + 1 < len(starts) else len(lines)
        block_lines = lines[start_i:end_i]
        block_text = "\n".join(block_lines).strip()
        if not block_text:
            continue
        comment = extract_preceding_comment(lines, start_i)
        yield start_i + 1, end_i, match.group("kind"), lines[start_i], block_text, comment


def split_statement_and_proof(block_text: str) -> Tuple[str, str, bool]:
    """Split a declaration block into rough formal statement and proof code."""
    markers = [":= by", ":="]
    for marker in markers:
        pos = block_text.find(marker)
        if pos != -1:
            statement = block_text[:pos].strip()
            proof = block_text[pos:].strip()
            return statement, proof, True

    m = re.search(r"\n\s*by\b", block_text)
    if m:
        statement = block_text[: m.start()].strip()
        proof = block_text[m.start() :].strip()
        return statement, proof, True

    return block_text.strip(), "", False


def extract_proofs(atlas_dir: Path, atlas_repo_root: Path, limit: Optional[int] = None) -> List[Dict[str, Any]]:
    lean_files = find_lean_files(atlas_dir)
    commit = get_git_commit(atlas_repo_root)
    records: List[Dict[str, Any]] = []

    for file_path in lean_files:
        text = read_text(file_path)
        imports = file_imports(text)
        rel_file = file_path.as_posix()

        try:
            rel_file = file_path.relative_to(Path.cwd()).as_posix()
        except ValueError:
            pass

        for start_line, end_line, kind, first_line, block_text, comment in iter_declaration_blocks(text):
            if kind not in ALLOWED_PROOF_KINDS:
                continue

            fallback_name = f"anonymous_{stable_hash(rel_file + ':' + str(start_line))}"
            first_line_match = DECL_START_RE.match(first_line)
            rest = first_line_match.group("rest") if first_line_match else ""
            lean_name = extract_decl_name(kind, rest, fallback_name)
            statement, proof_code, has_proof = split_statement_and_proof(block_text)

            proof_id = "atlas.real_analysis." + stable_hash(f"{rel_file}:{start_line}:{lean_name}:{block_text}")
            records.append(
                {
                    "proof_id": proof_id,
                    "source": "atlas-lean",
                    "source_subset": "Atlas/RealAnalysis",
                    "atlas_commit": commit,
                    "source_file": rel_file,
                    "start_line": start_line,
                    "end_line": end_line,
                    "kind": kind,
                    "lean_name": lean_name,
                    "formal_statement": statement,
                    "comment": comment,
                    "proof_code": proof_code,
                    "raw_declaration": block_text,
                    "imports": imports,
                    "has_detected_proof": has_proof,
                }
            )

            if limit is not None and len(records) >= limit:
                return records

    return records


# -----------------------------------------------------------------------------
# Stage 2: Split proof into enumerated Lean steps
# -----------------------------------------------------------------------------


def strip_lean_block_comments(text: str) -> str:
    """Remove Lean block/doc comments from proof text.

    This is a heuristic text-level remover, not a full Lean lexer, but it avoids
    sending nearby prose comments to the proof-explanation stage.
    """
    return re.sub(r"/-.*?-\/", "", text, flags=re.DOTALL)


def strip_line_comment(line: str) -> str:
    """Remove simple Lean line comments while preserving code before `--`.

    This is intentionally simple and does not handle strings containing `--`.
    """
    if "--" in line:
        return line.split("--", 1)[0]
    return line


def split_proof_into_steps(proof_code: str) -> List[Dict[str, Any]]:
    """Split a Lean proof into numbered steps.

    Current policy: one non-empty, non-comment line becomes one step. This keeps the
    correspondence transparent and easy to review, though it may be refined later into
    AST- or tactic-aware segmentation.
    """
    proof_code = strip_lean_block_comments(proof_code)
    steps: List[Dict[str, Any]] = []
    for raw_line in proof_code.splitlines():
        cleaned = strip_line_comment(raw_line).rstrip()
        if not cleaned.strip():
            continue
        if cleaned.strip().startswith("/-") or cleaned.strip().startswith("-/"):
            continue
        steps.append(
            {
                "step_number": len(steps) + 1,
                "lean_step": cleaned.strip(),
            }
        )
    return steps


def format_enumerated_steps(steps: List[Dict[str, Any]], field: str) -> str:
    """Return numbered text from a list of step records."""
    lines: List[str] = []
    for step in steps:
        value = str(step.get(field, "")).strip()
        lines.append(f"{step['step_number']}. {value}")
    return "\n".join(lines)


# -----------------------------------------------------------------------------
# OpenAI-compatible API calls
# -----------------------------------------------------------------------------


def call_openai_chat(
    *,
    api_key: str,
    model: str,
    system_prompt: str,
    user_prompt: str,
    api_base: str = "https://api.openai.com/v1",
    temperature: float = 1.0,
    max_tokens: int = 500,
    reasoning_effort: Optional[str] = "high",
    timeout: int = 120,
    max_retries: int = 3,
    retry_sleep: float = 2.0,
) -> str:
    """Call OpenAI Chat Completions API using only Python stdlib."""
    url = api_base.rstrip("/") + "/chat/completions"
    payload = {
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

    ssl_context = None
    try:
        import certifi  # type: ignore

        ssl_context = ssl.create_default_context(cafile=certifi.where())
    except Exception:
        # Fall back to Python's default certificate configuration. If that is broken,
        # the resulting SSL error will explain the issue to the user.
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


def generate_textbook_proof_explanation(
    *,
    lean_name: str,
    formal_statement: str,
    comment: str,
    enumerated_lean_code: str,
    api_key: str,
    model: str,
    api_base: str,
    temperature: float,
    reasoning_effort: Optional[str],
) -> str:
    user_prompt = (
        f"Lean theorem/proof name: {lean_name}\n\n"
        f"Comment before theorem, if available:\n{comment or '[No preceding comment found]'}\n\n"
        f"Formal statement:\n{formal_statement}\n\n"
        "Enumerated Lean proof code:\n"
        f"{enumerated_lean_code}\n\n"
        "Write a textbook-style English proof explanation after reading the entire Lean proof. "
        "Do not translate each symbol mechanically. Explain the mathematical argument, why the steps work, "
        "and how the Lean proof establishes the theorem. Return only the English proof explanation."
    )
    return call_openai_chat(
        api_key=api_key,
        model=model,
        api_base=api_base,
        system_prompt=TEXTBOOK_PROOF_PROMPT,
        user_prompt=user_prompt,
        temperature=temperature,
        max_tokens=900,
        reasoning_effort=reasoning_effort,
    )

def identify_key_strategies(
    *,
    lean_name: str,
    formal_statement: str,
    comment: str,
    enumerated_lean_code: str,
    textbook_explanation: str,
    api_key: str,
    model: str,
    api_base: str,
    temperature: float,
    reasoning_effort: Optional[str],
) -> str:
    user_prompt = (
        f"Lean theorem/proof name: {lean_name}\n\n"
        f"Comment before theorem, if available:\n{comment or '[No preceding comment found]'}\n\n"
        f"Formal statement, if available:\n{formal_statement}\n\n"
        "Enumerated Lean original code:\n"
        f"{enumerated_lean_code}\n\n"
        "Textbook-style English proof explanation:\n"
        f"{textbook_explanation}\n\n"
        f"{KEY_STRATEGY_PROMPT}\n\n"
        "Return only the enumerated key ideas."
    )
    return call_openai_chat(
        api_key=api_key,
        model=model,
        api_base=api_base,
        system_prompt="You are a careful mathematical proof analyst. Focus on core proof ideas, not superficial syntax.",
        user_prompt=user_prompt,
        temperature=temperature,
        max_tokens=700,
        reasoning_effort=reasoning_effort,
    )


# -----------------------------------------------------------------------------
# Stage 3-5: Translate steps and attach key strategies
# -----------------------------------------------------------------------------


def load_existing_by_proof_id(path: Path) -> Dict[str, Dict[str, Any]]:
    return {row["proof_id"]: row for row in read_jsonl(path) if "proof_id" in row}


def process_proofs_with_llm(
    *,
    proofs: List[Dict[str, Any]],
    translated_path: Path,
    key_labels_path: Path,
    final_path: Path,
    api_key: str,
    model: str,
    api_base: str,
    temperature: float,
    reasoning_effort: Optional[str],
    sleep_seconds: float,
    resume: bool,
    dry_run: bool,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Translate proof steps and identify key strategies.

    If resume=True, already translated/key-labeled proof records are loaded from disk
    and not recomputed.
    """
    existing_translated = load_existing_by_proof_id(translated_path) if resume else {}
    existing_keys = load_existing_by_proof_id(key_labels_path) if resume else {}
    existing_final = load_existing_by_proof_id(final_path) if resume else {}

    translated_records: List[Dict[str, Any]] = []
    key_label_records: List[Dict[str, Any]] = []
    final_records: List[Dict[str, Any]] = []

    if dry_run:
        # Build a small preview without calling the API.
        for proof in proofs:
            steps = split_proof_into_steps(proof.get("proof_code", ""))
            enumerated_lean = format_enumerated_steps(steps, "lean_step")
            textbook_explanation = "[DRY RUN] A textbook-style proof explanation would be generated by the API after reading the whole Lean proof."
            key_strategies = "1. [DRY RUN] Key strategies would be generated by the API."
            translated_records.append(make_translated_record(proof, steps, enumerated_lean, textbook_explanation, model))
            key_label_records.append(make_key_label_record(proof, key_strategies, model))
            final_records.append(make_final_record(proof, steps, enumerated_lean, textbook_explanation, key_strategies, model))
        return translated_records, key_label_records, final_records

    for i, proof in enumerate(proofs, start=1):
        proof_id = proof["proof_id"]
        print(f"Processing proof {i}/{len(proofs)}: {proof.get('lean_name')} ({proof_id})")

        if proof_id in existing_final:
            print("  - Found existing final record; reusing.")
            final_record = existing_final[proof_id]
            final_records.append(final_record)
            if proof_id in existing_translated:
                translated_records.append(existing_translated[proof_id])
            if proof_id in existing_keys:
                key_label_records.append(existing_keys[proof_id])
            continue

        # Whole-proof textbook explanation stage.
        if proof_id in existing_translated:
            print("  - Found existing textbook-explanation record; reusing.")
            translated_record = existing_translated[proof_id]
            steps = translated_record.get("steps", [])
            enumerated_lean = translated_record.get("lean_original_code", "")
            textbook_explanation = translated_record.get("plain_english", translated_record.get("textbook_explanation", ""))
        else:
            steps = split_proof_into_steps(proof.get("proof_code", ""))
            enumerated_lean = format_enumerated_steps(steps, "lean_step")
            print("  - Generating textbook-style proof explanation")
            textbook_explanation = generate_textbook_proof_explanation(
                lean_name=proof.get("lean_name", ""),
                formal_statement=proof.get("formal_statement", ""),
                comment=proof.get("comment", ""),
                enumerated_lean_code=enumerated_lean,
                api_key=api_key,
                model=model,
                api_base=api_base,
                temperature=temperature,
                reasoning_effort=reasoning_effort,
            )
            if sleep_seconds > 0:
                time.sleep(sleep_seconds)

            translated_record = make_translated_record(proof, steps, enumerated_lean, textbook_explanation, model)
            append_jsonl(translated_path, translated_record)

        translated_records.append(translated_record)

        # Key-strategy extraction stage.
        if proof_id in existing_keys:
            print("  - Found existing key-strategy record; reusing.")
            key_label_record = existing_keys[proof_id]
            key_strategies = key_label_record.get("key_strategies", "")
        else:
            print("  - Identifying key strategies")
            key_strategies = identify_key_strategies(
                lean_name=proof.get("lean_name", ""),
                formal_statement=proof.get("formal_statement", ""),
                enumerated_lean_code=enumerated_lean,
                comment=proof.get("comment", ""),
                textbook_explanation=textbook_explanation,
                api_key=api_key,
                model=model,
                api_base=api_base,
                temperature=temperature,
                reasoning_effort=reasoning_effort,
            )
            key_label_record = make_key_label_record(proof, key_strategies, model)
            append_jsonl(key_labels_path, key_label_record)
            if sleep_seconds > 0:
                time.sleep(sleep_seconds)

        key_label_records.append(key_label_record)

        final_record = make_final_record(proof, steps, enumerated_lean, textbook_explanation, key_strategies, model)
        append_jsonl(final_path, final_record)
        final_records.append(final_record)

    return translated_records, key_label_records, final_records


def make_translated_record(
    proof: Dict[str, Any],
    steps: List[Dict[str, Any]],
    enumerated_lean: str,
    textbook_explanation: str,
    model: str,
) -> Dict[str, Any]:
    return {
        "proof_id": proof["proof_id"],
        "lean_name": proof["lean_name"],
        "source_file": proof["source_file"],
        "start_line": proof.get("start_line"),
        "end_line": proof.get("end_line"),
        "formal_statement": proof.get("formal_statement", ""),
        "comment": proof.get("comment", ""),
        "lean_original_code": enumerated_lean,
        "plain_english": textbook_explanation,
        "textbook_explanation": textbook_explanation,
        "steps": steps,
        "translation_model": model,
        "created_at": now_iso(),
    }


def make_key_label_record(proof: Dict[str, Any], key_strategies: str, model: str) -> Dict[str, Any]:
    return {
        "proof_id": proof["proof_id"],
        "lean_name": proof["lean_name"],
        "source_file": proof["source_file"],
        "formal_statement": proof.get("formal_statement", ""),
        "comment": proof.get("comment", ""),
        "key_strategies": key_strategies,
        "strategy_model": model,
        "created_at": now_iso(),
    }


def make_final_record(
    proof: Dict[str, Any],
    steps: List[Dict[str, Any]],
    enumerated_lean: str,
    textbook_explanation: str,
    key_strategies: str,
    model: str,
) -> Dict[str, Any]:
    return {
        "proof_id": proof["proof_id"],
        "lean_name": proof["lean_name"],
        "source": proof.get("source"),
        "source_subset": proof.get("source_subset"),
        "atlas_commit": proof.get("atlas_commit"),
        "source_file": proof["source_file"],
        "start_line": proof.get("start_line"),
        "end_line": proof.get("end_line"),
        "kind": proof.get("kind"),
        "formal_statement": proof.get("formal_statement", ""),
        "comment": proof.get("comment", ""),
        "lean_original_code": enumerated_lean,
        "plain_english": textbook_explanation,
        "textbook_explanation": textbook_explanation,
        "key_strategies": key_strategies,
        "steps": steps,
        "model": model,
        "annotation_status": "llm_generated_unreviewed",
        "created_at": now_iso(),
    }


# -----------------------------------------------------------------------------
# CLI and main
# -----------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate textbook-style Lean proof explanations and extract key proof strategies.")
    parser.add_argument(
        "--atlas-dir",
        default="external/atlas-lean/Atlas/RealAnalysis",
        help="Path to ATLAS RealAnalysis directory. Default: external/atlas-lean/Atlas/RealAnalysis",
    )
    parser.add_argument(
        "--atlas-repo-root",
        default="external/atlas-lean",
        help="Path to root of cloned atlas-lean repo. Used to record git commit.",
    )
    parser.add_argument(
        "--out-dir",
        default="data",
        help="Output data directory. Default: data",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional maximum number of declarations to process, useful for testing.",
    )
    parser.add_argument(
        "--model",
        default="gpt-5.6-sol",
        help="OpenAI model for translation and strategy extraction. Default: gpt-5.6-sol",
    )
    parser.add_argument(
        "--api-base",
        default="https://api.openai.com/v1",
        help="OpenAI-compatible API base URL. Default: https://api.openai.com/v1",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=1.0,
        help="Sampling temperature. Default: 1.0",
    )
    parser.add_argument(
        "--reasoning-effort",
        choices=["low", "medium", "high"],
        default="high",
        help="Reasoning effort for reasoning-capable OpenAI models. Default: high",
    )
    parser.add_argument(
        "--sleep-seconds",
        type=float,
        default=0.0,
        help="Optional sleep between API calls to avoid rate limits. Default: 0.0",
    )
    parser.add_argument(
        "--no-resume",
        action="store_true",
        help="Do not reuse existing JSONL outputs. By default, the pipeline resumes from existing outputs.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run extraction and build preview records without calling the API or writing incremental outputs.",
    )
    return parser.parse_args()


def print_summary(
    proofs: List[Dict[str, Any]],
    translated_records: List[Dict[str, Any]],
    key_label_records: List[Dict[str, Any]],
    final_records: List[Dict[str, Any]],
) -> None:
    total_steps = sum(len(r.get("steps", [])) for r in final_records)
    print("\nProof strategy extraction pipeline summary")
    print("-" * 56)
    print(f"Extracted proof/declaration records: {len(proofs)}")
    print(f"Translated proof records:           {len(translated_records)}")
    print(f"Key-strategy records:               {len(key_label_records)}")
    print(f"Final proof records:                {len(final_records)}")
    print(f"Total enumerated steps:             {total_steps}")
    print()


def main() -> int:
    args = parse_args()
    atlas_dir = Path(args.atlas_dir)
    atlas_repo_root = Path(args.atlas_repo_root)
    out_dir = Path(args.out_dir)

    if not atlas_dir.exists():
        print(f"ERROR: ATLAS RealAnalysis directory does not exist: {atlas_dir}")
        print("\nExpected setup:")
        print("  git clone --filter=blob:none --sparse https://github.com/facebookresearch/atlas-lean.git external/atlas-lean")
        print("  cd external/atlas-lean")
        print("  git sparse-checkout set Atlas/RealAnalysis")
        return 1

    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not args.dry_run and not api_key:
        print("ERROR: OPENAI_API_KEY is not set.")
        print("Set it before running, for example:")
        print("  export OPENAI_API_KEY='your-api-key-here'")
        return 1

    dirs = ensure_dirs(out_dir)
    extracted_path = dirs["processed"] / "real_analysis_extracted_proofs.jsonl"
    translated_path = dirs["processed"] / "translated_proofs.jsonl"
    key_labels_path = dirs["annotations"] / "key_strategy_labels.jsonl"
    final_path = dirs["processed"] / "proofs_with_key_strategies.jsonl"
    metadata_path = dirs["metadata"] / "proof_strategy_pipeline_run.json"

    print(f"Reading ATLAS RealAnalysis from: {atlas_dir}")
    proofs = extract_proofs(atlas_dir=atlas_dir, atlas_repo_root=atlas_repo_root, limit=args.limit)

    # Keep only records with a detected proof body and at least one non-empty step.
    proofs = [p for p in proofs if p.get("has_detected_proof") and split_proof_into_steps(p.get("proof_code", ""))]

    if args.dry_run:
        print("Dry run: API calls will be skipped and output files will not be written.")
    else:
        write_jsonl(extracted_path, proofs)

    translated_records, key_label_records, final_records = process_proofs_with_llm(
        proofs=proofs,
        translated_path=translated_path,
        key_labels_path=key_labels_path,
        final_path=final_path,
        api_key=api_key,
        model=args.model,
        api_base=args.api_base,
        temperature=args.temperature,
        reasoning_effort=args.reasoning_effort,
        sleep_seconds=args.sleep_seconds,
        resume=not args.no_resume,
        dry_run=args.dry_run,
    )

    print_summary(proofs, translated_records, key_label_records, final_records)

    metadata = {
        "created_at": now_iso(),
        "pipeline_script": "workflows/proof_strategy_extraction/run_pipeline.py",
        "workflow_description": [
            "Extract Lean proofs from ATLAS RealAnalysis.",
            "Split each proof into enumerated Lean steps.",
            "Call OpenAI-compatible API once per proof to generate a textbook-style English proof explanation.",
            "Call API once per proof to identify enumerated key strategies.",
            "Attach key_strategies to the final proof record.",
        ],
        "atlas_dir": str(atlas_dir),
        "atlas_repo_root": str(atlas_repo_root),
        "atlas_commit": get_git_commit(atlas_repo_root),
        "limit": args.limit,
        "model": args.model,
        "api_base": args.api_base,
        "temperature": args.temperature,
        "reasoning_effort": args.reasoning_effort,
        "dry_run": args.dry_run,
        "resume": not args.no_resume,
        "prompts": {
            "textbook_proof_prompt": TEXTBOOK_PROOF_PROMPT,
            "key_strategy_prompt": KEY_STRATEGY_PROMPT,
        },
        "outputs": {
            "extracted_proofs": str(extracted_path),
            "translated_proofs": str(translated_path),
            "key_strategy_labels": str(key_labels_path),
            "proofs_with_key_strategies": str(final_path),
        },
        "counts": {
            "proof_records": len(proofs),
            "translated_records": len(translated_records),
            "key_strategy_records": len(key_label_records),
            "final_records": len(final_records),
            "total_steps": sum(len(r.get("steps", [])) for r in final_records),
        },
        "notes": [
            "Step splitting is currently line-based and should be reviewed.",
            "The plain_english field now stores a whole-proof textbook-style explanation, not per-step literal translations.",
            "LLM translations and key strategies are generated annotations, not verified facts.",
            "Raw ATLAS files are read from external/ and are not modified.",
        ],
    }

    if args.dry_run:
        print("Dry run only; no files written.")
    else:
        write_json(metadata_path, metadata)
        print("Wrote outputs:")
        print(f"  {extracted_path}")
        print(f"  {translated_path}")
        print(f"  {key_labels_path}")
        print(f"  {final_path}")
        print(f"  {metadata_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
