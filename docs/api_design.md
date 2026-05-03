# Thiết kế API cho Hệ thống CareLoop

Dựa trên các màn hình HTML của hệ thống CareLoop (Patient Dashboard, Appointments, Chatbot, Relative Settings, Relative Support, Missed Appointment), dưới đây là thiết kế chi tiết cho các API cần thiết để phục vụ các chức năng của ứng dụng.

## 1. Users & Relatives (Người dùng & Người thân)

Các API quản lý thông tin bệnh nhân và cài đặt người thân hỗ trợ (từ `patient_dashboard.html`, `patient_relative_settings.html`).

### `GET /api/v1/users/me`
- **Mô tả**: Lấy thông tin cá nhân của người dùng hiện tại (Tên, tuổi, avatar...).
- **Response**:
  ```json
  {
    "id": "u123",
    "name": "Bác Hùng",
    "avatar_url": "https://...",
    "overall_health_status": "Sức khỏe của bác đang rất tốt..."
  }
  ```

### `GET /api/v1/users/relatives`
- **Mô tả**: Lấy danh sách người thân đã được kết nối.
- **Response**:
  ```json
  [
    {
      "id": "rel1",
      "name": "Anh Tuấn",
      "relationship": "Con trai",
      "phone": "090xxxx123",
      "is_connected": true,
      "allow_notifications": true
    }
  ]
  ```

### `POST /api/v1/users/relatives`
- **Mô tả**: Gửi lời mời hoặc thêm người thân mới.
- **Body**: `{ "name": "...", "phone": "...", "relationship": "..." }`

### `PUT /api/v1/users/relatives/:id/notifications`
- **Mô tả**: Bật/tắt quyền gửi thông báo lịch tái khám cho người thân cụ thể.
- **Body**: `{ "allow_notifications": false }`

---

## 2. Appointments (Lịch hẹn & Thăm khám)

Các API quản lý lịch khám bệnh, xác nhận, dời lịch và tóm tắt kết quả (từ `patient_dashboard.html`, `patient_appointments.html`, `relative_support.html`).

### `GET /api/v1/appointments/next`
- **Mô tả**: Lấy thông tin lịch hẹn sắp tới nhất cần xác nhận.
- **Response**:
  ```json
  {
    "id": "app_1",
    "title": "Tái khám Đái tháo đường",
    "location": "Bệnh viện ĐHYD",
    "date": "2025-05-20",
    "time": "08:30",
    "status": "NEEDS_CONFIRMATION" 
  }
  ```

### `PUT /api/v1/appointments/:id/confirm`
- **Mô tả**: Bệnh nhân tự xác nhận lịch khám.

### `PUT /api/v1/appointments/:id/reschedule`
- **Mô tả**: Yêu cầu đổi lịch hoặc hủy lịch khám.
- **Body**: `{ "action": "reschedule", "new_date": "...", "reason": "..." }`

### `POST /api/v1/appointments/:id/relative-confirm`
- **Mô tả**: Người thân xác nhận lịch khám thay cho bệnh nhân (từ `relative_support.html`).

### `GET /api/v1/appointments/last-summary`
- **Mô tả**: Lấy tóm tắt kết quả lâm sàng của lần khám gần nhất.
- **Response**:
  ```json
  {
    "date": "2026-04-18",
    "clinical_summary": "Sức khỏe ổn định",
    "metrics": ["Huyết áp: 120/80 mmHg", "Đường huyết: 7.2 mmol/L"],
    "doctor_notes": "Tiếp tục duy trì phác đồ điều trị hiện tại",
    "warning": "Lưu ý: Giảm tinh bột buổi tối.",
    "next_steps": "Duy trì thói quen vận động 30 phút mỗi ngày trước lần khám tới.",
    "next_appointment_date": "2026-05-15"
  }
  ```

---

## 3. Health Metrics & Medications (Chỉ số sức khỏe & Thuốc)

Cung cấp dữ liệu đo lường sức khỏe cho Dashboard và biểu đồ xu hướng (từ `patient_dashboard.html`, `patient_appointments.html`, `relative_support.html`).

### `GET /api/v1/metrics/latest`
- **Mô tả**: Lấy các chỉ số sức khỏe mới nhất (Đường huyết, Huyết áp) để hiển thị trên thẻ (Card).
- **Response**:
  ```json
  {
    "blood_glucose": { "value": 7.2, "unit": "mmol/L", "status": "GOOD", "updated_at": "30 phút trước" },
    "blood_pressure": { "value": "135/85", "unit": "mmHg", "status": "STABLE", "updated_at": "1 giờ trước" }
  }
  ```

### `GET /api/v1/metrics/trend`
- **Mô tả**: Lấy dữ liệu lịch sử để vẽ biểu đồ xu hướng (ví dụ: Blood Glucose Chart).
- **Query Params**: `?type=blood_glucose&days=7`
- **Response**:
  ```json
  [
    { "date": "15/04", "value": 6.8 },
    { "date": "16/04", "value": 7.5 },
    { "date": "17/04", "value": 7.2 }
  ]
  ```

### `GET /api/v1/medications/status`
- **Mô tả**: Lấy trạng thái uống thuốc trong ngày (để hiển thị cho người thân).
- **Response**:
  ```json
  {
    "status": "TAKEN", 
    "time": "Sáng nay"
  }
  ```

---

## 4. AI Advisor & Chatbot (Trợ lý AI CareLoop)

Các API phục vụ giao diện trò chuyện, phân tích dữ liệu AI và video (từ `patient_chatbot.html`, `patient_appointments.html`, `relative_support.html`).

### `POST /api/v1/ai/chat`
- **Mô tả**: Gửi tin nhắn (văn bản hoặc được chuyển từ giọng nói) tới AI Advisor.
- **Body**:
  ```json
  {
    "message": "Cách dùng thuốc Metformin",
    "attachments": [] 
  }
  ```
- **Response**:
  ```json
  {
    "reply": "Bác nên uống Metformin vào sau bữa ăn...",
    "sources": []
  }
  ```

### `POST /api/v1/ai/upload-attachment`
- **Mô tả**: Tải lên hình ảnh (ví dụ đơn thuốc, kết quả xét nghiệm) để AI phân tích trong phiên chat.

### `GET /api/v1/ai/suggestions`
- **Mô tả**: Lấy danh sách các câu hỏi gợi ý hiển thị nhanh cho người dùng.

### `GET /api/v1/ai/insights`
- **Mô tả**: Lấy các phân tích/gợi ý chủ động từ AI cho bệnh nhân hoặc người thân (VD: "Chỉ số ổn định. Tiếp tục duy trì chế độ ăn ít tinh bột").

### `GET /api/v1/ai/video-advice`
- **Mô tả**: Lấy video AI Advisor tóm tắt dặn dò sau khám.
- **Response**:
  ```json
  {
    "video_url": "https://...",
    "thumbnail_url": "https://...",
    "title": "Video giải thích tóm tắt",
    "description": "..."
  }
  ```

---

## 5. Notifications & Alerts (Thông báo & Cảnh báo)

Các API phục vụ hệ thống cảnh báo khẩn cấp, đặc biệt cho người thân (từ `relative_missed_appointment.html`).

### `GET /api/v1/notifications`
- **Mô tả**: Lấy danh sách thông báo và cảnh báo (Ví dụ: "Cảnh báo trễ hạn", "Bệnh nhân chưa xác nhận lịch").

### `GET /api/v1/notifications/:id`
- **Mô tả**: Lấy chi tiết một cảnh báo cụ thể, bao gồm AI Insight (VD: "Bác Hùng thường có xu hướng quên lịch hẹn vào cuối tuần...").

### `PUT /api/v1/notifications/:id/dismiss`
- **Mô tả**: Bỏ qua thông báo / Đánh dấu đã đọc.
