from retriever import ChromaRetriever
import google.generativeai as genai

class RAGPipeline:
    def __init__(self):
        self.retriever = ChromaRetriever()
        # self.generator = OpenAIGenerator()

    # def chat(self, query):
    #     """Runs full RAG retrieval + generation."""
    #     docs, _ = self.retriever.retrieve(query)
    #     context = "\n".join(docs) if docs else "No relevant information found."
    #     return self.generator.generate(context, query)
    # def chat(request: ChatRequest):
    #     query = request.query
    #     if not query:
    #         raise HTTPException(status_code=400, detail="Query is required")
    #     docs, metadatas = retrieve_relevant_docs(query)
    #     context = "\n".join(docs)
    #     response = generate_response(context, query)
    #     return {"response": response}