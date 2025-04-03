import os
import re

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("API_KEY")
genai.configure(api_key=GEMINI_API_KEY)  

# class GenAIGenerator:
#     def __init__(self, model="gemini-2.0-flash"):
#         self.model = model  
#         self.api_key = GEMINI_API_KEY 

#     def generate(self, context, query):
        # """Generates a response using GenAI."""
        # prompt = f"""
        # You are an e-commerce assistant. Answer customer queries about products using the provided context.
        # If the context does not contain enough information, say 'I don't know'.
        # Keep responses short and direct.

        # Context: {context}
        # Question: {query}
        # Answer:
        # """
        # model = genai.GenerativeModel(self.model)
        # print(f'=== prompt === {prompt}')
        # response = model.generate_content(prompt)  

        # return response.text.strip()

class GenAIGenerator:
    def __init__(self, model="gemini-2.0-flash"):
        self.model = genai.GenerativeModel(model)
        self.api_key = GEMINI_API_KEY

    def generate(self, question, history=None):
        """Generates a response for Namperfume chatbot with conversation history support."""
        
        # Prepare chat history
        history_text = "\n".join(history) if history else ""

        # Define the perfume assistant prompt
        prompt_begin_template = f"""
        Bạn là trợ lý ảo của Namperfume, chuyên tư vấn nước hoa. Hãy bắt đầu cuộc trò chuyện một cách tự nhiên và đặt câu hỏi một cách linh hoạt để hiểu rõ sở thích của khách hàng. Dưới đây là một số gợi ý về thông tin bạn có thể thu thập:

        * Mùi hương khách hàng yêu thích là gì? (Ví dụ: tươi mát, hoa cỏ, gỗ, trái cây, vani,...)
        * Xác định giới tính của khách hàng sử dụng? Mua cho bản thân hay mua tặng cho ai?
        * Khách hàng muốn sử dụng nước hoa cho mục đích gì? (Hàng ngày, dịp đặc biệt, đi làm, hẹn hò,...)
        * Phong cách mà khách hàng hướng đến là gì? (Năng động, thanh lịch, lãng mạn, cá tính, quyến rũ,...)
        * Khách hàng mong muốn nước hoa mang lại cảm giác gì? (Tự tin, thư giãn, nổi bật, ấm áp,...)
        * Thời tiết hoặc mùa nào mà khách hàng thường sử dụng nước hoa?
        * Ngân sách mà khách hàng dự định chi cho nước hoa là bao nhiêu?
        * Khách hàng có thương hiệu nước hoa yêu thích nào không?

        **Lưu ý quan trọng:**
        * Không nhất thiết phải hỏi tất cả các câu hỏi. Hãy lắng nghe câu trả lời của khách hàng và đặt câu hỏi tiếp theo một cách tự nhiên dựa trên thông tin đã có.
        * Nếu bạn cảm thấy đã thu thập đủ thông tin để đưa ra gợi ý phù hợp, hãy chuyển sang bước giới thiệu sản phẩm mà không cần hỏi thêm.
        * Ưu tiên tạo ra một cuộc trò chuyện thoải mái và hữu ích cho khách hàng.
        * Chỉ hỏi chưa tư vấn sản phẩm cụ thể nào.
        * Sau khi thu thập đủ thông tin thì nói khách hàng đợi để tìm kiếm sản phẩm phù hợp.

        ######
        {history_text}

        ChatBot: 

        Khách hàng: {question}

        ChatBot:
        """

        print(f"=== Prompt Sent ===\n{prompt_begin_template}\n")

        try:
            response = self.model.generate_content(prompt_begin_template)
            return response.text.strip()
        except Exception as e:
            return f"Error generating response: {str(e)}"
        
    
    def explore_customer_preferences(self, history):
        """Generates detailed customer preference descriptions."""
        full_text_history = "\n".join(history)
        history_chat = full_text_history.split("######")[1]

        query_explore_template = f"""
        Dựa vào lịch sử trò chuyện sau đây...
        
        **Lịch sử trò chuyện:**
        {history_chat}
        
        **Yêu cầu:**
        
        Mô tả 1: ...
        Mô tả 2: ...
        Mô tả 3: ...
        Mô tả 4: ...
        Mô tả 5: ...
        """
        
        response = self.model.generate_content(query_explore_template)
        return response.text.strip()

    def split_descriptions(self, text):
        """Splits descriptions into a structured list."""
        descriptions = re.split(r'\n\nMô tả \d+:\s*', text)
        return [f"Mô tả {idx+1}: " + item if not item.startswith("Mô tả") else item for idx, item in enumerate(descriptions)]

    def rank_products(self, response, product_recommendations):
        """Ranks the most suitable perfume recommendations."""
        prompt_ranking = f"""
        Dưới đây là danh sách các sản phẩm nước hoa gợi ý...
        
        {response}
        
        ##########
        DANH SÁCH SẢN PHẨM
        
        """
        
        for item in product_recommendations:
            prompt_ranking += item
        
        return self.model.generate_content(prompt_ranking).text
