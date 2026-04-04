# LAB 1 - API
#  Question Answering API
---

## 1. Thông tin sinh viên
- **Họ tên:** *Dương Ngọc Minh Thư*
- **MSSV:** 24120144
- **Mã lớp:** 24CTT5

---

## 2. Mô hình sử dụng
- **Tên mô hình:** `distilbert-base-cased-distilled-squad`
- **Liên kết tới mô hình:** https://huggingface.co/distilbert-base-cased-distilled-squad

## 3. Mô tả chức năng của hệ thống
API Hỏi đáp (Question Answering) là hệ thống tiếp nhận các truy vấn dưới dạng ngôn ngữ tự nhiên, tự động phân tích và tra cứu thông tin chính xác từ tập dữ liệu định sẵn. Kết quả phản hồi được chuẩn hóa dưới định dạng JSON

## 4. Cài đặt các thư viện

### Yêu cầu hệ thống
- Python 3.8 trở lên
- Git

### Bước 1 - Clone repository
```bash
git clone https://github.com/dnmthuw/Lab-1-API
```

### Bước 2 - Tạo môi trường ảo

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

> Khi môi trường ảo đã được kích hoạt, bạn sẽ thấy `(venv)` xuất hiện ở đầu dòng lệnh.

### Bước 3 — Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### Tắt môi trường ảo (khi dùng xong)
```bash
deactivate
```

## 5. Chạy chương trình

### Bước 1 — Chạy server (trên Google Colab)
Mở file `lab_1_api.ipynb` trên Google Colab và chạy từng cell theo thứ tự từ trên xuống dưới (có thể chọn Runtime Type là T4 GPU)

### Bước 2 — Tạo tunnel public (Pinggy)
Chạy lệnh sau trong terminal của Colab để tạo địa chỉ public:
```bash
ssh -p 443 -R0:localhost:8000 qr@a.pinggy.io
```
Copy link được sinh ra (ví dụ: `http://oxlng-xxx.run.pinggy-free.link`) và thay vào `BASE_URL` trong file `test_api.py`.

### Bước 3 — Chạy file test
```bash
python test_api.py
```

## Ví dụ gọi API

### GET /
```bash
curl http://your-link.pinggy.link/
```
Response:
```json
{"system": "LAB 1: Question Answering API", "model": "distilbert-base-cased-distilled-squad", "description": "The Question Answering API retrieves answers from a predefined dataset based on user queries and returns them in JSON format"}
```

### GET /health
```bash
curl http://your-link.pinggy.link/health
```
Response:
```json
{"status": "ok"}
```

### POST /predict
```bash
curl -X POST http://your-link.pinggy.link/predict \
     -H "Content-Type: application/json" \
     -d '{"question": "What is the capital of Vietnam?"}'
```
Response:
```json
{"question": "What is the capital of Vietnam?", "answer": "Hanoi"}
```

## Video demo
