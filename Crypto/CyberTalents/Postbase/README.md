## Postbase — Writeup (CyberTalents)

### Mô tả
Chuỗi Base64 bị nhiễu (tiền tố hỏng) cần loại bỏ phần thừa rồi giải mã Base64 để lấy flag.

### Yêu cầu
- Python 3

### Lời giải
Trong thư mục `Postbase`:

```bash
python .\main.py
```

Script loại phần tiền tố lỗi và `base64.b64decode` để in ra flag ở dạng bytes.

### Ghi chú
- Base64 hợp lệ có độ dài bội số của 4; nếu có tiền tố rác, hãy cắt đi trước khi decode.
- Nếu output là bytes, có thể cần `.decode()` để ra chuỗi (nếu dữ liệu là ASCII/UTF-8).

### Flag
`FLAG{B453_61X7Y_4R}`