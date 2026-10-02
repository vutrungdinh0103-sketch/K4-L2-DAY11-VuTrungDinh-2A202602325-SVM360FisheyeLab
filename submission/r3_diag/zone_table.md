# Zone table (slice của bạn)

Lệnh `python3 lab11.py model` tự ghi bảng số (cùng cách đếm với `r1_craft/compare.md` và `model_compare.md`); chạy lại lệnh sẽ cập nhật bảng và giữ nguyên phần nhận xét. Bạn chỉ viết mục Nhận xét.

| Zone | n_ref | L missing | L spurious | M missing (`LR_noM` + `R_only`) | M thừa (`LM_noR` + `M_only`) | Lỗi L chính (`what`) |
|---|---:|---:|---:|---:|---:|---|
| center | 9 | 2 | 5 | 3 | 4 | SPURIOUS (3) |
| mid | 7 | 4 | 3 | 3 | 4 | MISSING (3) |
| edge | 4 | 2 | 1 | 4 | 3 | WRONG_CLASS (1) |

## Nhận xét

- Người (L) gãy nhiều nhất ở **mid**: 4/7 box reference bị bỏ sót (`R2` ở `adasind_167700.jpg`; `R3`, `R4`, `R6`
  ở `adasind_199770.jpg`) cộng 3 box thừa; lỗi L chính của zone cũng là `MISSING (3)`. Model (M) gãy nặng nhất ở
  **edge**: 4 box reference không có box model nào khớp và 3 box thừa trên chỉ 4 ref — `edge` cũng là zone duy
  nhất model không khớp được box nào ở IoU 0.50 (`iou_sweep.md`). **center** nhiều box thừa nhất về số tuyệt đối
  (5 box L thừa ở block B3, 11 `SPURIOUS` toàn block trong `10_error_card.md`) nhưng lỗi L chính vẫn là
  `SPURIOUS (3)`, không phải bỏ sót.
- Giả thuyết: (1) **box kéo vào vùng don't-care** — box xe đạp dưới vòng kính và box người cạnh `ego_body` bị kéo
  dài cho "đủ vật", thành don't-care rồi chính vật đó bị báo `MISSING` (`R2` 167700; `R3`/`R4` 199770); (2) **box
  lỏng/trùng ở center** — ba box cho cùng một người `611-704` (`L9`/`L10`/`L12`) và box xe đạp rộng 127.9 px so
  với reference 71 px (`L1` 199770); (3) **vật quá nhỏ ở edge** — cụm xe đạp `91-144` chỉ rộng 24-53 px, cao 43 px
  nên model vừa bỏ sót vừa sai lớp. Giới hạn của slice ba frame: chỉ 20 box reference và 27 lần đối chiếu, nên bảng này
  dùng để **tìm chỗ cần soi lại**, không dùng để suy tỷ lệ lỗi; `center/mid/edge` là vị trí trên ảnh, không phải
  khoảng cách vật-xe; ba frame này còn cùng một cảnh nên không được tính thành ca độc lập.
