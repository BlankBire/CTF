## Great Snakes — Writeup (CryptoHack)

### Mô tả tổng quan
- Script kèm theo in ra flag khi chạy.
- Bản chất: mỗi số trong mảng là ký tự flag đã XOR với `0x32`.

### Lời giải
```python
ords = [81,64,75,66,70,93,73,72,1,92,109,2,84,109,66,75,70,90,2,92,79]
print("".join(chr(o ^ 0x32) for o in ords))
```

### Ghi chú
- XOR với một hằng số là phép biến đổi tự nghịch: giải mã bằng cách XOR lại cùng hằng số.

### Flag
`crypto{z3n_0f_pyth0n}`