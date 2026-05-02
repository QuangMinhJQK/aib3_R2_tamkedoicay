# CareLoop – Ứng dụng chăm sóc sức khỏe

Gồm 6 màn hình (frame) cho **bệnh nhân** và **người thân**, hỗ trợ theo dõi chỉ số, lịch hẹn, chatbot AI và cảnh báo trễ hẹn.

---

## 📱 Các frame chính

### 🧑‍⚕️ Luồng bệnh nhân (Bác Hùng)

| Frame | Tên file | Chức năng |
|-------|----------|------------|
| 1 | `patient_dashboard.html` | Trang chủ: chào, AI Advisor, chỉ số nhanh (đường huyết, huyết áp), lịch hẹn sắp tới. |
| 2 | `patient_appointments.html` | Chi tiết kết quả khám, biểu đồ đường huyết, video dặn dò từ bác sĩ AI. |
| 3 | `patient_chatbot.html` | Chat với AI Advisor: hỏi về thuốc, chế độ ăn, chỉ số. Hỗ trợ nhập văn bản/giọng nói. |
| 4 | `patient_relative_settings.html` | Cài đặt người thân hỗ trợ: thêm, xóa, bật/tắt thông báo cho người nhà. |

**🔁 Điều hướng giữa 4 frame:** Dùng thanh bottom nav (Trang chủ, Lịch hẹn, AI Advisor, Tài khoản) – có sẵn trong mỗi file.

---

### 👨‍👩‍👧 Luồng người thân (Anh Tuấn)

| Frame | Tên file | Chức năng |
|-------|----------|------------|
| 5 | `relative_support.html` | Màn hình chính của người thân: xem tóm tắt sức khỏe của bác Hùng, nhận cảnh báo trễ hẹn. |
| 6 | `relative_missed_appointment.html` | Màn hình cảnh báo khẩn cấp: chi tiết lịch trễ, gợi ý từ AI, nút gọi điện / xác nhận thay. |

**🔁 Điều hướng giữa 2 frame:**  
- Từ `relative_support.html`, nhấn vào nút “Chi tiết” hoặc toàn bộ thẻ cảnh báo → chuyển sang `relative_missed_appointment.html`.  
- Từ `relative_missed_appointment.html`, nhấn nút **Quay lại** (góc trái header) → về `relative_support.html`.

---

## 🚀 Cách chạy

- **Mở trước:** `patient_dashboard.html` (nếu xem vai bệnh nhân) hoặc `relative_support.html` (nếu xem vai người thân).  
- Các file còn lại sẽ được điều hướng tự động từ bottom nav hoặc nút bấm bên trong.

> Hiện tại chưa có cơ chế đăng nhập – bạn cần chọn thủ công vai trò bằng cách mở đúng file.  
> Dự án chỉ hoạt động thuần trên trình duyệt, không cần cài đặt thêm.
