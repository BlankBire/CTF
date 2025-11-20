## RSA101 - Writeup (V1tCTF)

### Mô tả

- Challenge cung cấp các tham số RSA cơ bản `n`, `e`, `c` trong file `RSA_101.txt`.
- Nhiệm vụ: Tìm khóa riêng và giải mã `c` để thu được flag.

### Tệp đính kèm

- `RSA_101.txt`

### Phân tích

- `n` phân tích được thành hai thừa số nhỏ: `p = 101` và `q = 313846144900241708687128313929756784551`.
- Khi đã biết `p`, `q` ta có $\varphi(n) = (p-1)(q-1)$.
- Khóa riêng là nghịch đảo của $e$ modulo $\varphi(n)$: $d \equiv e^{-1} \pmod{\varphi(n)}$.
- Giải mã: $m \equiv c^d \pmod{n}$, sau đó đổi $m$ từ số sang chuỗi.
- Vì RSA làm việc trên số nguyên modulo $n$, bản rõ thực tế có thể được biểu diễn dạng $m + k n$ khi thiếu padding hoặc bị rút gọn byte đầu; thử thêm vài giá trị $k$ nhỏ giúp kiểm tra các biểu diễn đó và tìm chuỗi printable.

### Lời giải

```python
from Cryptodome.Util.number import long_to_bytes

n = 31698460634924412577399959706905435239651
p = 101
q = 313846144900241708687128313929756784551
e = 65537
c = 23648999580642514140599125257944114844209

phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)
m = pow(c, d, n)

for k in range(5):
    candidate = long_to_bytes(m + k * n)
    print(candidate)
```

- Script in ra chuỗi ASCII chứa flag ở lần lặp `k = 1`.

### Flag

`v1t{RSA_101_b4by}`
