# ETH paper explorer

Static reading companion for OpenAI’s *The Exponential Time Hypothesis is False*, October 25, 2026 version (67 pages).

- Proposition 3.4: the shared-summary counting and interpolation engine.
- Proposition 6.4: exact fixed-width SAT counting via sparse checks and disjoint sparsification.
- The sharper Theorem 1.1/Appendix D result is distinguished on the overview and dependency map; its tensor-contraction proof is not expanded here.

Each explorer contains 12 source-linked moves, a proof graph, a state graph, three written editions, and alternative checks. Toolkit lemmas are named dependencies. Key steps are editorial selections. Alternatives are mathematical comparisons with provenance, not recorded search executions or measured LLM trials.

`paper-data.json` holds the arguments. `paper-model.js` validates state transitions. `examples.js` implements the four-variable SAT and shared-summary examples. `paper.js` renders and animates the interface. `paper.pdf` pins the supplied source version for page links.

Run `node --test tests/test_eth_explorer.cjs` from the repository root. For a standalone static preview, run `python3 -m http.server 8883 --directory docs` and open `/papers/eth/`.

The published copy is `docs/papers/eth/`. Copy this directory there when updating, then change the theme stylesheet path in its index.html from `../../explorer-theme.css` to `../../proof-explorer/explorer-theme.css`. No credentials or backend are required.
