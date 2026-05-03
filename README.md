# CareLoop – Hệ sinh thái chăm sóc sức khỏe thông minh

CareLoop là một giải pháp toàn diện hỗ trợ bệnh nhân và người thân trong việc quản lý sức khỏe, theo dõi lịch hẹn và tư vấn y tế thông qua trí tuệ nhân tạo (AI). Dự án kết hợp giao diện người dùng hiện đại, hệ thống backend mạnh mẽ và mô hình dự báo XGBOOST.

---

## 📂 Cấu trúc dự án

- **`frontend/`**: Chứa các giao diện HTML/CSS/JS thuần cho Bệnh nhân và Người thân.
- **`backend/`**: Hệ thống API xây dựng trên FastAPI, quản lý dữ liệu, thông báo và tích hợp AI.
- **`XGBOOST/`**: Mô hình và dữ liệu dự báo (ví dụ: dự báo khả năng bỏ lỡ lịch hẹn).
- **`video_renderer/`**: Công cụ tạo video hướng dẫn cá nhân hóa (nếu có).

---

## 📱 Các tính năng chính

### 🧑‍⚕️ Dành cho Bệnh nhân (Patient Flow)
- **Dashboard**: Theo dõi chỉ số sức khỏe (đường huyết, huyết áp) và lịch hẹn sắp tới.
- **AI Advisor**: Chatbot tư vấn về đơn thuốc, chế độ ăn uống và nhắc nhở sức khỏe.
- **Lịch hẹn & Video**: Xem chi tiết lịch khám và video dặn dò từ bác sĩ AI.
- **Cài đặt người thân**: Quản lý danh sách và quyền nhận thông báo của người nhà.

### 👨‍👩‍👧 Dành cho Người thân (Relative Flow)
- **Support Dashboard**: Theo dõi tình trạng sức khỏe tổng quát của người thân.
- **Cảnh báo thông minh**: Nhận thông báo khẩn cấp nếu người thân bỏ lỡ lịch khám.
- **Hành động nhanh**: Gọi điện trực tiếp hoặc xác nhận thay đổi lịch hẹn cho người thân.

---

## 🛠️ Hướng dẫn cài đặt & Chạy ứng dụng

### 1. Yêu cầu hệ thống
- Python 3.8+
- Trình duyệt web hiện đại (Chrome, Edge, v.v.)

### 2. Cài đặt Backend
Mở terminal tại thư mục gốc của dự án:

```bash
# Tạo môi trường ảo (khuyến nghị)
python -m venv .venv
source .venv/bin/activate  # Trên Windows: .venv\Scripts\activate

# Cài đặt các thư viện cần thiết
pip install -r requirements.txt
```

### 3. Cấu hình môi trường
Sao chép tệp `.env.example` thành `.env` và điền các API Key cần thiết:
```bash
cp .env.example .env
```
Các thông số quan trọng:
- `GOOGLE_API_KEY`: Dùng cho các dịch vụ AI của Google (Gemini).
- `ELEVENLABS_API_KEY`: Dùng cho dịch vụ chuyển đổi văn bản thành giọng nói (TTS).

### 4. Chạy Backend API
Chạy lệnh sau để khởi động server:

```bash
uvicorn backend.main:app --reload --port 8000
```
- API sẽ chạy tại: `http://localhost:8000`
- Tài liệu API (Swagger UI): `http://localhost:8000/docs`

### 5. Xem Frontend
Mở trực tiếp các tệp HTML trong thư mục `frontend/` bằng trình duyệt:
- Bệnh nhân: `frontend/patient_dashboard.html`
- Người thân: `frontend/relative_support.html`

*Lưu ý: Đảm bảo Backend đang chạy để các tính năng dữ liệu và AI hoạt động chính xác.*

---

## 🤖 Công nghệ sử dụng
- **Frontend**: HTML5, CSS3 (Vanilla CSS), JavaScript (ES6+).
- **Backend**: Python, FastAPI, SQLite (Cơ sở dữ liệu), Uvicorn.
- **AI/ML**: Google Gemini API, OpenAI API, ElevenLabs TTS, XGBoost.

---
© 2024 CareLoop Team - Advanced Agentic Coding.
