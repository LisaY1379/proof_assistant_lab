#!/usr/bin/env python3
"""
Repair failed/empty HDS reverse-engineered strategy-category entries.

This scans:
  data/high_dimensional_statistics/processed/proofs_with_key_strategies.jsonl

and regenerates `strategies_refined` only for records whose current value is:
  - missing
  - an empty list
  - contains category/status markers such as UNPARSED_RESPONSE or EMPTY_RESPONSE

It reuses the shared reverse-engineering logic from:
  workflows/proof_strategy_extraction/01_lean_translation/reverse_engineer_strategy_categories.py

but, like the HDS wrapper, it supplies the cleaned LaTeX textbook statement/proof as
the plain-English proof explanation sent to the LLM. It also passes the full
`lean_original_code` by injecting it into the formal-statement context used by the
shared reverse-engineering prompt.

Run from project root:

  .venv/bin/python workflows/proof_strategy_extraction/02_pdf_text_extraction/repair_hds_reverse_engineered_strategies.py --until-proof 58

Dry run:

  .venv/bin/python workflows/proof_strategy_extraction/02_pdf_text_extraction/repair_hds_reverse_engineered_strategies.py --until-proof 58 --dry-run
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SHARED_REVERSE = PROJECT_ROOT / "workflows" / "proof_strategy_extraction" / "01_lean_translation" / "reverse_engineer_strategy_categories.py"
HDS_PROCESSED = PROJECT_ROOT / "data" / "high_dimensional_statistics" / "processed"
HDS_PROOFS_JSONL = HDS_PROCESSED / "proofs_with_key_strategies.jsonl"
HDS_PROOFS_JSON = HDS_PROCESSED / "proofs_with_key_strategies.json"
HDS_CATEGORIES = HDS_PROCESSED / "strategy_categories.txt"

FAILED_CATEGORY_MARKERS = {
    "UNPARSED_RESPONSE",
    "EMPTY_RESPONSE",
    "EMPTY",
    "PARSE_ERROR",
    "ERROR",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_shared_reverse() -> Any:
    shared_dir = SHARED_REVERSE.parent
    if str(shared_dir) not in sys.path:
        sys.path.insert(0, str(shared_dir))

    spec = importlib.util.spec_from_file_location("hds_shared_reverse_engineer_repair", SHARED_REVERSE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not import shared reverse workflow: {SHARED_REVERSE}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def cleaned_hds_textbook_explanation(proof: Dict[str, Any]) -> str:
    statement = str(
        proof.get("plain_english_statement_cleaned")
        or proof.get("plain_english_statement")
        or proof.get("plain_english")
        or ""
    ).strip()
    proof_text = str(
        proof.get("plain_english_proof_cleaned")
        or proof.get("plain_english_proof")
        or ""
    ).strip()

    parts: List[str] = []
    if statement:
        parts.append("Statement:\n" + statement)
    if proof_text:
        parts.append("Proof:\n" + proof_text)
    return "\n\n---\n\n".join(parts)


def hds_formal_context_with_lean_code(proof: Dict[str, Any]) -> str:
    """Build formal context for the shared prompt, including full Lean code.

    The shared reverse-engineering script sends `formal_statement` but not
    `lean_original_code`. To avoid duplicating that script, this repair workflow
    places the full Lean block inside `formal_statement` for the copied prompt
    record.
    """
    formal_statement = str(proof.get("formal_statement") or "").strip()
    lean_original_code = str(proof.get("lean_original_code") or "").strip()
    official_decl = str(proof.get("official_lean_declaration") or proof.get("lean_name") or "").strip()
    official_file = str(proof.get("official_lean_file") or proof.get("source_file") or "").strip()

    parts: List[str] = []
    if formal_statement:
        parts.append("Formal statement:\n" + formal_statement)
    if official_decl or official_file:
        parts.append(
            "Official Lean target:\n"
            + (f"Declaration: {official_decl}\n" if official_decl else "")
            + (f"File: {official_file}" if official_file else "")
        )
    if lean_original_code:
        parts.append("Full Lean original code:\n" + lean_original_code)
    return "\n\n---\n\n".join(part for part in parts if part.strip())


def has_book_text(proof: Dict[str, Any]) -> bool:
    return bool(cleaned_hds_textbook_explanation(proof).strip())


def refinement_is_failed_or_empty(proof: Dict[str, Any]) -> bool:
    value = proof.get("strategies_refined")
    if not isinstance(value, list) or len(value) == 0:
        return True

    for item in value:
        if not isinstance(item, dict):
            return True
        category = str(item.get("category", "")).strip().upper()
        raw_category = str(item.get("raw_category", "")).strip().upper()
        if category in FAILED_CATEGORY_MARKERS or raw_category in FAILED_CATEGORY_MARKERS:
            return True
        if category.startswith("UNPARSED") or category.startswith("EMPTY"):
            return True
    return False


def strip_json_fence(text: str) -> str:
    stripped = str(text or "").strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped)
        stripped = re.sub(r"\s*```$", "", stripped)
    return stripped.strip()


def escape_invalid_json_backslashes(text: str) -> str:
    """Escape LaTeX-style backslashes that make model JSON invalid.

    Model responses often contain JSON strings with raw LaTeX like \(x\) or
    \mathbb{R}. In strict JSON, backslashes are only valid before characters such
    as `"`, `\\`, `/`, `b`, `f`, `n`, `r`, `t`, or `u`. This repair converts invalid
    occurrences like `\(`, `\m`, `\s` into `\\(`, `\\m`, `\\s` before json.loads.
    """
    return re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', text)


def parse_refined_response_tolerant(raw: str, shared: Any, category_names: List[str]) -> List[Dict[str, Any]]:
    """Parse a reverse-engineering response with a LaTeX-backslash repair fallback."""
    parsed = shared.parse_refined_response(raw, category_names)
    temp = {"strategies_refined": parsed}
    if not refinement_is_failed_or_empty(temp):
        return parsed

    text = strip_json_fence(raw)
    try:
        obj = json.loads(escape_invalid_json_backslashes(text))
    except Exception:
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            return parsed
        try:
            obj = json.loads(escape_invalid_json_backslashes(text[start : end + 1]))
        except Exception:
            return parsed

    items: Any
    if isinstance(obj, dict) and isinstance(obj.get("strategies_refined"), list):
        items = obj["strategies_refined"]
    elif isinstance(obj, list):
        items = obj
    elif isinstance(obj, dict):
        items = [obj]
    else:
        return parsed

    results: List[Dict[str, Any]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        category, exact = shared.normalize_category(str(item.get("category", "")), category_names)
        if not category:
            continue
        results.append(
            {
                "category": category,
                "evidence": str(item.get("evidence", item.get("where", ""))).strip(),
                "explanation": str(item.get("explanation", item.get("reason", ""))).strip(),
                "confidence": str(item.get("confidence", "medium")).strip().lower(),
                "category_name_match": exact,
                "raw_category": str(item.get("category", "")).strip(),
                "json_repaired_from_latex_backslashes": True,
            }
        )
    return results or parsed


def reverse_engineer_one_proof_tolerant(
    *,
    proof: Dict[str, Any],
    categories_text: str,
    category_names: List[str],
    api_key: str,
    model: str,
    api_base: str,
    temperature: float,
    reasoning_effort: Any,
    max_tokens: int,
    shared: Any,
) -> List[Dict[str, Any]]:
    """Same prompt as the shared reverse workflow, but with tolerant JSON parsing.

    We keep this local copy only for the repair workflow so that failed records like
    Proposition 1.1 can recover from raw LaTeX backslashes in JSON strings.
    """
    system_prompt = (
        "You are a careful real-analysis proof analyst. Your task is to reverse-engineer "
        "which proof-strategy categories appear in a proof, using only the provided category taxonomy. "
        "Choose categories because they explain the mathematical proof, not because of superficial wording."
    )
    allowed_categories = "\n".join(f"- {name}" for name in category_names)
    plain_english = proof.get("textbook_explanation") or proof.get("plain_english") or ""
    user_prompt = f"""
You are given one processed Lean theorem/lemma and a fixed strategy category taxonomy.

Your job:
1. Read the theorem comment, formal statement, Lean original code if included, and textbook-style English proof explanation.
2. Pick the strategy category/categories from the taxonomy that likely appear in this proof.
3. For each chosen category, explain which step or part of the proof corresponds to that category.
4. Use exact category names from the allowed list whenever possible.
5. Do not invent new categories unless no listed category fits; if you must invent one, make confidence low.
6. Do not over-classify routine wording: only include categories that genuinely help explain how the proof works.
7. Return at most 4 categories.
8. Keep each evidence and explanation under 30 words.
9. IMPORTANT: Return strict JSON. Inside JSON strings, avoid LaTeX backslash commands if possible; use plain Unicode/math words instead.

CATEGORY TAXONOMY:
{categories_text.strip()}

ALLOWED CATEGORY NAMES:
{allowed_categories}

PROOF RECORD:
Lean name: {proof.get('lean_name') or proof.get('official_lean_declaration') or proof.get('book_name')}
Proof id: {proof.get('proof_id') or proof.get('report_target_id')}

Comment before theorem:
{proof.get('comment') or '[No comment provided]'}

Formal statement / Lean context:
{proof.get('formal_statement') or '[No formal statement provided]'}

Textbook-style English proof explanation:
{plain_english or '[No textbook explanation provided]'}

Return strict JSON only in this exact shape:
{{
  "strategies_refined": [
    {{
      "category": "<exact category name from allowed list>",
      "evidence": "<which step/part of the proof shows this category>",
      "explanation": "<why this category is relevant to the proof>",
      "confidence": "high|medium|low"
    }}
  ]
}}
""".strip()
    raw = shared.call_openai_chat(
        api_key=api_key,
        model=model,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        api_base=api_base,
        temperature=temperature,
        max_completion_tokens=max_tokens,
        reasoning_effort=reasoning_effort,
    )
    return parse_refined_response_tolerant(raw, shared, category_names)


def make_backup(path: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = path.with_name(path.name + f".bak_repair_reverse_engineered_{stamp}")
    shutil.copy2(path, backup)
    return backup


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Repair failed/empty HDS strategies_refined entries by regenerating them with the API."
    )
    parser.add_argument(
        "--until-proof",
        type=int,
        default=58,
        help="Scan/regenerate HDS proofs from #1 through this proof number. Default: 58.",
    )
    parser.add_argument("--proofs-jsonl", type=Path, default=HDS_PROOFS_JSONL)
    parser.add_argument("--proofs-json", type=Path, default=HDS_PROOFS_JSON)
    parser.add_argument("--categories", type=Path, default=HDS_CATEGORIES)
    parser.add_argument("--model", default="gpt-5.6-sol", help="OpenAI model. Default: gpt-5.6-sol")
    parser.add_argument("--api-base", default="https://api.openai.com/v1")
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument(
        "--reasoning-effort",
        choices=["low", "medium", "high", "none"],
        default="high",
        help="Reasoning effort for supported models. Use none to omit. Default: high.",
    )
    parser.add_argument("--max-tokens", type=int, default=4000, help="Max completion tokens per proof. Default: 4000.")
    parser.add_argument("--sleep", type=float, default=0.0, help="Seconds to sleep between API calls. Default: 0.")
    parser.add_argument("--dry-run", action="store_true", help="Inspect failed/empty entries without API calls or writes.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    shared = load_shared_reverse()

    if not args.proofs_jsonl.exists():
        raise FileNotFoundError(f"HDS proof library not found: {args.proofs_jsonl}")
    if not args.categories.exists():
        raise FileNotFoundError(
            f"HDS category taxonomy not found: {args.categories}\n"
            "Run first:\n"
            "  .venv/bin/python workflows/proof_strategy_extraction/02_pdf_text_extraction/categorize_strategy_library.py --no-resume"
        )

    shared.load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not args.dry_run and (not api_key or api_key == "your-openai-api-key-here"):
        raise RuntimeError("OPENAI_API_KEY is missing or still set to the placeholder. Put a real key in .env or export it.")

    proofs = shared.read_jsonl(args.proofs_jsonl)
    if not proofs:
        raise RuntimeError(f"No proof records found in {args.proofs_jsonl}")
    if args.until_proof <= 0:
        raise ValueError("--until-proof must be positive")
    if args.until_proof > len(proofs):
        raise ValueError(f"--until-proof={args.until_proof} exceeds available proof records: {len(proofs)}")

    categories_text = args.categories.read_text(encoding="utf-8")
    category_names = shared.parse_category_names(categories_text)
    selected = proofs[: args.until_proof]

    pending_indices: List[int] = []
    skipped_no_book_text = 0
    for idx, proof in enumerate(selected):
        if not refinement_is_failed_or_empty(proof):
            continue
        if not has_book_text(proof):
            skipped_no_book_text += 1
            continue
        pending_indices.append(idx)

    print(f"Loaded proofs: {len(proofs)}")
    print(f"Selected proofs: 1..{args.until_proof}")
    print(f"Parsed category names: {len(category_names)}")
    print(f"Failed/empty strategies_refined needing repair: {len(pending_indices)}")
    print(f"Failed/empty but no book text skipped: {skipped_no_book_text}")

    if args.dry_run:
        for idx in pending_indices[:20]:
            proof = proofs[idx]
            value = proof.get("strategies_refined")
            print(
                f"  would repair proof #{idx + 1}: "
                f"{proof.get('lean_name') or proof.get('book_name') or proof.get('official_lean_declaration') or '(unnamed)'}; "
                f"current={value}"
            )
        print("Dry run: no API calls and no file writes.")
        return

    if not pending_indices:
        print("No failed/empty reverse-engineered strategy entries to repair.")
        return

    backup = make_backup(args.proofs_jsonl)
    print(f"Backup written: {backup}")

    reasoning_effort = None if args.reasoning_effort == "none" else args.reasoning_effort

    for done, idx in enumerate(pending_indices, start=1):
        proof = proofs[idx]
        name = proof.get("lean_name") or proof.get("book_name") or proof.get("official_lean_declaration") or "(unnamed)"
        print(f"[{done}/{len(pending_indices)}] Regenerating strategies_refined for proof #{idx + 1}: {name}", flush=True)

        proof_for_prompt = dict(proof)
        proof_for_prompt["textbook_explanation"] = cleaned_hds_textbook_explanation(proof)
        proof_for_prompt["plain_english"] = proof_for_prompt["textbook_explanation"]
        proof_for_prompt["formal_statement"] = hds_formal_context_with_lean_code(proof)

        refined = []
        token_budgets = [args.max_tokens]
        if args.max_tokens < 6000:
            token_budgets.append(6000)

        for attempt, token_budget in enumerate(token_budgets, start=1):
            refined = reverse_engineer_one_proof_tolerant(
                proof=proof_for_prompt,
                categories_text=categories_text,
                category_names=category_names,
                api_key=api_key,
                model=args.model,
                api_base=args.api_base,
                temperature=args.temperature,
                reasoning_effort=reasoning_effort,
                max_tokens=token_budget,
                shared=shared,
            )
            temp_check = dict(proof)
            temp_check["strategies_refined"] = refined
            if not refinement_is_failed_or_empty(temp_check):
                break
            if attempt < len(token_budgets):
                print(
                    f"  Regenerated response was still unparsable/empty with max_tokens={token_budget}; retrying with max_tokens={token_budgets[attempt]}...",
                    flush=True,
                )

        proof["strategies_refined"] = refined
        proof["strategies_refined_model"] = args.model
        proof["strategies_refined_at"] = now_iso()
        proof["strategies_refined_source"] = "repaired_reverse_engineered_from_cleaned_hds_statement_proof"
        if refinement_is_failed_or_empty(proof):
            proof["strategies_refined_repair_status"] = "repair_attempted_but_still_failed"
        else:
            proof["strategies_refined_repair_status"] = "repaired"

        shared.write_jsonl(args.proofs_jsonl, proofs)
        shared.write_json_mirror(args.proofs_json, proofs)

        if args.sleep > 0:
            time.sleep(args.sleep)

    shared.write_jsonl(args.proofs_jsonl, proofs)
    shared.write_json_mirror(args.proofs_json, proofs)
    print(f"Done. Repaired {len(pending_indices)} proof records.")
    print(f"Updated JSONL: {args.proofs_jsonl}")
    print(f"Updated JSON mirror: {args.proofs_json}")


if __name__ == "__main__":
    main()
