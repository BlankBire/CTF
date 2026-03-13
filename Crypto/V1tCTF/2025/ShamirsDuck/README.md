## ShamirsDuck - Writeup (V1tCTF)

### Mô tả

Secret bị chia ra thành 6 shares, threshold = 3 (ít nhất 3 shares ghép lại mới phục hồi secret) $\Rightarrow$ Dấu hiệu rõ ràng của thuật toán `Shamir Secret Sharing`.
Tệp kèm theo:

- `shares.txt`

### Phân tích

- Đây là bài Shamir: Secret được mã hóa như một đa thức $f(x)$ trên trường $\mathbb{F}_p$, mỗi share là $y_i = f(x_i) \mod p$.
- Thông tin quan trọng: Không cho $p$, chỉ có các giá trị $y$ (dưới dạng hex). Một trick thường dùng là chọn $p$ là một số nguyên tố lớn hơn mọi share $p = \text{nextprime}(\max(y_i))$. Vì share < $p$, chọn $p$ như vậy cho phép làm việc trong trường thích hợp.
- Threshold là ít nhất 3 shares $\Rightarrow$ đa thức $\le 2$ (degree < 3). Do đó, bằng 3 điểm có thể khôi phục $f(x)$, đặc biệt $f(0)$ chính là secret ban đầu (giả định secret được nhúng làm hệ số tự do).

### Ý tưởng

- Chuyển các hex share thành số nguyên (base 16 $\rightarrow$ int).
- Lấy $p = \text{nextprime}(\max(\text{shares}))$.
- Với mỗi tổ hợp (combination) của 3,4,5,6 shares, thực hiện Lagrange interpolation để tính $f(0) \mod p$.
- Chuyển giá trị $f(0)$ thành byte (hex $\rightarrow$ bytes). Kiểm tra xem chuỗi có nhiều ký tự printable ($>60\%$) để lọc ra kết quả hợp lý.
- In các combo và secret tương ứng, từ đó xác định ai phối hợp được.

### Lời giải

```python
# Lagrange interpolation
def lagrange_at_zero(xs, ys, p):
    out = 0
    k = len(xs)
    for i in range(k):
        xi, yi = xs[i], ys[i]
        num = 1
        den = 1
        for j in range(k):
            if j==i: continue
            xj = xs[j]
            num = (num * (-xj)) % p
            den = (den * (xi - xj)) % p
        out = (out + yi * num * pow(den, -1, p)) % p
    return out
```

```python
# Ghép shares phục hồi secret
for r in range(3,7):
    for combo in combinations(range(len(shares)), r):
        xs = [i+1 for i in combo]
        ys = [shares[i] for i in combo]
        secret_int = lagrange_at_zero(xs, ys, p)
        hexs = hex(secret_int)[2:].rjust(48,'0')  # đảm bảo 24 bytes
        secret = bytes.fromhex(hexs)
        frac = sum(1 for b in secret if 32 <= b <= 126) / len(secret)
        if frac > 0.6:
            print("combo", combo, "->", secret)
```

### Flag

`v1t{555_s3cr3t_sh4r1ng}`
