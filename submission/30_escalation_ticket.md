# Escalation ticket

## Ticket 1 — model yolo26m sai lớp và vẽ vào vùng `lens_border`

- **Frame:** `adasind_199770.jpg` (box `M12`: model gọi `ThreeWheeler` R8/L4 là `Car`; box `M6`: gọi xe tải L5/R7
  là `Car`; box `M4`/`M5`/`M8`: box trùm vào `lens_border`). Cùng lỗi lớp này còn ở `adasind_167700.jpg` (model
  gọi xe ba bánh là `Truck`), đã ghi trong `40_decision_log.csv` D04.
- **Ảnh chụp:** `submission/screenshots/adasind_199770_model_car_vs_threewheeler.png`; ảnh phụ
  `submission/screenshots/adasind_199770_left_edge_bikes.png` (model bỏ/sai cụm xe đạp rìa trái).
- **Expected impact:** nếu ai đó lấy model làm chuẩn thì toàn bộ thống kê zone bị lệch: `local_quality.md` cho
  `Bike` precision 0.333 / recall 0.167, `ThreeWheeler`/`Truck` bị lẫn class, và `iou_sweep.md` cho thấy `edge`
  không khớp được box nào ở IoU 0.50. Kết luận "model gãy ở edge" hiện không tách được **sai lớp** với **sai hình
  học vì méo fisheye**, nên phần chẩn đoán lỗi của buổi học dừng ở mức suy đoán.
- **Owner:** `ai_team`
- **Recommendation:** bổ sung mẫu `ThreeWheeler` nhìn từ trên cao và ở rìa vòng kính vào tập train; kiểm lại
  mapping `Car`/`Truck`/`ThreeWheeler` cho vật cao < 80 px; công bố model card nêu rõ hạn chế ở vùng `lens_border`
  và `ego_body`. Trong buổi học: không dùng `assets/model-yolo26m.xml` làm teaching reference cho slice này.

## Ticket 2 — R09 miễn trừ một phía làm người gán đúng luật vẫn bị trừ điểm

- **Frame:** `adasind_199770.jpg`, box reference `R4` (`R_only`, zone `mid`, `ThreeWheeler` nằm phần lớn trong
  `ego_body`/`lens_border`; probe lưới 10×10 trả `ignored=True`).
- **Ảnh chụp:** `submission/screenshots/adasind_199770_ego_body_right.png`.
- **Expected impact:** R09 cấm người gán vẽ box ≥50% trong `ignore_region`, nhưng matcher chỉ miễn trừ phía người
  gán; reference có box trong vùng don't-care nên nó vẫn bị tính là `MISSING` và hạ recall lớp `ThreeWheeler`
  (0.750 trong `local_quality.md`). Không sửa luật thì mọi người gán làm đúng R09 đều bị trừ điểm ở vùng này, và
  bảng zone của mọi slice đều bị lệch theo.
- **Owner:** `guideline`
- **Recommendation:** ban hành R09b (miễn trừ đối xứng ≥50%, ngưỡng phải đo bằng probe 10×10 và ghi vào
  `evidence`), ghi vào `20_guideline_patch.md` và bump `rules_version` lên v1.1.0 từ round `rework`; kèm một
  polygon `ego_body` mẫu cho hai frame này để người gán mới đo giống nhau.
