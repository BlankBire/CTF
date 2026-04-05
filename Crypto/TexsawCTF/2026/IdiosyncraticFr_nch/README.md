## Idiosyncratic Fr*nch - Writeup (Texsaw CTF 2026)

### Mô tả

- Thử thách cung cấp một tệp tin `ciphertext.txt` chứa một đoạn mã hóa văn bản.
- Gợi ý từ tiêu đề "Idiosyncratic Fr*nch" (thiếu chữ 'e' trong từ "French") và mô tả yêu cầu giải mật mã, sau đó dùng OSINT để tìm tác giả của văn bản gốc.
- Flag format: `txsaw{first_last}`.

### Tệp đính kèm

- `ciphertext.txt`.

### Phân tích

- **Nhận dạng mã hóa:**
  Dựa vào cấu trúc các từ ngắn (N, zi, zw, bp), có thể dự đoán đây là mã hóa thay thế đơn giản (Simple Substitution Cipher). Tần suất các chữ cái trong ciphertext cho thấy sự tương đồng với các cấu trúc từ tiếng Anh thông dụng.
- **Giải mã:**
  Bằng cách phân tích các từ lặp lại và cấu trúc câu:
  - `Azza wfahv ztu` -> `Noon rings out` (A=N, z=O, a=n, w=R, f=I, h=G, v=S, t=U, u=T).
  - `ugnu` -> `that` (u=T, g=H, n=A).
  - `rgflg` -> `which` (r=W, g=H, f=I, l=C).
  - `zi` -> `of` (z=O, i=F).
- **Nội dung sau giải mã:**
  Văn bản sau khi giải mã là đoạn mở đầu của cuốn tiểu thuyết nổi tiếng **"A Void"** (bản dịch tiếng Anh) của tác giả **Georges Perec**.
- **OSINT:**
  Cuốn tiểu thuyết này nguyên tác tiếng Pháp là **"La Disparition"** nổi tiếng vì là một lipogram - toàn văn không chứa chữ cái 'e'. Đây là lý do tại sao tiêu đề thử thách lại viết là "Fr*nch". Tác giả của nguyên tác chính là Georges Perec.
  Một chi tiết thú vị là tên của Georges Perec chứa rất nhiều chữ 'e', tạo nên sự tương phản đầy tính biểu tượng với tác phẩm của ông.

### Lời giải

Script `solve.py` thực hiện giải mã dựa trên bảng alphabet thay thế đã tìm được:

```python
def decrypt(text):
    mapping = {
        'a': 'n', 'b': 'm', 'c': 'l', 'd': 'k', 'e': 'j', 'f': 'i', 'g': 'h', 'h': 'g',
        'i': 'f', 'j': 'q', 'k': 'd', 'l': 'c', 'm': 'b', 'n': 'a', 'o': 'p', 'p': 'y',
        'q': 'x', 'r': 'w', 's': 'v', 't': 'u', 'u': 't', 'v': 's', 'w': 'r', 'x': 'z',
        'y': 'p', 'z': 'o'
    }

    res = ""
    for char in text:
        lower_char = char.lower()
        if lower_char in mapping:
            new_char = mapping[lower_char]
            res += new_char.upper() if char.isupper() else new_char
        else:
            res += char
    return res
```

Kết quả giải mã tiết lộ văn bản thuộc về tác phẩm của **Georges Perec**.

### Flag

`txsaw{georges_perec}`