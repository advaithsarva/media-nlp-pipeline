from pathlib import Path
import logging
from typing import Iterator, Union
from typing import Dict, Any, Optional
from io_adapters.file_readers import (
    TxtReader,
    PDFReader,
    DocsReader,
    CSVReader,
    JSONReader,
    JSONLReader,
    HTMLReader,
    XMLReader,
    MarkdownReader,
)
from datetime import datetime
import hashlib
import json
from core.internal_document import InternalDocument, SourceType, ProcessingStatus
from core.exceptions import (
    IngestionError,
    UnsupportedInputError,
    SourceConnectionError,
    UnsupportedFileTypeError,
    InvalidInputError,
    NoTextFoundError,
    ExtractionError,
)
from io_adapters.ingest_clients import (
    APIClient,
    ESClient,
    KafkaClient,
    S3Client,
)


class InputRouter:
    """
    Responsibilities:
    1. Determine input type (file, API, stream, etc.)
    2. Route to appropriate reader/client
    3. Normalize raw records to InternalDocument
    4. Handle errors gracefully
    5. Provide unified interface for all sources
    
    Usage:
        router = InputRouter(config)
        
        # Push mode (someone gives us input)
        doc = router.route_push_input(file_path="/path/to/file.pdf")
        
        # Pull mode (we fetch from source)
        for doc in router.route_pull_source(source_type="elasticsearch"):
            process(doc)
    """
    
    def __init__(self, config: Dict[str, Any], output_dir: str = "./ingestion_output"):
        self.config = config
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self.logger = logging.getLogger('InputRouter')
        self.logger.setLevel(logging.INFO)
        
        # Initialize file readers
        self.file_readers = self._initialize_file_readers()
        
        # Initialize source clients
        self.ingest_clients = self._initialize_source_clients()
        
        self.logger.info("InputRouter initialized")
    
    def _initialize_file_readers(self) -> Dict[str, Any]:
        """Initialize all file readers"""
        # These would import from your file_readers.py
        # For now, using placeholder that you'll replace
        
        return {
            '.txt': 'TxtReader()',
            '.text': 'TxtReader()',
            '.md': 'MarkdownReader()',
            '.markdown': 'MarkdownReader()',
            '.pdf': 'PDFReader()',
            '.docx': 'DocsReader()',
            '.doc': 'DocsReader()',
            '.csv': 'CSVReader()',
            '.tsv': 'CSVReader()',
            '.json': 'JSONReader()',
            '.jsonl': 'JSONLReader()',
            '.ndjson': 'JSONLReader()',
            '.html': 'HTMLReader()',
            '.htm': 'HTMLReader()',
            '.xml': 'XMLReader()',
            '.parquet': 'ParquetReader()',
            '.png': 'ImageReader()',
            '.jpg': 'ImageReader()',
            '.jpeg': 'ImageReader()',
            '.tiff': 'ImageReader()',
            '.bmp': 'ImageReader()',
            '.zip': 'ArchiveReader()',
            '.tar': 'ArchiveReader()',
            '.gz': 'ArchiveReader()',
            '.tgz': 'ArchiveReader()'
        }
    
    def _initialize_source_clients(self) -> Dict[str, Any]:
        """Initialize all source clients"""
        return {
            'api': 'APIClient()',
            'elasticsearch': 'ESClient()',
            'kafka': 'KafkaClient()',
            's3': 'S3Client()',
            'scraper': 'ScraperClient()',
            'sql': 'SQLClient()',
            'mongodb': 'MongoClient()'
        }
    
    # PUSH MODE - Someone gives us input
    
    def route_push_input(self, 
                        file_path: Optional[str] = None,
                        file_bytes: Optional[bytes] = None,
                        api_payload: Optional[Dict] = None,
                        es_hit: Optional[Dict] = None,
                        kafka_message: Optional[Dict] = None,
                        raw_text: Optional[str] = None) -> InternalDocument:
        """
        PUSH MODE: Route any input type to appropriate handler
        
        Args:
            file_path: Path to file on disk
            file_bytes: Raw file bytes (with filename/extension hint)
            api_payload: Data from API response
            es_hit: Elasticsearch hit document
            kafka_message: Kafka message
            raw_text: Plain text input
        
        Returns:
            InternalDocument ready for NLP pipeline
        """
        try:
            # Route based on input type
            if file_path is not None:
                return self._handle_file_path(file_path)
            
            elif file_bytes is not None:
                return self._handle_file_bytes(file_bytes)
            
            elif api_payload is not None:
                return self._handle_api_payload(api_payload)
            
            elif es_hit is not None:
                return self._handle_es_hit(es_hit)
            
            elif kafka_message is not None:
                return self._handle_kafka_message(kafka_message)
            
            elif raw_text is not None:
                return self._handle_raw_text(raw_text)
            
            else:
                raise InvalidInputError("No valid input provided")
        
        except Exception as e:
            self.logger.error(f"Push input routing failed: {e}", exc_info=True)
            raise IngestionError(f"Failed to route input: {e}")
    
    # PULL MODE - We fetch from source
    
    
    def route_pull_source(self, 
                         source_type: str,
                         source_config: Optional[Dict] = None) -> Iterator[InternalDocument]:
        """
        PULL MODE: Fetch from external source and yield documents
        
        Args:
            source_type: Type of source (elasticsearch, kafka, s3, api, etc.)
            source_config: Configuration for the source
        
        Yields:
            InternalDocument for each record from source
        """
        if source_config is None:
            source_config = self.config.get('sources', {}).get(source_type, {})
        
        self.logger.info(f"Starting pull from source: {source_type}")
        
        try:
            if source_type not in self.ingest_clients:
                raise IngestionError(f"Unsupported source type: {source_type}")
            
            client = self.ingest_clients[source_type]
            
            # Fetch records from source (client-specific)
            for raw_record in self._fetch_from_source(client, source_config):
                try:
                    doc = self._to_internal_document(raw_record, source_type)
                    yield doc
                
                except Exception as e:
                    self.logger.error(f"Failed to process record: {e}")
                    # Log to errors but continue processing
                    self._log_error(raw_record, e)
                    continue
        
        except Exception as e:
            self.logger.error(f"Pull source failed: {e}", exc_info=True)
            raise SourceConnectionError(f"Failed to fetch from {source_type}: {e}")
    
    # FILE HANDLING LOGIC
    
    
    def _handle_file_path(self, file_path: str) -> InternalDocument:
        """Handle file from disk path"""
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Determine file type
        extension = path.suffix.lower()
        
        # Handle special cases
        if path.name.endswith('.tar.gz'):
            extension = '.tar.gz'
            reader_key = '.tar'
        else:
            reader_key = extension
        
        # Get appropriate reader
        if reader_key not in self.file_readers:
            raise UnsupportedFileTypeError(f"Unsupported file type: {extension}")
        
        self.logger.info(f"Processing file: {file_path} (type: {extension})")
        
        # Read file (this would call your actual reader)
        # reader = self.file_readers[reader_key]
        # raw_record = reader.read(file_path)
        
        # For demonstration, creating mock raw_record
        raw_record = self._mock_file_read(file_path, extension)
        
        # Convert to InternalDocument
        return self._to_internal_document(raw_record, f"file_{extension.strip('.')}")
    
    def _handle_file_bytes(self, file_bytes: bytes, 
                          filename: str = "unknown",
                          mime_type: Optional[str] = None) -> InternalDocument:
        """Handle file from bytes (e.g., uploaded file)"""
        # Write to temp file and process
        import tempfile
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(filename).suffix) as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name
        
        try:
            return self._handle_file_path(tmp_path)
        finally:
            Path(tmp_path).unlink()
    
    def _handle_raw_text(self, text: str) -> InternalDocument:
        """Handle raw text input"""
        doc_id = self._generate_document_id(text)
        
        return InternalDocument(
            document_id=doc_id,
            text=text,
            source_type=SourceType.FILE_TXT,
            ingestion_timestamp=datetime.now().isoformat(),
            source_metadata={'input_method': 'raw_text'},
            processing_status=ProcessingStatus.INGESTED
        )
    
    
    # API/STREAM HANDLING LOGIC
    
    
    def _handle_api_payload(self, payload: Dict) -> InternalDocument:
        """Handle API response payload"""
        # Extract text from common API response formats
        text = self._extract_text_from_payload(payload)
        doc_id = payload.get('id') or self._generate_document_id(text)
        
        return InternalDocument(
            document_id=str(doc_id),
            text=text,
            source_type=SourceType.API_REST,
            ingestion_timestamp=datetime.now().isoformat(),
            source_metadata=payload,
            title=payload.get('title'),
            author=payload.get('author'),
            processing_status=ProcessingStatus.INGESTED
        )
    
    def _handle_es_hit(self, hit: Dict) -> InternalDocument:
        """Handle Elasticsearch hit"""
        source = hit.get('_source', {})
        text = self._extract_text_from_payload(source)
        
        return InternalDocument(
            document_id=hit.get('_id', self._generate_document_id(text)),
            text=text,
            source_type=SourceType.ELASTICSEARCH,
            ingestion_timestamp=datetime.now().isoformat(),
            source_metadata={
                'index': hit.get('_index'),
                'score': hit.get('_score'),
                'source': source
            },
            processing_status=ProcessingStatus.INGESTED
        )
    
    def _handle_kafka_message(self, message: Dict) -> InternalDocument:
        """Handle Kafka message"""
        value = message.get('value', {})
        text = self._extract_text_from_payload(value)
        
        return InternalDocument(
            document_id=self._generate_document_id(text),
            text=text,
            source_type=SourceType.KAFKA,
            ingestion_timestamp=datetime.now().isoformat(),
            source_metadata={
                'topic': message.get('topic'),
                'partition': message.get('partition'),
                'offset': message.get('offset'),
                'timestamp': message.get('timestamp'),
                'value': value
            },
            processing_status=ProcessingStatus.INGESTED
        )
    
    # CONVERSION TO INTERNAL DOCUMENT (CRITICAL)
    
    
    def _to_internal_document(self, raw_record: Dict[str, Any], 
                             source_hint: str) -> InternalDocument:
        """
        CRITICAL METHOD: Convert any raw record to InternalDocument
        
        This is where normalization happens.
        All inputs must pass through here.
        """
        
        # Extract text (with fallback strategy)
        text = self._extract_text(raw_record)
        
        # Generate or extract document ID
        doc_id = raw_record.get('file_hash_sha256') or \
                 raw_record.get('document_id') or \
                 self._generate_document_id(text)
        
        # Determine source type
        source_type = self._determine_source_type(raw_record, source_hint)
        
        # Extract optional fields
        language = raw_record.get('language')
        title = raw_record.get('title') or raw_record.get('file_name')
        author = raw_record.get('author') or raw_record.get('document_properties', {}).get('author')
        
        # Extract structural data
        tables = raw_record.get('tables', [])
        images = raw_record.get('images', [])
        sections = raw_record.get('sections', [])
        
        # Quality indicators
        quality_flags = raw_record.get('quality_indicators', {})
        
        # Create InternalDocument
        doc = InternalDocument(
            document_id=doc_id,
            text=text,
            source_type=source_type,
            ingestion_timestamp=raw_record.get('processed_timestamp') or datetime.now().isoformat(),
            source_metadata=raw_record,
            language=language,
            title=title,
            author=author,
            tables=tables,
            images=images,
            sections=sections,
            quality_flags=quality_flags,
            processing_status=ProcessingStatus.INGESTED
        )
        
        self.logger.debug(f"Created InternalDocument: {doc_id} ({source_type.value})")
        
        return doc
    
    def _extract_text(self, raw_record: Dict[str, Any]) -> str:
        """
        Extract text from raw record with fallback strategy
        
        Priority:
        1. full_raw_text (from PDFs, DOCX)
        2. extracted_text (from HTML, XML)
        3. raw_content (from TXT)
        4. text field (generic)
        5. Concatenate from structured data
        """
        
        # Try common text fields
        for field in ['full_raw_text', 'extracted_text', 'raw_content', 'text', 'content', 'body']:
            if field in raw_record and raw_record[field]:
                text = raw_record[field]
                if isinstance(text, str) and text.strip():
                    return text.strip()
        
        # Try paragraphs
        if 'paragraphs' in raw_record and raw_record['paragraphs']:
            paragraphs = raw_record['paragraphs']
            if isinstance(paragraphs, list):
                return '\n\n'.join(str(p) for p in paragraphs if p)
        
        # Try OCR results (images)
        if 'ocr_results' in raw_record:
            ocr = raw_record['ocr_results']
            if isinstance(ocr, dict) and 'extracted_text' in ocr:
                return ocr['extracted_text']
        
        # Try raw_data (CSV, JSON)
        if 'raw_data' in raw_record:
            data = raw_record['raw_data']
            if isinstance(data, str):
                return data
            elif isinstance(data, (list, dict)):
                return json.dumps(data, ensure_ascii=False, indent=2)
        
        # Last resort: stringify entire record
        if raw_record:
            return json.dumps(raw_record, ensure_ascii=False, indent=2)
        
        raise NoTextFoundError("Could not extract text from record")
    
    def _determine_source_type(self, raw_record: Dict, source_hint: str) -> SourceType:
        """Determine SourceType from raw record and hint"""
        
        # Check reader_class first
        reader_class = raw_record.get('reader_class', '')
        
        if 'PDFReader' in reader_class or 'pdf' in source_hint.lower():
            return SourceType.FILE_PDF
        elif 'DocsReader' in reader_class or 'docx' in source_hint.lower():
            return SourceType.FILE_DOCX
        elif 'TxtReader' in reader_class or 'txt' in source_hint.lower():
            return SourceType.FILE_TXT
        elif 'CSVReader' in reader_class or 'csv' in source_hint.lower():
            return SourceType.FILE_CSV
        elif 'JSONReader' in reader_class or 'json' in source_hint.lower():
            return SourceType.FILE_JSON
        elif 'JSONLReader' in reader_class or 'jsonl' in source_hint.lower():
            return SourceType.FILE_JSONL
        elif 'HTMLReader' in reader_class or 'html' in source_hint.lower():
            return SourceType.FILE_HTML
        elif 'XMLReader' in reader_class or 'xml' in source_hint.lower():
            return SourceType.FILE_XML
        elif 'MarkdownReader' in reader_class or 'markdown' in source_hint.lower():
            return SourceType.FILE_MARKDOWN
        elif 'ParquetReader' in reader_class or 'parquet' in source_hint.lower():
            return SourceType.FILE_PARQUET
        elif 'ImageReader' in reader_class or any(img in source_hint.lower() for img in ['png', 'jpg', 'jpeg']):
            return SourceType.FILE_IMAGE
        elif 'ArchiveReader' in reader_class or any(arc in source_hint.lower() for arc in ['zip', 'tar', 'gz']):
            return SourceType.FILE_ARCHIVE
        elif 'api' in source_hint.lower():
            return SourceType.API_REST
        elif 'elasticsearch' in source_hint.lower():
            return SourceType.ELASTICSEARCH
        elif 'kafka' in source_hint.lower():
            return SourceType.KAFKA
        elif 's3' in source_hint.lower():
            return SourceType.S3
        else:
            return SourceType.FILE_TXT  # Default fallback
    
    
    # HELPER METHODS
    
    
    def _extract_text_from_payload(self, payload: Dict) -> str:
        """Extract text from generic payload (API, ES, Kafka)"""
        # Try common fields
        for field in ['text', 'content', 'body', 'message', 'description', 'data']:
            if field in payload and payload[field]:
                return str(payload[field])
        
        # Stringify entire payload if no text field found
        return json.dumps(payload, ensure_ascii=False, indent=2)
    
    def _generate_document_id(self, text: str) -> str:
        """Generate deterministic document ID from text"""
        return hashlib.sha256(text.encode('utf-8')).hexdigest()
    
    def _fetch_from_source(self, client: Any, config: Dict) -> Iterator[Dict]:
        """Fetch records from source client (placeholder)"""
        # This would call the actual client fetch method
        # For now, return empty iterator
        return iter([])
    
    def _log_error(self, raw_record: Dict, error: Exception):
        """Log error to errors.jsonl"""
        error_file = self.output_dir / "errors.jsonl"
        
        error_entry = {
            'timestamp': datetime.now().isoformat(),
            'error': str(error),
            'error_type': type(error).__name__,
            'record': raw_record
        }
        
        with open(error_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(error_entry, ensure_ascii=False) + '\n')
    
    def _mock_file_read(self, file_path: str, extension: str) -> Dict[str, Any]:
        """Mock file reading for demonstration"""
        # This simulates what your actual readers would return
        return {
            'file_path': file_path,
            'file_name': Path(file_path).name,
            'file_extension': extension,
            'file_hash_sha256': 'mock_hash_12345',
            'reader_class': f'{extension.strip(".")}Reader',
            'processed_timestamp': datetime.now().isoformat(),
            'full_raw_text': f'Mock content from {file_path}',
            'file_size_bytes': 1024,
            'mime_type': f'application/{extension.strip(".")}'
        }
    
    
    # BATCH PROCESSING
    
    
    def process_directory(self, directory: str, 
                         recursive: bool = True,
                         output_file: str = "internal_documents.jsonl") -> Dict[str, Any]:
        """
        Process all files in directory and output InternalDocuments to JSONL
        
        Returns:
            Statistics dictionary
        """
        directory = Path(directory)
        
        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")
        
        # Find all files
        if recursive:
            files = [f for f in directory.rglob('*') if f.is_file()]
        else:
            files = [f for f in directory.glob('*') if f.is_file()]
        
        self.logger.info(f"Found {len(files)} files to process")
        
        output_path = self.output_dir / output_file
        
        stats = {
            'total': len(files),
            'success': 0,
            'failed': 0,
            'skipped': 0
        }
        
        with open(output_path, 'w', encoding='utf-8') as out_file:
            for file_path in files:
                try:
                    doc = self.route_push_input(file_path=str(file_path))
                    
                    # Write to JSONL
                    out_file.write(doc.to_jsonl() + '\n')
                    
                    stats['success'] += 1
                    self.logger.info(f"✅ {file_path.name}")
                
                except UnsupportedFileTypeError:
                    stats['skipped'] += 1
                    self.logger.info(f"⚠️  {file_path.name} (unsupported)")
                
                except Exception as e:
                    stats['failed'] += 1
                    self.logger.error(f"❌ {file_path.name}: {e}")
                    self._log_error({'file_path': str(file_path)}, e)
        
        self.logger.info(f"Processing complete: {stats['success']}/{stats['total']} successful")
        self.logger.info(f"Output: {output_path}")
        
        return stats