from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ..rag.generator import GenAIGenerator
from ..rag.retriever import ChromaRetriever
from pydantic import BaseModel
import re
# from .endpoints import orders, products
# from ..config import Settings

# Initialize FastAPI app
app = FastAPI(
    title="E-commerce Dataset API",
    description="API for querying e-commerce sales data",
    version="1.0.0"
)

history_chat = []

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
# @app.post("/chat")
# def chat(request: ChatRequest):
#     query = request.query
#     if not query:
#         raise HTTPException(status_code=400, detail="Query is required")
#     print(f"query: {query}")

#     # retriever = ChromaRetriever()
#     # docs = retriever.retrieve(query)
#     # context = retriever.format_docs(docs)
#     # print(context)

#     generator = GenAIGenerator(model="gemini-2.0-flash")
#     # response = generator.generate(context, query)         #old

#     response = generator.generate(question=query, history=history_chat)
#     history_chat.append(f"User: {query}")
#     history_chat.append(f"ChatBot: {response}")

#     return {"response": response}

class ChatRequest(BaseModel):
    query: str

# Function to extract and format customer preferences
def extract_customer_preferences(history_chat, generator):
    full_text_history = "\n".join(history_chat)
    history_chat_text = full_text_history.split("######")[1] if "######" in full_text_history else full_text_history
    
    query_explore_template = """
    Dựa vào lịch sử trò chuyện sau đây, bạn hãy đóng vai trò là một chuyên gia tư vấn nước hoa cao cấp. 
    Hãy tạo ra 5 mô tả chi tiết về sở thích của khách hàng để tìm nước hoa phù hợp.

    **Lịch sử trò chuyện:**
    {history_chat}
    """
    
    prompt = query_explore_template.format(history_chat=history_chat_text)
    response = generator.generate("", prompt)
    
    return re.split(r'\n\nMô tả \d+:\s*', response)

# Function to retrieve product recommendations
def get_product_recommendations(descriptions, retriever):
    docs = [retriever.retrieve(desc) for desc in descriptions if desc]
    
    recommendations = []
    for doc in docs:
        ids = doc['ids'][0]
        for id, meta in zip(ids, doc['metadatas'][0]):
            recommendations.append({
                "id": id,
                "brand": meta["brand"],
                "name": meta["name"],
                "description": meta["description"],
                "origin": meta["origin"],
                "style": meta["product_style"],
                "notes": meta["product_note"],
                "gender": meta["product_gender"],
                "price": meta["price"]
            })
    
    return recommendations

# Function to rank the best perfumes
def rank_products(generator, descriptions, products):
    prompt_ranking = """
    Dưới đây là danh sách sản phẩm nước hoa gợi ý dựa trên mô tả khách hàng.
    Hãy chọn ra 3 sản phẩm phù hợp nhất.

    ### Mô tả khách hàng:
    {descriptions}

    ### Sản phẩm:
    {products}
    """.format(descriptions="\n".join(descriptions), products="\n".join([str(p) for p in products]))
    
    return generator.generate("", prompt_ranking)

@app.post("/chat")
async def chat(request: ChatRequest):
    query = request.query.strip()

    if not query:
        raise HTTPException(status_code=400, detail="Query is required")

    print(f"User Query: {query}")

    generator = GenAIGenerator(model="gemini-2.0-flash")

    history_chat.append(f"User: {query}")

    # **BƯỚC 1: Chatbot phản hồi câu hỏi của khách hàng**
    response = generator.generate(question=query, history=history_chat)
    history_chat.append(f"ChatBot: {response}")

    if len(history_chat) == 8:  
        full_text_history = "\n".join(history_chat)

        extract_customer_preferences_template = f"""
        Dựa vào lịch sử trò chuyện sau đây, bạn hãy phân tích và tạo ra 5 mô tả chi tiết về sở thích nước hoa của khách hàng.

        **Lịch sử trò chuyện:**
        {full_text_history}
        
        **Định dạng đầu ra:**
        Mô tả 1: [Mô tả chi tiết]
        Mô tả 2: [Mô tả chi tiết]
        Mô tả 3: [Mô tả chi tiết]
        Mô tả 4: [Mô tả chi tiết]
        Mô tả 5: [Mô tả chi tiết]
        """

        response_preferences = generator.generate(extract_customer_preferences_template)
        history_chat.append(f"ChatBot (Phân tích sở thích): {response_preferences}")

        # **BƯỚC 3: Tìm kiếm sản phẩm nước hoa phù hợp**
        def split_descriptions(text):
            descriptions = re.split(r'\n\nMô tả \d+:\s*', text)
            return [desc.strip() for desc in descriptions if desc]

        descriptions = split_descriptions(response_preferences)
        retriever = ChromaRetriever()
        retrieved_docs = [retriever.retrieve(desc) for desc in descriptions]

        # **BƯỚC 4: Định dạng danh sách sản phẩm**
        def product_description(id, metadata):
            return f"""
            ------------
            ID: {id}
            Brand: {metadata['brand']}
            Name: {metadata['name']}
            Price: {metadata['price']}
            Style: {metadata['product_style']}
            Notes: {metadata['product_note']}
            Description: {metadata['description']}
            """

        product_recommendations = []
        for doc in retrieved_docs:
            for id, metadata in zip(doc["ids"][0], doc["metadatas"][0]):
                product_recommendations.append(product_description(id, metadata))

       
        ranking_prompt = f"""
        Dưới đây là danh sách nước hoa phù hợp nhất. Chọn ra 3 sản phẩm tốt nhất:

        {response_preferences}

        ###### DANH SÁCH SẢN PHẨM ######
        {''.join(product_recommendations)}
        """

        ranked_response = generator.generate(ranking_prompt)
        history_chat.append(f"ChatBot (Top 3 sản phẩm): {ranked_response}")
        print(f"===Top 3 sản phẩm==={ranked_response}")
        return {"response": ranked_response}

    

    return {"response": response}


if __name__ == "__main__":
    import uvicorn
    # settings = Settings()
    uvicorn.run(
        "src.api.main:app",
        host="127.0.0.1", port=8000, # host=settings.HOST, # port=settings.PORT,
        reload=True
    )