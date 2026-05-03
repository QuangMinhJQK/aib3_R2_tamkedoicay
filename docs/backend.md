# Backend CareLoop

Tài liệu này mô tả nhanh cấu trúc backend hiện tại của CareLoop, các module chính, luồng dữ liệu và các API quan trọng đang được dùng bởi frontend và pipeline tạo video.

## 1. Tổng quan

Backend được viết bằng FastAPI, dùng SQLite làm database, và chia theo các lớp:

- `api/endpoints`: các route HTTP.
- `services`: logic nghiệp vụ.
- `schemas`: model Pydantic cho request/response.
- `models`: model dữ liệu phục vụ nội bộ và pipeline video.
- `core/database.py`: kết nối SQLite.
- `services/video`: pipeline tạo video personalized bằng Remotion + FFmpeg.

## 2. Cấu trúc chính

### `backend/main.py`
Entry point của FastAPI app. Nơi mount router và cấu hình ứng dụng.

### `backend/app/api/endpoints/`
- `appointments.py`: lịch hẹn, summary lần khám gần nhất.
- `metrics.py`: dữ liệu chỉ số sức khỏe và lịch sử.
- `ai.py`: chat AI, video advice, cập nhật video URL.
- `video.py`: tạo video personalized và tra trạng thái job.
- `users.py`, `notifications.py`: người dùng và thông báo.

### `backend/app/services/`
- `appointment_service.py`: lấy summary lần khám, gọi Gemini khi cần, cache vào `medical_records.ai_summary`.
- `metric_service.py`: lấy số liệu mới nhất, trend, lịch sử clinical metrics.
- `ai_service.py`: AI insights, video advice, cập nhật `ai_video_url`.
- `job_service.py`: lưu trạng thái job render video vào DB.
- `video/pipeline.py`: điều phối toàn bộ pipeline tạo video.
- `video/llm_agent.py`: sinh nội dung có cấu trúc cho video.
- `video/tts_engine.py`: tạo audio từ text.
- `video/subtitle_generator.py`: tạo subtitle.
- `video/remotion_runner.py`: render composition Remotion.
- `video/video_compositor.py`: ghép audio/video bằng FFmpeg.
- `video/cleanup.py`: dọn file tạm.

### `backend/app/schemas/`
Định nghĩa request/response cho API.

### `backend/app/models/video_schema.py`
Contract Pydantic giữa backend và `video_renderer`.
Các trường quan trọng:
- `patientName`
- `overallStatus`
- `metrics`
- `advices`
- `sectionNarrations`
- `sectionDurationsInFrames`
- `clinicalHistory`

## 3. Luồng summary lâm sàng

Luồng summary hiện tại ở `appointment_service.get_last_summary(patient_id)`:

1. Lấy medical record mới nhất theo patient.
2. Nếu `ai_summary` đã là JSON hợp lệ, parse và trả về cache.
3. Nếu chưa có cache, lấy clinical metrics gần nhất.
4. Gọi `generate_clinical_summary()` trong `gemini_service.py`.
5. Lưu JSON kết quả vào `medical_records.ai_summary`.
6. Trả response cho frontend hoặc pipeline video.

### Cột DB liên quan
- `medical_records.ai_summary`: summary AI dạng JSON string.
- `medical_records.ai_video_url`: đường dẫn video đã render.

## 4. Luồng tạo video

Video generation bắt đầu từ `POST /api/v1/videos/generate`:

1. Lấy summary bệnh nhân bằng `get_last_summary(patient_id)`.
2. Tạo `job_id`.
3. Tạo record job trong bảng `video_jobs` qua `job_service.create_job()`.
4. Gửi job vào `run_video_pipeline()`.
5. Pipeline tạo `MasterProps`.
6. Remotion render `silent_video.mp4`.
7. FFmpeg ghép audio và video thành file mp4 cuối.
8. Cập nhật:
   - `video_jobs.video_url`
   - `medical_records.ai_video_url`

### API job
- `GET /api/v1/videos/{job_id}/status`: lấy trạng thái job từ DB trước, fallback sang memory.
- `GET /api/v1/videos/`: liệt kê job gần đây.

## 5. API chính

### Appointments
- `GET /api/v1/appointments/next`
- `GET /api/v1/appointments/last-summary`
- `PUT /api/v1/appointments/{id}/confirm`
- `PUT /api/v1/appointments/{id}/reschedule`
- `POST /api/v1/appointments/{id}/relative-confirm`

### Metrics
- `GET /api/v1/metrics/latest`
- `GET /api/v1/metrics/trend`
- `GET /api/v1/metrics/history`

### AI
- `POST /api/v1/ai/chat`
- `GET /api/v1/ai/suggestions`
- `GET /api/v1/ai/insights`
- `GET /api/v1/ai/video-advice`
- `PUT /api/v1/ai/video-url`

### Video
- `POST /api/v1/videos/generate`
- `GET /api/v1/videos/{job_id}/status`
- `GET /api/v1/videos/`

## 6. Database

CSDL nằm ở `backend/data/careloop.db`.

### Bảng quan trọng
- `patients`
- `appointments`
- `medical_records`
- `clinical_metrics`
- `video_jobs`
- `generation_jobs`  
- `communication_logs`

### Ghi chú
- `get_db()` trong `core/database.py` tự commit khi thoát context.
- Foreign keys được bật bằng `PRAGMA foreign_keys = ON`.

## 7. Biến môi trường quan trọng

- `GEMINI_API_KEY`: dùng cho summary lâm sàng.
- `VIDEO_PER_SERIES_FRAMES`: số frame cộng thêm cho mỗi series clinical history trong video.
- `VIDEO_BASE_URL`: nếu muốn lưu URL public thay vì path file local.

## 8. Ghi chú vận hành

- `appointment_service.get_last_summary()` là nguồn summary chuẩn cho cả UI và video.
- `ai_summary` hiện được dùng vừa như cache, vừa như dữ liệu hiển thị cho AI advisor.
- Nếu muốn đổi từ path local sang URL public cho `ai_video_url`, nên sửa tại `video/pipeline.py` và `ai_service.update_latest_video_url()`.

## 9. File liên quan để đọc tiếp

- `backend/app/services/appointment_service.py`
- `backend/app/services/gemini_service.py`
- `backend/app/services/video/pipeline.py`
- `backend/app/services/ai_service.py`
- `backend/app/services/job_service.py`
- `backend/app/models/video_schema.py`
