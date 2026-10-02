# Đề xuất gold set theo camera — tình huống giả lập

**Đầu bài:** 50.000 frame từ bốn camera SVM, ngân sách chọn 200 frame để review/gold. Đây là tình huống trên slide,
**không phải** 50.000 frame có trong repo. Phân bổ đúng 200 ở `45_sampling_plan.csv` cho bốn camera, mỗi camera có
normal và hard slice. “Gold set” ở đây là **kế hoạch tạo** reference sau kiểm chứng, không phải teaching reference
ADASIND hoặc nhãn bạn vừa vẽ. Nếu cần, dùng `notebooks/day11-svm360-colab.ipynb` để thử tổng phân bổ; notebook
không làm thay phần lý do.

| camera_id | Hard case cần chọn | Vì sao dễ sai | Annotation space / calibration cần giữ | Cách review trước khi gọi là gold |
|---|---|---|---|---|
| front | Vật nhỏ ở `mid`/`edge` ngay dưới vòng kính: van nhỏ và xe ba bánh cao < 80 px (như `L5`/`R4` ở `adasind_167700.jpg`); xe ba bánh nhìn từ trên cao | Ba class `Car`/`Truck`/`ThreeWheeler` chồng nhau khi vật nhỏ và mờ (R04); vòng kính làm vật cong nên box "đúng" theo mắt vẫn sai theo IoU | Nội tại fisheye (tiêu cự, tâm vòng kính) + ngoại (cao, góc chúi, vị trí gắn); polygon `ego_body`/`lens_border` mỗi frame; bảng mapping class v1.1.0 (`R04b`) | Hai người gán độc lập rồi adjudicate các box lệch; kiểm `H=40` trên ảnh gốc; probe 10×10 để chắc không box nào ≥50% trong `ignore_region` |
| rear | Cụm xe bám đuôi sát `ego_body` và biển số mờ; vật bị che một phần, dễ lẫn `truncated` với `occluded` | Vành `lens_border` phía dưới dày nên vật bị cắt nhiều; người gán hay vẽ "đủ kích thước thật" và tự đẩy box vào vùng don't-care; van gần giống minibus | Cùng bộ calibration với `front`; thêm đồng bộ thời gian (timestamp) cho ca seam với camera `left`/`right`; polygon ignore mỗi frame | Soát riêng hai attribute theo R05 (`truncated` do vòng kính ≠ `occluded` do vật khác che); chạy lại quality report để xem có bias theo lớp không |
| left | Vật vào từ mép trái rất nhanh: cụm hai xe đạp rìa trái `91-144` ở `adasind_199770.jpg` (rộng chỉ 25-53 px), có khi chỉ thấy nửa người | Méo fisheye mạnh nhất ở mép; dễ bỏ sót chiếc thứ hai trong cụm và dễ gộp hai vật thành một box | Calibration + zone mapping của camera trái; polygon `lens_border` trái; quy ước cụm (`crowd_or_group`) khi không tách được | Mở 3 frame liền nhau để đếm lại cụm, chỉ lấy một frame làm ca; kiểm bằng hai người gán khác nhau, nếu lệch số vật thì đưa vào diện cần quyết định |
| right | Vùng seam phải với camera sau: cùng một vật xuất hiện hai box, hai zone khác nhau | Chưa có policy "một vật hai box" nên người gán dễ tự xoá một box; méo ở hai ảnh khác nhau nên không thể so box bằng mắt | Timestamp đồng bộ giữa hai camera; calibration cả hai; homography/BEV để chiếu hai box về cùng hệ; policy output (giữ cả hai hay hợp nhất) | Review chéo hai camera trước khi gọi là gold; không xoá box nào khi policy chưa được duyệt; ghi decision log cho policy đó |

- Khi nào cần refresh gold set (đổi camera, calibration hoặc rule): khi đổi ống kính/vị trí gắn camera (calibration
  mới làm méo và vùng `lens_border` khác), khi bump `rules_version` (v1.0.0 → v1.1.0 là ca đầu, đổi ngưỡng R09 và
  ví dụ biên R04), hoặc khi đổi định nghĩa output (per-camera → BEV fusion). Khi đó chỉ re-adjudicate phần bị ảnh
  hưởng — các class/vùng liên quan tới rule vừa đổi — chứ không gán lại toàn bộ 200 frame.
- Một ca seam/cross-camera cần policy và evidence trước khi ghép hai box: ví dụ một người đi bộ đi từ camera
  `front` sang `right` ở góc phải-trước. Policy phải quyết trước: (a) output per-camera giữ **cả hai** box với
  `track_id` riêng, hay (b) hợp nhất thành một box sau BEV. Evidence cần: timestamp hai frame lệch trong ngưỡng
  đồng bộ cho phép, calibration của cả hai camera, và toạ độ BEV của cùng vật trùng nhau trong sai số cho phép.
- Vì sao peer agreement hoặc quality report trên ảnh một camera chưa chứng minh gold set đúng cho cả bốn camera:
  hai người cùng đọc **một** camera sẽ cùng sai theo hệ thống (cùng méo, cùng vùng `lens_border`, cùng bảng mapping
  class) nên agreement cao vẫn có thể sai giống nhau; quality report trên một camera cũng không thấy được lỗi chỉ
  xuất hiện khi ghép hai camera (seam, vật bị cắt khác nhau, track gãy). Gold cho hệ bốn camera phải kiểm cả ba
  tầng: nhãn trên ảnh gốc, calibration/không gian toạ độ, và policy output.
