## Encoding Base64 — Writeup (CryptoHack)

### Mô tả tổng quan
- Base64 biểu diễn dữ liệu nhị phân dưới dạng chuỗi ASCII với 64 ký tự.
- 4 ký tự Base64 mã hoá 3 byte nhị phân; thường dùng để nhúng dữ liệu trong các hệ thống văn bản.

### Đề bài
- Cho chuỗi hex: `72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf`
- Yêu cầu: giải hex → bytes, sau đó mã hoá Base64.

### Lời giải
```python
import base64

h = "72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf"
b = bytes.fromhex(h)
ans = base64.b64encode(b).decode()
print(ans)
```

### Ghi chú
- `bytes.fromhex()` chuyển hex → bytes; `base64.b64encode()` trả về bytes Base64, cần `.decode()` để thành chuỗi.

### Flag
`crypto/Base+64+Encoding+is+Web+Safe/`