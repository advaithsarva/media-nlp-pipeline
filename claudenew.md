# NLPpipline — Consolidated Design & Research Reference

> **What this is.** Everything of substance from four ChatGPT conversation exports, merged,
> de-duplicated and reorganised by topic. Chat noise (greetings, "just tell me which one you
> want next", repeated file trees, environment-install trial-and-error, git command loops) has
> been removed; every design decision, formula, schema, code template, lexicon, threshold and
> rationale has been kept.
>
> **Sources merged**
> | Source file | Date range | What it contributed |
> |---|---|---|
> | `Project approach and role.md` | Nov 28 → May 23 | Role definition, team integration, repo structure, environment/Docker/CI, IO-adapter architecture, config design, OOP design, build discipline, ES vs FAISS, final project self-description |
> | `NLP - NLP pipeline creation request.md` | Dec 16 | "Production-Ready NLP Pipeline for Media/News Bias and Fallacy Analysis" — Bronze/Silver/Gold architecture, 13 feature layers, fallacy detection, taxonomy + scoring, serving, QA strategy |
> | `NLP - Data analysis fallacy check.md` | Dec 4 → Dec 6 | Per-fallacy mathematics, the 33-characteristic detection catalog, and the full module-by-module "Media Bias and Propaganda Detection System Design" (math, calibration, validation, integration, DB schema, real-time vs batch) |
> | `NLP - Score to NLP model.md` | — | Evidence-grounded scoring & explanation ("no claim without evidence") |
>
> Ordering note: the design evolved over time. Where two sources disagree, the **later /
> more specific** decision is marked as authoritative and the earlier one is kept as history.
>
> ⚠ **This document is a catalogue of what the system *could* be — it is not a build plan.**
> Following it literally produces a 3–5 engineer-year build that never ships. The binding
> decisions **R1–R7 in `CLAUDE.md`** override anything here that contradicts them, in
> particular: build the vertical slice first (R1); precision over recall, τ = 0.8 (R2); do not
> expose uncalibrated composite scores (R3); evidence spans are mandatory (R4); only the
> admitted detector list gets built (R5); determinism ≠ correctness (R6); accelerators, Kafka,
> Spark, Ray, ES and FAISS stay frozen (R7).

---

## Table of contents

1. [What the project is](#1-what-the-project-is)
2. [Roles, deliverables and team integration](#2-roles-deliverables-and-team-integration)
3. [System architecture](#3-system-architecture)
4. [Determinism contract](#4-determinism-contract)
5. [Data contracts and schemas](#5-data-contracts-and-schemas)
6. [Configuration design](#6-configuration-design)
7. [Ingestion layer — IO adapters](#7-ingestion-layer--io-adapters)
8. [Preprocessing](#8-preprocessing)
9. [Segmentation](#9-segmentation)
10. [Argument mining](#10-argument-mining)
11. [Feature extraction — the 13 layers](#11-feature-extraction--the-13-layers)
12. [Logical fallacy detection](#12-logical-fallacy-detection)
13. [Propaganda and rhetorical technique detection](#13-propaganda-and-rhetorical-technique-detection)
14. [Linguistic bias analysis](#14-linguistic-bias-analysis)
15. [Factuality, truthiness and data accuracy](#15-factuality-truthiness-and-data-accuracy)
16. [Entity-level sentiment and bias](#16-entity-level-sentiment-and-bias)
17. [Stance detection](#17-stance-detection)
18. [Structural and syntactic analysis](#18-structural-and-syntactic-analysis)
19. [Framing theory and moral foundations](#19-framing-theory-and-moral-foundations)
20. [Taxonomy classification and feature gating](#20-taxonomy-classification-and-feature-gating)
21. [Scoring engine — all mathematics](#21-scoring-engine--all-mathematics)
22. [Evidence-grounded scoring and explanation](#22-evidence-grounded-scoring-and-explanation)
23. [Embeddings and vector search](#23-embeddings-and-vector-search)
24. [Output contract and postprocessing](#24-output-contract-and-postprocessing)
25. [Storage, versioning and database schema](#25-storage-versioning-and-database-schema)
26. [API and serving](#26-api-and-serving)
27. [Batch processing, Airflow and big data](#27-batch-processing-airflow-and-big-data)
28. [Deployment, Docker, CI/CD](#28-deployment-docker-cicd)
29. [QA and testing strategy](#29-qa-and-testing-strategy)
30. [Build order and coding discipline](#30-build-order-and-coding-discipline)
31. [Decisions log](#31-decisions-log)
32. [Accelerators — C++ and CUDA](#32-accelerators--c-and-cuda)
33. [Master file-by-file blueprint](#33-master-file-by-file-blueprint)
34. [Reader raw-record contracts](#34-reader-raw-record-contracts)
35. [InputRouter — production implementation details](#35-inputrouter--production-implementation-details)
36. [Config-driven multi-source ingestion](#36-config-driven-multi-source-ingestion)
37. [Elasticsearch vector search — capability boundaries](#37-elasticsearch-vector-search--capability-boundaries)
38. [The employer-facing pipeline summary (v2.0)](#38-the-employer-facing-pipeline-summary-v20)
39. [IO adapter design — evolution and rejected alternatives](#39-io-adapter-design--the-evolution-and-the-rejected-alternatives)
40. [Deep IO adapter pseudocode](#40-deep-io-adapter-pseudocode)
41. [Boundary rules and the architecture audit](#41-boundary-rules-and-the-architecture-audit)
42. [Where big-data engineering actually appears](#42-where-big-data-engineering-actually-appears)
43. [Type and identifier registry](#43-type-and-identifier-registry)

*Appendices: [A Known bugs](#appendix-a--known-bugs-to-fix-before-building-new-code) ·
[B Fallacy list](#appendix-b--the-15-logical-fallacy-types-canonical-list) ·
[C Propaganda list](#appendix-c--the-13-propaganda--rhetorical-techniques-canonical-list) ·
[D Visualization plans](#appendix-d--visualization-and-dashboard-plans) ·
[E Learning path](#appendix-e--learning-path-grouped-with-search-terms)*

---

## 1. What the project is

A confidential **media-analysis system built under NDA**. It ingests media content (news
articles, reports, documents), processes the text, tags sentences against a predefined internal
taxonomy, scores the article with an internally defined scoring matrix, and returns
**deterministic JSON** — the same input always producing the same output. A frontend renders
highlights, labels and scores; QA verifies reproducibility.

Formally: a **Media Objectivity / Topic Classification + Scoring Platform**, whose purpose is
to detect **rhetorical fallacies, propaganda techniques and bias** in news text and produce
structured output that highlights manipulative content with bias/fallacy scores.

By the end of the design conversations the project had grown into an
**Enterprise Hybrid NLP Intelligence Pipeline**:

```
PDF / DOCX / APIs / Kafka / ES / S3 / Web
   ↓  Enterprise Ingestion Layer
   ↓  InternalDocument Contract
   ↓  Deterministic NLP Pipeline
   ↓  Hybrid Rules + ML Classification
   ↓  Embeddings + Vector Search
   ↓  Structured Intelligence
   ↓  JSON / Parquet / ES / Redis
```

One-sentence description:

> A scalable enterprise-grade NLP platform that ingests multi-source data, normalizes it into a
> unified document abstraction, processes it through deterministic and ML-enhanced NLP
> pipelines, and supports semantic retrieval, taxonomy classification, and distributed
> orchestration.

The project's defining shift: it stopped being *"build an NLP model"* and became
*"build an AI system."* Most student NLP projects are `PDF → preprocess → model → output`;
this one is a platform.

Two priorities dominate every design decision:

- **Traceability** — every result can be traced through versioned data and logs.
- **Determinism** — the same input yields identical output on every run.

---

## 2. Roles, deliverables and team integration

### 2.1 Data / NLP Engineer — "the brain of the system"

Without this pipeline the system cannot score or analyze anything.

| # | Responsibility |
|---|---|
| A | Build the entire NLP pipeline: sentence segmentation, cleaning & normalization, tokenization, rule-based / hybrid-ML classifiers, mapping text → predefined taxonomy, scoring logic |
| B | Ensure determinism: set random seeds, use deterministic algorithms, prefer rule-based logic, no stochastic drift between runs |
| C | Power backend & frontend: the pipeline outputs the JSON that backend exposes and frontend renders |
| D | Maintain & evolve the taxonomy: add categories, adjust rules, keep category definitions tight |
| E | Deliver structured output: JSON, sentence-level metadata, category IDs, position offsets for highlighting |

**Deliverables**

1. A fully functional NLP pipeline as an importable Python package.
2. A deterministic category-mapping system — rule-based heuristics, pattern matching, regex,
   lexicons, syntactic cues.
3. A scoring engine that takes category outputs, applies the proprietary formula, and produces
   final scores.
4. A strict JSON output schema (backend and frontend depend on the exact structure).
5. Documentation: how the taxonomy works, how scoring works, how determinism is maintained, the
   API contract with backend.
6. Tests: unit tests + reproducibility tests.

### 2.2 The other roles

| Role | Responsibility |
|---|---|
| **Senior Lead Engineer** | Architects everything; builds secure APIs; manages backend, cloud, CI/CD; integrates the NLP pipeline; ensures reproducible output across the system; enforces integration points via code review |
| **Backend Engineer** | Implements API endpoints; formats NLP output into frontend-friendly JSON; ensures performance and security |
| **Frontend Engineer** | Displays highlighted sentences, category tags, scoring-matrix visualisations |
| **QA Tester** | Validates deterministic output; tests consistency and reproducibility; flags mismatches between NLP, backend and frontend |
| **DevOps / Cloud** | Deploys containers, builds CI/CD, manages Airflow deployment, monitoring, scaling, security |

### 2.3 How the NLP engineer serves each role

**QA** gets: testable deterministic outputs (re-run and verify no drift); log-friendly metadata
(sentence IDs, category IDs, taxonomy & scoring version numbers); audit-friendly, traceable
pipeline behaviour. *This is what makes QA's job possible at all.*

**Backend** gets: clean structured JSON; sentence-level offsets for highlight rendering;
API-ready output; a plug-and-play module. Backend only needs to wrap the output into endpoints.

**Lead Engineer** gets: best-practice data schemas, deterministic functions, clear explanations
of the NLP logic, output matched to system architecture, clear internal documentation — fewer
integration headaches.

**Frontend** gets: exact spans for highlights, clean labels, human-readable tags, deterministic
formatting.

### 2.4 What everyone still does after the pipeline exists

This was an explicit worry ("after doing all this, will a backend developer or QA tester still
have something to do?"). Answer: **everyone has a lot of work; your pipeline becomes one part
of a bigger product. You are building the brains; they build the body, face, arms and
communication.**

- **Backend devs** — integrate your FastAPI into their larger API (auth, rate limits, token
  checks, logging, monitoring), build endpoints (`POST /analyze`, `POST /batch/analyze`,
  `GET /taxonomy`, `GET /scores/{id}`), build storage/database layers (PostgreSQL, MongoDB,
  Redis, S3, Parquet, Elasticsearch) with endpoints like `GET /results/{doc_id}` and
  `GET /history?user=123`, and deploy your Docker container (AWS ECS, Lambda + API Gateway,
  Kubernetes EKS/GKE, Docker Compose, Nginx). Typical integration:
  ```python
  @app.post("/analyze")
  async def analyze(doc: DocRequest):
      from nlp_pipeline.main import run_pipeline
      return run_pipeline(doc.dict())
  ```
- **QA testers** — functional tests (`/analyze` returns valid JSON, matches
  `output_schema.json`, scoring matches the rules, running twice gives the same output),
  performance tests (100 requests/sec, 10,000 documents), integration tests (backend ↔ FastAPI,
  Airflow triggers the pipeline correctly), API contract tests, regression tests (taxonomy
  changes must not break scoring; code changes must keep categorisations reproducible).
- **Frontend devs** — website UI, results dashboard, news-analysis interface, document upload,
  visual scoring charts, interactive taxonomy tree, Elasticsearch query UI, login, admin UI for
  editing the taxonomy. They simply call
  `fetch("/api/analyze", { method: "POST", body: JSON.stringify({text: userInput}) })`.
- **DevOps** — deploy to ECS/EKS/Lambda/Cloud Run, CI/CD (GitHub Actions or GitLab CI:
  build → test → deploy), Airflow on Kubernetes or MWAA, monitoring (Prometheus, Grafana,
  CloudWatch, ELK), scaling (autoscaling, load balancing, caching, security).

**Path to the internet:** you build the pipeline (FastAPI app, Dockerfile, pipeline code,
requirements, configs, Airflow DAG) → backend wraps it with auth/logging/DB/routing/business
logic → DevOps builds CI/CD (git push → GitHub Actions builds the Docker image → deploys to
AWS → updates the load balancer → the website backend points at your API) → frontend connects →
QA tests everything.

### 2.5 The proposal sent to the company

> As a Data / NLP Engineer on this project, I would focus on designing a **deterministic,
> mathematically grounded text analysis pipeline** that maps content to your internal taxonomy
> at scale and produces clean, reproducible JSON outputs for the backend and frontend teams.

Its sections and commitments:

- **Project Structure & Integration** — a modular Python package with clear separation between
  preprocessing, segmentation, taxonomy mapping, scoring and I/O, exposed through a simple
  service layer so backend calls a single function/endpoint and receives a strictly validated
  JSON response conforming to an agreed schema. NLP components can evolve internally without
  breaking contracts.
- **Deterministic Taxonomy Mapping** — a strong rule-based core (lexicons, patterns,
  dependency-based rules) for determinism and explainability, with an optional hybrid layer
  (classical ML or a compact transformer) for ambiguous cases. Routing between rules and ML is
  strictly defined and fully configurable; all models versioned with fixed seeds and no online
  learning.
- **Mathematical Scoring Engine** — a standalone engine driven by YAML that encodes the
  proprietary logic as weighted formulas and thresholds. Because it is configuration-driven,
  the company retains full control and the same config can be reapplied to guarantee
  reproducibility and easy auditing.
- **Multi-Label & Ontology Support** — a sentence may belong to multiple taxonomy nodes; the
  taxonomy (and optional ontology relations) is a graph where sentences link to multiple
  categories with confidence scores — straightforward for backend/frontend to highlight
  segments and display overlapping labels while staying deterministic and audit-friendly.
- **Scalability** — batch processing, efficient preprocessing and feature computation, caching;
  deterministic embedding models and exact similarity search where reproducibility is required;
  Airflow integration for scheduled or bulk processing.
- **Intelligent but Controlled Taxonomy Evolution** — an internal tool that analyses
  low-confidence or unmatched sentences, clusters them with deterministic embeddings and
  clustering, and surfaces candidate new categories as human-reviewable suggestions. Approved
  changes are versioned into new taxonomy/scoring config files with clear traceability.
- **JSON Output & Collaboration** — document-level scores, sentence-level classifications, text
  spans for highlighting, and metadata such as taxonomy and scoring versions.

**Standing-out strategy** (7 points): show deep understanding of the determinism requirement ·
propose a rule-based deterministic pipeline using spaCy · propose a versioned taxonomy stored
in YAML · propose the scoring engine as a stateless pure function · propose an Airflow DAG for
scheduled batch processing · propose a JSON schema plus reproducibility unit tests · propose
audit logs (version, timestamp, hash).

---

## 3. System architecture

### 3.1 Medallion (Bronze / Silver / Gold) data flow

```
[SOURCES]
 ├─ Files (txt, md, PDF, DOCX, HTML, XML, JSON, JSONL, CSV)
 ├─ Databases (SQL, NoSQL)
 ├─ Streams / APIs (Kafka topics, REST feeds, RSS)
 └─ Audio/Video → ASR (Whisper, Kaldi) → transcript
        ↓
[INGESTION LAYER]  bulk import via Spark/Ray jobs or streaming consumers
        ↓
[BRONZE ZONE]  raw data stored (Parquet/JSONL) + minimal metadata — immutable landing zone
        ↓
[PREPROCESSING]  cleaning, normalization, language detection, metadata enrichment
        ↓
[SILVER ZONE]  cleaned canonical text in structured form (clean_text, tokens, sentences, entities)
        ↓
[ARGUMENT MINING]  sentence segmentation; extract claims, premises, relations
        ↓
[GOLD ZONE]  rich features + annotations + scores
        ├──► Vector DB (FAISS) — embeddings index for semantic search
        ├──► Feature Registry (YAML schema of features, in Git)
        └──► Taxonomy Engine — taxonomy classification & scoring
                   ↓  Fallacy & Bias Scores, Content Labels
[SERVING DB]  results in SQL for fast API lookup
        ↓
[API & FRONTEND]  REST JSON with highlights/tags for the UI
```

**Zone semantics**

- **Bronze (raw)** — near-raw ingested content with basic metadata (source name/ID, source type
  "web" vs "print", ingest timestamp, `doc_id` or content hash, and any upstream title/author/
  publish date). Very little transformation. HTML entities and extra whitespace may remain.
  Philosophy: **store first, clean later** — a fallback if cleaning or parsing has a bug, and
  the basis for re-processing from scratch.
- **Silver (cleaned)** — canonical normalized corpus ready for NLP. Storing it avoids redoing
  cleaning for every experiment.
- **Gold (features & scores)** — token- and sentence-level annotations, all extracted features,
  argument structure, labels, and scores.

All three zones use the **same underlying storage format (Parquet)** but with different
guarantees and progressively enriched schema. Separating them enforces logical separation of
raw vs processed data and makes the pipeline easier to maintain and debug.

**Coordination** — a pipeline orchestrator (Airflow DAG or a custom scheduler) ensures
ingestion completes before preprocessing, which triggers feature extraction, and so on. Each
stage's output is the next stage's input through well-defined interfaces, so every component
can be developed and tested in isolation and then integrated.

### 3.2 The combined taxonomy + fallacy pipeline (the full intended flow)

```
[Ingestion → JSONL/Bronze] → [Preprocessing → Silver Parquet]
→ [Taxonomy Classification] → [Argument Mining]
→ [Feature Extraction] → [Taxonomy-Aware Feature Gating]
→ [Fallacy Detection Engine] → [Scoring + Confidence]
→ [Gold Parquet] → [SQL Serving + Reports]
```

### 3.3 The parallel-module view (from the detection-strategy design)

```
[Input Article] → [Preprocessing]
   → [ Lexical Module | Sentiment Module | Logic Module | Fact-check Module |
       Propaganda Classifier | Framing Module | Coherence Module ]   (run in parallel)
   → [Integration of Features] → [Scoring Engine] → [Output Results]
```

Modules, in detail:

1. **Data ingestion** — raw text of an article or transcript; may include a web scraper or API
   client.
2. **Preprocessing** — cleaning (HTML tags, scripts), normalization (Unicode), optional split
   into title/body/paragraphs; spaCy tokenize + POS + dependency parse + NER producing a Doc
   object; optional coreference resolution.
3. **Feature extraction modules** (mostly independent, so they can run in parallel):
   - *Lexical Scanning* — pattern matching (regex / spaCy `Matcher`) for bandwagon terms,
     authority phrases, emotional language, hedging words, quantifiers → a dict of flags/counts.
   - *Sentiment & Emotion* — sentiment analyser or emotion classifier per sentence/paragraph →
     overall sentiment, emotional-appeal score, loaded-language score.
   - *Logic & Consistency* — NLI models for contradictions and entailment; rules/classifiers
     for strawman, red herring, circular reasoning.
   - *Evidence & Fact-Checking* — claim extraction; optional external API / local KB
     verification; claim-to-evidence ratio; quote verification for false attribution.
   - *Propaganda Technique Classifier* — a multi-label model (e.g. trained on SemEval-2020
     Task 11 data) predicting a probability per technique per sentence, thresholded into flags.
   - *Topic & Framing* — main topics/entities; framing lexicons; whether multiple perspectives
     are present.
   - *Readability & Coherence* — readability scores, sentence-to-sentence similarity, LM
     perplexity; flags anomalies.
4. **Feature Integration Layer** — assembles the feature vector, e.g.
   `{bandwagon: True, authority_misuse: False, emotional_score: 0.8, strawman: True,
   loaded_language_score: 0.5, contradictions: 2, claim_evidence_ratio: 5.0,
   hedging_density: 0.03, …}` plus the specific phrases/sentences that triggered each flag.
5. **Scoring Engine** — weighted sum (configurable) or a trained meta-model → score,
   classification, and a summary of top contributing factors.
6. **Report Generation** — JSON with all flags and the score, or a human-readable summary; span
   highlighting for the UI.
7. **(Optional) Feedback loop** — editors/analysts correct false positives/negatives; the
   system refines thresholds or retrains the meta-model.

Architectural considerations: keep modules independently developable and testable; watch
efficiency (pairwise NLI is expensive on long articles — pre-filter key sentences or cluster
first); run modules in parallel (async/multithreading on CPU, batching on GPU); cache external
lookups (fact-check queries are slow and rate-limited); scale by splitting into services (one
for NLI tasks, one for sentiment and lexicon checks) behind a central coordinator.

### 3.4 Repository structure (final)

```
NLPpipeline/
├── Dockerfile
├── .dockerignore
├── .gitignore
├── pyproject.toml                  # packaging (PEP 621), src layout
├── requirements-dev.txt
├── README.md
│
├── conf/
│   ├── pipeline_v1.yaml            # pipeline toggles, IO sources, model choices
│   ├── taxonomy_v1.yaml            # category definitions, hierarchy
│   └── scoring_v1.yaml             # weights, formulas, thresholds
│
├── data_schema/
│   ├── input_schema.json           # contract for the ingestion layer
│   └── output_schema.json          # contract for backend/frontend consumers
│
├── src/
│   ├── main.py                     # PipelineRunner orchestrator + CLI
│   ├── core/
│   │   ├── internal_document.py    # THE ingestion→processing contract
│   │   └── exceptions.py
│   ├── nlp_pipeline/
│   │   ├── preprocessing.py        # TextProcessor
│   │   ├── segmentation.py         # SentenceSegmenter
│   │   ├── argument_miner.py       # ArgumentMiner (claims/premises)
│   │   ├── feature_registry.py     # taxonomy-aware feature gating
│   │   ├── features.py             # FeatureExtractor + 13 feature layers
│   │   ├── embeddings_onnx.py      # EmbeddingGenerator
│   │   ├── vector_index.py         # VectorIndex (FAISS)
│   │   ├── rules_engine.py         # RuleEngine
│   │   ├── ml_classifier.py        # MLClassifier
│   │   ├── hybrid_router.py        # HybridRouter
│   │   ├── ontology_graph.py       # OntologyGraph (networkx)
│   │   ├── scoring_engine.py       # ScoringEngine
│   │   ├── postprocessing.py       # PostProcessor / OutputBuilder
│   │   ├── deterministic_utils.py  # seeds, hashing, version stamping (functions only)
│   │   └── gpu_router.py           # optional GPU dispatch (functions only)
│   │
│   ├── taxonomy_tools/
│   │   ├── taxonomy_loader.py      # load + validate taxonomy configs
│   │   ├── taxonomy_versioning.py  # version, diff, migration, audit
│   │   └── taxonomy_suggestions.py # clustering / active learning for new nodes
│   │
│   ├── io_adapters/
│   │   ├── input_router.py         # InputRouter — the traffic controller
│   │   ├── file_readers.py         # BaseReader + per-format readers
│   │   ├── ingest_clients.py       # API, ES, S3, Kafka, Scraper, Redis clients
│   │   └── storage_clients.py      # ParquetWriter, RedisWriter, LocalStorageWriter
│   │
│   ├── batch_processing/
│   │   ├── preprocess_spark.py
│   │   ├── preprocess_ray.py
│   │   ├── classify_batch.py
│   │   └── score_batch.py
│   │
│   ├── api/
│   │   ├── service.py              # FastAPI service exposing the pipeline
│   │   └── models.py               # Pydantic request/response contracts
│   │
│   ├── core_accelerators/          # optional CPU acceleration
│   │   ├── text_ops.cpp / text_ops.h
│   │   ├── nlp_accel.cpp
│   │   ├── bindings.cpp            # PyBind11
│   │   └── CMakeLists.txt
│   │
│   └── gpu_support/                # optional GPU acceleration
│       ├── cuda_ops.cu / cuda_ops.h
│       ├── bindings.cpp
│       └── build.sh
│
├── airflow_dags/
│   └── media_nlp_batch_dag.py
│
├── tests/
│   ├── test_preprocessing.py
│   ├── test_segmentation.py
│   ├── test_rules_engine.py
│   ├── test_scoring_engine.py
│   ├── test_determinism.py
│   └── test_output_schema.py
│
├── notebooks/                      # research only; never imported by production code
│   ├── 01_exploration.ipynb        # EDA on text, distributions
│   ├── 02_rules_design.ipynb       # prototype rules
│   ├── 03_ml_baselines.ipynb       # prototype ML classifier
│   └── 04_taxonomy_suggestions.ipynb
│
├── models/                         # gitignored — large binaries
│   ├── taxonomy_model.pkl          # scikit-learn trained classifier
│   ├── news_classifier.onnx
│   ├── sentence_encoder.onnx
│   └── vector.index                # FAISS
│
├── data/                           # gitignored runtime data
│   ├── raw/ validated/ normalized/ extracted/ failed/ logs/
│
└── logs/                           # run logs, audit trails
```

Who uses what:
- Backend / Lead Engineer call `src/api/service.py`, which takes input JSON, runs
  `nlp_pipeline.*`, and returns strict JSON conforming to `data_schema/output_schema.json`.
- QA uses `tests/test_determinism.py` plus logs to verify reproducibility.
- The NLP engineer owns everything in `nlp_pipeline/`, `taxonomy_tools/`, `scoring_engine.py`
  and the configs.

### 3.5 Technology stack

| Layer | Tools |
|---|---|
| Language | Python 3.10 (3.12 broke the dependency set) |
| NLP | spaCy 3.8, pysbd, NLTK, Stanza, regex |
| Embeddings | HuggingFace Tokenizers (Rust) + SentenceTransformers, ONNX Runtime |
| ML | scikit-learn, ONNX Runtime |
| Vector search | FAISS (local, exact) |
| Taxonomy graph | networkx |
| File reading | pdfplumber, PyMuPDF, python-docx, BeautifulSoup, lxml, pyarrow, pandas |
| API | FastAPI + Uvicorn |
| Storage | Parquet, Redis, boto3 (S3), Elasticsearch |
| Batch | PySpark, Ray |
| Orchestration | Apache Airflow |
| Validation | pydantic v2, jsonschema |
| Sentiment | vaderSentiment (fast path), transformer models (accurate path) |
| OCR | pytesseract |
| Packaging | pyproject.toml + setuptools (src layout) |
| Container | Docker (`python:3.10-slim`) |
| Accelerators | C++ via PyBind11 (CPU SIMD), optional CUDA |

---

## 4. Determinism contract

**The rule:** *Given identical input and identical configuration, the pipeline must produce
byte-identical output across runs, platforms, and environments.* This makes the system suitable
for audit-sensitive environments — media analysis, decision support, finance, policy evaluation.

### 4.1 Every source of randomness and its control

| Source | Control |
|---|---|
| Python `random` | `random.seed(seed)` |
| NumPy | `np.random.seed(seed)` |
| PyTorch | `torch.manual_seed(seed)` |
| sklearn estimators | `random_state=seed` on every constructor |
| ONNX inference | deterministic by construction (frozen graph) |
| Rule evaluation | strictly ordered; no stochastic branching |
| k-means (taxonomy suggestions) | `KMeans(random_state=seed)` |
| Parallel processing order | enforce single-thread ordering where output order matters |
| NLP model versions | lock the model file (e.g. spaCy v3.x with a specific model hash) and record it in `feature_version` |

`seed` always comes from `pipeline_v1.yaml → pipeline.seed`. It is **never hard-coded**.

### 4.2 Version stamping

Every output record carries `pipeline_version`, `feature_version`, `taxonomy_version`,
`score_version` and `processed_at`, so any result can be audited back to the exact code and
config that produced it.

### 4.3 Design invariants (non-negotiable)

- No randomness without explicit seeding.
- Rule evaluation is stable and idempotent.
- Taxonomy changes are version-controlled.
- Scores do not drift unless the scoring YAML changes.
- Pipeline updates are atomic (config + code bundled together).
- API outputs always satisfy `output_schema.json`.
- No external network calls except through `io_adapters`.
- Preprocessing idempotency: **`preprocess(preprocess(text)) == preprocess(text)`** — enforced
  in tests.
- Segmentation: spaCy is used *only* as a boundary detector; every boundary is post-validated
  for determinism; no nondeterministic ML models; boundaries stable across CPU/GPU platforms.
- **The vector DB is read-only semantic memory and never participates in scoring** — embedding
  similarity is statistical and could introduce nondeterminism, which would undermine
  reproducibility.
- GPU code is never used by default.

---

## 5. Data contracts and schemas

### 5.1 InternalDocument — the ingestion↔processing contract

The single most important abstraction. Without it, PDFReader returns one format, the API
another, Kafka another — chaos. With it, NLP does not care where data came from.

```python
class SourceType(Enum):
    FILE_TXT, FILE_PDF, FILE_DOCX, FILE_CSV, FILE_JSON, FILE_JSONL, FILE_HTML, FILE_XML,
    FILE_MARKDOWN, FILE_PARQUET, FILE_IMAGE, FILE_ARCHIVE,
    API_REST, API_GRAPHQL, ELASTICSEARCH, KAFKA, S3,
    DATABASE_SQL, DATABASE_NOSQL, WEB_SCRAPER, STREAM

class ProcessingStatus(Enum):
    INGESTED, VALIDATED, PROCESSED, FAILED, SKIPPED

@dataclass
class InternalDocument:
    # Required
    document_id: str
    text: str
    source_type: SourceType
    ingestion_timestamp: str
    source_metadata: Dict[str, Any] = field(default_factory=dict)
    # Optional
    language: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    # Processing metadata
    processing_status: ProcessingStatus = ProcessingStatus.INGESTED
    processing_metadata: Dict[str, Any] = field(default_factory=dict)
    # Structural data — attached but NOT processed by NLP unless needed
    tables: List[Any] = field(default_factory=list)
    images: List[Dict] = field(default_factory=list)
    sections: List[Dict] = field(default_factory=list)
    # Quality indicators + counts
    quality_flags: ...
    char_count: int; word_count: int; line_count: int
```
Methods: `to_dict()`, `to_json()`, `to_jsonl()`, `from_dict()`.

**Rule: only `InternalDocument.text` flows into NLP.** Rich reader output (tables, images,
stats, structural metadata) stays attached but is not processed unless explicitly needed. This
keeps NLP fast, clean and modular — and it is why raw readers must never leak into the NLP
layer.

### 5.2 Canonical Parquet schema (Silver / Gold)

All pipeline stages conform to and evolve **one** canonical schema — no format conversion
between stages; new features join existing records by `doc_id`.

| Column | Type | Populated at |
|---|---|---|
| `doc_id` | string | Bronze |
| `source` | string | Bronze |
| `source_type` | string | Bronze (`"web"` / `"pdf"` / `"social"`) |
| `language` | string | Silver |
| `raw_text` | string | Bronze |
| `clean_text` | string | Silver |
| `tokens` | list[string] | Silver |
| `sentences` | list[struct] | Silver |
| `entities` | list[struct] `{text, label, start, end}` | Silver |
| `arguments` | list[struct] | Argument Mining |
| `labels` | list[string] | Gold |
| `features` | struct | Gold |
| `scores` | struct | Gold |
| `metadata` | struct `{author, published_at, url, …}` | Throughout |
| `pipeline_version` | string | Gold |
| `processed_at` | timestamp | Gold |

Expanded Gold example:

```json
{
  "doc_id": "string", "source": "string", "language": "string",
  "raw_text": "string", "clean_text": "string",
  "tokens": ["string"], "sentences": ["string"],
  "entities": [ {"text":"string","label":"string","start":0,"end":0} ],
  "features": {
    "num_sentences": 0, "avg_sentence_length": 0.0, "type_token_ratio": 0.0,
    "passive_voice_ratio": 0.0, "sentiment_avg": 0.0, "emotion_dominant": "string",
    "fallacy_strawman": false, "fallacy_strawman_span": "string",
    "fallacy_ad_hominem": false, "propaganda_namecalling": false,
    "bias_entity_sentiment_diff": 0.0
  },
  "scores": { "bias_score": 0.0, "manipulation_score": 0.0, "toxicity_score": 0.0 },
  "pipeline_version": "string", "processed_at": "timestamp"
}
```

**Storage strategy**
- Scalar features → individual Parquet columns (columnar selection means an analysis over just
  sentiment and bias never has to read the heavy text or entity lists).
- List features (tokens, sentences) → nested arrays.
- Structured features (entities, argument graph) → nested structs.
- Embeddings → **not** in Parquet; only an `embedding_vector_id` referencing the vector DB.
- Scores → Parquet, versioned (`score_version=1.0`).

### 5.3 Argument structure sub-schema

```json
"argument_structure": {
   "claims":     [ {"sentence_id": 2, "text": "X", "implicit": false} ],
   "premises":   [ {"sentence_id": 3, "text": "Y", "supports": 2} ],
   "conclusion": {"sentence_id": 1, "text": "Z"}
}
```

### 5.4 Entity analysis sub-schema

```json
"entity_analysis": [
  {"entity": "Alice", "mentions": 5, "sentiment":  0.2, "quotes": 2},
  {"entity": "Bob",   "mentions": 3, "sentiment": -0.5, "quotes": 0}
]
```
(Reading: Alice is quoted twice, Bob never, and Bob's mentions carry negative sentiment —
a bias signal.)

### 5.5 Formal document model

Document *D* = sentences *S₁ … S_m*; sentence *S_i* = tokens *t_i1 … t_in_i*.
Per token: `POS(t)`, `lemma(t)`, `is_stopword(t)`, `NER(t)`.
Per sentence: length |S|, average word length, plus placeholders for sentiment, subjectivity,
stance, factual density, fallacy/propaganda flags, logical-flow score, complexity.
Per document: aggregates of the sentence features plus bias/fallacy/propaganda score vectors.

Aggregation rules: mean or sum for most things
(`document sentiment = (1/m)·Σ sentiment(S_i)`; `POS distribution = (1/N_t)·Σ_t 1{POS(t)=X}`),
but **fallacy presence aggregates by MAX — one strong fallacy taints the whole piece.**
Keep features in arrays so mean and variance are computed in one pass.

**Normalization**: counts ÷ total sentences/tokens → rates in [0,1]; min-max at corpus level for
unbounded features (document length) to cap outliers; z-score during combination so each feature
contributes comparably; final user-facing scores scaled to [0,1] or [-1,1]; logistic/sigmoid
for heavy-tailed counts — `f(x) = 1 − e^(−λx)` converts a raw count into a 0–1 severity.

**Sparse / missing data**: default to 0 or a neutral score; every formula handles a zero
denominator safely (if no claims were found, the verified-claim ratio is defined as 0 by
convention); missing data must never propagate as an error (no discourse connectives simply
means connective frequency 0).

**Statistical validation of the base layer**: check feature distributions across a large corpus
(average sentence length ~15–20 words); validate the syllable counter and sentence splitter
against known Flesch-Kincaid results on a sample; verify POS counts on simple sentences against
manual counts; compare the corpus POS distribution against known linguistic corpora
(e.g. ~40% nouns depending on domain).

---

## 6. Configuration design

**Config = external settings that control how the pipeline behaves without changing Python
code.** Configs are not code — they are instructions for code. The code NEVER hardcodes URLs,
file paths, index names, models or settings.

Who reads what:

| Consumer | Config |
|---|---|
| InputRouter | `pipeline_v1.yaml` → decides which adapter to call |
| IO adapters (ESClient, APIClient, …) | their connection block in `pipeline_v1.yaml` |
| Preprocessing | `preprocessing:` block |
| Segmentation | `segmentation:` block |
| Embedding generator | `embeddings:` block (model + backend) |
| Taxonomy engine / loader | `taxonomy:` block → `taxonomy_v1.yaml` |
| Scoring engine | `scoring:` block → `scoring_v1.yaml` |
| Output writers | `output:` block |

### 6.1 `conf/pipeline_v1.yaml` — the canonical shape

```yaml
pipeline:
  name: media_nlp_pipeline
  version: 1.0
  seed: 42                      # MUST be a real integer — determinism depends on it

input:
  mode: pull                    # pull | push
  source_type: es               # file | api | es | s3 | kafka | redis | web

  es:
    hosts: ["http://localhost:9200"]
    index: "news_articles"
    query: { match_all: {} }
    batch_size: 500

  file:
    path: "/data/raw/"
    allowed_ext: [".pdf", ".txt", ".docx", ".json"]

  api:
    endpoint: "https://newsapi.org/v1/articles"
    headers: { Authorization: "Bearer <token>" }
    params: { category: "politics" }

  s3:
    bucket: "my-ingestion-bucket"
    prefix: "incoming/articles/"

  kafka:
    bootstrap_servers: ["localhost:9092"]
    topic: "incoming_news"
    group_id: "nlp_pipeline"

  redis:
    host: "localhost"
    port: 6379
    stream: "incoming_stream"

preprocessing:
  lowercase: true
  remove_html: true
  normalize_unicode: true
  remove_urls: true
  remove_emojis: true
  lemmatize: true
  remove_stopwords: false

segmentation:
  algorithm: "spacy"            # spacy | nltk | custom
  paragraph_split: true

embeddings:
  model: "sentence-transformers/all-MiniLM-L6-v2"
  backend: "onnx"               # onnx | cpu | gpu
  vector_dim: 384

taxonomy:
  file: "conf/taxonomy_v1.yaml"
  allow_multi_label: true

scoring:
  file: "conf/scoring_v1.yaml"

output:
  writer: parquet               # parquet | redis | local
  parquet: { path: "/data/processed/" }
  redis:   { host: "localhost", port: 6379 }
  local:   { folder: "output/" }
```

### 6.2 `conf/taxonomy_v1.yaml`

```yaml
taxonomy:
  version: "1.0"
  categories:
    politics:
      keywords: ["election", "government", "policy"]
      subcategories:
        foreign_policy:
          keywords: ["diplomacy", "international relations"]
    finance:
      keywords: ["market", "stocks", "inflation"]
```

A harm/abuse taxonomy in the same style (from the evidence-grounded design):

```yaml
harm_categories:
  emotional_abuse:
    indicators: [insults, dehumanization, shaming]
  psychological_manipulation:
    indicators: [fear_induction, guilt_tripping, moral_coercion]
  hate_or_discrimination:
    indicators: [group_targeting, slur_usage]
```

### 6.3 `conf/scoring_v1.yaml`

```yaml
scoring:
  weights:
    politics: 1.2
    finance: 1.0
    health: 0.9
  formulas:
    objectivity_score:
      - rule: "sentiment <= 0.2"
        weight: 0.5
      - rule: "bias_terms < 3"
        weight: 0.5
  score_bands:                     # deterministic score → language mapping
    low:    { range: [0.0, 0.3], phrase: "largely non-harmful" }
    medium: { range: [0.3, 0.6], phrase: "contains some harmful language" }
    high:   { range: [0.6, 1.0], phrase: "contains clearly harmful language" }
```

### 6.4a YAML vs Airflow — they are not substitutes

A recurring confusion: *"what is the use of YAML if I have Airflow?"* **YAML ≠ Airflow. They do
completely different jobs, and you need both.**

| | YAML | Airflow |
|---|---|---|
| Role | **Configuration** — business rules, logic, parameters | **Orchestration** — scheduling, automation, DAGs |
| Contains | Taxonomy definitions, scoring rules, pipeline settings, version info, thresholds, weights, model config | "Run the pipeline at 2AM", "fetch new articles hourly", "save outputs", "retry if the API fails", "notify on failure" |
| Answers | *How* to classify and score; which categories exist; which version of the logic applies; whether ML/GPU is on | *When / where / how* the pipeline runs |
| Scope | Used **INSIDE** the pipeline | Sits **OUTSIDE** the pipeline |
| Analogy | Your brain — knowledge, rules, categories, scoring logic | Your calendar — when tasks run |

**Airflow reads nothing from these YAMLs.** It simply calls `run_pipeline()`. It doesn't know
which rules you use, how you score, or what the taxonomy looks like — and it doesn't care.

How they compose:
```
1. The Airflow DAG runs daily → run_pipeline()
2. Inside run_pipeline():
       taxonomy = load_yaml("conf/taxonomy_v1.yaml")
       scoring  = load_yaml("conf/scoring_v1.yaml")
       settings = load_yaml("conf/pipeline_v1.yaml")
3. The NLP pipeline uses the YAML to classify and score
4. Airflow just orchestrates the run
```
Why companies like the combination: YAML lets **non-programmers** (analysts, product leads)
update business logic — add a taxonomy node, change a weight, add a threshold — with **no code
change, no redeploy, no errors**; Airflow automates and schedules the run.

### 6.4 What the YAML architecture buys you

Switch ES → S3 → API without touching code · add/remove preprocessing steps via config · change
the embedding model instantly · update the taxonomy without touching Python · add new scoring
formulas · change output storage · let Airflow choose any source · let QA test multiple configs
easily · keep runs deterministic · let policy/analyst teams modify pipeline behaviour without
engineering involvement.

### 6.5 Feature Registry

A YAML file in Git enumerating **every** feature — name, description, data type, version. The
extraction code loads the registry *before* running and stores only registry-defined features,
which prevents feature drift. Adding a feature bumps `feature_version`, and every record carries
the `feature_version` used to produce it, so a score change can be traced to a feature-definition
change.

The registry also does **taxonomy-aware feature gating**: it must be consulted *before*
`FeatureExtractor` runs, because running all 13 feature layers on every document is wasteful and
the taxonomy determines which layers are relevant.

---

## 7. Ingestion layer — IO adapters

### 7.1 The cardinal rule

**All input enters ONLY through IO adapters. Preprocessing never reads files. The pipeline never
reads files. Only IO adapters read files.**

### 7.2 Supported input types

- Plain text — `.txt`, `.md`
- Documents — `.pdf`, `.docx`, `.pptx` (layout parsing; OCR for scanned PDFs via pytesseract)
- HTML / XML — web pages, RSS feeds (tag stripping, boilerplate removal)
- JSON / JSONL — **JSONL preferred for intake**: streaming-friendly, one document per line,
  fits message queues, easy to debug
- CSV / TSV — labelled datasets, content metadata
- Databases — PostgreSQL (SQL), MongoDB (NoSQL)
- Streaming — Kafka topics, news-API streams, webhooks
- Cloud — S3 / GCS / Azure Blob
- Audio / video — via speech-to-text (Whisper, Kaldi) producing transcripts that then enter the
  pipeline normally

Per-type handlers: Apache Tika / PyPDF / pdfplumber / PyMuPDF for PDF, BeautifulSoup + lxml for
HTML, direct line reads for JSONL. Language detection routes content to language-specific models
or stops early on unsupported languages (English-only for now; the design stays extensible).

### 7.3 Adapter input signatures — how inputs are segregated

Even though every adapter eventually returns a text string, inputs are **not** similar: each has
a unique *shape/signature*, and that shape is what routing keys on.

| Adapter | Expected input | Example | Result |
|---|---|---|---|
| UniversalLoader / file readers | file path | `"C:/docs/news.pdf"`, `"article.txt"` | text string |
| ScraperClient | URL string | `"https://bbc.com/news/election-2025"` | text string |
| IngestAPIClient | URL + params, or a dict | `{"endpoint":"/getArticle","apikey":"ABC","article_id":"10291"}` | text string |
| ESClient | search query / document ID | `{"index":"news_articles","query":"election fraud"}` | text string |
| S3Loader / S3Client | S3 URI | `"s3://news-bucket/2025/jan/article.pdf"` | text string (internally calls the file readers) |
| KafkaConsumer / KafkaClient | topic name → messages | `"news_topic"` → `{"article_id":322,"text":"Breaking news: …"}` | text string |
| RedisCache / RedisClient | key + value | `("article_1020", "cleaned text…")` | stores value — **output, not input** |
| ParquetWriter | pipeline result dict | `{"sentences":[…],"labels":[…],"scores":{…}}` | writes a file — **output** |
| StorageClient | path + data | `("path/to/store/file.json", data_dict)` | saves a file — **output** |

### 7.4 The routing decision tree

```
if   input is dict                                   → APIClient or ESClient
elif input starts with "http" / "https"              → Scraper
elif input starts with "s3://"                       → S3Loader
elif input ends with (.pdf, .docx, .pptx, .txt, …)   → file readers
elif input matches a topic in the Kafka config       → KafkaConsumer
elif input is a (key, value) tuple                   → RedisCache
else                                                 → error: unsupported input
```

Signature summary: file paths contain `.` and end with a known extension · URLs start with
`http` · S3 URIs start with `s3://` · API inputs are dicts (often with `endpoint` / `api_key`) ·
ES inputs are dicts containing `query` / `index` / `_id` · Kafka is a preconfigured topic name ·
Redis is a key-value pair.

### 7.5 Push mode vs pull mode — the two-method pattern

Every ingest adapter exposes exactly two methods:

- **`receive(payload)` — PUSH.** Someone hands you data: a FastAPI upload, a backend POST, an S3
  "new file uploaded" event, a Kafka consumer callback, a Redis pub/sub message. Converts the
  input into an `InternalDocument` immediately; performs no fetching.
- **`fetch(config)` — PULL.** Actively goes and gets data: runs an ES query and scrolls, calls an
  external API, downloads from S3, polls a Kafka topic, scrapes a URL, reads Redis keys. Returns
  internal documents.

Consequently: **Airflow always calls `.fetch()`; FastAPI always calls `.receive()`.**

Mental flows:
- *ES push*: backend gives you an ES hit → `ESClient.receive(es_hit_dict)` → internal doc.
  *ES pull*: Airflow triggers → `ESClient.fetch(config)` → connects, queries, scrolls → docs.
- *API push*: backend POSTs JSON → `APIClient.receive(json_payload)`.
  *API pull*: Airflow triggers → `APIClient.fetch(config)` → calls the external API.
- *S3 push*: an S3 event fires → `S3Client.receive(event_object)` → downloads the file.
  *S3 pull*: Airflow triggers → `S3Client.fetch(config)` → lists the folder, downloads objects.

Note on ES specifically: **pull mode is the real, important one**; the push mode (being handed
ES hits by another service) is rare and can be ignored for now.

Output adapters have no push/pull — only `write(document)` and `save_batch(documents)`:
ParquetWriter (single Parquet write / Parquet dataset), RedisWriter (key or stream), and
LocalStorageWriter (a JSON file / a folder of JSON files).

### 7.6 Final IO layout

```
src/io_adapters/
  input_router.py     # InputRouter — the central brain
                      #   route_input()/route_push_input()  — PUSH
                      #   route_source()/route_pull_source() — PULL
  file_readers.py     # BaseReader + TxtReader, MarkdownReader, PDFReader, DocsReader,
                      #   PPTReader, CSVReader, JSONReader, JSONLReader, HTMLReader, XMLReader
                      #   — each with receive(file_bytes) and fetch(file_path)
  ingest_clients.py   # ESClient, APIClient, S3Client, KafkaClient, ScraperClient, RedisClient
                      #   — each with receive() and fetch()
  storage_clients.py  # ParquetWriter, RedisWriter, LocalStorageWriter — write()/save_batch()
```

**BaseReader must stay in `file_readers.py`.** That module represents *file-like inputs* (files
on disk, archives, structured and semi-structured documents) and BaseReader is the contract for
file ingestion. It must not be mixed with API / Kafka / Elasticsearch / streaming ingestion —
those are *source readers*, not file readers. The four-way split
(`file_readers` | `ingest_clients` | `input_router` | `storage_clients`) is exactly how large
systems do it.

### 7.7 Build order and difficulty of the adapters

| Stage | Adapters | Difficulty | Why |
|---|---|---|---|
| 1 — easy wins | TextReader → JSONFileReader → CSVReader → DocxReader → PDFReader → PPTReader → ParquetWriter → LocalStorageWriter | ★ | predictable logic; builds confidence and shows that all adapters share one architecture |
| 2 — medium | ScraperClient, APIClient | ★★ | HTML parsing + failed-site error handling + clean text extraction (BeautifulSoup); GET/POST, headers, pagination, JSON parsing |
| 3 — big systems | ESClient (★★★), RedisClient (★★★★), S3Client (★★★★) | ★★★–★★★★ | nested ES responses, scroll API, pagination, query building, `_source` extraction, connection reliability · Redis may be key-value, lists, streams or pub/sub and you must detect which · boto3 configs, bucket prefixes, listing, downloading, content-type detection, large files |
| 4 — big data | KafkaClient | ★★★★★ | consumers, polling loops, offsets, message decoding, timeouts, batching, error handling, async vs sync consumption |

Start with **TextReader**.

After the file readers, the next readers in priority order: **ParquetReader** (very important
for pipelines) → **ArchiveReader** (zip, tar, gzip) → S3Client (reuse the file readers) →
APIClient → KafkaClient. **Do not start preprocessing until ingestion is frozen** — the
ingestion layer is foundational.

### 7.8 Configs differ per source — hence config-driven adapters

Every API has different base URLs, auth (API key, OAuth, headers), endpoints, parameters and
JSON structures; the same is true of ES, Redis and Parquet targets. So none of it is hardcoded:
you build a **config-driven adapter system**, and Airflow simply calls the adapters with the
right config.

### 7.9 The ingestion flow and the InputRouter

```
File / API / ES / Kafka
   ↓
Reader (PDFReader, JSONReader, …)
   ↓
Raw Ingestion Record (rich dict: raw content, structural metadata, statistics, quality flags,
                      extracted text)
   ↓
InputRouter
   ↓
InternalDocument      ← ONLY THIS goes into NLP
   ↓
preprocessing.py
```

```python
class InputRouter:
    def __init__(self, config):
        self.config = config
        self.file_readers = {
            ".txt": TxtReader(),   ".md": MarkdownReader(), ".pdf": PDFReader(),
            ".docx": DocsReader(), ".csv": CSVReader(),     ".json": JSONReader(),
            ".jsonl": JSONLReader(), ".html": HTMLReader(), ".xml": XMLReader(),
        }
        self.ingest_clients = {
            "api": APIClient(), "elasticsearch": ESClient(), "kafka": KafkaClient(),
            "s3": S3Client(),   "scraper": ScraperClient(),
        }

    # ---- PUSH ----------------------------------------------------------
    def route_push_input(self, input_payload):
        if input_payload.type == "file_path":
            return self._handle_file(input_payload.path)
        if input_payload.type == "file_bytes":
            return self._handle_bytes(input_payload.bytes)
        if input_payload.type == "api_payload":
            return self._to_internal_document(APIClient.receive(input_payload.data))
        if input_payload.type == "es_hit":
            return self._to_internal_document(ESClient.receive(input_payload.hit))

    # ---- PULL ----------------------------------------------------------
    def route_pull_source(self):
        client = self.ingest_clients[self.config.input.source_type]
        for raw_record in client.fetch(self.config.input):
            yield self._to_internal_document(raw_record)

    # ---- helpers -------------------------------------------------------
    def _handle_file(self, file_path):
        ext = Path(file_path).suffix.lower()
        if ext not in self.file_readers:
            raise UnsupportedFileTypeError(ext)
        return self._to_internal_document(self.file_readers[ext].read(file_path))

    def _to_internal_document(self, raw_record):
        return InternalDocument(
            document_id     = raw_record["file_hash_sha256"] or generated_id,
            text            = self._extract_text(raw_record),
            source_type     = raw_record["reader_class"],
            source_metadata = raw_record,
            ingestion_metadata = {
                "timestamp": raw_record["processed_timestamp"],
                "reader":    raw_record["reader_class"],
            },
        )

    def _extract_text(self, raw_record):          # text-extraction policy, in priority order
        if "full_raw_text"  in raw_record: return raw_record["full_raw_text"]
        if "extracted_text" in raw_record: return raw_record["extracted_text"]
        if "raw_content"    in raw_record: return raw_record["raw_content"]
        raise NoTextFoundError()
```

### 7.10 What a good reader layer does (senior review of the implemented `file_readers.py`)

Verdict on the code actually written: *"closer to enterprise ETL ingestion than typical NLP
projects… data-platform quality, not notebook quality"* — it demonstrates data engineering
thinking, provenance tracking, auditability, fault tolerance and format-agnostic ingestion.

The eight hard problems it solved that most juniors miss:

1. **Encoding detection** — `charset_normalizer` with a fallback
2. **Content hashing** — SHA-256 for deduplication and provenance
3. **MIME detection** — `magic`
4. **Metadata standardization**
5. **Error isolation** — write to `errors.jsonl` instead of crashing
6. **Structure preservation** — JSON/XML/HTML depth, tables, headings
7. **Non-lossy ingestion** — raw + extracted + statistics all retained
8. **JSONL output** — stream-friendly and scalable

Employer's reading of that work: *"This candidate understands ingestion, metadata, auditability
and platform design — not just NLP models."*

Ingestion dependency set:
```
charset-normalizer python-magic-bin pdfplumber pymupdf python-docx beautifulsoup4 lxml
markdown pandas pyarrow pytesseract Pillow sqlalchemy pymongo boto3 kafka-python
elasticsearch requests
```

### 7.11 Two ingestion modes

- **Bulk / historical** — a batch Spark job or Python ETL script reads the source files/DB,
  converts each record into the internal JSONL schema (assigning a unique `doc_id`, capturing
  source info), and writes to the Bronze Parquet store. Writing Bronze directly as Parquet with
  minimal fields (`doc_id`, `raw_text`, basic metadata) is effective.
- **Streaming** — a consumer parses each message and appends it to Bronze in micro-batches or
  via a stream append; alternatively, real-time ingestion can trigger downstream processing per
  item (careful design required to maintain throughput).

### 7.12 Ingestion logging

Every item is logged: which `doc_id` was ingested, from what source, and any errors, in `.log`
or JSON-log format. These logs aid traceability, feed a monitoring dashboard (ingestion rates,
error rates) and let QA confirm every expected input was accounted for and spot anomalies such
as error spikes.

---

## 8. Preprocessing

`src/nlp_pipeline/preprocessing.py` — class `TextPreprocessor` / `TextProcessor`, one class with
an `__init__` that loads config and a `clean` / `process` / `normalize` method. It operates
**only on `InternalDocument.text`** — never on PDFs, never on APIs. That separation is critical.

### 8.1 The six stages

1. **Clean raw input** — remove HTML, URLs, emails, phone numbers, emojis, excess whitespace,
   control characters, junk symbols, ads/footers/boilerplate, duplicate whitespace.
2. **Normalize text** — Unicode normalization (NFKC/NFKD), accent handling, standardize
   quotes/apostrophes, fix spacing, remove repeated symbols, lowercase where appropriate
   (**keep case for proper nouns**).
3. **Optional stopword removal** — config-driven: leave words intact if the rules rely on
   keywords; remove them if the ML relies on bag-of-words features.
4. **Lemmatization** — spaCy ("running"/"ran" → "run"; "policies"/"policy" → "policy"). Improves
   rule matching, ML features and embedding consistency.
5. **Basic tokenization** — splitting into meaningful units, marking punctuation, identifying
   parts of speech (spaCy handles this efficiently).
6. **Return a clean string** — clean, normalized, optionally lemmatized, ready for segmentation.

Also part of Bronze→Silver preprocessing: **boilerplate removal** (header/footer noise,
navigation menus; readability algorithms for main-text extraction), **metadata enrichment**
(parse publication date to datetime, attach author/outlet, section/category), **language
detection** (set `language`, filter non-English if required), and **consistency checks**
(`clean_text` not empty — drop or mark if it is; encoding issues resolved; drop documents that
are too short or out of scope).

### 8.2 Reference pseudocode

```python
def preprocess_raw(doc):
    text = doc.raw_text
    meta = doc.metadata
    text = normalize_unicode(text)
    text = fix_whitespace(text)
    if meta.source_type == "html":
        text = strip_html_tags(text)
    text = remove_boilerplate(text)          # e.g. "Advertisement" labels
    sentences = nltk.sent_tokenize(text)     # or spaCy
    lang = detect_language(text)
    return {
        "doc_id": doc.doc_id,
        "clean_text": text,
        "sentences": sentences,
        "language": lang,
        "metadata": {"title": meta.title, "author": meta.author,
                     "published_at": parse_date(meta.date)},
    }
```
(In practice also handle errors, log any changes, and preserve the raw text for reference.)

### 8.3 The most important preprocessing rule

**Preprocessing must NOT be too aggressive.** Rules, ML, taxonomy and scoring all depend on
important words. Do not remove: numbers · meaning-splitting punctuation · specific keywords ·
named entities · verbs the rules rely on. Keep it light and safe.

### 8.4 QA expectations

Given the same PDF, the extracted text must always be identical. Dates must parse correctly. No
content may be silently dropped — an unexpectedly empty `clean_text` indicates a cleaner bug
(e.g. an unusual HTML structure confusing the parser) and should prompt an improvement.

---

## 9. Segmentation

`SentenceSegmenter` — the sentence is the fundamental unit of the whole system (sentiment per
sentence, fallacy flags per sentence, highlight spans per sentence).

- Use **spaCy (and/or pysbd)** as a *boundary detector only*; post-validate every boundary for
  determinism.
- No nondeterministic ML models in the boundary path.
- Custom patch rules for domain-specific segments (media abbreviations).
- Multi-split handling: headline / sub-title / lead paragraph.
- Mark paragraph breaks for large texts.
- Boundaries must be stable across CPU/GPU platforms.

Each sentence is then tokenized with linguistic annotations (POS tags, dependency parse, NER).
This token-level analysis is deterministic given a locked library model version, recorded in
`feature_version`.

### spaCy vs NLTK — decided

**Use spaCy. Do not use NLTK.**

| | spaCy | NLTK |
|---|---|---|
| Character | Modern, fast (Cython), industrial, production-ready | Old-school, academic, slow |
| Good at | Normalization, tokenization, lemmatization, POS, NER, sentence segmentation, rule-based pattern matching, HuggingFace/ONNX integration, deterministic pipelines | Simple normalization, tokenization, stopword lists, stemming, basic text utilities |
| Weaknesses | — | Weak sentence tokenizer, not optimized for large datasets, hard to maintain large rulesets, not production-suitable |
| Used by | Bloomberg, Netflix, ExplosionAI, many MLOps teams | Mostly a learning tool |

| Task | Best tool |
|---|---|
| Cleaning | regex + manual rules (fast, deterministic) |
| Normalization | spaCy or simple utils |
| Lemmatization | spaCy (NLTK's is weak) |
| Stopwords | spaCy (clean list) |
| Tokenization | spaCy (industrial performance) |
| Emoji/HTML cleanup | your own rules (smarter control) |

Model choice: `en_core_web_lg` (includes word vectors for similarity) or `xx_ent_wiki_sm` for
multilingual; Stanza as a fallback for languages spaCy doesn't cover (slower). SparkNLP 4.x for
distributed parsing.

**Complexity**: O(N_t) per document for tokenization and tagging; spaCy processes roughly
1M tokens per CPU core per second. Parsing (dependency + NER) is also near-linear per sentence
with a small constant.

**Scaling**: `nlp.pipe(docs, n_process=8)` for multi-core; Ray remote batches of ~1000 docs;
Spark `mapPartitions` with the model loaded per executor (use a broadcast variable or
initializer so the model isn't reloaded per record). **Stream through documents — never hold the
whole corpus in memory.**

```python
import spacy
nlp = spacy.load("en_core_web_lg")

def process_document(doc_id, text):
    doc = nlp(text)
    token_features = [{
        "token": t.text, "lemma": t.lemma_, "pos": t.pos_, "is_stopword": t.is_stop,
        "ner_type": t.ent_type_ or None,
        "sentiment": 0.0, "toxicity": 0.0,
        "fallacy_signal": 0.0, "bias_signal": 0.0, "propaganda_signal": 0.0,   # placeholders
    } for t in doc]

    sentence_features = [{
        "sentence_id": i, "text": sent.text,
        "sentiment": 0.0, "subjectivity": 0.0, "stance": None, "factual_density": 0.0,
        "fallacy_present": False, "propaganda_present": False,
        "logical_flow_score": 1.0, "complexity": 0.0,
    } for i, sent in enumerate(doc.sents)]

    doc_features = {
        "doc_id": doc_id, "topic_distribution": {}, "overall_bias_vector": [],
        "fallacy_vector": [], "propaganda_vector": [], "stance_distribution": {},
        "factuality_score": 0.0, "transparency_score": 0.0, "data_accuracy_score": 0.0,
        "conflict_score": 0.0, "aggregate_quality_score": 0.0,
    }
    return {"tokens": token_features, "sentences": sentence_features, "document": doc_features}
```

**Integration rule:** every later module **updates** these sentence/document dicts rather than
building new structures — everything stays linked by `sentence_id`, so you always know exactly
which sentence a fallacy was found in.

**Storage caveat:** token-level features for 1M documents are enormous. Store sentence- and
document-level features in the database; keep token features in memory during processing, or
serialize them compressed, or retain them only for troubleshooting and examples.

Distributed template:
```python
import ray
ray.init()

@ray.remote
def process_batch(batch):
    return [process_document(doc_id, text) for doc_id, text in batch]

batches = [docs[i:i+1000] for i in range(0, len(docs), 1000)]
results = ray.get([process_batch.remote(b) for b in batches])
```

---

## 10. Argument mining

An **explicit pipeline stage** sitting between segmentation (Silver) and feature extraction.
Module: `nlp_pipeline/argument_miner.py`, class `ArgumentMiner`, method `extract(sentences)`.

### 10.1 What it identifies

- **Claims / Conclusions** — statements expressing a stance or assertion; the article's main
  point or sub-claims supporting it.
- **Premises / Evidence** — statements providing support or reasons (factual evidence, quotes,
  logical reasoning).
- **Opposing / Counterarguments** — present in balanced articles; their *absence* is itself a
  feature (biased articles often omit them).
- **Relations** — which premises support which claims (a directed graph; support and attack
  edges).

### 10.2 Detection methods

**Rule-based** — conclusion markers ("therefore", "thus", "in summary", "in conclusion",
"overall"); premise markers ("because", "since", "due to", "as a result"); dependency parsing
for `<claim>, because <premise>` structures; quotation marks or references indicating evidence.

**ML** — a BERT-style classifier labelling sentences as {Premise, Claim, None}; pretrained
argument-mining models from research; argument relation classification models. Given the
confidential nature and the timeline, a simpler approach is acceptable.

**Relations heuristic** — link premises to the nearest claim or to the article's main
conclusion; "premise sentences directly following a claim sentence likely support that claim".

### 10.3 Reference implementation

```python
doc = nlp(clean_text)                       # spaCy with dependency parse
sentences = list(doc.sents)
argument_graph = {"claims": [], "premises": [], "conclusion": None}

for i, sent in enumerate(sentences):
    text = sent.text
    if any(word.lower_ in ["in conclusion", "overall", "thus"] for word in sent):
        argument_graph["conclusion"] = {"sentence_id": i, "text": text}
    if any(word.lower_ in ["because", "since", "as a result"] for word in sent):
        argument_graph["premises"].append({"sentence_id": i, "text": text})
    if sent[-1].lemma_ == "?":
        continue                            # skip questions
    if sent.root.pos_ == "VERB" and sent.root.dep_ == "ROOT":
        argument_graph["claims"].append({"sentence_id": i, "text": text})   # root-level assertion
# then link premises to claims via adjacency or an ML model
```

### 10.4 Why this stage is critical

Many fallacies are *argumentative errors* and can only be caught with explicit structure:

- **Non sequitur** — the conclusion doesn't follow from the premises; found by mapping premises
  to conclusion and detecting a logical gap.
- **Circular reasoning** — a premise is essentially the conclusion; found as a cycle in the
  graph, or when the conclusion repeats a claim.
- **Missing premises / hidden assumptions** — an isolated strong claim with no supporting
  premises.
- **Slippery slope** — a chain of claims each implying the next without support (A→Z with no
  intermediate steps).

**Without explicit argument structure, fallacy detection becomes fragile and relies on shallow
cues.** Fallacy detection, PropScore and stance classification all depend on this structure.

### 10.5 Cost and QA

News articles are only a few dozen sentences, so this is manageable: use the spaCy dependency
parse as the first cut and resort to heavier ML only if needed. The approach is versioned
(`feature_version` or a dedicated `argument_version`).

QA test cases: given "Because X, therefore Y." the graph must identify X as a premise and Y as a
conclusion with a supporting link. An opinion piece with no "because" must still process without
error — a claims-only graph is itself the signal "unsubstantiated claims".

---

## 11. Feature extraction — the 13 layers

Feature extraction is the heart of the pipeline's intelligence, designed in layers from
fundamental linguistic features up to high-level semantic and rhetorical indicators. Simpler
features (word counts, POS tags) form the foundation for more complex inferences (detecting a
slippery-slope argument). Every layer's output is added to the Gold dataset.

**Build phases** (deliver a working MVP quickly, then enhance):

| Phase | Layers | Rationale |
|---|---|---|
| **Phase 1 — must-have** | 1 Structural, 2 Lexical, 5 Entity, 6 Sentiment, + embeddings | the basics needed for any analysis |
| **Phase 2 — differentiators** | 7 Framing, 8 Rhetorical, 9 Fallacy, 10 Factuality, attribution | what truly distinguishes the system at detecting manipulation |
| **Phase 3 — advanced** | 11 Temporal, 12 Cross-document/network, 13 Metadata | research-grade; needs cross-document data |

### Layer 1 — Structural & Textual (foundation)

Document length in tokens/characters/sentences · average sentence length · paragraph count and
length distribution · punctuation counts (`?` for rhetorical questions, `!` for emotional tone) ·
quote density (how much text is inside quotation marks — high density may mean more factual
sourcing, or a particular bias depending on *who* is quoted) · headline length and
clickbait/sensational words · title-vs-body discrepancy.

These features "stabilize everything else": they explain variance independent of content.
Extremely short articles or extremely long sentences affect readability and correlate with
style — a manipulative article tends toward either very short punchy sentences or very long
convoluted ones.

```python
num_tokens = len(doc.tokens)
num_sentences = len(doc.sentences)
avg_sentence_length = num_tokens / num_sentences if num_sentences > 0 else 0
question_count    = text.count('?')
exclamation_count = text.count('!')
quote_count       = text.count('"') // 2      # roughly the number of quoted segments
```

### Layer 2 — Lexical & Vocabulary

Type-Token Ratio (unique tokens / total tokens) · lexical diversity indices (e.g. Shannon
entropy of word frequency) · rare-word density (words outside the top 5k common words —
propaganda sometimes uses simple mass-appeal language, sometimes jargon) · abstract vs concrete
language ratio via lexicon (highly abstract language suggests ideological content over concrete
data) · **loaded language** count (emotionally charged words: "disaster", "outrageous",
"brilliant"; NRC emotion lexicon or a custom list) · intensifiers ("very", "extremely",
"absolutely") · **absolutist terms** ("always", "never", "everyone", "no one" — signal
overgeneralization and black-and-white framing) · ideological lexicon usage ("liberal agenda",
"deep state") · polarizing adjectives and slanted descriptors ("so-called" prefixed to undermine
a term; "corrupt leader" vs "esteemed leader").

Critical for **early** bias detection — word choice reveals sentiment and bias before deeper
structure is analysed. Derogatory name-calling shows up here as well as in the propaganda layer.

```python
intensifiers = {"very", "extremely", "deeply", "highly"}
absolutes    = {"always", "never", "everyone", "no one", "all", "none"}
intensifier_count = sum(1 for t in tokens if t.lower_ in intensifiers)
```
Normalize each count by text length to get a frequency.

### Layer 3 — Syntactic & Grammatical

POS tag distribution (many adjectives/adverbs → opinionated or emotional; many nouns and numbers
→ factual reporting) · syntactic complexity (average parse-tree depth, frequency of subordinate
clauses — convoluted sentences may indicate obfuscation, extremely simple ones a different
style) · **nominalizations** ("the destruction of" instead of "destroying" — makes text abstract
and impersonal) · **passive voice usage** · hedging vs certainty ("might", "it is possible that"
vs "must", "undoubtedly") · **attribution verbs** ("claims", "admits", "alleges" instead of
"says" injects doubt — subtle linguistic bias).

```
passive_voice_ratio = passive_sentences / total_sentences
```
Detection: a form of "to be" + past participle, or the spaCy dependency label `nsubjpass`.
Above ~0.5 signals that the text frequently avoids assigning direct blame or action to agents
("Mistakes were made" vs "We made mistakes") — a responsibility-evasion flag.

Syntax can also hide propaganda: **loaded questions** ("Why does [target] always do X?") are
question sentences containing an embedded assumption.

### Layer 4 — Semantic & Topic

**Embeddings** — token (contextual BERT or static word2vec), sentence and document embeddings
(~768-d for BERT, 384-d for MiniLM). *Not* stored in Parquet — pushed to the vector DB, with
Parquet holding only an `embedding_vector_id`. Enables: finding similar articles (clustering
propaganda by narrative) and nearest-neighbour comparison against known propaganda exemplars.
The vector DB must be updated in step with Parquet so the embedding matches the same version of
the text.

**Topic modelling** — LDA or keyword categorisation assigns a topic or a distribution over
topics. Bias interacts with topic (political news carries more partisan language than sports).

**Known-narrative similarity** — comparison against corpora of known biased narratives (advanced;
in general the embedding + vector DB already supports narrative clustering).

**Contradiction checks** — an NLI model labels sentence pairs entailment / contradiction /
neutral. An internal contradiction is a strong sign of poor quality or deliberate inconsistency
→ `internal_contradiction = True/False` or a count of contradictory pairs.

**Headline-body coherence** — cosine similarity between the headline embedding and the body
embedding. Very low similarity indicates a misleading or off-topic headline (clickbait).

**Semantic coherence** — average cosine similarity between consecutive sentences or paragraphs;
extremely low values signal a narrative jump or inserted content.

**Concept drift** — concepts introduced that don't relate to the main topic (topic segmentation
or unusual word occurrence).

### Layer 5 — Entity & Attribution

NER (Person, Organization, Location, …), stored as a nested list with type and offsets ·
**entity frequency and prominence** (repeating a name to villainize or lionize) · **sentiment
toward each entity** (aggregate the sentiment of the sentences mentioning them — one entity
consistently positive and an opposing one consistently negative is bias) · **toxicity or abusive
language toward entities** (hate lexicon or a toxicity classifier such as Perspective API; high
toxicity aimed at an entity suggests ad hominem) · **quotation and sourcing** (who is quoted vs
merely talked about → *quote imbalance* if only one side is quoted) · **attribution bias**
(track verbs per entity — "Alice said…" vs "Bob claimed…") · **entity absence** (an expected
stakeholder never mentioned — e.g. one party entirely missing from a political story) · **power
dynamics** (elite — politicians, CEOs — vs non-elite framing).

### Layer 6 — Sentiment & Subjectivity

Overall sentiment polarity in [−1, 1] per sentence, aggregated to the document · **sentiment
volatility** (variance/range across sentences — wild swings suggest emotional manipulation or
sarcasm) · **emotion categories** via an emotion classifier or the NRC Emotion Lexicon (anger,
fear, joy, sadness, disgust, hope, outrage — anger and fear matter most for propaganda),
producing an emotion vector `{anger: 0.3, fear: 0.4, joy: 0.1, …}` · **subjectivity ratio**
(subjective sentences / total) · **assertiveness vs hedging** (certainty modals and adverbs;
high certainty combined with low evidence is a red flag) · **emotional appeal index** =
emotional words / factual references.

Models: `distilbert-base-uncased-finetuned-sst-2-english` for polarity; a multi-class emotion
model (e.g. `bhadresh-savani/distilbert-base-uncased-emotion`) or NRCLex/VADER/TextBlob for the
lexicon route. spaCy's `Matcher` can flag extreme adjectives or exclamation marks as quick cues.

```python
emotion_scores = emotion_model(text)          # {"anger":0.4, "joy":0.1, "sadness":0.2, ...}
dominant_emotion = max(emotion_scores, key=emotion_scores.get)
if dominant_emotion in ["anger", "fear"] and emotion_scores[dominant_emotion] > 0.5:
    flags["emotional_appeal"] = True
```

Important distinction: **emotion is not sentiment.** A piece can be negatively emotional
(anger/fear) in a way that is targeted emotional manipulation rather than mere "negative
sentiment". High emotion combined with low evidence indicates an Appeal to Emotion fallacy.

### Layer 7 — Framing & Narrative

**Issue frames** — Conflict (us vs them, winners vs losers) · Human interest (personal stories
evoking sympathy) · Morality (arguments in terms of morals or religion) · Economic (cost/benefit)
· Nationalism (patriotic rhetoric) · Victim vs oppressor.

**Narrative arcs** — hero/villain casting (one entity consistently associated with positive
words, another with negative); whether the story offers resolution or only paints a crisis
(crisis without resolution incites anger).

**Blame attribution** — is a person or group consistently blamed → scapegoat framing.

**Agenda cues** — multiple articles sharing the same talking points or phrases (requires
cross-document analysis).

Start with keyword proxies per frame: conflict = "battle, attack, defend, enemy"; human interest
= "family, child, individual stories"; morality = "sin, ethics, moral, corrupt". A significant
count ticks a binary indicator for that frame.

**Omission framing** (bias by omission) is noted as hard to quantify from a single document — it
requires an external reference for what *should* have been mentioned.

### Layer 8 — Rhetorical & Persuasion

**Ethos / Pathos / Logos**: Ethos = reliance on authority figures or credentials (quoting
experts is ethos-based; misused it becomes a fallacy). Pathos = the emotional-appeal features.
Logos = whether arguments are logically structured and evidence-based (argument structure +
factual evidence count).

**Persuasion tactics**: appeal to fear · appeal to authority/tradition ("experts say", "we've
always done it this way") · **whataboutism** ("X happened… but what about Y?") · slippery slope ·
strawman · name-calling / ad hominem · **loaded questions** ("Have you stopped wasting money?"
implies you were) · **repetition** (repeating a message to drum it in — measure repeated phrases
or identical sentences) · glittering generalities · flag-waving · thought-terminating clichés ·
card stacking.

Each technique is recorded as a binary flag and/or an intensity score
(`propaganda_name_calling = True`, or an integer insult count).

### Layer 9 — Logical Fallacy Detection (signature layer)

See §12 for the full catalog. Prepared for by the argument graph and the supporting features
(causal words, quantifiers, toxicity, entity sentiment).

### Layer 10 — Factuality & Evidence

Presence of factual claims (sentences containing numbers, dates, names) · count of numbers and
statistics · cited sources (URLs, "According to [source]") · **fact density** (factual vs opinion
statements; proxy = counts of numbers and proper nouns) · **claim specificity** (concrete —
"5,000 people in France on July 14" — vs vague — "some people in a European country"; low
specificity + high certainty indicates deception) · **unverifiable claims** ("experts say"
without naming, "it is known that…", "many people are saying…") · **quantifier misuse**
("millions" with no basis) · clickbait indicators in headlines.

Numeric checks: **numerical consistency** (5 million in one place, 10 million in another) ·
**percentage sum check** (do the cited percentages sum to ~100% when they should?) · **outlier
detection** ("120% of people support something") · **data omission/manipulation cues**
("up 300%" with no baseline; "record high" or "unprecedented" without context).

Outputs: flags such as `has_unverifiable_claims`, `has_statistical_misuse`, and an overall
factual reliability score starting at 1.0 with deductions per issue.

### Layer 11 — Temporal & Contextual

Event timeline consistency (is chronology distorted for narrative effect?) · selective history /
omitted historical context · repetition cycles (the same slogan repeated periodically) · context
omissions · comparison of `published_date` against the dates of events mentioned (an old event
framed as new; present tense for something long past) · **discourse markers** ("however",
"although", "meanwhile") counted as narrative-shift signals.

A concrete manipulation to catch: reporting one side's response without mentioning the
provocation that preceded it — creating a misleading cause-and-effect.

### Layer 12 — Cross-Document & Network (advanced)

Source comparison for the same event (how does this source's language differ?) · narrative
consistency across articles · propaganda-network signals (reused phrases or hashtags) · source
clustering (position this article's language in embedding space relative to known left-leaning,
right-leaning and centre clusters) · shared n-grams with known propaganda outlets.

Not implemented initially, but the pipeline is structured so a batch job can compute these
metrics after processing many articles and append them to the Gold records.

### Layer 13 — Metadata & Provenance

Outlet information joined to external bias/reliability data (e.g. MediaBiasFactCheck) →
`source_bias_rating` (lean left / centre / lean right), `source_reliability_score` · author
information and history · publication context (region/country) · social-media traction (shares,
likes — interesting but *not* a direct bias measure, since popularity-as-truth is itself a
bandwagon fallacy) · network membership.

Metadata amplifies text signals by providing context — but must be used carefully to avoid
circular reasoning (don't assume bias merely because of the source).

---

## 12. Logical fallacy detection

### 12.1 Mathematical signatures — one formula per check

| # | Check | Formula / signal |
|---|---|---|
| 1 | Bandwagon | `B = #unverified universal claims / total claims`; cross-check "everyone / most people / majority believe" frequency against actual polling numbers |
| 2 | Authority misuse | `A = 1 − (#verified authority links / total authority mentions)` |
| 3 | Emotional appeal (pathos) | `E = Σ|emotion intensities| / token count`; threshold → emotion-laden |
| 4 | Strawman | `S = d(embedding(claim), embedding(original source))`; distance > threshold → strawman |
| 5 | Ad hominem | `H = #personal attack tokens / total tokens` |
| 6 | Red herring | `R = 1 − topic coherence score` (LDA / BERTopic / embedding clusters); a sudden drop flags it |
| 7 | Slippery slope | `SS = max depth of implication chain` (count the depth of "if-then" / "will lead to" cascades) |
| 8 | Transparency | `T = #verifiable references / #total claims`; low T → low transparency |
| 9 | Cherry picking | `C = 1 − variance(reported)/variance(global)`; only extreme values cited → cherry picking |
| 10 | Data accuracy | `DA = 1 − (#fact mismatches / #claims)` against an external KB (Wikidata, fact-check APIs) |
| 11 | Logical flow | `LF = average_entailment_score` over a sentence-level entailment graph |
| 12 | Conflict / contradiction | `Conf = #contradictions / total sentence pairs` via pairwise NLI |

Normalise the resulting 12-dim vector `[B, A, E, S, H, R, SS, T, C, DA, LF, Conf]` to 0–1, then
`BiasScore = w₁·B + w₂·E + w₃·C + …`, with weights tuned by logistic regression / SVM / a neural
model against human-annotated labels.

Method per check:

| Check | Feature type | Method |
|---|---|---|
| Bandwagon | keyword + factual check | regex, polling APIs |
| Authority misuse | citation verification | NER + link check |
| Emotional appeal | sentiment / emotion | RoBERTa-Emotion |
| Strawman | cross-source distance | embedding diff |
| Ad hominem | profanity / personal attack | dictionary lexicon |
| Red herring | topic coherence | BERTopic |
| Slippery slope | conditional chain depth | dependency parse |
| Transparency | citation count | regex |
| Cherry picking | statistical distribution comparison | numerical extraction |
| Data accuracy | fact-check + Wikidata | FEVER, DeBERTa-NLI |
| Logical flow | sentence entailment | RoBERTa NLI |
| Conflict | contradiction detection | pairwise NLI |

```python
def analyze_article(text):
    claims     = extract_claims(text)
    sentiments = emotion_score(text)
    topics     = topic_model(text)
    entities   = ner(text)
    fallacies = {}
    fallacies["bandwagon"]        = detect_bandwagon(text, claims)
    fallacies["authority_misuse"] = detect_authority_misuse(text, entities)
    fallacies["emotional_appeal"] = sentiments
    fallacies["strawman"]         = detect_strawman(text)
    fallacies["ad_hominem"]       = detect_ad_hominem(text)
    fallacies["red_herring"]      = topic_coherence(text)
    fallacies["slippery_slope"]   = detect_conditional_chains(text)
    fallacies["transparency"]     = citation_ratio(text)
    fallacies["cherry_picking"]   = compare_stats(text)
    fallacies["data_accuracy"]    = fact_check(claims)
    fallacies["logical_flow"]     = coherence_score(text)
    fallacies["conflict"]         = contradiction_score(text)
    return fallacies
```

**The golden rule:** combine *mathematics* (statistics, probability, vector distances) +
*programming* (Python, NLP frameworks) + *linguistic reasoning* (fallacies and rhetorical
structures). That fusion is what produces a deterministic, scalable, enterprise-grade media bias
detection system.

**How the big players do it:** Google / Twitter / Meta — zero-shot NLI + embedding distance,
topic-drift monitoring, sentiment and propaganda models. PolitiFact / Snopes — automated claim
extraction and cross-referencing against knowledge graphs. Reuters / AP — strict citation
validation and statistical anomaly detection for cherry-picking.

### 12.2 The fallacy set and detection strategies

The full set `F` used by the classifier: strawman, ad_hominem, slippery_slope, red_herring,
circular_reasoning, false_dilemma, burden_of_proof, cherry_picking, hasty_generalization,
false_cause, appeal_to_authority, equivocation, no_true_scotsman, appeal_to_emotion, bandwagon.
(Plus loaded question, anecdotal evidence, appeal to tradition/novelty, false attribution,
motive fallacy, guilt by association, scapegoating, whataboutism, gaslighting — see §13.)

| Fallacy | Definition | Detection strategy |
|---|---|---|
| **Strawman** | Misrepresenting an opponent's stance to refute it | Two-step pattern: (1) identify reported speech / an introduced opposing claim — "some people say", "critics argue", "opponents claim", "it has been said" — (2) check whether the next sentence dismisses it with a refutation cue ("but", "however", "yet", "in reality"). Measure *paraphrase distance* between the actual position and how it's presented; flag arguments attributed to a vague group where the stated claim is absurd; note absence of any genuine counterpoint. NLI: treat "some say X" as premise and the author's counter as hypothesis — contradiction indicates a strawman refutation. |
| **Ad Hominem** | Attacking the person, not the argument | Toxicity model (Perspective API, `unitary/toxic-bert`) run on sentences containing PERSON entities; insult lexicon `["idiot","stupid","liar","fool","corrupt","ignorant","crazy"]` near a name; dependency pattern `[Person] + copula + [insult]` ("He is a fraud"); insult density relative to length; subtler character attacks and insinuations ("Of course he would say that, he's a banker"). Rule: `if toxicity_score > 0.9 and PERSON in sentence_ents: flags["ad_hominem"] = True` |
| **Slippery Slope** | A minor step inevitably leads to an extreme outcome without evidence | Detect causal chains and conditional cascades ("if we allow A, then B, and eventually Z"); unusual frequency of conditional connectors (if, then, leads to, results in) near extreme-outcome words (disaster, chaos); future-tense/modal verbs ("will surely") tied to escalating scenarios; the argument graph showing a chain of claims with little evidence; frame semantics identifying the initial trigger and the final outcome; NLI check on whether X truly entails Y (a leap shows up as neutral/low-confidence entailment) |
| **Red Herring** | Diverting to an irrelevant topic | Topic-shift detection: LDA outlier topic in one paragraph; segment embeddings (Sentence-BERT) where a segment's similarity to the main topic is very low (<0.2); abrupt change in named entities/keywords with the new entity never revisited; low coherence between adjacent segments; cue phrases "By the way…", "Interestingly…"; NLI returning "neutral" (irrelevant) against the article thesis. (SemEval's propaganda task merged Red Herring with Straw Man.) |
| **Cherry Picking / Suppressed Evidence** | Selecting only favourable evidence | Evidence count per claim; source diversity; `evidence_support_ratio`; flag when supporting facts ≥1 and opposing = 0; viewpoint-diversity score very low; stance-classify each sentence toward the main topic and flag when `pro > 0 and con == 0` (or the reverse). The rigorous version compares against an external baseline / knowledge graph to identify omitted studies. |
| **False Cause (post hoc)** | Correlation treated as causation | Causal connectors (because, therefore, hence, due to, consequently) linking events with no proven mechanism; `"because"` connecting two past-tense clauses (chronological correlation misused as causation); temporal-only linkage ("after X, Y happened, so X caused Y"); singular-cause phrases ("the sole reason", "nothing else but"); metric `temporal_link_count` vs `explicit_cause_count`; SRL/OpenIE for cause-effect extraction; NLI as a causal consistency check. Propaganda taxonomy calls this **Causal Oversimplification**. |
| **Equivocation** | The same term used in two different senses | Detect polysemous key terms; compute the term's contextual embedding at each occurrence and cluster — two clusters means two senses. Or WSD (pyWSD, NLTK WordNet) per occurrence. Example: "public interest" used first as curiosity, later as public benefit. Hard to fully automate; a placeholder flag is acceptable. |
| **Bandwagon (Appeal to Popularity)** | True/good because everyone believes it | Lexicon `["everyone","everybody","all of us","most people","the people","the majority"]` matched with spaCy `PhraseMatcher`; `bandwagon_score = count / len(doc)`; threshold. Enhancement: check dependency context ("[most people] think") to confirm it's used as a persuasion device. A transformer classifier can output a bandwagon probability as an alternative score. |
| **Appeal to Authority (misused)** | Leaning on authority instead of evidence | NER for titled persons ("Dr. X", "Professor Y", "Senator") plus generic "experts", "scientists say", "research shows"; dependency parse to see whether the authority is used *as* the evidence; a window search for reporting verbs ("said", "claims", "according to"); cross-verify the authority's domain against the claim (a medical doctor cited on climate policy = misuse) via a knowledge base / Wikipedia API |
| **Appeal to Emotion** | Emotional rhetoric replacing argument | Reuse the emotional-appeal flag; high fear/anger relative to neutral content and low factual evidence; fear-appeal keyword list ("dangerous", "catastrophic", "terrifying"); zero-shot {emotional, factual} classification |
| **False Dilemma / Black-and-White** | Only two options presented when more exist | either/or constructions; phrases "either", "no other", "only if", "the only way", "with us or against us", "no other choice", "no alternative", "either way", "only option", "no middle ground", "we have no choice but to…"; absence of nuance words ("maybe", "sometimes", "partial"); modality diversity (only absolute modals must/never/always with no hedging); extreme antonym pairs (good/evil). It is a labelled category in propaganda datasets. |
| **Hasty Generalization / Overgeneralization** | Broad conclusion from a small or unrepresentative sample | Universal quantifiers ("all", "everyone", "no one", "none", "always", "never") used to generalize, especially right after a single narrow example; flag a universal-quantifier sentence lacking nearby evidence cues ("for example", "such as", "data", "study"); ratio of the mentioned sample size to the described population (1 : N). CAMPFIRE's canonical example: *"My cat is black, so all cats are black."* |
| **No True Scotsman** | Counterexamples defined away to protect a universal claim | Phrase patterns "no true [group] would…" — e.g. "No true patriot would criticize the war" |
| **Burden of Proof Shift** | The claimant demands others disprove | "can you prove that I'm wrong?", "nobody has proven X false, so it's true"; search for "prove" in challenge contexts |
| **Circular Reasoning / Begging the Question** | The conclusion restates the premise | Argument-graph cycle, or a claim node supporting itself with no independent evidence; high semantic similarity between the conclusion sentence and a premise sentence; split on "because"/"since" and measure similarity of the two sides (`difflib.SequenceMatcher > 0.7`, better with WordNet or embedding similarity); tautological phrases ("it is what it is"); a QA probe — ask "Why does the author claim X?" and if the answer is basically X, it's circular. Example: *"We must trust the leader because he is trustworthy."* |
| **Loaded Question** | A question embedding an unproven assumption | Question sentences containing a presupposition ("Have you stopped wasting money?") |

### 12.3 Reference detection snippets

```python
# Bandwagon
bandwagon_terms = ["everyone", "everybody", "all of us", "most people", "the majority"]
count = sum(1 for token in tokens if token.lower_ in bandwagon_terms)
bandwagon_score = count / len(tokens)
if bandwagon_score > 0.001:                       # threshold; 0.01 also used in places
    flags["bandwagon_effect"] = True
```
```python
# Appeal to authority
for ent in doc.ents:
    if ent.label_ == "PERSON" and ent._.has_title:          # custom attr set during NER
        window = doc[max(0, ent.start-3): min(len(doc), ent.end+10)]
        if re.search(r"\b(said|claims?|according to)\b", window.text, re.IGNORECASE):
            authority_references.append(window.text)
if authority_references:
    flags["authority_misuse"] = True
```
```python
# Ad hominem — lexicon near a PERSON, plus a toxicity model
insults = ["idiot", "stupid", "liar", "fool", "corrupt", "ignorant", "crazy"]
for ent in doc.ents:
    if ent.label_ == "PERSON":
        window = doc[max(0, ent.start-3): min(ent.end+3, len(doc))]
        if any(token.lower_ in insults for token in window):
            flags["ad_hominem"] = True

toxic_model = pipeline("text-classification", model="unitary/toxic-bert")
for sent in doc.sents:
    if toxic_model(sent.text)[0]['score'] > 0.9 and \
       'PERSON' in [e.label_ for e in sent.ents]:
        flags["ad_hominem"] = True
```
```python
# Red herring — embedding distance from the main topic
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
sentences  = [s.text for s in doc.sents]
embeddings = model.encode(sentences)
main_emb   = embeddings[0]
for i, emb in enumerate(embeddings[1:], start=1):
    if util.cos_sim(main_emb, emb) < 0.2:
        flags["red_herring"] = True
        break
```
```python
# Circular reasoning
import difflib
for sent in doc.sents:
    if 'because' in sent.text.lower():
        conclusion, premise = sent.text.split('because', 1)
        if difflib.SequenceMatcher(None, premise.strip().lower(),
                                   conclusion.strip().lower()).ratio() > 0.7:
            flags["circular_reasoning"] = True
```
```python
# Contradiction detection (pairwise NLI, restricted to related sentences)
model = AutoModelForSequenceClassification.from_pretrained("roberta-large-mnli")
tokenizer = AutoTokenizer.from_pretrained("roberta-large-mnli")
sentences = [s.text for s in doc.sents]
contradictions = 0
for i in range(len(sentences)):
    for j in range(i+1, len(sentences)):
        if any(ent in sentences[j] for ent in re.findall(r"[A-Z]\w+", sentences[i])):
            pair = tokenizer(sentences[i], sentences[j], return_tensors='pt', truncation=True)
            logits = model(**pair).logits
            if logits.argmax().item() == 2:        # 0=entailment 1=neutral 2=contradiction
                contradictions += 1
if contradictions > 0:
    flags["contradiction"] = True
```
> ⚠ **Label-index caution:** the MNLI label order differs between models and between the two
> code samples in the source material (one uses 0=entailment/1=neutral/2=contradiction, another
> uses 0=contradiction/1=neutral/2=entailment). **Always read `model.config.id2label`.**

```python
# Logical-flow coherence via adjacent-sentence similarity
model = SentenceTransformer('all-MiniLM-L12-v2')
sens = [s.text for s in doc.sents]
cos_sims = [float(util.cos_sim(model.encode(sens[i]), model.encode(sens[i+1])))
            for i in range(len(sens)-1)]
avg_sim = sum(cos_sims) / len(cos_sims) if cos_sims else 1.0
flags["logical_flow"] = not (avg_sim < 0.1 or min(cos_sims) < LOW_THRESHOLD)
```

### 12.4 The formal fallacy model (severity, confidence, disruption)

Each detected instance is a tuple `(fallacy_type, text_span, s, c, ℓ)`:

- `text_span` — the exact excerpt containing the fallacious reasoning
- `c ∈ [0,1]` — **confidence**: the classifier's probability for that type
- `s ∈ [0,1]` — **severity**: how severely it attempts to mislead or manipulate
- `ℓ ∈ [0,1]` — **logical flow disruption**: how much it breaks the argument's coherence

```
fallacy_present(S_i) = 1{ max_{f∈F} P(f|S_i) > τ }
fallacy_type(S_i)    = argmax_{f∈F} P(f|S_i)

severity   s = c × I_emotional × I_repetition × …        (each I normalized to [0,1],
                                                          defaults to 1 when N/A)
   simpler  s = c × w_f                                   (w_f = per-type base weight,
                                                          e.g. w_slippery = 0.7, w_fear = 0.9)
   capped at 1.0

document-level accumulation over n_f instances of type f:
             severity_f = 1 − exp(−n_f)

disruption  ℓ = max_i ( s_i × d_{f_i} )                  d_red_herring = 1.0 (directly diverts)
                                                          d_hasty_generalization = 0.5
coherence score = 1 − ℓ         (ℓ = 0 when no fallacies; a floor above 0 when any exist)
```

**Thresholding**: a global τ — 0.8 for high precision (be very sure before accusing a text),
0.5 for recall. τ can vary per type: require higher confidence for False Cause (harder to
detect) than for a keyword-obvious Ad Hominem.

**Rule/ML fusion**: `c = max(c_ML, c_rule)` per type. If multiple types fire on the same span,
take the highest confidence, or report both when they are conceptually different. If the model is
unsure (many outputs ~0.4), either report nothing (avoiding false positives) or label the span
"Unclear fallacy" with low confidence for analyst review.

**Calibration**: apply temperature scaling or Platt scaling on a validation set so `c` is a true
probability; then `c > 0.5` = moderate evidence, `c > 0.8` = strong evidence. Target severities:
a minor infraction (slight exaggeration, borderline false cause) ≈ 0.3; egregious manipulation
(a blatant fear appeal with strong language) ≈ 1.0. Repetition matters — using Ad Hominem five
times indicates a more systematically fallacious argument than using it once.

### 12.5 Implementation and scaling

Hybrid: rule-based cues **plus** a Transformer sequence classifier. Fine-tune `roberta-base` or
`deberta-v3-large` on a logical-fallacy dataset (Jin et al.); `distilroberta-base` if speed
matters. Complexity is O(N_s · L) per document — 30 sentences × 1M documents = 30M
classifications, so batch 32–64 sentences on GPU.

Optimisations: pre-filter with rules to skip obviously non-fallacious sentences (~50%);
distributed inference (TensorFlow Serving, PyTorch + DeepSpeed, or chunked multi-GPU); a FAISS
similarity cache so duplicate sentences across articles are not re-embedded/re-classified.

```python
weight = fallacy_severity_weights.get(f_type, 1.0)     # {"Ad Hominem":0.8,"Red Herring":0.9,…}
severity = conf * weight
sent_feat["severity"] = round(min(severity, 1.0), 3)

disruption_weight = fallacy_disruption_weights.get(f_type, 1.0)
sent_feat["logical_flow_disruption"] = round(min(severity * disruption_weight, 1.0), 3)
sent_feat["fallacy_span"] = sent_feat["text"]          # refine via token attributions/attention
```

Document-level aggregation produces a `fallacy_vector`, e.g.
`{"Ad Hominem": 2, "Strawman": 1, …}` (counts, or summed severities).

### 12.6 Validation

- Quantitative evaluation on the Jin et al. logical-fallacy dataset (precision/recall per type).
- Synthetic test cases per type — e.g. *"Opponent: We should improve public transport.
  Response: So you want to bankrupt the city by giving out free rides to everyone?"* must tag
  "you want to bankrupt the city…" as Strawman with `fallacy_present = True` and that exact span.
- False-positive check: run on factual, high-quality editorials and academic text — the detector
  should output no spans (or only very low confidences). If it flags something incorrectly,
  adjust the threshold or refine features.
- Inter-annotator agreement: have human experts label a sample of system outputs
  correct/incorrect to estimate accuracy.
- Maintain a small benchmark set of paragraphs with known fallacies (debate transcripts, forums)
  to track whether a code or model change improves detection.

### 12.7 Integration notes

Fallacy spans often coincide with propaganda techniques (Name-calling ≈ Ad Hominem) — the
modules must **share signals to avoid double counting or conflicting output**. Each detection
provides a clear explanation point: *"This looks like an X fallacy (confidence 90%)"*, shown on
the dashboard. Confidence and severity feed the aggregate manipulation score. The module depends
on good sentence segmentation and sometimes coreference (to resolve "this proposal" vs "that").

Storage: per document store `{fallacy_type, span_text, sentence_id, confidence, severity}`.
Storing detailed spans for millions of documents is heavy — always store the aggregated counts
and a "any fallacy present" indicator for quick filtering, and keep detailed spans only for a
subset (recent articles, or those with high manipulation scores).

Runtime: fallacy detection is costly, so it runs in batch, not in a live on-demand API — unless
powerful GPUs are available. For a real-time check (a journalist pasting a paragraph), run a
distilled model.

---

## 13. Propaganda and rhetorical technique detection

### 13.1 The technique set and quantities

`P` = {name_calling, loaded_language, glittering_generalities, fear_appeal,
appeal_to_prejudice, flag_waving, whataboutism, repetition, oversimplification, exaggeration,
minimization, obfuscation, thought_terminating_cliche}.
(The 13 media-analysis techniques targeted elsewhere in the design: Loaded Language, Name
Calling, Glittering Generalities, Card Stacking, Bandwagon, Appeal to Fear, Appeal to Authority,
Plain Folks, Testimonial, Transfer, Guilt by Association, Scapegoating, False Dilemma.)

Per technique p:

```
frequency(p)  = f_p = Σ_i I_p(S_i)                         # sentences using p
intensity(p) ∈ [0,1]                                       # how blatant the usage is
transparency_violation(p) = min(1, u_p × intensity(p) + α × f_p / N_s)

  u_p = the technique's inherent dishonesty weight
        (u_obfuscation = 1.0; u_glittering_generalities = 0.7)
  α   = tuning parameter for the frequency contribution

PropScore = 1 − Π_{p∈P} (1 − v_p)          v_p = transparency_violation(p)
```
`PropScore` tends to 1 if any single technique is high and is 0 when none are present.
**Calibration target:** an ordinary news article scores 0.1–0.2; known propaganda (state-
sponsored disinformation) scores above 0.8.

Intensity examples: loaded language — `IN_loaded(s) = W_loaded(s) / N_s` (proportion of loaded
words), document intensity = `max_s IN_loaded(s)` or a weighted average; repetition — intensity
∝ repeat count normalised (e.g. count/10, capped at 1).

**Normalization**: frequency ÷ document length so a 100-word social post and a 2000-word article
compare fairly. Calibrate intensity so one strong word in a sentence ≈ 0.5 and a sentence packed
with slurs/emotional adjectives > 0.8. Use a log or saturating scale for heavy repetition —
20 repeats is not subjectively twice as bad as 10 (diminishing returns).

Output shape:
```json
{ "technique": "Loaded Language", "intensity": 0.9,
  "text_span": "brutal regime of ruthless…", "frequency": 3,
  "transparency_violation": 0.85 }
```

### 13.2 Per-technique detection

**Loaded Language** — high density of adjectives/adverbs with strong emotional connotation
("disastrous failure", "glorious triumph", "ridiculous policy"); high sentiment magnitude and
variance. `Loaded Language Score` = % of words in a loaded lexicon
`{"disaster","outrageous","shameful","triumphant","so-called","ridiculous"}`, typically flagged
above 3–5%; a complementary sentiment method counts sentences with `|polarity| > 0.5`.
**Easiest propaganda class to detect** because of its clear lexical signature; SemEval 2020
Task 11 provides span-level training data. Example: *"This brutal policy is an assault on our
rights."*
```python
loaded_count = sum(1 for t in doc if t.text.lower() in loaded_lexicon)
if loaded_count / len(doc) > SOME_THRESHOLD:
    flags["loaded_language"] = True
polarities = [TextBlob(s.text).sentiment.polarity for s in doc.sents]
if sum(1 for p in polarities if abs(p) > 0.5) > X:
    flags["loaded_language"] = True
```

**Name Calling / Labeling** — a derogatory noun or label attached to a person or group; nickname
epithets ("Crooked X"). Patterns `[Entity] is a [label]` and `[Entity], a [label],` using spaCy
NER (PERSON/ORG/NORP) plus dependency; lexicon
`{"liar","hypocrite","idiot","buffoon","criminal","crook"}`; Hatebase for slurs. Overlaps with
ad hominem, and for groups ("All [group] are traitors") with overgeneralization. Political
labelling ("socialist", "elitist" used pejoratively) needs context — tone or pairing with
negative adjectives usually clarifies.
```python
for ent in doc.ents:
    if ent.label_ in ["PERSON", "ORG", "NORP"]:
        end = ent.end
        if end < len(doc) and doc[end].lemma_ == "be":                 # "[Entity] is a [label]"
            if end+1 < len(doc) and doc[end+1].lemma_.lower() in name_calling_labels:
                flags["name_calling"] = True
        if end < len(doc) and doc[end].text == ",":                    # "[Entity], a [label],"
            if end+2 < len(doc) and doc[end+1].lemma_ in ["a","an","the"] \
               and doc[end+2].lemma_ in name_calling_labels:
                flags["name_calling"] = True
```

**Glittering Generalities** — vague positive virtue words (freedom, liberty, justice, honor,
integrity, prosperity, unity, progress) evoking approval without specifics, often in slogans.
Rule: ≥2 virtue words in a sentence under 15 words → flag; or a single virtue word with no
elaboration cue ("because", "for example", "such as") → flag. Related dataset category:
*Slogans*. Example that trips it: "Fighting for Freedom and Justice!"; example that shouldn't:
"We need economic justice because current disparities…".

**Whataboutism** — deflecting criticism by raising a different issue. Hallmark: a sentence
beginning "What about" / "And what about" / "How about"; also tu quoque ("You criticize X, but
you do Y" / "you did Y as well"). The literal phrase catch covers most cases; optionally compare
the nouns in the question against the prior context — largely disjoint confirms a topic change.

**Repetition** — count 3-grams across the document with a `Counter` and flag phrases appearing
≥3 times.

**Appeal to fear / prejudice, flag-waving, oversimplification, exaggeration, minimization,
obfuscation, thought-terminating clichés** — keyword and pattern rules plus the ML classifier;
flag-waving is detected via country/national symbols with valorizing language ("our great nation
must…"); thought-terminating clichés via phrases like "it is what it is".

**Guilt by Association** — "X is connected to Y (bad thing), therefore X is tainted". Markers:
"ally of", "associated with", "linked to", "connected to", "in the same camp as", "ties to",
combined with a vilified entity (Hitler, Nazis, terrorist, criminal, mafia). *Reductio ad
Hitlerum* ("He's the next Hitler") is the extreme form — any comparison to Hitler/Nazi is
practically always this fallacy. Implementation: split the sentence on the association term and
check the entities either side against a bad-entity list; better with dependency (proper-noun
subject + associate/link verb + prepositional object).

**Scapegoating** — a group repeatedly blamed for problems. High co-occurrence of a group name
with negative verbs (caused, ruined, responsible for) and problem words (crime, unemployment,
crisis, job loss, fault). For each ORG/NORP/GPE entity, count sentences containing blame phrases
("blame", "responsible for", "cause of", "fault of") or problem words; flag when the count for
the same target ≥2 and record `metadata["scapegoat_target"]`. Targeted sentiment analysis is the
stronger model-based route; overlaps with hate speech. Note that scapegoating typically has
exaggerated breadth — one group blamed for many separate issues.

**Card Stacking** — presenting only information favourable to one side. Signals: asymmetric
sentiment by entity (one side all positive, the other all negative), no counter-argument
acknowledged, all sources from one side. Implementation: build an entity-sentiment map and flag
when `max(avg_sentiment) > 0.5 and min(avg_sentiment) < -0.5`. Overlaps with cherry-picking and
omission bias.
```python
entity_sentiment = {}
for ent in doc.ents:
    if ent.label_ in ["PERSON","ORG","NORP"]:
        polarity = TextBlob(ent.sent.text).sentiment.polarity
        entity_sentiment.setdefault(ent.text, []).append(polarity)
avg_sent = {e: sum(v)/len(v) for e, v in entity_sentiment.items()}
if len(avg_sent) >= 2 and max(avg_sent.values()) > 0.5 and min(avg_sent.values()) < -0.5:
    flags["card_stacking"] = True
```

**Gaslighting** — making someone doubt their own perception. Phrase list: "you're being
paranoid", "you're crazy", "that never happened", "you're imagining things", "don't be so
sensitive", "no one will believe you", "you're overreacting", "it's all in your head". Flag even
when the article is *quoting* someone else gaslighting — the engine's goal is to detect the
presence of the tactic in the content, whoever is using it.

**Anecdotal Evidence** — personal stories or isolated examples used as proof. Markers:
"I remember", "we once", "one time", "a story", "a case where", "In my experience", "A friend of
mine", first-person pronouns, past-tense narrative style. Flag when an anecdote sentence is
followed by a generalizing sentence ("therefore", "this shows", "thus", "all", "everyone"). NLI:
anecdote as premise, general claim as hypothesis → "neutral" means the claim isn't proven.

**Appeal to Tradition / Appeal to Novelty** — tradition markers ("tradition", "traditional",
"time-honored", "long-standing", "ages") or novelty markers ("new", "innovative", "cutting-edge",
"latest", "modern") co-occurring with a positive-evaluation word (good/better/best/superior/must,
improved/excellent) — i.e. "traditional = good" or "new = good" used as the reason. Simple but
prone to over-flagging ("traditional dish" in a neutral context); refine by requiring
argumentative usage ("because it's traditional").

**False Attribution** — citing a source that is misquoted, out of context, or not actually
supportive. Clues: quotes with no clear speaker (`"…"` with no `— Name` or "said [Name]"); famous
names cited for things they never said; authority names used outside their expertise or
timeline. Implementation: NER around quotation marks and "According to X"; verify quotes
externally (Wikiquote API, search); maintain a database of known misattributed quotes.

**Motive Fallacy (questioning motives)** — dismissing an argument by attacking the arguer's
motive. Markers: "only because", "just because", "only want", "agenda", "vested interest", "for
your own gain", combined with a person/group pronoun. Dependency version: a "because" clause
whose subject is you/they and whose content is a motive (money, power, fame). Catches: *"He
supports the policy only because he's paid to."*

**Transparency Gaps** — important details about sources, data or methods omitted. Metric:
**attribution ratio** = the fraction of factual statements containing an explicit source. Rules:
flag sentences matching "It is said that…", "Some people claim…", "Studies show…", "Experts
believe…" with no named study or person; count passive constructions with no agent.
```python
passive_count = textstat.passive_voice_count(text)
unattributed = sum(
    1 for s in sentences
    if re.search(r"\b(study|experts?|research|report)\b", s.lower())
    and not re.search(r'\b(according to|said|stated)\b.*[A-Z]\w+', s)
)
transparency_gap_score = unattributed / len(sentences)
if transparency_gap_score > 0.2 or passive_count > X:
    flags["transparency_gaps"] = True
```

**Source Opaqueness** — specifically about citations. Metric: **Unnamed Source Count** — vague
references ("experts say", "observers say", "analysts believe", "a source close to X", "it has
been reported", "reportedly", "sources say", "according to a study/report/source") vs named
attributions ("said [Name]"). Flag when opaque > 0 and named = 0, or when opaque > named.

**Conflict of Interest** — mostly metadata, not text. Textual signs: no disclosure statement
where one is expected; first-person plural referencing an organisation ("we at Company X") in an
ostensibly neutral article; unusually promotional language toward an affiliated entity. Requires
a knowledge base of author/outlet affiliations and ownership (MediaBiasFactCheck, Wikidata):
`knowledge_base.is_affiliated(author, topic_entity)`. Treated as a separate meta-analysis
component.

**Omission Bias** — presenting information in a way that omits crucial facts. Requires
multi-document analysis: gather related articles (news API/search), extract named entities and
events from each, and diff — entities/events present in others but missing here are candidate
omissions, recorded in `metadata["omitted_points"]`. Within-document proxy: a high
claim-to-evidence ratio implies omitted supporting context. Another indirect check: whether the
piece answers the basic journalistic questions (who, what, where, when, why, how).

**Statistical Manipulation** — statistics used misleadingly. Signs: a percentage with no
denominator or timeframe; big numbers with no unit or baseline ("up 300%!"); cherry-picked
timeframes ("record-breaking" without stating the window); inconsistent mixing of percentages
and absolutes. Implementation: regex-extract all numbers and percentages; require a context cue
near a percentage (of / out of / in / from / than) and a unit or descriptor near a raw number
(year, people, dollar, vote, cases, km); percentage-sum check.

**Framing Bias** — differing language for the two sides; loaded synonym choices ("rioters" vs
"protesters", "illegal aliens" vs "undocumented immigrants", "climate crisis" vs "climate
alarmism", "gun safety" vs "gun control", "freedom fighters" vs "terrorists"). Implementation:
topic-specific frame lexicons; check whether only one frame's vocabulary appears
(`frame: positive_only` / `negative_only`); advanced — summarise the article and compare against
a neutral summary (Wikipedia) via NLI/embeddings; LIWC categories to reveal a fear frame.

**Narrative Inconsistency** — timeline or behaviour that doesn't add up; events out of
chronological order; an entity's story changing mid-article. Implementation: temporal extraction
(HeidelTime, SUTime, spaCy), build a timeline and compare the narrated order against the
chronological order; coreference to track entities; NLI between earlier and later parts. Largely
subsumed by contradiction detection and coherence metrics.

**Coherence Drop** — a section suddenly becomes harder to follow, possibly where filler or
propaganda was inserted. Implementation: GPT-2 perplexity per sentence, flagging a sentence whose
perplexity is >2× the previous one *and* above an absolute threshold; readability (Flesch) in a
sliding window; BERT next-sentence probability; local minima in Sentence-BERT adjacent
similarity.
```python
model = GPT2LMHeadModel.from_pretrained("gpt2")
perp_scores = []
for sent in sents:
    inputs = tokenizer(sent, return_tensors='pt')
    loss = model(**inputs, labels=inputs["input_ids"]).loss
    perp_scores.append(float(torch.exp(loss)))
for i in range(1, len(perp_scores)):
    if perp_scores[i] > 2 * perp_scores[i-1] and perp_scores[i] > SOME_THRESHOLD:
        flags["coherence_drop"] = True
        break
```

**Claim-to-Evidence Ratio** — `ratio = count_claims / max(1, count_evidence)`; > 3 flags. Claim
heuristic: a sentence with a linking verb, number, percent or "million". Evidence heuristic: the
sentence contains a quotation mark, "according to", or mentions data/study/report/source. Stored
as `metadata["claim_evidence_ratio"]`.

**Unsupported Quantifiers** — many, most, numerous, several, a lot of, countless, few. Flag an
occurrence when the sentence contains no number, %, "according to", "study" or "report".
"Many (37%) of respondents" is correctly not flagged. Overlaps with bandwagon and transparency
gaps — **double-flagging across categories is acceptable.**

**Hedging Signals** — may, might, could, perhaps, possibly, suggests, "it is possible", "up to",
"as much as", "could mean". `hedge_density = hedge_count / total tokens`; > 0.02 (2 per 100
words) flags. **Not inherently manipulative** — hedging can be a sign of honest journalism — so
it is tracked as style and scored differently from a fallacy (weight ~0.05 or excluded).

### 13.3 Implementation approach

Rules first (regex/keyword for slogans, "what about", insult lists, loaded-word density >20% of
a sentence), then repetition via the 3-gram counter, then a multi-class/multi-label transformer.
SemEval-2020 Task 11 suggests a two-step approach: **span detection**, then **technique
classification** on those spans (`bert-base-cased` / `roberta-large`; distilBERT if speed-bound).
Pre-scan with rules to select candidate sentences for the model. Use a FAISS cache of known
propagandistic phrase embeddings so recurring slogans are flagged by nearest-neighbour lookup
instead of re-inference.

```python
propaganda_flags = {tech: {"count": 0, "spans": []} for tech in P}

for sent in doc_data["sentences"]:                       # 1. rule-based cues
    text = sent["text"].lower()
    if "what about" in text or "how about" in text:
        propaganda_flags["whataboutism"]["count"] += 1
        propaganda_flags["whataboutism"]["spans"].append(sent["text"])
    for insult in ["idiot", "racist", "ignorant"]:
        if f" {insult}" in text:
            propaganda_flags["name_calling"]["count"] += 1
            propaganda_flags["name_calling"]["spans"].append(insult)
    loaded_count = sum(1 for w in text.split() if w in loaded_words_set)
    if loaded_count / len(text.split()) > 0.2:
        propaganda_flags["loaded_language"]["count"] += 1
        propaganda_flags["loaded_language"]["spans"].append(sent["text"])

from collections import Counter                          # 2. repetition
phrases = Counter()
for sent in doc_data["sentences"]:
    words = sent["text"].lower().split()
    for i in range(len(words)-3):
        phrases[" ".join(words[i:i+3])] += 1
for phrase, count in phrases.items():
    if count >= 3 and len(phrase.split()) > 1:
        propaganda_flags["repetition"]["count"] += 1
        propaganda_flags["repetition"]["spans"].append(phrase)

# 3. ML classification for cases needing context (e.g. flag_waving)
for sent in doc_data["sentences"]:
    probs = technique_model(**technique_tokenizer(sent["text"], return_tensors='pt',
                                                 truncation=True)).logits.softmax(dim=1)[0]
    label_idx = int(probs.argmax())
    if label_idx != 0 and float(probs[label_idx]) > 0.8:
        tech = technique_model.config.id2label[label_idx]
        propaganda_flags[tech]["count"] += 1
        propaganda_flags[tech]["spans"].append(sent["text"])
```
(A sentence may use several techniques, so a multi-label head with sigmoid outputs is more
appropriate than single-label softmax.)

Intensity and transparency-violation computation:
```python
for tech, info in propaganda_flags.items():
    if info["count"] == 0:
        continue
    if tech == "loaded_language":
        intensity = max(sum(1 for w in span.split() if w.lower() in loaded_words_set)
                        / len(span.split()) for span in info["spans"])
    elif tech == "repetition":
        max_phrase = max(info["spans"], key=lambda ph: phrases[ph])
        intensity = min(1.0, phrases[max_phrase] / 10.0)
    else:
        intensity = min(1.0, info["count"] / 5.0)          # 5+ occurrences saturates
    base_violation = transparency_weights.get(tech, 0.8) * intensity
    trans_violation = min(1.0, base_violation
                          + 0.2 * info["count"] / len(doc_data["sentences"]))
```

### 13.4 Thresholds, edge cases, validation

- Intensity must exceed ~0.2 to be noteworthy; a single mild loaded word should not be listed.
- **Avoid double-penalising**: if a span is already scored as a fallacy with severity, reduce its
  propaganda transparency_violation so the impact is not counted twice.
- **False positives**: genuinely emotional contexts (a tragic news story using "heartbreaking")
  look like loaded language but are not propaganda. Mitigate with topic/intent context checks —
  propaganda typically co-occurs with political topics and persuasive intent.
- Technique weighting: Glittering Generalities is propaganda but relatively benign in deception
  terms, so its transparency_violation stays moderate; Whataboutism actively evades
  accountability and gets a higher base violation. Weights are set with expert input, or learned
  by regressing rated articles.
- Validation: SemEval-2020 Task 11 dev/test (realistic span-detection F1 is 0.4–0.6); manual
  review across the political spectrum; frequency-distribution sanity checks (if
  thought-terminating cliché never fires, test "it is what it is"; if loaded language fires on
  nearly every article, tighten the criteria); cross-check overlap with the fallacy module;
  neutral Wikipedia text → near-zero, wartime propaganda → high.

---

## 14. Linguistic bias analysis

Linguistic bias is about **how** information is presented rather than **what** is said. Three
subcategories: **Framing Bias**, **Source & Attribution Bias**, **Lexical Bias**.

Output per bias instance:
```python
{
  "bias_type": str,             # "Framing Bias" | "Attribution Bias" | "Lexical Bias"
  "polarity": float,            # [-1,1]; negative = bias against / negative portrayal
  "affected_entities": [str],   # which entities or groups are impacted
  "linguistic_markers": [str],  # the specific words/phrases indicating the bias
  "transparency_score": float,  # [0,1]; 1 = fully transparent/unbiased language
}
```

### 14.1 Phenomena captured

- **Positive/negative framing** — asymmetric sentiment per entity: one group consistently
  described with positive words, the opposing group with negative words.
- **Asymmetric verb choice** — skeptical reporting verbs `{claimed, alleged, admitted}` vs
  neutral `{said, stated, according}`. Bias when one entity predominantly receives the skeptical
  verbs.
- **Hedging** — count hedges and note if they cluster around particular claims (downplaying
  commitment selectively).
- **Presuppositions** — triggers such as "stop", "continue", "again" ("When did X stop doing
  Y?" presupposes X did Y).
- **Implicature** — implied meaning beyond the literal; partially detectable via semantic
  analysis and rhetorical questions.
- **Modal certainty** — an epistemic modality score per sentence: +1 for strong certainty
  ("must", "definitely", "clearly"), −1 for strong uncertainty ("maybe", "possibly",
  "arguably"). Uneven application across the two sides is the bias signal.
- **Quote imbalance** — `Q_entity` counts; one side quoted 10 times and the other 0 is coverage
  bias. Quantify as a ratio or difference.
- **Source credibility framing** — "According to reputable scientist Dr. A…" vs "so-called
  expert Dr. B…". Extract `[ADJ + noun]` patterns around named-entity attributions.
- **Active vs passive voice** — passive can hide who did an action ("protestors were shot" vs
  "police shot protestors"). `passive_ratio = passive_sentences / total_sentences`
  (spaCy: `token.dep_ == "nsubjpass"`, or tag `VBN`). Bias when passive clusters specifically on
  certain actors (e.g. always passive when one's own military causes harm).
- **Claim-evidence mismatch** — claims not followed by a quote, citation or further detail;
  compute the unsupported-claim ratio. Biased pieces assert without backup; balanced journalism
  provides sources.
- **Loaded adjectives/adverbs** — brutal, heroic, alleged, allegedly. Record which entity or
  action each describes. If Entity X is often near "brutal" and Entity Y near "heroic", that is
  clear bias.
- **Euphemisms vs dysphemisms** — euphemism = a mild term for a harsh reality ("enhanced
  interrogation" for torture); dysphemism = a harsh term for something neutral ("scheme" for
  plan).
- **Toxicity-weighted vocabulary** — insults or slurs indicate extreme bias; record the maximum
  toxicity or the fraction of sentences above a toxicity threshold.

### 14.2 Scoring

**Polarity** per entity: gather all words around the entity (same sentence or a window), sum
their sentiment/connotation values, normalize to [−1, 1]. If bias is not entity-specific
(narrative framing bias), `affected_entities` may be empty.

**Linguistic markers**: output the actual triggered words — e.g.
`["claims", "allegedly", "extremist"]`.

**Transparency**:
```
linguistic_transparency = 1 − γ₁·hedge_density − γ₂·loaded_word_density − γ₃·passive_ratio − …
```
each ratio normalized to [0,1], clamped at ≥ 0. It is 1 when language is neutral and clear and
decreases as bias markers accumulate.

### 14.3 Implementation

Rules and lexicons first, statistical modelling for subtler patterns. spaCy for dependency
parsing (passive voice, subject-object relations); NLTK/TextBlob/VADER for sentiment lexicons;
sklearn logistic regression for a biased-vs-neutral sentence classifier; hedge word lists from
linguistics research (or "weasel word" lists); `unitary/toxic-bert` or Perspective API for
toxicity; `nlptown/bert-base-multilingual-uncased-sentiment` for sentiment;
`roberta-large-mnli` to probe presuppositions/implicatures.

```python
# Framing bias via entity sentiment (VADER for the fast path)
sia = SentimentIntensityAnalyzer()
entity_sentiments = {}
for sent in doc.sents:
    vs = sia.polarity_scores(sent.text)
    for ent in doc.ents:
        if ent.text in sent.text:
            entity_sentiments[ent.text] = entity_sentiments.get(ent.text, 0.0) + vs["compound"]

for ent, score in entity_sentiments.items():
    polarity = max(-1.0, min(1.0, score))
    if abs(polarity) > 0.3:                       # threshold for noteworthy bias
        markers = [doc[t.i+1].text for t in doc
                   if t.text == ent and t.i+1 < len(doc) and doc[t.i+1].pos_ == "ADJ"]
        bias_outputs.append({"bias_type": "Framing Bias", "polarity": round(polarity, 3),
                             "affected_entities": [ent], "linguistic_markers": markers,
                             "transparency_score": None})

# Attribution bias via skeptical reporting verbs
reporting_verbs_skeptical = {"claimed", "alleged", "admitted"}
reporting_verbs_neutral   = {"said", "stated", "according"}
for sent in doc.sents:
    for token in sent:
        if token.lemma_ in reporting_verbs_skeptical:
            subj = [c.text for c in token.children if c.dep_ == "nsubj"]
            bias_outputs.append({"bias_type": "Attribution Bias", "polarity": -0.5,
                                 "affected_entities": subj, "linguistic_markers": [token.text],
                                 "transparency_score": None})

# Passive voice / agency hiding
passive_count = sum(1 for sent in doc.sents
                    if any(t.dep_ == "nsubjpass" for t in sent))
passive_ratio = passive_count / len(list(doc.sents))
if passive_ratio > 0.3:
    bias_outputs.append({"bias_type": "Attribution Bias", "polarity": 0.0,
                         "affected_entities": [], "linguistic_markers": ["passive_voice"],
                         "transparency_score": None})
```

### 14.4 Thresholds, calibration, validation

- Do not emit a finding for 1–2 mild loaded words in a long article. Require e.g. >20% loaded
  words in a sentence, or repeated occurrences.
- Skeptical verbs are only flagged when repeatedly aimed at the same entity (>2 instances) — one
  "claimed" among many "said"s is not bias.
- **Genre edge case**: opinion pieces intentionally use strong language. If metadata says
  `section = Opinion`, lower the severity — the bias is expected and acceptable there.
- Polarity calibration: a neutral article should sum to ~0 across entities; a known partisan
  article should show one politician at ~+0.8 and another at ~−0.8. Calibrate against known bias
  datasets (articles labelled left/right or pro/anti).
- Hedge calibration: `hedge_density > 5%` is significant; compare quality journalism against
  gossip blogs to set the level.
- Transparency calibration: compare against expert judgements of article clarity — if experts
  rate an article as very transparent but the score is low, the weights (e.g. the hedge penalty)
  are too harsh. Some hedging is normal, not deceitful.
- Avoid double-counting with the propaganda module: **the propaganda module focuses on presence
  and intensity of loaded language; the bias module focuses on its polarity/direction.** Both
  transparency numbers can be combined later (weighted average or max).
- Validation: paired case studies (one outlet's "freedom fighters" vs another's "terrorists" for
  the same group must produce opposite-polarity markers); statistical check that the top markers
  across a corpus are plausible bias words ("allegedly", "claims"); extreme scenarios — a clearly
  biased opinion piece must yield multiple bias outputs with low transparency and strong
  polarity, while a dry news report yields almost nothing.

Runtime: this module is fast (mostly rules/lexicons + VADER), so it can run in real time —
a few milliseconds per document for the lexicon scans, well under 0.5 s per document even with a
transformer sentiment model on CPU. Only the NLI-based implicature probing needs to be skipped
in a live path.

---

## 15. Factuality, truthiness and data accuracy

### 15.1 Metrics

| Symbol | Metric | Definition |
|---|---|---|
| `N_c` | Claim count | number of verifiable factual claims |
| `N_v` | Verified claims | claims backed by a citation, quote from a named expert, or reference to data |
| `r_vc` | Verified claim ratio | `N_v / N_c` (defined as 0 when `N_c = 0`, by convention) |
| `σ̄` | Mean claim specificity | `σ(s) = 1 − 1{vague phrasing or no proper nouns/numbers}` averaged over claims |
| `C_n` | Numerical consistency | 1 = no contradictions, 0 = blatant contradictions |
| `L_f` | Logical flow | coherence of the argumentation from a factual/logical standpoint |
| `M` | Misleading score | use of misleading techniques |
| `D` | Data quality | numeric data plausibility, consistency and contextualisation |
| `T` | Transparency | how open the article is about sources and methods |
| `F` | Factuality score | the overall aggregate |

### 15.2 Formulas

```
F   = w₁·r_vc + w₂·σ̄ + w₃·C_n + w₄·L_f + w₅·(1 − M) + w₆·D′
        (w₁, w₃, w₄ — evidence, consistency, coherence — carry the largest weights)

D   = (C_n + I_baselines + I_methodology) / 3
        I_baselines    = baseline/context provided for key numbers  (0 | 0.5 | 1)
        I_methodology  = methods or sample size mentioned for surveys/polls

T   = (r_vc + I_citations) / 2          I_citations = hyperlinks ÷ claims, capped at 1

M   = 1 − exp(−k · n_mislead)

C_n = 1 − (#numeric inconsistencies / #numeric claims)      clamped to ≥ 0
```

Concrete weights used in the reference implementation:
```python
contradiction_penalty = min(1.0, factuality["contradictions"] / 2)    # each contradiction hurts
misleading_penalty    = min(1.0, factuality["misleading_indicators"] / 5)
numeric_penalty       = min(1.0, factuality["numeric_issues"] / 3)

data_quality      = 1 - numeric_penalty
logical_flow      = 1 - contradiction_penalty
misleading_score  = misleading_penalty
transparency_score = (verified_ratio
                      + min(1.0, factuality["external_citations"] / max(1, claim_count))) / 2

factuality_score = (verified_ratio * 0.4
                    + (1 - misleading_penalty) * 0.2
                    + data_quality * 0.2
                    + logical_flow * 0.2)
```

### 15.3 Claim identification and verification

A claim is a sentence containing a digit, a date, a proper noun, "according to", or an assertive
factual verb. For each claim, `I_source(s) = 1` if the sentence or its neighbour contains an
explicit source (a URL, "according to", a named study, a quote from a named expert);
`N_v = Σ I_source(s)`.

Verification options: query an external knowledge base (Wikipedia API, DBpedia, Wikidata Query
Service, Google Fact Check Tool API, Diffbot KG); or use a FEVER-style model classifying
(claim, evidence) as Supported / Refuted / NotEnoughInfo — e.g. `uclnlp/bert-tiny-fever`,
`ynie/roberta-large-snli_mnli_fever_anli_R1_R2_R3-nli`; plus internal-consistency NLI with
`facebook/bart-large-mnli` or `roberta-large-mnli`.

### 15.4 Numeric checks

- Same-referent numbers differing significantly (>20% relative or >5 absolute) — "the budget was
  $5 million" vs "the budget was $7 million".
- Percentage lists summing outside 90–110% (allowing for rounding): "A 50%, B 30%, C 25%" = 105%.
- Out-of-range values: "age 200", "120% of the population", "1000% increase".
- Unit consistency: "10 km" and "6 miles" for the same distance must be convertible; at minimum
  ensure units are consistent or the change is made explicit.
- Ignore trivial differences (100 vs 101) — thresholds prevent naive false positives.
- Do **not** label something an outlier without context ("5 million attended" may be plausible).

```python
numbers = [(float(m.group()), full_text[max(0, m.start()-10): m.end()+10])
           for m in re.finditer(r'\b\d+(\.\d+)?\b', full_text)]
for j, (num1, ctx1) in enumerate(numbers):
    for k, (num2, ctx2) in enumerate(numbers):
        if k <= j: continue
        if set(ctx1.split()) & set(ctx2.split()):                 # same referent, roughly
            if abs(num1 - num2) > max(5, 0.2 * max(num1, num2)):
                factuality["numeric_issues"] += 1

if re.search(r'\b\d+%.*\d+%.*\d+%', full_text):
    percents = [float(p.strip('%')) for p in re.findall(r'\d+%', full_text)]
    if sum(percents) > 110:
        factuality["numeric_issues"] += 1
```

### 15.5 Misleading indicators

Universal quantifiers (always, never, everyone, no one, nobody, all of them) · unverifiable
phrases ("it is said", "people are saying", "many believe", "experts claim" with no name) ·
correlation stated as causation ("linked to"/"associated with" reinterpreted as "causes") ·
clickbait ("won't believe", "shocking", "secret revealed", "undisputed truth"). Count unique
*categories* of misleading pattern rather than raw occurrences, so repeated instances of the same
phrase don't inflate the score.

### 15.6 Complexity and scaling

Regex and counting are linear. The expensive part is pairwise NLI: O(N_c²) worst case — 20 claims
→ 190 pairs (fine); 100 claims → 4,950 pairs (heavy but still thousands, not millions).
Optimisations: only run NLI when contradiction cues exist (negations, antonyms); cluster claim
sentences by embedding and only compare within clusters; batch pairs across documents; and offer
a **graceful-degradation flag** that disables deep consistency checks for speed.

### 15.7 Edge cases, calibration, validation

- **An opinion piece with zero claims**: `r_vc` is undefined. Default `factuality_score` to 0.5
  ("neither factual nor unfactual") or handle opinion pieces separately via metadata.
- Don't over-punish domains that structurally don't cite (TV transcripts). Academic use-cases
  may weight citation much more heavily — the weighting can be domain-configured.
- Guidance: `factuality_score < 0.3` = very unreliable; `> 0.7` = quite factual.
- Validation: fact-checked-false articles must score low; synthetic contradictions ("Ten people
  attended the event." … "Twenty people attended the event.") must drop numerical consistency
  and register a contradiction; "That's 120% of the population." must flag; "According to a
  study by XYZ, coffee cures disease." → 1 claim, verified, high transparency; "Experts say
  coffee cures disease." → 1 claim, unverifiable phrase, low transparency.
- Distribution check on 1,000 random articles: if 90% score ~0.9 the criteria are too lax; if
  most score ~0.2 they are too strict. A slight skew toward high is expected since most
  mainstream articles are fairly factual.
- Cross-check that `logical_flow_score` correlates with the fallacy module — if the fallacy
  module found many logical issues, logical flow here should also be low. Conflict indicates a
  bug.

---

## 16. Entity-level sentiment and bias

Per named entity *E*, a profile:

| Field | Range | Meaning |
|---|---|---|
| `sentiment` S_E | [−1,1] | overall sentiment toward the entity |
| `toxicity` X_E | [0,1] | toxic language directed at or associated with them |
| `quote_count` Q_E | ℕ | how often they are quoted (how much voice they get) |
| `threat_association_score` T_E | [0,1] | how strongly they are linked to threat/fear terms |
| `framing_score` F_E | [−1,1] | empowering vs undermining language (verbs and roles) |
| `moral_valence` M_E | [−1,1] | hero ↔ villain spectrum |
| `conflict_involvement` | bool/float | whether they are portrayed as part of a conflict |

```
S_E = (1/N_E) · Σ_mentions sentiment(context around mention_i)          clipped to [−1,1]

X_E = 1 − Π_{i: E∈S_i} (1 − x_i)     # probability at least one toxic reference exists;
                                     # or simply max toxicity across mentions

T_E = (#threat words within N words of any mention of E)
      / (total words near E across mentions)

F_E = tanh( (1/N_E) · Σ_i frame_score(E, context_i) )

M_E = f(positive moral words near E − negative moral words near E)      normalized [−1,1]
```

`frame_score`: +1 when E is the subject of a power verb (lead, organize, announce, defend);
−0.5 for admit / deny / blame / accuse; −1 when E is the *object* of kill / attack / arrest /
defeat (they are the target of a bad action).

Lexicons: threat words = threat, danger, terror, security, fear, crime, criminal. Moral good =
hero, honest, innocent, brave. Moral bad = villain, corrupt, evil, criminal.

Conflict flag: patterns "E vs / versus / against", or an opposing-sign sentiment against another
main entity.

Quote counting: regex `"…"\s*[,-]\s*(said|says|stated|according to)\s*([A-Z]\w+)`, or the
dependency parse with E as the subject of a speech verb.

**Coreference matters**: pronoun mentions ("he/she") should be folded in via a coref component
(NeuralCoref, a transformer coref model), and aliases normalized ("President Biden" and "Biden"
are one entity). Otherwise counts and sentiments are wrong.

Tools: spaCy NER + dependency; `nlptown/bert-base-multilingual-uncased-sentiment`;
`unitary/toxic-bert` or `unitary/unbiased-toxic-roberta`; VADER for the fast path; NetworkX for
the co-mention graph.

**Scaling note**: a transformer inference per mention across 1M documents adds up. Reuse the
sentence-level sentiment already computed, use lexicons for threat and moral terms, propagate
token-level toxicity, and compute the full profile only for *significant* entities (frequently
mentioned or central). An article may name 50 entities but only a handful matter.

**Consistency check**: toxicity = 1 combined with positive sentiment is a bug signal.
**False positive to guard**: *"X said 'we will not tolerate threats'"* must not mark X as a
threat — it is X *talking about* threats.
**Known risk**: two different people sharing a name get conflated; coreference helps but is
error-prone, producing contradictory scores from mixed contexts.

Calibration expectations: clearly favourable description ("accomplished, respected leader") →
sentiment ≈ +0.8; very negative ("corrupt, notorious criminal") → ≈ −0.8; neutral reporting → ~0.
Toxicity is typically 0 in mainstream text and jumps toward 1 on insults, with partial credit
(~0.5) for milder terms like "incompetent". Threat: consistent association ("people fear X",
"X is a danger") → >0.7; a single "X could pose a threat" → ~0.3; weight direct statements
("X is a threat") more than reported ones ("X said there is a threat"). Framing: all power verbs
→ ≈ +1; "X was arrested, X was accused" → ≈ −1; a mix centres near 0.

Sanity scenarios: an article about a criminal → negative sentiment, high threat, negative moral
valence · a profile praising someone → positive sentiment and moral valence, positive framing ·
an opinion piece attacking a politician → negative sentiment, possible toxic epithets, threat
portrayal ("X endangers the country"), conflict = yes.

Downstream uses: the co-mention graph (nodes = entities, edges = co-occurrence weighted by
frequency, node colour = average sentiment) · voice balance ("if an entity is central but has
zero quotes while another has many, that imbalance is a bias sign") · direct input to stance
detection.

---

## 17. Stance detection

Determines the document's position toward a target (claim, topic or entity):
support / oppose / neutral, plus **stance strength** [0,1], **explicitness**, **internal
consistency**, and a **conflict check**.

```
st(t) ∈ {−1, 0, +1}          oppose / neutral / support
stance_strength = |polarity|
```

Approaches:
- **For entities** — entity sentiment *is* the stance: > 0.2 → support, < −0.2 → oppose,
  otherwise neutral; strength = |sentiment|.
- **For issues** — repurpose NLI as zero-shot stance: premise = article text, hypothesis =
  "Policy P should be implemented." Entailment → support; contradiction → oppose; neutral →
  neutral.
- **Stance lexicon** — "should"/"must" + an action indicates support; "X is a bad idea"
  indicates opposition; "the case for X" / "the case against X".
- **Explicitness** = 1 when overt stance verbs or first-person statements appear ("I support X",
  "we oppose Y", "I believe", "we should"). First-person voice usually means an opinion article
  with an explicit stance.
- **Internal consistency** = 0 when the same entity receives both strongly positive and strongly
  negative contexts in the author's own voice.
- **Conflict** = True when opposing viewpoints appear — e.g. a second main entity with
  opposite-sign sentiment, or "however"-type contrast markers.

**Crucial interpretive note:** a balanced news piece quoting both sides has `conflict = True` but
is still internally consistent — the author is not contradicting themselves; the article's own
stance is neutral. Internal consistency should mainly apply when the article *attempts* a stance.
If stance is neutral, consistency is either not applicable or trivially true.

Output:
```python
{"target": ..., "stance": "support|oppose|neutral", "stance_strength": 0.0,
 "explicitness": bool, "internal_consistency": 1.0, "conflict": bool}
```
Populates `stance_distribution`, e.g. `{"support": 30%, "oppose": 20%, "neutral": 50%}` across a
corpus ("Out of 100 articles on topic X, 30% support, 50% neutral, 20% oppose").

**Consistency requirement**: if entity sentiment says A is −0.8, the stance toward A must be
"oppose, strength ≈ 0.8" — otherwise the user sees contradictory information.

Validation: an editorial endorsing a candidate vs one opposing must be classified correctly ·
a neutral news story must output "neutral" (or nothing significant) · flip tests ("X is great"
vs "X is terrible") · implicit stance ("While X has some benefits, it ultimately causes more
harm.") implicitly opposes X — check the signals catch it. Without a dedicated stance model, the
heuristic approach will miss subtle cases.

Lightweight enough for real time, since it mostly reuses previously computed results.

---

## 18. Structural and syntactic analysis

Metrics: **POS distribution** (fraction per tag, forming a vector summing to 1 over major
categories) · **passive voice ratio** · **nominalization frequency** (nouns ending in -tion,
-ment, -ness, -ity, -ance, -ence, -ship ÷ sentences — a high rate indicates a formal or
obfuscated style) · **sentence complexity** (max dependency-tree depth per sentence, count of
subordinate conjunctions, or average sentence length as a proxy) · **discourse connective
density** (however, although, moreover, therefore, meanwhile, in contrast, on the other hand,
per sentence or per 100 words) · **topic coherence** (adjacent-sentence embedding similarity, or
Jaccard overlap of content words >3 characters as the cheap proxy) · **narrative shift count**
("on the other hand", "however", "but", "meanwhile") · **coreference density** (pronouns ÷
entities, or average coreference cluster size; also the ratio of unique entities to total
mentions — many mentions of few entities means cohesive focus, many unique entities means
scattered content).

**Readability formulas**
```
Flesch-Kincaid Grade = 0.39·(words/sentences) + 11.8·(syllables/words) − 15.59
Flesch Reading Ease  = 206.835 − 1.015·(words/sentences) − 84.6·(syllables/words)
SMOG                 = 1.0430·√(poly-syllable words · 30/sentences) + 3.1291   (30-sentence sample)
Gunning Fog          = 0.4·((words/sentences) + 100·(complex_words/words))
                        complex_words = words with >2 syllables
```
Library: `textstat` (`flesch_reading_ease`, `flesch_kincaid_grade`, `smog_index` — needs ≥3
sentences, `gunning_fog`, `syllable_count`).

```python
pos_counts = Counter(t.pos_ for t in tokens)
pos_dist = {pos: pos_counts[pos]/num_tokens for pos in
            ["NOUN","VERB","ADJ","ADV","PROPN","PRON","NUM"]}

passive_sents = sum(1 for sent in doc.sents if any(t.dep_ == "nsubjpass" for t in sent))
passive_ratio = passive_sents / num_sents

nominalizations = sum(1 for t in tokens if t.pos_ == "NOUN" and
                      re.search(r'(tion|ment|ness|ity|ance|ence|ship)\b', t.text.lower()))
nominalization_freq = nominalizations / num_sents

# dependency depth per sentence → avg_depth
# readability via textstat
# connective_density = connective_count / num_sents
# adjacent-sentence similarity (Jaccard of content words, or embeddings)
# coref_density = pronouns / max(1, len(doc.ents))
```

Optional composite:
`complexity_score = σ(α·FK_grade + β·avg_depth + γ·nominalization_freq)`.

These are mostly **diagnostic/style metrics, weighted low in bias scoring** — complexity is not
inherently malicious (some topics are just complex). But extreme values matter: very low
readability plus low transparency suggests deliberate **obfuscation**, and propaganda tends to
be either very simplistic slogans or overly convoluted conspiracy prose.

Validation: an academic abstract → low reading ease, high grade level, high nominalization · a
simple news piece → ease ~70 · a shuffled-sentence text → very low adjacent similarity · known
passive/active examples correctly classified · "implementation" counted as a nominalization but
"apple" not · cross-check against an external tool (e.g. MS Word readability). A normal news
article typically scores Flesch ease ~50–60 or grade ~10–12 — if a scholarly article comes back
at 5th-grade level, something is wrong.

---

## 19. Framing theory and moral foundations

### 19.1 Framing dimensions (each scored [0,1])

```python
frames = {"Economic": 0, "Moral": 0, "Conflict": 0, "HumanInterest": 0, "Responsibility": 0}
frame_d = min(1, count_words(lexicon_d) / max(1, num_sents/2))
```
(The five keys above are the literal dict/JSON keys — `HumanInterest` is one word.)

| Frame | Lexicon |
|---|---|
| Economic | cost, price, economic, investment, financial, tax, benefit |
| Moral | moral, immoral, ethic, sin, honor, virtue, integrity |
| Conflict | vs, fight, battle, war, conflict, attacked, clashed, tension |
| HumanInterest | family, children, story, personal, heart, emotion, tragedy |
| Responsibility | responsible, blame, fault, credit, accountable, cause |

Descriptions: *Economic* — cost/benefit and financial aspects. *Moral* — moral/ethical
judgements, religious or ideological principles. *Conflict* — winners/losers, us vs them, war
metaphors, two-sided language, quotes from opposing sides. *Human interest* — individuals and
emotion carrying the story; personal anecdote in a policy issue; many proper names and few
statistics. *Responsibility* — who is to blame or to credit ("X is responsible for Y", "due to
X's actions", "thanks to X").

### 19.2 Moral Foundations Theory (Haidt) — each axis [−1, +1]

```
axis_score = Σ(valence × count) / Σ count
```

| Axis | Virtue words (+1) | Vice words (−1) |
|---|---|---|
| Care / Harm | care, compassion, kind, help | harm, hurt, suffer |
| Fairness / Cheating | fair, justice, equal | inequality, cheat, fraud, unfair |
| Loyalty / Betrayal | loyal, patriot, ally | betray, traitor, treason |
| Authority / Subversion | duty, obedien*, respect, honor, authority, law, order | (subversion, rebellion) |
| Sanctity / Degradation (Purity) | pure, clean, sacred, holy, virtuous | degenerat*, disgust |

Source: the Moral Foundations Dictionary (Graham et al.).

**Known limitation, explicitly flagged:** a text saying "this policy is unfair" uses a negative
fairness word, which the naive lexicon reads as morally negative on fairness — whereas the author
is in fact *upholding* fairness by calling out its violation. Capturing that nuance requires
negation and context handling. Accepted as noise for now, but it must be documented.

### 19.3 Use and interpretation

Framing correlates with bias — partisan outlets favour the conflict and responsibility frames.
Moral foundations reveal ideological bent: some political rhetoric appeals more to loyalty and
purity, other rhetoric to fairness and care (per Haidt's theory), so this identifies subtle
biases in *value appeals*. A radar chart is the natural visualisation. **Treat these as one
signal among many, not a verdict** — the output means "the article uses a lot of conflict
language", not "the author endorses that perspective".

Validation: an article about caring for the poor should show Care/Harm positive; a law-and-order
speech should show Authority positive; an economic news piece should show a high Economic frame.
If a dimension is always high erroneously, refine the lexicon (note that "attack" legitimately
signals the conflict frame whether literal or argumentative).

Implementation: pure lexicon scanning — very fast, negligible overhead, no new dependencies.

---

## 20. Taxonomy classification and feature gating

### 20.1 The taxonomy

A **controlled vocabulary defined upfront in config**, not emerging ad hoc. It can cover:

- Propaganda / rhetoric types — "Fear-mongering", "Appeal to Authority", "Disinformation",
  "Personal Attack", "Propaganda: Flag-Waving", "Propaganda: Appeal to Fear"
- Logical fallacy types — the full fallacy list
- Bias categories — "Political Bias: Left", "Political Bias: Right", "Ideological Bias:
  Left-Leaning", "Clickbait", "Satire", "Loaded Language"
- Optional topical categories — "Topic: Immigration", "Topic: Climate"

It may be hierarchical (a broad "Logical Fallacy" parent with a "Strawman" child) and is
versioned via `taxonomy_version`. The Data Engineer owns maintaining and updating it as the
project evolves.

### 20.2 How classification works

Feed the features and flags from the previous layer into a **classification engine** that
assigns taxonomy labels. In many cases this is direct — if a specific fallacy flag is true, the
document (or segment) gets the corresponding label. For complex or overlapping categories, use
rule-based logic or an ML multi-label classifier.

**Rule-based mapping is preferred** (deterministic, traceable, tunable). The mapping logic lives
in configuration — "Category X is triggered if feature A > 0.8 and feature B is true" — so
non-engineers and analysts can tweak category assignment without touching code.

```python
labels = []
score  = 0
if flags["ad_hominem"]:        labels.append("Ad Hominem Attack");  score += 10
if flags["strawman"]:          labels.append("Strawman Argument");  score += 8
if flags["bandwagon_effect"]:  labels.append("Bandwagon Appeal");   score += 5
if flags["emotional_appeal"]:  labels.append("Emotional Appeal");   score += 5
# … and so on for all fallacies and bias types …
if features["counterargument_present"]:
    score -= 5                                 # balance reduces the score
bias_score = min(100, max(0, score))
if   bias_score > 80: labels.append("Highly Manipulative")
elif bias_score > 50: labels.append("Some Bias")
result = {"labels": labels, "scores": {"bias_score": bias_score}}
```

Composite examples:
- "Misleading Use of Data" ← `fallacy_false_cause` OR `statistical_misuse_flag` OR `outlier_flag`
- "Emotionally Manipulative" ← `fallacy_appeal_to_emotion` OR `sentiment_extremes`
- "Loaded Language" ← high emotional tone + specific keywords
- "Unsubstantiated Claims" ← a claim made with no evidence
- "One-sided Sourcing" ← quotes are one-sided
- "Lacks Counterargument" ← no counter-argument present

Severity/combination labels: multiple fallacies → "Highly Manipulative"; one minor issue →
"Slight Spin".

Classification happens at the **sentence level first**, then aggregates to a document-level label
array (Sentence 3 = Ad Hominem, Sentence 5 = Strawman → the document carries both). Each label
can carry a confidence — a probability from ML, or an implicit 1.0 for a satisfied rule.

Stored form: `labels = {propaganda: ["Appeal to Fear", "Loaded Language"], fallacy: ["Slippery Slope"]}`.

The taxonomy also translates myriad low-level signals into human-readable categories — multiple
fear-related features (fear words, high negative sentiment, catastrophic predictions)
collectively resolve to the single label "Appeal to Fear". It drives what explanation text the
UI shows per label (educating users) and gives developers a **checklist of techniques the
detectors must cover**, plus a structure for logging how often each type is found.

### 20.3 Taxonomy-aware feature gating

**The FeatureRegistry must be consulted BEFORE FeatureExtractor runs.** Running all 13 feature
layers on every document is wasteful; the taxonomy classification determines which layers are
relevant:

| Document class | Layers triggered |
|---|---|
| **Opinion** | Rhetorical (L8), Fallacy (L9), Sentiment (L6), Framing (L7) |
| **News Report** | Factuality (L10), Entity (L5), Temporal (L11) |
| **Scientific** | Logical Fallacy (L9), Factuality (L10), citation quality |

This means **the taxonomy controls which scoring mathematics runs on each document.**
Implement `nlp_pipeline/feature_registry.py` before calling `FeatureExtractor`.

### 20.3a Classification tiers — how rules and ML combine

The three-tier scheme that governs every classification decision.

**Tier 1 — Rule-based (primary, always runs).** Lexicons + regex + spaCy dependency patterns in
`rules_engine.py`, reading `taxonomy_v1.yaml` for category definitions and rule sets. If
confidence ≥ threshold → assign the category and **skip ML for that sentence**. Rules take
precedence whenever confidence is high.
```python
if contains_any(sentence, bias_lexicon) and contains_any(sentence, political_actor_lexicon):
    assign("political_bias", conf=0.95)     # a satisfied compound rule → very high confidence
```

**Tier 2 — ML classifier (secondary, for ambiguous cases only).** Classical ML (LogReg / SVM) or
a frozen compact transformer via ONNX. **Only invoked when rule-engine confidence < threshold.**
The model is versioned, seed-fixed at training, and never updated online.

**Tier 3 — HybridRouter merge.** Combines tier-1 and tier-2 results using the blend formula
(§21.1 formula 2), with a strict precedence order defined in config. Same input → same output,
always.

Routing logic — **implement exactly this** in `hybrid_router.py`:
```python
if rule_confidence >= threshold:          # threshold from pipeline_v1.yaml
    return rule_result
else:
    blended = α * conf_rules + (1 - α) * conf_ml
    return assign_labels(blended, thresholds)
```

### 20.4 Taxonomy suggestion workflow

1. Collect low-confidence / unmatched sentences.
2. Cluster using k-means on embeddings with a fixed seed (deterministic).
3. Compute top keywords and representative examples per cluster.
4. Output a **human-reviewable YAML diff** proposing new subcategories.
5. Approved diffs become `taxonomy_v2.yaml` with a full audit trail.

```yaml
proposed_new_category:
  parent: political_bias
  keywords: [...]
  examples: [...]
```

The system must **never silently mutate the production taxonomy.**

### 20.5 OntologyGraph

`nlp_pipeline/ontology_graph.py` wraps the taxonomy as a networkx graph. Methods:
`get_ancestors`, `get_descendants`, `project_labels_to_levels`, `validate_label_set`. Used by
`RuleEngine` (threshold calibration), `HybridRouter` (merge logic) and `FeatureRegistry`
(gating). Supports multi-parent DAG reasoning as an extension point.

---

## 21. Scoring engine — all mathematics

Owned by the NLP/Data Engineer. Must be **deterministic and reproducible**; the exact weights are
proprietary and set by domain experts; all of it is documented in `scoring_v1.yaml` so changes
are versioned and testable.

### 21.1 The five core formulas (implement these exactly — do not invent new ones)

**1 — Article-level scoring**
```
score_article = Σ_{c ∈ taxonomy} ( w_c × s_c )
```
- `w_c` = weight of category c, from `scoring_v1.yaml`
- `s_c` = normalized per-category score (sentence fraction + rule bonuses/penalties)

**2 — Hybrid sentence confidence**
```
conf(sentence, category) = α × conf_rules(s, c) + (1 − α) × conf_ml(s, c)
```
- `α ∈ [0,1]`, configured in `pipeline_v1.yaml`; controls the rule-vs-ML balance
- Final category-assignment thresholds also come from config, never hard-coded

**3 — Logical fallacy severity**
```
s_i = c_i × w_f
```
- `c_i` = confidence for fallacy instance i (0–1), from rule or ML
- `w_f` = fallacy-type weight from `scoring_v1.yaml` (reflects that type's severity)

Logical flow disruption (how much fallacies disrupt argument coherence):
```
ℓ = max( s_i × d_{f_i} )    over all detected fallacy instances i
```
- `d_{f_i}` = disruption factor for fallacy type f (a domain-specific constant from config)

**4 — Propaganda score / PropScore**
```
PropScore = 1 − Π_p ( 1 − v_p )     for each propaganda technique p detected
```
- `v_p` = intensity of technique p (0–1), from the rule match and pattern strength
- The **product** form ensures that multiple weak techniques compound into a high score

**5 — Factuality score**
```
F = w₁·r_vc + w₂·σ̄ + w₃·Cn + w₄·Lf + w₅·(1 − M)
```
- `r_vc` = claim verification rate (verified claims / total claims)
- `σ̄` = mean source credibility across all cited sources
- `Cn` = internal consistency (no contradictions)
- `Lf` = logical flow (no disruptions; ℓ is low)
- `M` = missing-context penalty (fraction of key facts omitted)
- `w₁..w₅` from `scoring_v1.yaml`, **must sum to 1**

**6 — Multi-label graph**: sentences and taxonomy nodes are graph nodes; edges are
`sentence --(belongs_to, weight=conf)--> taxonomy_node`. A sentence can link to multiple
taxonomy nodes — **multi-label is first-class.**

**7 — Embedding similarity**
```
d(i, j) = 1 − cos(e_i, e_j)
```
Use **exact** cosine search (not approximate) to keep results reproducible. Used for clustering
misfit / low-confidence sentences to propose new taxonomy nodes.

### 21.2 Composite indices

```
BiasScore = (1/Z) · ( w₁·avg_entity_sentiment_polarity + w₂·bias_marker_density
                    + w₃·propaganda_intensity + w₄·framing_asymmetry ),      Z = Σ w
   bands: 0–0.3 Low Bias · 0.3–0.6 Moderate · 0.6+ High Bias

ManipulationIndex = 1 − Π_{feature ∈ {fallacy, propaganda, misleading}} (1 − feature_score)

FactualityRating  = factuality_score (§15), optionally adjusted by source credibility

QualityScore = w_f·F + w_t·T + w_d·D + w_m·(1 − M) + w_b·(1 − BiasScore)
   suggested: w_f = 0.4, w_t = 0.2, w_d = 0.1, w_m = 0.1, w_b = 0.2
   (can be presented as a 5-star rating or a letter grade)
```

Alternative earlier forms kept for reference:
```
ManipulationIndex = w₁·num_fallacies + w₂·sentiment_variance + w₃·(1 − source_credibility) + …
manipulation_score = Σ_i w_i · feature_i     (positive weight for negative traits,
                                              negative weight for positive traits like balance)
BiasScore  = tanh(a·F + b·E + c·B)   F = # distinct fallacy types (or weighted count),
                                     E = emotional appeal flag (1/0),
                                     B = bias-indicator count
CredibilityScore = 1 − BiasScore
bias_score = Σ_i w_i · feature_i / Σ_i w_i         (normalized weighted average form)
```

**The four-step combining procedure** (the canonical way to turn detections into one score):

1. **Feature normalization** — convert each detected characteristic into a number:
   `bandwagon_effect` as binary 0/1 or a frequency count, `loaded_language` as `loaded_ratio`,
   `contradiction` as the number of contradictions found — then normalize all to a common
   0–1 scale.
2. **Weighting** — assign weights by impact. Factual issues (`data_accuracy`, `contradiction`)
   weigh more than style issues (`hedging`); `cherry_picking`, `false_causality` and
   `loaded_language` weigh high. Weights are set by experts, or learned by training on a
   labelled dataset of articles with known bias scores.
3. **Aggregation** — `bias_score = Σ_i w_i · feature_i / Σ_i w_i` → a value in [0,1] (or 0–100).
4. **Calibration** — test against known neutral vs known biased content, then map to bands.

**Per-signal additive scheme (0–1 scale)** — the concrete increment table:

| Signal | Adds |
|---|---|
| `loaded_language`, `name_calling`, `ad_hominem` | **+0.1** each |
| `false_causality`, `contradiction` | **+0.2** each |
| `omission`, `cherry_picking` | **+0.15** |
| `hedging_signals` | **+0.05** (if at all — hedging can indicate caution rather than manipulation) |

Clip the total at **1.0**. Band interpretation for this scale: **0–0.3 low bias · 0.3–0.7
moderate · 0.7–1 high manipulation.** (The `BiasScore` composite in §21.2 uses slightly
different bands — 0–0.3 / 0.3–0.6 / 0.6+ — because it aggregates different inputs; keep the two
straight.)

For transparency the system outputs the breakdown, not just the total:
*"Score contributed by loaded language: 0.1, by contradictions: 0.2, … total = 0.7."*

**Additive rubric alternative** (transparent and easy to tune, 0–100 scale): start at 0; +5 per fallacy (more
for severe ones such as Ad Hominem or outright falsehood); up to +10 for high emotional language
proportional to intensity; +10 if one-sided (cherry-picking, no counter viewpoints); subtract
points for balance or plentiful evidence; cap at 100.

Worked example: Bandwagon (+5) + Loaded Language (+5) + one-sided sentiment toward two entities
(+10) = 20 → *moderately manipulative*. Many fallacies plus very high emotional tone → 70–80 →
*highly manipulative*.

Score dimensions produced: Overall Bias Score · sub-scores per category (Logical Fallacy Score,
Emotional Tone Score, Source Credibility Score) · Credibility Score · Sentiment Bias Score ·
Factuality Score · Emotional Intensity · Logical Soundness · Manipulation Score.
Conceptually the "scoring matrix" is a table whose rows are taxonomy categories and whose columns
are contributions to each output score; per document it is stored as
`scores: {bias: X, factuality: Y, …}` with a `score_version`.

### 21.3 Feature weighting strategy

- **Factual accuracy features weigh strongest.** A single outright false claim or glaring
  contradiction is very damaging — a factual error can single-handedly cap the FactualityRating
  regardless of other positives.
- **Propaganda and fallacies weigh highest in the ManipulationIndex.** One blatant Ad Hominem or
  Fear Appeal pushes it high even when everything else is mild.
- **Subtle linguistic bias** (hedging, mild loaded language) carries medium weight — individually
  small, but they accumulate.
- **Structural/style features** (complexity, passive voice) carry the lowest weight; they are
  diagnostic and secondary. Extremely convoluted language may slightly reduce the transparency
  score but must not overshadow factuality.
- **Source metadata acts as a prior** — a known bias/reliability rating sets an expectation;
  flag when the computed scores deviate from it rather than silently overriding them.
- **Learned weighting later** — regress on a labelled set of articles once expert ratings exist.
- **Avoid double counting** correlated features (toxicity vs name-calling frequency; fallacy vs
  misleading score). Use a correlation heatmap or PCA to decide what to merge or drop.
- **Document the weighting rationale and allow user override** — expose sliders for "importance
  of factual accuracy vs bias vs style" and recompute composites on the fly. This is feasible
  precisely because the sub-scores are modular. Researchers may legitimately weight bias above
  factuality for a particular study.
- **Severity escalation rule**: if certain severe issues occur (outright contradictions, provably
  false information), the score is automatically high regardless of other factors.
- **Interaction handling**: bandwagon and unsupported_quantifiers are related (both about vague
  majority appeals) — they reinforce rather than over-count, which a well-chosen weight handles.

**Keep composites interpretable.** Every number must drill down to raw features — the user can
see "Score contributed by loaded language: 0.1, by contradictions: 0.2, … total = 0.7".

### 21.4 Calibration and testing

Calibrate by testing on examples of neutral vs highly biased content; map the score into bands
(0–0.3 low, 0.3–0.7 moderate, 0.7–1 high). QA test cases: a clearly neutral article must produce
a low bias score; a known biased op-ed a high one; running the same article twice must give
exactly the same score; when features or weights change, regression-test previous examples so
score shifts are intentional.

---

## 22. Evidence-grounded scoring and explanation

This is the **explainability contract** — how a score is communicated. It is *Explainable NLP
(X-NLP)*, not black-box sentiment.

### 22.1 The core principle: "No Claim Without Evidence"

Every high-level claim must be backed by:
```
Claim → Rule → Evidence → Location
```
❌ Not enough: *"The article uses emotionally harmful language."*
✅ Correct: *"The article uses emotionally harmful language, such as 'these people are parasites'
(Sentence 14), which falls under Dehumanization / Abusive Framing."*

### 22.2 The golden rule of ordering

**The model never "thinks" first. It extracts evidence first, then forms a judgement.**

```
❌ Bad:      score → explanation → cherry-picked quote
✅ Correct:  evidence → aggregation → score → explanation
```

Pipeline:
```
Text → Sentence Segmentation → Feature Detection (lexical + syntactic + semantic)
     → Rule / Pattern Match → Evidence Extraction (text spans)
     → Scoring → Evidence-grounded Explanation (NLG)
```
**Evidence is extracted before explanation, never after.**

### 22.3 Span-level evidence, not document-level scores

Instead of `"hurtfulness": 0.78`, produce:
```json
"hurtfulness_evidence": [
  { "category": "emotional_abuse", "indicator": "insult",
    "text_span": "these people are parasites",
    "sentence_id": 14, "start_char": 3124, "end_char": 3150,
    "confidence": 0.91 }
]
```
This makes the system auditable, verifiable and testable.

Extraction methods (combined):
1. **Lexicon + pattern rules (deterministic)** —
   `INSULT_TERMS = ["parasite", "vermin", "scum"]`; if any term appears, `mark_evidence(...)`.
2. **Syntactic patterns** — `[group noun] + "are" + [dehumanizing noun]`, e.g. "Immigrants are
   criminals".
3. **Semantic similarity (controlled)** — sentence embeddings compared against known harmful
   prototypes, thresholded, with no randomness.

### 22.4 The output contract: Score → Interpretation → Evidence

Human-readable:
```
Hurtfulness Score: 0.82 (High)
The content is considered harmful because it uses dehumanizing and insulting language.
This is supported by phrases such as:
  "these people are parasites"     (Sentence 14)
  "they deserve to be wiped out"   (Sentence 27)
```
Machine-readable:
```json
{
  "metric": "hurtfulness",
  "score": 0.82,
  "level": "high",
  "model_interpretation": "The content contains harmful language characterized by dehumanization.",
  "evidence": [
    { "text": "these people are parasites", "sentence_id": 14,
      "category": "dehumanization",   "rule_id": "HARM_DEHUM_01", "confidence": 0.91 },
    { "text": "they deserve to be wiped out", "sentence_id": 27,
      "category": "violent_language", "rule_id": "HARM_VIOL_02", "confidence": 0.88 }
  ]
}
```
Full production shape:
```json
{ "scores": { "hurtfulness": 0.82 },
  "classification": "harmful",
  "explanation": {
    "summary": "The text contains emotionally harmful language.",
    "categories": ["emotional_abuse", "dehumanization"],
    "evidence": [ { "text": "these people are parasites", "sentence_id": 14,
                    "category": "dehumanization", "rule_id": "EA_DEHUM_01" } ] } }
```

### 22.5 Internal reasoning (never exposed raw)

```json
{ "detected_indicators": { "dehumanization": 2, "violent_language": 1 },
  "severity_weights":   { "dehumanization": 0.4, "violent_language": 0.6 } }
```
```
hurtfulness_score = Σ_i ( count_i × weight_i × confidence_i )    then normalize → 0–1
```

### 22.6 Two modes, one engine

- **Mode A — score generated by the system**: takes the generated score, knows which text
  segments contributed, produces a natural-language judgement, and combines it with the exact
  text that justified the score.
- **Mode B — score given externally**: takes a score as input, interprets what it means in
  language, finds or is given the text that caused it, and combines score → explanation →
  evidence.

**The output is identical in both cases.** You do not build two models — you build a **scoring
engine**, an **evidence tracker**, and an **explanation generator**.

Unified input contract:
```json
{ "metric": "hurtfulness", "score": 0.82,
  "score_source": "internal | external",
  "text": "full original content here",
  "evidence_spans": [ { "text": "these people are parasites", "sentence_id": 14,
                        "start": 3124, "end": 3150, "category": "dehumanization" } ] }
```
⚠ If `score_source = external`, `evidence_spans` must be provided or computed separately.

```python
def interpret_score(score):
    if score < 0.3:  return "low"
    elif score < 0.6: return "moderate"
    else:            return "high"

def explain_score(score, text, evidence_spans):
    level  = interpret_score(score)
    phrase = score_to_phrase(level)          # from the YAML band table
    evidence_texts = [e["text"] for e in evidence_spans]
    ...
```
Score→language mapping is deterministic, from `scoring_v1.yaml → score_bands`
(see §6.3) — **the model never improvises language.**

### 22.7 Hard constraints (do not break)

- ⚠ Never let the model **invent** evidence.
- ⚠ Evidence must be **exact substrings** of the input — no paraphrased quotes.
- ⚠ Always store the sentence index **and** character offsets.
- ⚠ The explanation must never introduce new facts.
- ⚠ The explanation must derive **only from extracted evidence**, never directly from the raw
  text. *That is the line between Explainable NLP and Opinionated NLP.*
- ⚠ The score explanation must depend only on score bands + evidence.

### 22.8 Why this design is correct

Defensible (legal/academic) · reproducible · deterministic · explainable · works **without
LLMs** · can optionally add LLM phrasing later · decouples scoring from explanation · works with
external models or human-supplied scores · QA-testable · NDA-safe · scoring logic is replaceable.
It matches the practice in media bias research, harm detection, propaganda analysis, and
compliance/audit systems.

**Optional LLM enhancement, done safely**: feed the model *only* the score band, metric name and
evidence text; lock temperature to 0; **never give it the raw article text.**

### 22.9 What QA can now verify

✔ the evidence text exists in the input · ✔ the sentence indices are correct · ✔ the score
changes only if the evidence changes · ✔ the same input gives the same output.

Role split for this feature: Data/NLP Engineer owns evidence extraction + scoring logic; Backend
owns the API schema and JSON contract; Lead Engineer owns determinism, versioning and infra;
QA owns reproducibility and regression tests.

---

## 23. Embeddings and vector search

### 23.1 Model choice

**SentenceTransformers MiniLM (`all-MiniLM-L6-v2`), ONNX version, 384 dimensions.** Reasons:
very fast, runs on CPU, high quality, widely used in media classification, trustworthy, works
without a GPU, suitable for deterministic pipelines. The broader recommendation is **HuggingFace
Tokenizers (Rust) + SentenceTransformers with ONNX**, which speeds up vectorization 5×–20× and
significantly reduces model latency. With a GPU, TensorRT would add another ~3×; without one,
ONNX on CPU is the best option.

`EmbeddingGenerator` structure: load the ONNX model → preprocess text → tokenize → generate
embeddings → return numpy arrays. **Batch 16 or 32 sentences** — never run the model
per-sentence, which wastes overhead.

```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
def embed_sentences(sentences):
    return model.encode(sentences, convert_to_numpy=True, batch_size=32)
```

Embedding is **step 4** of the pipeline: preprocess → segment → features → **embeddings** →
(rules + ML) → hybrid → ontology → scoring → output.

### 23.2 When to add a vector store

The correct real-world sequence:
1. Build embeddings
2. Store embeddings **in memory**
3. Add vector search (**FAISS**)
4. *(Optional)* replace FAISS with a vector DB
5. *(Optional)* add similarity-based rules / hybrid routing

**You never start with the vector DB.** Vector DBs are only needed for embedding-based
similarity search, category suggestions, fuzzy mapping of new taxonomy terms, semi-supervised
classification, and clustering/IR tasks. Version 1 of the pipeline runs fully deterministically
without one.

Add FAISS only when reaching: `taxonomy_suggestions.py` (find similar sentences → recommend new
categories) · `hybrid_router.py` similarity fallback · rule expansion ("find content similar to
known patterns") · content deduplication of crawled articles.

Options and the verdict:
- **Local FAISS** — free, fast, where most enterprise NLP pipelines start. ✅ chosen.
- **Local Annoy / HNSW** — lighter alternatives if FAISS feels like overkill.
- **Cloud vector DBs (Milvus, Pinecone, Weaviate, Qdrant)** — ❌ not needed: this is a
  deterministic pipeline, not a semantic search engine; no cloud indexing; no horizontal scaling;
  they cost money; the company doesn't require them.

### 23.3 VectorIndex

```python
import faiss, numpy as np

class VectorIndex:
    def __init__(self, index_path: str, dim: int):
        self.index_path = index_path
        self.dim = dim
        self.index = None
    def load(self):
        self.index = faiss.read_index(self.index_path)
    def add(self, vectors: np.ndarray):
        self.index.add(vectors)
    def search(self, query_vec: np.ndarray, k: int = 5):
        distances, indices = self.index.search(query_vec, k)
        return distances, indices
    def save(self, new_path=None):
        faiss.write_index(self.index, new_path or self.index_path)
```
Simple builder form:
```python
def build_faiss_index(embeddings):
    index = faiss.IndexFlatL2(embeddings.shape[1])       # exact search — reproducible
    index.add(embeddings)
    return index
```
This is a **stateful** component (loads data, stores embeddings, provides search, may switch
CPU/GPU, needs reloading and versioning) — hence a class. It also encapsulates state cleanly for
`PipelineRunner`, is easy to mock in tests, and works in both batch and API modes.

### 23.4 The read-only rule

**The vector DB is read-only semantic memory. It does NOT participate in classification
decisions and is NOT a decision-maker.** It is deliberately kept out of the deterministic
scoring path because embedding similarity is a statistical measure that may introduce
nondeterministic behaviour depending on the model, and using it in core scoring would undermine
reproducibility. Insights from it (narrative clusters) are supplementary or for offline
analysis.

Purposes: "find articles similar to this one" · cluster articles by narrative · detect a talking
point circulating across multiple sources (agenda setting) — e.g. take an article that scored
high on propaganda and query for near neighbours to reveal a network of content carrying the
same message. Exposed via an endpoint like `/similar_articles?doc_id=123` returning the top-N
nearest neighbours (optionally excluding the same publisher).

Embeddings are stored **outside** Parquet with only their IDs in the main data, both to avoid
bloating Parquet and because specialised vector indices are far faster for similarity search.

### 23.5 FAISS vs Elasticsearch vs ESClient — the confusion resolved

| Thing | What it actually is |
|---|---|
| **Elasticsearch (ES)** | A separate **search server**. Stores documents, indexes them, runs search queries. Not part of your code. "Like Google, but for your data." |
| **ESClient** | *Your* small Python wrapper that talks to that server — **a connector only**. It does not store data, create clusters, run the server, do vector math locally, or replace FAISS. Analogy: a remote control (ESClient) operating a TV (Elasticsearch). |
| **Vector search** | Searching using embeddings instead of keywords: "India GDP growth" → [0.12, 0.88, 0.33, …] → find similar-meaning documents. |
| **FAISS** | A **local** vector-search library running inside your Python process. Fast, no server, you control everything. ("personal calculator") |
| **ES vector search** | Vector search performed **inside the ES server**; your code sends embeddings to ES, ES stores and searches them. ("online search engine") |

So: **ESClient ≠ ES · ESClient ≠ vector search · ESClient ≠ FAISS.** ESClient *can request* ES to
run a vector search (like asking Google to search — Google runs the algorithm, not you). ESClient
**cannot** create clusters; it **can** create indexes inside a cluster.

**"Index" in ES = a database table**, not a FAISS index: index = database, document = row,
field = column. Vector search requires a dense_vector field inside the ES index:
```json
"embedding": { "type": "dense_vector", "dims": 384 }
```

One-liner: *FAISS = local vector search · Elasticsearch = remote search engine · ESClient = your
pipeline's remote controller for Elasticsearch · vector search can run on both, but ESClient
never does vector math itself.*

ESClient's two jobs: **(1) data source** — Airflow or a batch script scrolls an index and feeds
documents into preprocessing → taxonomy → scoring → embeddings; **(2) search backend** — FastAPI
runs keyword or semantic search and returns the top-N articles with scores. Implement (1) first.

---

## 24. Output contract and postprocessing

`PostProcessor.to_output_schema(original_doc, normalized_doc, segments, final_classification,
scores)` builds the final JSON. It adds token offsets, span normalization, metadata (pipeline
version, taxonomy version, hashing) and enforces the contract via Pydantic.

The JSON returned to the backend must include:
- **Document-level scores** — one score per taxonomy category
- **Sentence-level classifications** — a list of `{sentence, labels, confidences}`
- **Text spans** — character offsets for each classified sentence (frontend highlighting)
- **Metadata** — taxonomy version, scoring version, pipeline version, run timestamp
- **Multi-label support** — each sentence may carry multiple category labels

### 24.1 Target output shape (implement exactly)

```json
{
  "document_id": "sha256-hash",
  "pipeline_version": "1.0.0",
  "taxonomy_version": "v1",
  "scoring_version": "v1",
  "run_timestamp": "2026-05-23T00:00:00Z",
  "document_scores": {
    "bias": 0.73,
    "logical_fallacy": 0.12
  },
  "sentences": [
    {
      "text": "...",
      "span_start": 0,
      "span_end": 142,
      "labels": ["bias", "rhetorical"],
      "confidences": { "bias": 0.91, "rhetorical": 0.67 }
    }
  ]
}
```

### 24.2 Alternative serving shapes seen in the design

Backend-facing, richer:
```json
{
  "doc_id": "123", "title": "...", "source": "...",
  "bias_score": 75.0, "manipulation_score": 80.0,
  "labels": ["Propaganda: Appeal to Fear", "Fallacy: Slippery Slope"],
  "highlights": [
     { "text_span": "If we allow this, society will collapse", "label": "Slippery Slope" },
     { "text_span": "hordes of criminals", "label": "Loaded Language" }
  ],
  "entities": [ { "name": "John Doe", "avg_sentiment": -0.6, "mentions": 3 } ],
  "published": "2025-12-10",
  "processed_at": "..."
}
```
Simpler highlight form:
```json
{ "doc_id": "12345", "bias_score": 72,
  "labels": ["Ad Hominem Attack", "Cherry Picking", "Emotional Appeal"],
  "segments": [
     { "text": "John Doe is an idiot", "label": "Ad Hominem Attack", "start": 256, "end": 275 },
     { "text": "everyone knows that...", "label": "Bandwagon Appeal", "start": 310, "end": 332 }
  ],
  "metadata": { ... } }
```
Earliest form (still valid for the sentence-level contract):
```json
{ "doc_id": "12345",
  "sentences": [ { "id": 1, "text": "...", "category": "bias_framing",
                   "spans": [[10,24],[30,35]] } ],
  "scores": { "objectivity": 0.82, "sentiment_tension": "low" } }
```

`data_schema/input_schema.json` defines the ingestion contract (required fields — language,
body, metadata; minimally `{"doc_id": "string", "text": "string"}`) and is enforced at both the
API and batch layers. `data_schema/output_schema.json` guarantees a stable structure, version
stamping, consistent score formatting and **deterministic label ordering** — and the output must
validate against it.

Front-end usage: labels shown as tags ("Labels: Ad Hominem, Cherry-Picking, Emotional Appeal")
plus an overall bias meter (e.g. 70/100), with each label mapping to a static explanation that
educates the user about that fallacy or bias type.

---

## 25. Storage, versioning and database schema

### 25.1 Gold → serving database

A relational database (PostgreSQL) is convenient: query by document ID, date, and run analytical
queries. Elasticsearch if full-text search is needed. Querying Parquet directly (e.g. via Spark
SQL) is possible but higher-latency for user-facing requests, so a cache or DB is normally added.

Tables:

- **`Document`** — `doc_id` (PK), `title`, `publisher_id`, `date_published`, `author`, `section`,
  `bias_score`, `factuality_score`, `manipulation_index`, `quality_score`; JSON/JSONB columns for
  `fallacy_vector`, `propaganda_vector`, `linguistic_bias_vector`; `text` or a reference to it.
  A JSONB column can hold the entire structured output for flexibility.
- **`Publisher`** — `publisher_id`, `name`, `bias_rating` (categorical), `bias_score` (−1 left to
  +1 right, or 0–1), `factuality_rating` ("High" / "Mixed"), `reliability_history`. Small table,
  joined to Document.
- **`SentenceFeatures`** — `doc_id`, `sentence_id`, `text`, `sentiment`, `has_fallacy`,
  `fallacy_type`, `has_propaganda`, `technique`. ⚠ Millions of rows for 1M documents —
  alternatively store the sentences as a JSON array on the Document row, since retrieval is
  usually per-document anyway.
- **`EntityFeatures`** — `doc_id`, `entity_name`, `entity_type`, `sentiment`, `toxicity`,
  `framing_score`, `moral_valence`, `quote_count`. Enables queries like
  `SELECT * FROM EntityFeatures WHERE entity_name='Facebook' AND sentiment < -0.5`.
- **`Stance`** — `doc_id`, `target`, `stance`, `strength`, `explicit`.
- **`ArticleAnalysis`** — the flat per-article results table from the earlier serving design:
  `doc_id`, `bias_score`, `labels` (JSON array), plus references to the detail tables. Overlaps
  with `Document` above; `Document` is the fuller, authoritative form.
- **`PropagandaSpan`** / **`ArticleSegments`** — `doc_id`, `technique`/`label`, `sentence_num`,
  `span_text`, `confidence` — one row per highlight or fallacy instance.
- **`SocialMetrics`** *(optional)* — `doc_id`, `share_count`, `like_count`, `trending_score`.
- **Scores History** *(optional)* — retained if analyses are re-run and score changes need
  tracking; unnecessary for a static corpus.
- **No Token table** — millions of tokens × millions of documents is too large.

Example query:
```sql
SELECT D.title, D.publisher_id, D.bias_score, D.factuality_score
FROM Document D
JOIN Publisher P ON D.publisher_id = P.publisher_id
WHERE P.bias_rating = 'Right'
  AND D.bias_score > 0.7
  AND D.factuality_score < 0.5;
```

### 25.2 Performance

Index `publisher_id`, `date_published` and the composite scores (for range queries such as
"all low-factuality articles"). GIN indexes on JSONB in Postgres. Volume: 1M documents × a few
KB of feature JSON ≈ a few GB — fine on a single server; shard or partition beyond ~100M.
Elasticsearch for combined full-text + score-range queries (store `doc_id`, `text` and the
analysis scores as ES fields). FAISS/Milvus for embedding similarity (index built offline, kept
updated as new documents arrive; can store either a neural embedding of the content or a
concatenation of key scores as a "bias vector" for feature-profile similarity). A graph DB
(Neo4j) only if extensive entity-network querying is needed — most network queries can be
answered with SQL joins or a precomputed adjacency matrix.

### 25.3 Versioning

Every record carries `pipeline_version`, `feature_version`, `taxonomy_version`, `score_version`
and `processed_at`. Any change to code, taxonomy or scoring is documented in version control and
in a changelog linked to `pipeline_version`. Because the raw text is preserved in Bronze, any
analysis can be reproduced exactly by re-running the same pipeline version on it.

---

## 26. API and serving

### 26.1 Endpoints

| Endpoint | Purpose |
|---|---|
| `POST /analyze` | Accept raw content (or a URL), run (or queue) the pipeline, return the analysis result |
| `POST /batch/analyze` | Batch classification |
| `GET /analysis/{doc_id}` | Retrieve the stored analysis JSON from the serving DB |
| `GET /highlight/{doc_id}` | Return just the highlighted spans and tags for frontend rendering |
| `GET /similar_articles?doc_id=…` | Vector-DB nearest neighbours |
| `GET /taxonomy` | Taxonomy version info |
| `GET /scores/{id}` | Stored scores |
| `GET /health` | Health check |

### 26.2 Two serving modes

1. **On-demand analysis** — the client submits content, the backend passes it to the pipeline,
   which runs on the fly and returns results. Requires a light in-memory path (spaCy small model,
   models cached in memory) optimised for low latency.
2. **Scheduled batch** — the pipeline runs continuously or on a schedule (e.g. ingesting new
   articles hourly), stores all results in the serving DB, and the API simply queries that DB.

**Given confidentiality and determinism requirements, the batch mode on a controlled schedule is
the chosen approach**, with the API serving stored results. On-demand may use a lighter-weight
distilled pipeline.

### 26.3 Service wiring

```python
runner = PipelineRunner(global_config)     # constructed once at startup
output = runner.run(user_text)             # called per request
```
`api/service.py` calls `runner.run(ingest(request))`. `api/models.py` holds the Pydantic
request/response contracts. The backend attaches highlights server-side using the stored spans
and original text (producing HTML or annotated text), or the frontend renders them from the
indices and categories.

### 26.4 Security and operations

Authentication and authorization (API keys or OAuth); HTTPS for data in transit; graceful error
handling (a missing analysis returns a clean error; pipeline exceptions are caught and returned
as error codes); API access logs recording user ID, time and doc ID for the audit trail; caching
for repeated requests; a load balancer in front when serving many users.

---

## 27. Batch processing, Airflow and big data

### 27.1 What Airflow is for

Orchestration · scheduling · dependency management · triggering Spark/Ray/ONNX jobs · monitoring
and retries · backfilling and reproducible workflows.

**Airflow does not process text.** Airflow tasks are lightweight wrappers around heavy jobs.

```
[Airflow orchestrates the entire DAG]
  Ingestion (Kafka/S3)      ← Airflow triggers
  Preprocessing (Spark/Ray) ← Airflow schedules
  Sentence Split            ← task
  Taxonomy Classifier       ← task
  Embeddings (ONNX)         ← task
  Vector Index (FAISS)      ← task
  Scoring Engine            ← task
  Save to S3/Parquet        ← task
  FastAPI Serve             ← Airflow triggers reload
```

| Stage | Airflow's role |
|---|---|
| Ingestion | trigger crawlers/extractors |
| Preprocessing | trigger Spark/Dask jobs |
| Classification | trigger Python scripts |
| Embeddings | batch + retries + logs |
| Scoring | run scoring scripts |
| Storage | load → save → archive |
| Serving | restart / reload the index |

**Not for**: real-time ingestion (use Kafka) · streaming pipelines (Flink / Spark Streaming) ·
low-latency inference (FastAPI) · heavy compute inside tasks (Spark/Ray).

Five reasons it earns its place: scheduling · dependency ordering (task A must finish before B)
· failure handling with automatic retries, alerting, full logging and resumption from the last
successful step · versioned reproducible workflows (run `classification_v2` only on new
articles, backfill using older configs) · triggering distributed jobs.

### 27.2 DAG examples

Minimal (the placeholder that ships in the repo):
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from src.api.service import run_pipeline

def batch_process():
    result = run_pipeline({"doc_id": "demo", "text": "Sample article text"})
    print(result)

default_args = {"start_date": datetime(2024, 1, 1)}
with DAG("media_nlp_batch_pipeline", schedule_interval="@daily",
         default_args=default_args, catchup=False) as dag:
    run_batch = PythonOperator(task_id="run_media_pipeline", python_callable=batch_process)
```

Full chain:
```python
with DAG("nlp_pipeline", schedule_interval="@daily") as dag:
    ingest     = BashOperator(task_id="fetch_articles",         bash_command="python ingest.py")
    preprocess = BashOperator(task_id="preprocess_text",         bash_command="python preprocess_spark.py")
    classify   = BashOperator(task_id="taxonomy_classification", bash_command="python classify.py --config taxonomy.yaml")
    embed      = BashOperator(task_id="generate_embeddings",     bash_command="python embed.py")
    score      = BashOperator(task_id="score_content",           bash_command="python score.py --config scoring.yaml")
    store      = BashOperator(task_id="save_results",            bash_command="python store.py")

    ingest >> preprocess >> classify >> embed >> score >> store
```
Airflow needs `main.py` as the entry point: the DAG loads raw files, triggers the main pipeline,
saves outputs as Parquet, and sends results to S3 or the DB. Run locally with
`airflow dags test media_nlp_batch_dag`. Optimised for both LocalExecutor and Cloud Composer.

### 27.3 Batch scripts

```python
# src/batch_processing/preprocess_spark.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from nlp_pipeline.preprocessing import preprocess

spark = SparkSession.builder.appName("NLP_Preprocess").getOrCreate()
preprocess_udf = udf(preprocess)
df = spark.read.parquet("raw_docs/")
df = df.withColumn("clean_text", preprocess_udf("text"))
df.write.mode("overwrite").parquet("clean_docs/")
```
```python
# src/batch_processing/classify_batch.py
from nlp_pipeline.main import run_pipeline
from pyspark.sql.functions import udf
pipeline_udf = udf(lambda text: run_pipeline({"text": text}))
```
Also: `preprocess_ray.py`, `score_batch.py`.

Storage helpers:
```python
# src/io_adapters/parquet_writer.py
import pandas as pd
def save_results(df, path="results.parquet"):
    df.to_parquet(path, index=False)
```
```python
# src/io_adapters/es_client.py (indexing side)
from elasticsearch import Elasticsearch
es = Elasticsearch("http://localhost:9200")
def index_result(doc):
    es.index(index="nlp_results", document=doc)
```
```python
# src/io_adapters/kafka_consumer.py  (future)
from kafka import KafkaConsumer
import json
def stream_documents(topic: str):
    consumer = KafkaConsumer(topic, bootstrap_servers="localhost:9092",
                             value_deserializer=lambda v: json.loads(v.decode("utf-8")),
                             auto_offset_reset="earliest")
    for msg in consumer:
        yield msg.value
```
```python
# src/io_adapters/s3_loader.py   (free if using MinIO)
import boto3
def load_from_s3(bucket, key):
    s3 = boto3.client("s3")
    return s3.get_object(Bucket=bucket, Key=key)["Body"].read().decode()
```

### 27.4 Big-data layer reference

1. **Ingestion (distributed, fault-tolerant)** — Kafka (streaming, event-based), S3/GCS/Azure
   Blob (bulk), Airbyte / Apache NiFi (connectors), Scrapy / Newspaper3k (news scraping).
   Principles: always store **raw text first** (immutable, versioned); ingestion writes Parquet.
2. **Preprocessing (distributed)** — Apache Spark / PySpark (best for large corpora), Ray
   (lightweight scaled Python), Dask (medium-big). Order: cleaning (HTML strip, boilerplate) →
   normalization (lowercase, unicode, accents) → tokenization (spaCy, HuggingFace Tokenizers,
   SparkNLP) → sentence segmentation → optional stopword removal → lemmatization. SparkNLP is
   attractive because it is distributed, has GPU acceleration available, extremely fast
   tokenizers, and is built for TB-scale.
3. **Taxonomy / ontology classification** — YAML with hierarchical keys, JSON schema, or Neo4j
   for large evolving ontologies. Methods in order of preference: rule-based matching (spaCy
   patterns, regex, keyword mapping) → ML classifiers (scikit-learn, XGBoost, SVM) → hybrid
   models (best for media analysis) → embedding similarity (SBERT, fastText, GloVe) → LLM
   zero-shot (slow; use sparingly). Scaling: preload the taxonomy into RAM, cache embeddings, use
   FAISS or Milvus for vector search.
4. **Embedding & vectorization** — the heaviest stage; see §23.
5. **Scoring & aggregation** — deterministic, YAML-driven; see §21.
6. **Storage** — Parquet (superior), Feather (fast), DuckDB (local analytics); vectors in FAISS
   (local CPU) or Milvus/Pinecone (cloud).
7. **Query & serving** — FastAPI, gRPC if speed matters, Redis caching,
   Elasticsearch/OpenSearch for text search, DuckDB for analytics queries.

**Free/open-source status**: Spark (Apache 2.0), Dask (BSD), Ray, Scrapy (BSD), the open-source
NLP libraries, FAISS, Parquet and open-source databases are all free to use. Caveat: **Airbyte's
core uses Elastic v2, which is not strictly OSI-approved**, so "free and open-source" needs
care. Managed/cloud versions of anything (managed warehouses, managed vector DBs, SaaS wrappers)
cost money. The dominant real cost is infrastructure — compute, storage, bandwidth, possibly
GPUs — not licences. Avoiding paid SaaS gives maximum control, flexibility and transparency,
which matches the reproducibility and customisation requirements.

### 27.5 Real-time vs batch split

**Real-time (< 1 s/document):** spaCy tokenization/POS/NER/sentence splitting (~0.1 s) · VADER
or a small-model sentiment pass · all lexicon and rule checks (loaded words, passive voice,
readability, quantifiers, hedges) · distilled or linear models (DistilBERT ≈ 0.5 s on CPU for a
few hundred words) · composite-score arithmetic · linguistic bias analysis · a light version of
entity analysis.

**Batch only:** per-sentence heavy transformers (fallacy classifier, fine-grained propaganda
classifier) · coreference resolution · pairwise NLI contradiction detection · NLI-based stance ·
trend analysis, LDA updates, classifier retraining · dimensionality reduction and clustering ·
FAISS index building · anything requiring corpus-wide data (trending keywords, share counts).

**Hybrid strategy:** new documents go through a **fast lane** (rules + small models) that
populates the database immediately with preliminary scores; a background process then runs the
heavy analyses and updates the records (adding fallacy spans, adjusting scores). The data is
available almost immediately at reasonable accuracy and improves over time. Periodic batch
re-processing runs when algorithms improve or new features are added. For an interactive
browser-extension use case, embed only the real-time components, or serve precomputed insights
when the article is already in the database.

Explicit note: **GPT-4 is "not deterministic or explainable enough for our needs."**

---

## 28. Deployment, Docker, CI/CD

### 28.1 Dockerfile (final, at the project root)

The Dockerfile **must** be at the repository root so Docker can see `src/`, `conf/`,
`data_schema/`, tests and requirements — Docker builds by collecting everything inside the
project directory. Placing it inside `src/`, `airflow_dags/`, `conf/` or `core_accelerators/` is
wrong and the build will fail to find the code and configs.

```dockerfile
FROM python:3.10-slim
WORKDIR /app

# OS dependencies for spaCy + scikit-learn
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Dependency files first — Docker layer caching
COPY requirements-dev.txt .
COPY pyproject.toml .
RUN pip install --no-cache-dir -r requirements-dev.txt

# Then the rest of the project
COPY . .

# NLTK data
RUN python -m nltk.downloader punkt stopwords wordnet

EXPOSE 8000
CMD ["uvicorn", "src.api.service:app", "--host", "0.0.0.0", "--port", "8000"]
```
Build and run:
```bash
docker build -t nlp-pipeline .
docker run -p 8000:8000 nlp-pipeline
# → http://localhost:8000/docs  (FastAPI Swagger UI)
```
Container logs showing `Application startup complete.` means Docker is working.

### 28.2 `.dockerignore`

```
pipe/
__pycache__/
*.pyc
*.pyo
*.pyd
*.log
.vscode/
.git/
.gitignore
notebooks/
output.txt
python310.exe
*.egg-info
```

### 28.3 `pyproject.toml`

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "media-nlp-pipeline"
version = "0.1.0"
description = "Deterministic NLP pipeline with taxonomy classification and scoring"
authors = [{ name = "Advaith Narayana Sarva" }]
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
  "pydantic>=2.0", "pyyaml>=6.0", "regex", "numpy",
  "scikit-learn", "spacy>=3.8", "nltk", "fastapi", "uvicorn",
]

[project.optional-dependencies]
dev = ["pytest", "black", "flake8"]

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]
```
Why it matters: it tells Python the code lives in `src/` (**without this the imports break**),
allows `pip install .` so the code runs inside Docker/Airflow/other machines, lists core
dependencies so Docker installs them automatically, and lets backend developers write
`from nlp_pipeline.preprocessing import clean_text`.

### 28.4 CI/CD — `.github/workflows/ci.yml`

```yaml
name: NLP Pipeline CI
on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"
      - name: Install dependencies
        run: pip install -r requirements-dev.txt
      - name: Run tests
        run: pytest
```
Merges to main run the tests, then deploy to staging; only if the tests pass (and, optionally,
after manual review) is the change promoted to production. Nothing untested goes live.

### 28.5 Infrastructure

Docker images orchestrated by Kubernetes (or Docker Compose for local); Infrastructure-as-Code
(Terraform / CloudFormation) for the data lake storage, databases, etc.; secrets (API keys, DB
passwords) stored securely and never hard-coded. Typical cloud mapping: **S3** for the
Bronze/Silver/Gold Parquet zones (encrypted bucket, restricted access) · **RDS or DynamoDB** for
the serving DB · **Amazon ES or Neptune** if search/graph is needed · **EC2 or EKS** for pipeline
jobs and APIs · the vector DB as a managed service or on the cluster.

Scaling: schedule Spark jobs for hundreds of articles per hour; run multiple analysis-service
instances in parallel; put the API behind a load balancer; cache repeated requests.

### 28.6 Logging and monitoring

Logs: per-document/batch pipeline logs (*"Doc 123: 2 fallacies detected (AdHominem, Strawman),
bias_score=72"*), error logs for failed documents, API access logs, system resource logs — all
aggregated centrally (ELK stack or CloudWatch).

Metrics to monitor: pipeline throughput (docs/hour) · latency per document · error rate · API
latency and error rate · CPU/memory utilisation · **drift in feature distributions** (e.g. the
average number of fallacies per article shifting over time — either a real trend in content or a
pipeline bug; either way it is interesting). Out-of-bounds values trigger an email/Slack alert.

Basic in-code logging:
```python
import logging
logging.basicConfig(filename="logs/pipeline.log", level=logging.INFO)
```

### 28.7 Security and confidentiality

Air-gapped-capable design · minimal OS surface (`python:3.10-slim`) · no external downloads at
runtime · no external network calls except through `io_adapters` · logs go to `logs/` and can be
disabled · Pydantic validates inbound and outbound data · all config YAML-validated before
runtime · private-network deployment with restricted access · encrypted data at rest and in
transit · all team members under NDA · **QA refers to content by ID rather than pasting
sensitive text into bug reports.**

### 28.8 Continuous improvement

The modular design (feature registry, taxonomy config, versioned models) allows components to be
updated without an overhaul. ML models are retrained periodically; every update is a new version
that must pass the same QA suite. Code reviews are enforced through Git/PR workflows. Internal
documentation covers the taxonomy, the scoring rationale, and how to interpret each feature —
necessary both for onboarding and for explaining results to stakeholders and clients who will
ask why an article received a given score.

### 28.9 Environment setup

Python **3.10** (3.12 broke the dependency set). Create the virtual environment in a **global
envs folder outside the project** so the project directory stays clean, and add the env name to
`.gitignore`.
```bash
python -m venv pipe
.\pipe\Scripts\activate          # Windows
source pipe/bin/activate         # macOS/Linux
pip install -r requirements-dev.txt
uvicorn src.api.service:app --reload
pytest -q
```
Install **CPU-only PyTorch**
(`torch==2.0.1 --extra-index-url https://download.pytorch.org/whl/cpu`) — no GPU is available,
and this keeps the system deterministic.
`.gitignore` covers: Python artifacts, the virtual environment, VS Code, logs, byte-compiled
files, Airflow junk, Docker, notebook caches, build artifacts and OS files. A `.gitattributes`
was added to normalise line endings (the Windows CRLF/LF warnings are harmless).

---

## 29. QA and testing strategy

### 29.1 The ten pillars

1. **Unit tests for components** — feed a known sentence to each detector and assert the flag.
   e.g. the bandwagon detector on *"Everyone knows the election was rigged."* must set
   `flags["bandwagon_effect"] = True` with a score above threshold; the ad hominem detector on a
   sentence containing an insult and a PERSON name must fire.
2. **Integration tests for the pipeline** — a curated set of sample articles with known issues,
   with the *expected full output* (features, flags, scores) stored and compared. A balanced test
   article → low bias score, no fallacy flags. A heavily biased test article → specific flags.
   Whenever code changes, these catch unexpected output changes; intentional changes update the
   expectations with version tracking.
3. **Deterministic reproducibility checks** — run the pipeline on the same input multiple times
   with the same version and require **bit-for-bit identical** results. Any nondeterminism (from
   parallel processing order or an ML model) must be identified and eliminated or controlled.
   Also verify that `pipeline_version` and other version metadata are correctly attached.
4. **Performance and load testing** — time the pipeline on various input sizes; batch throughput
   within an acceptable window; memory usage (embedding generation is heavy). If a single article
   takes too long, flag it for optimisation (caching language models, etc.).
5. **Regression testing on updates** — re-run all prior test articles and compare against the
   previous version. With no intended logic change, *nothing* should change. With an intended
   change (a new fallacy detector), only the expected new outputs may appear. Also **diff the
   Parquet schemas** to catch unwanted schema drift (a feature silently disappearing).
6. **Logging and traceability** — every document logged with its detections and score; each run
   has a run ID; outputs carry `processed_at` and version info. QA must be able to take an output,
   trace through the logs to the run that produced it, and reproduce that run in a debugging
   environment.
7. **Audit trails and version control** — every code or taxonomy change documented in version
   control plus a changelog linked to `pipeline_version`. It must be possible to answer *"why did
   this article get flagged?"* down to the specific rules and version applied.
8. **End-to-end acceptance testing** — validate the output JSON against the JSON Schema; verify
   highlighted spans map **exactly** to the original text (no off-by-one index errors, no missing
   context); check the frontend renders them correctly.
9. **Automated testing tools** — a test harness script that runs a set of input documents through
   the pipeline and diffs against expected output, producing a report; pytest/Postman for API
   calls including authentication, status codes and JSON shape; Selenium for UI checks
   (secondary).
10. **Continuous improvement** — QA also proposes improvements: if two similar articles yield
    inconsistent scores, the rules may need adjustment or a new feature may be required. In a
    small team the feedback loop is tight — issues found are discussed immediately and lead to
    quick fixes.

### 29.2 The canonical acceptance test

> *"According to Professor Smith, society is on the brink of collapse. Everyone agrees that if we
> allow the new policy, it will lead to disaster."*

Expected: **Appeal to Authority** (citing Professor Smith for a broad claim) + **Bandwagon**
("everyone agrees") + **Slippery Slope** (policy → disaster). QA verifies those flags are present,
that their text spans correspond to the right phrases, and that the final scores are bumped
appropriately. Missing flags = a detection bug; extra flags = a false positive to evaluate.

### 29.3 Cross-environment consistency

The pipeline must produce the same results on a developer machine and in production. Any
discrepancy points to a dependency or configuration issue — commonly a different model version
installed.

### 29.4 Test file responsibilities

| Test | Guards |
|---|---|
| `test_preprocessing.py` | cleaning / normalization behaviour (including idempotency) |
| `test_segmentation.py` | sentence splitting is stable and correct |
| `test_rules_engine.py` | rule-based category mapping |
| `test_scoring_engine.py` | scoring matches `scoring_v1.yaml` |
| `test_determinism.py` | same input twice → identical output (**the critical invariant**) |
| `test_output_schema.py` | every API output matches `output_schema.json` |

Quality gates: `pytest -q` · `flake8` · `black --check .`

---

## 30. Build order and coding discipline

### 30.1 The ten rules for actually writing the code

1. **Start with ONLY ONE module** — `preprocessing.py`. It is easy, predictable, deterministic,
   the first pipeline stage, required by everything downstream, and gives immediate momentum and
   a visible first success.
2. **Build ONE class at a time**, in this order:
   TextPreprocessor → SentenceSegmenter → FeatureExtractor → EmbeddingGenerator → RuleEngine →
   MLClassifier → HybridRouter → OntologyGraph → ScoringEngine → OutputBuilder. **Do not jump
   around.**
3. **Do not write functional code in `main.py` yet** — it stays minimal until the preprocessor,
   segmenter, features and embeddings exist, because the pipeline cannot run before then.
4. **Keep tests ready so you don't break things** — code → run test → fix → run test, like real
   QA.
5. **Focus on MINIMUM CODE first** — preprocessor returns cleaned text · segmenter returns
   sentences · features returns basic features · embeddings returns dummy vectors · rule engine
   returns no labels · classifier returns dummy predictions · hybrid router merges · scoring
   produces a simple score · postprocessor returns JSON. Add heavy logic only after that works.
   **Do not write the advanced version first.**
6. **Code ONE FILE → git commit → move to the next file.** Progress stays clean and safe.
7. **Do not touch GPU, C++, CUDA or FAISS yet** — leave `gpu_router`, `core_accelerators`,
   `vector_index` and advanced `embeddings_onnx` for later. Build the logic first.
8. **Build a "stupid simple pipeline" first**:
   `clean → split → fake_features → fake_embeddings → fake_labels → fake_score → json`.
   This proves the pipeline flow works, lets Airflow run it, lets FastAPI call it, and makes
   basic tests pass. **Jumping straight to the heavy stuff is the #1 beginner mistake.**
9. **Then upgrade modules one by one** — batch logic, real embeddings, the ML model, the FAISS
   index, ontology logic, scoring formulas. One improvement at a time.
10. **Remember the mission** — a production-level deterministic media analysis pipeline, not a
    college project. The "side quest hours" spent on folder structure, configs, YAML, schemas,
    environment, Docker, git and the orchestration plan were not wasted: coding becomes
    effortless because the design is solid.

### 30.2 The reduced roadmap (for when it feels overwhelming)

Only **three things** matter at the start.

- **PHASE 1 (today)** — preprocess → segment → embed. Single goal: *"Given a raw text, can my
  pipeline produce sentence embeddings?"* Do not think about the vector DB, scoring, taxonomy,
  ML, the hybrid router, C++, CUDA/GPU, Airflow, FastAPI, `main.py`, storage or batching.
- **PHASE 2 (later)** — rule engine (simple, keyword-based) + scoring engine (simple, count
  labels). This produces the first real output.
- **PHASE 3 (later)** — hybrid + vector search: FAISS, ML, ONNX, scoring YAML logic, taxonomy
  graph.
- **PHASE 4 (last)** — production engineering: Docker, Airflow, FastAPI, batch processing, C++
  accelerators, GPU router, vector DB.

### 30.3 The full recommended build order

1. `nlp_pipeline/shared_types.py` — convert `NormalizedDocument` and `Sentence` to proper
   dataclasses; add `Features`, `ArgumentSpan`, `Classification`, `ScoredDocument`. These are the
   contracts every stage signs.
2. **Fix `InputRouter`** — instantiate real reader objects in the constructor; wire
   `_handle_file_path()` to actually call `reader.read(file_path)`; remove `_mock_file_read()`.
3. `nlp_pipeline/deterministic_utils.py` — implement `set_global_seeds`, `hash_to_document_id`,
   `compute_config_hashes`.
4. `conf/taxonomy_v1.yaml` — design and fill the taxonomy. Everything downstream (OntologyGraph,
   FeatureRegistry, RuleEngine) depends on it.
5. `taxonomy_tools/taxonomy_loader.py` + `nlp_pipeline/ontology_graph.py` — load the taxonomy,
   build the networkx graph.
6. `io_adapters/storage_clients.py` — `JSONLWriter` for Bronze, `ParquetWriter` for Silver/Gold
   using the canonical schema; `StorageClientFactory` wires them.
7. `nlp_pipeline/preprocessing.py` — implement `TextProcessor.normalize()`. Output → Silver.
8. `nlp_pipeline/segmentation.py` — implement `SentenceSegmenter.segment()` using pysbd/spaCy.
9. **Argument mining** — new module `nlp_pipeline/argument_miner.py`, `ArgumentMiner.extract()`
   returning claim/premise/support spans. Sits between segmentation and feature extraction.
10. **Feature Registry** — new module `nlp_pipeline/feature_registry.py` implementing
    taxonomy-aware feature gating; consults `OntologyGraph` to decide which of the 13 layers run.
11. `nlp_pipeline/features.py` — implement all 13 layers in priority order (Phase 1 first).
12. `conf/scoring_v1.yaml` — design the weights for all formulas (w_c, w_f, disruption factors,
    w1..w5 for factuality).
13. `nlp_pipeline/rules_engine.py` — rule-based classification; taxonomy-aware; use OntologyGraph
    for threshold calibration.
14. `nlp_pipeline/scoring_engine.py` — implement all five scoring formulas; reads
    `scoring_v1.yaml`.
15. `nlp_pipeline/hybrid_router.py` — merge logic.
16. `nlp_pipeline/postprocessing.py` — output schema builder; write the Gold Parquet; fill
    `data_schema/output_schema.json` alongside it.
17. `main.py` — implement the `PipelineRunner` class; fix hard-coded config paths (use an env var
    or CLI argument).
18. **ML path** (in parallel after step 11) — `embeddings_onnx.py`, `vector_index.py`,
    `ml_classifier.py` need actual ONNX model files in `models/`.
19. `api/service.py` + `api/models.py` — the FastAPI app: ingestion → pipeline → Gold Parquet →
    SQL serving DB.
20. **Tests** — implement everything in `tests/`.
21. **Batch processing** — `batch_processing/preprocess_ray.py`, `preprocess_spark.py`,
    `classify_batch.py`.

Reader/adapter build order runs alongside: file readers → ParquetReader → ArchiveReader →
S3Client → APIClient → KafkaClient, **freezing ingestion before moving to preprocessing.**

### 30.4 PipelineRunner — the orchestrator

```python
class PipelineRunner:
    def __init__(self, config):
        self.pre    = TextProcessor(config)
        self.seg    = SentenceSegmenter(config)
        self.feat   = FeatureExtractor(config)
        self.embed  = EmbeddingGenerator(config)       # optional
        self.rules  = RuleEngine(config)
        self.ml     = MLClassifier(config)             # optional
        self.hybrid = HybridRouter(self.rules, self.ml, config)
        self.score  = ScoringEngine(config)
        self.post   = PostProcessor(config)

    def run(self, doc: InternalDocument) -> ScoredDocument:
        normalized = self.pre.normalize(doc)
        sentences  = self.seg.segment(normalized)
        features   = self.feat.build_features(normalized, sentences, doc.source_metadata)
        labels     = self.hybrid.merge(
                         self.rules.classify(features, sentences),
                         self.ml.predict(features, sentences),
                         ontology,
                     )
        scores     = self.score.score(labels, features)
        return self.post.to_output_schema(doc, normalized, sentences, labels, scores)
```
An earlier equivalent form using the text-in/text-out signature:
```python
    def run(self, text):
        clean   = self.pre.clean(text)
        sents   = self.seg.split(clean)
        feats   = self.fe.extract(sents)
        vectors = self.embed.embed(sents)
        labels  = self.hybrid.classify(sents, feats, vectors)
        scored  = self.score.apply(labels, sents)
        return self.post.build(scored)
```
`main.py` also parses CLI arguments (`--text`, `--input`, `--config`), calls `set_global_seeds`,
and is the **single entry point that both Airflow and FastAPI depend on**. FastAPI loads the
pipeline once at startup and calls `run` per request.
```bash
python src/main.py --text "The president announced new policies today..."
```

### 30.5 OOP guidance

Use OOP for pipeline components; plain functions for stateless utilities.

| File | Class |
|---|---|
| `preprocessing.py` | `TextPreprocessor` / `TextProcessor` |
| `segmentation.py` | `SentenceSegmenter` |
| `features.py` | `FeatureExtractor` |
| `embeddings_onnx.py` | `EmbeddingGenerator` |
| `rules_engine.py` | `RuleEngine` |
| `ml_classifier.py` | `MLClassifier` |
| `hybrid_router.py` | `HybridRouter` |
| `ontology_graph.py` | `OntologyGraph` |
| `scoring_engine.py` | `ScoringEngine` |
| `postprocessing.py` | `OutputBuilder` / `PostProcessor` |
| `vector_index.py` | `VectorIndex` (stateful → definitely a class) |
| `deterministic_utils.py` | **functions only** |
| `gpu_router.py` | **functions only** (a capability checker + dispatcher with no state) |

**Not OOP**: simple helpers, YAML loaders, deterministic utilities, C++/CUDA wrappers.

Why OOP here: extensible (add a new model, scoring version or rules without breaking old code) ·
reusable (batch, API and Airflow call the *same* classes) · testable (unit tests target class
methods) · dependency injection (`RuleEngine(config.rules)`, `ScoringEngine(config.scoring)`,
`MLClassifier(model_path)`) · deterministic (classes encapsulate state).

`gpu_router.py` should stay functional:
```python
def has_gpu():
    try:
        import torch
        return torch.cuda.is_available()
    except Exception:
        return False

def cosine_similarity(a, b):
    return cuda_cosine_sim(a, b) if has_gpu() else cpu_cosine_sim(a, b)
```
You want `sim = cosine_similarity(vec1, vec2)`, not `router = GPURouter(); router.cosine_similarity(...)`.
Make it a class only if you need GPU memory pooling, dynamic multi-GPU switching, fallback
strategies, warm vs cold kernels, or async CUDA-stream batch queueing.

### 30.6 How data travels between modules

**Never pass text through files between modules.** File I/O is slow, disk-bound, hard to
parallelize, hard to test, hard to scale, and impossible to keep deterministic if files mutate.
That is how junior engineers build pipelines.

Pass everything **in memory as Python objects**:
```
raw string → cleaned string → list of sentences → list of tokens → embeddings
           → labels → scores → output JSON
```

| Stage | Format | Why |
|---|---|---|
| Ingestion (API) | JSON → text string | clean & fast |
| Ingestion (batch) | Parquet | best for TB-scale |
| Inside the pipeline | Python objects (str, list, dict, ndarray) | fastest processing |
| ML & embeddings | numpy arrays | needed for vector math |
| Saving results | JSON or Parquet | depends on mode |
| Feeding backend | JSON | frontend-friendly |
| Long-term storage | Parquet / Feather | efficient |

Very large text (100k–1M characters): still keep it in memory as a string, break it into
sentences, and vectorize in batches. If documents genuinely exceed RAM (books, legal corpora,
research archives): use **streaming batch ingestion** — read in chunks, process in streaming
batches, still passing cleaned chunks in memory. Spark/Ray handles this automatically.

Avoid: writing cleaned text to disk · passing files between modules · using JSON files between
steps · writing/reading intermediate Parquet between steps · passing data through temporary
directories · serializing after every stage.

This in-memory design is how fast deterministic NLP pipelines work at Bloomberg, Google News,
GDELT, Factiva, Reuters NLP and media bias monitoring systems.

The ideal end-to-end data flow:
```
(Input) JSON / Parquet
  ↓ (Ingestion)      → in-memory string
  ↓ Preprocessing    → in-memory string
  ↓ Segmentation     → list of sentences
  ↓ Feature extractor→ list of feature dicts
  ↓ Embedding        → numpy matrix
  ↓ Rules + ML       → label dicts
  ↓ Hybrid Router    → final labels
  ↓ Ontology Graph   → hierarchical labels
  ↓ Scoring          → score dict
  ↓ Postprocessing   → output JSON object
  ↓ Output save      → JSON (API) or Parquet (batch)
```

---

## 31. Decisions log

| Decision | Verdict | Reasoning |
|---|---|---|
| **Kafka now?** | ❌ No — Phase 1 has no Kafka | The project is deterministic batch processing, not streaming. Kafka adds cluster management, brokers, partitions, offsets, retries, idempotency, schema registry, monitoring, load balancing and deployment for **zero current benefit**. Removing it simplifies IO adapters, lowers maintenance, shrinks Docker images, speeds development and eases Airflow integration. **You never add Kafka before you need it.** |
| **Kafka later?** | ✅ Easy to add | Phase 2 adds `kafka_consumer.py` / `kafka_producer.py` as a **new entry point, not a rewrite**, because `run_pipeline()` is pure, input/output schemas are structured, and IO adapters are independent. Design for it now by keeping ingestion modular, `run_pipeline()` pure, inputs and outputs schema-structured, and adapters independent. |
| **Which Kafka image (when needed)?** | `bitnami/kafka` + `bitnami/zookeeper` | Best stability and documentation; works on Windows/Linux/Mac; no weird bugs; handles ZooKeeper automatically; production-grade configs; light and easy in Docker Desktop. Avoid Confluent `cp-kafka` (heavy, complex, enterprise-only features, needs Control Center + Schema Registry, overkill) and `wurstmeister/kafka` (old, unmaintained, breaks on Windows and Docker Desktop, ZooKeeper and hostname issues). |
| **spaCy or NLTK?** | ✅ spaCy, ❌ NLTK | spaCy is modern, fast (Cython), industrial and production-ready with a strong tokenizer, lemmatizer, NER and rule matcher, and integrates with HuggingFace/ONNX. NLTK is slow, academic, has a weaker sentence tokenizer and is not suited to production or large datasets. |
| **Files or memory between modules?** | ✅ In-memory Python objects | See §30.6. Files at the boundaries only (JSON for API, Parquet for batch). |
| **Vector DB now?** | ❌ Not for v1; FAISS when needed | Embeddings first, stored in memory; add FAISS only at `taxonomy_suggestions.py`, hybrid similarity fallback, rule expansion or deduplication. Cloud vector DBs (Milvus/Pinecone/Weaviate/Qdrant) are unnecessary, cost money, and add infrastructure the project doesn't need. |
| **Does the vector DB affect scores?** | ❌ Never | It is read-only semantic memory. Embedding similarity is statistical and would undermine determinism. |
| **Rules or ML first?** | ✅ Rules primary, ML secondary | Rule-based is deterministic, explainable and auditable — exactly what enterprise AI, moderation, legal, finance and healthcare buyers want. ML fills the ambiguous gaps. |
| **OOP everywhere?** | Only where it helps | Classes for stateful pipeline components; functions for utilities, YAML loaders, deterministic helpers and C++/CUDA wrappers. |
| **GPU by default?** | ❌ No | Determinism. GPU paths are optional, disabled by default, and activated only if explicitly enabled or detected. |
| **Hadoop / Hive / MapReduce?** | ❌ Skip | The project is modern Python NLP, embedding-heavy and streaming-friendly — Spark, Ray and (eventually) Kafka fit; the old Hadoop ecosystem does not. |
| **Which big-data tools?** | ✅ Spark, Ray, Kafka (later) | All free/open-source; the real cost is compute, storage and bandwidth. |
| **Python version** | 3.10 | 3.12 broke the dependency set. |
| **WSL required?** | ❌ No | Not needed for this project — it runs natively on Windows with Docker Desktop. |
| **PyTorch build** | CPU-only wheel | No GPU available; also keeps the system deterministic. |
| **GPT-4 in the pipeline?** | ❌ | "Not deterministic or explainable enough for our needs." |
| **Where does file-reading code live?** | `io_adapters/` only | Preprocessing and the pipeline never read files. Originally a single `universal_loader.py`; the final design splits into `file_readers.py` (BaseReader + per-format readers) plus `ingest_clients.py`. |
| **Should `BaseReader` move out of `file_readers.py`?** | ❌ Keep it there | `file_readers.py` represents file-like inputs and BaseReader is the contract for file ingestion; mixing in API/Kafka/ES ingestion would conflate *file readers* with *source readers*. |
| **Do readers feed NLP directly?** | ❌ No | Introduce `InternalDocument`; only its `text` flows into NLP. Never let raw readers leak into the NLP layer. |
| **Airflow for text processing?** | ❌ Orchestration only | Tasks are lightweight wrappers around heavy jobs run by Spark/Ray. |
| **Where does the Dockerfile go?** | Repository root | Docker must see `src/`, `conf/`, `data_schema/`, tests and requirements. |
| **Serving mode** | Scheduled batch + API reads from the serving DB | Chosen for confidentiality and determinism; on-demand analysis uses a lighter path. |
| **Taxonomy mapping: rules or ML?** | Rule-based mapping preferred | Deterministic, traceable, and tunable by non-engineers via YAML. |
| **Can the system auto-expand the taxonomy?** | Only as human-reviewable suggestions | Never silently mutate the production taxonomy; approved diffs become a new versioned file with an audit trail. |

---

## 32. Accelerators — C++ and CUDA

### 32.1 Why they exist

There is no GPU on the development machine, so most of the pipeline can still be made fast on
CPU using **Cython** (simple), **PyBind11** (professional-grade), C++ modules compiled to
`.so`/`.pyd`, and **SIMD operations (AVX2/AVX-512)**. GPU support is provided as optional hooks
for users who do have a GPU.

### 32.2 Placement

```
src/core_accelerators/          # CPU acceleration
  CMakeLists.txt
  text_ops.cpp / text_ops.h     # heavy text operations: fast loops, normalization, regex-like ops,
                                #   SIMD-friendly prefix scans
  nlp_accel.cpp                 # higher-level NLP acceleration (feature computation)
  bindings.cpp                  # PyBind11 bridge exposing C++ to Python

src/gpu_support/                # GPU acceleration
  cuda_ops.cu / cuda_ops.h      # CUDA kernels: batched similarity, heavy vector ops
  bindings.cpp
  build.sh
```
Build and use:
```bash
pip install pybind11
pip install .
```
```python
from core_accelerators import text_ops
fast_sentence_split = text_ops.split_sentences(...)
```

### 32.3 Minimal valid templates

```cpp
// text_ops.cpp
#include "text_ops.h"
#include <string>
std::string reverse_text(const std::string &input) {
    std::string out = input;
    std::reverse(out.begin(), out.end());
    return out;
}
```
```cpp
// bindings.cpp
#include <pybind11/pybind11.h>
#include "text_ops.h"
namespace py = pybind11;
PYBIND11_MODULE(text_ops, m) {
    m.def("reverse_text", &reverse_text);
}
```
```cpp
// cuda_ops.cu — placeholder kernel; proves the structure, never actually run without a GPU
extern "C" __global__
void multiply_by_two(float *x, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) x[idx] *= 2;
}
```

### 32.4 GPU routing rules

**GPU code must NOT be used by default — determinism comes first.** It must be optional, not
required to run, disabled by default, and activated only when explicitly enabled or a GPU is
detected.

```python
# src/nlp_pipeline/gpu_router.py
import torch

def use_gpu():
    return torch.cuda.is_available()

def gpu_vectorize(text):
    if not use_gpu():
        raise RuntimeError("GPU not available")
    from gpu_support import cuda_ops
    return cuda_ops.vectorize(text)
```
Guarded-import pattern used by consumers:
```python
try:
    from gpu_support import cuda_ops
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False
```
Service-level selection:
```python
def run_pipeline(doc):
    if use_gpu():
        print("GPU acceleration enabled")
    else:
        print("Running CPU-only deterministic mode")
    return classify(doc)
```
**Deterministic mode always uses CPU.** GPU mode is used only when manually enabled or detected.

### 32.5 Status and staging

`src/core_accelerators/` and `src/gpu_support/` currently hold one-line stubs. **Do not wire them
into the main path until the core NLP logic works** (build-discipline rule #7). Their presence
demonstrates the architecture supports an optional performance layer; the intended CPU use is
PyBind11-exposed SIMD acceleration for heavy token operations (normalization, prefix scans) and
the intended GPU use is parallel feature extraction or token-level operations.

Learning budget quoted for the whole advanced stack: Airflow ~2 h · Docker ~2–3 h · PyBind11
~15 min · CUDA ~10–20 min · GitHub Actions ~30 min ≈ **6 hours total**.

---

---

## 33. Master file-by-file blueprint

Produced in three passes: a first "high-level pseudocode for every file" pass (rejected as "the
worst, not good pseudocode"), a **principal-engineer pass** ("how a principal engineer would
sketch the implementation before handing it to a team"), and finally an **OPTION A full
enterprise blueprint** with exact imports, libraries and learning topics per file. The content
below merges passes two and three.

### 33.1 `src/main.py` — orchestration brain

Single entry point for non-Airflow runs (CLI / script). Wires config, IO adapters, pipeline
stages, storage.

**Libraries:** stdlib `os`, `pathlib`, `logging`, `argparse`, `json`; third-party `pyyaml`,
optionally `jsonschema`.

```python
# standard
import os, json, logging, argparse
from pathlib import Path
# third-party
import yaml                                    # pyyaml
# import jsonschema                            # optional
# internal
from io_adapters.input_router import InputRouter
from io_adapters.storage_clients import StorageClientFactory
from taxonomy_tools.taxonomy_loader import load_taxonomy
from nlp_pipeline.preprocessing import TextProcessor
from nlp_pipeline.segmentation import SentenceSegmenter
from nlp_pipeline.features import FeatureExtractor
from nlp_pipeline.rules_engine import RuleEngine
from nlp_pipeline.ml_classifier import MLClassifier
from nlp_pipeline.hybrid_router import HybridRouter
from nlp_pipeline.ontology_graph import OntologyGraph
from nlp_pipeline.scoring_engine import ScoringEngine
from nlp_pipeline.postprocessing import PostProcessor
from nlp_pipeline.embeddings_onnx import EmbeddingGenerator
from nlp_pipeline.vector_index import VectorIndex
from nlp_pipeline.deterministic_utils import set_global_seeds, compute_config_hashes
```
```python
def load_yaml(path: str) -> dict:
    """Load a YAML file and return as dict."""

def load_configs():
    pipeline_cfg = load_yaml("conf/pipeline_v1.yaml")
    taxonomy_cfg = load_yaml("conf/taxonomy_v1.yaml")
    scoring_cfg  = load_yaml("conf/scoring_v1.yaml")
    return pipeline_cfg, taxonomy_cfg, scoring_cfg

def build_context(pipeline_cfg, taxonomy_cfg, scoring_cfg):
    """Create every service the pipeline needs. Seeds FIRST."""
    set_global_seeds(pipeline_cfg["pipeline"]["seed"])
    taxonomy  = load_taxonomy(taxonomy_cfg)
    ontology  = OntologyGraph(taxonomy)
    input_router   = InputRouter(pipeline_cfg["input"])
    storage_client = StorageClientFactory.create(pipeline_cfg["output"])
    text_processor    = TextProcessor(pipeline_cfg["pipeline"])
    segmenter         = SentenceSegmenter(pipeline_cfg["pipeline"])
    feature_extractor = FeatureExtractor(pipeline_cfg["feature_extraction"])
    rule_engine       = RuleEngine(taxonomy_cfg)

    ml_classifier = None
    if pipeline_cfg["pipeline"]["enable_ml_classifier"]:
        ml_classifier = MLClassifier(pipeline_cfg["ml"])

    hybrid_router  = HybridRouter(pipeline_cfg.get("hybrid", {}), ontology)
    scoring_engine = ScoringEngine(scoring_cfg)

    embedding_generator = vector_index = None
    if pipeline_cfg["pipeline"]["enable_embeddings"]:
        embedding_generator = EmbeddingGenerator(pipeline_cfg["embeddings"])
    if pipeline_cfg["pipeline"]["enable_vector_index"]:
        vector_index = VectorIndex(pipeline_cfg["embeddings"])

    postprocessor = PostProcessor(
        output_schema_path="data_schema/output_schema.json",
        pipeline_config=pipeline_cfg, taxonomy_config=taxonomy_cfg,
        scoring_config=scoring_cfg)

    config_hashes = compute_config_hashes(pipeline_cfg, taxonomy_cfg, scoring_cfg)
    return { "input_router": …, "storage_client": …, "text_processor": …, "segmenter": …,
             "feature_extractor": …, "rule_engine": …, "ml_classifier": …,
             "hybrid_router": …, "ontology": …, "scoring_engine": …,
             "embedding_generator": …, "vector_index": …, "postprocessor": …,
             "config_hashes": config_hashes }

def process_document(ctx, raw_input_obj):
    internal_doc = ctx["input_router"].to_internal_document(raw_input_obj)
    normalized   = ctx["text_processor"].normalize(internal_doc)
    segments     = ctx["segmenter"].segment(normalized)
    features     = ctx["feature_extractor"].build_features(
                       normalized, segments, internal_doc.metadata)
    rules_result = ctx["rule_engine"].classify(features, segments)

    ml_result = None
    if ctx["ml_classifier"] is not None:
        ml_result = ctx["ml_classifier"].predict(features, segments)

    final_labels = ctx["hybrid_router"].merge(rules_result, ml_result, ctx["ontology"])
    scores       = ctx["scoring_engine"].score(final_labels, features)

    if ctx["embedding_generator"] is not None:
        embedding = ctx["embedding_generator"].embed(normalized.full_text)
        if ctx["vector_index"] is not None:
            ctx["vector_index"].upsert(internal_doc.document_id, embedding,
                                       final_labels, scores)

    return ctx["postprocessor"].to_output_schema(
        internal_doc, normalized, segments, final_labels, scores, ctx["config_hashes"])

def run_pipeline():
    ctx = build_context(*load_configs())
    for batch in ctx["input_router"].iter_source_batches():
        for raw_input_obj in batch:
            ctx["storage_client"].write(process_document(ctx, raw_input_obj))

if __name__ == "__main__":
    # parse CLI args (config path override, run mode), configure logging, run_pipeline()
```
**Learn:** "Python PyYAML tutorial" · "Python logging basicConfig" · "dependency injection
python simple pattern" · "argparse python tutorial".

### 33.2 `src/api/models.py` — contracts between FastAPI and pipeline

**Libraries:** `pydantic`, `typing`.
```python
class AnalyzeRequest(BaseModel):
    source_type: str                       # "file" | "inline_text" | "url" | "es" | "api"
    text: Optional[str]
    file_name: Optional[str]
    mime_type: Optional[str]
    payload: Optional[Dict[str, Any]]      # raw JSON if needed
    source_config_override: Optional[Dict[str, Any]]

class SentenceLabel(BaseModel):
    sentence_id: str
    text: str
    start_char: int
    end_char: int
    taxonomy_nodes: List[Dict[str, Any]]   # {id, label, score}

class DocumentScore(BaseModel):
    metric_name: str                       # e.g. "objectivity_score"
    value: float
    explanation: Optional[str]

class AnalyzeResponse(BaseModel):
    document_id: str
    normalized_text: str
    sentences: List[SentenceLabel]
    scores: List[DocumentScore]
    taxonomy_version: str
    pipeline_version: str
    run_metadata: Dict[str, Any]           # config hashes, timestamps, seed
```
**Learn:** "Pydantic BaseModel basics" · "FastAPI request & response models".

### 33.3 `src/api/service.py` — thin HTTP layer

**Libraries:** `fastapi`, `uvicorn`; internal `main.load_configs/build_context/process_document`,
`api.models`.
```python
app = FastAPI()
PIPELINE_CONTEXT = None

@app.on_event("startup")
def startup_event():
    """Initialize the pipeline context ONCE when the API starts."""
    global PIPELINE_CONTEXT
    PIPELINE_CONTEXT = build_context(*load_configs())

@app.get("/health")
def health_check() -> Dict[str, Any]:
    # optionally ping the ONNX model, vector index, config hashes
    return {"status": "ok"}

@app.get("/taxonomy")
def taxonomy():
    return currently loaded taxonomy + version id

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    ctx = PIPELINE_CONTEXT
    raw_input_obj = {"source_type": request.source_type, "text": request.text,
                     "file_name": request.file_name, "mime_type": request.mime_type,
                     "payload": request.payload,
                     "source_config_override": request.source_config_override}
    output_obj = process_document(ctx, raw_input_obj)
    # validate against output_schema.json, then wrap
    return AnalyzeResponse(**output_obj)
```
**Learn:** "FastAPI tutorial" · "FastAPI startup events" · "Uvicorn how to run FastAPI app".

### 33.4 `batch_processing/preprocess_spark.py`

**Libraries:** `pyspark`; internal input router + the three NLP base components.
```python
def spark_preprocess():
    pipeline_cfg, taxonomy_cfg, scoring_cfg = load_configs()
    input_router      = InputRouter(pipeline_cfg["input"])
    text_processor    = TextProcessor(pipeline_cfg["pipeline"])
    segmenter         = SentenceSegmenter(pipeline_cfg["pipeline"])
    feature_extractor = FeatureExtractor(pipeline_cfg["feature_extraction"])

    spark = SparkSession.builder.appName("NLPPreprocess").getOrCreate()
    raw_docs_iter = input_router.iter_raw_records_for_spark()
    # create a Spark DataFrame from raw_docs_iter
    # define UDFs: udf_preprocess(text) -> cleaned_text, tokens …
    #   (wraps TextProcessor + FeatureExtractor operations)
    # df.write.mode("overwrite").parquet(pipeline_cfg["output"]["path"] + "/preprocessed.parquet")
    spark.stop()
```
**Learn:** "PySpark DataFrame basics" · "Spark UDF tutorial" · "When to use Spark vs plain
Python".

### 33.5 `batch_processing/preprocess_ray.py`

```python
@ray.remote
def process_single_remote(raw_input_obj, pipeline_cfg, feature_cfg):
    """Recreate TextProcessor/Segmenter/FeatureExtractor INSIDE the worker, then process."""

def ray_preprocess():
    ray.init()
    pipeline_cfg, taxonomy_cfg, scoring_cfg = load_configs()
    input_router   = InputRouter(pipeline_cfg["input"])
    storage_client = StorageClientFactory.create(pipeline_cfg["output"])
    futures = [process_single_remote.remote(obj, pipeline_cfg["pipeline"],
                                            pipeline_cfg["feature_extraction"])
               for batch in input_router.iter_source_batches() for obj in batch]
    for result in ray.get(futures):
        storage_client.write_preprocessed(result)
    ray.shutdown()
```
**Learn:** "Ray remote functions and actors" · "Ray vs Spark differences".

### 33.6 `batch_processing/classify_batch.py`

```python
def classify_batch():
    ctx = build_context(*load_configs())
    preprocessed_path = pipeline_cfg["output"]["path"] + "/preprocessed.parquet"
    # df = pd.read_parquet(preprocessed_path)
    # for each row: reconstruct raw_input_obj or normalized_doc,
    #               run classification + scoring with ctx,
    #               write output via ctx["storage_client"]
    # (skip the steps already done during preprocessing)
```
**Learn:** "Pandas read_parquet" · "Separating preprocessing from classification".

### 33.7 `io_adapters/input_router.py`

```python
class InputRouter:
    def __init__(self, input_config):
        self.config = input_config
        self.pdf_reader  = PDFReader();  self.docx_reader = DocxReader()
        self.ppt_reader  = PPTReader();  self.txt_reader  = TxtReader()
        self.csv_reader  = CSVReader(input_config.get("csv", {}))
        self.json_reader = JSONReader(input_config.get("json", {}))
        self.api_client     = APIClient(input_config.get("api", {}))
        self.es_client      = ESClient(input_config.get("es", {}))
        self.kafka_client   = KafkaClient(input_config.get("kafka", {}))
        self.s3_client      = S3Client(input_config.get("s3", {}))
        self.scraper_client = ScraperClient(input_config.get("scrape", {}))
        self.redis_client   = RedisClient(input_config.get("redis", {}))

    def _route_file(self, file_name, file_bytes, mime_type):
        """Choose the reader by extension or MIME type, call reader.receive(), return doc."""

    def to_internal_document(self, raw_input_obj):       # PUSH (API / CLI)
        """Validate against input_schema, dispatch by source_type."""

    def iter_source_batches(self):                        # PULL (batch / Airflow)
        """Generator yielding BATCHES of InternalDocument.
        Handles pagination and backpressure for large workloads."""
```
**Learn:** "Python isinstance/dict/list handling" · "MIME types and file extensions" ·
"adapter / strategy patterns in Python".

### 33.8 `io_adapters/file_readers.py`

**Libraries:** `pdfplumber` or `PyPDF2`, `PyMuPDF` (fitz), `python-docx`, `python-pptx`, `csv`,
`json`, `chardet`/`charset_normalizer`, `beautifulsoup4`, `markdown`, `pandas`, `pyarrow`,
`Pillow` + `pytesseract`, `magic`.

Shared helper `_make_internal_document(text, file_metadata)` generates a deterministic
`document_id` from `hash(path + size + timestamp)` (or the SHA-256 content hash) and attaches
source `"file"` plus the subtype.

```python
class PDFReader:
    def receive(self, file_bytes, file_name):
        """Load with the PDF lib from memory, extract text per page, join with separators."""
    def fetch(self, file_path):
        return self.receive(Path(file_path).read_bytes(), file_path)

class DocxReader:  # python-docx, same skeleton
class PPTReader:   # extract text from slide shapes
class TxtReader:   # open with the detected encoding, best effort
class CSVReader:
    def __init__(self, csv_config): self.text_column = csv_config.get("text_column")
    def fetch_many(self, file_path):
        """One InternalDocument per row (row_id appended)."""
class JSONReader:
    def __init__(self, json_config): self.text_field = json_config.get("text_field")
    def fetch_many(self, file_path):
        """Handle JSON lines or an array of objects; locate the configured text field."""
```
**Learn:** "pdfplumber basic usage" · "python-docx tutorial" · "python-pptx text extraction" ·
"CSV file handling in Python".

### 33.9 `io_adapters/ingest_clients.py`

**Libraries:** `requests`, `elasticsearch`, `boto3`, `kafka-python` (or `confluent-kafka`),
`redis`, `beautifulsoup4`.

```python
class APIClient:
    def __init__(self, config):
        self.base_url = config.get("base_url"); self.auth = config.get("auth")
    def receive(self, payload):    """PUSH: extract text from the incoming payload fields."""
    def fetch(self, query_config): """PULL: HTTP GET/POST, handle pagination (next_page tokens),
                                    yield one InternalDocument per item."""

class ESClient:
    def receive(self, hit_dict):   """Take _source, extract text + fields."""
    def fetch(self, query_config): """Build the query from config (index, filters, time range);
                                    use scroll / search_after for large result sets."""

class S3Client:
    def receive(self, s3_event):   """Triggered by an S3 event JSON: bucket/key → download →
                                    dispatch to FileReaders by extension."""
    def fetch(self, s3_config):    """list_objects_v2 with prefix/date filters, stream each
                                    object into the file readers."""

class KafkaClient:
    def receive(self, message):    """Parse the message value (JSON/string)."""
    def fetch(self, consumer_config):
        """Connect, subscribe, poll in a loop with backoff, commit offsets, batch-aware yield."""

class ScraperClient:
    def receive(self, html_content):  """HTML cleaner → visible text → doc with url metadata."""
    def fetch(self, scrape_config):   """Iterate URLs from config/list file, download, reuse
                                       receive()."""

class RedisClient:
    def receive(self, key_value):     """Treat the value as JSON or text."""
    def fetch(self, redis_config):    """Depending on mode (key pattern, list, stream) fetch
                                       records and convert."""
```
**Learn:** "Requests GET POST Python" · "Elasticsearch Python client docs" · "boto3 S3 list +
get object" · "KafkaConsumer basic usage" · "Redis Python client" · "BeautifulSoup text
extraction".

### 33.10 `io_adapters/storage_clients.py`

```python
class LocalStorageWriter:
    def __init__(self, config):
        self.output_dir = Path(config.get("path", "output"))
        self.output_dir.mkdir(parents=True, exist_ok=True)
    def write(self, output_obj):
        """One JSON file per doc, named by document_id."""
    def save_batch(self, documents):
        """One file per doc, OR a single newline-delimited JSON file."""

class ParquetWriter:
    def __init__(self, config):
        self.output_path = Path(config.get("path", "output/data.parquet")); self.batch = []
    def write(self, output_obj):
        self.batch.append(output_obj)
        if len(self.batch) >= 1000: self._flush()
    def _flush(self):
        """DataFrame → to_parquet with DETERMINISTIC file naming (timestamp + shard)."""
    def save_batch(self, documents): ...

class RedisWriter:
    def write(self, output_obj):   """rpush JSON string to the configured key/list/stream."""
    def save_batch(self, documents): """pipeline; e.g. mset or a batch push."""

class StorageClientFactory:
    @staticmethod
    def create(output_cfg):
        t = output_cfg.get("type", "json")
        return {"json": LocalStorageWriter, "parquet": ParquetWriter,
                "redis": RedisWriter}.get(t, LocalStorageWriter)(output_cfg)
```
**Learn:** "pandas DataFrame basics" · "pandas to_parquet / read_parquet" · "Python pathlib".

### 33.11 `nlp_pipeline/preprocessing.py`

**Libraries:** `re`, `unicodedata`, optionally `spacy`.
```python
class TextProcessor:
    def __init__(self, pipeline_cfg):
        self.lowercase        = pipeline_cfg.get("lowercase", True)
        self.remove_html      = pipeline_cfg.get("remove_html", True)
        self.use_lemmatization= pipeline_cfg.get("use_lemmatization", False)
        # pre-load regexes, stopword lists, spaCy model if lemmatizing

    def _strip_html(self, text): ...
    def _normalize_unicode(self, text): return unicodedata.normalize("NFKC", text)
    def _normalize_whitespace(self, text): """collapse multiple spaces/newlines"""
    def _lemmatize(self, text): """spaCy; return text unchanged if disabled"""

    def normalize(self, doc: InternalDocument) -> NormalizedDocument:
        text = doc.raw_text
        if self.remove_html: text = self._strip_html(text)
        text = self._normalize_unicode(text)
        if self.lowercase: text = text.lower()
        text = self._normalize_whitespace(text)
        # optional: expand common abbreviations (config-driven)
        # optional: tokenize
        if self.use_lemmatization: text = self._lemmatize(text)
        # return NormalizedDocument(full_text, tokens, token_offsets, metadata carried over)
```
**Learn:** "Regular expressions in Python" · "Unicode normalization Python" · "spaCy
lemmatization tutorial".

### 33.12 `nlp_pipeline/segmentation.py`

```python
class SentenceSegmenter:
    def __init__(self, pipeline_cfg):
        self.mode = pipeline_cfg.get("sentence_segmentation", "simple")   # simple|spacy|pysbd
        # if pysbd: self.segmenter = pysbd.Segmenter(language="en", clean=False)

    def segment(self, normalized_doc) -> List[Sentence]:
        """Produce sentences with start/end char offsets.
        Guarantee NO OVERLAP and FULL COVERAGE of the text. Attach sentence IDs."""
```
**Learn:** "Basic sentence segmentation methods" · "pysbd library usage".

### 33.13 `nlp_pipeline/features.py`

```python
class FeatureExtractor:
    def __init__(self, feature_cfg):
        self.use_ngrams = feature_cfg.get("use_ngrams", True)
        self.max_ngram  = feature_cfg.get("max_ngram", 2)
        # self.use_pos_tags = feature_cfg.get("use_pos_tags", False)

    def _tokenize(self, text) -> List[str]: ...
    def _extract_ngrams(self, tokens) -> Counter:
        """for n in range(1, max_ngram+1): slide a window, count"""

    def build_features(self, normalized_doc, sentences, metadata) -> Dict[str, Any]:
        """per sentence: token counts, n-grams, keyword flags, regex flags, POS tags,
                         lexicon-based sentiment hints
           document-level: length stats, headline features, section counts,
                           dictionary hits for bias/stance/tone lists
           return {"document": {...}, "sentences": {sent_id: {...}}}"""
```
**Learn:** "n-grams in NLP" · "feature engineering for text".

### 33.14 `nlp_pipeline/rules_engine.py`

```python
class RuleEngine:
    def __init__(self, taxonomy_cfg):
        """Parse taxonomy_v1.yaml into internal structures: rules per node, keyword lists,
        pattern lists, node priorities, mutually-exclusive groups. PRE-COMPILE the regexes."""

    def _evaluate_node_rules(self, node_id, sentence_features) -> float:
        """Return the score/weight if the rules are satisfied; apply boosts and penalties."""

    def classify(self, feature_bundle, sentences):
        """For each sentence × each taxonomy node: evaluate rule conditions against the
        sentence AND document features, accumulate score/flags.
        Build sentence_labels (node id + score + EVIDENCE) and document_labels.
        Ensure DETERMINISTIC TIE-BREAKING (sort by score, then id)."""
```
**Learn:** "Rule-based text classification" · "Regular expressions with Python" · "How to design
configs for rules".

### 33.15 `nlp_pipeline/ml_classifier.py`

```python
class MLClassifier:
    def __init__(self, ml_cfg):
        self.model_path = ml_cfg.get("model_path")
        # load sklearn (joblib) or ONNX model; cache label indices
    def _features_to_vector(self, feature_bundle) -> np.ndarray:
        """Flatten the feature dict into a numeric vector."""
    def predict(self, feature_bundle, sentences):
        """Batch sentences or the whole doc; return probabilities per node per sentence/doc."""
```
⚠ `from sklearn.externals import joblib` was removed in scikit-learn 0.23 — use `import joblib`.
**Learn:** "Scikit-learn text classification pipeline" · "ONNX Runtime Python tutorial".

### 33.16 `nlp_pipeline/hybrid_router.py`

```python
class HybridRouter:
    def __init__(self, hybrid_cfg, ontology): ...
    def merge(self, rule_result, ml_result, ontology):
        """Per sentence:
             start from the RULE labels as the baseline
             if ML enabled: confidence-boost labels where ML probability is high;
                            suppress labels where ML probability is extremely low (if config allows)
             enforce ontology constraints (no mutually-exclusive nodes together)
           Compute the final label sets for sentences and document → FinalClassification."""
```
**Learn:** "Ensemble methods: combining rule-based and ML" · "Conflict resolution in
taxonomies".

### 33.17 `nlp_pipeline/ontology_graph.py`

```python
class OntologyGraph:
    def __init__(self, taxonomy_cfg):
        self.nodes = {}      # node_id -> metadata (names, descriptions, weights)
        self.parents = {}    # node_id -> parent_id
        self.children = {}   # node_id -> [children]
    def get_ancestors(self, node_id):    """climb parents to the root"""
    def get_descendants(self, node_id):  """DFS/BFS from the node"""
    def project_labels_to_levels(self, label_set):
        """propagate fine-grained labels up to top-level categories"""
    def validate_label_set(self, label_set):
        """drop ids not in self.nodes; enforce required parents if configured"""
```
**Learn:** "Tree / graph data structures in Python" · "DFS / BFS".

### 33.18 `nlp_pipeline/scoring_engine.py`

```python
class ScoringEngine:
    def __init__(self, scoring_cfg):
        """Parse: weights per node, aggregation formulas (sum, weighted_avg, max),
        penalty rules."""
    def score(self, final_classification, feature_bundle):
        """Compute base scores per metric; aggregate sentence-level → document-level;
        apply penalties/bonuses from config (e.g. presence of extreme language);
        return a structured ScoreResult (metric → value + breakdown)."""
```
**Learn:** "Weighted scoring systems" · "How to design metrics from config".

### 33.19 `nlp_pipeline/postprocessing.py`

```python
class PostProcessor:
    def __init__(self, output_schema_path, pipeline_config, taxonomy_config, scoring_config):
        self.pipeline_version = pipeline_config["pipeline"]["name"]
        self.taxonomy_version = taxonomy_config["taxonomy"]["version"]
    def to_output_schema(self, internal_doc, normalized_doc, segments,
                         final_classification, scores, config_hashes):
        """Map sentences with offsets and assigned taxonomy nodes; attach score metrics and
        explanations; include doc id, source, timestamps, config hashes, taxonomy_version,
        pipeline_version; run JSON-schema validation before returning."""
```
**Learn:** "JSON Schema basics" · "How to validate JSON against a schema in Python".

### 33.20 `nlp_pipeline/embeddings_onnx.py`

```python
class EmbeddingGenerator:
    def __init__(self, emb_cfg):
        # self.session   = ort.InferenceSession(emb_cfg["model_path"])
        # self.tokenizer = AutoTokenizer.from_pretrained(emb_cfg["tokenizer_name"])
    def embed(self, text_or_segments) -> np.ndarray:
        """tokenize → ONNX inference → pool (e.g. CLS token) → L2-normalize → return vector(s)"""
```
**Learn:** "ONNX Runtime for NLP" · "HuggingFace transformers basic usage".

### 33.21 `nlp_pipeline/vector_index.py`

```python
class VectorIndex:
    def __init__(self, emb_cfg):
        self.dim = emb_cfg.get("dim", 384)
        # self.index = faiss.IndexFlatIP(self.dim)     # or load from disk
        self.id_to_doc = {}       # internal index id -> document_id
        self.next_id = 0
    def upsert(self, document_id, embedding, labels, scores):
        """Add the vector, record the mapping; optionally store metadata in a side store.
        (Updating an existing doc_id needs explicit handling.)"""
    def search(self, query_embedding, top_k) -> List[Tuple[str, float]]:
        """Nearest-neighbour search → [(document_id, distance/similarity, metadata)]"""
```
**Learn:** "FAISS CPU tutorial" · "Cosine similarity vs dot product".

### 33.22 `nlp_pipeline/deterministic_utils.py` — functions only

```python
def set_global_seeds(seed: int):
    random.seed(seed); np.random.seed(seed)   # torch.manual_seed(seed) …

def hash_to_document_id(input_str: str) -> str:
    return hashlib.sha256(input_str.encode("utf-8")).hexdigest()

def compute_config_hashes(pipeline_cfg, taxonomy_cfg, scoring_cfg) -> Dict[str, str]:
    """Dump each dict to CANONICAL JSON and hash it →
    {"pipeline_hash": …, "taxonomy_hash": …, "scoring_hash": …}
    These are embedded in run_metadata on every output."""
```
**Learn:** "hashlib sha256 usage" · "Reproducibility in ML pipelines".

### 33.23 `nlp_pipeline/gpu_router.py` — functions only

```python
def is_cuda_available():
    """check env var + try importing GPU libs → bool"""
def select_backend(operation_type):
    """'gpu' if available AND the operation is heavy (embeddings, similarity), else 'cpu'"""
```

### 33.24 `taxonomy_tools/*`

```python
# taxonomy_loader.py
def load_taxonomy(taxonomy_cfg) -> Dict[str, Any]:
    """Validate: unique node ids, NO CYCLES, parent/child relationships consistent.
    Raise on invalid. Single source of truth for taxonomy loading."""

# taxonomy_versioning.py
def diff_taxonomies(old, new) -> Dict[str, Any]:
    """added / removed / renamed nodes + changes of parent relationships → TaxonomyDiff"""
def plan_migration(diff) -> Dict[str, Any]:
    """Suggest how to map old labels to new ones for historical data.
    Simple example: for removed nodes, map to the parent."""

# taxonomy_suggestions.py
def suggest_new_nodes(embeddings, existing_taxonomy) -> Dict[str, Any]:
    """k-means cluster the embeddings; for clusters with low coverage in the taxonomy,
    compute representative top keywords and propose new node candidates with short labels."""
```

### 33.25 `core_accelerators/*` and `gpu_support/*`

C++ side exposes `fast_tokenize(text)`, `fast_regex_search(text, patterns)`,
`fast_ngram_generation(tokens)`; CUDA side exposes `vector_norm`, `cosine_similarity`, fast
embedding transformations. `bindings.cpp` exposes them as Python functions consumed by
`TextProcessor`, `FeatureExtractor` and `VectorIndex`. Boilerplate placeholders for now.

### 33.26 `airflow_dags/media_nlp_batch_dag.py` — orchestration only

```python
with DAG("media_nlp_batch", schedule_interval="@daily",
         start_date=datetime(2025, 1, 1), catchup=False) as dag:
    preprocess = BashOperator(task_id="preprocess",
        bash_command="python -m src.batch_processing.preprocess_spark --config conf/pipeline_v1.yaml")
    classify   = BashOperator(task_id="classify",
        bash_command="python -m src.batch_processing.classify_batch --config conf/pipeline_v1.yaml")
    preprocess >> classify
```
**Learn:** "Apache Airflow DAG basics" · "BashOperator usage".

### 33.27 `tests/*` — assert behaviour, not implementation

```python
from nlp_pipeline.preprocessing import TextProcessor
from io_adapters.shared_types import InternalDocument

def test_basic_html_removal():
    processor  = TextProcessor({"remove_html": True})
    doc        = InternalDocument("id1", "<p>Hello</p>", {})
    normalized = processor.normalize(doc)
    assert normalized.full_text == "Hello"
```
- `test_preprocessing.py` — raw text with HTML + weird spaces → normalized matches expectation
- `test_segmentation.py` — tricky punctuation → sentences split in the right places
- `test_rules_engine.py` — controlled text with known keywords → correct taxonomy nodes fire
- `test_scoring_engine.py` — synthetic classification result → score matches the YAML formula
- `test_determinism.py` — same input twice with the same configs and seeds → identical JSON
- `test_output_schema.py` — validate a sample output against `output_schema.json`

**Learn:** "pytest basics" · "Test-driven development for functions".

### 33.28 Alternate `pipeline_v1.yaml` shape used by this blueprint

```yaml
pipeline:
  name: "media_nlp_pipeline_v1"
  language: "en"
  seed: 42
  enable_ml_classifier: true
  enable_embeddings: true
  enable_vector_index: false

input:
  mode: "pull"                      # or "push"
  source_type: "files"              # files | api | es | kafka | s3 …
  file_glob: "data/raw/*.txt"
  csv:
    text_column: "content"

output:
  type: "parquet"                   # jsonl | redis | …
  path: "data/processed/"

feature_extraction:
  use_ngrams: true
  max_ngram: 3
  use_pos_tags: false

ml:
  model_path: "models/news_classifier.onnx"

embeddings:
  model_path: "models/sentence_encoder.onnx"

logging:
  level: "INFO"
```
Node-list taxonomy shape (an alternative to the nested `categories:` form in §6.2):
```yaml
taxonomy:
  version: "1.0.0"
  nodes:
    - id: "politics"
      label: "Politics"
      parent: null
      rules:
        any_keywords: ["election", "parliament", "policy"]
    - id: "economy"
      label: "Economy"
      parent: null
      rules:
        any_keywords: ["gdp", "inflation", "unemployment"]
    - id: "economy.inflation"
      label: "Inflation"
      parent: "economy"
      rules:
        any_keywords: ["inflation", "cpi"]
        threshold: 2
```
Metric-oriented scoring shape (an alternative to §6.3):
```yaml
scoring:
  metrics:
    objectivity_score:
      base_weight: 1.0
      category_weights:
        "politics": -0.1
        "economy.inflation": -0.2
      formula: "1.0 + sum(category_weight * hit_count)"
    bias_score:
      base_weight: 0.0
      lexicon_penalties:
        "strong_bias_words": -0.3
```

---

## 34. Reader raw-record contracts

Each reader returns a **rich dict** (the "raw ingestion record"), not an `InternalDocument`.
Understanding these fields matters because `InputRouter._extract_text()` and
`_to_internal_document()` read them by name.

**Common `BaseReader` behaviour** — every record starts with `get_base_metadata()`:

```python
{
  'file_path', 'file_name', 'file_size_bytes', 'file_extension',
  'mime_type',                      # python-magic
  'file_hash_sha256',               # streamed in 4096-byte blocks
  'created_timestamp', 'modified_timestamp', 'processed_timestamp',
  'reader_class'                    # self.__class__.__name__
}
```
Plus the shared machinery:
- `detect_encoding()` — `charset_normalizer` on the first 100 KB, falling back through
  `utf-8 → latin-1 → cp1252 → iso-8859-1`, defaulting to `utf-8`.
- `calculate_hash()` — SHA-256, block-streamed so large files don't load into memory.
- `write_to_jsonl()` — append one JSON line, `ensure_ascii=False`.
- `read()` — abstract; every subclass implements it.
- `process_and_save()` — wraps `read()` in try/except; on failure writes
  `{file_path, error, timestamp, reader_class}` to **`errors.jsonl`** and returns `False`
  instead of crashing the batch.
- `_extract_strings_only()` — recursively keeps only string values while preserving structure
  (drops ints, floats, bools, nulls). Used by the JSON readers.

**Per-reader extra fields**

| Reader | Fields emitted beyond base metadata |
|---|---|
| `TxtReader` | `encoding_detected`, `raw_content`, `raw_lines`, `line_count`, `char_count`, `byte_count`, `empty_lines`, `max_line_length`, `contains_null_bytes`, `contains_bom`, `line_endings` (CRLF/LF/CR detection), `whitespace_stats {spaces, tabs, newlines}` |
| `MarkdownReader` | `raw_markdown`, `rendered_html`, `plain_text`, `structure {headings[{level,text}], heading_count, code_blocks[{language,content}], code_block_count, links[{text,url}], link_count, list_count, table_count}`, `markdown_features {has_frontmatter, has_code_fence, has_inline_code, has_blockquote, has_images}` |
| `PDFReader` | `pdf_metadata`, `page_count`, `pages[{page_number,width,height,rotation,text_length,has_text,table_count}]`, `raw_text_by_page`, **`full_raw_text`**, `tables[{page,data}]`, `table_count`, `images`, `image_count`, `text_statistics {total_chars,total_words,total_lines,avg_chars_per_page}`, `quality_indicators {needs_ocr, is_scanned, has_tables, has_images, is_empty}`, `extraction_method` |
| `DocsReader` | `document_properties {title,author,subject,keywords,created,modified,revision}`, `paragraphs[{text,style,alignment,is_heading,runs}]`, `paragraph_count`, **`full_raw_text`**, `headings`, `heading_count`, `tables[{table_index,rows,cols,data}]`, `table_count`, `sections`, `text_statistics`, `style_distribution` |
| `CSVReader` | `encoding_detected`, `delimiter` (via `csv.Sniffer`), `row_count`, `column_count`, `columns`, `columns_info[{name,dtype,null_count,unique_count,sample_values}]`, `data_types`, `raw_data` (all records), `sample_data` (first 10), `statistics {total_cells,null_cells,memory_usage_bytes}`, `data_quality {has_null_values,has_duplicates,duplicate_count}` |
| `JSONReader` | `raw_json_string`, parsed data, and a **string-only** projection via `_extract_strings_only` |

**PDF specifics worth keeping**: pdfplumber is the primary extractor, **PyMuPDF (fitz) the
fallback when the joined text is empty**; OCR need is inferred heuristically —
`needs_ocr = len(full_text.strip()) < len(page_data) * 50` (suspiciously little text for the
page count) which also sets `is_scanned`.

**DOCX specifics**: only `.docx` is supported directly; `.doc` returns
`{'error': 'Only .docx format supported. Convert .doc to .docx first.', 'supported_format': False}`.

**CSV specifics**: pandas is the primary parser with a **fallback to the stdlib `csv` reader**
that returns `raw_data` as rows plus `{'error': 'Pandas parsing failed: …'}`.

---

## 35. InputRouter — production implementation details

### 35.1 Exception hierarchy (`core/exceptions.py`)

```python
class IngestionError(Exception):            """Base exception for ingestion errors"""
class UnsupportedFileTypeError(IngestionError):  """File type is not supported"""
class NoTextFoundError(IngestionError):     """No text content could be extracted"""
class InvalidInputError(IngestionError):    """Input format is invalid"""
class SourceConnectionError(IngestionError):"""Cannot connect to source"""
class ExtractionError(IngestionError):      """Content extraction failed"""
```

### 35.2 `InternalDocument` — computed fields and serialization

```python
def __post_init__(self):
    """Auto-calculate statistics if not provided."""
    if self.text:
        if self.char_count == 0: self.char_count = len(self.text)
        if self.word_count == 0: self.word_count = len(self.text.split())
        if self.line_count == 0: self.line_count = len(self.text.split('\n'))

def to_dict(self):   # asdict() + enum .value for source_type and processing_status
def to_json(self):   # json.dumps(..., ensure_ascii=False, indent=2)
def to_jsonl(self):  # json.dumps(..., ensure_ascii=False)   — single line
@classmethod
def from_dict(cls, data):  # re-hydrate the two enums, then cls(**data)
```

### 35.3 The full extension → reader registry

```python
'.txt', '.text'                 → TxtReader
'.md', '.markdown'              → MarkdownReader
'.pdf'                          → PDFReader
'.docx', '.doc'                 → DocsReader
'.csv', '.tsv'                  → CSVReader
'.json'                         → JSONReader
'.jsonl', '.ndjson'             → JSONLReader
'.html', '.htm'                 → HTMLReader
'.xml'                          → XMLReader
'.parquet'                      → ParquetReader
'.png', '.jpg', '.jpeg', '.tiff', '.bmp'  → ImageReader     (OCR)
'.zip', '.tar', '.gz', '.tgz'   → ArchiveReader
```
Source clients: `api → APIClient`, `elasticsearch → ESClient`, `kafka → KafkaClient`,
`s3 → S3Client`, `scraper → ScraperClient`, `sql → SQLClient`, `mongodb → MongoClient`.

> ⚠ **This registry is the source of the known bug**: in the committed code the values are
> *strings* (`'TxtReader()'`) rather than instantiated objects, and `_handle_file_path()` calls
> `self._mock_file_read(...)` instead of the real reader. Instantiate in the constructor and
> delete the mock. (Appendix A, item 1.)

### 35.4 The push-mode signature

```python
def route_push_input(self,
                     file_path: Optional[str] = None,
                     file_bytes: Optional[bytes] = None,
                     api_payload: Optional[Dict] = None,
                     es_hit: Optional[Dict] = None,
                     kafka_message: Optional[Dict] = None,
                     raw_text: Optional[str] = None) -> InternalDocument:
    """Exactly one argument is expected; dispatch in order and raise
    InvalidInputError('No valid input provided') if none was supplied.
    Wrap everything: on exception log with exc_info and re-raise as IngestionError."""
```
Handlers: `_handle_file_path`, `_handle_file_bytes`, `_handle_api_payload`, `_handle_es_hit`,
`_handle_kafka_message`, `_handle_raw_text`.

- `_handle_file_path` — check existence (`FileNotFoundError`), take the lowercase suffix, special-
  case `.tar.gz` (reader key `.tar`), raise `UnsupportedFileTypeError` for unknown extensions,
  then read and normalize.
- `_handle_file_bytes` — write to a `tempfile.NamedTemporaryFile` preserving the suffix, delegate
  to `_handle_file_path`, and **unlink the temp file in a `finally` block**.
- `_handle_raw_text` — build the document directly with
  `source_metadata={'input_method': 'raw_text'}`.
- `_handle_api_payload` — `document_id = payload.get('id') or generated`;
  `source_type = API_REST`; carries `title` and `author` from the payload; the whole payload
  becomes `source_metadata`.
- `_handle_es_hit` — reads `hit['_source']`; `document_id = hit['_id']` (or generated);
  `source_metadata = {index, score, source}`.
- `_handle_kafka_message` — reads `message['value']`; `source_metadata =
  {topic, partition, offset, timestamp, value}`.

### 35.5 Pull mode with per-record error isolation

```python
def route_pull_source(self, source_type: str,
                      source_config: Optional[Dict] = None) -> Iterator[InternalDocument]:
    source_config = source_config or self.config.get('sources', {}).get(source_type, {})
    if source_type not in self.ingest_clients:
        raise IngestionError(f"Unsupported source type: {source_type}")
    client = self.ingest_clients[source_type]
    for raw_record in self._fetch_from_source(client, source_config):
        try:
            yield self._to_internal_document(raw_record, source_type)
        except Exception as e:
            self.logger.error(f"Failed to process record: {e}")
            self._log_error(raw_record, e)      # log and CONTINUE — one bad record
            continue                            # must not kill the batch
    # a connection-level failure raises SourceConnectionError
```

### 35.6 `_to_internal_document` — the critical normalization method

```python
def _to_internal_document(self, raw_record, source_hint) -> InternalDocument:
    text = self._extract_text(raw_record)
    doc_id = (raw_record.get('file_hash_sha256')
              or raw_record.get('document_id')
              or self._generate_document_id(text))
    source_type = self._determine_source_type(raw_record, source_hint)
    language = raw_record.get('language')
    title    = raw_record.get('title')  or raw_record.get('file_name')
    author   = raw_record.get('author') or raw_record.get('document_properties', {}).get('author')
    tables   = raw_record.get('tables',   [])
    images   = raw_record.get('images',   [])
    sections = raw_record.get('sections', [])
    quality_flags = raw_record.get('quality_indicators', {})
    return InternalDocument(
        document_id=doc_id, text=text, source_type=source_type,
        ingestion_timestamp=raw_record.get('processed_timestamp') or datetime.now().isoformat(),
        source_metadata=raw_record,                 # the ENTIRE rich record is retained
        language=language, title=title, author=author,
        tables=tables, images=images, sections=sections,
        quality_flags=quality_flags,
        processing_status=ProcessingStatus.INGESTED)
```

### 35.7 Text-extraction fallback order (authoritative)

```
1. full_raw_text     (PDF, DOCX)
2. extracted_text    (HTML, XML)
3. raw_content       (TXT)
4. text              (generic)
5. content
6. body
7. otherwise: concatenate from the structured data
→ if nothing yields text: raise NoTextFoundError()
```

---

## 36. Config-driven multi-source ingestion

The question that drove this design: *"If there is an API, does every API have the same format?
And ES clients? If Airflow pulls from APIs, ES, Redis or Parquet — how, since every API is
written differently?"*

**Answer: no, they are all different — which is exactly why you never hardcode them.** You do
not write a new class per API. You write **one generic client per source *type*** and drive it
with **one config entry per source *instance***.

What a per-source config must specify:

| Source type | Config fields |
|---|---|
| API | `base_url`, auth type, endpoint path, query params, **which JSON field contains the text** |
| Elasticsearch | `host`, `index`, query template, **which field is the article body** |
| Redis | `host`, `db`, key pattern (e.g. `news:*`), value format (`plain_text` or `json.text`) |
| Parquet | file path / S3 URI, **column name containing the text**, optional filters |

So: one generic API client class serves many APIs · one ES client serves many indices · one
Redis client serves many logical caches · one Parquet reader/writer serves many datasets.
**You don't change code for a new source; you add a config entry.**

A `SourceConfig` registry (in `conf/pipeline_v1.yaml` or its own file) holds named entries:

```
nytimes_api    → type: api,     base_url: …,  text_field: response.body
guardian_es    → type: es,      host: …,      index: articles, text_field: content
redis_news     → type: redis,   host: …,      key_pattern: news:*
parquet_daily  → type: parquet, path: s3://…/daily.parquet, text_column: body
```

The generic ingestion layer then: reads the source type from the config → routes to the correct
client (`IngestAPIClient`, `ESClient`, `RedisCache`, `ParquetReader`) → normalizes everything to
the internal document schema → sends documents into the pipeline.

**Where Airflow fits:** Airflow is about orchestration and scheduling, not formats. Each Airflow
task is simply *"run this adapter with this config"* — it passes a **source id / config name**:

- Task A → "Ingest from `nytimes_api` today"
- Task B → "Ingest from `guardian_es` for the last 24h"
- Task C → "Backfill from `parquet_daily` for last month"

Airflow does not care about URL formats, ES schemas or Redis key patterns. All those tasks flow
through the same ingestion layer with different configs.

**What to actually do first** (explicit advice, to avoid overbuilding): pick **ONE** source type
(local files, or one API), design a simple config entry for it, make the ingestion layer read
that config and return text in the internal schema, and **ignore ES, Redis and Parquet until the
pipeline works end-to-end on that one source.** Then add sources by adding config and extending
adapters slowly. *"That's how big companies do it."*

The agreed linear order once ingestion resumed: **ES client → API client → the remaining IO
adapters → preprocessing.**

---

## 37. Elasticsearch vector search — capability boundaries

Follow-on to §23.5, answering *"can my ESClient create a vector search index like FAISS?"*

**FAISS** is a *library* — your Python code can create an index, add/search/update/delete
vectors and store them locally, entirely in-process.

**Elasticsearch** is a *distributed search server*; vector search happens inside it, after the
index already exists.

| ESClient **CAN** | ESClient **CANNOT** |
|---|---|
| Create a vector-enabled index | Create an ES cluster |
| Define mappings with `dense_vector` fields | Create ES nodes |
| Update index settings (e.g. HNSW parameters) | Create Elasticsearch itself |
| Insert documents with embeddings | Deploy the ES server |
| Run vector (kNN / ANN) search queries | Manage OS-level cluster resources |
| Run `script_score` vector search | Replace FAISS |
| Combine vector + keyword search (hybrid ranking) | |
| Perform hybrid ranking and scroll vector-enabled queries | |
| Monitor index health | |

This is **application-level control, not cluster-level** — precisely what the Elasticsearch REST
API exposes. Cluster creation belongs to Docker Compose, Kubernetes, Elastic Cloud or DevOps
scripts.

Mapping and document shape:
```json
"embeddings": { "type": "dense_vector", "dims": 384 }
```
```json
{ "title": "...", "body": "...", "embedding": [0.12, 0.88, ...] }
```

**Layer separation:** the ES *cluster* is infrastructure (managed by Docker/Kubernetes/Cloud, and
it exists before your ESClient ever runs); the *ESClient* is application code that fetches
documents and returns internal documents. They are completely separate layers.

**Both can coexist**, and many real systems use both: `vector_index.py` (FAISS) for local fast
semantic search — fully controlled by your Python code, works offline, you create/save/load/
rebuild the index — and `es_client.py` for distributed semantic search, where ES handles
sharding, memory and indexing. Use cases unlocked: hybrid search (keyword + embeddings),
queries like *"biased articles about climate change"*, question-answering systems, loading raw
data from ES, and searching processed data.

---

## 38. The employer-facing pipeline summary (v2.0)

Written deliberately in the style used by FAANG/Bloomberg/OpenAI/DeepMind/Meta AI/HuggingFace
proposals — intended to be copy-pasted into a job proposal, portfolio or technical document.

> **MEDIA-NLP PIPELINE v2.0 — Enterprise-Grade Architecture**
> *A deterministic, scalable, hybrid rule+ML pipeline for large-scale document classification,
> scoring and ontology mapping.*

**Pipeline goals** — process millions of unstructured documents delivering: deterministic,
auditable classification (taxonomy-driven, rule-based, ML-enhanced, transparent logic) ·
scalable ingestion (Kafka streams, APIs, S3, PDF, DOCX, HTML, TXT, CSV, JSON) · high performance
(ONNX embeddings with optional GPU, FAISS vector index, Spark/Ray distributed preprocessing) ·
flexible serving (Airflow batch, FastAPI REST, Kafka streaming, file-based) · extensibility
(**add taxonomy nodes, scoring rules and embedding models with zero code changes**) ·
reproducibility (config-based orchestration, deterministic hashing, seed control, schema
validation).

```
┌───────────────────────────────────────────┐
│              Ingestion Layer              │
│   (Files | APIs | S3 | Kafka | ES | URLs) │
└──────────────────┬────────────────────────┘
                   ↓  src/io_adapters/InputRouter
┌───────────────────────────────────────────┐
│            Preprocessing Layer            │
│   Cleaning → Normalization → Unicode fix  │
└──────────────────┬────────────────────────┘
                   ↓  Sentence Segmentation Layer
┌───────────────────────────────────────────┐
│               Feature Layer               │
│   N-grams | Keyword hits | Regex flags    │
│   POS (optional) | Lexicon features       │
└──────────────────┬────────────────────────┘
                   ↓
┌──────────────────────────────────────────────────┐
│         Hybrid Taxonomy Classification           │
│   Deterministic Rules + ML classifier            │
│   + Ontology Graph consistency                   │
└──────────────────┬───────────────────────────────┘
                   ↓  Scoring Engine (scoring_v1.yaml)
                      • Objectivity Score • Bias Score • Intensity Index
┌──────────────────────────────────────────────────┐
│      Embedding + Vector Index (optional)         │
│   ONNX (MiniLM / BERT) + FAISS for similarity    │
└──────────────────┬───────────────────────────────┘
                   ↓  Postprocessing → output_schema.json
┌────────────────────────────────────────────────────────────┐
│                       Output Layer                         │
│  Parquet | JSON | Redis | Elasticsearch | FastAPI response │
└────────────────────────────────────────────────────────────┘
```

**Six reasons this beats most candidate submissions:** (1) deterministic **and** ML hybrid —
most candidates do only one, this proposes hybrid + ontology enforcement; (2) configuration-
driven via taxonomy/scoring/pipeline YAML; (3) distributed-ready with Spark + Ray + Airflow
built in; (4) scalable embeddings via ONNX + FAISS showing production-level thinking; (5)
plug-and-play ingestion through the InputRouter; (6) auditable outputs via config hashes +
deterministic utilities.

Design references cited: Google Dataflow, LinkedIn Kafka pipelines, Bloomberg news
classification, Meta semantic indexing.

**Recruiter/CV version:**

> I designed and implemented a fully modular, scalable NLP pipeline that supports multi-source
> ingestion (files, APIs, Kafka, S3), deterministic preprocessing, hybrid classification
> (rules + ML), ontology-aware taxonomy mapping, and configurable scoring. The system uses ONNX
> acceleration, FAISS vector indexing, Airflow orchestration, Spark/Ray for distributed
> preprocessing, and FastAPI for real-time serving. All components are config-driven using YAML
> schemas, ensuring reproducibility and enabling non-engineers to evolve taxonomy and scoring
> logic without touching code. Outputs are validated with JSON schemas, stored in
> Parquet/JSON/Redis/ES depending on mode, and are fully versioned through configuration hashing
> and deterministic utilities.

One more line worth reusing verbatim in interviews, about the ingestion contract:

> "Ingestion is fully decoupled from processing through a normalized `InternalDocument`
> contract, so NLP, ML, and scoring remain deterministic and isolated."

---

## 39. IO adapter design — the evolution and the rejected alternatives

The IO layer went through four design iterations. Keeping the rejected ones matters, because the
final design only makes sense as an answer to their specific failures.

### 39.1 Iteration 1 — one file per format (REJECTED)

The first proposal was eleven separate loader modules:

```
file_loader.py · pdf_loader.py · docx_loader.py · ppt_loader.py · csv_loader.py
json_loader.py · text_loader.py · web_scraper.py · s3_loader.py · api_ingest.py
kafka_consumer.py
```
Each with a single responsibility (e.g. `pdf_loader.py` — open the PDF, extract text with
PyPDF2/pdfminer, return a raw string; `csv_loader.py` — read CSV, extract the target column;
`web_scraper.py` — Requests + BeautifulSoup, strip HTML, extract article text).

**Rejected** on the user's own instinct — *"rather divide it into small segments of loading so
that you don't have a cluster of files… rather create a class in a file to extract everything"* —
which was confirmed as the correct senior-engineer intuition:

> "Don't create 10 separate files for every input format. Instead, have ONE high-level loader
> with small helper classes."

Grouping rule that replaced it: **1 file → Router · 1 file → all file readers · 1 file → all
ingestion clients · 1 file → storage writers.** Clean, scalable, testable — "the sweet spot".
Putting *all* code in one file is equally wrong (messy, unmaintainable).

### 39.2 Iteration 2 — a single `universal_loader.py` (SUPERSEDED)

For a while the design called for one master file — `src/io_adapters/universal_loader.py` (or
`file_loader.py`) — as the *only* place where PDF/Word/PPT/text/CSV/JSON/system-file reading
happened, detecting the file type, routing to the correct reader, extracting and returning the
final raw text.

Superseded by the `file_readers.py` (BaseReader + per-format reader classes) +
`ingest_clients.py` split once it became clear that *file-like inputs* and *external source
systems* are different concerns (§7.6).

### 39.3 Iteration 3 — separate Receiver and Fetcher classes (FOLDED INTO ONE CLASS)

The pivotal clarification from the user:

> "There are two ways to get an input. First, someone provides us the input. Second, we pull the
> input… for the ES client I should have two separate codes: one takes the given input and
> converts it to text, the second converts into the input format."

This first produced two *parallel class families*:

| Push — "Receiver Adapters" | Pull — "Fetcher Adapters" |
|---|---|
| `APIReceiver` — FastAPI receives input | `ESClient` / `ESClientFetcher` |
| `FileReceiver` — a file is uploaded | `APIClient` / `APIFetcher` (pull API) |
| `KafkaReceiver` — Kafka pushes a message | `S3Loader` / `FileFetcher` |
| `JSONReceiver` — backend POSTs JSON | `Scraper` / `ScraperFetcher` |
| `ESDocumentParser` — parses an ES doc handed to you, **no connection needed** | `KafkaConsumer` / `KafkaFetcher` (poll mode) |

Worked example of the distinction, for ES:
- **Case 1 (push)** — a backend hands you
  `{"_id": "123", "_source": {"title": …, "body": …, "published_at": …}}`. You don't call ES,
  you don't fetch — you simply convert the ES doc into an internal document.
- **Case 2 (pull)** — you decide *"give me all docs from news_index with query X"*: connect,
  run the query, scroll the results, convert each hit.

**Final resolution:** rather than two class families, **each adapter carries both modes as two
methods on one class** — `receive()` for push and `fetch()` for pull (§7.5). Same architecture,
half the classes.

### 39.4 Iteration 4 — the final naming (AUTHORITATIVE)

```
src/io_adapters/
  input_router.py     → class InputRouter                      # the brain; never extracts text itself
  file_readers.py     → PDFReader · DocxReader · PPTReader · TextReader ·
                        CSVReader · JSONFileReader             # local files only
  ingest_clients.py   → ESClient · APIClient · S3Client ·
                        KafkaClient · ScraperClient · RedisClient   # external systems
  storage_clients.py  → ParquetWriter · RedisWriter · LocalStorageWriter
```
Answering the original question directly: **yes, create classes for the IO adapters; no, not one
class per file type — group them logically.** The "universal adapter" *is* the `InputRouter`;
each reader/client is a small class with one job; API and ES inputs vary, so they are driven by
config; Airflow uses the router by passing a **source id**; all of them produce the same internal
document shape.

### 39.5 What adapters return — the contract that changed

An early rule stated that **all IO adapters must return a plain Python string — not JSON, not a
file.** The internal document schema of that era was:

```
id · source (e.g. "es_news") · title (optional) · raw_text (what goes into NLP) ·
published_at (datetime or None) · metadata (dict: url, tags, author, …)
```

> ⚠ **This is superseded.** The final contract is: **readers return a rich raw-record dict**
> (§34), and **only `InputRouter._to_internal_document()` produces an `InternalDocument`** (§35).
> A reader that directly constructs an `InternalDocument` is an architecture error (§41).

---

## 40. Deep IO adapter pseudocode

Language-agnostic, translatable directly into Python. Every class returns an `InternalDocument`
(in the final design, via the router).

### 40.1 `InputRouter`

```
class InputRouter:
    method load_config(config_path):
        load YAML file into memory; store in self.config

    method route_input(input_obj):                # PUSH — data handed to us
        if input_obj is file bytes:               detect type → FileReader.receive()
        if input_obj looks like an ES document:   ESClient.receive(input_obj)
        if input_obj contains a "url" field:      ScraperClient.receive(input_obj)
        if input_obj is a JSON/API payload:       APIClient.receive(input_obj)
        if input_obj is a Kafka message:          KafkaClient.receive(input_obj)
        if input_obj is a Redis message:          RedisClient.receive(input_obj)
        raise "Unsupported push input"

    method route_source():                        # PULL — we fetch
        mode = config.input.mode                  # pull | push
        type = config.input.source_type           # es | api | s3 | kafka | web | redis | file
        if mode != "pull": raise "route_source called in push mode!"
        if type == "es":     return ESClient().fetch(config.input.es)
        if type == "api":    return APIClient().fetch(config.input.api)
        if type == "s3":     return S3Client().fetch(config.input.s3)
        if type == "kafka":  return KafkaClient().fetch(config.input.kafka)
        if type == "web":    return ScraperClient().fetch(config.input.web)
        if type == "redis":  return RedisClient().fetch(config.input.redis)
        if type == "file":   return FileReaders.fetch_folder(config.input.file)
        raise "Unknown source type"
```

### 40.2 Common template for every file reader

```
class <ReaderName>:
    method receive(file_bytes):
        validate file bytes
        extract text using the appropriate library
        build InternalDocument with raw_text = extracted text,
                                   source_type = file,
                                   metadata = {file_type, size}
        return document

    method fetch(file_path):
        if file_path does not exist: raise error
        read file from disk
        return self.receive(file_bytes)          # fetch always delegates to receive
```
Per-reader specifics:
```
PDFReader.receive:   try text = extract_pdf_text(bytes) except → log error, text = ""
                     metadata = {file_type: "pdf", page_count: count_pages(bytes)}
DocxReader.receive:  parse_docx → merge all paragraphs into one string
                     metadata = {paragraphs: count(paragraphs)}
PPTReader.receive:   parse_ppt → concatenate the text of each slide
                     metadata = {slide_count: count(slides)}
CSVReader.receive:   parse CSV → detect the best column OR use config →
                     join all rows from that column;  metadata = {row_count}
                     (fetch returns a LIST of InternalDocument — one per row)
JSONFileReader.receive: parse JSON → extract "text" | "body" | the config-defined field
                     metadata = keys of the json object
TextReader.receive:  decode text
```

### 40.3 Ingest clients

```
class ESClient:
    method receive(hit):
        text = hit._source.get("body") OR hit._source.get("content")
        doc_id = hit._id
        metadata = {index: hit._index, score: hit._score}
        return InternalDocument(doc_id, text, "es", metadata)

    method fetch(es_config):
        connection = connect_to_es(es_config.hosts)
        scroll = connection.search(index=es_config.index, query=es_config.query,
                                   scroll="2m", size=es_config.batch_size)
        loop until scroll empty:
            for hit in scroll.hits: results.append(self.receive(hit))
            scroll = connection.scroll(scroll_id)
        return results

class APIClient:
    method receive(json_payload):
        text = payload.get("text") OR payload.get("content")
        return InternalDocument(payload.get("id"), text, "api", payload)
    method fetch(api_config):
        response = http_request(api_config.endpoint, api_config.params)
        for item in response["articles"] OR response["data"]: documents.append(receive(item))
        return documents

class S3Client:
    method receive(s3_event):
        bucket, key = s3_event.bucket, s3_event.key
        file_bytes = s3_download(bucket, key)
        return FileRouter.choose_reader(key).receive(file_bytes)
    method fetch(s3_config):
        for obj in list_objects(bucket=s3_config.bucket, prefix=s3_config.prefix):
            reader = choose_reader_by_extension(obj.key)
            documents.append(reader.receive(download(obj)))
        return documents

class KafkaClient:
    method receive(message):
        decoded = decode_kafka_message(message)
        return InternalDocument(decoded.get("id") or generate_uuid(),
                                decoded.get("text"), "kafka", decoded)
    method fetch(kafka_config):
        consumer = connect_to_kafka(kafka_config)
        loop for N batches or until timeout:
            for msg in consumer.poll(): documents.append(self.receive(msg))
        return documents

class ScraperClient:
    method receive(html_content):
        text = strip_html(html_content);  metadata = {length: len(text)}
        return InternalDocument(random_id, text, "html", metadata)
    method fetch(scrape_config):
        return InternalDocument(scrape_config.url, strip_html(http_get(scrape_config.url)),
                                "web", {})

class RedisClient:
    method receive(message):
        return InternalDocument(message.id or generate_uuid(), message.value, "redis", {})
    method fetch(redis_config):
        for key in connect_redis(redis_config).scan(pattern=redis_config.key_pattern):
            documents.append(self.receive({id: key, value: connection.get(key)}))
        return documents
```

### 40.4 Storage writers (one direction only — no receive/fetch)

```
class ParquetWriter:
    write(document):        convert to a row; append to a Parquet file
    save_batch(documents):  convert the list to a table; write a PARTITIONED Parquet dataset

class RedisWriter:
    write(document):        store document.raw_text under a Redis key
    save_batch(documents):  push all documents into a Redis list or stream

class LocalStorageWriter:
    write(document):        serialize as JSON, save to disk
    save_batch(documents):  save each document as an individual JSON file in a folder
```

### 40.5 Config distribution rule

**IO adapters NEVER load config directly. `InputRouter` loads the config once and distributes
the relevant slice to each adapter.**

```yaml
input:
  source_type: es
  mode: pull
  es:
    hosts: ["http://localhost:9200"]
    index: "news"
```
→ the router picks `ESClient` and calls `ESClient.fetch(config["input"]["es"])`. Likewise
`APIClient` receives `{endpoint, headers, params}` and `S3Client` receives `{bucket, prefix}`.

Why it matters: when the company changes the Elasticsearch index name, the S3 bucket, the API
endpoint, the embedding model or the scoring version — **you don't change code, you edit YAML in
`/conf`.**

### 40.6 Per-source ES config block (field-level)

```
id: es_news
type: es
host: <URL of ES>
index: news_articles
query_template:  # e.g. "all docs from last 24h", or a basic match_all
text_field: body
title_field: title
id_field: _id            # or article_id
published_field: published_at
batch_size: 500
scroll_timeout: "2m"
```
The ES client's responsibilities, in order: (1) initialize with a `source_config` block;
(2) connect to the ES host; (3) run the query per `query_template`, optionally with a time
window; (4) paginate/scroll to fetch all results in batches; (5) per hit, read id/title/text/
published_at **using the field names from config**; (6) yield internal documents as a generator.
From the outside it reads as: *"give me all documents from ES source `es_news` between T1 and T2,
as internal docs."*

Its job **ends** at "return internal doc objects" — nothing about preprocessing, segmentation or
embeddings. Adding a second index later means adding another config block, not changing code.

### 40.7 Adapter difficulty ranking with time estimate

Easiest → hardest, with the recommendation to start at the top:

1. **Local file readers** ★☆☆☆☆ — input is bytes or a path, output is text; no network, no
   external system; clean, predictable, easy to test. Order: TextReader → JSONFileReader →
   CSVReader → DocxReader → PDFReader → PPTReader. They need no config beyond a file path,
   a column selection (CSV) and a field selection (JSON). **All the file readers can be finished
   in 1–2 hours.**
2. **LocalStorageWriter** ★☆☆☆☆ — `write(document)` saves JSON into `/output/`. Trivial.
3. **ParquetWriter** ★★☆☆☆ — text → DataFrame → Parquet via pyarrow/pandas. Just file
   serialization; no API, no network.
4. Then ScraperClient and APIClient (★★), then ESClient (★★★), RedisClient and S3Client (★★★★),
   and finally KafkaClient (★★★★★) — see §7.7.

---

## 41. Boundary rules and the architecture audit

### 41.1 The file-placement authority table

| Component | File | Purpose |
|---|---|---|
| `InternalDocument`, `SourceType`, `ProcessingStatus` | `src/core/internal_document.py` | The single contract for NLP |
| All exceptions | `src/core/exceptions.py` | Central error handling (cross-cutting) |
| File readers | `src/io_adapters/file_readers.py` | Extract raw content |
| API / ES / Kafka clients | `src/io_adapters/ingest_clients.py` | Pull external data |
| Input routing | `src/io_adapters/input_router.py` | Normalize inputs |
| CLI / demo / usage examples | `src/main.py` | How the system is used |
| NLP logic | `src/nlp_pipeline/*` | Pure processing |
| Storage | `src/io_adapters/storage_clients.py` | Save outputs |

Why `core/`: the contract must be importable everywhere and **must not depend on IO adapters**;
exceptions are cross-cutting, used by IO adapters, the pipeline and the API layer.

`input_router.py` keeps only `InputRouter`, the routing logic, `_to_internal_document`,
`_extract_text` and `_determine_source_type` — with imports shaped like:
```python
from core.internal_document import InternalDocument, SourceType, ProcessingStatus
from core.exceptions import *
from io_adapters.file_readers import *
from io_adapters.ingest_clients import *
```

### 41.2 The four "do NOT"s

- ❌ Do **not** let NLP code read PDFs.
- ❌ Do **not** let readers return `InternalDocument`.
- ❌ Do **not** let API clients touch NLP.
- ❌ Do **not** put ingestion logic inside Airflow DAGs — Airflow only calls `main.py` or the
  batch scripts.

### 41.3 The architecture audit checklist

**1. Core layer — the most commonly missed.** `src/core/` must contain `__init__.py`,
`internal_document.py` (with `InternalDocument`, `SourceType`, `ProcessingStatus`) and
`exceptions.py` — and `exceptions.py` must **not** live inside `io_adapters`. Common mistakes:
keeping `InternalDocument` inside `input_router.py`; scattering exceptions across files. A
missing file here is a real architectural gap.

**2. IO adapters — structure, not implementation.**
- `input_router.py` must import `InternalDocument` from core, import the readers and clients,
  and contain **no NLP logic and no demo/`main()` code**. Example prints still present → ❌
- `file_readers.py` must contain `BaseReader`, and readers must return **raw record dicts, not
  `InternalDocument`**. A reader constructing an `InternalDocument` directly → ❌
- `ingest_clients.py` must contain *clients, not processors* — ES/API/Kafka clients only fetch
  raw data, with **no normalization**. Any text cleaning, segmentation or embeddings here → ❌
- `storage_clients.py` must only accept `InternalDocument` or `.to_dict()`; no ingestion logic,
  no NLP logic.

**3. NLP pipeline — pure, clean, isolated.** `preprocessing.py` must accept an
`InternalDocument` and output a modified one; it must **not read files** and must not touch IO
adapters. If it takes a file path → ❌. Embeddings and vector index must be stateless or
cache-controlled and must never read from disk directly.

**4. Entry point.** `src/main.py` must exist and import `InputRouter`; it is where CLI usage,
directory processing, batch execution and the Airflow call target live. If an Airflow DAG
imports `input_router` directly instead of `main.py` → ❌

**5. Airflow — correct role.** The DAG calls a script (CLI or `PythonOperator`); it contains no
NLP logic and parses no documents.

**6. Config files — very often underused.** `pipeline_v1.yaml` defines the enabled stages, batch
sizes and source toggles; `taxonomy_v1.yaml` contains **no code logic**; `scoring_v1.yaml`
contains **no Python expressions**. Scoring math hardcoded in Python → ❌

**7. Tests — minimum expectation.** All six test files exist; tests import `InternalDocument`;
tests **do not depend on files or the network**. If a test requires a PDF or an API → ❌

**8. Acceptable to be missing now, but professional to have:** `src/core/config_loader.py`,
`src/utils/logging.py`, a `Makefile` or `scripts/run_batch.sh`, `.env.example`. Employers like
seeing the placeholders.

### 41.4 The five-question verdict test

Answer yes/no. **If all five are YES, the structure is enterprise-correct:**

1. Can I replace file ingestion with Kafka **without touching NLP code**?
2. Can I replace Elasticsearch with S3 **without touching NLP code**?
3. Does every document become an `InternalDocument` **before** NLP?
4. Is Airflow **only** orchestration?
5. Can I unit-test preprocessing **without files**?

### 41.5 The preprocessing input contract (settled definitively)

> **`preprocessing.py` NEVER takes JSON. NEVER reads files. NEVER loads PDFs.**

Preprocessing is not responsible for input formats and not responsible for reading anything — not
PDFs, Word documents, websites, JSON, files, API requests or storage. It receives **a string**.

| Path | How the string arrives |
|---|---|
| API | FastAPI receives `{"text": "Some article text…"}` → extracts `"text"` → string → preprocessing |
| Batch (Airflow / Spark / local) | Input is Parquet with a `text` column; Spark reads the Parquet, and for each row `row.text` → string → preprocessing |

```
User/Source → IO Adapter → text (string) → Preprocess → Segment → Embed → Classify → Score → Output
```
IO adapters send a string; preprocessing receives a string; preprocessing returns a string.
The conceptual flow inside the class:
```
text → remove HTML → normalize → remove noise → (optional) remove stopwords
     → (optional) lemmatize → final cleaned text
```
*"Preprocessing is a machine with multiple sub-machines inside."*

### 41.6 The end-to-end file-by-file path

```
User / Airflow / API / CLI
        ↓
   src/main.py
        ↓
   InputRouter.route_push_input()
        ↓
   io_adapters/file_readers.py
        ↓
   Raw Record (rich metadata dict)
        ↓
   InputRouter._to_internal_document()
        ↓
   InternalDocument        ← ONLY THIS ENTERS NLP
        ↓
   nlp_pipeline/preprocessing.py
        ↓
   features.py → embeddings → vector_index.py
        ↓
   scoring_engine.py
        ↓
   storage_clients.py
```

### 41.7 Batch-directory ingestion and the demo entry point

`InputRouter.process_directory(directory, recursive=True, output_file="internal_documents.jsonl")`
walks the directory (`rglob` when recursive), routes every file through `route_push_input`,
writes `doc.to_jsonl()` per line, and returns statistics `{total, success, failed, skipped}` —
counting `UnsupportedFileTypeError` as *skipped* and any other exception as *failed* (logged to
`errors.jsonl`), so one bad file never stops the batch.

The usage examples belong in `src/main.py`, **not** in `InputRouter`:
```python
router = InputRouter(config, output_dir="./ingestion_output")

doc = router.route_push_input(file_path='report.pdf')          # 1 single file
doc = router.route_push_input(raw_text='Hello world')          # 2 raw text
doc = router.route_push_input(api_payload={'id': '123', 'text': 'Article content...'})   # 3
doc = router.route_push_input(es_hit={                          # 4 Elasticsearch hit
        "_id": "abc123", "_index": "news_articles", "_score": 1.23,
        "_source": {"title": "Breaking News",
                    "body": "This is the article text from Elasticsearch"}})
doc = router.route_push_input(kafka_message={                   # 5 Kafka message
        "topic": "news_stream", "partition": 0, "offset": 1024,
        "timestamp": "2025-01-01T12:00:00Z",
        "value": {"content": "Streaming news article text"}})

for doc in router.route_pull_source(source_type="elasticsearch"):   # 6 pull/batch mode
    print(doc.document_id, doc.word_count)

stats = router.process_directory(directory="./sample_docs", recursive=True)   # 7 directory
```
Router config for those examples:
```python
config = {'sources': {
    'elasticsearch': {'host': 'localhost:9200', 'index': 'documents'},
    'kafka':         {'bootstrap_servers': 'localhost:9092', 'topic': 'documents'}}}
```

### 41.8 `_determine_source_type` — the resolution order

Checks `raw_record['reader_class']` **first**, then falls back to substring matching on the
`source_hint`: PDFReader/pdf → `FILE_PDF` · DocsReader/docx → `FILE_DOCX` · TxtReader/txt →
`FILE_TXT` · CSVReader/csv → `FILE_CSV` · JSONReader/json → `FILE_JSON` · JSONLReader/jsonl →
`FILE_JSONL` · HTMLReader/html → `FILE_HTML` · XMLReader/xml → `FILE_XML` · MarkdownReader/
markdown → `FILE_MARKDOWN` · ParquetReader/parquet → `FILE_PARQUET` · ImageReader/png|jpg|jpeg →
`FILE_IMAGE` · ArchiveReader/zip|tar|gz → `FILE_ARCHIVE` · api → `API_REST` · elasticsearch →
`ELASTICSEARCH` · kafka → `KAFKA` · s3 → `S3` · **default fallback `FILE_TXT`**.

Supporting helpers:
```python
def _extract_text_from_payload(self, payload):     # for API / ES / Kafka payloads
    for field in ['text', 'content', 'body', 'message', 'description', 'data']:
        if field in payload and payload[field]: return str(payload[field])
    return json.dumps(payload, ensure_ascii=False, indent=2)      # stringify as last resort

def _generate_document_id(self, text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()       # deterministic

def _log_error(self, raw_record, error):
    """Append {timestamp, error, error_type, record} to errors.jsonl"""
```
And the full `_extract_text` fallback chain, beyond the six named fields of §35.7: try
`paragraphs` (join with blank lines) → try `ocr_results['extracted_text']` → try `raw_data`
(return it if a string, else `json.dumps` it) → last resort, stringify the entire record →
otherwise raise `NoTextFoundError`.

---

## 42. Where big-data engineering actually appears

The project *looks* like a normal NLP pipeline but is built exactly like a big-data enterprise
media-analysis pipeline. **Roughly 70% of the pipeline is designed as a big-data system.**
It appears in four layers:

**1. Ingestion — 100% big-data engineering.** KafkaConsumer (millions of messages/hour, news
streams, continuous logs, live updates), S3Loader (terabytes of raw articles, huge archives,
daily media dumps, Parquet storage), ESClient (indexing millions of articles/logs/documents),
APIClient, ScraperClient. These are not small-text readers.

**2. Preprocessing — distributed framework integration.** `preprocess_spark.py` (TB-scale
tokenization, cleaning, segmentation — for 100M+ articles), `preprocess_ray.py` (big-data
concurrency without a heavyweight Spark cluster), `classify_batch.py` (classification across the
entire data lake).

**3. Storage — columnar storage is pure big-data tech.** Parquet (data lakes, petabyte-scale
pipelines, analytics, Spark/Hive/Athena), plus S3, Elasticsearch and Redis. Parquet is one of the
strongest signals that this is a big-data project.

**4. Scalability — embeddings and vector indexes.** Computing embeddings for 10M pages is
impossible on normal hardware without batching, distributed processing, ONNX optimization and
FAISS indexing. Vector DBs are modern big-data infrastructure.

```
[Kafka / S3 / APIs / ES]  →  (big-data ingestion)
        ↓  [Input Router]
        ↓  [Spark / Ray preprocessing]
        ↓  [Segmentation + NLP]
        ↓  [Embeddings ONNX / Vector Index]
        ↓  [Scoring Engine]
        ↓  [Parquet / Redis / Elastic]
        ↓  [FastAPI serving]
```

Files that are definitively big-data oriented: `preprocess_spark.py` (tokenizing millions of
documents) · `preprocess_ray.py` (parallel CPU cleaning and NLP) · `classify_batch.py`
(classification over entire data lakes) · `parquet_writer.py` (scalable columnar data) ·
`s3_loader.py` (massive object storage) · `vector_index.py` (indexes for millions of embeddings)
· `kafka_consumer.py` (real-time ingestion streams) · `es_client.py` (querying large document
indexes) · `embeddings_onnx.py` (batch vectorization optimized for CPU).

**One-sentence answer:** big-data engineering is used in ingestion, batching, preprocessing,
embeddings, indexing, scoring and storage.

### 42.1 Hadoop / MapReduce / Hive / Spark — the verdict

| Technology | Use it? | Reason |
|---|---|---|
| **Hadoop** | ❌ **No — ever** | Dead technology. HDFS replaced by S3/GCS/Azure Blob; MapReduce is painfully slow; nobody uses Hadoop for NLP pipelines anymore; even LinkedIn, Netflix and Uber moved away. Using it would make a modern pipeline old, slow and unnecessary. |
| **MapReduce** | ❌ No | Superseded by Spark 10+ years ago; slow, outdated, hard to debug, zero value for embeddings or classification. |
| **Hive** | ❌ No | Only useful for petabyte-scale SQL on HDFS+Hadoop via HiveQL. This project uses Parquet, S3, Python, Spark/Ray, FastAPI, embeddings and a vector index — Hive has no place. |
| **Spark** | ✔ Optional | Useful for large-scale cleaning, large-scale tokenization, batch embeddings over millions of docs, distributed preprocessing, and Ray+Spark hybrids. Modern and used everywhere (Databricks, AWS EMR, GCP Dataproc). |
| **Ray** | ✔ Recommended | Modern, lightweight parallelism. |
| **Dask** | Optional | Alternative to Ray. |

*"You are building a modern media analysis platform, not a 2010 data warehouse."* Hadoop/Hive
would make the project slower, outdated, harder to maintain, less impressive and misaligned with
industry.

### 42.2 Elasticsearch learning path (the notebooks to actually read)

**Must do — the complete foundation (3):**
1. `01-keyword-search.ipynb` — basic ES queries: `match`, `match_phrase`, `term`, filters. Needed
   for taxonomy-based / rule-based keyword retrieval.
2. `03-semantic-search.ipynb` — semantic search in Elasticsearch with dense vectors; the queries
   used inside `ESClient`.
3. `03-es-vector.ipynb` — storing vectors inside ES, vector indexing and kNN search.

**Optional but useful (2):** `02-hybrid-search.ipynb` (keyword + vector, relevant to
`hybrid_router`) and `04-semantic-ranking.ipynb` (post-retrieval ranking, applicable in
`scoring_engine`).

**Skip — not relevant to `ESClient`:** generative AI, LangChain/RAG, document chunking, model
upgrades, Cohere integrations, external rerankers.

Rationale: `ESClient` needs keyword search, full-text search, optional vector search, hybrid
search, pagination, retrieving hits, handling `_source` fields, and converting results into
`InternalDocument`.

### 42.3 `features.py` vs the IO adapters — the boundary question

`FeatureExtractor` owns embeddings, n-grams and vectorizers:
```python
class FeatureExtractor:
    def __init__(self):
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
    def ngrams(self, text, n=2): ...
    def tfidf(self, texts): ...
    def embed(self, sentences):
        return self.embedding_model.encode(sentences, convert_to_numpy=True)
```
`io_adapters/` owns only *talking to external systems* — S3, Kafka, Elastic, Redis, local/remote
APIs, databases, Parquet/Feather/DuckDB. `nlp_pipeline/preprocessing.py` is the standard
Python-only preprocessing used by `main.py`, the API, the rules engine and the classification
pipeline — **it does not move**. `batch_processing/` is *only* for Spark/Ray, which are heavy
distributed tools and must not be mixed into the normal Python pipeline.

---

## 43. Type and identifier registry

Every named type, class and external identifier that appears anywhere in the design
conversations, with its role — so a name encountered in old notes or code can always be
resolved, and so `shared_types.py` can be written without inventing names.

### 43.1 Inter-stage data types (the contracts each stage returns)

These are the objects that flow between pipeline stages. **`shared_types.py` should declare
them; they are the contracts every stage signs.**

| Type | Produced by | Contents |
|---|---|---|
| `InternalDocument` | `InputRouter._to_internal_document()` | The ingestion↔NLP contract (§5.1) |
| `NormalizedDocument` | `TextProcessor.normalize()` | `full_text`, `tokens`, `token_offsets`, metadata carried from the original |
| `Sentence` / `SegmentList` | `SentenceSegmenter.segment()` | Sentence id, text, `start_char`, `end_char`; no overlap, full coverage |
| `ArgumentSpan` | `ArgumentMiner.extract()` | claim / premise / support / rebuttal spans |
| `FeatureBundle` | `FeatureExtractor.build_features()` | `{"document": {…}, "sentences": {sent_id: {…}}}` |
| `RuleClassificationResult` | `RuleEngine.classify()` | `sentence_labels` (node id + score + **evidence**), `document_labels` |
| `MLClassificationResult` | `MLClassifier.predict()` | probabilities per node per sentence/doc |
| `FinalClassification` | `HybridRouter.merge()` | the merged label sets used by scoring |
| `ScoreResult` | `ScoringEngine.score()` | metric → value, plus a breakdown |
| `ScoredDocument` | `PostProcessor.to_output_schema()` | the final output-schema-conformant object |

**`InternalDocumentRaw` vs `InternalDocumentProcessed`** — an earlier design proposed *two*
internal document schemas: a raw one straight out of ingestion and a processed one after NLP.
The final design **collapsed these into one** `InternalDocument` (the raw rich reader output
stays attached as `source_metadata`, and processing state is tracked by the
`ProcessingStatus` enum) — but the two-schema idea appears in older notes and is worth
recognising.

### 43.2 Wiring / config types

| Type | Role |
|---|---|
| `PipelineContext` | The object returned by `build_services()`/`build_context()` holding every constructed service plus the configs. (`main.py` currently returns a plain dict; a dataclass is the cleaner form.) |
| `PipelineConfig` | Parsed `pipeline_v1.yaml` |
| `TaxonomyConfig` | Parsed + validated `taxonomy_v1.yaml` (returned by `load_taxonomy`) |
| `ScoringConfig` | Parsed `scoring_v1.yaml` |
| `TaxonomyDiff` | Returned by `diff_taxonomies(old, new)` |
| `SourceConfig` | A named per-source ingestion config entry (§36) |

### 43.3 API model names — two naming generations

| Earlier pass | Final pass | Role |
|---|---|---|
| `PipelineRequest` | `AnalyzeRequest` | POST /analyze request body |
| `PipelineResponse` | `AnalyzeResponse` | POST /analyze response |
| — | `SentenceLabel`, `DocumentScore` | nested response types |

Both appear in the notes; **`AnalyzeRequest`/`AnalyzeResponse` is authoritative** (§33.2).

### 43.4 Composite score names

Named composites that appear across the design: **`BiasScore`** · **`ManipulationIndex`** ·
**`PropScore`** (per-document propaganda score, §21.1 formula 4) · **`PropagandaIndex`** (the
same quantity under its alternative name, `1 − Π(1 − transparency_violation(p) × w'_p)`) ·
**`FactualityRating`** · **`QualityScore`** · **`CredibilityScore`** · **`ManipulationScore`** ·
**`EmotionalIntensity`** · **`LogicalSoundness`** · **`objectivity_score`** ·
**`Media Objectivity Score (MOS)`** — the project's original internal name for the headline
metric.

### 43.5 Reader classes — built, planned and deferred

| Class | Status |
|---|---|
| `TxtReader`, `MarkdownReader`, `PDFReader`, `DocsReader`, `CSVReader`, `JSONReader`, `JSONLReader`, `HTMLReader`, `XMLReader` | implemented in `file_readers.py` |
| `PPTReader` | designed, not implemented |
| `ParquetReader` | **next priority** after the file readers (§7.7) |
| `ArchiveReader` | planned — zip, tar, gzip |
| `ImageReader` | planned — OCR via pytesseract |
| `AudioReader` | stubbed as a commented-out class; ASR (Whisper/Kaldi) → transcript → normal pipeline |
| `HadhoopReader` *(sic — misspelling of Hadoop in the source)* | commented-out stub; **not needed** — Hadoop is explicitly rejected (§42.1) |

### 43.6 Naming variants and known typos

| Appears as | Correct form | Note |
|---|---|---|
| `ParqueWriter` | `ParquetWriter` | typo flagged in the source itself: *"fix name to ParquetWriter in real code"* |
| `Bais` | `Bias` | live typo in `features.py` (Appendix A, bug 5) |
| `Sentiment_Subjecivity` | `Sentiment_Subjectivity` | live typo in `features.py` |
| `UniversalInputLoader` / `UniversalLoader` | `file_readers.py` + `InputRouter` | the superseded single-loader design (§39.2) |
| `ScraperReceiver` / `APIReceiver` / `FileReceiver` / `KafkaReceiver` / `ESDocumentParser` / `ESClientFetcher` / `api_receiver` / `api_fetcher` | `.receive()` / `.fetch()` methods on one class | the superseded Receiver/Fetcher class-pair design (§39.3) |
| `UnsupportedInputError` | `UnsupportedFileTypeError` | the implemented exception name (§35.1) |
| `RulesEngine` | `RuleEngine` | singular is the implemented name |
| `EmbeddingsONNX` | `EmbeddingGenerator` | class inside `embeddings_onnx.py` |
| `CleanText()` | `TextProcessor.normalize()` | the original name for the cleaning function |
| `DocumentFactory`, `BatchRunner` | `StorageClientFactory`, `PipelineRunner` | early alternative names |
| `IssueStance` | `Stance` | DB table name variant (§25.1) |
| `VectorSearch` | `VectorIndex` (FAISS) or ES kNN | ambiguous in old notes — see §37 for which is meant |

### 43.7 Concrete model and service identifiers

Every externally-named model or service referenced in the design:

**Embeddings / sentence encoders**
- `sentence-transformers/all-MiniLM-L6-v2` — the chosen encoder (384-d, ONNX, CPU)
- `sentence-transformers/paraphrase-MiniLM-L6-v2` — used in the red-herring similarity example
- `all-MiniLM-L12-v2` — used in the logical-flow coherence example
- spaCy `en_core_web_lg` (word vectors) / `en_core_web_sm` / `xx_ent_wiki_sm` (multilingual)

**NLI / contradiction**
- `roberta-large-mnli`, `facebook/bart-large-mnli`
- `ynie/roberta-large-snli_mnli_fever_anli_R1_R2_R3-nli`, `uclnlp/bert-tiny-fever` — fact verification

**Sentiment / emotion / toxicity**
- `distilbert-base-uncased-finetuned-sst-2-english` — polarity
- `bhadresh-savani/distilbert-base-uncased-emotion` — emotion classes
- `nlptown/bert-base-multilingual-uncased-sentiment` — 1–5 stars → [-1,1]
- `unitary/toxic-bert`, `unitary/unbiased-toxic-roberta` — toxicity
- Google **Perspective API** — external toxicity service
- VADER (`nltk.sentiment.vader`), TextBlob, NRCLex, LIWC — lexicon-based alternatives

**Fallacy / propaganda classifiers**
- `roberta-base`, `deberta-v3-large`, `distilroberta-base` — fine-tuning bases for the fallacy
  classifier
- `bert-base-cased`, `roberta-large`, `bert-large-uncased-news` — propaganda span/technique models
- `sknfer/propaganda-techniques` — a possible pre-existing propaganda model ("if it exists")
- `myorg/roberta-fallacy-detector`, `myorg/bert-propaganda-techniques` — **placeholder names** for
  your own fine-tuned models in the code templates; replace with real paths

**QA / generation**
- `ktrapeznikov/albert-xlarge-v2-squad-v2` — retrieval QA, used for verifying whether a quote can
  be found (false-attribution detection)
- `google/flan-t5` — noted as a possible future extension for truthiness verification
- GPT-2 (`GPT2LMHeadModel`) — perplexity for coherence-drop detection
- GPT-4 — **explicitly rejected**: "not deterministic or explainable enough for our needs"

**Datasets / corpora**
- SemEval-2020 Task 11 (Propaganda Techniques Corpus, PTC) — propaganda span data
- Jin et al. logical fallacy dataset — fallacy classifier training/eval
- CAMPFIRE corpus — fallacy frames (slippery slope, hasty generalization)
- FEVER — fact verification
- Jigsaw Toxic Comments — toxicity
- Moral Foundations Dictionary (Graham et al.) — §19.2
- NRC Emotion Lexicon, Connotation Lexicon, Hatebase (slurs), WordNet

**External knowledge / verification services**
- **MediaBiasFactCheck** and **AllSides** — outlet bias & reliability ratings
- Wikidata Query Service, DBpedia, Wikipedia API, Wikiquote API — fact and quote verification
- Google Fact Check Tool API, Diffbot Knowledge Graph
- **DuckDuckGo API** (`api.duckduckgo.com`, `AbstractText` field) — used in the data-accuracy
  code sample as a quick search-and-compare step
- **WikiBrowser** — named as an option for retrieving known facts on a topic
- Bing Search API — alternative claim lookup
- GDELT, NewsAPI — news corpora/streams

**Libraries named for specific jobs**
- `charset_normalizer` (encoding), `python-magic` (MIME), `pdfplumber` + `PyMuPDF`/`fitz` (PDF),
  `python-docx`, `python-pptx`, `markdown`, `BeautifulSoup`/`lxml`, `pandas`/`pyarrow`,
  `pytesseract` + `Pillow` (OCR), `sqlalchemy`, `pymongo`, `boto3`, `kafka-python`/
  `confluent-kafka`, `redis`, `elasticsearch`, `requests`
- `textstat` (readability, passive voice), `pysbd` (segmentation), `Stanza`/StanfordNLP,
  `AllenNLP` (SRL, OpenIE, coreference), `NeuralCoref`, `Arguendo` (argument mining),
  `pyWSD` (word-sense disambiguation), `HeidelTime`/`SUTime` (temporal extraction),
  `pyRST`/`rstlite` (discourse parsing), `DeCLUTR` (sentence clustering),
  `Gensim`/`sklearn` LDA, `BERTopic`, `fastText`, `GloVe`, `NetworkX`, `SciPy` (outlier
  detection), `difflib` (string similarity), `newspaper3k`, `Scrapy`
- `SparkSubmitOperator` — the Airflow operator for launching Spark jobs (alongside
  `BashOperator` / `PythonOperator`)

**Infrastructure images / services**
- `python:3.10-slim` (Docker base), `bitnami/kafka` + `bitnami/zookeeper` (§31),
  Elastic Cloud / Docker Compose / Kubernetes for ES clusters, MinIO (free S3-compatible),
  FAISS / Milvus / Weaviate / Pinecone / Qdrant (vector stores), DuckDB, Neo4j

### 43.8 Model artifacts on disk

```
models/taxonomy_model.pkl      # scikit-learn trained classifier (LogReg / SVM / RandomForest)
models/news_classifier.onnx    # referenced by pipeline_v1.yaml → ml.model_path
models/sentence_encoder.onnx   # referenced by pipeline_v1.yaml → embeddings.model_path
models/vector.index            # FAISS index
```
All gitignored (large binaries). `models/` does not exist yet and must be created before the ML
or embedding stages can run.

Example data-lake paths from the design: `data/raw/news_2025_01.parquet` (Bronze),
`data/processed/` (Gold), `clean_docs/` and `raw_docs/` in the Spark example,
`/data/raw/` and `/data/processed/` in `pipeline_v1.yaml`.

---

## Appendix A — Known bugs to fix before building new code

1. **`io_adapters/input_router.py`** — `_initialize_file_readers()` stores reader *class names as
   strings* (`'TxtReader()'`) instead of instances, and `_handle_file_path()` ignores the dict
   entirely and always calls `_mock_file_read()`. The real readers are never called. Fix:
   instantiate the readers in the constructor and remove `_mock_file_read()`.
2. **`ml_classifier.py`** — `from sklearn.externals import joblib` was removed in scikit-learn
   0.23. Replace with `import joblib`.
3. **`io_adapters/shared_types.py`** — a duplicate stub whose `InternalDocument` is an empty
   function; it shadows the real one in `core/internal_document.py`. Delete or repurpose it.
4. **`conf/pipeline_v1.yaml`** — `seed: #idk` must become a real integer (e.g. `42`).
5. **`features.py`** — class-name typos: `Bais` → `Bias`, `Sentiment_Subjecivity` →
   `Sentiment_Subjectivity`. Fix before building any feature logic.
6. **`conf/taxonomy_v1.yaml` and `conf/scoring_v1.yaml`** are empty; `data_schema/*.json` are
   placeholder comment strings, not real JSON schemas.
7. **`main.py`** — `process_document()` and `run_pipeline()` are `pass`; `build_services()`
   returns nothing; config paths are hard-coded absolute Windows paths.
8. **`models/`** does not exist yet but is referenced by `pipeline_v1.yaml`
   (`models/news_classifier.onnx`, `models/sentence_encoder.onnx`).
9. `tree.txt` should be gitignored, not committed.

---

## Appendix B — The 15 logical fallacy types (canonical list)

Ad Hominem · Straw Man · False Dilemma · Slippery Slope · Circular Reasoning ·
Hasty Generalization · Red Herring · Appeal to Authority · Appeal to Emotion · Bandwagon ·
Cherry Picking · False Cause · Equivocation · Appeal to Tradition · Appeal to Novelty

Each instance must produce `{fallacy_type, fallacy_span, confidence_score, severity}`.

*(The wider catalog also covers: No True Scotsman, Burden of Proof Shift, Loaded Question,
Anecdotal Evidence, False Attribution, Motive Fallacy, Guilt by Association, Whataboutism,
Gaslighting, Scapegoating, Card Stacking, Omission Bias, Statistical Manipulation, Framing Bias,
Narrative Inconsistency, Coherence Drop, Transparency Gaps, Source Opaqueness, Conflict of
Interest, Unsupported Quantifiers and Hedging Signals — see §12 and §13.)*

## Appendix C — The 13 propaganda / rhetorical techniques (canonical list)

Loaded Language · Name Calling · Glittering Generalities · Card Stacking · Bandwagon
(Propaganda) · Appeal to Fear · Appeal to Authority · Plain Folks · Testimonial · Transfer ·
Guilt by Association · Scapegoating · False Dilemma (Propaganda)

Each instance must produce `{technique, text_span, intensity}`.

*(The system-design variant of the set: name_calling, loaded_language, glittering_generalities,
fear_appeal, appeal_to_prejudice, flag_waving, whataboutism, repetition, oversimplification,
exaggeration, minimization, obfuscation, thought_terminating_cliche.)*

## Appendix D — Visualization and dashboard plans

- **Scatter**: x = BiasScore, y = FactualityScore, one point per article, coloured by publisher
  or topic. Quality journalism clusters in the high-factuality / low-bias corner; fringe
  propaganda in the low-factuality / high-bias corner.
- **Radar / spider charts** per article: one spoke per propaganda technique intensity, or per
  moral foundation. A propaganda-heavy article spikes on specific spokes; a neutral report stays
  near the centre.
- **Heatmaps / bar charts** of logical fallacy occurrence by type across a collection.
- **Entity sentiment bar chart** showing how positively or negatively each entity is portrayed.
- **Timeline** of average bias score per topic per month, to see whether coverage is polarising.
- **Network graph** of co-mentioned entities: nodes = people/organisations, edges weighted by
  co-mention count, node colour = average sentiment — uncovers polarising figures and which
  "side" mentions them positively.
- **Interactive article viewer** with colour-coded highlights (red = fallacies, orange =
  propaganda, blue = loaded language, green = evidence/citations) and hover tooltips
  ("Propaganda: Loaded Language (intensity 0.8)"). *This is the key explainability surface.*
- **Distribution histograms** — e.g. reading level by publisher, propaganda index across the
  dataset.
- **Comparison charts** — outlets compared on average bias/factuality; stacked bars showing the
  distribution of propaganda techniques in left- vs right-leaning sources.
- **Dimensionality-reduction plots** — PCA (PC1 may track factuality vs misinformation, PC2
  partisan bias) or an interactive t-SNE/UMAP plot where each point is an article and clusters
  can be annotated by topic or style.
- **Filters** by date range, publisher, topic and score thresholds; selecting a subset (one
  outlet's content) shows its aggregate bias/propaganda profile.
- **Drill-down**: clicking a BiasScore expands the contribution breakdown ("Loaded language: 0.8,
  One-sided reporting: 0.7") with the actual text examples.
- **Stance summary**: "Out of 100 articles on topic X, 30% support, 50% neutral, 20% oppose."

Every number in a composite score must be traceable to raw features — *transparency in the
dashboard is as important as transparency in the analysis.* Visualizations must convey
uncertainty and intensity properly (colour gradients, tooltips with the actual scores).
Journalists gravitate to the text-highlight view and the bias/factuality scatter; researchers to
the PCA cluster view for spotting outliers and groups.

---

## Appendix E — Learning path (grouped, with search terms)

| Area | Topics | Search terms |
|---|---|---|
| **IO adapters** | Python file I/O (`open`, `pathlib`); PDF/DOCX/PPT parsing; APIs; basic Kafka, Redis, S3, ES concepts | "Real Python file handling", "Python requests guide", the official docs for each library |
| **NLP core** | Tokenization, lemmatization, n-grams; rule-based vs ML classification; sentence segmentation algorithms; embeddings & ONNX | "spaCy 101", "HuggingFace transformers beginner guide", "sentence embeddings tutorial" |
| **Infra / big data** | Docker basics; PySpark vs Ray; Airflow as orchestration | "Docker getting started", "PySpark quickstart", "Airflow tutorial" |
| **Testing & config** | pytest; YAML configuration patterns; JSON Schema | "pytest tutorial", "YAML vs JSON configuration", "jsonschema Python tutorial" |
| **Advanced stack** | Airflow ~2 h · Docker ~2–3 h · PyBind11 ~15 min · CUDA ~10–20 min · GitHub Actions ~30 min | ≈ 6 hours total |

Per-module learning notes are attached inline to each file in §33.

---

*End of consolidated reference.*
