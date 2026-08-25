#!/usr/bin/env python3
"""Local review UI server for proof strategy extraction.

Run from the project root:

    python tools/review_ui/server.py

Then open:

    http://127.0.0.1:8765

This server intentionally binds to localhost only. It provides:
- workflow control: run the proof strategy extraction pipeline with --limit N
- inspection: read data/processed/proofs_with_key_strategies.jsonl and display it
"""

from __future__ import annotations

import datetime as _dt
import importlib.util
import json
import os
import subprocess
import sys
import threading
import traceback
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, List, Optional


HOST = "127.0.0.1"
PORT = 8765

PROJECT_ROOT = Path(__file__).resolve().parents[2]
UI_DIR = Path(__file__).resolve().parent
PIPELINE_SCRIPT = PROJECT_ROOT / "workflows" / "proof_strategy_extraction" / "run_pipeline.py"
CLASSIFY_SCRIPT = PROJECT_ROOT / "workflows" / "proof_strategy_extraction" / "classify_strategy_categories.py"
RESULTS_FILE = PROJECT_ROOT / "data" / "processed" / "proofs_with_key_strategies.jsonl"
ATLAS_DIR = PROJECT_ROOT / "external" / "atlas-lean" / "Atlas" / "RealAnalysis"
ATLAS_REPO_ROOT = PROJECT_ROOT / "external" / "atlas-lean"
ENV_FILE = PROJECT_ROOT / ".env"


job_lock = threading.Lock()
current_job: Dict[str, Any] = {
    "running": False,
    "started_at": None,
    "finished_at": None,
    "workflow": None,
    "limit": None,
    "returncode": None,
    "stdout": "",
    "stderr": "",
    "error": None,
}


def now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat()


def load_dotenv() -> Dict[str, str]:
    """Load simple KEY=VALUE pairs from project .env without external packages."""
    values: Dict[str, str] = {}
    if not ENV_FILE.exists():
        return values

    for raw_line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            values[key] = value
    return values


def load_pipeline_module() -> Any:
    """Import run_pipeline.py so the UI can reuse its extraction logic."""
    spec = importlib.util.spec_from_file_location("proof_strategy_run_pipeline", PIPELINE_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not import pipeline script: {PIPELINE_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_overview() -> Dict[str, Any]:
    """Enumerate all theorem/lemma proof records and mark processed ones."""
    if not ATLAS_DIR.exists():
        return {
            "error": f"ATLAS RealAnalysis directory does not exist: {ATLAS_DIR.relative_to(PROJECT_ROOT)}",
            "items": [],
            "total": 0,
            "processed_count": 0,
            "next_unprocessed_index": None,
        }

    pipeline = load_pipeline_module()
    proofs = pipeline.extract_proofs(
        atlas_dir=ATLAS_DIR,
        atlas_repo_root=ATLAS_REPO_ROOT,
        limit=None,
    )
    # Match pipeline main filtering: keep records with a detected proof body and at least one step.
    proofs = [
        p for p in proofs
        if p.get("has_detected_proof") and pipeline.split_proof_into_steps(p.get("proof_code", ""))
    ]

    processed_records = parse_pretty_json_records(RESULTS_FILE)
    processed_by_id = {r.get("proof_id"): r for r in processed_records if r.get("proof_id")}
    processed_ids = set(processed_by_id)

    items: List[Dict[str, Any]] = []
    next_unprocessed_index: Optional[int] = None
    for i, proof in enumerate(proofs, start=1):
        processed = proof.get("proof_id") in processed_ids
        processed_record = processed_by_id.get(proof.get("proof_id"), {})
        strategy_items = processed_record.get("key_strategies") if isinstance(processed_record, dict) else None
        strategy_count = 0
        categorized_count = 0
        if isinstance(strategy_items, list):
            for strategy_item in strategy_items:
                if isinstance(strategy_item, dict):
                    strategy_count += 1
                    if str(strategy_item.get("category", "")).strip():
                        categorized_count += 1
        category_processed = bool(strategy_count and categorized_count == strategy_count)
        if not processed and next_unprocessed_index is None:
            next_unprocessed_index = i
        comment = proof.get("comment", "") or ""
        comment_excerpt = " ".join(comment.split())
        if len(comment_excerpt) > 180:
            comment_excerpt = comment_excerpt[:177] + "..."
        items.append({
            "index": i,
            "proof_id": proof.get("proof_id"),
            "lean_name": proof.get("lean_name"),
            "kind": proof.get("kind"),
            "source_file": str(proof.get("source_file", "")),
            "start_line": proof.get("start_line"),
            "end_line": proof.get("end_line"),
            "comment_excerpt": comment_excerpt,
            "processed": processed,
            "strategy_count": strategy_count,
            "categorized_strategy_count": categorized_count,
            "category_processed": category_processed,
        })

    return {
        "items": items,
        "total": len(items),
        "processed_count": sum(1 for item in items if item["processed"]),
        "category_processed_count": sum(1 for item in items if item.get("category_processed")),
        "next_unprocessed_index": next_unprocessed_index,
        "results_file": str(RESULTS_FILE.relative_to(PROJECT_ROOT)),
        "atlas_dir": str(ATLAS_DIR.relative_to(PROJECT_ROOT)),
    }


def parse_pretty_json_records(path: Path) -> List[Dict[str, Any]]:
    """Read compact JSONL or pretty-printed multi-line JSON records."""
    if not path.exists():
        return []

    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []

    # First try compact JSONL, one JSON object per line.
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

    # Then parse pretty-printed records by balanced braces.
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


def append_job_stdout(text: str, max_chars: int = 200_000) -> None:
    """Append streaming output to current_job while keeping memory bounded."""
    with job_lock:
        current = str(current_job.get("stdout") or "") + text
        if len(current) > max_chars:
            current = "...[older logs truncated]...\n" + current[-max_chars:]
        current_job["stdout"] = current


def start_streaming_job(*, workflow: str, limit: int, cmd: List[str]) -> None:
    """Start a subprocess and stream combined stdout/stderr into /api/status."""
    def worker() -> None:
        with job_lock:
            current_job.update(
                {
                    "running": True,
                    "workflow": workflow,
                    "started_at": now_iso(),
                    "finished_at": None,
                    "limit": limit,
                    "returncode": None,
                    "stdout": f"Running command: {' '.join(cmd)}\n\n",
                    "stderr": "",
                    "error": None,
                }
            )

        try:
            env = os.environ.copy()
            # .env should override stale shell variables for the server process.
            env.update(load_dotenv())
            env["PYTHONUNBUFFERED"] = "1"

            proc = subprocess.Popen(
                cmd,
                cwd=str(PROJECT_ROOT),
                env=env,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=1,
            )

            assert proc.stdout is not None
            for line in proc.stdout:
                append_job_stdout(line)
            returncode = proc.wait()

            with job_lock:
                current_job.update(
                    {
                        "running": False,
                        "finished_at": now_iso(),
                        "returncode": returncode,
                    }
                )
        except Exception as exc:  # noqa: BLE001 - local UI should report full errors.
            with job_lock:
                current_job.update(
                    {
                        "running": False,
                        "finished_at": now_iso(),
                        "returncode": None,
                        "error": f"{exc}\n\n{traceback.format_exc()}",
                    }
                )

    thread = threading.Thread(target=worker, daemon=True)
    thread.start()


def start_pipeline_job(limit: int) -> None:
    """Start pipeline in a background thread.

    `limit` means: process/resume all proof items from the beginning through this
    enumerated item number. Existing final records are reused by the pipeline, so
    this effectively continues from where previous work stopped.
    """
    cmd = [sys.executable, "-u", str(PIPELINE_SCRIPT), "--limit", str(limit)]
    start_streaming_job(workflow="textbook_key_strategy", limit=limit, cmd=cmd)


def start_classification_job(until_proof: int) -> None:
    """Classify strategy-object categories through proof item number N."""
    cmd = [sys.executable, "-u", str(CLASSIFY_SCRIPT), "--until-proof", str(until_proof)]
    start_streaming_job(workflow="strategy_category_classification", limit=until_proof, cmd=cmd)


class Handler(BaseHTTPRequestHandler):
    server_version = "ProofStrategyReviewUI/0.1"

    def log_message(self, fmt: str, *args: Any) -> None:
        # Keep server logs compact.
        sys.stderr.write("[%s] %s\n" % (self.log_date_time_string(), fmt % args))

    def send_json(self, data: Any, status: int = 200) -> None:
        payload = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def send_text(self, text: str, status: int = 200, content_type: str = "text/plain; charset=utf-8") -> None:
        payload = text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API.
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path in {"/", "/index.html"}:
            index_path = UI_DIR / "index.html"
            self.send_text(index_path.read_text(encoding="utf-8"), content_type="text/html; charset=utf-8")
            return

        if path == "/api/status":
            with job_lock:
                data = dict(current_job)
            self.send_json(data)
            return

        if path == "/api/overview":
            try:
                overview = make_overview()
                status = 500 if overview.get("error") else 200
                self.send_json(overview, status=status)
            except Exception as exc:  # noqa: BLE001
                self.send_json({"error": str(exc), "traceback": traceback.format_exc()}, status=500)
            return

        if path == "/api/proofs":
            try:
                proofs = parse_pretty_json_records(RESULTS_FILE)
                self.send_json(
                    {
                        "path": str(RESULTS_FILE.relative_to(PROJECT_ROOT)),
                        "count": len(proofs),
                        "proofs": proofs,
                    }
                )
            except Exception as exc:  # noqa: BLE001
                self.send_json({"error": str(exc), "traceback": traceback.format_exc()}, status=500)
            return

        self.send_json({"error": f"Not found: {path}"}, status=404)

    def do_POST(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API.
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length).decode("utf-8") if length else "{}"
        try:
            payload = json.loads(body or "{}")
        except json.JSONDecodeError:
            self.send_json({"error": "Invalid JSON request body."}, status=400)
            return

        if path in {"/api/run", "/api/classify-strategies"}:
            with job_lock:
                if current_job.get("running"):
                    self.send_json({"error": "A workflow job is already running.", "job": dict(current_job)}, status=409)
                    return

            raw_limit = payload.get("limit")
            try:
                limit = int(raw_limit)
            except Exception:
                self.send_json({"error": "limit must be an integer."}, status=400)
                return

            if limit <= 0:
                self.send_json({"error": "limit must be positive."}, status=400)
                return
            if limit > 10000:
                self.send_json({"error": "limit is too large for the local UI safety check."}, status=400)
                return

            if path == "/api/run":
                if not PIPELINE_SCRIPT.exists():
                    self.send_json({"error": f"Pipeline script not found: {PIPELINE_SCRIPT}"}, status=500)
                    return
                start_pipeline_job(limit)
                self.send_json({"ok": True, "message": f"Started pipeline to process through item #{limit} (--limit {limit})"})
                return

            if not CLASSIFY_SCRIPT.exists():
                self.send_json({"error": f"Classification script not found: {CLASSIFY_SCRIPT}"}, status=500)
                return
            start_classification_job(limit)
            self.send_json({"ok": True, "message": f"Started strategy-category classification through proof item #{limit}"})
            return

        self.send_json({"error": f"Not found: {path}"}, status=404)


def main() -> None:
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Pipeline:     {PIPELINE_SCRIPT.relative_to(PROJECT_ROOT)}")
    print(f"Classifier:   {CLASSIFY_SCRIPT.relative_to(PROJECT_ROOT)}")
    print(f"Results:      {RESULTS_FILE.relative_to(PROJECT_ROOT)}")
    print(f"Atlas:        {ATLAS_DIR.relative_to(PROJECT_ROOT)}")
    print(f"Open:         http://{HOST}:{PORT}")
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
