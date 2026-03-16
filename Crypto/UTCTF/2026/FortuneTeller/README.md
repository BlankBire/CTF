## Fortune Teller - Writeup (UTCTF)

### Mô tả

- Một thử thách về Linear Congruential Generator (LCG) khá cơ bản.
- Người chơi được cung cấp 4 output liên tiếp đầu tiên của bộ sinh ($x_1, x_2, x_3, x_4$) và `ciphertext` hex.
- Mục tiêu là cần tìm ra các tham số bí mật (multiplier $a$, increment $c$) bị giấu để từ đó tính được output thứ 5 ($x_5$) dùng làm khóa XOR để giải mã lấy flag.

### Tệp đính kèm

- `main.py`, `lcg.txt`.

### Phân tích

- **Cấu trúc của LCG:**
  Trong LCG, mỗi state sinh ra state tiếp theo theo công thức $x_{n+1} \equiv (a \cdot x_n + c) \pmod m$. Với $m = 4294967296$ ($2^{32}$) và 4 giá trị $x_1, x_2, x_3, x_4$ đã biết, bài toán được quy về việc giải hệ phương trình đồng dư.
- **Loại bỏ biến c:**
  Thiết lập phương trình cho 2 output liên tiếp:
  $x_2 \equiv (a \cdot x_1 + c) \pmod m$
  $x_3 \equiv (a \cdot x_2 + c) \pmod m$.
  Lấy phương trình trên trừ phương trình dưới, khử được $c$:
  $x_2 - x_3 \equiv a \cdot (x_1 - x_2) \pmod m$
- **Tìm a và c:**
  Từ phương trình khử, có thể tính được $a$ thông qua modulo nghịch đảo:
  $a \equiv (x_2 - x_3) \cdot (x_1 - x_2)^{-1} \pmod m$.
  Sau đó, dễ dàng tính được $c$:
  $c \equiv (x_2 - a \cdot x_1) \pmod m$

### Lời giải

Script `main.py` thực hiện các bước:

1. Thiết lập các giá trị $x_1, x_2, x_3, x_4$ và tham số module $m = 2^{32}$.
2. Tính $a$ bằng cách lấy $(x_2 - x_3)$ nhân với nghịch đảo modulo của $(x_1 - x_2)$ theo $m$.
3. Tính $c = (x_2 - a \cdot x_1) \pmod m$.
4. Áp dụng công thức LCG để tìm output thứ 5: $x_5 = (a \cdot x_4 + c) \pmod m$.
5. Chuyển đổi $x_5$ sang cấu trúc 4-byte big-endian.
6. Lấy từng byte của đoạn ciphertext hex XOR tuần tự với $x_5$ (lặp lại dạng 4-byte key) để khôi phục flag.

```python
ciphertext = bytes.fromhex(ciphertext_hex)

a = (x2 - x3) * pow((x1 - x2), -1, m) % m
c = (x2 - a * x1) % m

x5 = (a * x4 + c) % m
x5_bytes = x5.to_bytes(4, 'big')

flag = bytes(ciphertext[i] ^ x5_bytes[i % 4] for i in range(len(ciphertext)))
```

### Flag

`utflag{pr3d1ct_th3_futur3_lcg}`
