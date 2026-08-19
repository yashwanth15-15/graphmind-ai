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
3. Make sure you have [Ollama](https://ollama.com/) installed and running locally (`localhost:11434`), and that you have pulled your preferred model (e.g., `ollama run llama3`).
4. Start the backend: `cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload`
5. Start the frontend: `cd frontend && npm install && npm run dev`
