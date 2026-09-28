# So sánh L với R

Chỉ số L/R là thứ tự box cao ≥ H=40 trong từng frame, theo thứ tự XML; bắt đầu từ 1.
Box L trong ignore_region được báo IGNORE_SCOPE, không tính SPURIOUS.

## adasind_145860.jpg
## adasind_167700.jpg
- L9 mid IGNORE_SCOPE
- L11 mid IGNORE_SCOPE
- L2 mid SPURIOUS
- L4+R9 mid BOX_GEOMETRY
- L5+R4 center WRONG_CLASS
- R2 mid MISSING
## adasind_199770.jpg
- L7 mid IGNORE_SCOPE
- L8 mid IGNORE_SCOPE
- L1+R9 center BOX_GEOMETRY
- L3 mid SPURIOUS
- L6+R5 edge WRONG_CLASS
- L9 center SPURIOUS
- L10 center SPURIOUS
- L12 center SPURIOUS
- R3 mid MISSING
- R4 mid MISSING
- R6 edge MISSING

## Theo zone
| zone | n_ref | matched | missing | spurious |
|---|---|---|---|---|
| center | 9 | 7 | 2 | 5 |
| mid | 7 | 3 | 4 | 3 |
| edge | 4 | 2 | 2 | 1 |
