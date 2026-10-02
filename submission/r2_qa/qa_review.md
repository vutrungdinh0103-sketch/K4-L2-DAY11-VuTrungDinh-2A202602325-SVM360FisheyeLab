# QA review · B3-dense

Mã khóa: 18F4-D916

Soát mù bản đã khoá của người khác bằng luật, chưa mở teaching reference hay model. Mã khoá đã đối chiếu với
`submission/r1_craft/lock.txt` (`sha256: 18f4d916…`, `code: 18F4-D916`) nên file nhận đúng là bản cuối đã khoá,
không phải bản nháp. Theo GUIDE, các dòng `round=r2_qa` trong `findings.csv` có `rule_id` và **để `why` trống** vì
QA chỉ ghi điều quan sát được và luật liên quan, chưa chẩn đoán nguyên nhân; `cell=L_only` theo mẫu của lệnh.

| frame | object_ref | rule_id | nhận xét |
|---|---|---|---|
| adasind_167700.jpg | L9 · box 9 (Pedestrian) | R05 | `truncated=true` là hợp lý về hình học: box chạm biên khung/vòng kính chứ không bị vật khác che. Cần mở ảnh gốc xác nhận trước khi coi là lỗi attribute. |
| adasind_199770.jpg | L8 · box 8 (ThreeWheeler) | R09 | Probe cho thấy box nằm phần lớn trong vùng don't-care (`ignore_region`) nên người soát không xác nhận được đúng/sai; theo R09 phải trả lại người gán để bỏ box, không tự quyết. |
| adasind_199770.jpg | L6 · box 6 (Truck) | R04 | Vật ở rìa trái trông có hai bánh nhưng đang gán `Truck`; nếu là cụm xe hai bánh thì phải là `Bike` theo R04/R03. |
| adasind_199770.jpg | L3 · box 3 (Pedestrian) | R03 | Box `Pedestrian` nằm trọn trong box `ThreeWheeler` L4; R03 nói người ngồi trong phương tiện khác không có box riêng. |

## P4 — trả lời từng nhận xét QA

- **L9 (R05):** giữ `truncated=true` vì box bị vòng kính/biên khung cắt, không phải bị vật khác che. Nhưng khi mở
  reference tôi thấy cùng box này còn nằm ≥50% trong `ego_body` ⇒ chuyển `action` sang `rework` theo R09 và bỏ box
  ở bản v2 (dòng findings `r1_craft` L9, `IGNORE_SCOPE`).
- **L8 (R09):** đồng ý với người soát — bỏ box trong vùng don't-care; `rework/delta.md` cho thấy `IGNORE_SCOPE` của
  slice giảm 6 → 0 sau bản v2.
- **L6 (R04):** đồng ý — sửa `Truck` → `Bike` cho cụm hai xe đạp rìa trái, đồng thời bổ sung box xe đạp `109-144`
  (quyết định D03 trong `40_decision_log.csv`); sau đó cặp `R5`/`R6` ghép đúng.
- **L3 (R03):** đồng ý — xoá box `Pedestrian` trùng bên trong `ThreeWheeler` `L4`; box trùng thứ hai trên cùng một
  người (`L9`/`L10`/`L12`) cũng bị xoá ở bản v2.
