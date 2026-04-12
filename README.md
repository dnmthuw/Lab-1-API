# LAB 1: XÂY DỰNG API HỆ THỐNG HỎI ĐÁP (QUESTION ANSWERING)

## 1. Thông tin sinh viên
- **Họ tên:** Dương Ngọc Minh Thư
- **MSSV:** 24120144
- **Mã lớp:** 24CTT5

## 2. Mô hình sử dụng
- **Tên mô hình:** `distilbert-base-cased-distilled-squad`
- **Liên kết tới mô hình:** [HuggingFace - distilbert-base-cased-distilled-squad](https://huggingface.co/distilbert-base-cased-distilled-squad)

## 3. Mô tả chức năng của hệ thống
Dự án này là một API Web (được xây dựng bằng FastAPI) hỗ trợ tra cứu và trả lời câu hỏi tự động. Hệ thống sẽ đọc một tập văn bản tri thức định sẵn (`data/data.txt`) và sử dụng mô hình AI của HuggingFace để trích xuất ra câu trả lời chính xác nhất. Hệ thống bao gồm:
- API `GET /`: Hiển thị thông tin tổng quan của hệ thống
- API `GET /health`: Kiểm tra trạng thái hoạt động của máy chủ 
- API `POST /predict`: Chấp nhận câu hỏi người dùng, thực hiện suy luận và trả về câu trả lời ở định dạng JSON. Nó bao gồm các biện pháp xác thực dữ liệu và xử lý bắt lỗi ở mức cơ bản

## 4. Cấu trúc nguồn của dự án (Source Code Structure)
Dưới đây là cấu trúc các tệp tin trong dự án:

```
project_root/
│ 
├── app/                  # Chứa logic code chính của API Server
│   ├── main.py           # Khởi tạo FastAPI, định nghĩa các routers/endpoints & xử lý lỗi.
│   ├── model.py          # Class nạp mô hình HuggingFace, tải Text data và dự đoán kết quả.
│   └── __init__.py       # Đánh dấu thư mục app là 1 module Python.
│ 
├── config/               # Cấu hình tĩnh
│   └── config.yaml       # Lưu thông tin tên mô hình, đường dẫn data text, điểm tin cậy
│ 
├── data/                 # Thư mục lưu dữ liệu
│   └── data.txt          # Tập văn bản thô dùng làm ngữ cảnh cho mô hình tra cứu thông tin.
│ 
├── tests/                # Chứa file kiểm thử hệ thống
│   └── test_api.py       # Bộ Test tự động cho các đường dẫn sử dụng thư viện requests.
│ 
├── requirements.txt      # Danh sách thư viện bắt buộc
├── .env                  # Lưu trữ các biến môi trường cấu hình động
├── .gitignore            # Những file không đẩy lên github
└── README.md             # File hướng dẫn
```

## 5. Hướng dẫn cài đặt thư viện
Yêu cầu máy tính đã cài đặt sẵn **Python 3.8+**. Để chương trình vận hành chính xác, hãy thiết lập không gian ảo (Virtual Environment) và cài đặt thư viện theo các bước sau:

**Bước 1: Tạo và kích hoạt môi trường ảo**
```bash
python -m venv venv

# Dành cho Windows:
venv\Scripts\activate
# Dành cho MacOS/Linux:
source venv/bin/activate
```

**Bước 2: Cài đặt thư viện**
```bash
pip install -r requirements.txt
```

## 6. Hướng dẫn chạy chương trình
Sau khi đã cài đặt xong các thư viện, chạy lệnh sau ở Terminal (đã kích hoạt venv) để bắt đầu khởi động máy chủ API:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
- Máy chủ sẽ bắt đầu lắng nghe tại địa chỉ: `http://localhost:8000`. Cửa sổ terminal này phải được giữ mở trong suốt quá trình chạy.
- Giao diện tài liệu Swagger UI tự động: `http://localhost:8000/docs`.

### Hướng dẫn chạy Test tự động (Pytest)
Mở một cửa sổ Terminal THỨ HAI (phải để cửa sổ Số một vẫn đang chạy Uvicorn):
```bash
venv\Scripts\activate
pytest tests/test_api.py -v
```

### Hướng dẫn đưa API lên Public (Với Pinggy)
Nếu bạn muốn API có thể được gọi từ một máy tính rác hoặc thiết bị di động, bạn có thể thiết lập đường hầm Pinggy miễn phí (Không cần tắt Uvicorn hiện tại):
1. Mở một **Terminal mới** (Terminal thứ ba).
2. Chạy lệnh sau để chuyển hướng cổng 8000:
```bash
ssh -p 443 -R0:127.0.0.1:8000 a.pinggy.io
```
*(Nếu được hỏi "Are you sure you want to continue connecting?", hãy gõ `yes` và nhấn Enter).*

3. Sau vài giây, Pinggy sẽ cung cấp một đường link dạng `https://[id].a.free.pinggy.link`. Bạn có thể thay thế `http://localhost:8000` bằng đường link này để mọi người cùng test qua internet.

## 7. Hướng dẫn gọi API và Ví dụ (Request/Response)
Bạn có thể sử dụng cURL, Postman hoặc trực tiếp tương tác bằng trình duyệt qua **Swagger UI** tại `http://localhost:8000/docs`. Sau đây là ví dụ gọi bằng lệnh cURL:

### A. Endpoint `GET /`
- **Mô tả:** Trả về thông tin mô tả chức năng của hệ thống.

**Request:**
```bash
curl -X GET http://localhost:8000/
```
**Response (200 OK):**
```json
{
  "system": "LAB 1: Question Answering API",
  "model": "distilbert-base-cased-distilled-squad",
  "description": "The Question Answering API retrieves answers from a predefined dataset based on user queries and returns them in JSON format"
}
```

### B. Endpoint `GET /health`
- **Mô tả:** Kiểm tra trạng thái hoạt động của hệ thống

**Request:**
```bash
curl -X GET http://localhost:8000/health
```
**Response (200 OK):**
```json
{
  "status": "ok"
}
```

### C. Endpoint `POST /predict`
- **Mô tả:** Tiếp nhận câu hỏi dạng JSON, phân tích và trả về câu trả lời.

**Request:**
```bash
curl -X POST http://localhost:8000/predict \
     -H "Content-Type: application/json" \
     -d '{"question": "What is the capital of Vietnam?"}'
```
**Response (200 OK - Thành công):**
```json
{
  "question": "What is the capital of Vietnam?",
  "answer": "Hanoi"
}
```

**Response (400 Bad Request - Sai Format/Trống):**
```json
{
  "detail": "Question cannot be empty"
}
```

## 8. Liên kết Video Demo
Dưới đây là video quá trình hướng dẫn thao tác chạy hệ thống:

***[Video Demo Lab 1 API - QA Model](https://youtu.be/YcEV1pkAfvw)***