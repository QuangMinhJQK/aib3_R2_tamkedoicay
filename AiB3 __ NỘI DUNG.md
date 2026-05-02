# **OUTLINE R1 \- AI IN BUSINESS 3 \- CareLoop (5 trang)**

## **TRANG BÌA**

## **DANH MỤC TỪ VIẾT TẮT**

## **DANH MỤC HÌNH ẢNH** 

## **BẢNG VIẾT TẮT**

| Từ viết tắt | Giải thích tiếng Việt | Giải thích tiếng Anh |
| ----- | ----- | ----- |
| AI | Trí tuệ nhân tạo | Artificial Intelligence |
| COPD | Bệnh phổi tắc nghẽn mãn tính | Chronic Obstructive Pulmonary Disease |
| CSKH | Chăm sóc khách hàng | Customer Service |
| EMR | Hồ sơ bệnh án điện tử | Electronic Medical Record |
| GDPR | Quy định bảo vệ dữ liệu chung (EU) | General Data Protection Regulation |
| LLM | Mô hình ngôn ngữ lớn | Large Language Model |
| ML | Học máy | Machine Learning |
| PACS | Hệ thống lưu trữ và truyền thông hình ảnh | Picture Archiving and Communication System |
| PDPD | Nghị định bảo vệ dữ liệu cá nhân (Việt Nam) | Personal Data Protection Decree |
| XGBoost | Thuật toán học máy tăng cường gradient | eXtreme Gradient Boosting |

---

## 

## **LỜI MỞ ĐẦU (0.5 trang)**

Trong bối cảnh già hóa dân số nhanh chóng tại Việt Nam, bệnh mãn tính đang chiếm tỷ lệ ngày càng cao, với khoảng 40% dân số trưởng thành mắc ít nhất một bệnh như tiểu đường, tăng huyết áp hoặc COPD (VnEconomy, 2025). Kéo theo đó là tỷ lệ bỏ lịch tái khám định kỳ lên tới 30-40% (VTC News, 2026), dẫn đến biến chứng nặng, tăng chi phí điều trị và tạo áp lực lên các cơ sở y tế. Các bệnh viện và phòng khám đang đối mặt với câu hỏi: làm thế nào để ứng dụng công nghệ nhằm giảm tỷ lệ bỏ lịch, tối ưu chi phí vận hành và nâng cao hiệu quả điều trị?

Ứng dụng trí tuệ nhân tạo (AI) là hướng đi tất yếu, bởi AI không chỉ tự động hóa quy trình nhắc nhở mà còn dự báo rủi ro, cá nhân hóa tương tác và leo thang thông minh. Theo nghiên cứu tại NHS Anh, AI có thể giảm 40% tỷ lệ bỏ lịch ở nhóm bệnh nhân nguy cơ cao (University of Reading, 2025). Với nhóm bệnh nhân mãn tính chủ yếu là người cao tuổi, đối tượng cần sự hỗ trợ từ người thân, việc tích hợp AI vào quy trình chăm sóc sau khám sẽ là yếu tố cốt lõi giúp các cơ sở y tế nâng cao chất lượng dịch vụ.

Bài báo cáo “**CareLoop \- Hệ thống AI Agent giảm no-show & tăng tuân thủ tái khám cho bệnh nhân mãn tính**” phân tích thực trạng bỏ lịch tái khám và đề xuất giải pháp ứng dụng AI Agent vào quy trình quản lý, chăm sóc bệnh nhân sau khám, nhằm giảm tỷ lệ bỏ lịch, tăng tuân thủ điều trị, từ đó củng cố hiệu quả điều trị và tối ưu vận hành cho các cơ sở y tế.

## **TÓM TẮT (0.5 trang)**

Bài báo cáo “**CareLoop \- Hệ thống AI Agent giảm no-show & tăng tuân thủ tái khám cho bệnh nhân mãn tính**” trình bày thực trạng bỏ lịch tái khám định kỳ phổ biến tại các cơ sở y tế Việt Nam, đặc biệt ở nhóm bệnh nhân mãn tính (30-40%), dẫn đến biến chứng nặng và tăng chi phí điều trị. Với mục tiêu giảm tỷ lệ bỏ lịch và nâng cao hiệu quả điều trị, báo cáo đề xuất giải pháp CareLoop \- hệ thống multi-agent AI có ba điểm khác biệt cốt lõi: (1) dự báo nguy cơ bỏ lịch bằng XGBoost, phân nhóm bệnh nhân theo mức độ rủi ro; (2) Caregiver Loop tự động báo cho người thân sau 48 giờ không phản hồi; (3) Post-Visit AI Bundle tóm tắt buổi khám, biểu đồ tiến triển bệnh và video hướng dẫn gửi đến bệnh nhân cùng người thân. CareLoop kỳ vọng đạt giúp giảm tỷ lệ bỏ lịch và nâng cao trải nghiệm người bệnh.

## **CHƯƠNG 1\. GIỚI THIỆU VÀ XÁC ĐỊNH VẤN ĐỀ** 

### **1.1. Tổng quan lĩnh vực**

Đến năm 2025, Việt Nam có hơn 16,1 triệu người cao tuổi (Tuổi Trẻ, 2025), gần 70% mắc ít nhất một bệnh mãn tính (VnEconomy, 2025). Bệnh nhân mãn tính chiếm 50-60% tổng lượt khám tuyến cuối (Tuổi Trẻ, 2024), nhưng tỷ lệ bỏ lịch hẹn 30-40% do thiếu công cụ nhắc nhở thông minh, rào cản thời gian (VTC News, 2026).

### **1.2. Xác định vấn đề** 

CareLoop giải quyết ba lớp vấn đề chính, lấp đầy khoảng trống so với các bệnh viện lớn hiện nay:

*Bảng: Phân tích khoảng trống công nghệ theo từng lớp vấn đề.*

| Vấn đề | Tính năng | Bệnh viện Bạch Mai | Bệnh viện  Vinmec | Bệnh viện  ĐHYD TP.HCM | CareLoop |
| :---: | :---: | :---: | :---: | :---: | ----- |
| **Y tế** (Bỏ lịch → biến chứng nặng) | *Dự báo bỏ lịch* | Chưa có | Chưa có | Chưa có | XGBoost phân nhóm nguy cơ |
| **Kinh doanh** (Tốn CSKH, lãng phí thời gian bác sĩ) | *Nhắc nhở cá nhân hóa* | Giờ cố định (Bạch Mai Care) | MyVinmec \+ tổng đài | UMC Care | Đề xuất theo khung giờ, kênh ưa thích |
| **Quản lý** (Thiếu công cụ phân tích, quy trình thủ công) | *Báo người thân* | Chưa có  | Chưa có | Chưa có  | Tự động sau 48h |
| **Sau khám** (Bệnh nhân quên lời dặn) | *Tóm tắt sau khám* | Chỉ lưu hồ sơ | AI tóm tắt \+ biểu đồ (DrAid) | Có hồ sơ số, PACS | Tóm tắt nội dung \+ biểu đồ \+ video |
| **Toàn diện** | *Số cấp độ nhắc* | 1 cấp (app) | 1-2 cấp (app \+ tổng đài) | 1 cấp (app) | 3 cấp (App/SMS/Email → người thân → CSKH) |

## **CHƯƠNG 2\. GIẢI PHÁP VÀ TÁC ĐỘNG (3 trang)**

## **2.1. Tổng quan giải pháp \- CareLoop (*0.25 trang*)**

CareLoop là hệ thống AI Agent chuyên giải quyết bài toán bỏ lịch tái khám cho bệnh nhân mãn tính. Hệ thống có ba điểm khác biệt chính:

1. Dự báo bỏ lịch tái khám bằng XGBoost (phân nhóm nguy cơ).   
2. Caregiver Loop: sau 48h không phản hồi, tự báo cho người thân đã đăng ký.   
3. Post-Visit AI Bundle: tóm tắt chẩn đoán, lời dặn, kèm biểu đồ so sánh chỉ số và video hướng dẫn chung, gửi tự động cho bệnh nhân và người thân.

### **2.2. Kiến trúc & Luồng hoạt động (*2.5 trang*)**

Hình: Sơ đồ pipeline ([Draw.io](https://draw.io/)) \- ***0.5 trang***

*2.2.1. Adherence Loop Agent*  **(*0.75 trang*)**

Trong vận hành y tế Việt Nam, thất thoát lớn nhất là bệnh nhân quên/bỏ lịch do thiếu nhắc nhở đúng lúc. Adherence Loop Agent lấp đầy bằng luồng tuyến tính có rẽ nhánh, kích hoạt theo phản hồi của bệnh nhân.

***Bước 1 \- Dự báo nguy cơ bỏ lịch.*** Định kỳ mỗi ngày, mô hình XGBoost chạy trên danh sách bệnh nhân có lịch tái khám, tính điểm rủi ro cho từng người, phân thành ba nhóm nguy cơ, làm cơ sở để ưu tiên mức độ can thiệp ở các bước tiếp theo.

***Bước 2 \- Đề xuất khung giờ cá nhân hóa.*** Gemini phân tích sinh hoạt và lịch sử tương tác của từng bệnh nhân để đề xuất khung giờ phù hợp, cân bằng với năng lực bệnh viện (ví dụ: sáng giữa tuần cho người cao tuổi). Cơ chế này vừa tăng khả năng chấp nhận lịch, vừa phân tán workload đều hơn cho bệnh viện.

***Bước 3 \- Xử lý phản hồi và leo thang.*** Luồng sẽ rẽ nhánh theo hành động của bệnh nhân. Nếu xác nhận và đến khám, hệ thống kích hoạt Post-Visit AI Bundle (mục 2.2.2). Nếu không phản hồi sau 48 giờ, chuỗi leo thang ba mức được kích hoạt:

* *Mức 1 (nhẹ)*: Gửi lại thông báo qua kênh thay thế, nội dung cấp bách hơn.  
* *Mức 2 (trung bình)*: Sau 48 giờ tiếp theo, kích hoạt Caregiver Loop tự động gửi tóm tắt lịch đến người thân đã đăng ký (cơ chế opt-in).  
* *Mức 3 (mạnh)*: Khi còn 1 ngày (H-1) mà chưa xác nhận, tạo ticket ưu tiên cho CSKH gọi điện. Trong cuộc gọi, AI (ElevenLabs) tự động trả lời các câu hỏi trong phạm vi dữ liệu có sẵn (lịch hẹn, tên bác sĩ, địa chỉ,...). Nếu bệnh nhân hỏi ngoài phạm vi, cuộc gọi sẽ chuyển liền mạch cho CSKH.

***Bước 4 \- Học từ vòng lặp phản hồi.*** Toàn bộ kết quả tương tác (kênh được phản hồi, khung giờ được chọn, nội dung có tỷ lệ xác nhận cao) được đưa trở lại để cải thiện Smart Scheduler, tối ưu thông điệp nhắc nhở, tạo vòng lặp tự học ngày càng hiệu quả.

*2.2.2. Post-Visit AI Bundle*  **(*0.75 trang*)**

Để giải quyết sự đứt gãy giao tiếp y khoa sau khi bệnh nhân rời viện, Post-Visit AI Bundle tự động biên dịch dữ liệu chuyên môn thành chuỗi thông tin cá nhân hóa, trực quan. Hệ thống gửi gói nội dung này qua App/SMS/Email trong vòng 2 giờ sau khám, với ba chức năng đột phá:

**Clinical Summary Text**

*Vấn đề*: Hồ sơ bệnh án và đơn thuốc mang tính học thuật cao, gây khó hiểu cho bệnh nhân, dẫn đến sai phác đồ hoặc quên chỉ định.

*Tích hợp AI:* LLM \- Gemini trích xuất nội dung từ diễn tiến khám, chuyển ngữ sang ngôn ngữ phổ thông, chắt lọc 3 phân đoạn: (1) kết quả thăm khám; (2) liều lượng và lưu ý tương tác thuốc; (3) lịch tái khám và yêu cầu chuẩn bị. Nội dung được gửi đồng thời cho bệnh nhân và người thân (để phòng trường hợp bệnh nhân quên sau 48h).

**Clinical Progress Chart**

*Vấn đề*: Bệnh nhân mãn tính dễ nản lòng, từ chối tái khám vì không thấy được kết quả điều trị.

*Tích hợp AI:* Hệ thống so sánh chỉ số cận lâm sàng hiện tại với quá khứ, trực quan hóa thành biểu đồ xu hướng (đường huyết, huyết áp, mỡ máu…). Gemini phân tích và sinh bình luận động viên, ví dụ: "Đường huyết giảm từ 8.5 xuống 7.2 mmol/L \- dấu hiệu rất tích cực, duy trì chế độ ăn và uống thuốc để đạt mức ổn định hơn."

**Personalized Video Advisor**

*Vấn đề*: Thời lượng tư vấn tại bệnh viện không cho phép đội ngũ y tế tư vấn chuyên sâu cho từng bệnh nhân.

*Tích hợp AI:* Hệ thống kết hợp Remotion (Render video từ nội dung y tế) và ElevenLabs (Text-to-Speech cung cấp giọng nói truyền cảm) tự động tạo video ngắn (30-60 giây) dựa trên bệnh nền và ghi chú của bác sĩ, hướng dẫn lối sống và cảnh báo dấu hiệu lâm sàng.

*2.2.3. Chatbot & Voice Advisor*  **(*0.5 trang*)**

Chatbot & Voice Advisor hỗ trợ song song 24/7, giúp bệnh nhân và người thân tra cứu nhanh lịch tái khám, cách dùng thuốc lưu ý sau khám bằng văn bản, giọng nói.

***Bước 1 \- Tiếp nhận câu hỏi theo ngữ cảnh cá nhân.*** Chatbot & Voice Advisor sẽ nhận diện ý định hỏi đáp (lịch tái khám, cách dùng thuốc, hướng dẫn sau khám, dấu hiệu cần quay lại kiểm tra, yêu cầu đổi lịch). Sau đó hệ thống đọc ngữ cảnh từ hồ sơ khám gần nhất để cá nhân hóa nội dung phản hồi.

***Bước 2 \- Tra cứu hồ và tạo câu hỏi dễ hiểu.*** Truy xuất dữ liệu từ lịch hẹn, chỉ định, ghi chú bác sĩ và Post-Visit Bundle. Gemini diễn giải bằng ngôn ngữ đơn giản và ElevenLabs chuyển thành giọng nói tự nhiên cho người không quen dùng ứng dụng.

***Bước 3 \- Kích hoạt hành động trong cuộc hội thoại.*** Nếu bệnh nhân muốn thực hiện tác vụ, hệ thống rẽ nhánh đến module phù hợp. Nếu câu hỏi vượt ngoài dữ liệu hoặc cần chuyên môn, chuyển cho CSKH hoặc nhân viên y tế.

***Bước 4 \- Học từ lịch sử tương tác.*** Lưu lại các câu hỏi thường gặp và phản hồi để tối ưu cách trả lời, giảm tải CSKH và giúp bệnh nhân bám sát điều trị.

### **2.3. Lợi ích và tác động (*0.25 trang*)**

*Về sức khỏe:* Tăng tỷ lệ tái khám đúng lịch nhờ dự báo rủi ro và nhắc nhở cá nhân hóa, hỗ trợ kiểm soát bệnh mãn tính. Post-Visit Summary và Progress Card giúp bệnh nhân hiểu rõ tình trạng, theo dõi tiến triển, nâng cao tuân thủ, giảm biến chứng.

*Về kinh doanh*: Giảm tỷ lệ bỏ lịch tối ưu doanh thu tái khám. Cá nhân hóa trải nghiệm nâng cao sự hài lòng và trung thành của bệnh nhân, đồng thời giảm lãng phí thời gian bác sĩ và khung giờ khám bỏ trống.

*Về quản lý*: Tự động hóa quy trình nhắc lịch và chăm sóc sau khám, giảm tải đáng kể cho CSKH. Dữ liệu hành vi bệnh nhân (phản hồi, kênh liên lạc, thời gian tương tác) cung cấp nền tảng phân tích, hỗ trợ cải thiện chiến lược vận hành và ra quyết định dựa trên dữ liệu.

---

## **KẾT LUẬN (0.5 trang)**

Bỏ lịch tái khám định kỳ ở bệnh nhân mãn tính là vấn đề lớn, gây thiệt hại kép cho cả hệ thống y tế và người bệnh. CareLoop không chỉ là công cụ nhắc nhở đơn thuần, mà là hệ thống AI Agent thông minh với ba điểm đột phá: (i) dự báo nguy cơ bỏ lịch bằng XGBoost; (ii) Caregiver Loop tự động báo người thân sau 48 giờ không phản hồi; (iii) Post-Visit AI Bundle tóm tắt buổi khám, biểu đồ tiến triển và video hướng dẫn.. CareLoop được xây dựng theo tư duy liên ngành: về sức khỏe, giúp kiểm soát bệnh tốt hơn, giảm biến chứng; về kinh doanh, tăng doanh thu tái khám, giảm chi phí CSKH; về quản lý, tự động hóa quy trình nhắc nhở và cung cấp dữ liệu phân tích hành vi. Về mặt kỹ thuật, kiến trúc hybrid AI-human dễ dàng tích hợp với hệ thống EMR hiện tại.

Tuy nhiên, mô hình ML phụ thuộc vào chất lượng dữ liệu lịch sử nên tự tạo nhãn no-show có thể có sai số, ElevenLabs giới hạn token nên cần giải pháp hybrid và hệ thống phải tuân thủ bảo mật y tế và sự đồng ý của bệnh nhân khi thêm người thân. Hướng phát triển trong tương lai bao gồm mở rộng sang nền tảng y tế từ xa, kết nối với bảo hiểm y tế và thêm tính năng phân tích hành vi theo thời gian thực.

## 

## **TÀI LIỆU THAM KHẢO** 

Tuổi Trẻ. (2025). \*Năm 2025, Việt Nam có 16% dân số là người cao tuổi, 1 người gánh 3-4 bệnh mạn tính\*.  
[https://tuoitre.vn/nam-2025-viet-nam-co-16-dan-so-la-nguoi-cao-tuoi-1-nguoi-ganh-3-4-benh-man-tinh-20250531122410678.htm](https://tuoitre.vn/nam-2025-viet-nam-co-16-dan-so-la-nguoi-cao-tuoi-1-nguoi-ganh-3-4-benh-man-tinh-20250531122410678.htm)

VnEconomy. (2025). *Hơn 70% người cao tuổi Việt Nam gánh từ 3 bệnh mãn tính trở lên*.  
[http://vneconomy.vn/hon-70-nguoi-cao-tuoi-viet-nam-ganh-tu-3-benh-man-tinh-tro-len.htm](http://vneconomy.vn/hon-70-nguoi-cao-tuoi-viet-nam-ganh-tu-3-benh-man-tinh-tro-len.htm)

Sức khỏe và Đời sống. (2026). *Bệnh thận mạn âm thầm gia tăng, hơn 12% người trưởng thành Việt Nam mắc bệnh*.  
[http://suckhoedoisong.vn/benh-than-man-am-tham-gia-tang-hon-12-nguoi-truong-thanh-viet-nam-mac-benh-169260312171439279.htm](http://suckhoedoisong.vn/benh-than-man-am-tham-gia-tang-hon-12-nguoi-truong-thanh-viet-nam-mac-benh-169260312171439279.htm)

VietnamNet. (2025). *Hàng nghìn người cao tuổi TP.HCM được tầm soát sức khỏe miễn phí*.  
[https://vietnamnet.vn/hang-nghin-nguoi-cao-tuoi-tp-hcm-duoc-tam-soat-suc-khoe-mien-phi-2467323.html](https://vietnamnet.vn/hang-nghin-nguoi-cao-tuoi-tp-hcm-duoc-tam-soat-suc-khoe-mien-phi-2467323.html)

Tuổi Trẻ. (2024). *Người bệnh mạn tính 'lặn lội' hàng chục km hằng tháng để tái khám*.  
[https://tuoitre.vn/nguoi-benh-man-tinh-lan-loi-hang-chuc-km-hang-thang-de-tai-kham-20240422173204048.htm](https://tuoitre.vn/nguoi-benh-man-tinh-lan-loi-hang-chuc-km-hang-thang-de-tai-kham-20240422173204048.htm)

VTC News. (2026). *Ngỡ ngàng đi khám bệnh viện công tuyến đầu chỉ mất hơn một tiếng*.  
[https://vtcnews.vn/ngo-ngang-di-kham-benh-vien-cong-tuyen-dau-chi-mat-hon-mot-tieng-ar1008160.html](https://vtcnews.vn/ngo-ngang-di-kham-benh-vien-cong-tuyen-dau-chi-mat-hon-mot-tieng-ar1008160.html)

Bệnh viện Bạch Mai. (2026). *AI, chuyển đổi số và bệnh viện thông minh: Kỷ nguyên mới của y tế toàn cầu*.  
[https://bachmai.gov.vn/bai-viet/ai-chuyen-doi-so-va-benh-vien-thong-minh-ky-nguyen-moi-cua-y-te-toan-cau?id=90a10578-6f75-41e2-9b89-9f5b4dc444cf](https://bachmai.gov.vn/bai-viet/ai-chuyen-doi-so-va-benh-vien-thong-minh-ky-nguyen-moi-cua-y-te-toan-cau?id=90a10578-6f75-41e2-9b89-9f5b4dc444cf)

Bệnh viện Bạch Mai. (2025). *Chuyển đổi số, trí tuệ nhân tạo \- Nền tảng phát triển đột phá của Y học hiện đại*.  
[https://bachmai.gov.vn/bai-viet/chuyen-doi-so-tri-tue-nhan-tao-nen-tang-phat-trien-dot-pha-cua-y-hoc-hien-dai?id=640595d7-c7aa-4bad-bd95-f52830f198b1](https://bachmai.gov.vn/bai-viet/chuyen-doi-so-tri-tue-nhan-tao-nen-tang-phat-trien-dot-pha-cua-y-hoc-hien-dai?id=640595d7-c7aa-4bad-bd95-f52830f198b1)

VietnamNet. (2025). *Bệnh viện Bạch Mai chuyển đổi số, ứng dụng AI trong khám chữa bệnh*.  
[https://vietnamnet.vn/benh-vien-bach-mai-chuyen-doi-so-ung-dung-ai-trong-kham-chua-benh-2468306.html](https://vietnamnet.vn/benh-vien-bach-mai-chuyen-doi-so-ung-dung-ai-trong-kham-chua-benh-2468306.html)

Vinmec. (2024). *Đột phá công nghệ AI tại Vinmec: Tiết kiệm 80% thời gian xử lý hồ sơ y tế*.  
[https://www.vinmec.com/vie/bai-viet/dot-pha-cong-nghe-ai-tai-vinmec-tiet-kiem-80-thoi-gian-xu-ly-ho-so-y-te](https://www.vinmec.com/vie/bai-viet/dot-pha-cong-nghe-ai-tai-vinmec-tiet-kiem-80-thoi-gian-xu-ly-ho-so-y-te)

Dân trí. (2024). *Đột phá công nghệ AI tại Vinmec: Tiết kiệm 80% thời gian xử lý hồ sơ y tế*.  
[https://dantri.com.vn/suc-khoe/dot-pha-cong-nghe-ai-tai-vinmec-tiet-kiem-80-thoi-gian-xu-ly-ho-so-y-te-20241206211249245.htm](https://dantri.com.vn/suc-khoe/dot-pha-cong-nghe-ai-tai-vinmec-tiet-kiem-80-thoi-gian-xu-ly-ho-so-y-te-20241206211249245.htm)

Bệnh viện Đại học Y Dược TP.HCM. (2025). *UMC Care \- Ứng dụng quản lý sức khỏe*.  
[https://apps.apple.com/us/app/umc-care/id1484775684](https://apps.apple.com/us/app/umc-care/id1484775684)

University of Reading. (2025). *Using AI to tackle health inequalities*.  
[https://research.reading.ac.uk/engagement-and-impact/artificial-intelligence-nhs/](https://research.reading.ac.uk/engagement-and-impact/artificial-intelligence-nhs/)

Henley Business School, University of Reading. (2025). *How AI is Helping the NHS Tackle Missed Appointments*.  
[https://www.henley.ac.uk/research/projects/how-ai-is-helping-the-nhs-tackle-missed-appointments](https://www.henley.ac.uk/research/projects/how-ai-is-helping-the-nhs-tackle-missed-appointments)

## **PHỤ LỤC**

* [Draw.io](http://Draw.io) → Pipeline  
* Figma/Stitch → UI Mockup

