from typing import List, Dict, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentChunker:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 150):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        )

    def chunk_document(self, filename: str, document_type: str, extracted_pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Chunks an extracted document into smaller pieces.
        extracted_pages is a list of dicts: {"page_number": int, "text": str, "metadata": dict}
        """
        chunks = []
        chunk_index = 0
        
        for page in extracted_pages:
            page_text = page.get("text", "")
            page_number = page.get("page_number", 1)
            
            if not page_text.strip():
                continue
                
            split_texts = self.splitter.split_text(page_text)
            
            for text_chunk in split_texts:
                chunks.append({
                    "text": text_chunk,
                    "source": filename,
                    "document_type": document_type,
                    "page_number": page_number,
                    "chunk_index": chunk_index
                })
                chunk_index += 1
                
        return chunks
