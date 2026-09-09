#!/usr/bin/env python3
"""
Local two-mode AI interface for proof-strategy work.

Run from project root:

    .venv/bin/python main/agent_server.py

Open:

    http://127.0.0.1:8877

Modes:
  1. control: direct GPT chat.
  2. library_rag: retrieves strategy nodes from data/general/strategy_hierarchy.json
     and requires the model to cite used strategy nodes at the end, or propose new
     strategies if none fit.

This server is local-only and uses only Python stdlib.
"""

from __future__ import annotations

import datetime as _dt
import json
import os
import re
import ssl
import sys
import time
import traceback
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

HOST = "127.0.0.1"
PORT = 8877

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MAIN_DIR = Path(__file__).resolve().parent
INDEX_HTML = MAIN_DIR / "index.html"
ENV_FILE = PROJECT_ROOT / ".env"
GRAPH_PATH = PROJECT_ROOT / "data" / "general" / "strategy_hierarchy.json"
DEFAULT_MODEL = "gpt-5.6-sol"
DEFAULT_API_BASE = "https://api.openai.com/v1"


def now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat()


def load_dotenv(path: Path = ENV_FILE) -> None:
    """Load simple KEY=VALUE entries. Project .env overrides stale shell values."""
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
    messages: List[Dict[str, str]],
    api_base: str = DEFAULT_API_BASE,
    temperature: float = 1.0,
    max_completion_tokens: int = 1800,
    reasoning_effort: Optional[str] = "high",
    timeout: int = 180,
    max_retries: int = 3,
) -> str:
    url = api_base.rstrip("/") + "/chat/completions"
    payload: Dict[str, Any] = {
        "model": model,
        "messages": messages,
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
            return str(data["choices"][0]["message"]["content"] or "").strip()
        except urllib.error.HTTPError as e:
            error_text = e.read().decode("utf-8", errors="replace")
            if e.code in {429, 500, 502, 503, 504} and attempt < max_retries:
                last_error = RuntimeError(f"OpenAI HTTP {e.code}: {error_text}")
                time.sleep(2.0 * attempt)
                continue
            raise RuntimeError(f"OpenAI API HTTP error {e.code}: {error_text}") from e
        except Exception as e:
            last_error = e
            if attempt < max_retries:
                time.sleep(2.0 * attempt)
                continue
            raise RuntimeError(f"OpenAI API call failed after {max_retries} attempts: {last_error}") from e

    raise RuntimeError(f"OpenAI API call failed: {last_error}")


def load_graph() -> Dict[str, Any]:
    if not GRAPH_PATH.exists():
        raise FileNotFoundError(
            f"Strategy hierarchy graph not found: {GRAPH_PATH.relative_to(PROJECT_ROOT)}. "
            "Run workflows/library_hierarchy/build_strategy_hierarchy.py first."
        )
    graph = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    if not isinstance(graph, dict):
        raise ValueError("strategy_hierarchy.json must be a JSON object")
    return graph


def tokenize(text: str) -> set[str]:
    stop = {
        "the", "and", "for", "with", "from", "that", "this", "into", "proof",
        "show", "prove", "using", "method", "strategy", "strategies", "then",
        "than", "where", "when", "which", "what", "does", "have", "has",
    }
    return {
        t.lower()
        for t in re.findall(r"[A-Za-z][A-Za-z0-9_\-]*", text or "")
        if len(t) > 2 and t.lower() not in stop
    }


def node_text(node: Dict[str, Any]) -> str:
    srcs = node.get("source_categories", [])
    src_text = ""
    if isinstance(srcs, list):
        src_text = " ".join(
            " ".join(str(src.get(k, "")) for k in ["dataset", "id", "name"])
            for src in srcs
            if isinstance(src, dict)
        )
    return "\n".join(
        [
            str(node.get("id", "")),
            str(node.get("label", "")),
            str(node.get("description", "")),
            src_text,
        ]
    )


def score_node(query_tokens: set[str], node: Dict[str, Any]) -> float:
    text = node_text(node)
    ntoks = tokenize(text)
    if not query_tokens or not ntoks:
        return 0.0
    overlap = query_tokens & ntoks
    score = len(overlap) / max(1, len(query_tokens))
    label = str(node.get("label", "")).lower()
    q = " ".join(query_tokens).lower()
    for token in query_tokens:
        if token in label:
            score += 0.15
    # Boost common proof-search themes.
    theme_boosts = [
        ("compact", ["compactness"]),
        ("continuity", ["continuity", "metric", "filter"]),
        ("integral", ["integral", "integration"]),
        ("derivative", ["derivative", "differential", "calculus"]),
        ("series", ["series", "convergence"]),
        ("probability", ["concentration", "tail", "probabilistic"]),
        ("tail", ["concentration", "tail", "moment"]),
        ("supremum", ["supremum", "extremal"]),
        ("epsilon", ["epsilon", "metric", "filter"]),
    ]
    text_lower = text.lower()
    for qtok, related in theme_boosts:
        if qtok in query_tokens and any(r in text_lower for r in related):
            score += 0.2
    return score


def retrieve_library_context(question: str, *, max_nodes: int = 10, min_score: float = 0.08) -> Tuple[str, List[Dict[str, Any]]]:
    graph = load_graph()
    nodes = [n for n in graph.get("nodes", []) if isinstance(n, dict)]
    edges = [e for e in graph.get("edges", []) if isinstance(e, dict)]
    node_by_id = {str(n.get("id")): n for n in nodes if n.get("id")}
    query_tokens = tokenize(question)

    scored = sorted(
        ((score_node(query_tokens, node), node) for node in nodes),
        key=lambda x: x[0],
        reverse=True,
    )
    selected_ids: List[str] = []
    # Only keep nodes with real lexical/theme overlap. The previous version kept
    # the top several nodes even when all scores were zero, which looked random.
    for score, node in scored:
        if score < min_score:
            continue
        nid = str(node.get("id"))
        if nid and nid not in selected_ids:
            selected_ids.append(nid)
        if len(selected_ids) >= max_nodes:
            break

    # Include direct parents/children of the strongest matches if room remains.
    top_ids = selected_ids[:5]
    if selected_ids:
        for edge in edges:
            src = str(edge.get("source", ""))
            tgt = str(edge.get("target", ""))
            if src in top_ids and tgt in node_by_id and tgt not in selected_ids:
                selected_ids.append(tgt)
            if tgt in top_ids and src in node_by_id and src not in selected_ids:
                selected_ids.append(src)
            if len(selected_ids) >= max_nodes:
                break

    selected_nodes = [node_by_id[nid] for nid in selected_ids if nid in node_by_id]
    selected_set = set(selected_ids)
    selected_edges = [
        e for e in edges
        if str(e.get("source")) in selected_set and str(e.get("target")) in selected_set
    ]

    lines = [
        "STRATEGY HIERARCHY CONTEXT",
        f"Source graph: {GRAPH_PATH.relative_to(PROJECT_ROOT)}",
        "",
    ]
    if not selected_nodes:
        lines.extend([
            "No strategy nodes had enough lexical overlap with the question.",
            "The answer may propose a new strategy if no listed library strategy fits.",
        ])
        return "\n".join(lines), []

    lines.append("Relevant nodes:")
    for node in selected_nodes:
        srcs = node.get("source_categories", [])
        src_summary = []
        if isinstance(srcs, list):
            for src in srcs[:5]:
                if isinstance(src, dict):
                    src_summary.append(f"{src.get('dataset')}:{src.get('id')} {src.get('name')}")
        lines.append(
            f"- node_id: {node.get('id')}\n"
            f"  label: {node.get('label')}\n"
            f"  level: {node.get('level')}\n"
            f"  description: {node.get('description')}\n"
            f"  source_categories: {'; '.join(src_summary)}"
        )
    lines.append("")
    lines.append("Relations among retrieved nodes:")
    for edge in selected_edges[:30]:
        lines.append(
            f"- {edge.get('source')} --{edge.get('relation', 'related_to')}--> {edge.get('target')}: "
            f"{edge.get('rationale', '')}"
        )
    return "\n".join(lines), selected_nodes


def trim_history(history: Any, max_messages: int = 8) -> List[Dict[str, str]]:
    if not isinstance(history, list):
        return []
    cleaned: List[Dict[str, str]] = []
    for item in history[-max_messages:]:
        if not isinstance(item, dict):
            continue
        role = item.get("role")
        content = str(item.get("content", ""))
        if role in {"user", "assistant"} and content.strip():
            cleaned.append({"role": role, "content": content[-6000:]})
    return cleaned


def build_messages(mode: str, message: str, history: Any) -> Tuple[List[Dict[str, str]], List[Dict[str, Any]]]:
    prior = trim_history(history)
    if mode == "library_rag":
        library_context, selected_nodes = retrieve_library_context(message)
        system = (
            "You are a proof-assistant research agent. The user may ask you to explain a proof, "
            "complete a proof, suggest a proof plan, debug a formalization, or identify methods. "
            "You must use the provided strategy hierarchy library as methodological grounding. "
            "When you use or mention a method, connect it to one or more strategy nodes from the library. "
            "If the proof needs a method not covered by the retrieved nodes, propose a new strategy explicitly. "
            "Include a brief section titled 'Reasoning summary' that summarizes the high-level steps you took, "
            "without exposing private chain-of-thought. Then at the end of every answer, include a section exactly titled "
            "'Referenced strategy nodes / proposed additions'. In that section list: (1) node id, label, and how it was used; "
            "and/or (2) proposed new strategy with rationale. Do not claim that a node was used unless it genuinely supports the reasoning."
        )
        user = (
            f"{library_context}\n\n"
            "USER QUESTION:\n"
            f"{message}\n\n"
            "Answer the user. Use the library context when discussing proof methods. "
            "Include a concise 'Reasoning summary' section with high-level reasoning steps only. "
            "End with 'Referenced strategy nodes / proposed additions'."
        )
        return [{"role": "system", "content": system}, *prior, {"role": "user", "content": user}], selected_nodes

    system = (
        "You are a helpful AI assistant for a proof-assistant research project. "
        "Answer directly and clearly. In this control mode, do not force library citations. "
        "When useful, include a concise high-level reasoning summary, but do not reveal private chain-of-thought."
    )
    return [{"role": "system", "content": system}, *prior, {"role": "user", "content": message}], []


def handle_chat(payload: Dict[str, Any]) -> Dict[str, Any]:
    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key or api_key == "your-openai-api-key-here":
        raise RuntimeError("OPENAI_API_KEY is missing or still set to the placeholder in .env.")

    message = str(payload.get("message", "")).strip()
    if not message:
        raise ValueError("message is required")
    mode = str(payload.get("mode", "control")).strip() or "control"
    if mode not in {"control", "library_rag"}:
        raise ValueError("mode must be 'control' or 'library_rag'")

    model = str(payload.get("model") or DEFAULT_MODEL).strip()
    api_base = str(payload.get("api_base") or DEFAULT_API_BASE).strip()
    max_tokens = int(payload.get("max_completion_tokens") or 4000)
    temperature = float(payload.get("temperature") or 1.0)
    reasoning_effort_raw = payload.get("reasoning_effort", "high")
    reasoning_effort = None if reasoning_effort_raw in {None, "", "none"} else str(reasoning_effort_raw)

    messages, selected_nodes = build_messages(mode, message, payload.get("history", []))
    answer = call_openai_chat(
        api_key=api_key,
        model=model,
        messages=messages,
        api_base=api_base,
        temperature=temperature,
        max_completion_tokens=max_tokens,
        reasoning_effort=reasoning_effort,
    )
    if not answer.strip():
        # Reasoning models can spend the whole token budget internally and return
        # empty visible content. Retry once with a larger visible budget; if it is
        # still empty, surface an explicit error rather than showing a blank reply.
        retry_tokens = max(max_tokens * 2, 6000)
        answer = call_openai_chat(
            api_key=api_key,
            model=model,
            messages=messages,
            api_base=api_base,
            temperature=temperature,
            max_completion_tokens=retry_tokens,
            reasoning_effort=reasoning_effort,
        )
    if not answer.strip():
        raise RuntimeError(
            "The model returned an empty visible response after retry. Try increasing max tokens, lowering reasoning effort, or switching models."
        )
    return {
        "ok": True,
        "mode": mode,
        "model": model,
        "created_at": now_iso(),
        "answer": answer,
        "steps": [
            "read_library" if mode == "library_rag" else "control_prompt",
            "model_reasoning",
            "response_complete",
        ],
        "retrieved_nodes": [
            {
                "id": n.get("id"),
                "label": n.get("label"),
                "level": n.get("level"),
                "description": n.get("description"),
            }
            for n in selected_nodes
        ],
    }


class Handler(BaseHTTPRequestHandler):
    server_version = "ProofAssistantMainUI/0.1"

    def log_message(self, fmt: str, *args: Any) -> None:
        sys.stderr.write("[%s] %s\n" % (self.log_date_time_string(), fmt % args))

    def send_json(self, data: Any, status: int = 200) -> None:
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_text(self, text: str, content_type: str = "text/html; charset=utf-8", status: int = 200) -> None:
        body = text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path in {"/", "/index.html"}:
            self.send_text(INDEX_HTML.read_text(encoding="utf-8"))
            return
        if parsed.path == "/api/status":
            graph_exists = GRAPH_PATH.exists()
            self.send_json(
                {
                    "ok": True,
                    "model_default": DEFAULT_MODEL,
                    "graph_path": str(GRAPH_PATH.relative_to(PROJECT_ROOT)),
                    "graph_exists": graph_exists,
                    "api_key_loaded": bool(os.environ.get("OPENAI_API_KEY") or (ENV_FILE.exists() and "OPENAI_API_KEY" in ENV_FILE.read_text(encoding="utf-8"))),
                }
            )
            return
        self.send_json({"error": f"Not found: {parsed.path}"}, status=404)

    def do_POST(self) -> None:  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path != "/api/chat":
            self.send_json({"error": f"Not found: {parsed.path}"}, status=404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length).decode("utf-8") if length else "{}"
            payload = json.loads(body or "{}")
            result = handle_chat(payload)
            self.send_json(result)
        except Exception as exc:  # noqa: BLE001
            self.send_json(
                {
                    "ok": False,
                    "error": str(exc),
                    "traceback": traceback.format_exc(),
                },
                status=500,
            )


def main() -> int:
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Graph:        {GRAPH_PATH.relative_to(PROJECT_ROOT)} ({'exists' if GRAPH_PATH.exists() else 'missing'})")
    print(f"Open:         http://{HOST}:{PORT}")
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
