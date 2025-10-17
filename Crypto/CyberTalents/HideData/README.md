## HideData — Writeup (CyberTalents)

### Mô tả
Giải mã chuỗi trong `cipher.txt` được mã hóa bằng ROT13.

### Yêu cầu
- Python 3 (dùng thư viện chuẩn `codecs`).

### Lời giải
Trong thư mục `HideData`:

```bash
python .\main.py
```

Script sẽ đọc `cipher.txt`, giải mã ROT13 và in ra plaintext (flag).

### GGhi chú
- ROT13 là phép thay thế chữ cái quay 13 ký tự, áp dụng hai lần sẽ trả về ban đầu.
- Cũng có thể tự kiểm tra nhanh bằng các công cụ online ROT13.

### Flag
`2j68yfhqlz`