from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer

class LocalEmbeddingService:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initializes the local embedding model once.
        """
        self.model_name = model_name
        self.model = SentenceTransformer(self.model_name)
        self.embedding_dimension = self.model.get_embedding_dimension()

    def embed_chunks(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Takes a list of chunks (each containing 'text', 'source', 'document_type', etc.)
        and computes embeddings for them locally, appending the 'embedding' field.
        """
        if not chunks:
            return []
        
        texts = [chunk.get("text", "") for chunk in chunks]
        
        # Compute embeddings
        # convert_to_numpy=True is default, but ensuring output is a list of floats
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        
        embedded_chunks = []
        for idx, chunk in enumerate(chunks):
            # Create a copy to avoid mutating the original chunk if not desired,
            # but modifying directly is also fine. Let's create a new dict.
            new_chunk = chunk.copy()
            new_chunk["embedding"] = embeddings[idx].tolist()
            embedded_chunks.append(new_chunk)
            
        return embedded_chunks
