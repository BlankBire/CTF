## Aescure - Writeup (AmateursCTF)

### Mô tả tổng quan

- Challenge cung cấp `chall.py`, sử dụng `AES.new(flag, AES.MODE_ECB)` rồi mã hóa một block toàn `0x00`.
- Kết quả duy nhất có thể biết là ciphertext `5aed095b21675ec4ceb770994289f72b`.
- Khóa chính là nội dung `flag.txt`, cũng chính là flag cần tìm.

### Đề bài

- Chỉ có file `chall.py` và ciphertext mẫu ở trên.
- Mục tiêu: khôi phục chuỗi flag sao cho `AES-128-ECB(flag, 0^{16}) = 5aed095b21675ec4ceb770994289f72b`.

### Phân tích

- AES-128 yêu cầu khóa dài đúng 16 byte. Flag của AmateursCTF có dạng `amateursCTF{...}`.
- Chuỗi `amateursCTF{` dài 12 byte, thêm `}` là 13 byte, còn thiếu 3 byte để đủ 16 → chỉ cần brute-force ba ký tự bên trong.
- Đây là known-plaintext attack: biết plaintext (block 0) và ciphertext, chỉ chưa biết khóa.
- Không gian tìm kiếm ~ `len(alphabet)^3`, chạy trong tích tắc.

### Lời giải

```python
from Crypto.Cipher import AES
import itertools
import string

TARGET_HEX = "5aed095b21675ec4ceb770994289f72b"
PREFIX = "amateursCTF{"
SUFFIX = "}"
PLAIN_BLOCK = b"\x00" * 16
alphabet = string.ascii_letters + string.digits + "_{}!?$@#"

for combo in itertools.product(alphabet, repeat=3):
    candidate = f"{PREFIX}{''.join(combo)}{SUFFIX}"
    cipher = AES.new(candidate.encode(), AES.MODE_ECB)
    if cipher.encrypt(PLAIN_BLOCK).hex() == TARGET_HEX:
        print(candidate)
        break
```

### Flag

`amateursCTF{@3s}`
