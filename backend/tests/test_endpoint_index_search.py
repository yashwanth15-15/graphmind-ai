from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_full_pipeline():
    # 1. Index document
    file_path = "sample_index.txt"
    with open(file_path, "wb") as f:
        f.write(b"GraphMind AI uses Qdrant for vector similarity search.")

    with open(file_path, "rb") as f:
        index_response = client.post("/api/v1/documents/index", files={"file": ("sample_index.txt", f, "text/plain")})
        
    print("Index Status Code:", index_response.status_code)
    index_data = index_response.json()
    print("Index Response:", index_data)

    # 2. Search document
    search_payload = {
        "query": "What database does GraphMind use for search?",
        "top_k": 2
    }
    search_response = client.post("/api/v1/search", json=search_payload)
    print("Search Status Code:", search_response.status_code)
    search_data = search_response.json()
    
    print("\nSearch Results:")
    for res in search_data.get("results", []):
        print(f"- Score: {res.get('score'):.4f} | Source: {res.get('source')} | Text: {res.get('text')}")

if __name__ == "__main__":
    test_full_pipeline()
