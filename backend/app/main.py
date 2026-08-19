from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routers import documents, search

app = FastAPI(
    title="GraphMind AI API",
    description="Backend API for Agentic GraphRAG Knowledge Platform",
    version="0.1.0",
)

# CORS setup for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["System"])
def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "ok", "message": "GraphMind AI backend is running."}

app.include_router(documents.router)
app.include_router(search.router)
