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

import base64
import datetime as _dt
import json
import os
import re
import secrets
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

# Local default remains 127.0.0.1:8877. For cloud/Hugging Face Docker Space,
# set HOST=0.0.0.0 and PORT=7860 in the environment.
HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "8877"))

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MAIN_DIR = Path(__file__).resolve().parent
INDEX_HTML = MAIN_DIR / "index.html"
ENV_FILE = PROJECT_ROOT / ".env"
GRAPH_PATH = PROJECT_ROOT / "data" / "train" / "general" / "strategy_hierarchy.json"
CHAT_LOG_PATH = PROJECT_ROOT / "data" / "general" / "chat_logs.jsonl"
DEFAULT_MODEL = "gpt-5.6-sol"
DEFAULT_API_BASE = "https://api.openai.com/v1"
DEFAULT_MAX_COMPLETION_TOKENS = 4000
MAX_ALLOWED_COMPLETION_TOKENS = int(os.environ.get("MAX_ALLOWED_COMPLETION_TOKENS", str(DEFAULT_MAX_COMPLETION_TOKENS)))
MIN_ALLOWED_COMPLETION_TOKENS = 100


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


def basic_auth_enabled() -> bool:
    return bool(os.environ.get("PROOF_AGENT_USERNAME") and os.environ.get("PROOF_AGENT_PASSWORD"))


def check_basic_auth(header: Optional[str]) -> bool:
    """Return True if request is authenticated or auth is disabled.

    In local development, Basic Auth is disabled unless both PROOF_AGENT_USERNAME
    and PROOF_AGENT_PASSWORD are set. In cloud deployment, set both variables.
    """
    load_dotenv()
    if not basic_auth_enabled():
        return True
    if not header or not header.startswith("Basic "):
        return False
    try:
        encoded = header.split(" ", 1)[1]
        decoded = base64.b64decode(encoded).decode("utf-8")
        username, password = decoded.split(":", 1)
    except Exception:
        return False
    expected_user = os.environ.get("PROOF_AGENT_USERNAME", "")
    expected_pass = os.environ.get("PROOF_AGENT_PASSWORD", "")
    return secrets.compare_digest(username, expected_user) and secrets.compare_digest(password, expected_pass)


def require_basic_auth(handler: BaseHTTPRequestHandler) -> bool:
    if check_basic_auth(handler.headers.get("Authorization")):
        return True
    body = b"Authentication required.\n"
    handler.send_response(401)
    handler.send_header("WWW-Authenticate", 'Basic realm="Proof Strategy Agent"')
    handler.send_header("Content-Type", "text/plain; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)
    return False


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
            "When a sentence or paragraph uses a strategy from the library, embed the reference directly in the answer immediately after that explanation using this exact block syntax:\n"
            "[STRATEGY: node_id | node label]\nDerived according to this strategy: <one concise explanation of how this strategy supports the preceding reasoning>.\n[/STRATEGY]\n"
            "If the proof needs a method not covered by any retrieved/library node, embed a proposed addition at the relevant point using:\n"
            "[NEW_STRATEGY: proposed strategy label]\nWhy this is new: <concise rationale>.\n[/NEW_STRATEGY]\n"
            "Do not put all referenced strategies in a final list. Do not include a section titled 'Referenced strategy nodes / proposed additions'. "
            "Use inline strategy blocks only where they genuinely support the reasoning. Include a brief 'Reasoning summary' section if useful, but do not expose private chain-of-thought."
        )
        user = (
            f"{library_context}\n\n"
            "USER QUESTION:\n"
            f"{message}\n\n"
            "Answer the user. Use the library context when discussing proof methods. "
            "When using a library strategy, insert an inline [STRATEGY: ...] block immediately after the relevant reasoning. "
            "If no retrieved node fits an essential method, insert an inline [NEW_STRATEGY: ...] block. "
            "Do not end with a separate list of referenced strategies."
        )
        return [{"role": "system", "content": system}, *prior, {"role": "user", "content": user}], selected_nodes

    system = (
        "You are a helpful AI assistant for a proof-assistant research project. "
        "Answer directly and clearly. In this control mode, do not force library citations. "
        "When useful, include a concise high-level reasoning summary, but do not reveal private chain-of-thought."
    )
    return [{"role": "system", "content": system}, *prior, {"role": "user", "content": message}], []


def append_chat_log(record: Dict[str, Any]) -> None:
    """Append one chat event to JSONL. Never log API keys or environment values."""
    CHAT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    safe_record = dict(record)
    # Defensive removal in case a caller accidentally included sensitive fields.
    for key in ["api_key", "OPENAI_API_KEY", "authorization", "headers"]:
        safe_record.pop(key, None)
    with CHAT_LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(safe_record, ensure_ascii=False, sort_keys=True) + "\n")


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
    requested_max_tokens = int(payload.get("max_completion_tokens") or DEFAULT_MAX_COMPLETION_TOKENS)
    max_tokens = max(
        MIN_ALLOWED_COMPLETION_TOKENS,
        min(requested_max_tokens, MAX_ALLOWED_COMPLETION_TOKENS),
    )
    temperature = float(payload["temperature"]) if "temperature" in payload and payload.get("temperature") is not None else 1.0
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
    created_at = now_iso()
    result = {
        "ok": True,
        "mode": mode,
        "model": model,
        "created_at": created_at,
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
    append_chat_log(
        {
            "created_at": created_at,
            "status": "success",
            "mode": mode,
            "model": model,
            "reasoning_effort": reasoning_effort_raw,
            "requested_max_completion_tokens": requested_max_tokens,
            "max_completion_tokens": max_tokens,
            "tokens_were_clamped": requested_max_tokens != max_tokens,
            "temperature": temperature,
            "message": message,
            "answer": answer,
            "retrieved_nodes": result["retrieved_nodes"],
            "steps": result["steps"],
        }
    )
    return result


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
        if not require_basic_auth(self):
            return
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
        if not require_basic_auth(self):
            return
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
            try:
                append_chat_log(
                    {
                        "created_at": now_iso(),
                        "status": "error",
                        "error": str(exc),
                        "traceback": traceback.format_exc(),
                    }
                )
            except Exception:
                pass
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
