## Linear 101 - Writeup (WannaGame Championship)

### Mô tả

- Một bài tập về hệ phương trình tuyến tính trên vành "max-plus" (tropical semiring).
- Người chơi cần vượt qua 64 vòng chơi, mỗi vòng gửi lên server vector nghiệm $x$ tương ứng với ma trận $A$ và vector kết quả $b$.

### Tệp đính kèm

- `chall.py`

### Phân tích

- **Lỗi Random Seed:** `random.seed("Wanna Win?")` là cố định. Do đó, ma trận $A$ sinh bởi `random.randbytes` có thể dự đoán và tái tạo chính xác ở phía client.
- **Hệ phương trình Max-Plus:** Phép toán mã hóa $b_i = \max_{j} (A_{ij} + x_j)$ tương đương với phép nhân ma trận trong đại số max-plus.
- **Nghịch đảo:** Tìm $x$ bằng cách áp dụng công thức nghiệm chính:
  $$ x_j = \min_{i} (b_i - A_{ij}) $$
  Công thức này đảm bảo $A_{ij} + x_j \le b_i$ với mọi $i, j$, và $x_j$ là giá trị lớn nhất thỏa mãn.

### Lời giải

Code giải đầy đủ trong `solve.py`. Tóm tắt các bước:

1. Kết nối đến server.
2. Khởi tạo `random.seed("Wanna Win?")` giống hệt server.
3. Lặp 64 vòng:
   - Tự sinh ma trận $A$.
   - Nhận $b$ từ server.
   - Tính $x$ theo công thức $x_j = \min_i (b_i - A_{ij})$.
   - Gửi $x$ lên server.

Trích đoạn xử lý chính:

```python
# Tái tạo A
A = [random.randbytes(N) for _ in range(N)]

# Tìm x
x_candidate = []
for j in range(N):
    min_diff = float('inf')
    for i in range(N):
        diff = b[i] - A[i][j]
        if diff < min_diff:
            min_diff = diff
    x_candidate.append(int(min_diff))
```

### Flag

`W1{weLI_1_tHinK_1t5_eAsIER-TH@N_NorMAI-L1NE@R-4lgebra_problem0}`
