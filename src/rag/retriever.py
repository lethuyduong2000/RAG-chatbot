import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from sentence_transformers import SentenceTransformer

from src.rag.config import (CHROM_DB_COLLECTION, 
                            DB_PATH,
                            EMBEDDING_MODEL)


class ChromaRetriever:
    def __init__(self, db_path=DB_PATH, model_name=EMBEDDING_MODEL):
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(
            name=CHROM_DB_COLLECTION)

    def add_documents(self, documents):
        """Adds documents to ChromaDB."""
        for i, doc in enumerate(documents):
            self.collection.add(
                ids=[str(i)],
                documents=[doc["text"]],
                metadatas=[doc["metadata"]]
            )

    # def retrieve(self, query, top_k=5):
    #     """Retrieves relevant documents from ChromaDB."""
    #     results = self.collection.query(query_texts=[query], n_results=top_k)
    #     return results["documents"], results["metadatas"]
    
    def retrieve(self, query):
        model = SentenceTransformer(EMBEDDING_MODEL)
        query_embedding = model.encode([query], convert_to_tensor=True).tolist()

        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=5
        )
        return results
    
    def format_docs(self,docs):
        if not docs["metadatas"]:
            return "No matching products found."

        return "\n\n".join([
            '\n'.join([res.get('name', 'No Name'), res.get("product_style", 'No Style')]) 
            for res in docs["metadatas"][0]
        ])