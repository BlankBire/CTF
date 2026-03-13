## MisconfiguredRSA - Writeup (V1tCTF)

### Mô tả

Các giá trị RSA bao gồm `n`, `e`, `c` được cung cấp, mục tiêu là thông qua 3 giá trị đó, giải mã `c` thu được thông điệp liên quan đến flag.
Tệp kèm theo:

- `misconfigured_RSA.txt`

### Ý tưởng

- Nếu `n` là tích hai số nguyên tố lớn `p * q` thì cần factor `n` để lấy $\phi(n) = (p-1)(q-1)$.
- Nếu `n` là một số nguyên tố thì $\phi(n) = n - 1$ (Ở trường hợp của challenge này thì `n` là một số nguyên tố lớn).
- Tính khóa riêng $d = e^{-1} \mod \phi(n)$.
- Thực hiện giải mã `c` bằng khóa riêng `d`, thu được thông điệp $m = c^d \mod n$, flag ẩn trong giá trị `m`.

### Lời giải

```python
# Sử dụng sympy.isprime(n) trả về True --> n là số nguyên tố lớn
phi = n - 1
d = pow(e, -1, phi)
m = pow(c, d, n)
print(bytes.fromhex(hex(m)[2:]).decode())
```

### Flag

`v1t{f3rm4t_l1ttl3_duck}`
