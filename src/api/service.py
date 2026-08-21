"""HTTP service. The backend calls this instead of importing the pipeline.

Three endpoints:

    GET  /health          is it up, and which taxonomy and config is it running
    POST /analyze         one article in, one report out
    POST /analyze/batch   several at once

Run it with:

    .venv\\Scripts\\python.exe -m uvicorn api.service:app --app-dir src --reload

The pipeline is built **once**, when the app starts, and reused for every request. Building
it per request would recompile every regex and reread the schema on each call, and would
also re-seed the random generators mid-flight.
"""

from fastapi import FastAPI, HTTPException

from api.models import (
    AnalyzeRequest,
    AnalyzeResponse,
    BatchAnalyzeRequest,
    BatchAnalyzeResponse,
    HealthResponse,
)
from core.exceptions import IngestionError
from main import PipelineRunner


def create_app(conf_dir=None) -> FastAPI:
    app = FastAPI(
        title="Media NLP Pipeline",
        version="1.0.0",
        description=(
            "Deterministic media analysis. Every finding is a verbatim substring of the "
            "submitted text at the character offsets given, and the same text always "
            "produces the same report."
        ),
    )

    runner = PipelineRunner(conf_dir) if conf_dir else PipelineRunner()

    @app.get("/health", response_model=HealthResponse)
    def health():
        return {
            "status": "ok",
            "taxonomy_version": runner.taxonomy.version,
            "categories": runner.taxonomy.ids(),
            "config_hashes": runner.config_hashes,
        }

    @app.post("/analyze", response_model=AnalyzeResponse)
    def analyze(request: AnalyzeRequest):
        payload = request.model_dump()
        # the router treats a bare string as a file path when a file of that name exists,
        # so text arriving over HTTP is wrapped in a dict to stay unambiguous
        payload["source_type"] = "api_rest"
        try:
            return runner.process_document(payload)
        except IngestionError as error:
            # the caller sent something unusable -- their problem, so 400
            raise HTTPException(status_code=400, detail=str(error))
        except ValueError as error:
            # the pipeline produced something that failed its own checks -- our problem
            raise HTTPException(status_code=500, detail=str(error))

    @app.post("/analyze/batch", response_model=BatchAnalyzeResponse)
    def analyze_batch(request: BatchAnalyzeRequest):
        if not request.documents:
            raise HTTPException(status_code=400, detail="no documents supplied")
        results = []
        for document in request.documents:
            payload = document.model_dump()
            payload["source_type"] = "api_rest"
            try:
                results.append(runner.process_document(payload))
            except IngestionError as error:
                raise HTTPException(status_code=400, detail=str(error))
        return {"results": results}

    return app


# uvicorn looks for a module-level object, so the app is created on import.
app = create_app()
