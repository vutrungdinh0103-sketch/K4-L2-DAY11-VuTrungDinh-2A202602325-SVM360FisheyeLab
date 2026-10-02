# Error analysis card

## Zone × block

| zone | block | what | count |
|---|---|---|---:|
| center | B3 | BOX_GEOMETRY | 1 |
| center | B3 | MISSING | 4 |
| center | B3 | SPURIOUS | 11 |
| center | B3 | WRONG_CLASS | 1 |
| center | C0 | SPURIOUS | 1 |
| edge | B3 | MISSING | 6 |
| edge | B3 | SPURIOUS | 4 |
| edge | B3 | WRONG_CLASS | 3 |
| edge | C0 | WRONG_CLASS | 1 |
| mid | B3 | ATTRIBUTE | 1 |
| mid | B3 | BOX_GEOMETRY | 1 |
| mid | B3 | IGNORE_SCOPE | 6 |
| mid | B3 | MISSING | 9 |
| mid | B3 | SPURIOUS | 8 |

## Top defects
- SPURIOUS: 24 (ví dụ frame adasind_019560.jpg)
- MISSING: 19 (ví dụ frame adasind_167700.jpg)
- IGNORE_SCOPE: 6 (ví dụ frame adasind_167700.jpg)

## Phân tích của bạn

Hai bảng trên do `python3 lab11.py card` tính từ `findings.csv`; chạy lại lệnh sẽ cập nhật bảng và giữ nguyên mục này. Viết cho lỗi nổi bật nhất, dẫn frame/`object_ref`.

- Nguyên nhân khả dĩ (`why`) và vì sao bạn nghĩ vậy: **`SPURIOUS` nhiều nhất (24 ca)** và tập trung ở `center`:
  ba box cho cùng một người `611-704` (`L9`/`L10`/`L12` ở `adasind_199770.jpg`, hai trong số đó là box trùng thứ
  hai) và box `ThreeWheeler` `161-261` ở `adasind_167700.jpg` chỉ là nửa phải của chiếc ba bánh đã có box `L7`
  khớp `R6`. Tôi xếp `E1_annotator_error` vì cùng một vật mà tôi tách thành nhiều box trong lúc gán, không phải
  reference sai. Nhóm thứ hai là **`MISSING` (19 ca)** chủ yếu ở `mid`/`edge`, do box bị kéo vào `ego_body`/
  `lens_border` nên chính vật đó thành don't-care: `R2` ở `adasind_167700.jpg` (box `L11` vẽ tới `y=1283`) và
  `R3`/`R4`/`R6` ở `adasind_199770.jpg`. Ở đây tôi tách `E1` khi chính tôi vẽ sai phạm vi và `E2` khi luật chưa nói
  ngưỡng (D06 trong `40_decision_log.csv`). Lưu ý `spurious` phía model còn có nguyên nhân khác (`E4`: model gọi
  sai lớp), nên không gộp hai nguồn này làm một.
- Cách sửa và ai nhận việc (`owner`): sửa ngay ở bản v2 rồi lock lại — bỏ box trong vùng don't-care, gộp ba box
  người thành một, thu box xe đạp về phần thấy được (`annotator`, xem `rework/delta.md`: spurious 9 → 0, missing
  `mid` 4 → 1). Gửi `guideline` cho R04/R09 (ngưỡng 50% phải đối xứng, cần ví dụ biên van/xe ba bánh) và `ai_team`
  cho việc model gọi sai `Car`/`Truck`/`ThreeWheeler` — chi tiết ở `30_escalation_ticket.md` (Ticket 1 và Ticket 2).
- Bằng chứng (ảnh trong `screenshots/`, dòng findings, rule): `screenshots/adasind_199770_ego_body_right.png`,
  `adasind_199770_left_edge_bikes.png`, `adasind_167700_bike_trim_755_975.png`,
  `adasind_199770_model_car_vs_threewheeler.png`; các dòng findings `L9`/`L10`/`L12` (`SPURIOUS`, round `r1_craft`),
  `L11`+`R2` (`IGNORE_SCOPE`/`MISSING`, round `r1_craft`/`r3_diag`), `M12` (`WRONG_CLASS` theo `R04`), rule dùng
  để phân loại là R01/R02/R03/R04/R09; delta trước/sau ở `rework/delta.md`.
