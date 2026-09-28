# So sánh L với R

Chỉ số L/R là thứ tự box cao ≥ H=40 trong từng frame, theo thứ tự XML; bắt đầu từ 1.
Box L trong ignore_region được báo IGNORE_SCOPE, không tính SPURIOUS.

## adasind_019560.jpg
- L1 center SPURIOUS
- L7+R3 edge WRONG_CLASS

## Theo zone
| zone | n_ref | matched | missing | spurious |
|---|---|---|---|---|
| center | 3 | 3 | 0 | 1 |
| mid | 2 | 2 | 0 | 0 |
| edge | 1 | 0 | 1 | 1 |
