# Reusable proof explorer

Run the main agent server and open `/explorer` (normally
<http://127.0.0.1:8877/explorer>). The main chat page links to it. Paste a theorem
and proof, select a step budget, and generate. Plain text and LaTeX are supported;
PDF extraction is outside this interface. The initial prototype accepts 40,000
characters and up to 16 grouped proof steps.

The renderer reuses the Hanson–Wright typography, colors, graph/reader layout,
three reading editions, selected-step highlighting, and expanded reading dialog.
Its mathematical content is theorem-neutral. The existing curated explorer is
preserved. `example.json` adapts its 14 ablations, including Ziemann attribution,
to the same portable format used by AI output. Opening it makes no model calls.
Rebuild it with `python3 tools/proof_explorer/export_portable_explorer.py`.

## Generation and evidence

1. A bounded model call decomposes the supplied proof into facts, goals,
   observations, and ordered actions. Exact source quotes anchor explanations;
   unquoted material is retained. Original proof text is never rewritten.
2. Python validates references, prerequisites, introduced nodes and goal changes,
   then derives the proof graph and successive have/want states from those actions.
   Structural validation does **not** certify mathematical implications.
3. For each action, optional Responses API `web_search` researches replacement
   strategies using the [Responses API web-search tool](https://developers.openai.com/api/docs/guides/tools-web-search).
   A separate model call writes the global strategy ban, replacement
   arguments, outcomes, and qualitative costs. Each branch starts at the original
   assumptions; earlier states are not silently assumed under the ban. Future
   checkpoint rejoins require an explicit argument and a valid checkpoint ID.
4. A final model call chooses conceptually critical steps. The original edition
   shows the supplied text; the full edition adds all explanations/ablations;
   the key-step edition expands selected steps and uses concise versions elsewhere.
   This is an editorial selection, not empirical difficulty measurement.

Online alternatives must name source IDs obtained from web-tool metadata, not
URLs invented in prose. The server rejects literature-assisted claims without
retrieved source IDs and forces that label whenever sources are attached. Sources,
adaptation notes, and research history remain in the JSON export and reading view.
A proposal made with retrieved literature available but no specific attribution
is marked as literature-exposed; it is never treated as independent discovery.
Search unavailable/disabled/not performed are distinct from a completed search.
Source presence validates provenance records, not that a paper proves the claim.
Imported source history is explicitly labeled as supplied and unverified.

A worked alternative is a **model-assessed** proof, not a formal certificate.
Unresolved, failed, and budget-exhausted outcomes cannot claim a successful rejoin.
No inferred infinite search difficulty or fabricated trial counts are displayed.
Red full-explanation sections mean no worked replacement was established in that
step's reviewed alternatives. Unreviewed steps remain neutral.

## Configuration and storage

The main server loads the existing project `.env`. `OPENAI_API_KEY` is kept on the
server; the selected model is used for structured calls. Optional settings:

- `PROOF_EXPLORER_SEARCH_MODEL`: override only the web-research model; it must
  support Responses API `web_search`.
- `OPENAI_API_BASE`: trusted server-side API base, default `https://api.openai.com/v1`.
- `PROOF_EXPLORER_MAX_TOKENS`: structured-call budget, default 12,000, bounded to
  4,000–20,000. This is separate from the main chat's 4,000-token budget.

With N steps, generation makes N+2 structured calls and up to N web-research
requests (6,000 output tokens each). These API calls incur usage charges. A failed
web request is recorded as unavailable; an invalid structured result stops the
run rather than displaying invented fallback mathematics. Each stage allows at most one additional structured call to correct malformed
output or invalid references. A second validation failure stops the run; there
are no unbounded retry loops. Stage progress reflects actual completion, not elapsed timers.
Stop takes effect between requests; an in-flight request may finish first.

Jobs and partial documents are saved atomically under ignored
`data/proof_explorers/`. Reload reconnects using `?run=<id>`; after a server restart,
unfinished jobs are marked interrupted and their completed material is retained.
**Continue unfinished work** resumes a stopped, failed, or interrupted run,
skipping accepted ablations and reusing saved research. It may make additional
API calls for the unfinished stages.
These records contain supplied proofs and generated research. They are not copied
into the public Pages build. The existing server authentication also protects the
explorer routes. Export saves a portable document; import revalidates it and
rebuilds graph/state data instead of trusting supplied layouts or closure flags.

## Portable document contract (schema_version: 1)

`example.json` is a complete working example. Required fields are:

- `schema_version`, `title`, `statement`, `original_proof`.
- `nodes`: objects with a unique simple `id`, `kind` (`fact`, `goal`, or
  `observation`), and mathematical `text`.
- `initial_facts`, `initial_goals`: node IDs.
- `steps`: ordered `a1`, `a2`, … actions. Each has `title`, a verbatim `quote`,
  `uses` (existing facts), `adds` (new facts), `opens` (new goals), `closes`
  (currently open goals), and `observations` (new observation IDs). Optional `motivated_by` names the
  specific active or newly opened goals that motivate those observations.
  Each also supplies `justification`, `observation`, `explanation`, `difficulty`,
  and `short_version` as text. Source offsets are derived from quotes.
- `ablations`: optional mapping from action ID to `{restriction, alternatives,
  research}`. Each alternative supplies `title`, `origin`, `source_ids`,
  `adaptation`, `route` (title/have/want steps), `argument`, `outcome`,
  `rejoin_state`, `assessment`, and `cost`. Origins: `model_proposed` or
  `literature_assisted`. Outcomes: `closed`, `rejoined`, `failed`, `unresolved`,
  `budget_exceeded`. Only `rejoined` takes a checkpoint such as `s3`.
  Research contains `status`, `sources` (id/title/url), `summary`, and tool `calls`.
  Optional `research_records` preserves completed research when an ablation is still
  pending or its analysis failed.
- `critical`: optional `{steps: [action IDs], rationale}`.

`states`, `proof_edges`, `closure`, source offsets and alternative IDs are derived.
A graph node's action is the action that **produced it**, not the following action.
All untrusted mathematical text is rendered as text; source links accept only
HTTP(S). MathJax supplies math layout with its safe extension; plain text remains
available when its CDN cannot be loaded.

Endpoints: `POST /api/explorers` starts generation; `GET /api/explorers/<id>`
retrieves progress; `POST /api/explorers/<id>/stop` requests a stop;
`POST /api/explorers/<id>/resume` continues unfinished work;
`POST /api/explorers/import` validates a portable document. The UI and pipeline
are independent: another producer can generate this format without generating UI
code or knowing anything about Hanson–Wright.

## Verification

`python3 -m unittest discover -s tests -p 'test_explorer.py'`

`node --test tests/test_explorer_view.cjs`

Tests use injected model responses and captured-shaped search metadata; they do
not use API credentials or spend money. They check graph references, shared closure,
exact source preservation (including Unicode), source attribution, invalid rejoin
rejection, interruption, persistence, all 14 portable Hanson–Wright ablations,
and the asynchronous generation flow.

A live smoke run with the supplied proof that the sum of two even integers is
even completed with four actions, five states, all four ablations, and a final
critical-step selection. Retrieved references appeared as linked,
literature-assisted alternatives. The run also exercised recovery after a
malformed remaining-goal field, and its completed explorer survived a server
restart. Browser checks covered both graphs, branch inspection/restoration, red
unresolved highlighting, the three editions, and the expanded reader.

## Protocol-based decomposition

New generations load the actual formal reference from
`tools/proof_explorer/protocol-reference.html` and the priority rule from
`tools/proof_explorer/protocol.html` into the decomposition instructions. The
exact supplied text, version, and SHA-256 fingerprint are saved in the document.
The Docker image includes both files; missing protocol content stops generation.

A required `protocol.context` declares domains, definitions, basic rules, and
named toolkit results with hypotheses. Each grouped step has a `protocol` record:
current context and target, basic progress, remaining gap, a structured motivating
observation, ordered atomic actions, logical relation, side conditions, and
remaining obligations. Atomic actions classify B-D/B-C/B-L execution separately
from strategic choice; later verification actions explicitly reference choices.
Toolkit calls name declared results and record their hypothesis checks.
The maximum-step setting limits groups, so it does not suppress these substeps.

Missing records, invalid classifications/dependencies, unchecked choices, and
inconsistent goal-relation labels trigger the existing single correction attempt.
This validates annotation structure, not mathematical truth or whether the model's
classification is justified. Unresolved reasoning cannot add established facts or
close goals. Scoped assumptions must remain inside conditional/quantified statements,
not enter the global fact list unconditionally.

The selected-step inspector and expanded written editions expose protocol records.
The generation record shows the declared context and supplied protocol text.
Existing saved explorers remain readable and resumable without being retroactively
labeled protocol-checked; generate anew to obtain the new decomposition. Imported
protocol provenance remains a supplied record, not independently authenticated.
