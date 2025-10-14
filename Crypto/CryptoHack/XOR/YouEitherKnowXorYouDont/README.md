## You Either Know XOR You Don't — Writeup (CryptoHack)

### Mô tả tổng quan

- Bài yêu cầu nhận ra cấu trúc flag bắt đầu bằng tiền tố `crypto{` và áp dụng XOR để khôi phục khoá/chuỗi đúng.
- Khi biết trước một phần plaintext (known-plaintext), có thể XOR ngược để tìm ra phần khoá tương ứng do tính chất: `C = P ^ K` ⇒ `K = C ^ P`.

### Đề bài

- Cho ciphertext dạng hex:
  `0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104`
- Biết flag có định dạng bắt đầu bằng `crypto{...}`.

### Lời giải

```python
from pwn import xor
encrypted_bytes = bytes.fromhex("0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104")
# Gợi ý từ đề: dùng known-plaintext để suy ra khoá "myXORkey"
key = b"myXORkey"
flag = xor(encrypted_bytes, key)
print(flag)
```

### Ghi chú

- Tính chất XOR: biết `P` và `C` thì suy được `K`. Với một phần đầu `P0 = b"crypto{"`, có thể thử suy khoá rồi lặp theo chu kỳ.
- Trong lời giải này, khoá tuần hoàn `"myXORkey"` được áp dụng trên toàn ciphertext để thu được flag đầy đủ.

### Flag

- `crypto{1f_y0u_Kn0w_En0uGH_y0u_Kn0w_1t_4ll}`
