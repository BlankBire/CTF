## Smooth Criminal - Writeup (UTCTF)

### Mô tả

- Một thử thách về bài toán Logarit rời rạc (Discrete Logarithm Problem - DLP) với lỗ hổng liên quan đến số trơn (Smooth number).
- Người chơi được cung cấp các tham số $p, g, h$ và phương trình $h \equiv g^x \pmod p$.
- Mục tiêu: Tìm giá trị số mũ bí mật $x$, sau đó chuyển $x$ từ dạng số nguyên sang dạng chuỗi byte để lấy flag.

### Tệp đính kèm

- `dlp.txt`, `main.py`

### Phân tích

- **Lỗ hổng: Thuật toán Pohlig-Hellman:**
  Với một số nguyên tố $p$, cấp của nhóm nhân modulo $p$ chính là $p - 1$. Độ an toàn của bài toán Logarit rời rạc phụ thuộc hoàn toàn vào việc $p - 1$ phải chứa ít nhất một thừa số nguyên tố cực kỳ lớn.
- Nếu $p - 1$ được tạo thành từ toàn các thừa số nguyên tố rất nhỏ (trong mật mã học gọi đây là số "Smooth" - số trơn), một kẻ tấn công có thể dễ dàng áp dụng thuật toán Pohlig-Hellman. Thuật toán này sẽ chia bài toán DLP siêu to khổng lồ ban đầu thành hàng loạt các bài toán DLP tí hon (có thể giải trong nháy mắt), sau đó dùng Định lý số dư Trung Hoa (CRT) để ghép nối kết quả lại và tìm ra $x$.
- Khi phân tích nhân tử số nguyên tố $p$ (dài 649-bit) của bài toán này, kết quả thật thảm họa: **Thừa số nguyên tố lớn nhất của $p - 1$ chỉ là 197!**
- Điều này biến cái ổ khóa 649-bit thành một trò hề vì nó quá "smooth", tạo điều kiện lý tưởng cho thuật toán Pohlig-Hellman phá vỡ trong tích tắc.

### Lời giải

Script `main.py` thực hiện các bước giải mã:

1. Import module giải DLP từ thư viện toán học học `sympy` (thư viện này sẽ tự động áp dụng thuật toán Pohlig-Hellman khi phát hiện $p-1$ là số trơn).
2. Nạp các hằng số $p, g, h$ cho trước.
3. Giải bài toán DLP tìm số nguyên $x = \log_g(h) \pmod p$ bằng hàm `discrete_log`.
4. Tính độ dài byte của $x$ và dùng `to_bytes` để chuyển $x$ về chuỗi byte (big-endian).
5. Giải mã chuỗi byte thành flag dạng text.

Trích đoạn code giải (`main.py`):

```python
x = discrete_log(p, h, g)
flag = x.to_bytes((x.bit_length() + 7) // 8, 'big')
```

### Flag

`utflag{sm00th_cr1m1nal_caught}`
