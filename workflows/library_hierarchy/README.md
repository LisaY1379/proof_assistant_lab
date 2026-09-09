# Library Hierarchy Workflow

This workflow builds a graph-like hierarchical strategy library from the two dataset-level category taxonomies:

```text
data/real_analysis/processed/strategy_categories.txt
data/high_dimensional_statistics/processed/strategy_categories.txt
```

It asks `gpt-5.6-sol` to discover broader/narrower relations across the two libraries. The key idea is that the two taxonomies may have different granularity: for example, RealAnalysis may split calculus/integration methods into many fine-grained categories, while HighDimensionalStatistics may group them under broader strategy families.

## Script

```text
workflows/library_hierarchy/build_strategy_hierarchy.py
```

## Outputs

```text
data/general/strategy_hierarchy.json
data/general/strategy_hierarchy.md
data/general/strategy_hierarchy_raw.txt
```

The JSON output is intended to represent a graph, with:

```json
{
  "nodes": [...],
  "edges": [...],
  "unmapped_source_categories": [...]
}
```

Each node should preserve provenance via source category IDs such as:

```text
real_analysis_24
high_dimensional_statistics_11
```

## Dry run

```bash
.venv/bin/python workflows/library_hierarchy/build_strategy_hierarchy.py --dry-run
```

## Run

```bash
.venv/bin/python workflows/library_hierarchy/build_strategy_hierarchy.py
```

## Model defaults

```text
model: gpt-5.6-sol
temperature: 1.0
reasoning_effort: omitted by default
max_completion_tokens: 12000
```

If the model/API requires a reasoning parameter, use for example:

```bash
.venv/bin/python workflows/library_hierarchy/build_strategy_hierarchy.py --reasoning-effort high
```

If JSON parsing fails but you still want to save a placeholder JSON plus raw output:

```bash
.venv/bin/python workflows/library_hierarchy/build_strategy_hierarchy.py --no-parse
```

## Visualize the hierarchy graph

After `data/general/strategy_hierarchy.json` exists, generate a standalone HTML graph and Mermaid graph:

```bash
.venv/bin/python workflows/library_hierarchy/visualize_strategy_hierarchy.py
```

Outputs:

```text
data/general/strategy_hierarchy_graph.html
data/general/strategy_hierarchy_graph.mmd
```

Open the HTML file in a browser, or paste the `.mmd` file into a Mermaid-compatible viewer.
