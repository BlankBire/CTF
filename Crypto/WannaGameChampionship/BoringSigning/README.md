## Boring Signing - Writeup (WannaGame Championship)

### Mô tả

- Một thử thách RSA Signing với khả năng ký (Sign) và kiểm tra (Verify).
- Mục tiêu: Giả mạo chữ ký (Verify thành công) cho một thông điệp cụ thể:
  `"1_d4r3_y0u_70_519n_7h15_3x4c7_51x7y_f0ur_by73_57r1n9_w17h_my_k3y"`

### Tệp đính kèm

- `chall` (binary), `src/` (source code), `Dockerfile`.

### Phân tích

- **Cấu trúc bộ nhớ:** Biến toàn cục `v` được khai báo với thuộc tính `packed`:
  ```c
  struct __attribute__((packed)) variable {
      uint8_t msg[64];
      uint8_t N[384];
      // ...
  } v;
  ```
  Do đó, `v.N` nằm ngay sau `v.msg` trong bộ nhớ.

- **Lỗi Buffer Overflow (Off-by-one):**
  Hàm `input_b85` trong `base85.c` thực hiện đọc dữ liệu theo từng khối. Code sử dụng `fread` để đọc trực tiếp vào buffer đích:
  ```c
  // Khi n = 4 (block cuối cùng của buffer 64 bytes)
  // Đọc 5 bytes từ stdin vào buf
  fread(buf, 1, 5, stdin); 
  ```
  Tại khối cuối cùng của `v.msg` (trong trường hợp này là bytes 60-63), `fread` sẽ đọc 5 ký tự. 4 ký tự đầu dâu vào `v.msg[60..63]`, nhưng ký tự thứ 5 sẽ ghi đè lên byte tiếp theo trong bộ nhớ, chính là `v.N[0]`.
  Điều này cho phép kẻ tấn công thay đổi byte đầu tiên (LSB hoặc MSB tùy kiến trúc, ở đây là byte đầu mảng) của Modulus $N$ thành một ký tự Base85 bất kỳ.

- **Chiến lược tấn công (Fault Injection):**
  1. Lấy $N$ ban đầu từ server.
  2. Brute-force ký tự cuối cùng của input (sẽ ghi đè `v.N[0]`) sao cho giá trị $N'$ mới là một số nguyên tố.
  3. Khi $N'$ là số nguyên tố, phi hàm Euler $\phi(N') = N' - 1$.
  4. Tính khóa bí mật giả mạo: $d' = e^{-1} \pmod{N' - 1}$.
  5. Ký thông điệp mục tiêu: $S = H(m)^{d'} \pmod{N'}$.
  6. Gửi $S$ để server kiểm tra (lúc này server đang dùng $N'$ trong bộ nhớ để verify).

### Lời giải

Script `exploit.py` thực hiện các bước:
1. Kết nối và lấy $N$.
2. Tìm ký tự đè `good_char` để `isPrime(modified_N)` trả về True.
3. Gửi payload: `b"!" * 79 + bytes([good_char])` (79 ký tự padding + ký tự ghi đè).
   - Lưu ý: Base85 convert 4 bytes -> 5 chars. 64 bytes cần 80 chars. Ký tự thứ 80 chính là ký tự thừa ra ghi vào `v.N[0]`.
4. Tính chữ ký giả mạo và gửi verify.

### Flag

`W1{I_Sh0u1D_u5e_pYThoN_TO-ImPL3m3n7_CRyP7o9r4pHlc-5CH3M3S..6f7}`
