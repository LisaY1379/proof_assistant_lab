# Proof Strategy Review UI

A lightweight local UI for the proof strategy extraction workflow.

## Features

Left sidebar:

1. **Workflow control**
   - Enter a number for `--limit`.
   - Click **Start Workflow** to run:

   ```bash
   python workflows/proof_strategy_extraction/run_pipeline.py --limit N
   ```

2. **Inspection**
   - Click **Load Proof Spreadsheet** to read:

   ```text
   data/processed/proofs_with_key_strategies.jsonl
   ```

   and display a spreadsheet with three columns:

   - Lean original code
   - English translation
   - Key strategies

## Run

From the project root:

```bash
python tools/review_ui/server.py
```

Then open:

```text
http://127.0.0.1:8765
```

If you want to make sure the same virtual environment is used:

```bash
.venv/bin/python tools/review_ui/server.py
```

## API key behavior

The server loads `.env` from the project root and uses it when starting the pipeline.
This means the project-local `.env` should override an old shell API key for workflow runs started from the UI.

Expected `.env` format:

```bash
OPENAI_API_KEY=your-active-key-here
```

Do not commit `.env`.
