## RSA101 — Writeup (CyberTalents)

### Mô tả
Giải mã ciphertext bằng khóa riêng RSA ở `key.pem` với padding PKCS#1 v1.5.

### Yêu cầu
- Python 3
- PyCryptodome (`pip install pycryptodome`)

### Lời giải
Trong thư mục `RSA101`:

```bash
python .\main.py
```

Script sẽ:
- Đọc `key.pem` và `cipher` (nhị phân)
- Dùng `PKCS1_v1_5.new(key).decrypt(...)` để lấy plaintext và in ra

### GGhi chú
- Nếu `print(plaintext.decode())` lỗi, có thể dùng `errors="ignore"` hoặc in dạng hex.
- Đảm bảo `key.pem` đúng định dạng PEM của private key.

### Flag
`flag{RSA_nice_try}`