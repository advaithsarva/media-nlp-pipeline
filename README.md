# NLPpipeline
A deterministic, configuration-driven NLP processing framework designed for high-integrity media and document analysis.  
The system emphasizes reproducibility, auditability, modularity, and strict schema-validated outputs.

---

## 1. Overview
`NLPpipeline` transforms raw documents into structured, taxonomy-mapped, and score-annotated outputs.  
It supports:

- Deterministic rule-based classification  
- Config-driven taxonomy/scoring logic  
- Optional ML fallback classification  
- Hybrid deterministic routing  
- Strict I/O schema validation  
- FastAPI service layer  
- Airflow-orchestrated batch runs  
- Optional CPU/GPU acceleration paths  

The pipeline is designed for environments where **reproducibility, consistency, and explainability** are mandatory.

---

## 2. Architecture

```mermaid
flowchart TD
    A[Input Document] --> B[Preprocessing]
    B --> C[Sentence Segmentation]
    C --> D[Rule Engine]
    C --> E[ML Classifier]

    D --> H[Hybrid Router]
    E --> H[Hybrid Router]

    H --> F[Scoring Engine]
    F --> G[Postprocessing + Output Schema Validation]

    G --> J[Final Structured JSON]

    subgraph Config
        T[taxonomy_v1.yaml]
        S[scoring_v1.yaml]
        P[pipeline.yml]
    end

    T --> D
    S --> F
    P --> H

NLPpipeline/
├── Dockerfile
├── pyproject.toml
├── requirements-dev.txt
│
├── config/
│   ├── taxonomy_v1.yaml
│   ├── scoring_v1.yaml
│   └── pipeline.yml
│
├── data_schemas/
│   ├── input_schema.json
│   └── output_schema.json
│
├── src/
│   ├── nlp_pipeline/
│   │   ├── preprocessing.py
│   │   ├── segmentation.py
│   │   ├── features.py
│   │   ├── rules_engine.py
│   │   ├── ml_classifier.py
│   │   ├── hybrid_router.py
│   │   ├── ontology_graph.py
│   │   ├── scoring_engine.py
│   │   ├── postprocessing.py
│   │   ├── deterministic_utils.py
│   │   └── gpu_router.py
│   │
│   ├── taxonomy_tools/
│   │   ├── taxonomy_loader.py
│   │   ├── taxonomy_versioning.py
│   │   └── taxonomy_suggestions.py
│   │
│   ├── io_adapters/
│   │   ├── ingest_api_client.py
│   │   └── storage_client.py
│   │
│   ├── api/
│   │   ├── service.py
│   │   └── models.py
│   │
│   ├── core_accelerators/
│   │   ├── text_ops.cpp
│   │   ├── text_ops.h
│   │   ├── nlp_accel.cpp
│   │   ├── bindings.cpp
│   │   └── CMakeLists.txt
│   │
│   └── gpu_support/
│       ├── cuda_ops.cu
│       ├── cuda_ops.h
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
└── notebooks/
    ├── 01_exploration.ipynb
    ├── 02_rules_design.ipynb
    ├── 03_ml_baselines.ipynb
    └── 04_taxonomy_suggestions.ipynb

4. Determinism Model

The system enforces strict reproducibility through:

Fixed PRNG seeds (Python, NumPy, sklearn)

Ordered rule evaluation

Version-pinned taxonomy and scoring configs

Deterministic segmentation overrides

Schema-validated outputs

No stochastic operations in rule or segmentation pipelines

Outputs must be byte-identical across runs and environments.

5. Local Development
Create Environment
python -m venv pipe
source pipe/bin/activate        # Windows: .\pipe\Scripts\activate
pip install -r requirements-dev.txt

Run the API
uvicorn src.api.service:app --reload


API Docs:

http://localhost:8000/docs

6. Docker Execution
Build
docker build -t nlp-pipeline .

Run
docker run -p 8000:8000 nlp-pipeline

7. Airflow Integration

airflow_dags/media_nlp_batch_dag.py provides orchestration for:

Ingestion

Batch classification

Scoring

Storage handoff

Supports LocalExecutor and cloud-managed Airflow.

8. Testing & QA
pytest -q
flake8
black --check .


Test suite validates:

Preprocessing equivalence

Segmentation boundary stability

Rule engine determinism

Score reproducibility

API schema conformance

Output JSON contract

9. Extension Points

The pipeline is designed for controlled evolution:

Area	Examples of Extensions
Rule Engine	dynamic rule loading, multi-rule strategies
ML Classifier	transformers, zero-shot classification
GPU Router	CUDA-powered feature extraction
Ontology Graph	hierarchical inference, DAG scoring
I/O Adapters	S3/GCS/SQL connectors
Scoring Engine	non-linear scoring operators
10. Operational Considerations

No runtime external dependencies unless explicitly configured

Fully containerized execution path

Config changes require version increments

Suitable for air-gapped or compliance environments

Determinism preserved across CPU/GPU execution paths