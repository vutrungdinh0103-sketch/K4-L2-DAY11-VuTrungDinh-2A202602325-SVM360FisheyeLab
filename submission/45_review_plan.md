# Kế hoạch review từ lỗi quan sát được

Từ `findings.csv` và `zone_table.md`, chọn **hai lát cắt của bài ADASIND một camera** cần review trước. Bảng này
giải thích dữ liệu thật bạn vừa làm; nó không thay cho kế hoạch bốn camera giả lập ở `45_sampling_plan.csv`.

| Lát cắt / frame | Số ca và loại lỗi | Vì sao review trước | Bằng chứng cần giữ |
|---|---|---|---|
| Lát cắt / frame | Số ca và loại lỗi | Vì sao review trước | Bằng chứng cần giữ |
|---|---|---|---|
| `adasind_199770.jpg` — cả frame (zone `center`+`mid`+`edge`) | 11 lỗi phía người gán: 4 `SPURIOUS`, 3 `MISSING`, 2 `IGNORE_SCOPE`, 1 `WRONG_CLASS`, 1 `BOX_GEOMETRY`; `local_quality.md`: TP 4 / FP 6 / FN 5 (accuracy 0.286) | Là frame gãy nặng nhất của slice và là frame duy nhất có đủ ba zone; hai lỗi `IGNORE_SCOPE` ở đây là P0 và cùng nguyên nhân với `adasind_167700.jpg`, chốt trước thì mới sửa được R09 cho cả slice | `r1_craft/compare.md` (dòng `L7`, `L8` `IGNORE_SCOPE`; `L1`+`R9` `BOX_GEOMETRY`), bảng theo frame trong `r3_diag/local_quality.md`, `screenshots/adasind_199770_ego_body_right.png`, `screenshots/adasind_199770_left_edge_bikes.png` |
| `adasind_167700.jpg` — vùng `mid` quanh vòng kính | 6 lỗi phía người gán: 2 `IGNORE_SCOPE`, 1 `SPURIOUS`, 1 `BOX_GEOMETRY`, 1 `WRONG_CLASS`, 1 `MISSING`; zone `mid`: n_ref 7, L missing 4 | `mid` là zone người gãy nhiều nhất (4/7 box reference bị bỏ sót) và cả hai lỗi P0 của slice nằm ở đây; box xe đạp `755-975` bị kéo vào `ego_body` làm `R2` thành `MISSING` nên phải chốt trước khi lock bản v2 | `r3_diag/zone_table.md` (dòng zone `mid`), `r1_craft/compare.md`, `screenshots/adasind_167700_bike_trim_755_975.png`, `screenshots/adasind_167700_bike_geometry_296_346.png` |

Giới hạn của kết luận từ ba frame ADASIND: slice chỉ có `adasind_145860.jpg`, `adasind_167700.jpg`,
`adasind_199770.jpg` — 3 frame, 20 box reference, 27 lần đối chiếu, nên không tách được lỗi theo thời gian và
không suy ra được tỷ lệ lỗi cho cả clip. `center/mid/edge` là vị trí trên ảnh chứ không phải khoảng cách vật-xe.
`adasind_145860.jpg` sạch (TP 2, không FP/FN) nên không nói được gì về độ khó. Một ca vẫn chưa chốt là `R9` ở
`adasind_199770.jpg` (`E5_unresolved`, chỉ reference có box): chưa đủ bằng chứng để nói ai sai nên tôi giữ
nguyên và ghi lại để người soát mở lại ảnh.

## Chuyển sang kế hoạch bốn camera giả lập

Cách soát độ phủ của 200 frame ở `45_sampling_plan.csv`: mỗi camera ở mỗi chế độ (`normal`/`hard`) phải có số
frame như dòng tổng trong file (8 dòng front/rear/left/right × normal/hard, cộng lại đúng 200), và mỗi ca phải
trỏ được về một frame + camera cụ thể chứ không chỉ một khoảng thời gian. Chống đếm trùng: trong cùng một cảnh
liên tục tôi chỉ lấy 1-2 frame đại diện và bắt buộc hai frame đại diện cách nhau một khoảng thời gian (không lấy
hai frame liền nhau của cùng một cảnh làm hai ca độc lập), vì chúng chia nhau cùng một bộ vật và cùng một kiểu
lỗi. Vì sao kế hoạch này chỉ **tìm** ca cần soi: đây là lấy mẫu chủ đích theo rủi ro (seam, vòng kính, vật nhỏ,
đêm/mưa), không phải lấy mẫu ngẫu nhiên có trọng số và cũng không có nhãn gold sẵn, nên nó không cho xác suất
lỗi — muốn có tỷ lệ lỗi phải có gold set được gán bằng quy trình đã kiểm chứng (mục `46_gold_set_plan.md`) rồi
đo lại trên chính phân bổ đó.
