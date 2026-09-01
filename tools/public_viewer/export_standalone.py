#!/usr/bin/env python3
"""
Create a standalone public viewer HTML file with all public dataset JSON embedded.

Run from the project root:

    .venv/bin/python tools/public_viewer/export_public_data.py
    .venv/bin/python tools/public_viewer/export_standalone.py

It creates:

    tools/public_viewer/standalone.html

This file does not depend on tools/public_viewer/data/*.json files.
"""

from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
VIEWER_DIR = PROJECT_ROOT / "tools" / "public_viewer"
INDEX_HTML = VIEWER_DIR / "index.html"
DATA_DIR = VIEWER_DIR / "data"
DATASETS_JSON = DATA_DIR / "datasets.json"
STANDALONE_HTML = VIEWER_DIR / "standalone.html"


def read_json(path: Path):
    if not path.exists():
        raise FileNotFoundError(
            f"Missing {path}. Run tools/public_viewer/export_public_data.py first."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    html = INDEX_HTML.read_text(encoding="utf-8")
    manifest = read_json(DATASETS_JSON)
    embedded_data = {"data/datasets.json": manifest}

    for item in manifest.get("datasets", []):
        overview_path = item.get("overview_path")
        proofs_path = item.get("proofs_path")
        if overview_path:
            embedded_data[overview_path] = read_json(VIEWER_DIR / overview_path)
        if proofs_path:
            embedded_data[proofs_path] = read_json(VIEWER_DIR / proofs_path)

    # Legacy aliases for old viewer paths.
    if "data/real_analysis_theorem_overview.json" in embedded_data:
        embedded_data["data/theorem_overview.json"] = embedded_data["data/real_analysis_theorem_overview.json"]
    if "data/real_analysis_proofs_with_key_strategies.json" in embedded_data:
        embedded_data["data/proofs_with_key_strategies.json"] = embedded_data["data/real_analysis_proofs_with_key_strategies.json"]

    embedded_script = """
    // Embedded public-viewer data. This makes standalone.html independent of data/*.json files.
    const EMBEDDED_PUBLIC_DATA = __PUBLIC_DATA_JSON__;
""".replace("__PUBLIC_DATA_JSON__", json.dumps(embedded_data, ensure_ascii=False))

    marker = "    let allProofs = [];\n    let overviewItems = [];\n    let datasetManifest = null;"
    if marker not in html:
        raise RuntimeError("Could not find application data variable marker in index.html; standalone export needs updating.")
    html = html.replace(marker, embedded_script + "\n" + marker)

    old_fetch = """    async function fetchJSON(path) {
      const response = await fetch(path, { cache: 'no-store' });
      if (!response.ok) {
        throw new Error(`${path} returned ${response.status} ${response.statusText}`);
      }
      return await response.json();
    }
"""

    new_fetch = """    async function fetchJSON(path) {
      if (typeof EMBEDDED_PUBLIC_DATA !== 'undefined' && Object.prototype.hasOwnProperty.call(EMBEDDED_PUBLIC_DATA, path)) {
        return EMBEDDED_PUBLIC_DATA[path];
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
    for item in manifest.get("datasets", []):
        print(f"Embedded {item.get('label')}: {item.get('proof_count')} proofs, {item.get('overview_count')} overview items")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
