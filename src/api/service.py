'''FastAPI app: defines endpoints like POST /analyze, POST /batch/analyze.
It imports run_pipeline or similar from nlp_pipeline and returns JSON.'''
from fastapi import FastAPI, UploadFile, File
from typing import Dict, Any
from api.models import AnalyzeRequest,AnalyzeResponse
from main import load_configs,build_services,process_document
def create_app():
    pass