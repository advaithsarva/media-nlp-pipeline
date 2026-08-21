# observe.md — running notes, review findings and open questions

Claude's working notebook for this project. Not a spec (that's `CLAUDE.md`) and not the design
catalogue (that's `claudenew.md`). This is: what was noticed, what's still wrong, what was
deferred, and what to revisit.

Newest entries at the top of each section.

---

## 1. Open — needs your action

*(Rewritten 2026-08-21. Everything that was blocking Phase 0 is now closed — see §8 for the
full build log. What remains is listed here.)*

### Nothing is blocking the pipeline

`python src/main.py --input data/raw/sample_article.txt` runs, emits schema-valid JSON with
verbatim evidence spans, and two runs are byte-identical. 43 tests pass. The five bugs from
`CLAUDE.md` are all fixed (§8.16).

### Open, in rough priority order

| Item | Why it matters |
|---|---|
| **Run it on a real article you choose** | Every threshold, weight and lexicon entry in the system is unvalidated. Reading the output on a piece of journalism you already have an opinion about is the fastest way to find where it is wrong. |
| **R8 literature review** | Not started. Gates the whole research track and can invalidate P1 outright. It is reading, not coding. |
| **`lambda = 4.0`, `beta = 0.5` are guesses** | Labelled as such in `conf/scoring_v1.yaml`. Fitting them is research work (F2). |
| **Quoted speech is not excluded from detection** | An article quoting someone else's loaded language currently scores as loaded itself. Real precision issue; needs a quotation-span detector, which is its own module. |
| **Only `.txt` has been run end to end** | The other eleven extensions are wired up and import cleanly, but reading a real PDF or `.docx` needs `pip install pdfplumber python-docx` first, and neither has been tried. |
| **`storage_clients.py` still a stub** | Output goes to stdout or `--out`. No Bronze/Silver/Gold Parquet. Phase 1. |
| **`myenv` (conda) — what is it for?** | Still unanswered, and now largely moot: this repo uses its own `.venv` (Python 3.10.10) and does not touch conda. |

### Closed this session

- ~~`main.py` does not parse~~ — rewritten; no absolute paths anywhere.
- ~~`deterministic_utils.py`: 110 lines of pasted prose above 22 lines of code~~ — prose removed.
- ~~`shared_types.py`: 44-line ASCII comment block; invariant test commented out~~ — comments
  moved next to what they explain; the test now lives in `tests/test_segmentation.py` and runs.
- ~~`io_adapters/shared_types.py` shadows the real `InternalDocument`~~ — file deleted.
- ~~`conf/taxonomy_v1.yaml` and `conf/scoring_v1.yaml` are 0 bytes~~ — both written.
- ~~`data_schema/output_schema.json` is a placeholder~~ — real draft-2020-12 schema.
- ~~`input_router.py` calls `_mock_file_read`~~ — rewritten, real readers invoked.
- ~~`preprocessing.py` methods are all `pass`~~ — written.
- ~~`tests/*.py` are empty~~ — 43 tests.
- ~~No environment exists~~ — `.venv` on Python 3.10.10, six packages.

## 2. Comments to add

**Working rule (R13):** after every module Claude supplies comment content as a
*location → text* table. Keep them short, placed next to what they explain, and about **why**.
Do not paste Claude's prose messages into `.py` files — that happened on `shared_types.py`
(173 lines of prose above 47 lines of code) and should be undone.

### `shared_types.py`

| Location | Comment |
|---|---|
| Top of file | Shapes only — no logic. Every pipeline stage speaks in these types, which is how stages stay independent of each other. |
| Top of file | Imports `core` + stdlib only. Never import `io_adapters` or other `nlp_pipeline` modules here — that creates circular imports. |
| Above `Token` | The "label, don't rewrite" rule made concrete: `text` is the word exactly as written; `lower` and `lemma` are labels *on* it. Original text is never modified, so `idx` stays true forever. |
| On `idx` | Start position in the original document text. spaCy supplies this. |
| Above `Sentence` | Invariant: `original_text[start_char:end_char] == text`. If that breaks, every offset downstream is wrong. |
| On `end_char` | Exclusive, like Python slicing. |
| Above `NormalizedDocument` | Holds the *original* text plus annotations — deliberately no `clean_text` field. Mutable because it accumulates as the pipeline runs. |
| On `tokens` | Required, not optional: a document with no tokens is meaningless and would hide a bug. |
| On `metadata` | `default_factory` gives each instance its own dict. A plain `{}` default would be shared by every instance. |
| Above `EvidenceSpan` | R4: evidence is a first-class object, not a string on a result. Same slice invariant as `Sentence`. `rule_id` is what makes a score traceable to the rule that produced it. |
| Above the TODO classes | Skeletons — shapes get finalised when the rules engine and scoring are written. |

### `deterministic_utils.py`

Write these in your own words — the point is to process the reasoning, not transcribe.

| Where | What the comment should capture |
|---|---|
| Top of file | This module exists so runs are reproducible and results traceable. No state, no classes, depends on nothing else in the project. |
| Above `set_global_seeds` | Every library keeps its **own separate** random generator. Seeding `random` does not seed numpy. That's why one function sets both — miss one and part of the pipeline stays random. |
| On the validation line | numpy rejects negatives and anything ≥ 2³². Fail here with a clear message rather than deep inside a model with a confusing one. |
| Above `hash_to_document_id` | Same text must always produce the same ID — no database, no counter. This is what makes IDs stable across machines and runs. |
| On the `.encode("utf-8")` | Hashing works on bytes, not text. utf-8 fixes how characters become bytes, so the same string hashes identically on every machine. |
| Above `compute_config_hashes` | A fingerprint of the settings that produced a result. Change any config value → different hash → you can prove which settings produced which output. |
| **On `sort_keys=True`** | **The critical line.** Dicts have no guaranteed order; `{a:1,b:2}` and `{b:2,a:1}` are the same config but would hash differently without sorting. Sorting makes the text form canonical: one config, one hash, always. |
| On the return | Returns `{"pipeline_hash": ..., "taxonomy_hash": ..., "scoring_hash": ...}` — stamped onto every output record. |

---

## 3. Known limitations (accepted, not bugs)

- **Boolean seeds pass validation.** `isinstance(True, int)` is `True` in Python — booleans *are*
  integers. So `set_global_seeds(True)` is accepted and behaves as seed 1. Harmless; noted so it
  doesn't surprise you.
- **`PYTHONHASHSEED` is outside this module's reach.** Python randomises string hashing per
  process, which can change set-iteration order. It's set by an environment variable *before*
  Python starts, so no runtime function can fix it. Only bites if iteration order over a set of
  strings affects output.
- **Identical text → identical document ID.** The same article from two sources collapses to one
  document. Excellent for deduplication, wrong if you ever need both copies. Chosen deliberately.
- **`json.dumps` raises on non-serialisable config values** — a `datetime`, or a Python object
  from YAML. Not a problem with current configs; will surface if one is added.

---

## 4. Deferred — explanations owed to you

- **The offset / immutable-text decision.** You deferred this as too abstract, which was
  reasonable. Decision recorded in `CLAUDE.md` hard rules: *text is immutable after ingestion,
  annotate rather than rewrite.* **Owed: a proper walkthrough against real spaCy tokens on
  screen when you reach `segmentation.py`.** The short version: rewriting text (lowercasing,
  collapsing spaces) shifts every character position, so evidence spans would point at the wrong
  characters in the real article — silently.
- **R8 literature review.** Not started. Gates the whole research track and can invalidate it.
  It's reading, not coding, so it can run in parallel with the rewrites.

---

## 4b. Working process — now mirrored in `C:\Projects\models`

Both projects run the same loop: pick module → Claude gives spec/contract → user writes it →
Claude **reads the actual file** before reviewing → findings logged here → comment table
supplied → next module.

Deliberate difference between the two repos:

| | NLPpipline | models |
|---|---|---|
| No-code rule | R10 | R1 |
| Scope | code **+ configs + plumbing** (extended to match models) | code + configs + plumbing |
| Pseudocode | **allowed and expected** — no hard-mode doc exists here | **restricted** — `pseudo_hardmode.md` deliberately strips recipes, so spec-covered components get contract + FIGURE OUT + CHECK instead |
| Docs Claude may write | `CLAUDE.md`, `observe.md`, `claudenew.md`, `README.md` | same |

---

## 5. Environment — unresolved

- **No `pipe` environment exists.** Two creation attempts were stopped by you; the plan is
  unfinished.
- **Python 3.10 is installed** at `...\Programs\Python\Python310\python.exe`. **`python` on PATH
  is 3.12.1** — and 3.12 is what broke the dependency install previously. Any venv must be
  created with `py -3.10` explicitly.
- **conda is installed** (`C:\Users\advai\anaconda3`) but **not on PATH**. Existing envs: `base`
  (3.11.5), **`myenv` (3.10.13 — already has spacy, pydantic, pytest)**, `quant` (3.10.19).
- **Unanswered: what is `myenv` for?** If it belongs to another project, don't install into it.
  If it was made for this one, it's usable as-is.
- Recommendation on the table: a fresh conda env `pipe` on Python 3.10, minimal packages, not
  the full 98-line `requirements-dev.txt` (which includes Airflow, Elasticsearch, PySpark — all
  frozen under R7).

---

## 6. Repo observations

- **`requirements-dev.txt` pins `docx==0.2.4`** — this is a known-broken package, distinct from
  `python-docx`, which is the one you actually want. Expect an install failure here.
- **`input_router.py` was already partly fixed** before this session: `_initialize_file_readers()`
  correctly returns real objects. `CLAUDE.md`'s bug list said otherwise and was stale — now
  corrected. Still stubbed: `_handle_file_path` calls `_mock_file_read` (lines 243–248), and
  `_initialize_source_clients` still returns strings.
- **`.mp3` → `AudioReader()`** exists in the reader registry but appears in no design document.
  Your addition; `AudioReader` is listed as a deferred/stub class.
- **Two `shared_types.py` files exist** — `io_adapters/` and `nlp_pipeline/`. The `io_adapters`
  one is a stub whose fake `InternalDocument` shadows the real one in `core/`. A likely source of
  confusing import errors. Decide its fate before writing new imports.
- **`file_readers.py` is 669 lines, `input_router.py` 436** — by far the largest files, and the
  most entangled. Under R12 these are the *last* things to rewrite, not the first.
- **Windows path literals are a live hazard in this repo.** `main.py` is the first casualty
  (`\N` syntax error, `\t` silent tab). Anywhere a path is written in Python: raw string,
  forward slashes, or `pathlib` — never a plain string with backslashes.
- **Prose-into-source has now happened twice** — `shared_types.py` (fixed) and
  `deterministic_utils.py` (current). Worth making a habit: the spec stays in chat or a scratch
  file; only the §2 comment table goes into the module.

---

## 7. Strategic observations

- **The evidence-first design (`claudenew.md` §22) is the strongest idea in the project** and is
  currently buried in the middle of a 6,400-line document. It's what makes the output defensible,
  and it's the research angle. It deserves to be the headline in any write-up.
- **F1 (the PropScore independence bug) may be a better first paper than P1.** Noisy-OR assumes
  propaganda techniques are independent; they aren't, so the score saturates and ordinary emotive
  journalism reads as propaganda. It's a specific, falsifiable, cheap-to-test claim that also
  explains a real defect in this system. Less crowded territory than the LLM citation audit.
  Decide during the R8 review.
- **Nothing in this repo has ever processed a real document end to end.** Until Phase 0 runs,
  every score, threshold and weight in the design is unvalidated.

---

# 8. Build log — 2026-08-21

**What happened in this session: Phase 0 was built and it runs.** For the first time in the
project's life, a real file goes in one end and a schema-valid JSON report comes out the other,
with verbatim quotes, real character offsets, and two consecutive runs producing byte-identical
output. 43 tests pass.

This section exists because of R14: every line of code written here is explained here. Read it
top to bottom and you should be able to open any file in the repo and know why each line is
there. Terminal commands are logged in §8.17.

**Rule change that made this possible:** R10 was flipped from "Claude writes ZERO code" to
"Claude MAY write code". R14–R17 were added at the same time (write-ups mandatory, simple code
only, no Claude attribution in git, work autonomously).

---

## 8.0 The shape of what now exists

```
data/raw/sample_article.txt
        │
        ▼  InputRouter.route_push_input()          io_adapters/input_router.py
   TxtReader.read() → a dict of everything in the file
        │
        ▼  _to_internal_document()
   InternalDocument   ← text is fixed from here on and never changes again
        │
        ▼  TextProcessor.normalize()               nlp_pipeline/preprocessing.py
   NormalizedDocument (same text + a list of Tokens, each with its position)
        │
        ▼  SentenceSegmenter.segment()             nlp_pipeline/segmentation.py
   + a list of Sentences, each with start_char / end_char
        │
        ▼  RuleEngine.classify()                   nlp_pipeline/rules_engine.py
   RuleClassificationResult — a list of EvidenceSpans
        │
        ▼  ScoringEngine.score()                   nlp_pipeline/scoring_engine.py
   ScoredDocument — one number per category, recomputable from the spans
        │
        ▼  PostProcessor.build_output() + validate()  nlp_pipeline/postprocessing.py
   a dict matching data_schema/output_schema.json
```

`main.py` holds the wiring and nothing else.

**The one idea the whole thing is built around:** every claim the system makes points at an exact
substring of the article, given as `(start_char, end_char)`. You can always slice the original
text with those two numbers and get back the exact words the system quoted. If that ever stops
being true, the system is worthless, so it is checked in three separate places — an assertion in
the segmenter, `PostProcessor.check_evidence()` on every run, and two tests.

---

## 8.1 Environment

There was no working Python environment for this repo before today. `python` on PATH is 3.12,
which had previously broken the dependency install; 3.10 was installed but unused.

Created `.venv` from Python 3.10.10 and installed **six** packages, not the 98 in
`requirements-dev.txt`:

| Package | Why |
|---|---|
| `pyyaml` | reads the three config files |
| `pysbd` | sentence splitting, rule-based so it is reproducible |
| `jsonschema` | validates the output record against `output_schema.json` |
| `numpy` | only for `np.random.seed` — nothing in Phase 0 computes with it |
| `pytest` | the test suite |
| `charset-normalizer` | encoding detection inside the file readers |

Everything else in `requirements-dev.txt` (Airflow, PySpark, Elasticsearch, ONNX, spaCy, pandas,
pdfplumber…) is frozen under R7 or not needed yet. `.venv/` was added to `.gitignore`.

---

## 8.2 `src/nlp_pipeline/shared_types.py` — the contracts

**What it is:** six dataclasses and no logic. A *dataclass* is a Python class where you just list
the fields and Python writes the boilerplate (`__init__`, `__repr__`, `==`) for you. These are
the shapes each stage hands to the next, which is what lets the stages stay ignorant of each
other.

The 44-line ASCII comment table that used to sit at the top of this file is gone — its content
moved to short comments placed next to the thing each one explains, which is what R13 actually
asked for.

**Walkthrough:**

| Code | What it does and why |
|---|---|
| `from dataclasses import dataclass, field` | `field` is needed for list/dict defaults, see the `default_factory` note below |
| `@dataclass(frozen=True)` on `Token` | frozen means the object cannot be modified after creation. A token's position must never be edited by accident. |
| `Token.text` | the word exactly as written in the article — `"The"`, capital and all |
| `Token.lower` | `"the"`. A **label sitting next to** the original, not a replacement for it. |
| `Token.lemma` | dictionary form. No lemmatiser is installed yet, so it currently equals `lower`. |
| `Token.idx` | character position where this token starts in the document text |
| `Token.is_stop`, `is_punct` | more labels. Analysis filters on these rather than deleting words from the text. |
| `@dataclass(frozen=True) class Sentence` | `sentence_id`, `text`, `start_char`, `end_char`. Invariant: `document_text[start_char:end_char] == text`. |
| `end_char` | exclusive, exactly like a Python slice — `text[0:5]` is five characters, positions 0–4 |
| `class NormalizedDocument` | **not** frozen: it accumulates as the pipeline runs. Tokens are attached by preprocessing, sentences by segmentation. |
| `text: str` on `NormalizedDocument` | the original text, unchanged. There is deliberately no `clean_text` field — having one would invite someone to analyse the cleaned copy and report offsets from it. |
| `tokens: List[Token]` (no default) | required. A document with zero tokens is a bug, and a default would hide it. |
| `metadata: Dict = field(default_factory=dict)` | `default_factory=dict` makes a **fresh** dict per instance. Writing `= {}` instead would give every document the *same* dict — a classic Python trap. |
| `word_count` property | counts non-punctuation tokens. A `@property` is a method you call without brackets: `doc.word_count`, not `doc.word_count()`. |
| `class EvidenceSpan` | the heart of R4. `text` + `start_char` + `end_char` + `rule_id` + `category` + `confidence` + `sentence_id`. |
| `EvidenceSpan.rule_id` | e.g. `"loaded_language:lexicon"` — this is what makes a score traceable back to the exact rule that fired |
| `RuleClassificationResult.spans_for(category)` | small helper; the scoring engine asks "what did you find for this category?" |
| `RuleClassificationResult.categories` | returns `sorted({...})`. **The `sorted` matters:** iteration order over a Python set is not stable between runs, so an unsorted version would silently break determinism. |
| `class CategoryScore` | `count`, `raw`, `score`, `calibrated`. `calibrated` is always `False` and stays that way until a labelled evaluation set exists (R3). |
| `class ScoredDocument` | the spans, the per-category scores, and `composite: Optional[float] = None` |
| `composite = None` | the single headline number, deliberately absent |

---

## 8.3 `src/nlp_pipeline/deterministic_utils.py`

**What it is:** four small functions. The 110 lines of pasted spec prose that used to sit above
them are gone.

| Code | What it does and why |
|---|---|
| `MAX_SEED = 4294967295` | that is 2³² − 1. numpy refuses anything larger. Named rather than inlined so the error message can use it. |
| `_set_global_seeds(seed)` | **Every library keeps its own separate random number generator.** Seeding Python's `random` does *not* seed numpy. Miss one and half your pipeline is still random. |
| the `isinstance(seed, int)` check | fails here with a clear message instead of deep inside a model with a confusing one |
| `random.seed(seed)` / `np.random.seed(seed)` | the two generators in play today |
| `_hash_to_document_id(text)` | SHA-256 of the text, as 64 hex characters |
| `.encode("utf-8")` | hashing works on **bytes**, not text. utf-8 fixes how characters become bytes, so the same string hashes identically on every machine. |
| `_compute_config_hashes(...)` | fingerprints the three config files, so any output can be traced to the exact settings behind it |
| `json.dumps(config, sort_keys=True)` | **the load-bearing line.** Dicts have no guaranteed order. `{a:1,b:2}` and `{b:2,a:1}` are the same config but would hash differently without sorting. There is a test for exactly this. |
| `default=str` in that `dumps` | YAML sometimes produces a `date` object, which JSON cannot serialise. Converting to its string form beats crashing. |
| `_round_floats(value, places=6)` | **new function.** Walks a nested dict/list and rounds every float. Float arithmetic can differ in the last bit between machines; rounding before serialising is what turns "nearly identical" into "byte-identical". |

**Naming gotcha found while testing:** these functions all start with an underscore (the user's
convention: underscore = my own function). Python's `from module import *` **skips** names
starting with `_`, so `import *` silently imports nothing from this module. Not a bug — explicit
imports work fine, and `main.py` uses them — but worth knowing.

---

## 8.4 `src/nlp_pipeline/preprocessing.py`

**The rule this module exists to obey: the text is never rewritten.**

Here is the concrete reason, which was owed to you (§4) and is now cashed out. Take the article
text `The plan was disastrous.` The word `disastrous` starts at character 14. Suppose
preprocessing lowercased and collapsed whitespace and handed on `the plan was disastrous.` —
still 14. Now suppose the original was `The  plan was disastrous.` with two spaces. Collapsing
gives `disastrous` at 14, but in the **real article** it is at 15. The report would quote
character 14–24 of the real article and get `disastrou` + a space. Off by one, wrong quote, and
nothing crashes to tell you.

So instead: keep the text exactly as it arrived, and hang labels off each word.

| Code | What it does and why |
|---|---|
| `TOKEN_PATTERN = re.compile(r"\w+(?:['’]\w+)*\|[^\w\s]")` | either a word (letters/digits, optionally with apostrophes so `didn't` stays one token) **or** a single non-space symbol so punctuation becomes its own token |
| `re.finditer` (used in `_tokenize`) | unlike `split`, `finditer` gives back **match objects**, and `match.start()` is the character position. That is where `Token.idx` comes from — for free, and always correct. |
| `STOPWORDS = frozenset("""…""".split())` | a hand-written list of ~90 common words. Kept in the file rather than pulled from nltk so it is visible, versionable and identical on every machine. `frozenset` because lookup is instant and it cannot be modified by accident. |
| `_normalize_unicode` → `unicodedata.normalize("NFC", text)` | the one rewrite that is allowed, done once. NFC combines `e` + a separate accent mark into the single character `é`. Two different byte sequences that look identical would otherwise hash to different document ids. |
| why NFC is safe | it runs at the boundary, before anything measures a position, and running it twice changes nothing — which is precisely what makes the pipeline idempotent |
| `_is_punct(word)` | true when no character in the token is a letter or digit |
| `_lemmatize(word)` | returns the word unchanged for now. Isolated in its own function so swapping in spaCy later touches one place. |
| `_tokenize(text)` | loops the pattern over the text, builds a `Token` per match |
| `normalize(doc)` | NFC the text, tokenise it, wrap it in a `NormalizedDocument`, copy `title`/`author`/`source_type` into metadata |

Note what `normalize` does **not** do: no `_strip_html` (HTML is stripped by `HTMLReader` at
ingestion, before NLP ever sees the text) and no `_normalize_whitespace` (forbidden — it is
exactly the rewrite described above).

---

## 8.5 `src/nlp_pipeline/segmentation.py`

**What it is:** splits text into sentences, keeping exact offsets. It was rewritten twice today,
and the reason is instructive.

**First version:** hand the whole text to pysbd, take its spans, trim whitespace. Ran the sample
article and got **12 sentences from 7**. Looking at the output:

```
1 'Sources say the minister ignored his own advisers, and critics claim the plan was'
2 'shameful from the start.'
```

pysbd treats a bare line break as a sentence boundary. A plain-text file wraps at a fixed width,
so one sentence arrives as two or three lines. Two things broke as a result: the sentence count
was nonsense, and — worse — the phrase `every\nsingle objection` straddled a wrap, so the
`unsupported_quantifier` detector never saw it. Rules run per sentence, so a phrase split across
two "sentences" is invisible.

**Second version** merged fragments back together. That fixed the wrap, and immediately broke the
opposite case: a headline with no full stop got glued to the paragraph below it, because a blank
line is a real boundary and the merge rule could not tell the difference. A test caught it.

**Third and current version:** split into paragraphs *first*, then segment inside each one.

| Code | What it does and why |
|---|---|
| `PARAGRAPH_BREAK = re.compile(r"\n[ \t]*\n\s*")` | a blank line — a newline, optional spaces/tabs, another newline. This is always a real boundary. |
| `SENTENCE_ENDINGS` | the punctuation that genuinely ends a sentence, including the versions with a closing quote or bracket (`."`, `?)`) |
| `pysbd.Segmenter(clean=False, char_span=True)` | `char_span=True` asks for positions, not just strings. **`clean=False` is not optional** — cleaning rewrites the text, and the offsets would then refer to a string we no longer have. |
| `_paragraphs(text)` | walks the blank-line matches and returns `(start, end)` for each block. Returns positions, never substrings, so nothing is copied or altered. |
| `_merge_wrapped_lines(paragraph, spans)` | joins a fragment to the previous one when the previous one does **not** end in sentence punctuation. Only the boundaries move; the text is untouched. |
| the offset arithmetic in `segment()` | pysbd works on one paragraph, so its positions are relative to that paragraph. `absolute_start = block_start + start` converts back to a position in the whole document. This is the single most error-prone line in the module. |
| the two `while … isspace()` loops | pysbd includes the whitespace *after* a sentence in its span; these pull the boundaries in so a quoted sentence has no stray spaces |
| `sentence_text = text[absolute_start:absolute_end]` | the text is sliced out of the **original document** using the final absolute offsets — so the invariant holds by construction rather than by hope |

Result on the sample article: 7 sentences, correct, and `every\nsingle objection` is now caught.

---

## 8.6 `conf/taxonomy_v1.yaml` — was 0 bytes, now the detector definitions

Five categories, not twenty-eight (R1, R5). Each had to be detectable from the text alone at
high precision; anything needing outside knowledge (strawman needs the opponent's real position,
cherry-picking needs the omitted data) is parked rather than done badly.

| Category | How it works | What was deliberately left out, and why |
|---|---|---|
| `loaded_language` | 20-word lexicon | `devastating`, `brutal`, `radical`, `corrupt` — all appear in plain factual reporting ("a devastating earthquake"). Including them would fire on neutral text. |
| `name_calling` | 17-word lexicon | `clown`, `snake`, `rat`, `puppet`, `extremist` — the first four have common literal meanings, the last is standard reporting vocabulary |
| `bandwagon` | 5 regexes | matched as **phrases** (`everyone knows`), because the signal is the construction, not the word "everyone" |
| `unsupported_quantifier` | 5 regexes | narrowed to explicit absolutes (`every single`, `without exception`, `all experts agree`) so that ordinary uses of "all" and "every" do not fire |
| `source_opaqueness` | 6 regexes | `officials said` excluded — that is standard sourced reporting. The target is attribution with no identifiable source at all. |

`default_threshold: 0.8`, not 0.5 — the precision end of the range offered by `claudenew.md`
§12.4, per R2. Regexes are written in **single quotes** in YAML, which is the literal form: no
escape processing, so `\b` and `\s` reach Python intact.

---

## 8.7 `src/taxonomy_tools/taxonomy_loader.py`

**Why load rather than pass the raw dict around:** so a malformed config fails here, at startup,
with a sentence you can read — instead of failing three modules later as a `KeyError`.

| Code | What it does and why |
|---|---|
| `@dataclass class Category` | one taxonomy entry as an object: `id`, `name`, `detector`, `base_confidence`, `terms`, `patterns` |
| `@dataclass class Taxonomy` | version, default threshold, and the list of categories, plus an `ids()` helper |
| `if not conf or "categories" not in conf` | catches the empty-file case, which is exactly what this file was until today |
| the `seen` set | rejects duplicate category ids. Two categories with the same id would silently overwrite each other in every downstream dict. |
| `detector not in VALID_DETECTORS` | only `lexicon` and `regex` exist; a typo like `lexicion` fails loudly |
| the `rules` check | a lexicon category with no `terms`, or a regex category with no `patterns`, is a config mistake and is refused |
| `float(...)` / `str(...)` casts | YAML will happily give you the string `"0.8"`; casting once here means nothing downstream has to wonder |

---

## 8.8 `src/nlp_pipeline/rules_engine.py`

**What it is:** runs the taxonomy over the text and produces evidence spans. About 55 lines.

| Code | What it does and why |
|---|---|
| `_compile_rules()` | compiles every pattern **once**, at construction, not per document. Compiling a regex inside the document loop would be the single biggest waste in the pipeline. |
| lexicon → `r"\b(?:" + "\|".join(re.escape(t) for t in cat.terms) + r")\b"` | all 20 words become **one** alternation regex, so the text is scanned once per category rather than 20 times |
| `re.escape(t)` | escapes any regex-special character in a term. Nothing in the current lexicon needs it; without it, adding a term containing `.` or `(` later would quietly break the pattern. |
| `\b` (word boundary) | this is what stops `liar` matching inside `familiar` and `ass` inside `assembly`. There is a test for it. |
| `re.IGNORECASE` | `Disastrous` at the start of a sentence must match `disastrous` |
| `rule_id` = `"loaded_language:lexicon"` or `"bandwagon:regex:0"` | stable identifier for the rule that fired. The trailing index means you can point at pattern 0 of 5 when one misbehaves. |
| `for sentence in doc.sentences:` | the outer loop. Rules are sentence-level constructs, and scanning per sentence gives `sentence_id` for free. |
| `if cat.base_confidence < self.threshold: continue` | the R2 gate. A category whose confidence sits below the threshold never emits anything. |
| `start = sentence.start_char + match.start()` | **the offset line.** `match.start()` is relative to the sentence; adding the sentence's own start converts it to a position in the whole document. |
| `text=doc.text[start:end]` | the quoted text is sliced from the **document** using the final offsets, not copied from the match object. If the arithmetic were ever wrong, the quote and the offsets would still agree with each other — so this is checked again in `PostProcessor.check_evidence`. |
| `spans.sort(key=lambda s: (s.start_char, s.end_char, s.rule_id))` | canonical order. Without it, output order would depend on the order categories happen to be listed in, and two runs could differ. |

---

## 8.9 `conf/scoring_v1.yaml` (was 0 bytes) and `src/nlp_pipeline/scoring_engine.py`

**The formula, in words:** add up the confidences of the evidence found for a category, divide by
document length so a long article is not penalised for being long, then squash into 0–1.

```
raw     = sum of the confidences of that category's evidence spans
density = raw / (word_count ** beta)
score   = 1 - exp(-lambda * density)
```

| Setting | Value | Meaning |
|---|---|---|
| `lambda` | 4.0 | how sharply density turns into a score. Hand-chosen — exactly the kind of number the research track (F2) is meant to *fit* rather than guess. |
| `beta` | 0.5 | length normalisation. `beta=0` is a raw count (long articles always score higher); `beta=1` is pure density (one loaded word in a two-line article dominates); 0.5 sits between. |
| `round_places` | 6 | round before writing, so two runs are byte-identical rather than differing in the last float digit |
| `expose_composite` | false | R3 |
| `category_weights` | all 1.0 | any other value would be invented |

**Engine walkthrough:**

| Code | What it does and why |
|---|---|
| `_score_one(raw, word_count)` | the formula above. `max(word_count, 1)` guards against dividing by zero on an empty document. |
| `if raw <= 0: return 0.0` | no evidence, no score — and it avoids `exp(-0)` returning a non-zero-looking 0.0 |
| `for cat in self.taxonomy.categories:` | **every** category gets an entry, including ones that found nothing. A stable output shape is far easier to validate, diff and store than one whose keys vary per document. |
| `round(..., self.round_places)` | applied to both `raw` and `score` |
| `composite=None if not self.expose_composite` | the headline number stays off |
| `_composite()` | only reachable if someone flips the flag. It is a plain **mean**, not the noisy-OR `1 − Π(1−v)` from the original design — that formula assumes the categories are statistically independent, and loaded language / name-calling / fear appeals co-occur heavily, so it saturates towards 1 and ordinary emotive journalism reads as propaganda. This is the F1 bug from the research track, avoided rather than shipped. |

The scoring engine **never looks at the text**. It sees only the spans. That is what makes the
numbers reconstructible: anyone holding the output can recompute every score by hand from the
findings list. There is a test that does exactly that.

---

## 8.10 `data_schema/output_schema.json` and `input_schema.json`

Both were one-line placeholder strings. They are now real JSON Schema (draft 2020-12) documents.

A *JSON Schema* is a description of what a valid JSON document looks like, written in JSON. A
library reads the schema and checks a document against it, so the contract is enforced by a file
rather than by everyone remembering.

**The output record:**

```
schema_version   "1.0.0"
document_id      64 hex characters (enforced by a regex in the schema)
source           {type, title, author, language}
config_hashes    {pipeline_hash, taxonomy_hash, scoring_hash} — 64 hex chars each
stats            {char_count, word_count, sentence_count}
findings         [{category, rule_id, sentence_id, text, start_char, end_char, confidence}]
category_scores  {category: {count, raw, score, calibrated}}
composite        null
notes            [strings]
```

Two decisions worth knowing:

- **`"additionalProperties": false`** on the objects. An unexpected field is an error, not a
  shrug. If a stage starts emitting something new, this catches it here instead of confusing the
  backend later.
- **There is no timestamp anywhere in the record.** This is the one that matters. The pipeline
  promises that the same article produces the same bytes on every run, and a clock reading breaks
  that on the very first run. Ingestion time still exists on the `InternalDocument` — it just
  does not reach the analysis output. There is a test asserting the words "timestamp",
  "ingested_at", "generated_at" and "processed_at" appear nowhere in the JSON.

`input_schema.json` describes a pushed dict payload (`text` required, everything else optional).
File paths and raw strings do not go through it.

---

## 8.11 `src/nlp_pipeline/postprocessing.py`

| Code | What it does and why |
|---|---|
| `SCHEMA_PATH = Path(__file__).resolve().parents[2] / "data_schema" / ...` | `__file__` is this file's path; `.parents[2]` climbs `nlp_pipeline` → `src` → repo root. Works regardless of where you run Python from — no hard-coded `C:\Projects\...` anywhere. |
| loading the schema in `__init__` | read once, not per document |
| `build_output(scored, doc, config_hashes)` | assembles the dict. Nothing is computed here; it is pure re-shaping. |
| the `findings` list comprehension | one dict per `EvidenceSpan`, field for field |
| `sorted(scored.category_scores.items())` | categories written in alphabetical order, so the serialised bytes do not depend on dict insertion order |
| `_round_floats(record)` at the end | one pass over the finished record, so no float anywhere escapes unrounded |
| `validate(record)` | `iter_errors` collects **all** violations; they are sorted by path and the first is reported with its location, e.g. `output failed schema check at stats/word_count: -1 is less than the minimum of 0` |
| `to_json(record)` | `sort_keys=True`, `indent=2`, `ensure_ascii=False`. `sort_keys` is what makes the byte comparison in the determinism test meaningful. |
| **`check_evidence(record, text)`** | the important one. It re-slices the original text at every finding's offsets and compares to the quoted string. This is the project's central promise, checked on every single run rather than assumed. |

---

## 8.12 `src/io_adapters/file_readers.py` — two surgical changes

This is inherited 669-line ChatGPT code. Under R12 it is reference material, but two things had
to change before anything could run at all.

**1. It could not be imported.** The top of the file imported `magic`, `pdfplumber`, `fitz`,
`docx`, `bs4`, `markdown`, `pandas`, `PIL`, `pytesseract`, `sqlalchemy` and `pymongo` — at module
level. That means reading a plain `.txt` file required installing roughly 2 GB of dependencies,
and `python-magic` on Windows needs a separate binary that is a well-known install headache.

Fix, in two parts:

- `import magic` → **removed**. It was used for one thing, `mime_type`, and the standard library's
  `mimetypes.guess_type(filename)` does the same job from the extension. A dependency deleted
  rather than satisfied.
- Every other heavy import **moved inside the method that uses it**. `import pdfplumber` now sits
  on the first line of the PDF branch. Python caches imports, so the cost is paid once, on first
  use, by whoever actually reads a PDF. A `.txt` file now needs nothing beyond the stdlib and
  `charset_normalizer`.

**2. Constructing a reader created a directory.** `BaseReader.__init__` called
`self.output_dir.mkdir(...)`, so simply building the reader registry left an empty
`./jsonl_output/` folder in whatever directory you happened to run from. The `mkdir` moved into
`write_to_jsonl`, where the directory is actually needed.

---

## 8.13 `src/io_adapters/input_router.py` — rewritten (this was bug 1)

**What was there:** lines 1–622 were the entire old implementation, commented out. Line 623 began
a new class the previous session had started — `def __init__(self,config:Dict[str,Any],)` — which
is a syntax error, so the file could not be imported. The original bug (readers stored as the
*string* `"TxtReader()"`, and `_handle_file_path` calling `_mock_file_read` instead of a real
reader) is why nothing in this repo had ever read a real file.

**Rewritten from scratch, ~200 lines.** The division of labour, which the old version got wrong:
readers return plain dictionaries; only `_to_internal_document` builds an `InternalDocument`.
Readers never build documents, and the router never parses files.

| Code | What it does and why |
|---|---|
| `EXTENSION_MAP` | `".txt" → (TxtReader, SourceType.FILE_TXT)` and eleven more. One table, so adding a format is one line. |
| `TEXT_KEYS = ("raw_content", "full_raw_text", "extracted_text", "plain_text", "text", "content")` | the readers were each written separately and each put the extracted text under a different key — `TxtReader` uses `raw_content`, `PDFReader` and `DocsReader` use `full_raw_text`, `HTMLReader` and `XMLReader` use `extracted_text`, `MarkdownReader` uses `plain_text`. This tuple is the one place that inconsistency is absorbed. |
| `__init__` building `self.readers` | **the actual bug fix.** One real instance per reader class, created once, stored in a dict keyed by the class. |
| `route_push_input(payload)` | dispatch on type: an `InternalDocument` passes through, a `Path` or an existing file path is read, `bytes` are decoded, a `dict` becomes a payload, anything else is text |
| `if len(payload) < 260 and candidate.is_file()` | a string is treated as a path **only if a file of that name actually exists**. The length check avoids handing a 5000-character article to the filesystem. 260 is the classic Windows path limit. |
| `route_pull_source()` | reads `enabled`, `path` and `glob_pattern` out of `pipeline_v1.yaml` and walks the directory |
| `sorted(folder.glob(pattern))` | the order the filesystem returns files in is not guaranteed. Sorting makes a directory run reproducible. |
| `_extract_text(raw_record)` | tries `TEXT_KEYS` in order; then falls back to CSV/JSONL row extraction using the column named in config; then a JSON field. Raises `NoTextFoundError` rather than returning an empty string — a silent empty document would be scored as clean. |
| `_configured_text_key()` | reads `csv.text_column` / `json.text_field` from config. The column is **never guessed**, because guessing wrong is a silent data bug. |
| `_cell_from_row(row, column)` | CSV rows are flat dicts; JSONL rows arrive wrapped as `{'line_number': n, 'data': {...}}`. Handles both. |
| `unicodedata.normalize("NFC", text)` in `_to_internal_document` | NFC applied **once**, here at the boundary. Every character offset the pipeline ever reports is measured against this exact string. |
| `document_id = _hash_to_document_id(text)` | the id is a hash of the text itself. Same article, same id, on any machine, with no database and no counter. Consequence, chosen deliberately: two identical articles from different sources collapse into one document. |
| `source_metadata` built by excluding `TEXT_KEYS` | everything the reader found *except* the text — file size, encoding, line endings, hashes — is kept as metadata |

---

## 8.14 `src/main.py` — rewritten

The old file had a `\N` syntax error from a Windows path literal (already fixed in a prior
session), a `build_services` that built four objects and returned none of them, and imports of
fourteen stub modules, seven of them frozen under R7.

| Code | What it does and why |
|---|---|
| `ROOT = Path(__file__).resolve().parent.parent` | derived from the file's own location. No absolute paths anywhere. |
| `sys.path.insert(0, str(ROOT / "src"))` | lets `python src/main.py` work without installing the package first |
| the `# noqa: E402` comments | tell a linter that imports below the `sys.path` line are intentional, not sloppy |
| `load_yaml(path)` | `yaml.safe_load` — `safe_load`, not `load`, because `load` can construct arbitrary Python objects from a YAML file |
| `or {}` in `load_yaml` | an empty YAML file parses to `None`; this turns it into an empty dict |
| `class PipelineRunner` | holds every stage. Built **once**, reused per document — the regexes, the schema and the segmenter are all expensive to construct and cheap to reuse. |
| the `seed is None` check | `pipeline_v1.yaml` used to say `seed: #idk`, which YAML parses as `None`. Now it is 42, and this catches a regression. |
| `_compute_config_hashes(...)` in `__init__` | computed once, stamped on every record |
| `process_document(raw_input)` | the seven-line spine of the whole system: route → normalize → segment → classify → score → build → validate |
| the `check_evidence` call | belt and braces. Every run re-reads every quote out of the article. |
| `run_pipeline()` | processes everything the pull source offers |
| `main(argv)` | `--input` (file or text), `--out` (file), `--conf` (config dir) |
| `json.dumps(..., sort_keys=True)` | again the byte-stability requirement |

---

## 8.15 `tests/` — six files, 43 tests, all passing

Previously six empty stub files.

**`conftest.py`** — pytest's shared-setup file. It puts `src/` on the path and defines fixtures
(a *fixture* is a named object pytest builds and hands to any test that asks for it by parameter
name). Two text constants live here:

- `NEUTRAL_TEXT` — a dry factual paragraph about the Forth Bridge. Contains "All of the original
  rivets were driven by hand" specifically to check that an ordinary "all" does not trip
  `unsupported_quantifier`.
- `LOADED_TEXT` — one example of every category, so a broken detector shows up as a failure
  rather than as silence.

| File | Tests | The ones that matter |
|---|---|---|
| `test_preprocessing.py` | 5 | `test_text_is_not_rewritten` — passes `"  The  MAYOR  said…  "` through and asserts the output is character-for-character identical. `test_token_offsets_point_at_the_real_word` slices the text at every token's `idx`. |
| `test_segmentation.py` | 6 | the offset invariant on every sentence; `Dr. Smith … Mon.` must not split (2 sentences, not 5); a hard-wrapped sentence must be 1; a blank line must still separate — **this last one caught the second version of the segmenter and forced the rewrite** |
| `test_rules_engine.py` | 11 | **`test_nothing_fires_on_neutral_text`** is the R2 gate: no detector may fire on the Forth Bridge paragraph. `test_word_boundaries_are_respected` checks `familiar` / `assembly` do not match `liar` / `ass`. Every category is parametrised so each must be able to fire. |
| `test_scoring_engine.py` | 6 | **`test_the_number_can_be_recomputed_from_the_evidence`** recomputes every score by hand from the spans and compares. That property — reconstructibility — is the point of the design. |
| `test_output_schema.py` | 8 | schema validation; every finding quoted back out of the text; `test_no_timestamp_anywhere_in_the_record`; two negative tests (a tampered record must be rejected, a tampered quote must be caught) |
| `test_determinism.py` | 7 | two runs in-process, **and two runs in separate interpreter processes** via `subprocess` comparing raw bytes — a single test process cannot fake that |

`pytest.ini` was added: `testpaths = tests`, `pythonpath = src tests`.

The docstring at the top of `test_determinism.py` states the thing that is easy to get wrong:
this proves the pipeline is **reproducible**, not that it is **correct**. A system can be
reproducibly wrong. Determinism is an audit property (R6).

---

## 8.16 Bug list from `CLAUDE.md` — status

| # | Bug | Status |
|---|---|---|
| 1 | `input_router.py` never calls the real readers | **fixed** — file rewritten, readers instantiated in `__init__`, `_mock_file_read` gone. Proven on a real `.txt`. |
| 2 | `from sklearn.externals import joblib` | **fixed** → `import joblib`. (File is still a stub and frozen under R7; the import would just have failed on the day it was unfrozen.) |
| 3 | duplicate `io_adapters/shared_types.py` shadowing the real `InternalDocument` | **fixed** — file deleted |
| 4 | `seed: #idk` parses as `None` | already fixed to `42`; `main.py` now also raises a clear error if it goes missing again |
| 5 | `features.py` typos `Bais` / `Sentiment_Subjecivity` | **fixed** → `Bias` / `Sentiment_Subjectivity` |

Also cleaned up:

- `requirements-dev.txt` — `docx==0.2.4` (a different, broken package) → `python-docx`; the
  duplicate line removed; `python-magic-bin` removed with a comment saying stdlib `mimetypes`
  replaced it.
- `.gitignore` — added `.venv/`, `tree.txt`, `data/processed/`, `jsonl_output/`. `tree.txt` was
  removed from git tracking.

---

## 8.17 Terminal log

Every command run this session, in order. `PY` is `./.venv/Scripts/python.exe`.

| # | Command | Purpose / result |
|---|---|---|
| 1 | `find . -type f` | survey the repo — 74 files |
| 2 | `python --version` / `py -0p` | 3.12.1 on PATH; 3.10 available via the launcher |
| 3 | `py -3.10 -m venv .venv` | created the environment → Python 3.10.10 |
| 4 | `PY -m pip install pyyaml pysbd jsonschema numpy pytest charset-normalizer` | six packages, not 98 |
| 5 | `PY -c "…"` after `shared_types.py` | slice invariant holds |
| 6 | `PY -c "…"` after `deterministic_utils.py` | **failed** — `NameError` on `import *`, because `import *` skips underscore names. Re-run with explicit imports: passed. |
| 7 | `PY -c "…"` after `preprocessing.py` | tokens `['The','mayor',"didn't",'resign','.']`, all offsets correct, NFC idempotent |
| 8 | `PY -c "…"` after `segmentation.py` | `Dr.` and `Mon.` handled; offsets exact |
| 9 | `PY -c "…"` on `taxonomy_v1.yaml` | all 5 categories parse, all 16 regexes compile |
| 10 | `PY -c "…"` on the rules engine | 4 spans on a 3-sentence sample; the neutral third sentence produced nothing |
| 11 | `PY -c "…"` on the scoring engine | per-category scores 0.27–0.64, composite `None` |
| 12 | `PY -c "…"` on both JSON schemas | both are valid draft-2020-12 schemas |
| 13 | a `cat > input_router.py` heredoc | **failed** — bash quoting error, nothing written. Switched to writing the file directly. |
| 14 | `PY /tmp/check_router.py` | first real file read: `fdea443b…`, 594 chars, 99 words |
| 15 | `ls -d jsonl_output` | found the stray directory created by `BaseReader.__init__`; patched, removed, confirmed gone |
| 16 | `PY src/main.py --input data/raw/sample_article.txt` | **first end-to-end run.** 8 findings, valid JSON. |
| 17 | run twice with `--out`, then `diff` | **byte-identical** |
| 18 | `PY /tmp/seg_check.py` | exposed the wrap bug: 12 sentences from 7 |
| 19 | after the merge fix: `main.py` twice + `diff` | 7 sentences, 9 findings — `every\nsingle objection` now caught — still byte-identical |
| 20 | `PY -m pytest` | **42 passed, 1 failed** — `test_blank_line_still_separates` |
| 21 | after the paragraph-first rewrite: `PY -m pytest` | **43 passed** |
| 22 | patches to `ml_classifier.py`, `features.py`, `requirements-dev.txt`, `.gitignore` | bugs 2 and 5 closed |

---

## 8.18 What is deliberately not done

- **No composite score.** R3. `composite` is `null` and `calibrated` is `false` everywhere.
- **`lambda = 4.0` and `beta = 0.5` are guesses.** Honest ones, labelled as such in the config
  comments, but guesses. Fitting them is research-track work (F2).
- **No quote handling in the detectors.** If an article quotes someone *else* using loaded
  language, the outlet is not being loaded — but the rules engine currently counts it. A real
  precision issue, deliberately deferred: fixing it needs quotation-span detection, which is a
  module of its own.
- **`lemma` equals `lower`.** No lemmatiser installed. Isolated in `TextProcessor._lemmatize` so
  swapping in spaCy touches one function.
- **Only the local-files pull source works.** API, Elasticsearch, Kafka, S3, Redis and the scraper
  are all `enabled: false` and frozen under R7.
- **Only `.txt` has actually been exercised end to end.** The other eleven extensions are wired
  into `EXTENSION_MAP` and their readers now import cleanly, but reading a real PDF or `.docx`
  needs `pip install pdfplumber python-docx` first, and none has been run.
- **Nothing is stored.** `storage_clients.py` is still a stub — output goes to stdout or to the
  file named by `--out`. No Bronze/Silver/Gold Parquet yet; that is Phase 1.

---

## 8.19 Where to pick up

Phase 0 is done by its own definition: `python src/main.py --input article.txt` emits schema-valid
JSON with verbatim spans and offsets, two consecutive runs are byte-identical, and every detector
has a passing false-positive test.

Next, in order:

1. **Run it on a real article of your own** — paste a news piece into `data/raw/` and look at what
   fires and what it misses. Every threshold in the system is currently unvalidated, and this is
   the cheapest way to start seeing where it is wrong.
2. **R8 literature review.** Still not started, still gates the entire research track, still just
   reading. It can invalidate P1 outright, so doing it before writing research code is the whole
   point.
3. **Phase 1:** `storage_clients.py` (JSONL first, Parquet after), then `api/service.py`.

To run anything after a restart:

```
.venv\Scripts\python.exe src\main.py --input data\raw\sample_article.txt
.venv\Scripts\python.exe -m pytest
```

---

# 9. Build log — Phase 1 (same session, 2026-08-21)

Phase 0 made the pipeline *work*. Phase 1 makes it *usable by something other than a person at a
terminal*: results can be stored, and a backend can call it over HTTP. Test count went 43 → 61.

Two Phase 1 items from `CLAUDE.md` were **deliberately not built** — reasons in §9.5.

---

## 9.1 `src/io_adapters/storage_clients.py` — rewritten

**What was there:** `ParquetWriter`, `RedisWriter`, `LocalStorageWriter`, `StorageClientFactory`
and `JSONLWriter`, every method `pass`, with `import pandas` and `import redis` at the top so the
file could not even be imported without both installed.

**What it is now:** three writers and a factory. `RedisWriter` was **deleted** (Redis is frozen
under R7) and `LocalStorageWriter` was **deleted** as well — it was the same idea as `JSONWriter`
under a vaguer name. Two classes removed rather than filled in.

**The rule the module obeys:** a writer takes the finished record and puts it somewhere. It never
changes it. If a writer reshaped the data, two storage backends would end up holding different
answers to the same question.

| Code | What it does and why |
|---|---|
| `class JSONLWriter` | one JSON object per line. Append-friendly, greppable, opens in a text editor, and needs nothing beyond the standard library — which is why it is now the default. |
| `mode = "a" if (self.append or self._started) else "w"` | the fiddly bit. The **first** write of a run truncates the file (unless `append: true` in config); every write **after** that in the same run appends. Without the `_started` flag, a batch of 50 records would leave a file containing exactly one. |
| `sort_keys=True` in the dump | same reason as everywhere else — the same record must serialise to the same bytes |
| `class JSONWriter` | one file per document, named from the first 16 characters of the document id. Sixteen hex characters is plenty to tell documents apart and keeps the filename readable. |
| `class ParquetWriter` | columnar storage, worth it once you have thousands of records to query rather than read |
| `_flatten(record)` | Parquet columns hold single values, not nested structures, so `findings` and `category_scores` are stored as JSON strings in one column each. The alternative — one row per finding — makes the document-level scores repeat on every row. |
| `import pyarrow` inside `save_batch` | pyarrow is large and nothing else needs it. Not installed in `.venv`; the writer will raise `ImportError` if used, which is the right failure. |
| `ParquetWriter.write` calls `save_batch([record])` | Parquet writes whole files, not lines. Writing one record means rewriting the file, which is exactly why this format is for batches. |
| `class StorageClientFactory` | a dict from the `output.type` string to the class. Adding a backend is one dict entry. |
| the `if kind not in cls.WRITERS` check | a typo in the config fails at startup with the list of valid options, not silently |

**Config change** in `conf/pipeline_v1.yaml`: `output.type` was `"parquet"`, which would have
crashed on first use because pyarrow is not installed. Now `"jsonl"`, with `path: data/processed`
and `file: records.jsonl`.

**Wired into `main.py`:** a new `--save` flag. Without it nothing is written to storage (the JSON
still goes to the screen or to `--out`); with it, `StorageClientFactory.create(...)` builds the
writer named in config and `save_batch` runs.

---

## 9.2 `src/api/models.py` — rewritten

**What was there:** four class names with `pass` bodies.

**What it is now:** nine pydantic models. A *pydantic model* is a class that declares field names
and types; pydantic checks incoming JSON against them and rejects anything that does not fit
**before** the request reaches any pipeline code. A caller sending a number where text belongs
gets a clear `422 Unprocessable Entity` rather than a crash halfway through segmentation.

| Model | Purpose |
|---|---|
| `AnalyzeRequest` | `text` (required, `min_length=1`), plus optional `title`, `author`, `language` |
| `Finding` | one evidence span, field for field as it appears in the output record |
| `CategoryScore` | `count`, `raw`, `score`, `calibrated` |
| `DocumentStats`, `DocumentSource` | the two small nested blocks |
| `AnalyzeResponse` | the whole record, with `composite: Optional[float] = None` |
| `BatchAnalyzeRequest` / `BatchAnalyzeResponse` | a list of each |
| `HealthResponse` | status, taxonomy version, category list, config hashes |

**Worth being clear about which contract is authoritative.** `data_schema/output_schema.json` is
the contract of record — it is what `PostProcessor.validate` enforces on **every** run, HTTP or
not. These pydantic classes duplicate that shape so FastAPI can publish it as OpenAPI
documentation at `/docs`. If the two ever disagree, the JSON Schema wins and the pydantic model
is the thing that is out of date.

---

## 9.3 `src/api/service.py` — rewritten

**What was there:** imports of `build_services` and `process_document` (a function that no longer
exists in that form) and `def create_app(): pass`.

| Code | What it does and why |
|---|---|
| `create_app(conf_dir=None)` | a factory rather than a bare module-level app, so tests can build an app pointed at a different config directory |
| `runner = PipelineRunner()` **inside** `create_app`, before the routes | built **once**, at startup, reused for every request. Building it per request would recompile every regex and reread the JSON schema on each call, and would re-seed the random generators mid-flight. |
| `GET /health` | returns the taxonomy version, the category list and the config hashes. Not just "is it up" — it tells a caller *which configuration* is answering, which matters when results have to be reproducible. |
| `POST /analyze` | `request.model_dump()` turns the pydantic object back into a plain dict, which is what `route_push_input` expects |
| `payload["source_type"] = "api_rest"` | the router treats a bare string as a file path when a file of that name exists. Wrapping HTTP text in a dict with an explicit source type removes that ambiguity entirely. |
| `except IngestionError → 400` | the caller sent something unusable; that is their problem |
| `except ValueError → 500` | the pipeline produced something that failed its own schema or evidence check; that is our problem. Splitting the two means the status code actually tells the caller who has to fix something. |
| `POST /analyze/batch` | loops; refuses an empty list with a 400 rather than returning an empty success |
| `app = create_app()` at module level | uvicorn needs a module-level object to serve |

Run it with:

```
.venv\Scripts\python.exe -m uvicorn api.service:app --app-dir src --reload
```

Installed for this: `fastapi`, `uvicorn`, `httpx` (httpx only so the tests can call the app).

---

## 9.4 New tests — 18 of them

**`tests/test_storage_clients.py`** (9 tests). A fixed `RECORD` constant stands in for pipeline
output, so these tests do not need the pipeline at all.

- round-trip: what comes back out of the JSONL file `==` what went in
- `test_jsonl_appends_within_one_run` — three records, three lines. This is the test that would
  have caught the truncation bug if the `_started` flag had been forgotten.
- `test_jsonl_starts_fresh_on_a_new_run` — a second `JSONLWriter` truncates
- `test_writing_twice_produces_identical_bytes` — determinism, at the storage layer
- three factory tests: right class per config string, defaults to JSONL, refuses nonsense
- `test_parquet_flattening_keeps_everything` — checks `_flatten` without needing pyarrow installed

**`tests/test_api.py`** (9 tests). Uses `fastapi.testclient.TestClient`, which calls the app
in-process — no server, no port, no network.

- `pytest.importorskip("fastapi.testclient")` at the top: if FastAPI is not installed the whole
  file skips instead of erroring, so the core suite still runs on a minimal environment
- `/health` reports the taxonomy and a 64-character config hash
- **offsets survive the round trip** — every finding is sliced back out of the text the client
  sent
- neutral text returns an empty findings list
- the same request twice returns the identical body
- empty text and missing text both get **422** (pydantic rejects them, the pipeline is never
  reached) — while an empty *batch* gets **400**, because that check is ours
- no composite and nothing calibrated over HTTP either

---

## 9.5 Phase 1 items deliberately not built

Two things `CLAUDE.md` lists under Phase 1 were skipped on purpose. Both are written down here
rather than quietly dropped.

**`ontology_graph.py` — a hierarchy over five flat categories.** The point of an ontology graph is
multi-label classification over a *tree*: "name-calling is a kind of ad-hominem, which is a kind
of fallacy of relevance". `taxonomy_v1.yaml` has five sibling categories and no tree. Building the
graph now means building the machinery for a structure that does not exist yet, and it would have
to be rebuilt the moment the real hierarchy arrives. It belongs with `taxonomy_v2`.

**`features.py` Phase-1 layers (structural, lexical, entity, sentiment).** Nothing consumes them.
`RuleEngine` reads the text and the taxonomy; `ScoringEngine` reads only the evidence spans.
Adding four feature layers today produces four classes that compute numbers nobody looks at — and
the entity layer needs spaCy plus a model download, and the sentiment layer needs a lexicon that
would itself need the R2 false-positive treatment. They become worth building when there is a
consumer: the ML classifier (Phase 2, gated on a labelled evaluation set).

The class-name typos in `features.py` were still fixed (`Bais` → `Bias`), because that costs
nothing and stops the typo from being copied into real code later.

---

## 9.6 Terminal log — Phase 1

| # | Command | Purpose / result |
|---|---|---|
| 23 | `git add -A && git commit` | Phase 0 committed as `8c5c9a8`, author `Sarva Advaith Narayana`, no Claude trailers (R16) |
| 24 | `PY -m pip install fastapi uvicorn httpx` | fastapi 0.141.1, uvicorn 0.52.4, httpx 0.28.1, pydantic 2.13.4 |
| 25 | edited `conf/pipeline_v1.yaml` output block | `type: parquet` → `jsonl`; parquet would have crashed on first use, pyarrow is not installed |
| 26 | `PY src/main.py --input … --save` | `stored: data\\processed\\records.jsonl`, one line, valid JSON |
| 27 | `PY -m pytest` | **61 passed** |

---

## 9.7 Where things stand

| | Phase 0 | Phase 1 |
|---|---|---|
| Pipeline runs end to end | yes | yes |
| Byte-identical reruns | yes | yes, including at the storage layer |
| Results can be stored | no | JSONL, JSON, Parquet (pyarrow required) |
| Callable by a backend | no | `/health`, `/analyze`, `/analyze/batch` |
| Tests | 43 | 61 |

**Still true and still the most important caveat:** the scores are uncalibrated. Nothing in this
system has been measured against labelled data. It reports how much evidence its five detectors
found, using thresholds chosen by hand. That is a useful, auditable thing — and it is not the same
as knowing how biased an article is.

**Next, unchanged from §8.19:** run it on real articles you have an opinion about, then the R8
literature review. Phase 2 (ML classifier, hybrid router, composite scoring, feature layers) stays
gated on a labelled evaluation set — building it before that measurement exists is how you get a
confident number nobody can defend.
