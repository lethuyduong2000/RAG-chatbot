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
    1.  **Embedding:** Chuyển đổi dữ liệu văn bản đã thu thập thành các vector embedding sử dụng mô hình [Tên mô hình embedding, ví dụ: sentence-transformers, OpenAI ada-002].
    2.  **Indexing:** Lưu trữ các vector embedding vào một cơ sở dữ liệu vector (vector database) như [Tên vector DB, ví dụ: FAISS, ChromaDB, Pinecone, Milvus] để tối ưu hóa việc tìm kiếm.
    3.  **Retrieval:** Khi có câu hỏi từ người dùng, chuyển câu hỏi thành vector embedding và tìm kiếm các đoạn văn bản có vector gần nhất trong cơ sở dữ liệu vector.
    4.  **Generation:** Sử dụng một Mô hình Ngôn ngữ Lớn (LLM) như [Tên LLM, ví dụ: GPT-4, Llama 3, Gemini] kết hợp với câu hỏi gốc và các đoạn văn bản đã tìm được (context) để sinh ra câu trả lời cuối cùng.
- **Thư viện/Framework:** Sử dụng [Tên thư viện RAG, ví dụ: LangChain, LlamaIndex] để tích hợp các thành phần trên.
- **Chi tiết:** [Mô tả thêm về cấu hình RAG, cách chọn top-k văn bản, cách xây dựng prompt cho LLM.]

### 3. Xây dựng API

- **Mục tiêu:** Cung cấp một giao diện lập trình ứng dụng (API) để người dùng hoặc các ứng dụng khác có thể tương tác với hệ thống RAG.
- **Framework:** Xây dựng bằng [Tên API framework, ví dụ: FastAPI, Flask, Django REST framework].
- **Endpoints:**
    - `POST /query`: Nhận câu hỏi từ người dùng, xử lý qua hệ thống RAG và trả về câu trả lời.
    - `GET /health`: Kiểm tra tình trạng hoạt động của API.
    - `[Thêm các endpoints khác nếu có]`
- **Chi tiết:** [Mô tả về định dạng input/output của API, cách xác thực (nếu có), ví dụ về request/response.]

## Cài đặt

