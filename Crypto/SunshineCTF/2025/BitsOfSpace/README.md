## Bits Of Space — Writeup (SunshineCTF)

### Mô tả tổng quan

- Service TCP ở `0.0.0.0:25401` nhận “subscription packet” là `IV || CIPHERTEXT` (AES-CBC, key bí mật phía server).
- Sau khi giải mã và unpad, server parse plaintext theo `struct.pack("<IQQI")` → 4 field:
  - `device_id: uint32`
  - `start: uint64`
  - `end: uint64`
  - `channel: uint32`
- Nếu `device_id == 0xdeadbabe` (Restricted Relay) thì server trả flag ngay.

File tham khảo trong thư mục:

- `relay.py`: server logic (giải mã AES-CBC, kiểm tra `device_id`, in thông điệp/flag).
- `voyager.bin`: payload mẫu đã được mã hoá (bao gồm IV ở 16 byte đầu).
- `secrets.py`: PoC chỉnh IV để mạo danh thiết bị.

### Ý tưởng khai thác

AES-CBC không có MAC → gói tin có thể bị chỉnh sửa một cách có chủ đích do tính chất “malleability” của CBC.

- Ở CBC, byte plaintext khối đầu tiên sau giải mã là: `P1 = D(K, C1) XOR IV`.
- Nếu muốn thay đổi 4 byte đầu của `P1` (tức là `device_id`), ta không cần biết key; chỉ cần chỉnh IV:
  - Gọi `old = struct.pack("<I", 0x13371337)` là `device_id` cũ trong plaintext ban đầu.
  - Gọi `new = struct.pack("<I", 0xdeadbabe)` là `device_id` mong muốn.
  - Khi đó chỉ cần XOR ở 4 byte đầu của IV: `IV'[i] = IV[i] XOR old[i] XOR new[i]` (i = 0..3).
- Gửi `IV' || CIPHERTEXT` tới server → sau giải mã, `device_id` trở thành `0xdeadbabe` ⇒ server trả flag.

### Các bước thực hiện

1. Đọc `voyager.bin`, tách `iv = data[:16]` và `body = data[16:]`.
2. Tính `old = pack('<I', 0x13371337)` và `new = pack('<I', 0xdeadbabe)`.
3. Thay 4 byte đầu của IV theo `iv[i] ^= old[i] ^ new[i]`.
4. Kết nối tới host challenge và gửi `iv + body`.

### PoC (Python, dùng pwntools)

```python
from pwn import remote
import struct

with open("voyager.bin", "rb") as f:
    data = f.read()

iv = bytearray(data[:16])
body = data[16:]

old = struct.pack("<I", 0x13371337)
new = struct.pack("<I", 0xdeadbabe)

for i in range(4):
    iv[i] ^= old[i] ^ new[i]

io = remote("sunshinectf.games", 25401)
io.send(iv + body)
print(io.recvall(timeout=2).decode(errors="ignore"))
```

Ghi chú:

- Có thể đổi `host/port` cho phù hợp nếu chạy bản local.
- Không cần thư viện crypto để khai thác; chỉ cần XOR IV vì mục tiêu là thay đổi `device_id` ở khối plaintext đầu.

### Kết luận

- Lỗ hổng là thiếu xác thực toàn vẹn (không có MAC/AEAD). Với AES-CBC thuần, kẻ tấn công có thể bitflip IV để điều khiển một phần plaintext sau giải mã.
- Khắc phục: sử dụng AEAD (ví dụ AES-GCM/ChaCha20-Poly1305) hoặc thêm MAC/HMAC trên toàn bộ `IV || CIPHERTEXT` và kiểm tra trước khi giải mã/parse.

### Flag

`sun{m4yb3_4_ch3ck5um_w0uld_b3_m0r3_53cur3}`
