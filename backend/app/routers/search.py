from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from backend.app.services.embeddings import LocalEmbeddingService
from backend.app.services.vector_store import QdrantService

router = APIRouter(prefix="/api/v1/search", tags=["Search"])

embedding_service = LocalEmbeddingService()
qdrant_service = QdrantService()

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

class SearchResult(BaseModel):
    query: str
    results: List[Dict[str, Any]]

@router.post("", response_model=SearchResult)
async def search_documents(request: SearchRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
        
    # Embed the query
    # We pass it as a chunk-like struct or just use the model directly
    # Since embed_chunks expects a list of dicts:
    dummy_chunks = [{"text": request.query}]
    embedded = embedding_service.embed_chunks(dummy_chunks)
    query_vector = embedded[0]["embedding"]
    
    # Search Qdrant
    results = qdrant_service.search(query_vector=query_vector, top_k=request.top_k)
    
    return SearchResult(
        query=request.query,
        results=results
    )
