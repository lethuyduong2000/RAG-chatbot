from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ..rag.generator import GenAIGenerator
from ..rag.retriever import ChromaRetriever
from pydantic import BaseModel

# from .endpoints import orders, products
# from ..config import Settings

# Initialize FastAPI app
app = FastAPI(
    title="E-commerce Dataset API",
    description="API for querying e-commerce sales data",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
# app.include_router(orders.router, prefix="/orders", tags=["orders"])
# app.include_router(products.router, prefix="/products", tags=["products"])

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "E-commerce Dataset API",
        "version": "1.0.0",
        "documentation": "/docs",
        "health_check": "/health"
    }
# Request model for chat queries
class ChatRequest(BaseModel):
    query: str

# Chat API endpoint
@app.post("/chat")
def chat(request: ChatRequest):
    query = request.query
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")
    print(f"query: {query}")
    retriever = ChromaRetriever()
    # docs, meta = retriever.retrieve(query)
    docs = retriever.retrieve(query)
    context = retriever.format_docs(docs)
    print(context)

    # context = "\n".join(docs)
    # context = 'Nước hoa nam có mùi nhẹ nhàng'
    generator = GenAIGenerator(model="gemini-2.0-flash")
    response = generator.generate(context, query)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    # settings = Settings()
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0", port=5000, # host=settings.HOST, # port=settings.PORT,
        reload=True
    )