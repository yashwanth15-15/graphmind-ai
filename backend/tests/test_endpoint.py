from fastapi.testclient import TestClient
from backend.app.main import app
import os

client = TestClient(app)

def test_chunking_endpoint():
    file_path = "sample.txt"
    with open(file_path, "wb") as f:
        f.write(b"This is a sample document that we will upload to test chunking. " * 20)

    with open(file_path, "rb") as f:
        response = client.post("/api/v1/documents/chunks", files={"file": ("sample.txt", f, "text/plain")})
        
    print("Status Code:", response.status_code)
    data = response.json()
    print("Filename:", data["filename"])
    print("Total Sections:", data["total_extracted_sections"])
    print("Total Chunks:", data["total_chunks"])
    print("First chunk preview:", data["chunks"][0] if data["chunks"] else None)

if __name__ == "__main__":
    test_chunking_endpoint()
