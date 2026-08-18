import pytest
from backend.app.services.embeddings import LocalEmbeddingService

@pytest.fixture(scope="module")
def embedding_service():
    return LocalEmbeddingService(model_name="sentence-transformers/all-MiniLM-L6-v2")

def test_embedding_service_initialization(embedding_service):
    assert embedding_service.model is not None
    assert embedding_service.embedding_dimension == 384

def test_embed_short_text(embedding_service):
    chunks = [{
        "text": "Hello world",
        "source": "test.txt",
        "document_type": "txt",
        "page_number": 1,
        "chunk_index": 0
    }]
    embedded_chunks = embedding_service.embed_chunks(chunks)
    
    assert len(embedded_chunks) == 1
    assert "embedding" in embedded_chunks[0]
    assert len(embedded_chunks[0]["embedding"]) == 384
    assert isinstance(embedded_chunks[0]["embedding"][0], float)

def test_embed_multiple_chunks(embedding_service):
    chunks = [
        {"text": "First chunk", "chunk_index": 0},
        {"text": "Second chunk", "chunk_index": 1}
    ]
    embedded_chunks = embedding_service.embed_chunks(chunks)
    
    assert len(embedded_chunks) == 2
    assert "embedding" in embedded_chunks[0]
    assert "embedding" in embedded_chunks[1]
    assert len(embedded_chunks[0]["embedding"]) == 384
    assert len(embedded_chunks[1]["embedding"]) == 384

def test_metadata_preservation(embedding_service):
    chunks = [{
        "text": "Testing metadata",
        "source": "file.pdf",
        "document_type": "pdf",
        "page_number": 5,
        "chunk_index": 10
    }]
    embedded_chunks = embedding_service.embed_chunks(chunks)
    
    assert len(embedded_chunks) == 1
    chunk = embedded_chunks[0]
    assert chunk["source"] == "file.pdf"
    assert chunk["document_type"] == "pdf"
    assert chunk["page_number"] == 5
    assert chunk["chunk_index"] == 10
    assert "embedding" in chunk

def test_deterministic_output_shape(embedding_service):
    chunks = [{"text": "Shape test", "chunk_index": 0}]
    embedded_chunks = embedding_service.embed_chunks(chunks)
    
    assert isinstance(embedded_chunks[0]["embedding"], list)
    assert len(embedded_chunks[0]["embedding"]) == 384
