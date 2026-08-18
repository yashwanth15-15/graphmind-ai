from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_embeddings_endpoint():
    file_path = "sample_embeddings.txt"
    with open(file_path, "wb") as f:
        f.write(b"This is a test document. It is short but should be embedded properly.")

    with open(file_path, "rb") as f:
        response = client.post("/api/v1/documents/embeddings", files={"file": ("sample_embeddings.txt", f, "text/plain")})
        
    print("Status Code:", response.status_code)
    data = response.json()
    print("Filename:", data["filename"])
    print("Total Chunks:", data["total_chunks"])
    print("Embedding Dimension:", data["embedding_dimension"])
    if data["preview"]:
        print("First chunk embedding length:", len(data["preview"][0]["embedding"]))
        print("First chunk preview embedding sample:", data["preview"][0]["embedding"][:5])

if __name__ == "__main__":
    test_embeddings_endpoint()
