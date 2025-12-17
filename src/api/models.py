'''Pydantic models for request/response schemas used by FastAPI.
Ties directly to input_schema.json and output_schema.json.'''
from typing import List,Optional,Dict,Any
from pydantic import BaseModel
class AnalyzeRequest(BaseModel):
    pass
class SentenceLabel(BaseModel):
    pass
class DocumentScore(BaseModel):
    pass
class AnalyzeResponse(BaseModel):
    pass