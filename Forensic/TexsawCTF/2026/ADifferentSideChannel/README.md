## A Different Side Channel - Writeup (Texsaw CTF 2026)

### Mô tả

- Thử thách cung cấp 500 mẫu tiêu thụ năng lượng (power traces) từ một thiết bị mã hóa AES phần cứng. Các bản rõ tương ứng đã được biết trước, nhưng khóa bí mật là ẩn số.
- Mục tiêu là sử dụng các mẫu năng lượng này để khôi phục khóa AES-128 và giải mã tệp tin chứa flag.
- Flag format: `texsaw{flag}`.

### Tệp đính kèm

- `plaintexts.npy`: Chứa 500 bản rõ (16 bytes mỗi bản).
- `traces.npy`: Chứa 500 power traces (mỗi trace có 100 samples).
- `encrypted_flag.bin`: Tệp tin flag đã bị mã hóa.

### Phân tích

- **Nhận dạng thử thách:**
  Đây là một bài toán tấn công Side-Channel Attack kinh điển, cụ thể là Correlation Power Analysis (CPA). Trong các thiết bị phần cứng, việc xử lý dữ liệu (ví dụ: các bit 0 và 1) tiêu thụ một lượng năng lượng khác nhau. Mối quan hệ này thường tỷ lệ thuận với Trọng số Hamming (Hamming Weight - số lượng bit '1') của dữ liệu đang được xử lý.
  
- **Mô hình năng lượng:**
  AES thực hiện phép XOR giữa `plaintext` và `key`, sau đó đi qua bảng `S-box`. Chúng ta giả định rằng năng lượng tiêu thụ tại thời điểm thực hiện vòng 1 của AES tỷ lệ thuận với Hamming Weight của đầu ra S-box:
  $$P \approx HW(Sbox(plaintext \oplus key))$$

- **Thuật toán CPA:**
  1. Với mỗi byte của khóa (từ 0 đến 15):
     - Ta giả định tất cả 256 giá trị có thể có của byte khóa đó.
     - Với mỗi giá trị giả định, tính toán Hamming Weight lý thuyết cho tất cả 500 bản rõ.
     - Tính độ tương quan Pearson giữa dãy Hamming Weight lý thuyết và dữ liệu thực tế trong `traces.npy`.
     - Giá trị khóa nào có độ tương quan cao nhất sẽ là byte khóa đúng.
  2. Sau khi tìm được đủ 16 byte khóa, ta có được khóa AES-128 hoàn chỉnh.

### Lời giải

```python
SBOX = [...] # Bảng Sbox 256 giá trị

# Hàm tính độ tương quan Pearson
def calculate_correlation(matrix1, matrix2):
    m1_c = matrix1 - matrix1.mean(axis=0)
    m2_c = matrix2 - matrix2.mean(axis=0)
    num = np.dot(m1_c.T, m2_c)
    den = np.outer(np.sqrt(np.sum(m1_c**2, axis=0)), np.sqrt(np.sum(m2_c**2, axis=0)))
    return num / (den + 1e-15)

plaintexts = np.load('plaintexts.npy')
traces = np.load('traces.npy')

# Tấn công CPA khôi phục khóa
recovered_key = []
for i in range(16):
    hypotheses = np.zeros((500, 256))
    for k in range(256):
        hypotheses[:, k] = [bin(SBOX[p ^ k]).count('1') for p in plaintexts[:, i]]
    
    corrs = calculate_correlation(hypotheses, traces)
    recovered_key.append(np.argmax(np.max(np.abs(corrs), axis=1)))

key = bytes(recovered_key)

# Giải mã Flag (AES-CBC với NULL IV)
with open('encrypted_flag.bin', 'rb') as f:
    ciphertext = f.read()
cipher = AES.new(key, AES.MODE_CBC, iv=b'\x00'*16)
decrypted = cipher.decrypt(ciphertext)
```

**Kết quả giải mã:**
Khóa bí mật khôi phục được: `66dce15fb33deacb5c0362f30e95f52e`.
Nội dung giải mã chứa chuỗi flag ở khối thứ 2.

### Flag

`texsaw{d1ffer3nti&!_p0w3r_@n4!y51s}`
