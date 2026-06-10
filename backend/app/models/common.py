from enum import Enum


class SourceType(str, Enum):
    PDF = "PDF"
    DOCX = "DOCX"
    HTML = "HTML"
    CONFLUENCE = "CONFLUENCE"
    S3 = "S3"
    URL = "URL"
    EML = "EML"
    TXT = "TXT"


class DocumentStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    INDEXED = "INDEXED"
    FAILED = "FAILED"


class EvalStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
