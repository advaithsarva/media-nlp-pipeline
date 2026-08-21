"""Request and response shapes for the HTTP API.

These are pydantic models. Pydantic checks incoming JSON against the declared types and
rejects anything that does not fit, before the request reaches any pipeline code -- so a
caller sending a number where text belongs gets a clear 422 rather than a crash halfway
through segmentation.

They mirror data_schema/output_schema.json. The JSON Schema is the contract of record --
it is what `PostProcessor.validate` enforces on every run, API or not. These classes exist
so FastAPI can also publish that contract as OpenAPI docs at /docs.
"""

from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    text: str = Field(min_length=1, description="The article text to analyse.")
    title: Optional[str] = None
    author: Optional[str] = None
    language: Optional[str] = None


class Finding(BaseModel):
    """One piece of evidence. `text` is always an exact substring of the submitted article."""
    category: str
    rule_id: str
    sentence_id: int
    text: str
    start_char: int
    end_char: int
    confidence: float


class CategoryScore(BaseModel):
    count: int
    raw: float
    score: float
    # False until the detectors have measured precision against a labelled set.
    calibrated: bool


class DocumentStats(BaseModel):
    char_count: int
    word_count: int
    sentence_count: int


class DocumentSource(BaseModel):
    type: str
    title: Optional[str] = None
    author: Optional[str] = None
    language: Optional[str] = None


class AnalyzeResponse(BaseModel):
    schema_version: str
    document_id: str
    source: DocumentSource
    config_hashes: Dict[str, str]
    stats: DocumentStats
    findings: List[Finding]
    category_scores: Dict[str, CategoryScore]
    # Deliberately nullable and currently always null -- see conf/scoring_v1.yaml.
    composite: Optional[float] = None
    notes: List[str] = []


class BatchAnalyzeRequest(BaseModel):
    documents: List[AnalyzeRequest]


class BatchAnalyzeResponse(BaseModel):
    results: List[AnalyzeResponse]


class HealthResponse(BaseModel):
    status: str
    taxonomy_version: str
    categories: List[str]
    config_hashes: Dict[str, str]
