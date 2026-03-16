## Oblivious Error - Writeup (UTCTF)

### Mô tả

- Một thử thách về giao thức truyền tải không phân biệt 1-2 (1-2 Oblivious Transfer) dựa trên hệ mã RSA.
- Tác giả đã vô tình xóa mất một đoạn code gốc của giao thức và thay thế bằng một dòng code lỗi, dẫn đến việc Message 2 bị hỏng và không thể giải mã theo cách thông thường.
- Mục tiêu: Tìm cách lợi dụng đoạn code lỗi này để khôi phục lại chuỗi Message 2 (vốn dĩ là nội dung chứa flag). 

### Tệp đính kèm

- `my-code.txt`, tương tác qua netcat `challenge.utctf.live 8379`.

### Phân tích

- **Giao thức 1-2 Oblivious Transfer cơ bản:** 
  Đáng lẽ ra, Bob (người nhận) sẽ tạo ra một giá trị $v = (x_b + k^e) \pmod N$, với $b \in \{0, 1\}$ là chỉ số của tin nhắn muốn nhận và $k$ là một số ngẫu nhiên dự định dùng làm khóa bảo mật. Alice (server) sẽ nhận $v$, dùng private key $d$ để giải ngược ra khóa $k_0, k_1$ rồi lấy từng tin nhắn $m_0, m_1$ cộng với khóa tương ứng rồi gửi lại cho Bob.

- **Lỗi triển khai:**
  Server vô tình ép cứng logic phía Bob lại và "tự biên tự diễn" bằng đoạn code:
  `v = (x0 + (int(k) ^ e)) % N`.
  Những sai lầm chí mạng ở dòng code này bao gồm:
  1. Luôn sử dụng `x0` thay vì tuỳ chọn `x0` hoặc `x1`. Điều này cản trở việc chọn tin nhắn hợp lệ thứ 2.
  2. Dùng phép XOR thao tác bit thay vì phép lũy thừa. Toàn bộ sức mạnh của modulo $N$ biến mất ở bước tạo $v$.
  
- **Khai thác:** 
  Server đang đóng vai trò Alice (tính toán Message 1, Message 2 rồi gửi về), nhưng lại hỏi người chơi nhập giá trị $k$. Sau khi có $k$, Server tự tính:
  $v = (x_0 + (k \oplus e)) \pmod N$
  
  Sau đó, theo chuẩn OT, Server tính các khóa "giải mã":
  $k_0 \equiv (v - x_0)^d \equiv (k \oplus e)^d \pmod N$
  $k_1 \equiv (v - x_1)^d \equiv (x_0 + (k \oplus e) - x_1)^d \pmod N$
  Và cuối cùng cộng 2 khóa này với tin nhắn gốc:
  $M_1 \equiv m_0 + k_0 \pmod N$
  $M_2 \equiv m_1 + k_1 \pmod N$
  
  Mục tiêu của chúng ta là triệt tiêu hoàn toàn khóa bảo vệ $k_1$ của $M_2$, tức là làm cho $k_1 = 0 \pmod N$. 
  Để $k_1 \equiv 0$, ta cần biểu thức bên trong mũ $d$ bằng $0$:
  $x_0 + (k \oplus e) - x_1 \equiv 0 \pmod N$
  $\Rightarrow k \oplus e \equiv (x_1 - x_0) \pmod N$
  Bởi vì phép XOR có tính chất đổi chỗ, ta dễ dàng tính được số $k$ cần gửi lên cho Server:
  $k = ((x_1 - x_0) \pmod N) \oplus e$
  
  Khi cung cấp đúng số $k$ này, khóa $k_1$ sẽ trả về $0$. Do đó, Message 2 nhận được từ server chính là thông điệp $m_1$ nguyên thủy chưa hề bị mã hóa!

### Lời giải

Script `solve.py` thực hiện các bước:

1. Kết nối với Netcat, thu thập các thông số RSA do server cấp, bao gồm $N, e, x_0, x_1$.
2. Tính toán magic number $k$: `k = ((x1 - x0) % N) ^ e`
3. Gửi $k$ lên máy chủ theo yêu cầu nhập liệu gốc.
4. Lấy giá trị của Message 2 do máy chủ trả về.
5. Chuyển đổi con số thu được thành chuỗi byte ASCII để thu được flag.

Trích đoạn code giải thuật toán (`solve.py`):

```python
# Để khóa k1 bằng 0 cần v - x1 = 0
# Mà v = x0 + (k ^ e) => x0 + (k ^ e) - x1 = 0 (mod N)
k = ((x1 - x0) % N) ^ e

r.sendline(str(k).encode())

# Đọc kết quả và chuyển thành byte
m2 = int(re.search(r'Message 2:\s+(\d+)', data_received).group(1))
print(long_to_bytes(m2).decode())
```

### Flag

`utflag{my_obl1v10u5_fr13nd_ru1n3d_my_c0de}`
