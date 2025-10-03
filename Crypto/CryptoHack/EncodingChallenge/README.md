## Encoding Challenge — Writeup (CryptoHack)

### Mô tả tổng quan
- Server chạy 100 level, mỗi level gửi JSON mô tả kiểu mã hoá và dữ liệu `encoded`.
- Client phải giải mã đúng và trả JSON với trường `decoded`. Qua 100 level sẽ nhận flag.

Kết nối: `socket.cryptohack.org 13377`

### Kiểu mã hoá có thể gặp
- `base64`: chuỗi Base64 → dùng `base64.b64decode()`.
- `hex`: chuỗi hex → `bytes.fromhex()`.
- `rot13`: dùng `codecs.decode(x, 'rot_13')`.
- `bigint`: chuỗi dạng `0x...` của `hex(bytes_to_long(msg))` → bỏ `0x`, hex→bytes→decode.
- `utf-8`: danh sách số nguyên mã ký tự → `"".join(chr(c) for c in arr)`.

### Khung script (pwntools)
```python
from pwn import remote
import json, base64, codecs

r = remote('socket.cryptohack.org', 13377)

def json_recv():
    return json.loads(r.recvline().decode())

def json_send(obj):
    r.sendline(json.dumps(obj).encode())

for _ in range(101):
    rec = json_recv()
    t = rec.get('type')
    v = rec.get('encoded')
    if t == 'base64':
        decoded = base64.b64decode(v).decode()
    elif t == 'hex':
        decoded = bytes.fromhex(v).decode()
    elif t == 'rot13':
        decoded = codecs.decode(v, 'rot_13')
    elif t == 'bigint':
        decoded = bytes.fromhex(v[2:]).decode()
    elif t == 'utf-8':
        decoded = ''.join(chr(c) for c in v)
    json_send({'type': t, 'decoded': decoded})
```

### Ghi chú
- Cài: `pip install pwntools pycryptodome`.
- Server luôn trao đổi JSON theo dòng, đọc/ghi từng dòng.

### Flag
`crypto{3nc0d3_d3c0d3_3nc0d3}`