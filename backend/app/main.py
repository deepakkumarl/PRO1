from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.config import settings

app = FastAPI(
    title="BMW Service Knowledge RAG Assistant API",
    description="AI-powered Retrieval-Augmented Generation (RAG) assistant for BMW service technicians.",
    version="1.0.0",
)

# Configure CORS for React frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows Vite dev server & production builds
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Router
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    print("=" * 60)
    print("BMW Service Knowledge RAG Assistant Backend Started")
    print(f"Ollama Model Configured: {settings.OLLAMA_MODEL} ({settings.OLLAMA_BASE_URL})")
    print(f"Embedding Model: {settings.EMBEDDING_MODEL}")
    print(f"Documents Directory: {settings.DOCUMENTS_DIR}")
    print(f"Vector Store Directory: {settings.VECTORSTORE_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
