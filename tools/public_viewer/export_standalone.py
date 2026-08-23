#!/usr/bin/env python3
"""
Create a standalone public viewer HTML file with data embedded directly inside it.

Run from the project root:

    python tools/public_viewer/export_public_data.py
    python tools/public_viewer/export_standalone.py

It creates:

    tools/public_viewer/standalone.html

This file does not depend on:

    tools/public_viewer/data/theorem_overview.json
    tools/public_viewer/data/proofs_with_key_strategies.json

Note: MathJax is still loaded from CDN unless index.html is changed to vendor MathJax locally.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
VIEWER_DIR = PROJECT_ROOT / "tools" / "public_viewer"
INDEX_HTML = VIEWER_DIR / "index.html"
OVERVIEW_JSON = VIEWER_DIR / "data" / "theorem_overview.json"
PROOFS_JSON = VIEWER_DIR / "data" / "proofs_with_key_strategies.json"
STANDALONE_HTML = VIEWER_DIR / "standalone.html"


def read_json(path: Path):
    if not path.exists():
        raise FileNotFoundError(
            f"Missing {path}. Run tools/public_viewer/export_public_data.py first."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    html = INDEX_HTML.read_text(encoding="utf-8")
    overview = read_json(OVERVIEW_JSON)
    proofs = read_json(PROOFS_JSON)

    embedded_script = """
    // Embedded public-viewer data. This makes standalone.html independent of data/*.json files.
    const EMBEDDED_THEOREM_OVERVIEW = __OVERVIEW_JSON__;
    const EMBEDDED_PROOFS_WITH_KEY_STRATEGIES = __PROOFS_JSON__;
""".replace(
        "__OVERVIEW_JSON__", json.dumps(overview, ensure_ascii=False)
    ).replace(
        "__PROOFS_JSON__", json.dumps(proofs, ensure_ascii=False)
    )

    html = html.replace("    let allProofs = [];\n    let overviewItems = [];", embedded_script + "\n    let allProofs = [];\n    let overviewItems = [];")

    old_fetch = """    async function fetchJSON(path) {
      const response = await fetch(path, { cache: 'no-store' });
      if (!response.ok) {
        throw new Error(`${path} returned ${response.status} ${response.statusText}`);
      }
      return await response.json();
    }
"""

    new_fetch = """    async function fetchJSON(path) {
      if (path === 'data/theorem_overview.json') {
        return EMBEDDED_THEOREM_OVERVIEW;
      }
      if (path === 'data/proofs_with_key_strategies.json') {
        return EMBEDDED_PROOFS_WITH_KEY_STRATEGIES;
      }
      throw new Error(`No embedded data available for ${path}`);
    }
"""

    if old_fetch not in html:
        raise RuntimeError("Could not find fetchJSON function in index.html; standalone export needs updating.")
    html = html.replace(old_fetch, new_fetch)

    html = html.replace(
        "Data is loaded from static JSON files under <code>data/</code>.",
        "Data is embedded directly in this HTML file.",
    )

    # Make the title clearly distinguishable.
    html = html.replace(
        "<title>Proof Strategy Public Viewer</title>",
        "<title>Proof Strategy Public Viewer — Standalone</title>",
    )
    html = html.replace(
        "<h1>Proof Strategy Public Viewer</h1>",
        "<h1>Proof Strategy Public Viewer<br><span style=\"font-size:12px;color:#9ca3af;\">Standalone read-only version</span></h1>",
    )

    STANDALONE_HTML.write_text(html, encoding="utf-8")
    print(f"Wrote standalone viewer: {STANDALONE_HTML}")
    print(f"Embedded overview items: {len(overview)}")
    print(f"Embedded processed proofs: {len(proofs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
