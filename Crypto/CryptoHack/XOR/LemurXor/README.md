## Lemur XOR — Writeup (CryptoHack)

### Mô tả tổng quan

- Bài cho hai ảnh PNG giống nhau về nội dung hiển thị nhưng khác dữ liệu nhị phân.
- Ý tưởng: hai ảnh đã bị XOR với cùng một khoá/hoặc nhau; thực hiện XOR pixel-by-pixel (hoặc byte-by-byte) giữa hai ảnh để lộ thông tin ẩn (thường là chữ/flag).

### Đề bài

- Cho hai tệp ảnh `flag.png` và `lemur.png`, yêu cầu tìm flag bằng kỹ thuật XOR ảnh.

### Lời giải (Python, Pillow)

```python
from PIL import Image

img1 = Image.open('lemur.png').convert('RGB')
img2 = Image.open('flag.png').convert('RGB')

# Đảm bảo cùng kích thước
assert img1.size == img2.size

out = Image.new('RGB', img1.size)
px1 = img1.load()
px2 = img2.load()
pxo = out.load()

for y in range(img1.height):
    for x in range(img1.width):
        r1,g1,b1,a1 = px1[x,y]
        r2,g2,b2,a2 = px2[x,y]
        pxo[x,y] = (r1 ^ r2, g1 ^ g2, b1 ^ b2)

out.save('xor_output.png')
```

### Ghi chú

- Nếu ảnh có kênh alpha, nên ép về `RGBA` để xử lý thống nhất; kết quả đặt alpha `255` cho rõ.
- Có thể XOR trực tiếp trên bytes của file, nhưng XOR theo pixel giúp quan sát kết quả ngay.

### Flag

- `crypto{X0Rly_n0t!}`
