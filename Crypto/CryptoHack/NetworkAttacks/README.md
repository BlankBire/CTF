## Network Attacks — Writeup (CryptoHack)

### Mô tả tổng quan
- Bài yêu cầu giao tiếp socket bằng JSON. Dùng `pwntools` để kết nối và gửi/nhận JSON theo dòng.
- Server bán duy nhất một mặt hàng đặc biệt: `flag`.

Kết nối: `socket.cryptohack.org 11112`

### Lời giải
Gửi JSON có trường `buy` với giá trị `flag`.
```python
from pwn import remote
import json

io = remote('socket.cryptohack.org', 11112)

def json_send(obj):
    io.sendline(json.dumps(obj).encode())

def json_recv():
    return json.loads(io.recvline().decode())

json_send({"buy": "flag"})
print(json_recv())
```

### Ghi chú
- Cài: `pip install pwntools`.
- Server trả JSON; chỉ cần đọc dòng tiếp theo sau khi gửi.

### Flag
`crypto{sh0pp1ng_f0r_fl4g5}`