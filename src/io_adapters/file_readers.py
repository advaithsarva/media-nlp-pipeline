import csv
import json
from pathlib import Path
import pdfplumber,fitz,pymupdf
import docx
import pptx
import chardet
from typing import Dict, Any, List
from nlp_pipeline.deterministic_utils import hash_to_document_id
from io_adapters.shared_types import InternalDocument

class PDFReader:
    def receive(self,file_bytes:bytes,file_name:str):
        pass
    def fetch(self,file_path:str):
        pass
class DocsReader:
    def receive(self,file_bytes:bytes,file_name:str):
        pass
    def fetch(self,file_path:str):
        pass
class PPTReader:
    def receive(self,file_bytes:bytes,file_name:str):
        pass
    def fetch(self,file_path:str):
        pass
class TxtReader:
    def receive(self,file_bytes:bytes,file_name:str):
        pass
    def fetch(self,file_path:str):
        pass
class CSVReader:
    def __init__(self,csv_config:Dict[str,Any]):
        self.text_column=csv_config.get("text_column")
    def fetch_many(self,file_path:str)-> List:
        pass

class JSONReader:
    def __init__(self,csv_config:Dict[str,Any]):
        self.text_column=csv_config.get("text_column")
    def fetch_many(self,file_path:str)-> List:
        pass

class ImageReader:
    def __init__(self):
        pass
