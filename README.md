# RAG-chatbot
RAG-based Chatbot for retail e-commerce

## Mục lục
- [Thành viên](#Thành-viên)
- [Giới thiệu](#giới-thiệu)
- [Workflow Dự án](#workflow-dự-án)
  - [1. Thu thập dữ liệu (Crawl data)](#1-thu-thập-dữ-liệu-crawl-data)
  - [2. Xây dựng RAG (Retrieval-Augmented Generation)](#2-xây-dựng-rag-retrieval-augmented-generation)
  - [3. Xây dựng API](#3-xây-dựng-api)
- [Cài đặt](#cài-đặt)
- [Sử dụng](#sử-dụng)
  - [Chạy Crawler](#chạy-crawler)
  - [Xây dựng/Chạy RAG](#xây-dựngchạy-rag)
  - [Khởi chạy API](#khởi-chạy-api)
- [Công nghệ sử dụng](#công-nghệ-sử-dụng)

## Thành viên
- 23C01027 - Lê Nguyễn Thuỳ Dương 
- 23C01034 - Nguyễn Thiên Ngân
- 23C01044 - Võ Đức Trọng


## Giới thiệu

Việc lựa chọn một loại nước hoa phù hợp thường có thể là một trải nghiệm khó khăn với vô số lựa chọn khác nhau. Khách hàng thường cần tư vấn dựa trên sở thích cá nhân (nhóm hương, dịp sử dụng, độ lưu hương mong muốn), hoặc đơn giản là muốn tìm hiểu thông tin chi tiết về một sản phẩm cụ thể.

Dự án này nhằm giải quyết vấn đề đó bằng cách xây dựng một **Chatbot tư vấn nước hoa thông minh**. Mục tiêu là tạo ra một trợ lý ảo có khả năng:

* Hiểu và trả lời các câu hỏi của khách hàng về sản phẩm nước hoa (ví dụ: thành phần, nhóm hương, độ lưu hương, phù hợp với dịp nào?).
* Đưa ra gợi ý sản phẩm phù hợp dựa trên mô tả hoặc yêu cầu của khách hàng.
* Cung cấp thông tin chi tiết gợi ý sản phẩm phù hợp

Bằng cách sử dụng kỹ thuật **Retrieval-Augmented Generation (RAG)** dựa trên dữ liệu đã thu thập, chatbot có thể cung cấp các câu trả lời chính xác và phù hợp với ngữ cảnh, từ đó nâng cao trải nghiệm mua sắm và giúp khách hàng đưa ra quyết định tốt hơn.

## Workflow Dự án

Quy trình tổng thể của dự án bao gồm ba giai đoạn chính:

### 1. Thu thập dữ liệu (Crawl data)

- **Mục tiêu:** Thu thập dữ liệu văn bản thô từ `https://namperfume.net`.
- **Phương pháp:** Sử dụng BeautifulSoup để tự động trích xuất nội dung cần thiết.
- **Lưu trữ:** Dữ liệu thô được làm sạch và lưu trữ dưới dạng CSV tại thư mục `data/namperfume_product.csv`.

### 2. Xây dựng RAG (Retrieval-Augmented Generation)

- **Mục tiêu:** Xây dựng một hệ thống có khả năng tìm kiếm thông tin liên quan từ kho dữ liệu đã thu thập và sử dụng thông tin đó để tạo ra câu trả lời mạch lạc, chính xác cho câu hỏi của người dùng.
- **Các bước chính:**
    1.  **Embedding:** Chuyển đổi dữ liệu văn bản đã thu thập thành các vector embedding sử dụng mô hình **paraphrase-multilingual-mpnet-base-v2**.
    2.  **Indexing:** Lưu trữ các vector embedding vào cơ sở dữ liệu vector **ChromaDB** để tối ưu hóa việc tìm kiếm.
    3.  **Retrieval:** Khi có câu hỏi từ người dùng, chuyển câu hỏi thành vector embedding và tìm kiếm các đoạn văn bản có vector gần nhất trong cơ sở dữ liệu vector.
    5.  **Generation:** Sử dụng một Mô hình Ngôn ngữ Lớn (LLM) như Gemini kết hợp với câu hỏi gốc và các đoạn văn bản đã tìm được để sinh ra câu trả lời cuối cùng.
- **Chi tiết thực hiện :**

<img width="1593" alt="image" src="https://github.com/user-attachments/assets/7411d4c0-f057-4e96-b8fb-ef2e6943f063" />


 _BƯỚC 1:_ Tạo cuộc hội thoại với khác hàng, Chatbot sẽ tạo ra các câu hỏi để khác thác các thông tin về nhu cầu mua nước hoa của người dùng
 - Mùi hương khách hàng yêu thích là gì? (Ví dụ: tươi mát, hoa cỏ, gỗ, trái cây, vani,...)
 - Xác định giới tính của khách hàng sử dụng? Mua cho bản thân hay mua tặng cho ai?
 - Khách hàng muốn sử dụng nước hoa cho mục đích gì? (Hàng ngày, dịp đặc biệt, đi làm, hẹn hò,...)* Phong cách mà khách hàng hướng đến là gì? (Năng động, thanh lịch, lãng mạn, cá tính, quyến rũ,...)
 - Khách hàng mong muốn nước hoa mang lại cảm giác gì? (Tự tin, thư giãn, nổi bật, ấm áp,...)
 - Thời tiết hoặc mùa nào mà khách hàng thường sử dụng nước hoa?
 - Ngân sách mà khách hàng dự định chi cho nước hoa là bao nhiêu?
 - Khách hàng có thương hiệu nước hoa yêu thích nào không?

  **PROMT**
  
       ```
       Bạn là trợ lý ảo của Namperfume, chuyên tư vấn nước hoa. Hãy bắt đầu cuộc trò chuyện một cách tự nhiên và đặt câu hỏi một cách linh hoạt để hiểu rõ sở thích của khách hàng. Dưới đây là một số gợi ý về thông tin bạn có thể thu thập:
       * Mùi hương khách hàng yêu thích là gì? (Ví dụ: tươi mát, hoa cỏ, gỗ, trái cây, vani,...)
       * Xác định giới tính của khách hàng sử dụng? Mua cho bản thân hay mua tặng cho ai?
       * Khách hàng muốn sử dụng nước hoa cho mục đích gì? (Hàng ngày, dịp đặc biệt, đi làm, hẹn hò,...)* Phong cách mà khách hàng hướng đến là gì? (Năng động, thanh lịch, lãng mạn, cá tính, quyến rũ,...)
       * Khách hàng mong muốn nước hoa mang lại cảm giác gì? (Tự tin, thư giãn, nổi bật, ấm áp,...)
       * Thời tiết hoặc mùa nào mà khách hàng thường sử dụng nước hoa?
       * Ngân sách mà khách hàng dự định chi cho nước hoa là bao nhiêu?
       * Khách hàng có thương hiệu nước hoa yêu thích nào không?

       **Lưu ý quan trọng:**
       * Không nhất thiết phải hỏi tất cả các câu hỏi. Hãy lắng nghe câu trả lời của khách hàng và đặt câu hỏi tiếp theo một cách tự nhiên dựa trên thông tin đã có.
       * Nếu bạn cảm thấy đã thu thập đủ thông tin để đưa ra gợi ý phù hợp, hãy chuyển sang bước giới thiệu sản phẩm mà không cần hỏi thêm.
       * Ưu tiên tạo ra một cuộc trò chuyện thoải mái và hữu ích cho khách hàng.
       * Chỉ hỏi chưa tư vấn sản phẩm cụ thể nào.
       * Sau khi thu thập đủ thông tin thì nói khách hàng đợi để tìm kiếm sản phẩm phù hợp
       ######
       ChatBot: Chào bạn, mình là trợ lý ảo của Namperfume. Rất vui được hỗ trợ bạn tìm kiếm mùi hương ưng ý. Bạn có thể cho mình biết bạn đang tìm kiếm loại nước hoa như thế nào không?
       Khách hàng: {question}
       ChatBot:

  _BƯỚC 2:_ Khi Chatbot đã thu thập đủ thông tin của khách hàng bằng kỹ thuật **Query Transformations** phân tích nhu cầu của khách hàng dựa vào lịch sử trò chuyện với khách hàng. Tạo ra 5 mô tả chi tiết về nhu cầu của khách hàng.
  
  **PROMT**

      ```
      Dựa vào lịch sử trò chuyện sau đây, bạn hãy đóng vai trò là một chuyên gia tư vấn nước hoa cao cấp. Nhiệm vụ của bạn là tạo ra **năm mô tả chi tiết và đa dạng** về sở thích, nhu cầu và mong muốn của khách hàng, nhằm mục đích tìm kiếm các mẫu nước hoa phù hợp nhất từ cơ sở dữ liệu vector.
      **Mục tiêu:** Bằng cách khai thác các khía cạnh khác nhau trong yêu cầu của khách hàng, bạn sẽ giúp hệ thống vượt qua những hạn chế của phương pháp tìm kiếm tương tự dựa trên khoảng cách đơn thuần, từ đó mang đến kết quả chính xác và phù hợp hơn.
      **Lịch sử trò chuyện:**
      {history_chat}
      **Yêu cầu:**
      * Mỗi mô tả cần tập trung vào việc phân tích và làm rõ các yếu tố sau:
        * Giới tính của khách hàng: Nam/Nữ
        * Mùi hương yêu thích: (ví dụ: tươi mát, hoa cỏ, gỗ, trái cây, vani,...)
        * Mục đích sử dụng: (ví dụ: hàng ngày, dịp đặc biệt, đi làm, hẹn hò,...)
        * Phong cách cá nhân: (ví dụ: năng động, thanh lịch, lãng mạn, cá tính, quyến rũ,...)
        * Ngân sách dự kiến: (ví dụ: 1.000.000 đồng - 2.000.000 đồng, 1.500.000 đồng - 2.000.000 đồng, ...)
      * Sử dụng ngôn ngữ chuyên nghiệp, tinh tế và giàu hình ảnh để truyền tải chính xác cảm xúc và mong muốn của khách hàng.
      * Tạo ra các mô tả có góc nhìn khác nhau, nhấn mạnh vào các khía cạnh khác nhau trong sở thích của khách hàng.
      * Đảm bảo mỗi mô tả đều đủ chi tiết để hệ thống có thể hiểu rõ và tìm kiếm hiệu quả trong cơ sở dữ liệu vector.
      * Mô tả cần đúng định dạng đầu ra.
    
      **Định dạng đầu ra:**
      Mô tả 1: [Mô tả chi tiết với góc nhìn 1]
      Mô tả 2: [Mô tả chi tiết với góc nhìn 2]
      Mô tả 3: [Mô tả chi tiết với góc nhìn 3]
      Mô tả 4: [Mô tả chi tiết với góc nhìn 4]
      Mô tả 5: [Mô tả chi tiết với góc nhìn 5]

 _BƯỚC 3:_ Sử dụng 5 mô tả được tạo để thực hiện **Retrieval** thông tin sản phẩm phù hợp từ **Vector DB**. Với mỗi mô tả tôi thực hiện **Retrieval** top 5 sản phẩm phù hợp

 _BƯỚC 4:_ Sau khi đã có danh sách sản phẩm chúng tôi thực hiện **Re-ranking** sản phẩm bằng cách sử dụng một LLM khác để chọn ra 3 sản phẩm phù hợp nhất.

  **PROMT**
       
       ```
        Dưới đây là danh sách các sản phẩm nước hoa gợi ý. Nhiệm vụ của bạn là chọn ra 3 sản phầm phù hợp nhất với những thông tin thu thập từ khách hàng
        
        ###########
        DƯỚI ĐÂY LÀ 5 MÔ TẢ (5 MÔ TẢ NÀY ĐƯỢC TẠO RA TỪ THÔNG TIN THU THẬP TỪ 1 KHÁCH HÀNG) SẢN PHẨM CỦA MỘT KHÁCH HÀNG VỀ NHU CẦU MUA NƯỚC HOA
        
        {response}
        
        ##########
        DANH SÁCH SẢN PHẨM 


### 3. Xây dựng API

- **Mục tiêu:** Cung cấp một giao diện lập trình ứng dụng (API) để người dùng hoặc các ứng dụng khác có thể tương tác với hệ thống RAG.
- **Framework:** Xây dựng bằng [Tên API framework, ví dụ: FastAPI, Flask, Django REST framework].
- **Endpoints:**
    - `POST /query`: Nhận câu hỏi từ người dùng, xử lý qua hệ thống RAG và trả về câu trả lời.
    - `GET /health`: Kiểm tra tình trạng hoạt động của API.
    - `[Thêm các endpoints khác nếu có]`
- **Chi tiết:** [Mô tả về định dạng input/output của API, cách xác thực (nếu có), ví dụ về request/response.]

## Cài đặt

