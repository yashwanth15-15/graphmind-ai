import pytest
from backend.app.services.chunking import DocumentChunker

def test_short_text():
    chunker = DocumentChunker(chunk_size=100, chunk_overlap=20)
    pages = [{"page_number": 1, "text": "This is a very short text.", "metadata": {"type": "txt"}}]
    chunks = chunker.chunk_document("test.txt", "txt", pages)
    
    assert len(chunks) == 1
    assert chunks[0]["text"] == "This is a very short text."
    assert chunks[0]["source"] == "test.txt"
    assert chunks[0]["document_type"] == "txt"
    assert chunks[0]["page_number"] == 1
    assert chunks[0]["chunk_index"] == 0

def test_text_requiring_multiple_chunks():
    chunker = DocumentChunker(chunk_size=50, chunk_overlap=10)
    long_text = "A" * 120
    pages = [{"page_number": 1, "text": long_text, "metadata": {"type": "txt"}}]
    chunks = chunker.chunk_document("test.txt", "txt", pages)
    
    # 120 chars, chunk size 50, overlap 10
    # chunk 1: 0-50
    # chunk 2: 40-90
    # chunk 3: 80-120 (length 40)
    assert len(chunks) == 3
    assert len(chunks[0]["text"]) == 50
    assert len(chunks[1]["text"]) == 50
    assert len(chunks[2]["text"]) == 40

def test_overlap_behavior():
    chunker = DocumentChunker(chunk_size=50, chunk_overlap=10)
    # create text with distinct words
    text = "0123456789" * 12
    pages = [{"page_number": 1, "text": text, "metadata": {"type": "txt"}}]
    chunks = chunker.chunk_document("test.txt", "txt", pages)
    
    # chunk 1: 0-50 -> ends with ...789
    # chunk 2: 40-90 -> starts with 0123456789 from the end of chunk 1
    assert chunks[0]["text"][-10:] == chunks[1]["text"][:10]

def test_metadata_preservation():
    chunker = DocumentChunker(chunk_size=100, chunk_overlap=20)
    pages = [
        {"page_number": 1, "text": "Slide 1 text", "metadata": {"type": "pptx_slide"}},
        {"page_number": 2, "text": "Slide 2 text", "metadata": {"type": "pptx_slide"}}
    ]
    chunks = chunker.chunk_document("presentation.pptx", "pptx", pages)
    
    assert len(chunks) == 2
    assert chunks[0]["page_number"] == 1
    assert chunks[0]["chunk_index"] == 0
    assert chunks[0]["source"] == "presentation.pptx"
    
    assert chunks[1]["page_number"] == 2
    assert chunks[1]["chunk_index"] == 1
    assert chunks[1]["source"] == "presentation.pptx"
