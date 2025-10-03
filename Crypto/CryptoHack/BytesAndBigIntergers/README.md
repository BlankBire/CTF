## Bytes and Big Integers — Writeup (CryptoHack)

### Mô tả tổng quan
- Nhiều hệ mật mã (như RSA) làm việc trên số nguyên lớn, trong khi thông điệp là chuỗi byte/ký tự.
- Cần ánh xạ chuỗi byte ↔ số nguyên. Thư viện `Crypto.Util.number` cung cấp `bytes_to_long()` và `long_to_bytes()` để chuyển đổi.
- Bài cho một số nguyên rất lớn; nhiệm vụ là chuyển ngược về thông điệp gốc bằng `long_to_bytes()`.

Ví dụ ánh xạ:
```
HELLO -> [0x48,0x45,0x4c,0x4c,0x4f] -> 0x48454c4c4f -> 310400273487
```

### Đề bài
- Cho số nguyên:
`11515195063862318899931685488813747395775516287289682636499965282714637259206269`
- Hãy chuyển số này về dạng bytes và giải mã ra chuỗi.

### Lời giải
- Dùng `long_to_bytes()` để chuyển số nguyên lớn về bytes, sau đó giải mã thành chuỗi.
```python
from Crypto.Util.number import long_to_bytes

n = 11515195063862318899931685488813747395775516287289682636499965282714637259206269
msg = long_to_bytes(n)
print(msg)
```

### Ghi chú
- Cần cài `pycryptodome`: `pip install pycryptodome`.
- Hàm là nghịch đảo của `bytes_to_long()`, rất hữu ích khi thao tác với RSA và dữ liệu binary.

### Flag
`crypto{3nc0d1n6_4ll_7h3_w4y_d0wn}`