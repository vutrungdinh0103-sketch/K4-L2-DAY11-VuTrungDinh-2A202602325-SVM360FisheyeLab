# Guideline patch

- **Rule mới đề xuất:**
  - **R09b — miễn trừ `ignore_region` phải đối xứng hai phía:** box (dù là của người gán hay của reference) nằm
    ≥50% diện tích trong `ignore_region` thì được miễn trừ cho **cả hai phía**; box nằm 20-50% thì phải vẽ phần
    nhìn thấy, ghi `truncated`, và ghi % đo bằng probe lưới 10×10 vào cột `evidence`.
  - **R04b — ví dụ biên cho R04:** van chở người ≤3,5 t dù thùng sau kín ⇒ `Car`; xe ba bánh có thùng/ghế chở
    người ⇒ `ThreeWheeler`; pickup/xe tải nhỏ thùng lộ ⇒ `Truck`; bắt buộc kèm ảnh tham chiếu cho vật cao < 80 px
    ở vùng ảnh mờ.
  - **R02b — box bị vòng kính cắt:** box chỉ bao phần còn thấy trên ảnh gốc, không kéo dài vào `lens_border`/`ego_body`
    để "cho đủ" vật; kéo dài là tự biến box thành don't-care và làm chính vật đó bị báo `MISSING`.
- **Áp dụng cho:** R09 (`ignore_region.reason` = `ego_body`, `lens_border`), R04 (class `Car` / `Truck` /
  `ThreeWheeler` / `Bus`), R02 (zone `edge` và `mid`, vật cao < 80 px); ảnh hưởng trực tiếp `Bike` và `Pedestrian`
  ở rìa vòng kính.
- **Vì sao luật hiện tại (`docs/02-rules-vi.md`) không đủ:** R09 chỉ cấm người gán đặt box ≥50% trong `ignore_region`
  nhưng không nói phía **reference** cũng phải được miễn trừ đối xứng, nên `R4` ở `adasind_199770.jpg` bị matcher
  báo `MISSING` trong khi probe 10×10 trả `ignored=True` — người gán đúng luật vẫn bị trừ recall
  (`local_quality.md`: `ThreeWheeler` recall 0.750). R04 liệt kê "van chở người → Car" và "xe ba bánh →
  ThreeWheeler" nhưng không có ví dụ biên, nên van nhỏ ở xa (`L5`/`R4` ở `adasind_167700.jpg`, vùng 580-700) bị
  gọi `Truck` và cụm xe đạp rìa trái (`L6`/`R5` ở `adasind_199770.jpg`) cũng bị gọi `Truck`. R02 nói vẽ trên ảnh
  gốc nhưng chưa nói box bị vòng kính cắt thì phải **thu về phần thấy được**, nên hai người gán có thể vẽ khác
  nhau (đây chính là lỗi `L11`/`R2` ở `adasind_167700.jpg`).
- **`rules_version` mới:** v1.0.0 → **v1.1.0** (ba rule R09b/R04b/R02b ở trên; các dòng `round=rework` trong
  `findings.csv` đã ghi `rules_version=v1.1.0`).
- **Hiệu lực từ:** round `rework` của slice `B3-dense` (bản `rework/annotations-v2.xml`, lock `620A-0335`); áp dụng
  luôn cho các slice của buổi sau, còn `r1_craft` giữ v1.0.0 để delta trước/sau còn so được.
