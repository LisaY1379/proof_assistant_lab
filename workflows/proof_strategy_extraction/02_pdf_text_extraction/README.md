# 02 PDF Text Extraction: HighDimensionalStatistics

This workflow builds an initial framework library for the HighDimensionalStatistics dataset by aligning:

1. ATLAS Lean declarations under `external/atlas-lean/Atlas/HighDimensionalStatistics/code/`
2. ATLAS natural-language target metadata in `targets.yaml`
3. Natural-language theorem/proof text extracted from the original textbook PDF

## Main output

```text
data/high_dimensional_statistics/processed/proofs_with_key_strategies.jsonl
```

For this workflow, each record contains the Lean-side context plus separate book-side statement/proof fields:

```json
{
  "comment": "Lean doc comment before the theorem or lemma",
  "lean_original_code": "Original Lean declaration/proof block",
  "plain_english_statement": "Corresponding original statement/description from the book, if aligned",
  "plain_english_proof": "Corresponding original proof text from the book, if aligned"
}
```

The review UI displays `plain_english_statement` and `plain_english_proof` together in the same English column, separated by a horizontal line.

After running the optional cleanup workflow, records may also contain:

```json
{
  "plain_english_statement_cleaned": "Cleaned Markdown + LaTeX statement",
  "plain_english_proof_cleaned": "Cleaned Markdown + LaTeX proof"
}
```

The raw PDF-extracted fields are preserved.

## Expected PDF location

Place the original book PDF at one of these locations:

```text
external/atlas-original/HighDimensionalStatistics/original.pdf
external/atlas-original/HighDimensionalStatistics.pdf
```

Recommended:

```text
external/atlas-original/HighDimensionalStatistics/original.pdf
```

If the PDF is copyrighted, do not commit it to GitHub. Add `external/atlas-original/` and raw PDF paths to `.gitignore`.

You may also pass a PDF path manually:

```bash
.venv/bin/python workflows/proof_strategy_extraction/02_pdf_text_extraction/build_hds_library.py --pdf /path/to/book.pdf
```

## Run

Dry run:

```bash
.venv/bin/python workflows/proof_strategy_extraction/02_pdf_text_extraction/build_hds_library.py --dry-run
```

Build the library:

```bash
.venv/bin/python workflows/proof_strategy_extraction/02_pdf_text_extraction/build_hds_library.py
```

If you want to build the Lean/code framework before the PDF text is available:

```bash
.venv/bin/python workflows/proof_strategy_extraction/02_pdf_text_extraction/build_hds_library.py --allow-empty-pdf
```

## Cleanup workflow: Markdown + LaTeX normalization

Raw PDF extraction often loses math formatting. To clean the extracted book statement/proof text into readable Markdown + LaTeX, run:

```bash
.venv/bin/python workflows/proof_strategy_extraction/02_pdf_text_extraction/clean_hds_pdf_text.py --until 5
```

This adds two fields to each processed record:

```text
plain_english_statement_cleaned
plain_english_proof_cleaned
```

The workflow preserves the raw fields:

```text
plain_english_statement
plain_english_proof
```

Dry run:

```bash
.venv/bin/python workflows/proof_strategy_extraction/02_pdf_text_extraction/clean_hds_pdf_text.py --until 5 --dry-run
```

Run through the full dataset:

```bash
.venv/bin/python workflows/proof_strategy_extraction/02_pdf_text_extraction/clean_hds_pdf_text.py
```

The script deduplicates identical raw statement/proof texts and caches cleaned results at:

```text
data/high_dimensional_statistics/processed/pdf_text_cleaning_cache.json
```

So multiple Lean declarations aligned to the same textbook theorem/proof do not require duplicate LLM cleanup calls.

## Key-strategy extraction workflow: book proof only

After the PDF-aligned library exists, you can run a focused workflow that keeps only Step 4 from the Lean pipeline:

```text
For each full proof, call the API to identify the key proof strategies / key ideas that make the proof work.
```

Run:

```bash
.venv/bin/python workflows/proof_strategy_extraction/02_pdf_text_extraction/extract_hds_key_strategies.py --until 10
```

This workflow does **not** translate Lean code back to English. It reads the book-side statement/proof fields:

```text
plain_english_statement_cleaned / plain_english_statement
plain_english_proof_cleaned / plain_english_proof
```

and writes plain enumerated key-strategy text into each record, matching the original Lean workflow's Step 4 behavior:

```json
"key_strategies": "1. One sentence stating the key idea.\n2. Another key idea."
```

No JSON parsing is performed in this workflow. If structured strategy objects are needed later, run a separate refinement script after this step.

Dry run:

```bash
.venv/bin/python workflows/proof_strategy_extraction/02_pdf_text_extraction/extract_hds_key_strategies.py --until 3 --dry-run
```

By default it resumes and skips records that already have `key_strategies`. Use `--no-resume` only if you intentionally want to regenerate them.

## Alignment logic v0.1

The workflow aligns Lean declarations with book proof text using this bridge:

```text
Lean declaration/file/comment
    ↔ ATLAS targets.yaml name/location/description
    ↔ PDF theorem/proof unit
```

Primary matching signal:

```text
Theorem/Lemma/Proposition/Corollary number, e.g. Theorem 1.9
```

Fallback matching signal:

```text
simple token-overlap similarity between statements/comments/descriptions
```

The alignment report is written to:

```text
data/high_dimensional_statistics/metadata/hds_pdf_lean_alignment_report.json
data/high_dimensional_statistics/metadata/hds_pdf_lean_alignment_report.md
```

## Notes

- PDF extraction uses `pdftotext` if available.
- If no PDF is available, use `--allow-empty-pdf`; then `plain_english_statement` may fall back to ATLAS target descriptions and `plain_english_proof` will be empty.
- This is an initial simple workflow and should be inspected before being used at scale.
