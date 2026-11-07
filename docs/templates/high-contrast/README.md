# High-contrast paper introduction template

[Open the template](https://lisay1379.github.io/proof_assistant_lab/templates/high-contrast/) · [Full explorer](https://lisay1379.github.io/proof_assistant_lab/papers/high-contrast/)

A static, reusable version of the high-contrast explorer, with its hero, material averaging interaction, expandable introduction, proof-strategy overview, source-linked formal definitions, assumptions and local dictionary. It excludes the dependency map, theorem proof/state graphs, written-proof editions and AI assistant.

## Run

From this folder, run `python3 -m http.server 8882`, then visit `http://localhost:8882`. No build step, backend or API key is required. MathJax and the Inter font load from public CDNs. Navigation to the full explorer assumes the repository's published directory layout; update that link if copying this folder elsewhere.

## Adapt to another paper

Copy this entire directory. All local assets are included.

- `index.html`: replace title, authors, source links, physical question, findings, earlier-work comparison, strategies, definitions and assumptions. Keep intuition before notation. The introduction starts open and remains collapsible. There are no theorem routes or graph data files to populate.
- `material.js`: replace the deterministic block-averaging illustration with a visualization suited to the new paper. The caption describes exactly what the displayed colors represent.
- `dictionary-data.js`: replace the term definitions, contextual questions and source-page references. `dictionary.js` provides hover/selection annotations and the sidebar without an AI service.
- `theme.css`: typography, title sizes and purple theme. `paper.css` retains the original explorer's styling; `template.css` contains the template-specific adjustments.
- `intro-math.js`: renders LaTeX in the introduction and reveals collapsed content when followed by a section link. Write inline math as `\( ... \)` and displayed math as `\[ ... \]` inside `.formal-math` containers, which protect formulas from dictionary annotation.

## Mathematical sources

Armstrong, Kuusi and Loher, *Homogenization at a polynomial scale in high contrast*, arXiv:2609.27647v1. Strategies follow §1.3 (pp.8–10), with supporting results in §§2–6. Definitions follow (1.2), (1.5)–(1.9), and (2.1)–(2.3). P1–P3 are in §1.1. The barred variational blocks are distinct from the pointwise symmetric and skew parts of the coefficient field. The statement refers to the original variational definition in [AK25]; this template does not replace that definition with an arithmetic conductivity average.
