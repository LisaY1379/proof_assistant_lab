#!/usr/bin/env python3
"""
Smoke-test OpenAI-compatible API access for gpt-5.6-sol with the proof-agent settings.

Default settings tested:
  model: gpt-5.6-sol
  temperature: 0
  reasoning_effort: high
  max_completion_tokens: 100

Run from project root:

  .venv/bin/python main/test_gpt56_sol_api.py

This script never prints or logs the API key.
"""

from __future__ import annotations

import argparse
import json
import os
import ssl
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, Optional

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = PROJECT_ROOT / ".env"
DEFAULT_API_BASE = "https://api.openai.com/v1"
DEFAULT_MODEL = "gpt-5.6-sol"


def load_dotenv(path: Path = ENV_FILE) -> None:
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


def call_api(
    *,
    api_key: str,
    api_base: str,
    model: str,
    temperature: float,
    reasoning_effort: Optional[str],
    max_completion_tokens: int,
    timeout: int,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": "API smoke test. Reply exactly: API test successful.",
            }
        ],
        "temperature": temperature,
        "max_completion_tokens": max_completion_tokens,
    }
    if reasoning_effort:
        payload["reasoning_effort"] = reasoning_effort

    req = urllib.request.Request(
        api_base.rstrip("/") + "/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    started = time.time()
    with urllib.request.urlopen(req, timeout=timeout, context=make_ssl_context()) as response:
        body = response.read().decode("utf-8")
    elapsed = time.time() - started
    data = json.loads(body)
    return {
        "ok": True,
        "elapsed_seconds": round(elapsed, 3),
        "model": data.get("model", model),
        "finish_reason": data.get("choices", [{}])[0].get("finish_reason"),
        "content": (data.get("choices", [{}])[0].get("message", {}) or {}).get("content", ""),
        "usage": data.get("usage", {}),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Test gpt-5.6-sol API access with proof-agent settings.")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--api-base", default=DEFAULT_API_BASE)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--reasoning-effort", choices=["none", "low", "medium", "high"], default="high")
    parser.add_argument("--max-completion-tokens", type=int, default=100)
    parser.add_argument("--timeout", type=int, default=120)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key or api_key == "your-openai-api-key-here":
        raise SystemExit("OPENAI_API_KEY is missing or still set to the placeholder. Put a real key in .env or export it.")

    reasoning_effort = None if args.reasoning_effort == "none" else args.reasoning_effort
    print("Testing API call with:")
    print(f"  model: {args.model}")
    print(f"  temperature: {args.temperature}")
    print(f"  reasoning_effort: {args.reasoning_effort}")
    print(f"  max_completion_tokens: {args.max_completion_tokens}")
    print("  api_key: [loaded, hidden]")

    try:
        result = call_api(
            api_key=api_key,
            api_base=args.api_base,
            model=args.model,
            temperature=args.temperature,
            reasoning_effort=reasoning_effort,
            max_completion_tokens=args.max_completion_tokens,
            timeout=args.timeout,
        )
    except urllib.error.HTTPError as e:
        error_text = e.read().decode("utf-8", errors="replace")
        print("API test failed with HTTP error:")
        print(f"  status: {e.code}")
        print(error_text)
        return 1
    except Exception as e:
        print("API test failed:")
        print(f"  {type(e).__name__}: {e}")
        return 1

    print("API test succeeded.")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
