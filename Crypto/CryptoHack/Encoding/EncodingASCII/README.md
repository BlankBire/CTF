## Encoding ASCII — Writeup (CryptoHack)

### Mô tả tổng quan
- ASCII là chuẩn 7-bit biểu diễn ký tự bằng số nguyên 0–127.
- Bài cho một mảng số nguyên, mỗi số là mã ASCII của ký tự trong cờ (flag).

### Đề bài
- Dữ liệu: `[99, 114, 121, 112, 116, 111, 123, 65, 83, 67, 73, 73, 95, 112, 114, 49, 110, 116, 52, 98, 108, 51, 125]`
- Yêu cầu: chuyển mỗi số sang ký tự (`chr`) rồi ghép lại thành chuỗi flag.

### Lời giải
```python
arr = [99,114,121,112,116,111,123,65,83,67,73,73,95,112,114,49,110,116,52,98,108,51,125]
print("".join(chr(i) for i in arr))
```

### Ghi chú
- `chr()` chuyển mã số → ký tự; `ord()` làm ngược lại.

### Flag
`crypto{ASCII_pr1nt4bl3}`