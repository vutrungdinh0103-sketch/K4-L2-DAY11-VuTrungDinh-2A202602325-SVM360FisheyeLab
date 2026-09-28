# Quan sát vạch ô đỗ

- Hai vạch `parking_line` đã vẽ (mô tả vị trí trong ảnh):  2 vạch sơn màu trắng ở khu vực gần góc trái bên dưới của ảnh.
- Một vạch/dấu sơn hoặc biên **không** vẽ, và vì sao: viền vỉa hè phía bên phải ảnh vì đây đều không phải là parking_line hay free_space
- Polygon `free_space` dừng ở đâu; có phần bị che nào không: Polygon biểu diễn làn đường di chuyển chạy cắt ngang bãi đỗ. Polygon này dừng lại chính xác tại các điểm đầu mút của các vạch đỗ xe. Toàn bộ vùng `free_space` này hiện hoàn toàn trống trải và không bị che khuất bởi bất kỳ phương tiện hay vật thể nào.
- Ca chưa chắc cần hỏi người soát (nếu không có, ghi “không có”): không có
