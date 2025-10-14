## XOR Starter — Writeup (CryptoHack)

### Mô tả tổng quan
- XOR (`^`) trả 1 khi bit khác nhau, trả 0 khi giống nhau. Là phép tự nghịch: `x ^ k ^ k = x`.
- Bài cho chuỗi `label`; yêu cầu XOR từng ký tự với số `13` rồi ghép lại.

### Lời giải ngắn
```python
s = "label"
print("".join(chr(ord(ch) ^ 13) for ch in s))
```

### Minh hoạ bit
```
l : 01101100
13: 00001101
^ : 01100001 -> 'a'
```

### Flag
`crypto{aloha}`