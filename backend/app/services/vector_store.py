import hashlib
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models

class QdrantService:
    def __init__(self, location: str = "http://localhost:6333", collection_name: str = "graphmind_documents", vector_size: int = 384):
        # We allow :memory: location for testing
        if location == ":memory:":
            self.client = QdrantClient(location)
        else:
            self.client = QdrantClient(url=location)
            
        self.collection_name = collection_name
        self.vector_size = vector_size
        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        try:
            collections_response = self.client.get_collections()
            collection_names = [collection.name for collection in collections_response.collections]
            
            if self.collection_name not in collection_names:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=self.vector_size,
                        distance=models.Distance.COSINE
                    )
                )
        except Exception as e:
            # We catch exceptions for when Qdrant is completely down, 
            # so the API can still boot, but vector operations will fail later.
            print(f"Warning: Could not connect to Qdrant or create collection: {e}")

    def _generate_id(self, source: str, chunk_index: int) -> str:
        """Generate a deterministic UUID-like string from source and index."""
        unique_string = f"{source}_{chunk_index}"
        return hashlib.md5(unique_string.encode('utf-8')).hexdigest()

    def upsert_chunks(self, embedded_chunks: List[Dict[str, Any]]) -> int:
        """
        Takes chunks with embeddings and inserts them into Qdrant.
        Expects chunk to have: text, source, document_type, page_number, chunk_index, embedding
        """
        if not embedded_chunks:
            return 0
            
        points = []
        for chunk in embedded_chunks:
            # Remove embedding from payload, as Qdrant stores it separately
            payload = {k: v for k, v in chunk.items() if k != "embedding"}
            
            # Generate deterministic ID
            source = payload.get("source", "unknown")
            chunk_index = payload.get("chunk_index", 0)
            point_id = self._generate_id(source, chunk_index)
            
            points.append(
                models.PointStruct(
                    id=point_id,
                    vector=chunk["embedding"],
                    payload=payload
                )
            )
            
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        return len(points)

    def search(self, query_vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar vectors.
        """
        try:
            search_result = self.client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                limit=top_k
            ).points
            
            results = []
            for hit in search_result:
                payload = hit.payload or {}
                results.append({
                    "score": hit.score,
                    **payload
                })
            return results
        except Exception as e:
            print(f"Search failed: {e}")
            return []
