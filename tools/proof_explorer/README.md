# Hanson–Wright proof explorer

A standalone, dependency-free interactive proof companion. Open `index.html` in a browser directly, or serve this directory:

```sh
python3 -m http.server 8766 --bind 127.0.0.1 --directory tools/proof_explorer
```

Then visit <http://127.0.0.1:8766>.

## Interaction

- The initial map contains three independent starting facts and one unconnected endpoint.
- The graph is vertical: the progress lane descends from the givens, and the adjacent goal lane decomposes upward from the endpoint. Observations sit between goal checkpoints.
- On desktop, the right half contains a complete, linear textbook-style proof. Its highlighted passage follows playback, manual moves, history navigation, and checkpoint selection, even when the thinking sequence visits passages out of written order. The final connection clip also highlights the estimates as it combines them.
- **Follow animation** controls automatic scrolling inside the proof reader; highlighting stays active when it is unchecked. On small screens the reader stacks below the map.
- **Work backward** chooses the next available goal reduction. **Work forward** chooses the next available deduction. Each checks its prerequisites. The controls explain when another direction is needed.
- **Play thinking order** follows a plausible interleaving of the two directions. It continues the user's existing route; it does not claim to reproduce a historical discovery process.
- Observation nodes precede newly reinterpreted goals. Click any node for the goal, current facts, motivating observation, mathematical verification, and toolkit dependencies.
- The timeline navigates actual moves taken. Moving back and taking a different action forks the route from that point.
- **Watch final connection** reveals the completed proof and replays the MGF connection and closure of the two tail branches.
- Reset view fits the graph width. Vertical scrolling and automatic tracking follow the active checkpoint; **Givens** and **Endpoint** jump to either end. Zoom remains available. On small screens, the map follows the active checkpoint and supports swiping. Playback pauses when the tab is hidden. Reduced-motion preferences are respected.

## Publishing

The public homepage is <https://lisay1379.github.io/proof_assistant_lab/>. GitHub Pages serves `docs/` on `main`.

After editing the explorer, run `python3 tools/proof_explorer/publish.py`, commit the explorer sources and generated `docs/` files, then push to `main`. The script copies only the site's HTML, CSS and JavaScript. The previous homepage remains at `proof-strategy-viewer.html`, linked as **Proof library**.

## Files and checks

- `proof.js`: mathematical content, graph, prerequisites, and pure availability/goal-state functions.
- `written-proof.js`: the linear proof and explicit mappings from thinking moves to written passages.
- `app.js`: browser interaction, playback, and the connection animation.
- `styles.css`: responsive light/dark presentation.
- `test_proof.cjs`: prerequisite and completion checks, including every reachable proof state.

```sh
node --test tools/proof_explorer/test_proof.cjs
```

Mathematical source: `data/observations/observation_02.md`, §1, and the corresponding local book extraction (Theorem 6.2.2, Lemmas 6.2.3–6.2.4, Remark 6.1.2). The diagonal branch is essential. The MGF domain is retained during replacement and optimization. The final prefactor adjustment uses the trivial probability bound 1. This is an explanatory companion, not a formally checked proof system.
