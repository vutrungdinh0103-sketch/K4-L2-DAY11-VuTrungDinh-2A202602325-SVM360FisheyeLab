# Exit ticket

Đọc `docs/10-svm360-reading-vi.md` trước khi trả lời câu 1–2. Các câu về zone, `why`, rework, parking và sampling
đã nằm trong file tương ứng nên không hỏi lại ở đây.

1. Một vật ở vùng seam giữa hai camera thật xuất hiện với hai box khác nhau: đó là lỗi `DUPLICATE` hay cần một quy
   tắc riêng? Vì sao? → **Cần một quy tắc riêng, không mặc định là `DUPLICATE`.** `DUPLICATE` trong bài dùng cho
   hai box trên **cùng một annotation space**, tức cùng ảnh và cùng phép chiếu, như ba box `L9`/`L10`/`L12` chồng
   lên cùng một người `611-704` ở `adasind_199770.jpg`. Hai camera thật là hai phép chiếu khác nhau của cùng một
   vật, và mỗi box có thể đúng trên ảnh gốc của nó (R02), nên "một vật — hai box" là hợp lệ ở tầng per-camera.
   Quy tắc riêng phải nói rõ: giữ cả hai box kèm `track_id`/timestamp, chỉ hợp nhất ở tầng BEV khi có calibration và
   ngưỡng khớp, và phải chỉ định camera nào là "chủ" của output. Thiếu policy đó thì người gán tự xoá một box, và
   cái bị mất là một quan sát đúng.
2. Một vật đi qua nhiều frame trên cùng camera: khi nào giữ cùng track ID, khi nào thêm keyframe hoặc trạng thái
   Outside? Nêu bằng chứng sẽ cần trước khi nối track qua hai camera. → Giữ cùng track ID khi cùng camera, cùng vật,
   còn quan sát liên tục và hình học đổi trong ngưỡng. Thêm keyframe khi thay đổi lớn: vật vào gần, bị vòng kính
   cắt nhiều, hoặc đổi lớp do góc nhìn (ở slice này là box xe đạp `755-975` ở `adasind_167700.jpg` — box phải thu về
   phần thấy được theo R02b thay vì kéo dài cho "đủ" vật). Dùng trạng thái Outside khi vật ra khỏi trường nhìn hoặc
   không còn đủ `H=40`. Trước khi nối track qua hai camera cần: timestamp đồng bộ giữa hai camera, calibration mỗi
   camera, một vùng chồng thật (seam) nơi vật xuất hiện đồng thời ở cả hai, và policy output; thiếu một trong bốn
   thứ đó thì tôi chỉ ghi `E5_unresolved` và để người soát quyết định.
3. Nhìn lại cả buổi: một chỗ bạn tin nhãn mình đúng nhưng reference hoặc người soát nghĩ khác (dẫn frame/`object_ref`),
   bạn đã xử lý thế nào, và nếu làm lại slice này bạn sẽ đổi gì trong cách làm? → Ở `adasind_167700.jpg` box `L11`,
   tôi tin phải phủ trọn chiếc xe đạp xuống tới đáy khung, còn reference chỉ giữ phần thấy được; `compare` báo
   `L11 IGNORE_SCOPE` (P0) và kéo theo `R2 MISSING`. Tôi không sửa reference mà tự kiểm lại bằng probe lưới 10×10
   để đo % diện tích box rơi vào `ego_body`/`lens_border`, ghi finding theo R09, thu box về `(755,1049)-(975,1283)`
   rồi lock lại bản `rework/annotations-v2.xml`; đổi lại `R2` ghép được nên zone `mid` từ 4 missing xuống 1
   (`rework/delta.md`). Nếu làm lại slice này tôi sẽ: soát `ego_body`/`lens_border` **trước** khi vẽ box, ghi % ignore
   ngay trong lúc gán thay vì sau khi so reference, và chốt R09b (miễn trừ đối xứng) với người soát trước khi lock
   `r1_craft` để không phải quay lại ở vòng rework.
