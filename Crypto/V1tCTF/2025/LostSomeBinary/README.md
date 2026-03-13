## Lost Some Binary - Writeup (V1tCTF)

### Mô tả

Một dãy các byte nhị phân, cách nhau bởi dấu cách được cung cấp với mô tả rằng một vài bit đã bị mất/ẩn.
Tệp kèm theo:

- `Lost_Some_Binary.txt`

### Phân tích

- File chứa nhiều byte dưới dạng nhị phân (8-bit groups). Khi nhìn qua, nhiều byte có vẻ là ký tự ASCII hợp lệ, nhưng mô tả nói "lost some binary" tức là có thể một phần thông tin bị mất, thường là ở LSB (least significant bit).
- Kỹ thuật phổ biến: Lấy bit cuối cùng (LSB) của mỗi byte và ghép lại thành một chuỗi bit mới, sau đó chia thành bytes 8-bit để giải mã ASCII. Đây là kỹ thuật steganography đơn giản: Ẩn giấu thông điệp ở LSB của mỗi byte - các bit được xem là ít quan trọng nhất.

### Ý tưởng

- Đọc file và tách thành danh sách các byte nhị phân.
- Tạo chuỗi bit mới bằng cách nối bit cuối cùng của từng byte.
- Nhóm chuỗi bit thành từng byte (8 bit) và chuyển sang ký tự ASCII.

### Lời giải

```python
with open("Lost_Some_Binary.txt", "r") as f:
    data = f.read().strip()
binary_list = data.split()
lsb_bits = ''.join(b[-1] for b in binary_list)
print("LSB bits:", lsb_bits)
lsb_message = ''
for i in range(0, len(lsb_bits), 8):
    if i+8 <= len(lsb_bits):
        byte = lsb_bits[i:i+8]
        lsb_message += chr(int(byte, 2))
print("LSB message:", lsb_message)
```

### Flag

`v1t{LSB:>}`
