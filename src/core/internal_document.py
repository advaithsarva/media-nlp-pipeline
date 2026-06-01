from dataclasses import dataclass, field, asdict
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum
import hashlib
import json


class SourceType(Enum):
    """All possible input sources"""
    FILE_TXT = "file_txt"
    FILE_PDF = "file_pdf"
    FILE_DOCX = "file_docx"
    FILE_CSV = "file_csv"
    FILE_JSON = "file_json"
    FILE_JSONL = "file_jsonl"
    FILE_HTML = "file_html"
    FILE_XML = "file_xml"
    FILE_MARKDOWN = "file_markdown"
    FILE_PARQUET = "file_parquet"
    FILE_IMAGE = "file_image"
    FILE_ARCHIVE = "file_archive"
    API_REST = "api_rest"
    API_GRAPHQL = "api_graphql"
    ELASTICSEARCH = "elasticsearch"
    KAFKA = "kafka"
    S3 = "s3"
    DATABASE_SQL = "database_sql"
    DATABASE_NOSQL = "database_nosql"
    WEB_SCRAPER = "web_scraper"
    STREAM = "stream"


class ProcessingStatus(Enum):
    """Document processing status"""
    INGESTED = "ingested"
    VALIDATED = "validated"
    PROCESSED = "processed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class InternalDocument:
    """
    THE CORE ABSTRACTION - Only this flows into NLP pipeline
    
    This is the contract between ingestion and processing.
    Everything must be normalized to this format.
    """
    
    # Primary fields (REQUIRED)
    document_id: str
    text: str
    source_type: SourceType
    
    # Metadata (REQUIRED)
    ingestion_timestamp: str
    source_metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Optional fields
    language: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    
    # Processing metadata
    processing_status: ProcessingStatus = ProcessingStatus.INGESTED
    processing_metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Structural data (attached but not processed by NLP unless needed)
    tables: List[Any] = field(default_factory=list)
    images: List[Dict] = field(default_factory=list)
    sections: List[Dict] = field(default_factory=list)
    
    # Quality indicators
    quality_score: Optional[float] = None
    quality_flags: Dict[str, bool] = field(default_factory=dict)
    
    # Statistics (for monitoring)
    char_count: int = 0
    word_count: int = 0
    line_count: int = 0
    
    def __post_init__(self):
        """Calculate statistics if not provided"""
        if self.text:
            if self.char_count == 0:
                self.char_count = len(self.text)
            if self.word_count == 0:
                self.word_count = len(self.text.split())
            if self.line_count == 0:
                self.line_count = len(self.text.split('\n'))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage/serialization"""
        data = asdict(self)
        data['source_type'] = self.source_type.value
        data['processing_status'] = self.processing_status.value
        return data
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    def to_jsonl(self) -> str:
        """Convert to JSONL format (single line)"""
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'InternalDocument':
        """Create from dictionary"""
        data['source_type'] = SourceType(data['source_type'])
        data['processing_status'] = ProcessingStatus(data['processing_status'])
        return cls(**data)



