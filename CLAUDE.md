# NLPpipline — Project Context for Claude

> **See `README.md`** for the full developer reference (architecture diagram, config schema, API contract, extension points). This file contains the context Claude needs that isn't derivable from code alone.

## Origin & purpose

This project was built as a **media/news NLP analysis platform** — originally proposed for a Data Engineer / NLP Engineer role at a media company. The brief was to build a deterministic, mathematically grounded text analysis pipeline that maps content to an internal taxonomy (bias, logical fallacies, rhetorical techniques, sentiment, stance, fact-checking) and produces clean, reproducible JSON for backend and frontend teams.

Key design constraints from the original proposal:
- **Deterministic**: same input must always produce same output. Fixed seeds, versioned models, no online learning.
- **Explainable**: rule-based core takes precedence; ML fills gaps for ambiguous cases.
- **Config-driven**: taxonomy and scoring logic live in YAML — the team controls weights/thresholds without touching code.
- **Contract-based**: backend calls one service function, gets back JSON that strictly matches `data_schema/output_schema.json`. No surprises.
- **Scalable**: batch via Airflow + Spark/Ray; real-time via API.

The project was **aborted mid-build** and is being resumed. **~15% implemented.** The ingestion layer is mostly done; every NLP processing stage is a stub.

---

## Tech stack

From `requirements-dev.txt` — key libraries:

| Concern | Library |
|---|---|
| NLP / tokenization | spaCy 3.8, pysbd, NLTK, stanza |
| Sentence embeddings | onnxruntime, transformers (MiniLM/SentenceTransformers) |
| ML classifier | scikit-learn 1.7, onnxruntime |
| Vector search | FAISS (not yet imported), numpy |
| Taxonomy graph | networkx |
| File reading | pdfplumber, PyMuPDF, python-docx, pyarrow, pandas |
| API | FastAPI + uvicorn |
| Storage | redis, boto3 (S3), kafka-python, pyarrow (Parquet) |
| Batch | pyspark 4.0 (in requirements), Ray (not yet — add when needed) |
| Orchestration | apache-airflow |
| Validation | pydantic v2, jsonschema |
| Sentiment | vaderSentiment |
| OCR | pytesseract |

---

## Intended data flow

The pipeline uses a **Bronze / Silver / Gold** Parquet data lake architecture. Each zone is an inter-stage storage checkpoint that decouples ingestion, processing, and serving.

```
RAW INPUT (file / API / ES / Kafka / S3 / scraper)
        ↓
   InputRouter  ──→  routes to right reader or client
        ↓
  InternalDocument   ← THE core contract between ingestion and processing
        ↓
  [BRONZE ZONE]  ── JSONL rows written by storage_clients.py (JSONLWriter)
        ↓
   TextProcessor.normalize(doc)  →  NormalizedDocument
        ↓
   SentenceSegmenter.segment(normalized)  →  List[Sentence]
        ↓
  [SILVER ZONE]  ── Parquet (clean text, tokens, sentences, entities) written by ParquetWriter
        ↓
   TaxonomyLoader.load()  →  OntologyGraph  ← reads taxonomy_v1.yaml
        ↓
   ArgumentMiner.extract(sentences)  →  argument spans + claim/premise labels
     (Stage not yet implemented — lives between segmentation and feature extraction)
        ↓
   FeatureRegistry.gate(ontology_labels)  ← YAML/Git registry; gates which features run
     Feature categories: LogicalFallacy, Rhetorical, Bias, Sentiment_Subjectivity,
                         Stance, FactCheck, Linguistic, Mathematics, Deterministic,
                         Metadata, Advanced
        ↓
   FeatureExtractor.build_features(normalized, segments, args, metadata)  →  feature bundle
        ↓
   EmbeddingGenerator.embed(text)  →  VectorIndex.upsert()   ← FAISS (read-only semantic memory)
        ↓
   RuleEngine.classify(features, segments)        ← taxonomy-aware; OntologyGraph thresholds it
        +
   MLClassifier.predict(features, sentences)      ← ONNX model from models/
        ↓
   HybridRouter.merge(rule_result, ml_result, ontology)  →  final labels
        ↓
   ScoringEngine.score(classification, features)  ← reads scoring_v1.yaml
        ↓
   PostProcessor.to_output_schema(...)  →  structured JSON
        ↓
  [GOLD ZONE]  ── Parquet (features, labels, scores, pipeline version) written by ParquetWriter
        ↓
   StorageClientFactory  →  SQL Serving DB / S3 / Kafka / Redis (for real-time query)
```

`OntologyGraph` (networkx) wraps the taxonomy. Used by `RuleEngine`, `HybridRouter`, and `FeatureRegistry`.

### Key architectural notes from the design documents

- **FeatureRegistry must be consulted BEFORE FeatureExtractor runs.** The taxonomy determines which features are relevant for a given document class. Running all 13 feature layers on every document is wasteful. The registry (YAML + Git-versioned) gates feature selection based on the taxonomy classification result from the previous step.
- **Argument Mining is an explicit stage** between Silver Parquet and Feature Extraction. It identifies claim/premise/support/rebuttal spans. Fallacy detection, PropScore, and stance classification depend on this structure.
- **Vector DB (FAISS) is read-only semantic memory** — it stores sentence embeddings for similarity search and taxonomy suggestion clustering. It does NOT participate in classification decisions. It is not a decision-maker.
- **Combined taxonomy + fallacy detection pipeline** (the full intended flow):
  ```
  [Ingestion → JSONL/Bronze] → [Preprocessing → Silver Parquet]
  → [Taxonomy Classification] → [Argument Mining]
  → [Feature Extraction] → [Taxonomy-Aware Feature Gating]
  → [Fallacy Detection Engine] → [Scoring + Confidence]
  → [Gold Parquet] → [SQL Serving + Reports]
  ```

### Canonical Parquet inter-stage schema

Every ParquetWriter write must conform to this schema:

| Column | Type | Populated at |
|---|---|---|
| `doc_id` | string | Bronze |
| `source` | string | Bronze |
| `raw_text` | string | Bronze |
| `clean_text` | string | Silver |
| `tokens` | list[string] | Silver |
| `sentences` | list[struct] | Silver |
| `entities` | list[struct] | Silver |
| `arguments` | list[struct] | Argument Mining |
| `labels` | list[string] | Gold |
| `features` | struct | Gold |
| `scores` | struct | Gold |
| `metadata` | struct | Throughout |
| `pipeline_version` | string | Gold |
| `processed_at` | timestamp | Gold |

---

## File map — what's done vs stub

### Complete / real code
- `core/internal_document.py` — `InternalDocument` dataclass. Fields: `document_id`, `text`, `source_type` (SourceType enum), `ingestion_timestamp`, `source_metadata`, `language`, `title`, `author`, `processing_status`, `tables`, `images`, `sections`, `quality_flags`, `char_count`, `word_count`, `line_count`. Has `to_dict()`, `to_json()`, `to_jsonl()`, `from_dict()`. **This is the main contract — everything flows through it.**
- `core/exceptions.py` — `IngestionError`, `UnsupportedFileTypeError`, `NoTextFoundError`, `InvalidInputError`, `SourceConnectionError`, `ExtractionError`
- `io_adapters/file_readers.py` — Real read logic for TxtReader, PDFReader, DocsReader, CSVReader, JSONReader, JSONLReader, HTMLReader, XMLReader, MarkdownReader
- `conf/pipeline_v1.yaml` — Full configuration. Input sources (files, API, ES, Kafka, S3, scraper, Redis), output formats (Parquet, JSONL, Redis, Kafka, S3), feature extraction flags, ML config, embeddings config, logging, batch processing settings.

### Built but broken — fix first
- `io_adapters/input_router.py` — Routing logic is correct. **Bug:** `_initialize_file_readers()` stores reader class names as strings (`'TxtReader()'`) not instances. `_handle_file_path()` then ignores the dict entirely and always calls `_mock_file_read()`. Real readers are never called. Fix: instantiate readers in the constructor, remove `_mock_file_read()`.

### Stubs — all method bodies are `pass`
- `nlp_pipeline/shared_types.py` — `NormalizedDocument` and `Sentence` are **empty functions**, not dataclasses. Must be converted.
- `nlp_pipeline/preprocessing.py` — `TextProcessor`: `_strip_html`, `_normalize_unicode`, `_normalize_whitespace`, `_lemmatize`, `normalize(doc: InternalDocument) -> NormalizedDocument`
- `nlp_pipeline/segmentation.py` — `SentenceSegmenter.segment(normalized_doc)` — imports pysbd + spaCy
- `nlp_pipeline/features.py` — `FeatureExtractor.build_features(normalized_doc, segments, metadata)` + empty feature category classes: `LogicalFallacy`, `Rhetorical`, `Bais` (typo for Bias), `Sentiment_Subjecivity` (typo), `Stance`, `FactCheck`, `Linguistic`, `Mathematics`, `Deterministic`, `Metadata`, `Advanced`
- `nlp_pipeline/rules_engine.py` — `RuleEngine.classify(features, segments)`, `_evaluate_node_rules(node_id, sentence_features) -> float`
- `nlp_pipeline/ml_classifier.py` — `MLClassifier.predict(feature_bundle, sentences)`, `_features_to_vector(feature_bundle) -> np.ndarray`
- `nlp_pipeline/hybrid_router.py` — `HybridRouter.merge(rule_result, ml_result, ontology)`
- `nlp_pipeline/scoring_engine.py` — `ScoringEngine.score(final_classification, feature_bundle)`
- `nlp_pipeline/postprocessing.py` — `PostProcessor.to_output_schema(original_doc, normalized_doc, segments, final_classification, scores)`
- `nlp_pipeline/ontology_graph.py` — `OntologyGraph`: `get_ancestors`, `get_descendants`, `project_labels_to_levels`, `validate_label_set` — uses networkx
- `nlp_pipeline/embeddings_onnx.py` — `EmbeddingGenerator.embed(text_or_segments) -> np.ndarray` — uses onnxruntime + transformers AutoTokenizer
- `nlp_pipeline/vector_index.py` — `VectorIndex.upsert(document_id, embedding, metadata)`, `search(query_embedding, top_k)` — FAISS (import is a TODO)
- `nlp_pipeline/deterministic_utils.py` — `set_global_seeds(seed)`, `hash_to_document_id(input_str)`, `compute_config_hashes()` — imports torch, numpy, random, hashlib
- `nlp_pipeline/gpu_router.py` — `is_cuda_available()`, `select_backend(operation_type)`
- `nlp_pipeline/extras.py` — `summarization()`
- `io_adapters/ingest_clients.py` — `APIClient`, `ESClient`, `S3Client`, `KafkaClient`, `ScraperClient`, `RedisClient` — each has `receive()` and `fetch()` stubs
- `io_adapters/storage_clients.py` — `ParquetWriter`, `JSONLWriter`, `RedisWriter`, `LocalStorageWriter`, `StorageClientFactory` — all stubs
- `io_adapters/shared_types.py` — duplicate stub file; `InternalDocument` here is an empty function. The real one is in `core/internal_document.py`. This causes import confusion.
- `taxonomy_tools/taxonomy_loader.py` — `load_taxonomy(taxonomy_cfg) -> Dict`
- `taxonomy_tools/taxonomy_versioning.py` — `diff_taxonomies`, `plan_migration`
- `taxonomy_tools/taxonomy_suggestions.py` — `suggest_new_nodes`
- `api/service.py` — `create_app()` stub
- `api/models.py` — empty
- `main.py` — `process_document()` and `run_pipeline()` are both `pass`; `build_services()` returns nothing; config paths are hard-coded absolute Windows paths
- All files in `tests/` — comments describing what to test, zero actual test code

### Stubs — C++ / CUDA acceleration folders (files exist, 1-line comments only)
- `src/core_accelerators/` — `text_ops.cpp`, `nlp_accel.cpp`, `bindings.cpp`, `CMakeLists.txt` — all 1-line stubs. Intended for PyBind11-exposed CPU SIMD acceleration. Do not wire into the main path until core NLP logic is working.
- `src/gpu_support/` — `cuda_ops.cu`, `cuda_ops.h`, `bindings.cpp` — all 1-line stubs. CUDA kernels for GPU acceleration. `gpu_router.py` is the Python-side entry point.

### Also incomplete — configs/schemas need content
- `conf/taxonomy_v1.yaml` — **empty** (1 blank line). Needed before RuleEngine or OntologyGraph can be built.
- `conf/scoring_v1.yaml` — **empty** (1 blank line). Needed before ScoringEngine can be built.
- `conf/pipeline_v1.yaml` — `seed: #idk` — needs a real integer.
- `data_schema/input_schema.json` — placeholder comment string, not a real JSON schema.
- `data_schema/output_schema.json` — placeholder comment string, not a real JSON schema.

### Other folders / files of note
- `data/` — runtime data directories: `raw/`, `validated/`, `normalized/`, `extracted/`, `failed/`, `logs/`. Gitignored, not committed.
- `models/` — **does not exist yet**. Must be created before ML or embedding stages can run. `pipeline_v1.yaml` references `models/news_classifier.onnx` and `models/sentence_encoder.onnx`. Gitignored (model files are large binaries).
- `pyproject.toml` — complete. Package name `media-nlp-pipeline`, entry point `src/`, Python ≥ 3.10, setuptools build backend.
- `tree.txt` — directory snapshot. Should be gitignored, not committed.
- `notebooks/` — research only. Not imported by any production code. Used for designing rules, testing embeddings, training ML baselines, and generating taxonomy suggestions offline.

---

## Known bugs to fix before building new code

1. **`input_router.py`** — `_initialize_file_readers()` must instantiate real reader objects, not store string names. Remove `_mock_file_read()`.
2. **`ml_classifier.py`** — `from sklearn.externals import joblib` was removed in sklearn 0.23. Replace with `import joblib`.
3. **`io_adapters/shared_types.py`** — This is a duplicate stub that shadows `core/internal_document.py`. Delete or repurpose it.
4. **`conf/pipeline_v1.yaml`** — `seed: #idk` must be a real integer (e.g., `42`).
5. **`features.py`** — typos in class names: `Bais` → `Bias`, `Sentiment_Subjecivity` → `Sentiment_Subjectivity`. Fix before building any feature logic.

---

## Determinism — what must be controlled

Every source of randomness is explicitly seeded. This table is the implementation target for `deterministic_utils.set_global_seeds()`:

| Source | Control |
|---|---|
| Python `random` | `random.seed(seed)` |
| NumPy | `np.random.seed(seed)` |
| PyTorch | `torch.manual_seed(seed)` |
| sklearn estimators | `random_state=seed` on every constructor |
| ONNX inference | Deterministic by construction (frozen graph) |
| Rule evaluation | Strictly ordered; no stochastic branching |
| k-means (taxonomy suggestions) | `KMeans(random_state=seed)` |

`seed` always comes from `pipeline_v1.yaml → pipeline.seed`. It is never hard-coded.

Preprocessing idempotency guarantee — enforce this in tests:
```
preprocess(preprocess(text)) == preprocess(text)
```

---

## Core mathematics — what the original proposal defined

These formulas are the **intended implementation targets** for `scoring_engine.py`, `hybrid_router.py`, and `rules_engine.py`. Do not invent new ones — implement these exactly.

### 1. Article-level scoring (→ `ScoringEngine`)
```
score_article = Σ (w_c × s_c)   for each category c in taxonomy
```
- `w_c` = weight of category c, loaded from `scoring_v1.yaml`
- `s_c` = normalized per-category score (sentence fraction + rule bonuses/penalties)

### 2. Hybrid sentence confidence (→ `HybridRouter`)
```
conf(sentence, category) = α × conf_rules(s, c) + (1 - α) × conf_ml(s, c)
```
- `α` ∈ [0, 1] — configured in `pipeline_v1.yaml`; controls rule vs ML weight
- Thresholds for final category assignment also come from config (not hard-coded)

### 3. Logical fallacy severity (→ `RuleEngine` + `ScoringEngine`)
```
s_i = c_i × w_f
```
- `c_i` = confidence for fallacy instance i (0–1), from rule or ML
- `w_f` = fallacy type weight from `scoring_v1.yaml` (reflects severity of that fallacy type)

Logical flow disruption score (how much fallacies disrupt argument coherence):
```
ℓ = max(s_i × d_fi)   over all detected fallacy instances i
```
- `d_fi` = disruption factor for fallacy type f (domain-specific constant from config)

### 4. Propaganda score / PropScore (→ `ScoringEngine`)
```
PropScore = 1 - Π(1 - v_p)   for each propaganda technique p detected
```
- `v_p` = intensity of propaganda technique p (0–1), from rule match + pattern strength
- Product formula ensures that multiple weak techniques compound into a high score

### 5. Factuality score (→ `ScoringEngine`)
```
F = w1×r_vc + w2×σ̄ + w3×Cn + w4×Lf + w5×(1 - M)
```
- `r_vc` = claim verification rate (verified claims / total claims)
- `σ̄` = mean source credibility score across all cited sources
- `Cn` = internal consistency score (no contradictions)
- `Lf` = logical flow score (no disruptions, ℓ is low)
- `M` = missing context penalty (fraction of key facts omitted)
- `w1..w5` = weights from `scoring_v1.yaml`, must sum to 1

### 6. Multi-label graph (→ `OntologyGraph` + `PostProcessor`)
- Sentences and taxonomy nodes are graph nodes
- Edges: `sentence --(belongs_to, weight=conf)--> taxonomy_node`
- A sentence can link to multiple taxonomy nodes — multi-label is first-class

### 7. Embedding similarity (→ `EmbeddingGenerator` + `taxonomy_suggestions.py`)
```
d(i, j) = 1 - cos(e_i, e_j)
```
- Use **exact** cosine search (not approximate) to keep results reproducible
- Used for clustering misfits/low-confidence sentences to propose new taxonomy nodes

### 8. Taxonomy suggestion workflow (→ `taxonomy_tools/taxonomy_suggestions.py`)
1. Collect low-confidence / unmatched sentences
2. Cluster using k-means on embeddings (fixed seed → deterministic)
3. Compute top keywords + representative examples per cluster
4. Output a **human-reviewable YAML diff** proposing new subcategories
5. Approved diffs become `taxonomy_v2.yaml` with full audit trail

---

## Feature extraction layers — build order and priority

`FeatureExtractor.build_features()` must produce features across 13 layers. The Feature Registry gates which layers run per document class. Build in three phases:

### Phase 1 (build first — foundational)
| Layer | What it produces |
|---|---|
| 1. Textual/Structural | sentence count, avg length, heading structure, list density |
| 2. Lexical/Vocabulary | n-grams, TF-IDF, vocabulary richness, loaded language flags |
| 5. Entity/Attribution | NER spans, quoted sources, citation presence |
| 6. Sentiment/Emotion | polarity [-1,1], emotion distribution, subjectivity score |
| (Embeddings) | ONNX sentence embeddings → FAISS upsert |

### Phase 2 (build after Phase 1)
| Layer | What it produces |
|---|---|
| 7. Framing/Narrative | framing cues, narrative arc markers |
| 8. Rhetorical/Persuasion | 13 propaganda technique scores (PropScore) |
| 9. Logical Fallacy | 15 fallacy types × (confidence, span, severity) |
| 10. Factuality/Evidence | claim count, source credibility, verification rate |

### Phase 3 (build last — requires cross-document data)
| Layer | What it produces |
|---|---|
| 11. Temporal/Contextual | date anchors, recency bias signals |
| 12. Cross-Document/Network | shared entity co-occurrence, cross-source contradiction |
| 13. Metadata/Provenance | source, author, publication date, pipeline version |

### Feature storage strategy
- **Scalar features** → Parquet columns (Gold zone)
- **List/nested features** (entity spans, sentences) → Nested Parquet structs
- **Embeddings** → FAISS / Vector DB (not in Parquet)
- **Scores** → Versioned Parquet columns stamped with `pipeline_version`

### The 15 logical fallacy types to detect (→ `LogicalFallacy` feature class)
Ad Hominem, Straw Man, False Dilemma, Slippery Slope, Circular Reasoning, Hasty Generalization, Red Herring, Appeal to Authority, Appeal to Emotion, Bandwagon, Cherry Picking, False Cause, Equivocation, Appeal to Tradition, Appeal to Novelty

Each instance must produce: `{fallacy_type, fallacy_span, confidence_score, severity}`

### The 13 propaganda / rhetorical techniques to detect (→ `Rhetorical` feature class)
Loaded Language, Name Calling, Glittering Generalities, Card Stacking, Bandwagon (Propaganda), Appeal to Fear, Appeal to Authority, Plain Folks, Testimonial, Transfer, Guilt by Association, Scapegoating, False Dilemma (Propaganda)

Each instance must produce: `{technique, text_span, intensity}`

### Taxonomy-aware feature gating (the link between taxonomy and features)
After taxonomy classification, the `FeatureRegistry` restricts which features run:
- A document classified as "Opinion" triggers: Rhetorical (P8), Fallacy (P9), Sentiment (P6), Framing (P7)
- A document classified as "News Report" triggers: Factuality (P10), Entity (P5), Temporal (P11)
- A document classified as "Scientific" triggers: Logical Fallacy (P9), Factuality (P10), Citation quality
This means the taxonomy controls which scoring math runs on each document — implement in `FeatureRegistry` before calling `FeatureExtractor`.

---

## Classification tiers — how rule + ML combine

### Tier 1: Rule-based (primary, always runs)
- Lexicons + regex + spaCy dependency patterns in `rules_engine.py`
- If confidence ≥ threshold → assign category, skip ML for that sentence
- Reads `taxonomy_v1.yaml` for category definitions and rule sets

### Tier 2: ML classifier (secondary, for ambiguous cases)
- Classical ML (LogReg / SVM) or frozen compact transformer via ONNX
- Only invoked when rule engine confidence < threshold
- Model is versioned, seed-fixed, never updated online

### Tier 3: HybridRouter merge
- Combines tier-1 and tier-2 results using the formula above
- Strict precedence order defined in config
- Same input → same output, always

Routing pseudocode (implement exactly this logic in `hybrid_router.py`):
```python
if rule_confidence >= threshold:          # threshold from pipeline_v1.yaml
    return rule_result
else:
    blended = α * conf_rules + (1 - α) * conf_ml
    return assign_labels(blended, thresholds)
```

---

## Output contract — what `PostProcessor` must produce

The JSON returned to the backend must include (per the proposal):
- **Document-level scores** — one score per taxonomy category
- **Sentence-level classifications** — list of `{sentence, labels, confidences}`
- **Text spans** — character offsets for each classified sentence (for frontend highlighting)
- **Metadata** — taxonomy version, scoring version, pipeline version, run timestamp
- **Multi-label support** — each sentence can carry multiple category labels

This output must validate against `data_schema/output_schema.json` (currently a placeholder — needs to be written).

Target output shape (implement this exactly in `PostProcessor.to_output_schema()`):
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
      "confidences": {
        "bias": 0.91,
        "rhetorical": 0.67
      }
    }
  ]
}
```

---

## PipelineRunner — target design for `main.py`

`process_document()` and `run_pipeline()` are currently `pass`. The intended implementation is a `PipelineRunner` class that wires all stages via constructor injection. Every consumer (API, batch, Airflow) calls `runner.run(doc)`.

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
                         ontology
                     )
        scores     = self.score.score(labels, features)
        return self.post.to_output_schema(doc, normalized, sentences, labels, scores)
```

`api/service.py` calls `runner.run(ingest(request))`.
`batch_processing/classify_batch.py` maps `runner.run` over a corpus.
`airflow_dags/` triggers the batch scripts.

Use OOP throughout `nlp_pipeline/` — each stage is a class. Use plain functions only for stateless utilities (`deterministic_utils.py`, `taxonomy_loader.py`).

---

## Recommended build order

Work through these roughly in order — each stage depends on the one above it.

1. **`nlp_pipeline/shared_types.py`** — Convert `NormalizedDocument` and `Sentence` to proper dataclasses. Add `Features`, `ArgumentSpan`, `Classification`, `ScoredDocument` while here. These are the contracts every stage signs.
2. **Fix `InputRouter`** — Instantiate real readers in constructor; wire `_handle_file_path()` to actually call `reader.read(file_path)`.
3. **`nlp_pipeline/deterministic_utils.py`** — Implement `set_global_seeds`, `hash_to_document_id`, `compute_config_hashes`.
4. **`conf/taxonomy_v1.yaml`** — Design and fill the taxonomy structure. Everything downstream (OntologyGraph, FeatureRegistry, RuleEngine) depends on this.
5. **`taxonomy_tools/taxonomy_loader.py`** + **`nlp_pipeline/ontology_graph.py`** — Load the taxonomy, build the networkx graph.
6. **`io_adapters/storage_clients.py`** (Bronze/Silver zone) — Implement `JSONLWriter` for Bronze zone, `ParquetWriter` for Silver/Gold zones, using the canonical Parquet schema above. `StorageClientFactory` wires them.
7. **`nlp_pipeline/preprocessing.py`** — Implement `TextProcessor.normalize()` using the existing imports (re, unicodedata). Output → Silver Parquet.
8. **`nlp_pipeline/segmentation.py`** — Implement `SentenceSegmenter.segment()` using pysbd (already imported).
9. **Argument Mining stage** — New module needed: `nlp_pipeline/argument_miner.py`. Implement `ArgumentMiner.extract(sentences)` returning claim/premise/support spans. Sits between segmentation and feature extraction.
10. **Feature Registry** — New module needed: `nlp_pipeline/feature_registry.py`. Implements taxonomy-aware feature gating. Consult `OntologyGraph` to decide which of the 13 feature layers run.
11. **`nlp_pipeline/features.py`** — Implement all 13 feature extraction layers in priority order (Phase 1 first). Fix typos: `Bais` → `Bias`, `Sentiment_Subjecivity` → `Sentiment_Subjectivity`.
12. **`conf/scoring_v1.yaml`** — Design scoring weights for all formulas above (w_c, w_f, disruption factors, w1..w5 for Factuality).
13. **`nlp_pipeline/rules_engine.py`** — Implement rule-based classification. Rules are taxonomy-aware; use OntologyGraph for threshold calibration.
14. **`nlp_pipeline/scoring_engine.py`** — Implement all 5 scoring formulas above. Reads `scoring_v1.yaml`.
15. **`nlp_pipeline/hybrid_router.py`** — Implement merge logic.
16. **`nlp_pipeline/postprocessing.py`** — Implement output schema builder. Write Gold zone Parquet. Fill `data_schema/output_schema.json` alongside this.
17. **`main.py`** — Implement `PipelineRunner` class (see below). Fix hard-coded config paths (use env var or CLI arg).
18. **ML path** (parallel after step 11) — `embeddings_onnx.py`, `vector_index.py`, `ml_classifier.py` need actual ONNX model files in `models/`.
19. **`api/service.py`** + **`api/models.py`** — FastAPI app. Ingestion → pipeline → Gold Parquet → SQL Serving DB.
20. **Tests** — implement everything in `tests/`.
21. **Batch processing** — `batch_processing/preprocess_ray.py`, `preprocess_spark.py`, `classify_batch.py`.
