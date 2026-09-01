# Proof Strategy Extraction Workflow

This workflow extracts proof strategies from the ATLAS RealAnalysis Lean files and turns them into a structured strategy database for use in the proof-assistant/agent pipeline.

The goal is not only to record Lean tactics, but also to identify the underlying mathematical methods used in each proof, such as contradiction, epsilon-delta reasoning, case splitting, algebraic manipulation, monotonicity, limit algebra, compactness-style arguments, and other key proof tricks.

## Big Picture

```text
external/atlas-lean/Atlas/RealAnalysis/
        ↓
proof strategy extraction workflow
        ↓
data/processed/real_analysis_proofs.jsonl
        ↓
data/processed/real_analysis_proof_steps.jsonl
        ↓
data/annotations/auto_strategy_labels.jsonl
        ↓
data/annotations/human_reviewed_strategy_labels.jsonl
        ↓
data/processed/proof_strategy_index.json
        ↓
agent retrieval / proof explanation / evaluation
```

## Recommended Location

This workflow should live inside the current research project rather than becoming a separate repository for now.

Recommended structure:

```text
proof_assistant_lab/
  external/
    atlas-lean/                    # ignored raw ATLAS repo

  data/
    metadata/
      atlas_real_analysis_source.json
    processed/
      real_analysis_proofs.jsonl
      real_analysis_proof_steps.jsonl
      proof_strategy_index.json
    annotations/
      auto_strategy_labels.jsonl
      human_reviewed_strategy_labels.jsonl

  workflows/
    proof_strategy_extraction/
      README.md
      config.yaml
      strategy_taxonomy.yaml
      extract_proofs.py
      segment_proofs.py
      classify_strategies.py
      review_annotations.py
      build_strategy_index.py
      run_pipeline.py

  src/
    atlas/
    strategies/
    retrieval/
    agent/
    evaluation/
```

## Why Keep This Workflow Inside This Project?

Proof-strategy extraction is central to the research goal. It forms the bridge between raw formal proofs and the logical backbone used by the agent.

The intended pipeline is:

```text
ATLAS raw Lean proofs
        ↓
proof strategy extraction
        ↓
proof strategy database
        ↓
agent retrieval and explanation system
        ↓
evaluation
```

It should become a separate repository only later if it becomes a reusable standalone tool.

Possible future standalone project names:

```text
lean-proof-strategy-extractor
proof-strategy-miner
atlas-strategy-miner
```

## Stage 1: Collect Lean Proof Units

### Input

```text
external/atlas-lean/Atlas/RealAnalysis/
```

Important source files may include:

```text
external/atlas-lean/Atlas/RealAnalysis/RealAnalysis.lean
external/atlas-lean/Atlas/RealAnalysis/code/*.lean
external/atlas-lean/Atlas/RealAnalysis/targets.yaml
external/atlas-lean/Atlas/RealAnalysis/report.json
```

### Output

```text
data/processed/real_analysis_proofs.jsonl
```

Each record should represent one theorem/proof unit.

Example schema:

```json
{
  "id": "atlas.real_analysis.some_theorem",
  "source": "atlas-lean",
  "source_file": "Atlas/RealAnalysis/code/Chapter1.lean",
  "lean_name": "some_theorem",
  "formal_statement": "...",
  "proof_code": "...",
  "imports": ["Mathlib..."],
  "status": "proved",
  "atlas_commit": "..."
}
```

### Notes

At this stage, the goal is only to extract proof objects faithfully. Do not yet classify strategies.

Recommended script:

```text
workflows/proof_strategy_extraction/extract_proofs.py
```

## Stage 2: Segment Proofs Into Steps

### Input

```text
data/processed/real_analysis_proofs.jsonl
```

### Output

```text
data/processed/real_analysis_proof_steps.jsonl
```

Example schema:

```json
{
  "proof_id": "atlas.real_analysis.some_theorem",
  "lean_name": "some_theorem",
  "steps": [
    {
      "step_id": 1,
      "lean_code": "by_contra h",
      "rough_meaning": "Assume the negation for contradiction."
    },
    {
      "step_id": 2,
      "lean_code": "obtain ⟨ε, hε, hbad⟩ := ...",
      "rough_meaning": "Extract a witness from the negated statement."
    }
  ]
}
```

### Notes

Segmentation can begin with simple heuristics:

- split around major Lean commands,
- identify `have`, `suffices`, `obtain`, `rcases`, `by_contra`, `apply`, `exact`, `rw`, `simp`, etc.,
- keep original Lean code as evidence.

Recommended script:

```text
workflows/proof_strategy_extraction/segment_proofs.py
```

## Stage 3: Identify Proof Strategies

This stage maps Lean/tactic-level patterns to mathematical proof strategies.

### Input

```text
data/processed/real_analysis_proof_steps.jsonl
```

### Output

```text
data/annotations/auto_strategy_labels.jsonl
```

Example schema:

```json
{
  "proof_id": "atlas.real_analysis.some_theorem",
  "lean_name": "some_theorem",
  "tactic_patterns": [
    "by_contra",
    "obtain",
    "linarith"
  ],
  "mathematical_strategies": [
    {
      "label": "contradiction",
      "evidence": "by_contra h",
      "confidence": 0.98
    },
    {
      "label": "epsilon_delta",
      "evidence": "unfold Metric.tendsto_nhds at h",
      "confidence": 0.74
    },
    {
      "label": "inequality_manipulation",
      "evidence": "linarith",
      "confidence": 0.70
    }
  ],
  "key_trick": "Negate the convergence statement to obtain a fixed epsilon witness, then derive a contradiction using the limit hypothesis."
}
```

### Important Distinction

Keep two levels separate:

#### 1. Lean/tactic-level pattern

Examples:

```text
by_contra
constructor
intro
cases
rcases
induction
rw
simp
linarith
norm_num
exact
apply
have
obtain
```

These are visible directly in Lean code.

#### 2. Mathematical proof strategy

Examples:

```text
proof by contradiction
epsilon-delta argument
case split
induction
squeeze argument
compactness/subsequence argument
monotonicity argument
algebraic rearrangement
inequality manipulation
limit algebra
reduce to known theorem
construct explicit witness
use order completeness
```

These are the ideas your research project mainly cares about.

The mapping is not one-to-one. For example:

```lean
by_contra h
```

is strong evidence for contradiction, while:

```lean
simp
linarith
```

may correspond mathematically to algebraic or inequality manipulation.

Recommended script:

```text
workflows/proof_strategy_extraction/classify_strategies.py
```

## Stage 4: Human or LLM Review

Some strategy labels can be detected automatically, but the most important part — the key mathematical trick — may require review.

### Input

```text
data/annotations/auto_strategy_labels.jsonl
```

### Output

```text
data/annotations/human_reviewed_strategy_labels.jsonl
```

Recommended schema:

```json
{
  "proof_id": "atlas.real_analysis.some_theorem",
  "lean_name": "some_theorem",
  "auto_labels": ["contradiction", "epsilon_delta"],
  "reviewed_labels": ["contradiction", "epsilon_delta", "inequality_manipulation"],
  "key_trick": "...",
  "review_status": "reviewed",
  "reviewer_notes": "The proof depends on negating the limit definition and extracting a bad epsilon."
}
```

### Notes

Do not overwrite automatic labels. Keep automatic and reviewed annotations separate.

This allows later evaluation of:

- automatic classification quality,
- human agreement,
- usefulness for agent retrieval,
- whether strategy labels improve proof explanations.

Recommended script:

```text
workflows/proof_strategy_extraction/review_annotations.py
```

## Stage 5: Build a Searchable Strategy Index

This stage creates the database used by the agent.

### Input

```text
data/annotations/human_reviewed_strategy_labels.jsonl
```

or, if no reviewed labels are available yet:

```text
data/annotations/auto_strategy_labels.jsonl
```

### Output

```text
data/processed/proof_strategy_index.json
```

Example index:

```json
{
  "epsilon_delta": [
    {
      "proof_id": "atlas.real_analysis.limit_unique",
      "lean_name": "limit_unique",
      "statement": "...",
      "key_trick": "Unfold the epsilon-delta definition and choose a small enough neighborhood.",
      "source_file": "Atlas/RealAnalysis/code/Chapter1.lean",
      "dependencies": []
    }
  ],
  "contradiction": [
    {
      "proof_id": "atlas.real_analysis.some_theorem",
      "lean_name": "some_theorem",
      "statement": "...",
      "key_trick": "Assume the negation and derive an impossible inequality."
    }
  ]
}
```

Recommended script:

```text
workflows/proof_strategy_extraction/build_strategy_index.py
```

## Stage 6: Use the Strategy Index in the Agent

Once the strategy index exists, it can be used by the agent for:

- retrieving similar proof patterns,
- generating more understandable proof explanations,
- suggesting likely proof strategies for new theorem statements,
- connecting Lean proof steps to human-readable mathematical reasoning,
- evaluating whether a formal logical backbone improves explanation quality.

Example retrieval query:

```text
Find real analysis proofs that use epsilon-delta reasoning and contradiction.
```

The agent should retrieve entries from:

```text
data/processed/proof_strategy_index.json
```

rather than scanning all raw Lean files each time.

## Suggested Strategy Taxonomy

Create a file:

```text
workflows/proof_strategy_extraction/strategy_taxonomy.yaml
```

Initial taxonomy example:

```yaml
strategies:
  contradiction:
    description: "Assume the negation and derive a contradiction."
    lean_signals:
      - "by_contra"
      - "contradiction"
      - "exfalso"

  epsilon_delta:
    description: "Use epsilon-delta or neighborhood-based reasoning for limits, continuity, or convergence."
    lean_signals:
      - "Metric.tendsto_nhds"
      - "dist"
      - "∀ ε > 0"
      - "eventually"
      - "nhds"

  case_split:
    description: "Divide the proof into cases."
    lean_signals:
      - "by_cases"
      - "cases"
      - "rcases"

  induction:
    description: "Prove the result by induction."
    lean_signals:
      - "induction"
      - "Nat.rec"

  inequality_manipulation:
    description: "Prove the result by rearranging or solving inequalities."
    lean_signals:
      - "linarith"
      - "nlinarith"
      - "positivity"
      - "ring_nf"

  limit_algebra:
    description: "Use algebraic closure rules for limits or convergence."
    lean_signals:
      - "tendsto_add"
      - "tendsto_mul"
      - "tendsto_sub"
      - "tendsto_inv"

  rewrite_simplification:
    description: "Transform the goal using rewriting and simplification."
    lean_signals:
      - "rw"
      - "simp"
      - "simpa"
      - "simp_all"

  witness_construction:
    description: "Construct an explicit object or witness satisfying an existential statement."
    lean_signals:
      - "use"
      - "exists"
      - "refine ⟨"
```

## Suggested Pipeline Runner

Create:

```text
workflows/proof_strategy_extraction/run_pipeline.py
```

The eventual pipeline could run:

```text
1. extract_proofs.py
2. segment_proofs.py
3. classify_strategies.py
4. review_annotations.py, optional/manual
5. build_strategy_index.py
```

Example command:

```bash
python workflows/proof_strategy_extraction/run_pipeline.py \
  --input external/atlas-lean/Atlas/RealAnalysis \
  --output data/processed/proof_strategy_index.json
```

## Versioning and Reproducibility

Always record:

- ATLAS source URL,
- ATLAS commit hash,
- Lean version from `lean-toolchain`,
- Mathlib/dependency versions from `lake-manifest.json`,
- extraction script version,
- strategy taxonomy version,
- whether labels are automatic or human-reviewed.

Suggested metadata file:

```text
data/metadata/atlas_real_analysis_source.json
```

Example:

```json
{
  "source": "https://github.com/facebookresearch/atlas-lean",
  "subset": "Atlas/RealAnalysis",
  "local_path": "external/atlas-lean/Atlas/RealAnalysis",
  "clone_method": "git sparse-checkout",
  "commit": "PUT_COMMIT_HASH_HERE",
  "lean_toolchain_file": "external/atlas-lean/lean-toolchain",
  "lake_manifest_file": "external/atlas-lean/lake-manifest.json"
}
```

## When to Split This Into a Separate Repository

Keep this workflow inside `proof_assistant_lab` for now.

Split it into a separate repository only if:

1. The extractor becomes useful independently of this project.
2. It supports multiple Lean datasets beyond ATLAS RealAnalysis.
3. It has a stable CLI and documentation.
4. Other researchers/users need to install it separately.
5. It develops its own tests, releases, and issue tracker.

Until then, keeping it inside this project makes iteration easier.

## Immediate TODO

- [ ] Create `strategy_taxonomy.yaml`.
- [ ] Create `extract_proofs.py`.
- [ ] Extract theorem/proof units from `../../../external/atlas-lean/Atlas/RealAnalysis`.
- [ ] Save extracted proofs to `data/processed/real_analysis_proofs.jsonl`.
- [ ] Create `segment_proofs.py`.
- [ ] Save proof steps to `data/processed/real_analysis_proof_steps.jsonl`.
- [ ] Create `classify_strategies.py`.
- [ ] Save automatic labels to `data/annotations/auto_strategy_labels.jsonl`.
- [ ] Design a lightweight human/LLM review process.
- [ ] Save reviewed labels to `data/annotations/human_reviewed_strategy_labels.jsonl`.
- [ ] Build `data/processed/proof_strategy_index.json`.
- [ ] Connect the strategy index to the agent/retrieval system.
