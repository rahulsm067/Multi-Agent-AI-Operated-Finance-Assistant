from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import faiss
import numpy as np
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    handlers=[
        logging.FileHandler("retriever_agent.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("retriever_agent")

app = FastAPI(
    title="Retriever Agent",
    description="Microservice for vector store indexing and retrieval (FAISS).",
    version="1.0.0"
)

# Enable CORS for local development and Streamlit UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Document(BaseModel):
    text: str
    metadata: Dict
    embedding: List[float]

class QueryRequest(BaseModel):
    query_embedding: List[float]
    top_k: int = 5
    threshold: float = 0.7

class IndexInfo(BaseModel):
    dimension: int
    total_documents: int
    last_updated: str

class VectorStore:
    def __init__(self, dimension: int = 768):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.documents = []
        self.last_updated = datetime.now()

    def add_documents(self, documents: List[Document]):
        if not documents:
            return
        embeddings = [doc.embedding for doc in documents]
        embeddings_array = np.array(embeddings).astype('float32')
        self.index.add(embeddings_array)
        self.documents.extend(documents)
        self.last_updated = datetime.now()
        logger.info(f"Added {len(documents)} documents to vector store.")

    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Dict]:
        query_array = np.array([query_embedding]).astype('float32')
        distances, indices = self.index.search(query_array, top_k)
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < len(self.documents):
                doc = self.documents[idx]
                results.append({
                    "text": doc.text,
                    "metadata": doc.metadata,
                    "score": float(1 / (1 + distance))  # Convert distance to similarity score
                })
        logger.info(f"Search returned {len(results)} results.")
        return results

    def get_info(self) -> IndexInfo:
        return IndexInfo(
            dimension=self.dimension,
            total_documents=len(self.documents),
            last_updated=self.last_updated.isoformat()
        )

# Initialize vector store
vector_store = VectorStore()

@app.post("/add-documents", tags=["Index"])
async def add_documents(documents: List[Document]):
    """Add documents (with embeddings) to the vector store."""
    logger.info(f"/add-documents called with {len(documents)} documents.")
    try:
        vector_store.add_documents(documents)
        return {"status": "success", "documents_added": len(documents)}
    except Exception as e:
        logger.error(f"Error in /add-documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search", tags=["Retrieval"])
async def search(request: QueryRequest):
    """Search for top-k similar documents given a query embedding."""
    logger.info(f"/search called with top_k={request.top_k}, threshold={request.threshold}")
    try:
        results = vector_store.search(
            query_embedding=request.query_embedding,
            top_k=request.top_k
        )
        filtered_results = [r for r in results if r["score"] >= request.threshold]
        logger.info(f"Search returned {len(filtered_results)} filtered results.")
        return {"results": filtered_results}
    except Exception as e:
        logger.error(f"Error in /search: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/info", tags=["Utility"])
async def get_info():
    """Get vector store index info."""
    logger.info("/info called.")
    return vector_store.get_info()

@app.get("/health", tags=["Utility"])
async def health_check():
    """Health check endpoint."""
    logger.info("Health check called.")
    return {"status": "healthy"}