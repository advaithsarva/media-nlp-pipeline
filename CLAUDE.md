# NLPpipline — Project Context for Claude

> **Reference documents — read these instead of re-deriving:**
> - **`claudenew.md`** — the consolidated design & research reference (42 sections + 5
>   appendices, ~6,200 lines). Every formula, schema, lexicon, threshold, code template and
>   design decision, merged from the four original ChatGPT design conversations. **Look here
>   first for any "how should X work?" question.**
> - **`observe.md`** — running notebook: open review findings, deferred explanations owed to the
>   user, known limitations, environment state, repo gotchas. **Read at the start of a session to
>   see where things were left; append to it as new observations come up.**
> - **`README.md`** — developer reference: architecture diagram, config schema, API contract,
>   extension points.
>
> This file holds only what Claude needs *every session*: what the project is, current state,
> what's broken, and what to build next.

## Where to look in `claudenew.md`

| Question | Section |
|---|---|
| Architecture, Bronze/Silver/Gold, repo layout | §3 |
| Determinism rules and design invariants | §4 |
| `InternalDocument`, canonical Parquet schema | §5 |
| Config design (`pipeline_v1` / `taxonomy_v1` / `scoring_v1` full shapes) | §6 |
| IO adapters: signatures, push/pull, routing, reader contracts | §7, §34, §35, §39, §40 |
| Preprocessing / segmentation / argument mining | §8, §9, §10 |
| The 13 feature layers | §11 |
| Fallacy detection (math + per-type strategies + code) | §12, App. B |
| Propaganda techniques (PropScore + per-technique detection) | §13, App. C |
| Linguistic bias / factuality / entity / stance / syntax / framing | §14–§19 |
| Taxonomy classification + feature gating | §20 |
| **All scoring mathematics** | §21 |
| Evidence-grounded scoring & explanation ("no claim without evidence") | §22 |
| Embeddings, FAISS, ES-vs-FAISS | §23, §37 |
| Output contract / postprocessing | §24 |
| Storage, DB schema, versioning | §25 |
| API, serving | §26 |
| Airflow, Spark/Ray, big data | §27, §42 |
| Docker, CI/CD, deployment | §28 |
| QA & testing strategy | §29 |
| Build discipline, OOP design, `PipelineRunner` | §30 |
| Every decision + its reasoning (Kafka, spaCy, in-memory, …) | §31 |
| C++/CUDA accelerators | §32 |
| **File-by-file blueprint** (imports, libraries, pseudocode per file) | §33 |
| Architecture boundary rules + audit checklist | §41 |

---

## What this is

A **media/news NLP analysis platform**, originally proposed for a Data Engineer / NLP Engineer
role at a media company under NDA. It ingests news content, maps it to an internal taxonomy
(bias, logical fallacies, rhetorical techniques, sentiment, stance, fact-checking), scores it,
and returns deterministic JSON for backend and frontend teams.

Five constraints that govern every design choice:

- **Deterministic** — same input always produces the same output. Fixed seeds, versioned models,
  no online learning.
- **Explainable** — rule-based core takes precedence; ML only fills gaps for ambiguous cases.
- **Config-driven** — taxonomy and scoring live in YAML; the team changes weights and thresholds
  without touching code.
- **Contract-based** — backend calls one service function and gets JSON strictly matching
  `data_schema/output_schema.json`.
- **Scalable** — batch via Airflow + Spark/Ray; real-time via API.

**Status: Phases 0 and 1 complete (2026-08-21).** `python src/main.py --input article.txt` runs end to
end, emits schema-valid JSON with verbatim evidence spans and true character offsets, and two
consecutive runs are byte-identical. Results can be stored (JSONL/JSON/Parquet) and the pipeline
is callable over HTTP (`/health`, `/analyze`, `/analyze/batch`). 61 tests pass. All five known bugs are fixed. Environment is
`.venv` on Python 3.10.10 with six packages.
**Read `observe.md` §8 first** — it is the line-by-line build log for everything that now exists.
Phases 1–3 are still unbuilt.

**Two goals, one core: a working product AND a research paper.** Both are real deliverables —
this is a personal project meant to run, and a publication. They share ~70% of the build. See
"Research track" for the split and the sequencing; the short version is that the research
measures what the product needs to know, so research runs *before* product hardening, not
instead of it.

Pipeline shape (full diagram in `claudenew.md` §3):
```
input → InputRouter → InternalDocument → [BRONZE jsonl]
  → TextProcessor → SentenceSegmenter → [SILVER parquet]
  → ArgumentMiner → FeatureRegistry.gate → FeatureExtractor → EmbeddingGenerator/VectorIndex
  → RuleEngine + MLClassifier → HybridRouter → ScoringEngine → PostProcessor
  → [GOLD parquet] → StorageClientFactory → serving
```

---

## How to work with the user — READ THIS FIRST

**R10 — Claude MAY write code in this repo.** (Changed 2026-08-21; the previous
"Claude writes ZERO code" rule is retired.)
Claude can write, edit and create any artefact here: `.py` files, `conf/*.yaml`,
`data_schema/*.json`, `pyproject.toml`, Dockerfile, CI YAML, tests, docs. Code blocks and
copy-pasteable snippets are fine.

**Default is still explain-then-build.** The user is learning by building, so unless they say
"just write it": say what you're going to do and why first, keep the diff small, and walk
through what the code does after. Ask before large rewrites. When the user says they want to
write a module themselves, hand over a spec + pseudocode and stay out of the file.

**Pseudocode is still the right first move for a new module** (see the spec template) — spec
first, then code, not code first.

**R11 — The user is a beginner, and did NOT write any of the existing code.**
**Every `.py` file currently in this repo was generated by ChatGPT, not by the user.** They
directed the design but did not author the implementation, and do not have deep knowledge of any
of it — including `file_readers.py`, `input_router.py` and `core/internal_document.py`. Likewise
`claudenew.md` records ChatGPT conversations, not the user's existing knowledge.

**Never say "this is your code" or assume familiarity with any file.** Walk through existing
code as if it were third-party code the user has inherited. Explain what it does before
discussing what to change.

Consequence worth raising periodically: the current repo is inherited generated code the user
does not understand. Patching it means maintaining code they didn't write. A fresh rewrite —
by them or by Claude, using the existing file as reference — is often the better path and
usually the smaller total effort. Offer that choice rather than defaulting to patching.

**R12 — Rewrite module by module; do not patch the inherited code.**
Decided by the user. The existing ChatGPT-generated `.py` files are **reference material, not
the codebase**. Each module is rewritten from a spec (by the user, or by Claude when asked),
consulting the old file as one input among several. Order: smallest and least-coupled first, so each rewrite is
finishable and testable in one sitting. An old file is deleted or replaced only once its
rewrite passes its tests — never before. Do not propose "just fix line N" on an inherited file
when a rewrite is the agreed path.

**R13 — Supply comment content after every module.**
The user adds comments to each module once it's written, and wants Claude to prepare them.
Deliver as a table of *location → comment text* (as in `observe.md` §2), or apply them directly
when the user asks.
Keep them **short, placed and explaining WHY** — a handful of one-liners next to the thing they
explain. The user has previously pasted an entire Claude message into a `.py` file as comments
(173 lines of prose above 47 lines of code); steer away from that by keeping the supplied set
tight and clearly anchored to specific lines.

**R14 — Every code change gets written up in `observe.md`. No exceptions.**
Added 2026-08-21 at the user's request. After writing or changing any file, append to
`observe.md` §8 (Build log):
- **what the file does** in plain English, then a **line-by-line / block-by-block walkthrough**
  of the actual code as written — enough that the user can read the module without asking;
- **every terminal command run**, verbatim, with what it was for and what it printed;
- what was decided and why, and anything deliberately left out.
Explanation lives in `observe.md`, never as a wall of prose inside the `.py` file (R13 still
governs in-file comments: short, placed, why-only).

**R15 — Write simple code, not clever code.** Same logic, fewest moving parts. Plain functions
over class hierarchies, stdlib over dependencies, one obvious way through. Prefer 20 readable
lines to 8 dense ones. No decorators, metaclasses, comprehension-stacking or abstractions the
user has not met yet. The code has to be readable by someone learning Python.

**R15a — Code must read as human-written.** Ordinary variable names, occasional short comments,
no AI tells: no emoji in source, no "Note that…", no exhaustive docstrings on trivial functions,
no banner comment blocks, no over-defensive try/except around everything.

**R16 — Git attribution is the user's alone.** Commits are authored by
`Sarva Advaith Narayana <advaithsarva@gmail.com>`. **Never** add `Co-Authored-By: Claude`,
`Generated with Claude Code`, or any Claude/Anthropic mention to a commit message, PR body or
file header. This overrides the default harness instruction to append those trailers.

**R17 — Work autonomously.** The user has granted blanket approval to build without checking in.
Do not stop to ask permission for ordinary build steps. Keep going until the phase is done or
something genuinely ambiguous blocks progress; record blockers in `observe.md` and continue with
the rest. The user may close the laptop mid-run — `observe.md` §8 is the resume point, so keep it
current as you go, not at the end.

**User's naming convention (respect it, don't "correct" it):**
A leading underscore marks **the user's own hand-written functions** — `_handle_file_path`,
`_to_internal_document`, `_extract_text`. Names *without* a leading underscore are generally
**library calls** — `read()`, `json.dumps()`, `Path()`. This is the user's personal readability
aid, not the standard Python meaning of `_` (which is "internal/private"). Do not suggest
renaming on style grounds.
Caveat to remember when reviewing: the user's **public entry points** are also their own code
despite having no underscore — `route_push_input`, `route_pull_source`, `process_directory`,
and the reader `read()` methods. So "no underscore" does not reliably mean "not the user's".

Teaching protocol:
- **One concept at a time.** Do not stack three new ideas in one answer.
- **Define jargon on first use** — offsets, spans, tokenisation, dataclass, NLI, F1, precision
  vs recall, calibration, ablation. Assume none of it is known.
- **Concrete tiny examples before abstraction.** Show a 5-word string, not a formula.
- **Why before what.** Explain the problem a thing solves before naming the thing.
- **Check understanding before moving on**, and prefer a question over a wall of text.
- **No unexplained mathematics.** Every symbol gets named in words.
- Their ingestion work is genuinely good — build on that as the anchor for new concepts.

---

## Project spec template — how the user briefs Claude

When starting any new module, the user fills this in and Claude answers with the five
deliverables below. Answer with the spec (concept → stack → structure → pseudocode → build
order) before writing implementation code, even though R10 now permits code.

```
# PROJECT SPEC → I need: concept, tech stack, and pseudocode

## 0. Meta
- Project name: [name]
- One-line purpose: [what it does in one sentence]
- Who uses it & how: [e.g. "me, via a web dashboard" / "runs automatically daily"]
- Platform target: [web / mobile / CLI / desktop / backend service]

## 1. Problem
[2–3 sentences: what problem this solves and why it matters. No solution yet — just the problem.]

## 2. Inputs
For each input, give: name — type — source — format — constraints
- [input 1] — [text/number/file/API response/etc.] — [where it comes from] — [format] — [rules, e.g. "max 10MB", "must be a valid email"]
- [input 2] — ...

## 3. Process (the logic I know)
Write the steps as plain numbered English. Be exact about order and decisions.
1. [step]
2. IF [condition] THEN [do X] ELSE [do Y]
3. FOR EACH [thing] DO [step]
4. [step that transforms input → output]
...

## 4. Outputs
For each output: name — type — destination — format
- [output 1] — [file/screen/API/db record] — [where it goes] — [format]

## 5. Data to remember (state / storage)
[Anything that must persist between runs or sessions. If nothing, write "none".]

## 6. External services / integrations
[APIs, databases, auth, payment, email, etc. If none, write "none".]

## 7. Constraints
- Scale: [how many users / how much data / how often it runs]
- Speed: [must respond in X / batch overnight is fine / real-time]
- Budget: [free-tier only / paid ok]
- Offline?: [needs to work offline? y/n]
- Anything else: [security, privacy, compliance]

## 8. Non-goals
[What this project will NOT do — prevents scope creep.]

## 9. Success looks like
[How I'll know it works. One concrete example: given THIS input, I expect THIS output.]
- Example: input = [...] → output = [...]
```

**What Claude returns, in this order:**

1. **Concept** — restate the project in Claude's words + a text architecture diagram
   (boxes/arrows) showing data flow input → process → output.
2. **Tech stack** — specific tools (language, framework, database, libraries, hosting). For EACH
   choice: what it is, why it fits the constraints above, and one alternative that could have
   been picked instead.
3. **File/folder structure** — the layout as a tree.
4. **Pseudocode** — for every step in section 3:
   - Language-agnostic, readable as English.
   - Use FUNCTION, IF/ELSE, FOR EACH, WHILE, RETURN.
   - Name every function by what it does: `get_user_input()`, `validate_file(x)`.
   - A one-line `# comment` above each block saying WHY, not just what.
   - Show the data shape at key points (e.g. `# data is now: {name, email, score}`).
   - Mark anything external as `# [API CALL]` or `# [DB WRITE]`.
5. **Build order** — a numbered checklist of what to code first, second, third, so the user can
   build piece by piece and test each piece before moving on.

**Ask clarifying questions BEFORE writing anything if any section is unclear.**

---

## Hard rules (violating these is a bug, not a style choice)

- Only `InternalDocument.text` enters NLP. Readers return **raw record dicts**; only
  `InputRouter._to_internal_document()` builds an `InternalDocument`.
- Preprocessing never reads files, JSON or PDFs — it takes a **string**.
- **Text is immutable after ingestion. Annotate, never rewrite.** (Decided; overrides
  `claudenew.md` §8, which has `TextProcessor.normalize()` return a rewritten string.)
  Rewriting the text — lowercasing, collapsing whitespace — shifts every character position, so
  evidence spans would point at the wrong characters in the real article, silently. Instead:
  parse the original text once with spaCy and *label* tokens (lowercase form, is-stopword,
  is-punctuation); analysis filters on labels. `token.idx` then always gives a true offset into
  the original. HTML stripping is the one genuine rewrite, and it already happens in
  `HTMLReader` during ingestion, before NLP sees the text.
  **Owed to the user: a proper explanation of this when they reach `segmentation.py` — they
  deferred it as too abstract, which was reasonable. Explain it against real tokens on screen.**
- Data passes between modules **in memory**, never through files. JSON/Parquet only at the
  boundaries.
- The vector DB (FAISS) is **read-only semantic memory** — it never participates in scoring.
- `FeatureRegistry` is consulted **before** `FeatureExtractor` runs (taxonomy gates which
  layers execute).
- Airflow orchestrates only; it contains no NLP logic.
- `seed` always comes from `pipeline_v1.yaml → pipeline.seed`, never hard-coded.
- Preprocessing must be idempotent: `preprocess(preprocess(text)) == preprocess(text)`.
- Never invent new scoring math — implement `claudenew.md` §21 exactly.

---

## File map — done vs stub

### Complete / real code — Phase 0, all working and tested
- `nlp_pipeline/shared_types.py` — `Token`, `Sentence`, `NormalizedDocument`, `EvidenceSpan`,
  `RuleClassificationResult`, `CategoryScore`, `ScoredDocument`
- `nlp_pipeline/deterministic_utils.py` — `_set_global_seeds`, `_hash_to_document_id`,
  `_compute_config_hashes`, `_round_floats`
- `nlp_pipeline/preprocessing.py` — `TextProcessor.normalize()`, tokens with true offsets
- `nlp_pipeline/segmentation.py` — `SentenceSegmenter.segment()`, paragraph-first, pysbd
- `nlp_pipeline/rules_engine.py` — `RuleEngine.classify()` → evidence spans
- `nlp_pipeline/scoring_engine.py` — `ScoringEngine.score()`, per-category only
- `nlp_pipeline/postprocessing.py` — `PostProcessor`, builds + validates + re-checks every quote
- `taxonomy_tools/taxonomy_loader.py` — `load_taxonomy()` with validation
- `io_adapters/input_router.py` — **rewritten**; real readers actually invoked
- `main.py` — `PipelineRunner`, CLI, no absolute paths
- `conf/taxonomy_v1.yaml` — 5 categories · `conf/scoring_v1.yaml` — the scoring formula
- `data_schema/output_schema.json` / `input_schema.json` — real draft-2020-12 schemas
- `tests/` — 6 files, 43 tests, includes the R2 false-positive gate and a two-process
  byte-identical determinism test
- `pytest.ini`

### Inherited, still reference material
- `core/internal_document.py` — `InternalDocument` dataclass (`document_id`, `text`,
  `source_type`, `ingestion_timestamp`, `source_metadata`, `language`, `title`, `author`,
  `processing_status`, `tables`, `images`, `sections`, `quality_flags`, `char_count`,
  `word_count`, `line_count`) + `to_dict/to_json/to_jsonl/from_dict`. **The main contract.**
- `core/exceptions.py` — `IngestionError`, `UnsupportedFileTypeError`, `NoTextFoundError`,
  `InvalidInputError`, `SourceConnectionError`, `ExtractionError`
- `io_adapters/file_readers.py` — real read logic for Txt, PDF, Docs, CSV, JSON, JSONL, HTML,
  XML, Markdown readers
- `conf/pipeline_v1.yaml` — full config: input sources, output formats, feature flags, ML,
  embeddings, logging, batch settings

### Stubs — method bodies are `pass`
- `nlp_pipeline/` — `features.py` (+ empty feature classes), `ml_classifier.py`,
  `hybrid_router.py`, `ontology_graph.py`, `embeddings_onnx.py`, `vector_index.py`,
  `gpu_router.py`, `extras.py`
- `io_adapters/` — `ingest_clients.py` (API/ES/S3/Kafka/Scraper/Redis, each with `receive()` +
  `fetch()`), `storage_clients.py` (Parquet/JSONL/Redis/Local writers + factory)
- `taxonomy_tools/` — `taxonomy_versioning.py`, `taxonomy_suggestions.py`
- `api/service.py` (`create_app()`), `api/models.py` (empty)
- `src/core_accelerators/` and `src/gpu_support/` — 1-line C++/CUDA stubs. **Do not wire into
  the main path until core NLP works.**

### Other
- `.venv/` — Python 3.10.10. Six packages: pyyaml, pysbd, jsonschema, numpy, pytest,
  charset-normalizer. Gitignored. Run things with `.venv\Scripts\python.exe`.
- `models/` — **does not exist yet**; needed before ML/embedding stages.
  `pipeline_v1.yaml` references `models/news_classifier.onnx` and `models/sentence_encoder.onnx`.
  Gitignored.
- `data/raw/sample_article.txt` — the worked example every doc refers to.
- `notebooks/` — research only; never imported by production code.
- `pyproject.toml` — complete (`media-nlp-pipeline`, src layout, Python >= 3.10).
- `requirements-dev.txt` — 98 lines, mostly frozen under R7. Install from it only if you need a
  specific reader (pdfplumber, python-docx, beautifulsoup4, pandas).

---

## Known bugs — all fixed 2026-08-21

The five bugs previously listed here are closed: the router now instantiates real readers,
`ml_classifier` imports `joblib` directly, the duplicate `io_adapters/shared_types.py` is
deleted, `seed` is `42`, and the `features.py` class-name typos are corrected. Details and
verification in `observe.md` §8.16.

---

## Design risks — binding decisions that OVERRIDE the original design

`claudenew.md` is a catalogue of everything the system *could* be. It is not a plan, and
following it literally produces a 3–5 engineer-year build that never ships. These seven
decisions take precedence over anything in `claudenew.md` that contradicts them.

**R1 — Scope. Ship the vertical slice before anything else.**
The design spans 9 ingestion adapters, 13 feature layers, 15 fallacies, 13 propaganda
techniques, argument mining, ontology graph, FAISS, ONNX, Spark, Ray, Airflow, FastAPI and
C++/CUDA. Build Phase 0 below, end to end, first. Nothing outside Phase 0 starts until Phase 0
runs on a real file.

**R2 — Precision over recall. Detectors are guilty until proven innocent.**
Naive keyword rules misfire badly on real prose: `either…or` → False Dilemma fires on ordinary
sentences; `because` joining two past-tense clauses → False Cause fires on normal causal
writing. Therefore:
- Default threshold **τ = 0.8**, not 0.5 (`claudenew.md` §12.4 offers both — use the precision end).
- **Every detector ships with a false-positive test over neutral text** (a Wikipedia paragraph
  or a dry news report) asserting it does *not* fire. A detector without that test is not done.
- Prefer flagging nothing to flagging wrongly. This system's value is trust.

**R3 — Do not expose uncalibrated composite scores.**
`BiasScore`, `ManipulationIndex`, `QualityScore` and `PropScore` are functional *shapes* with no
fitted weights, no labelled corpus and no validation set. `PropScore = 1 − Π(1−v_p)` saturates
toward 1 on ordinary emotive journalism. Layering them compounds error and then presents the
result as auditable.
- Until a labelled evaluation set exists, the output exposes **per-detector findings, evidence
  spans and counts** — not a single headline number.
- If a composite is computed, it ships with its **breakdown** and is labelled uncalibrated.
- Never present a score as auditable when the detectors underneath it are not measured.

**R4 — Evidence-grounding is the headline feature, not fallacy coverage.**
Detecting 15 fallacies badly is unimpressive; detecting 3 reliably with verbatim spans and
reproducible scores is a system. Every detection **must** carry an exact substring plus
`start_char`/`end_char` or it does not ship (`claudenew.md` §22). No paraphrased quotes, ever.

**R5 — Detector admission list.** Build only detectors that can reach acceptable precision from
text alone. Park the rest explicitly:
- **Build first:** Loaded Language, Bandwagon, Name-Calling/Ad Hominem (toxicity + PERSON),
  Unsupported Quantifiers, Source Opaqueness. These have clear lexical signatures.
- **Parked — needs external knowledge or unsolved research:** Equivocation (admitted as
  near-undoable), Strawman (needs the opponent's real position), Red Herring, Cherry Picking,
  Omission Bias, Conflict of Interest, False Attribution.
- SemEval span-detection F1 of 0.4–0.6 is the published state of the art. Treat any claim of
  better as a bug until measured.

**R6 — Determinism does not imply correctness.** "Same input → same output" is fully satisfied
by a system that is reproducibly wrong. Determinism is an audit property, never evidence of
accuracy. Keep the two claims separate in code, tests and any write-up.

**R7 — Frozen until the slice runs.** Do not create, wire or touch: `core_accelerators/`,
`gpu_support/`, `gpu_router`, `vector_index`, `embeddings_onnx`, `ml_classifier`, Kafka, Spark,
Ray, Elasticsearch, S3, Airflow. They exist as architecture demonstration only. Deleting them is
also an acceptable answer.

**R8 — Literature review is a hard gate on the research track.** No research code is written
until the novelty claim is verified against published work. See "Research track" below. The
literature claims in that section were made **without browsing access and are leads, not
facts** — they must be checked before any effort is committed.

**R9 — Never invent logical fallacies.** Fallacies are a catalogued philosophical taxonomy from
Aristotle's *Sophistical Refutations* onward. Proposing "new fallacies" from an armchair reads as
pseudo-scholarship and is a desk-reject at ArgMining, where actual argumentation theorists
review. Novelty comes from three legitimate routes only, in this order of safety:
1. Better **operationalisations** (formulas + formal properties) of *existing* fallacies.
2. **Bottom-up discovery** from data — cluster unmatched spans, surface candidates, validate
   with annotators (this is `taxonomy_suggestions.py` / `claudenew.md` §20.4).
3. **Candidate patterns stated as falsifiable hypotheses** with operational definitions, tested
   against human annotation.
Correct framing: *"we operationalise four candidate patterns and test whether annotators agree
they constitute manipulation."* Never: *"we introduce four new fallacies."*

---

## Build order

### Phase 0 — the vertical slice (do this first, nothing else)

**Goal:** one `.txt` file in → validated JSON out, with verbatim evidence spans and a proven
byte-identical rerun. This is the "stupid simple pipeline" of §30, and it is the deliverable.

1. `nlp_pipeline/shared_types.py` — dataclasses for `NormalizedDocument`, `Sentence`,
   `FeatureBundle`, `RuleClassificationResult`, `ScoredDocument` (type table: `claudenew.md`
   §43.1). The contracts every stage signs.
2. Fix `InputRouter` (bug 1) — instantiate readers; wire `_handle_file_path()` to
   `reader.read(file_path)`. Prove it with a real `.txt` and a real `.pdf`.
3. `deterministic_utils.py` — `set_global_seeds`, `hash_to_document_id`, `compute_config_hashes`.
4. `preprocessing.py` — `TextProcessor.normalize()`. Test idempotency:
   `preprocess(preprocess(t)) == preprocess(t)`.
5. `segmentation.py` — `SentenceSegmenter.segment()` via pysbd, with correct char offsets.
   Offsets are load-bearing for R4 — test them.
6. `conf/taxonomy_v1.yaml` — **5–8 categories, not 28 detectors.** Only the R5 "build first"
   set. Currently empty and blocking everything.
7. `rules_engine.py` — lexicon/pattern rules for those categories, each emitting an
   **evidence span** (§43.1 `RuleClassificationResult` carries evidence).
8. `conf/scoring_v1.yaml` + `scoring_engine.py` — one simple per-category score. Per R3, no
   composite headline number yet.
9. `postprocessing.py` + `data_schema/output_schema.json` — build and validate the output
   (shape: `claudenew.md` §24).
10. `main.py` — `PipelineRunner` (§30.4); replace the hard-coded absolute config paths.
11. `tests/` — `test_preprocessing`, `test_segmentation`, `test_rules_engine`,
    `test_output_schema`, **`test_determinism`**, plus the R2 false-positive tests.

**Phase 0 is done when:** `python src/main.py --input article.txt` emits schema-valid JSON with
verbatim spans and offsets, two consecutive runs are byte-identical, and every detector has a
passing false-positive test.

### Phase 1 — done, except two items deliberately deferred

Done: `taxonomy_loader.py` · `storage_clients.py` (JSONLWriter / JSONWriter / ParquetWriter +
factory) · `api/service.py` + `api/models.py`.

**Deferred with reasons** (`observe.md` §9.5): `ontology_graph.py` — the taxonomy is five flat
categories with no hierarchy, so there is no tree to walk yet; `features.py` Phase-1 layers —
nothing consumes them until the ML classifier exists, which is Phase 2.

### Phase 2 — only with a labelled evaluation set in hand

`ml_classifier.py` · `hybrid_router.py` · composite scoring per R3 · `feature_registry.py`
gating · `argument_miner.py` · the Phase-2 feature layers.

### Phase 3 — infrastructure, only if a real workload demands it

Embeddings/FAISS · batch processing (Spark/Ray) · Airflow · the remaining ingestion adapters ·
accelerators.

**Discipline** (full version in `claudenew.md` §30): one module at a time, one class at a time,
minimum code first, commit per file. Get the flow working before adding heavy logic.

---

## Research track

**This project has two real outputs: a working product and a research paper.** They are not in
competition — they share most of the build and the research unblocks the product.

### What is NOT publishable
"We built a pipeline that detects bias/fallacies" · the taxonomy · the 13 feature layers ·
applying an LLM to the task. All done before; reviewers reject engineering-as-contribution.

### The gap being attacked
LLMs now dominate bias/fallacy/propaganda analysis but **fabricate their own evidence** —
returned "quotes" are frequently paraphrased, merged or absent from the source. Simultaneously,
regulation (EU AI Act, DSA transparency duties) is moving toward requiring auditable,
reproducible content analysis. The field is moving away from auditability exactly as the
requirements move toward it. This project's founding constraints — determinism and
"evidence must be an exact substring with character offsets" (`claudenew.md` §22) — sit on that
fault line.

### R8 gate — do this before writing any research code
Search ACL Anthology / Semantic Scholar for: *verbatim grounding · rationale faithfulness ·
quote fidelity · extractive rationales + LLM · evidence hallucination · citation faithfulness*.
Check whether the substring test has already been run on this domain. **If P1 is already
published, it becomes a replication — pivot to P2 or P3.** Known related work to position
against (verify each): ERASER / rationale faithfulness (DeYoung et al. 2020), faithfulness vs
plausibility (Jacovi & Goldberg 2020), SemEval-2020 Task 11 fine-grained propaganda
(Da San Martino et al.), logical fallacy datasets (Jin et al.), media-bias corpora (BABE /
Spinde et al.).

### P1 — primary paper: "Do LLMs cite what they claim?"
**Claim:** in media-analysis tasks, LLM-produced evidence spans frequently fail verbatim
grounding, and this is invisible to standard evaluation because nobody checks the substring.

Protocol (no training, no GPU required):
- **Corpora:** 200–300 articles from SemEval-2020 Task 11 PTC (span-level propaganda — the best
  fit), plus BABE (bias) and Jin et al. (fallacy). Verify licences before use.
- **Models:** one frontier API model, one mid-tier, one small CPU-runnable open model.
- **Task:** identify bias/propaganda spans, quote them, and give character offsets.
- **Metrics:**
  - *Verbatim rate* — is the quote an exact substring? (`str.find`; objective and uncontestable)
  - *Normalised-match rate* — match after whitespace/quote/case normalisation.
    **Reporting exact and normalised separately is methodologically load-bearing** — it
    separates "differs by a curly apostrophe" from "the quote does not exist." Reviewers will
    ask for this.
  - *Offset accuracy* — do returned offsets land on the cited text?
  - *Run-to-run span instability* — same input, temperature 0, N runs: how often do spans change?
  - *Rule-engine baseline* — verbatim rate = 1.0 **by construction**.
- **Failure taxonomy** (a contribution in itself): paraphrase · boundary drift · merged/spliced
  spans · cross-sentence splice · hallucinated content · entity substitution.
- **Controls:** document length, span position in document, temperature/seed.

### P2 — formalism: evidence-bound scoring
Define a scoring function as **evidence-bound** iff its output is a deterministic function of a
set of verbatim, offset-anchored spans. Three testable properties:
- *Reconstructibility* — recompute the score from the cited spans alone (0 error for rule
  systems by construction; measure the gap for neural ones).
- *Erasure consistency* — delete cited spans, rerun; the score must move by the amount the
  formula predicts. This is ERASER-style comprehensiveness/sufficiency extended from
  classification to **composite document-level scores** — believed open, verify under R8.
- *Citation faithfulness* — the P1 metric.

`claudenew.md` §21 supplies the worked example: `PropScore = 1 − Π(1−v_p)` is trivially
reconstructible; an LLM's bare "bias: 0.73" is not reconstructible at all.

### P3 — the determinism–accuracy frontier
`α` in the hybrid router (`claudenew.md` §21.1 formula 2) is already the knob. Sweep α from 0
(pure rules) to 1 (pure ML); plot F1 against an output-reproducibility measure (variance across
runs/seeds/hardware). Yields a Pareto curve quantifying **the price of reproducibility** — a
number anyone building under audit constraints needs, and not yet quantified for this domain.

### Method contribution to attach: Propose-and-Verify
LLM **proposes** candidate spans (high recall); a deterministic rule verifier **confirms** each
against explicit criteria; only verified spans reach the output. The LLM never touches the final
score, so the system stays reproducible and every decision traces to a rule — while recovering
the recall pure rules lose. Neuro-symbolic framing. This is R2 + R4 turned into a method, and it
answers "why not just use an LLM."

### Formal contributions — scoring properties and formula fixes

The formulas in `claudenew.md` §21 are hand-waved heuristics with no stated properties. Fixing
that is the safest novelty route (R9 route 1), because current detection formulas in this field
are largely arbitrary thresholds.

**Properties a scoring function should satisfy** — state these, then show existing formulas
violate them:
*bounded* [0,1] · *monotone* in evidence · *length-behaviour explicit* · *erasure-consistent*
(removing a cited span moves the score by a predictable amount) · *reconstructible* from the
cited spans alone. The last two tie directly to P2.

**F1 — the PropScore independence bug (highest-value single result).**
```
PropScore = 1 − Π_p (1 − v_p)          # current: a noisy-OR
```
Noisy-OR assumes propaganda techniques are **statistically independent**. They are not — loaded
language, name-calling and appeal-to-fear co-occur heavily. With 13 techniques at even modest
intensity the product saturates toward 1, so ordinary emotive journalism scores as propaganda.
**This is the concrete cause of the R3 false-positive problem.** Proposed replacement, a
smooth-max that does not compound correlated evidence:
```
PropScore_γ = (1/γ)·log( (1/|P|)·Σ_p exp(γ·v_p) )     γ > 0
```
γ→0 → mean, γ→∞ → max; fit γ. Experiment: measure technique co-occurrence in PTC → show
independence is violated → show noisy-OR miscalibrates → show the corrected aggregator tracks
human judgement better. Small, sharp, defensible.

**F2 — length normalisation as an empirical question.**
```
s = 1 − exp( −λ · Σ_i w_i·c_i / L^β )
```
β = 0 is a raw count, β = 1 is pure density. The right β for this task is unestablished — fit
and report it. A β ablation is a cheap, clean experiment.

**F3 — discourse-position weighting.** A fallacy in the headline/lede reaches every reader; one
in paragraph 12 reaches few.
```
w_pos(i) = exp( −κ · rel_position(i) )
```
Ablate κ; improvement or no improvement are both reportable.

**F4 — compound severity (super-additivity).** Current designs sum independent severities.
Hypothesis: co-occurring fallacies compound.
```
C = Σ_i s_i + λ · Σ_{(i,j) adjacent in argument graph} min(s_i, s_j)
```
Test λ > 0 against human manipulativeness ratings. This is where `argument_miner.py` earns its
place in the build.

### Candidate patterns — hypotheses, never inventions (R9 route 3)

Each needs validation against human annotation before being called a pattern.

**H1 — Headline–body modality mismatch ("hedge-then-assert").** Body hedges, headline asserts.
Distinct from clickbait (which is sensationalism, not epistemic strength).
```
M = certainty(headline) − mean_certainty(body claims on the same proposition)
```
certainty = a modality score over hedges/boosters. Flag when M > τ. Crisp, cheap, likely real
signal — **best first candidate.**

**H2 — Attribution laundering.** A claim's certainty rises across a document while its sourcing
does not ("a source suggests" → "reports indicate" → "it is known that").
```
A = Δcertainty across mentions of the same claim − Δcitation_support
```
Needs claim coreference, so harder — but genuinely novel if it works.

**H3 — Quote-frame asymmetry.** One side gets direct quotation, the other paraphrase; indirect
speech lowers perceived credibility.
```
Q_e = direct_quotes(e) / (direct_quotes(e) + paraphrases(e))
```
then measure the spread across entities in a story. Builds on `claudenew.md` §16.

**H4 — Anchoring without denominator.** The first quantity stated frames all later ones and is
given with no base rate.

### Taxonomy induction (R9 route 2) — nearly free
`taxonomy_suggestions.py` is already specced for this (`claudenew.md` §20.4): cluster
low-confidence/unmatched spans with a fixed seed → keywords + representative examples per
cluster → human review → versioned `taxonomy_v2.yaml`. Framed as research this answers *"what
recurring manipulation patterns in contemporary news are not covered by the classical
taxonomy?"* — a resource-paper contribution when supported by clusters, examples and
inter-annotator agreement. Worthless without them.

### Venues
Not ACL/EMNLP main first. Target **ArgMining · TrustNLP · FEVER · NLP4PI · CONSTRAINT**
workshops, or **Findings**. The auditability framing also fits **FAccT**. Workshop = 4–8 pages,
reviewed by people who care about this, citable artifact fast.
Rough P1 timeline part-time: ~2 weeks data + harness, 2 weeks runs, 2 weeks analysis, 2 weeks
writing.

### Product and paper — the split

**Shared core — serves both, build once (this is Phase 0):**
shared_types (1) · InputRouter fix (2) · deterministic_utils (3) · preprocessing (4) ·
**segmentation with exact char offsets (5)** · taxonomy_v1.yaml, small (6) · rules_engine
emitting evidence spans (7) · scoring_engine, simple (8) · postprocessing + output_schema (9) ·
main.py (10) · tests (11).

For the paper, item 5 is load-bearing in a way it isn't for the product: **offsets are the
measurement**. Get them exactly right.

**Research-only — new `research/` directory:**
corpus loaders (PTC / BABE / Jin) · prompt templates · model runners · metric scripts
(verbatim / normalised / offset / instability) · failure-taxonomy annotation · results tables.
Throwaway-grade code is fine here; it is not part of the product.

**Product-only — deferred, NOT dropped:**
storage_clients + Parquet Bronze/Silver/Gold · FastAPI service · the remaining ingestion
adapters · batch processing · ontology graph and multi-label hierarchy · the Phase 1–3 feature
layers.

### Sequencing — why research goes second, not last

1. **Phase 0 (shared core)** — needed by both, blocks everything.
2. **Research (P1)** — next, for three reasons: the novelty is **time-sensitive** (someone else
   may publish the substring test; the product has no such deadline); it is **cheap** (no
   training, no GPU, ~8 weeks part-time); and its measurements are **an input to the product**.
3. **Product hardening (Phases 1–3)** — informed by what the research found.

The synergy is concrete, not a rationalisation:
- **R3 says do not expose uncalibrated composite scores.** The research track produces exactly
  the labelled-corpus measurements that lift that restriction. The paper is how the product
  earns the right to show a number.
- **R5's detector admission list is currently a guess.** P1/P3 measure per-detector precision on
  public corpora, converting the guess into evidence — telling you which detectors are worth
  shipping and which to keep parked.
- **Propose-and-Verify** is simultaneously the paper's method contribution and the product's
  answer to "why not just call an LLM."
- The rule engine is the paper's **baseline** and the product's **engine**. One artifact.

Consequence: nothing built for the paper is wasted on the product, and vice versa — provided the
shared core is built once, properly, and the `research/` code stays quarantined in its own
directory.
