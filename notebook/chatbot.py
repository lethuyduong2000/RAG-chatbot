from setup import *


prompt_begin_template = """
Bạn là trợ lý ảo của Namperfume, chuyên tư vấn nước hoa. Hãy bắt đầu cuộc trò chuyện một cách tự nhiên và đặt câu hỏi một cách linh hoạt để hiểu rõ sở thích của khách hàng. Dưới đây là một số gợi ý về thông tin bạn có thể thu thập:

* Mùi hương khách hàng yêu thích là gì? (Ví dụ: tươi mát, hoa cỏ, gỗ, trái cây, vani,...)
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

######
ChatBot: Chào bạn, mình là trợ lý ảo của Namperfume. Rất vui được hỗ trợ bạn tìm kiếm mùi hương ưng ý. Bạn có thể cho mình biết bạn đang tìm kiếm loại nước hoa như thế nào không?

Khách hàng: {question}

ChatBot:
"""


prompt_begin = ChatPromptTemplate.from_template(prompt_begin_template)
input_prompt_begin = prompt_begin.format(question="Tôi muốn được tư vấn nước hoa")

response = llm.generate_content(input_prompt_begin)
print(f"ChatBot: {str_output_parser(response)}\n")

history = [input_prompt_begin]  # Danh sách lưu lịch sử hội thoại

while True:
    user_input = input("Bạn: ")
    

    if "exit" in user_input.lower():
        print("🔹 Đã thoát khỏi chatbot.")
        break

    history.append(f"Bạn: {user_input}")
    full_prompt = "\n".join(history)
    
    # Chuỗi hội thoại đầy đủ
    response = llm.generate_content(full_prompt)

    # Xử lý phản hồi
    if hasattr(response, "text"):
        bot_response = response.text
    elif isinstance(response, dict) and "text" in response:
        bot_response = response["text"]
    else:
        bot_response = str(response)

    print(f"{bot_response}\n")
    # Lưu tin nhắn của chatbot vào lịch sử
    history.append(f"{bot_response}")

