from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

from backend.app.rag.service import RAGService

router = APIRouter(prefix="/api/v1/rag", tags=["RAG"])

rag_service = RAGService()

class RAGQueryRequest(BaseModel):
    query: str = Field(..., min_length=1, description="The user's question to be answered via RAG.")
    top_k: int = Field(5, ge=1, le=20, description="Number of context chunks to retrieve.")

class RAGSource(BaseModel):
    source: str
    page_number: Optional[int] = None
    chunk_index: Optional[int] = None
    score: Optional[float] = None
    document_type: Optional[str] = None

class RAGQueryResponse(BaseModel):
    query: str
    answer: str
    sources: List[RAGSource]

@router.post("/query", response_model=RAGQueryResponse)
async def query_rag(request: RAGQueryRequest):
    if not request.query.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query cannot be empty"
        )
        
    try:
        answer, sources = rag_service.query(question=request.query, top_k=request.top_k)
        
        return RAGQueryResponse(
            query=request.query,
            answer=answer,
            sources=[RAGSource(**s) for s in sources]
        )
    except Exception as e:
        if "Failed to communicate with local LLM" in str(e):
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(e)
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during RAG processing: {str(e)}"
        )
