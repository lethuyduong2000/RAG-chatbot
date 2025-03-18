from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from sentence_transformers import SentenceTransformer


# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(
    name="products",
    embedding_function=SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
)

# Request model for chat queries
class ChatRequest(BaseModel):
    query: str

# Function to add documents to ChromaDB
def add_documents(documents):
    for i, doc in enumerate(documents):
        collection.add(
            ids=[str(i)],
            documents=[doc["text"]],
            metadatas=[doc["metadata"]]
        )

# Function to retrieve relevant documents
def retrieve_relevant_docs(query, top_k=5):
    results = collection.query(query_texts=[query], n_results=top_k)
    return results["documents"], results["metadatas"]

# Function to generate a response using OpenAI
def generate_response(context, query):
    prompt = f"""
    You are a Toronto travel assistant. Users will ask you questions about their trip to Toronto.
    Use the following piece of context to answer the question.
    If you don't know the answer, just say you don't know.
    Your answer should be short and concise, no longer than 2 sentences.

    Context: {context}
    Question: {query}
    Answer:
    """
    model = genai.GenerativeModel(model)
    response = model.generate_content(
        model=self.model,
        messages=[{"role": "system", "content": prompt}],
        api_key=self.api_key
    )
    return response.text.strip()

# Chat API endpoint
@app.post("/chat")
def chat(request: ChatRequest):
    query = request.query
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")
    docs, metadatas = retrieve_relevant_docs(query)
    # context = "\n".join(docs)
    context = 'Nước hoa nam có mùi nhẹ nhàng'
    response = generate_response(context, query)
    return {"response": response}

# Run FastAPI app (example document ingestion)
if __name__ == "__main__":
    import uvicorn

    example_docs = [
        {"text": "Toronto has many attractions including the CN Tower.", "metadata": {"source": "travel_guide"}},
        {"text": "Public transport in Toronto includes subways, buses, and streetcars.", "metadata": {"source": "transit_info"}}
    ]
    add_documents(example_docs)
    uvicorn.run(app, host="0.0.0.0", port=5000)
