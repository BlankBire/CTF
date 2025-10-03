## Encoding Hex — Writeup (CryptoHack)

### Mô tả tổng quan
- Chuỗi ASCII có thể được biểu diễn dưới dạng hex: mỗi ký tự → mã ASCII → biểu diễn base-16.
- Việc mã hoá hex giúp dữ liệu nhị phân dễ chia sẻ/hiển thị.

### Đề bài
- Cho chuỗi hex:
`63727970746f7b596f755f77696c6c5f62655f776f726b696e675f776974685f6865785f737472696e67735f615f6c6f747d`
- Hãy giải hex về bytes/chuỗi để thu được flag.

### Lời giải
```python
s = "63727970746f7b596f755f77696c6c5f62655f776f726b696e675f776974685f6865785f737472696e67735f615f6c6f747d"
print(bytes.fromhex(s).decode())
```

### Ghi chú
- `bytes.fromhex()` đổi hex → bytes; cần `.decode()` để in ra chuỗi văn bản.

### Flag
`crypto{You_will_be_working_with_hex_strings_a_lot}`