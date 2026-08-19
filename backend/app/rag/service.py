import ollama
from typing import List, Dict, Any, Tuple
from backend.app.services.embeddings import LocalEmbeddingService
from backend.app.services.vector_store import QdrantService

class RAGService:
    def __init__(self, model_name: str = "qwen2.5:3b"):
        self.embedding_service = LocalEmbeddingService()
        self.qdrant_service = QdrantService()
        self.model_name = model_name
        self.score_threshold = 0.3 # Ignore chunks with very low similarity

    def query(self, question: str, top_k: int = 5) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Processes a RAG query and returns the generated answer and source documents.
        """
        # 1. Embed query
        embedded = self.embedding_service.embed_chunks([{"text": question}])
        query_vector = embedded[0]["embedding"]
        
        # 2. Search Qdrant
        results = self.qdrant_service.search(query_vector=query_vector, top_k=top_k)
        
        # Filter by score
        valid_results = [r for r in results if r.get("score", 0) >= self.score_threshold]
        
        if not valid_results:
            return "I cannot find the answer to this question in the uploaded documents.", []
            
        # 3. Construct Context
        context_parts = []
        sources = []
        for res in valid_results:
            text = res.get("text", "")
            if text:
                context_parts.append(text)
            
            # Extract metadata for sources
            source_info = {
                "source": res.get("source", "unknown"),
                "page_number": res.get("page_number"),
                "chunk_index": res.get("chunk_index"),
                "score": res.get("score")
            }
            if "document_type" in res:
                source_info["document_type"] = res.get("document_type")
            sources.append(source_info)
            
        context_str = "\n\n".join(context_parts)
        
        # 4. Prompt Generation
        system_prompt = (
            "You are an intelligent AI assistant. Use ONLY the provided context to answer the user's question. "
            "If the answer cannot be found in the context, say exactly: \"I cannot find the answer to this question in the uploaded documents.\" "
            "Do not try to make up an answer."
        )
        
        user_prompt = f"Context:\n{context_str}\n\nQuestion: {question}"
        
        # 5. LLM Call
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            answer = response["message"]["content"]
        except Exception as e:
            raise Exception(f"Failed to communicate with local LLM (Ollama): {str(e)}")
            
        return answer, sources
