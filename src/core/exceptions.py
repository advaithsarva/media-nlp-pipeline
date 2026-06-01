class IngestionError(Exception):
    """Base exception for ingestion errors"""
    pass


class UnsupportedFileTypeError(IngestionError):
    """Raised when file type is not supported"""
    pass


class NoTextFoundError(IngestionError):
    """Raised when no text content could be extracted"""
    pass


class InvalidInputError(IngestionError):
    """Raised when input format is invalid"""
    pass


class SourceConnectionError(IngestionError):
    """Raised when cannot connect to source"""
    pass


class ExtractionError(IngestionError):
    """Raised when content extraction fails"""
    pass

