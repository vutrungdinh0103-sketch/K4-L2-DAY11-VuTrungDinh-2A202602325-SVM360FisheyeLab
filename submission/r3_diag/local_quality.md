# Đối chiếu chất lượng cục bộ — rectangle

Teaching reference, không phải gold set đã phê duyệt; không có điểm đạt tự động.
Nguồn: export r1_craft đã khóa SHA256 `18f4d916ea939b105fd40f8f397d5c99cab4d144ea9b7e722f263bc8c0eeab96`; slice `B3-dense`.
Ghép hình học greedy một-một theo IoU ≥ 0.50, rồi so class; H ≥ 40 px.
Box trái nằm chủ yếu trong ignore_region reference không tính. Polygon, polyline, track không được chấm.
Đây là phép tính offline của lab, không phải báo cáo hay kết quả tương đương CVAT Premium.

Frame được tính: adasind_145860.jpg, adasind_167700.jpg, adasind_199770.jpg. Frame thiếu trong export: không.
TP=12; FP=9; FN=8; số lần đối chiếu=27; mean IoU của TP=0.763.

| Chỉ số | Micro | Macro | Nhãn thấp nhất |
|---|---:|---:|---:|
| accuracy | 0.444 | 0.874 | 0.741 |
| precision | 0.571 | 0.620 | 0.333 |
| recall | 0.600 | 0.633 | 0.167 |
| jaccard | 0.414 | 0.444 | 0.125 |
| dice | 0.585 | 0.591 | 0.222 |

| Nhãn | TP | FP | FN | Accuracy | Precision | Recall | Jaccard | Dice |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Bike | 1 | 2 | 5 | 0.741 | 0.333 | 0.167 | 0.125 | 0.222 |
| Car | 1 | 0 | 1 | 0.963 | 1.000 | 0.500 | 0.500 | 0.667 |
| Pedestrian | 3 | 3 | 1 | 0.852 | 0.500 | 0.750 | 0.429 | 0.600 |
| ThreeWheeler | 3 | 2 | 1 | 0.889 | 0.600 | 0.750 | 0.500 | 0.667 |
| Truck | 4 | 2 | 0 | 0.926 | 0.667 | 1.000 | 0.667 | 0.800 |

| Frame | TP | FP | FN | Accuracy | Precision | Recall |
|---|---:|---:|---:|---:|---:|---:|
| adasind_145860.jpg | 2 | 0 | 0 | 1.000 | 1.000 | 1.000 |
| adasind_167700.jpg | 6 | 3 | 3 | 0.545 | 0.667 | 0.667 |
| adasind_199770.jpg | 4 | 6 | 5 | 0.286 | 0.400 | 0.444 |

Confusion matrix: hàng = teaching reference; cột = export đã khóa.
`<missing>` là thiếu box; `<extra>` là box thừa. Xem `local_quality_confusion.csv`.

| Reference \ Export | Bike | Car | Pedestrian | ThreeWheeler | Truck | <missing> |
|---|---:|---:|---:|---:|---:|---:|
| Bike | 1 | 0 | 0 | 0 | 1 | 4 |
| Car | 0 | 1 | 0 | 0 | 1 | 0 |
| Pedestrian | 0 | 0 | 3 | 0 | 0 | 1 |
| ThreeWheeler | 0 | 0 | 0 | 3 | 0 | 1 |
| Truck | 0 | 0 | 0 | 0 | 4 | 0 |
| <extra> | 2 | 0 | 3 | 2 | 0 | 0 |

Chi tiết xung đột trong `local_quality_conflicts.csv`; dữ liệu máy đọc trong `local_quality.json`.
Mismatching label đóng góp một FP cho class vẽ và một FN cho class reference; attribute khác được báo riêng.
Micro accuracy đếm mỗi cặp ghép sai class là một lần đối chiếu; Jaccard đếm cả FP và FN.
Macro/worst bỏ nhãn không xuất hiện ở cả hai phía; chỉ số không có mẫu là N/A.
