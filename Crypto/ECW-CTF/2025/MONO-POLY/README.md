## MONO-POLY — Writeup (ECW-CTF)

### Mô tả tổng quan
- Challenge này sử dụng **monoalphabetic substitution cipher** (mã thay thế đơn âm) - một loại mã hóa cổ điển.
- Trong mã thay thế đơn âm, mỗi ký tự trong bảng chữ cái được thay thế bằng một ký tự khác theo một quy tắc cố định.
- Bài cho một đoạn văn bản đã được mã hóa và yêu cầu giải mã để tìm flag.

### Đề bài
- File `ciphertext.txt` chứa văn bản đã được mã hóa bằng monoalphabetic substitution cipher.
- Văn bản gốc là tiếng Anh, cần tìm quy tắc thay thế để giải mã.
- Flag được ẩn trong văn bản đã giải mã.

### Phân tích
- Văn bản mã hóa bắt đầu với "KFEEH DFQY" - có thể là "HELLO FRIEND".
- Dựa vào phân tích tần suất ký tự và ngữ cảnh, có thể xây dựng bảng thay thế.
- Các ký tự phổ biến trong tiếng Anh như E, T, A, O, I, N, S, H, R xuất hiện nhiều nhất.

### Lời giải
```python
try:
    with open('./ciphertext.txt', 'r', encoding='utf-8') as file:
        content = file.read()
    from_chars = "ABCEFGHIJKLMNOPQRSUVWXYZ"  
    to_chars   = "MSULEXORCHJGKPYAFZWQBVNI" 
    translation_table = str.maketrans(from_chars, to_chars)
    mapped_content = content.translate(translation_table)

    print(mapped_content)
except FileNotFoundError:
    print("File not found")
```

### Phương pháp giải
1. **Phân tích tần suất**: Đếm tần suất xuất hiện của từng ký tự trong văn bản mã hóa.
2. **So sánh với tiếng Anh**: So sánh với tần suất ký tự chuẩn trong tiếng Anh (E, T, A, O, I, N, S, H, R).
3. **Phân tích từ ngắn**: Tìm các từ 1-2 ký tự để xác định các ký tự phổ biến.
4. **Xây dựng bảng thay thế**: Dần dần xây dựng mapping từ ký tự mã hóa sang ký tự gốc.
5. **Kiểm tra và điều chỉnh**: Thử nghiệm và điều chỉnh bảng thay thế cho đến khi văn bản có nghĩa.
6. **Phát hiện flag giả**: Sau khi giải mã thành công, xuất hiện flag `ICO{BSUTJI_EFAVYHRMOF_DSR_LFI_WAL}` nhưng vẫn còn được mã hóa thêm một lớp nữa.
7. **Giải mã Vigenere**: Flag giả có format không đúng `ECW{...}` sau khi giải mã theo phân tích tần suất, cần giải mã thêm bằng Vigenere cipher như đã đề cập trong văn bản.
    - Phân tích key: I → E, C → C, O → W cho thấy key bắt đầu bằng "EAS".
      + I → E: (I - key_char) mod 26 = E → (8 - key_char) mod 26 = 4 → key_char = 4 → 'E'
      + C → C: (C - key_char) mod 26 = C → (2 - key_char) mod 26 = 2 → key_char = 0 → 'A'
      + O → W: (O - key_char) mod 26 = W → (14 - key_char) mod 26 = 22 → key_char = 18 → 'S'
    - Dựa vào ngữ cảnh challenge nhấn mạnh từ "EASY", xác định key là "EASY".
    - Sử dụng tool https://cipherott.blogspot.com/2015/01/online-dich-va-ma-hoa-vigenere.html với key "EASY" để giải mã flag cuối cùng.

### Ghi chú
- Monoalphabetic substitution cipher dễ bị phá bằng phân tích tần suất.
- Cần chú ý đến ngữ cảnh và cấu trúc từ để xác định chính xác mapping.
- Có thể sử dụng các công cụ online hoặc script tự động để hỗ trợ phân tích.

### Flag
`ECW{DOUBLE_ENCRYPTION_FOR_THE_WIN}`
