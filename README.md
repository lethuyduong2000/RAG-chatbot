# RAG-chatbot
RAG-based Chatbot for retail e-commerce

## Mục lục

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
- [Thành viên](#liên-hệ)

## Giới thiệu


## Workflow Dự án

Quy trình tổng thể của dự án bao gồm ba giai đoạn chính:

### 1. Thu thập dữ liệu (Crawl data)

- **Mục tiêu:** Thu thập dữ liệu văn bản thô từ [Nguồn dữ liệu cụ thể, ví dụ: trang web ABC, tài liệu XYZ].
- **Phương pháp:** Sử dụng [Tên thư viện/framework crawl, ví dụ: Scrapy, BeautifulSoup, Selenium] để tự động trích xuất nội dung cần thiết.
- **Lưu trữ:** Dữ liệu thô được làm sạch và lưu trữ dưới dạng [Định dạng file, ví dụ: JSON, CSV, text files] tại thư mục `[đường_dẫn/tới/dữ_liệu_thô]`.
- **Chi tiết:** [Mô tả thêm về cấu hình crawler, cách xử lý các trang động (nếu có), hoặc các bước tiền xử lý dữ liệu thô.]

### 2. Xây dựng RAG (Retrieval-Augmented Generation)

- **Mục tiêu:** Xây dựng một hệ thống có khả năng tìm kiếm thông tin liên quan từ kho dữ liệu đã thu thập và sử dụng thông tin đó để tạo ra câu trả lời mạch lạc, chính xác cho câu hỏi của người dùng.
- **Các bước chính:**
    1.  **Embedding:** Chuyển đổi dữ liệu văn bản đã thu thập thành các vector embedding sử dụng mô hình **paraphrase-multilingual-mpnet-base-v2**.
    2.  **Indexing:** Lưu trữ các vector embedding vào cơ sở dữ liệu vector **ChromaDB** để tối ưu hóa việc tìm kiếm.
    3.  **Retrieval:** Khi có câu hỏi từ người dùng, chuyển câu hỏi thành vector embedding và tìm kiếm các đoạn văn bản có vector gần nhất trong cơ sở dữ liệu vector.
    5.  **Generation:** Sử dụng một Mô hình Ngôn ngữ Lớn (LLM) như Gemini kết hợp với câu hỏi gốc và các đoạn văn bản đã tìm được để sinh ra câu trả lời cuối cùng.
- **Chi tiết thực hiện :**
    1. Tạo cuộc hội thoại với khác hàng
    ```text
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
* Sau khi thu thập đủ thông tin thì nói khách hàng đợi để tìm kiếm sản phẩm phù hợp

######
ChatBot: Chào bạn, mình là trợ lý ảo của Namperfume. Rất vui được hỗ trợ bạn tìm kiếm mùi hương ưng ý. Bạn có thể cho mình biết bạn đang tìm kiếm loại nước hoa như thế nào không?

Khách hàng: {question}

ChatBot:
```



### 3. Xây dựng API

- **Mục tiêu:** Cung cấp một giao diện lập trình ứng dụng (API) để người dùng hoặc các ứng dụng khác có thể tương tác với hệ thống RAG.
- **Framework:** Xây dựng bằng [Tên API framework, ví dụ: FastAPI, Flask, Django REST framework].
- **Endpoints:**
    - `POST /query`: Nhận câu hỏi từ người dùng, xử lý qua hệ thống RAG và trả về câu trả lời.
    - `GET /health`: Kiểm tra tình trạng hoạt động của API.
    - `[Thêm các endpoints khác nếu có]`
- **Chi tiết:** [Mô tả về định dạng input/output của API, cách xác thực (nếu có), ví dụ về request/response.]

## Cài đặt

