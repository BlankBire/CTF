## XOR Properties — Writeup (CryptoHack)

### Mô tả tổng quan
- Ôn lại tính chất XOR: giao hoán, kết hợp, phần tử đơn vị 0, tự nghịch (`x ^ x = 0`).
- Dùng các tính chất để gỡ chuỗi XOR nhiều khoá và tìm flag.

### Dữ liệu
```
KEY1 = a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313
KEY2 ^ KEY1 = 37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e
KEY2 ^ KEY3 = c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1
FLAG ^ KEY1 ^ KEY3 ^ KEY2 = 04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf
```

### Lời giải (ý tưởng)
- Khôi phục `KEY2 = (KEY2 ^ KEY1) ^ KEY1`.
- Khôi phục `KEY3 = (KEY2 ^ KEY3) ^ KEY2`.
- Flag `= (FLAG ^ KEY1 ^ KEY3 ^ KEY2) ^ KEY1 ^ KEY2 ^ KEY3`.

### Lời giải (mã mẫu)
```python
KEY1 = 0xa6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313
KEY12 = 0x37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e
KEY23 = 0xc1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1
KEY_F123 = 0x04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf

KEY2 = KEY1 ^ KEY12
KEY3 = KEY2 ^ KEY23
KEY_F = KEY1 ^ KEY2 ^ KEY3 ^ KEY_F123

print(bytes.fromhex(hex(KEY_F)[2:]))
```

### Flag
`crypto{x0r_i5_ass0c1at1v3}`