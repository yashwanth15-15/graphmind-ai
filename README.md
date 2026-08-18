# GraphMind AI

An enterprise-grade Agentic GraphRAG Knowledge Platform built from scratch.

## Architecture

- **Frontend**: React + TypeScript + Vite
- **Backend**: FastAPI + LangChain + LangGraph
- **LLM Engine**: Ollama (Qwen2.5)
- **Vector DB**: Qdrant
- **Graph DB**: Neo4j Community
- **Relational DB**: PostgreSQL

## Getting Started

1. Copy `.env.example` to `.env`
2. Start the database containers: `docker-compose up -d`
3. Start the backend: `cd backend && pip install -r requirements.txt && uvicorn main:app --reload`
4. Start the frontend: `cd frontend && npm install && npm run dev`
