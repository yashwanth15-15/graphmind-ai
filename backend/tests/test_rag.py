import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from backend.app.main import app

client = TestClient(app)

@pytest.fixture
def mock_embedding_service():
    with patch("backend.app.routers.rag.rag_service.embedding_service") as mock:
        mock.embed_chunks.return_value = [{"embedding": [0.1, 0.2, 0.3]}]
        yield mock

@pytest.fixture
def mock_qdrant_service():
    with patch("backend.app.routers.rag.rag_service.qdrant_service") as mock:
        yield mock

@pytest.fixture
def mock_ollama():
    with patch("backend.app.rag.service.ollama") as mock:
        mock.chat.return_value = {"message": {"content": "This is a mock answer."}}
        yield mock

def test_rag_query_success(mock_embedding_service, mock_qdrant_service, mock_ollama):
    # Setup mock qdrant search response
    mock_qdrant_service.search.return_value = [
        {
            "text": "This document is about AI.",
            "source": "ai_doc.pdf",
            "page_number": 1,
            "chunk_index": 0,
            "score": 0.85,
            "document_type": "application/pdf"
        }
    ]
    
    response = client.post("/api/v1/rag/query", json={"query": "What is AI?", "top_k": 3})
    
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "What is AI?"
    assert data["answer"] == "This is a mock answer."
    assert len(data["sources"]) == 1
    assert data["sources"][0]["source"] == "ai_doc.pdf"
    assert data["sources"][0]["score"] == 0.85

def test_rag_query_no_results(mock_embedding_service, mock_qdrant_service, mock_ollama):
    # Setup mock qdrant to return empty (or scores below threshold)
    mock_qdrant_service.search.return_value = []
    
    response = client.post("/api/v1/rag/query", json={"query": "What is AI?", "top_k": 3})
    
    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "I cannot find the answer to this question in the uploaded documents."
    assert len(data["sources"]) == 0
    # Ollama should not be called
    mock_ollama.chat.assert_not_called()

def test_rag_query_empty_query():
    response = client.post("/api/v1/rag/query", json={"query": "", "top_k": 3})
    assert response.status_code in [400, 422]

def test_rag_query_ollama_failure(mock_embedding_service, mock_qdrant_service, mock_ollama):
    mock_qdrant_service.search.return_value = [
        {
            "text": "This document is about AI.",
            "source": "ai_doc.pdf",
            "score": 0.85,
        }
    ]
    
    # Simulate Ollama connection error
    mock_ollama.chat.side_effect = Exception("Connection refused")
    
    response = client.post("/api/v1/rag/query", json={"query": "What is AI?", "top_k": 3})
    assert response.status_code == 503
    assert "Failed to communicate with local LLM" in response.json()["detail"]
