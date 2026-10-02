# Sensor context

- **Rig:** ADASIND là clip **một** camera fisheye gắn trong xe, ảnh gốc 1080×1920 (dọc). Repo không kèm tài liệu
  rig nên phần này ghi theo quan sát trên slice `B3-dense` (`adasind_145860.jpg`, `adasind_167700.jpg`,
  `adasind_199770.jpg`); tôi không suy ra tiêu cự, độ cao hay vị trí gắn camera trong không gian.
- **`ego_body`:** thân xe ego thấy ở **mép trái và đáy khung**, không phải một băng ngang liền khối. Ở
  `adasind_167700.jpg` tôi vẽ polygon `(0,1185)-(322,1695)` cộng thêm mảng nhỏ `(428,1730)-(548,1766)` (gương/tay
  lái); ở `adasind_199770.jpg` là dải `(0,980)-(140,1603)`. Vật đi qua vùng này vẫn trông thấy một phần, nên R09
  cần ngưỡng ≥50% chứ không phải "chạm là bỏ".
- **Vòng kính:** công cụ đã import sẵn 2 polygon `lens_border` mỗi frame nên tôi chỉ soát lại (R08). Biên vòng
  kính là một cung lớn: `adasind_167700.jpg` đi `(0,492) → (632,166) → (1080,913)`, `adasind_199770.jpg` đi
  `(0,508) → (610,191) → (1080,334)`. Vùng vành đen mỏng nhất ~166 px ở giữa khung và dày tới ~900 px ở góc;
  đường kính vòng kính lớn hơn chiều rộng ảnh nên vòng bị cắt ở hai mép trái/phải. Hệ quả: vật vào gần rìa luôn
  vừa bị cong vừa có nguy cơ bị cắt — đó là lý do lớp `edge` là nơi model gãy nhiều nhất.
- **Nhãn gặp trong slice:** `Car`, `Truck`, `ThreeWheeler`, `Bike`, `Pedestrian` (không gặp `Bus`). Vật nhỏ nhất
  tôi gặp chỉ rộng ~24-53 px và cao ~43-56 px (`Bike` `91-144` ở `adasind_199770.jpg`), sát ngưỡng `H=40` của R01
  nên phần này là chỗ tôi phải đo bằng probe thay vì đoán bằng mắt.
