# Batch Experiments

This workflow compares the proof agent's two modes on a batch of theorem/proof tasks:

1. `control`: direct model response, no library context.
2. `library_rag`: retrieves nodes from `data/general/strategy_hierarchy.json` and conditions the response on the retrieved strategy-library context.

The workflow reuses logic from the interactive interface in:

```text
main/agent_server.py
```

Specifically it reuses:

- `.env` loading,
- OpenAI-compatible API call wrapper,
- strategy hierarchy retrieval,
- prompt construction for control vs Library-RAG.

## Input format

The workflow accepts several JSON formats:

1. JSONL, one task per line.
2. A JSON array of task objects.
3. A single pretty-printed JSON object.
4. The PDF-unit object format produced by the HDS PDF extraction workflow.

Generic task object:

```json
{
  "id": "demo_compactness",
  "dataset": "demo",
  "name": "Compactness proof plan",
  "statement": "Let K be compact and f continuous...",
  "proof_context": "Optional proof/context/Lean code",
  "task": "Explain a proof plan and key strategies."
}
```

PDF-unit format is also accepted directly:

```json
{
  "pdf_unit_id": "hds.pdf.e5c3ce19eb1f",
  "kind": "proposition",
  "name": "Proposition 1.1",
  "statement": "...",
  "proof_text": "...",
  "raw_text": "...",
  "number_key": "proposition_1_1"
}
```

For PDF-unit records, `statement` is used as the theorem statement and `proof_text` is used as proof context.

Example file:

```text
workflows/batch_experiments/theorem_inputs.example.jsonl
```

## Dry run

```bash
.venv/bin/python workflows/batch_experiments/run_control_vs_rag.py \
  --inputs workflows/batch_experiments/theorem_inputs.example.jsonl \
  --dry-run
```

## Run small experiment

```bash
.venv/bin/python workflows/batch_experiments/run_control_vs_rag.py \
  --inputs workflows/batch_experiments/theorem_inputs.example.jsonl \
  --limit 2
```

## Outputs

Each run creates a timestamped directory:

```text
reports/control_vs_rag/run_YYYYMMDD_HHMMSS/
  metadata.json
  inputs.jsonl
  outputs.jsonl
  report.md
  report.html
```

`outputs.jsonl` contains one record per condition per input.

`report.md` and `report.html` compare the control and Library-RAG responses side-by-side for each theorem.

## Suggested settings

Defaults:

```text
model: gpt-5.6-sol
temperature: 1.0
reasoning_effort: high
max_completion_tokens: 4000
```

Override example:

```bash
.venv/bin/python workflows/batch_experiments/run_control_vs_rag.py \
  --inputs workflows/batch_experiments/theorem_inputs.example.jsonl \
  --model gpt-5.6-sol \
  --reasoning-effort high \
  --max-completion-tokens 4000
```

## AI evaluation workflow

After a run finishes, evaluate the control and Library-RAG outputs against the criterion:

```text
elaborate on critical steps, omit trivial steps
```

Dry run:

```bash
.venv/bin/python workflows/batch_experiments/evaluate_control_vs_rag.py \
  --run-dir reports/control_vs_rag/run_YYYYMMDD_HHMMSS \
  --dry-run
```

Run evaluation:

```bash
.venv/bin/python workflows/batch_experiments/evaluate_control_vs_rag.py \
  --run-dir reports/control_vs_rag/run_YYYYMMDD_HHMMSS
```

Outputs:

```text
reports/control_vs_rag/run_YYYYMMDD_HHMMSS/evaluation.jsonl
reports/control_vs_rag/run_YYYYMMDD_HHMMSS/evaluation_report.md
reports/control_vs_rag/run_YYYYMMDD_HHMMSS/evaluation_report.html
```

The evaluator asks the AI judge to highlight:

- where the Library-RAG response worked;
- where the Library-RAG response needs improvement;
- which critical steps should be elaborated;
- which trivial steps should be omitted or compressed;
- comparison notes against the control response.

## Notes

- This is for reproducible experiments, not interactive demos.
- Start with 5–10 theorem inputs before scaling.
- The only experimental difference should be `control` vs `library_rag`.
