## Favorite Byte — Writeup (CryptoHack)

### Mô tả tổng quan
- Dữ liệu đã bị XOR với một khoá 1 byte không biết trước.
- Cần brute-force khoá `k ∈ [0..255]` để khôi phục plaintext. Nhớ giải hex trước.

### Đề bài
- Chuỗi hex: `73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d`
- Yêu cầu: tìm khoá XOR 1 byte và giải mã ra flag.

### Lời giải (brute-force khoá 1 byte)
```python
from pwn import xor
keyString = "73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d"
data = bytes.fromhex(keyString)
for k in range(256):
    result = xor(data, k)
    try:
        decoded = result.decode('ascii')
        if all(32 <= ord(c) <= 126 for c in decoded):
            print(decoded)
    except UnicodeDecodeError:
        continue
```

### Ghi chú
- Heuristic: lọc kết quả printable và chứa mẫu `crypto{` để nhanh chóng nhận đáp án đúng.

### Flag
`crypto{0x10_15_my_f4v0ur173_by7e}`