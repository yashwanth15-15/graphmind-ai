import pytest
from backend.app.services.vector_store import QdrantService
from qdrant_client.http.models import Distance

@pytest.fixture(scope="module")
def qdrant_service():
    # Use :memory: so we don't need a real Docker container for unit tests
    return QdrantService(location=":memory:", collection_name="test_graphmind_documents", vector_size=384)

def test_qdrant_collection_creation(qdrant_service):
    collections = qdrant_service.client.get_collections().collections
    names = [c.name for c in collections]
    assert "test_graphmind_documents" in names
    
    # Check dimensions
    collection_info = qdrant_service.client.get_collection("test_graphmind_documents")
    assert collection_info.config.params.vectors.size == 384
    assert collection_info.config.params.vectors.distance == Distance.COSINE

def test_upsert_and_search_vectors(qdrant_service):
    dummy_embedding = [1.0] + [0.0] * 383
    
    chunks = [
        {
            "text": "This is a test chunk about apples.",
            "source": "test_apples.pdf",
            "document_type": "pdf",
            "page_number": 1,
            "chunk_index": 0,
            "embedding": dummy_embedding
        },
        {
            "text": "This is a test chunk about bananas.",
            "source": "test_bananas.txt",
            "document_type": "txt",
            "page_number": 2,
            "chunk_index": 1,
            "embedding": [0.0, 1.0] + [0.0] * 382
        }
    ]
    
    upsert_count = qdrant_service.upsert_chunks(chunks)
    assert upsert_count == 2
    
    # Search using a vector exactly like "apples"
    results = qdrant_service.search(query_vector=dummy_embedding, top_k=1)
    
    assert len(results) == 1
    assert "score" in results[0]
    assert results[0]["source"] == "test_apples.pdf"
    assert results[0]["document_type"] == "pdf"
    assert results[0]["text"] == "This is a test chunk about apples."
    assert "embedding" not in results[0] # Embedding should not be returned in payload

def test_generate_id(qdrant_service):
    id1 = qdrant_service._generate_id("file1.txt", 0)
    id2 = qdrant_service._generate_id("file1.txt", 0)
    id3 = qdrant_service._generate_id("file1.txt", 1)
    
    assert id1 == id2
    assert id1 != id3
    assert len(id1) == 32 # md5 hexdigest length
