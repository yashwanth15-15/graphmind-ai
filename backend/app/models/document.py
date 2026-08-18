from pydantic import BaseModel
from typing import List, Optional

class DocumentMetadata(BaseModel):
    filename: str
    file_type: str
    page_count: int
    char_count: int

class DocumentSegment(BaseModel):
    text: str
    page_number: Optional[int] = None

class ExtractedDocument(BaseModel):
    metadata: DocumentMetadata
    segments: List[DocumentSegment]
