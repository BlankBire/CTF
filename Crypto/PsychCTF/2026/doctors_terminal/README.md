## Doctor Terminal - Writeup (Psych CTF 2026)

### Mô tả

- Một thử thách yêu cầu giải mã chuỗi ciphertext bằng cách đảo ngược các bước mã hóa mà không cần lập trình, có thể giải quyết hoàn toàn bằng công cụ.
- Người chơi được cung cấp một file ảnh chứa gợi ý về công cụ CyberChef, một file chứa chuỗi ciphertext và một báo cáo y tế.
- Mục tiêu là xác định các lớp mã hóa đã được sử dụng và tìm ra khóa XOR từ báo cáo y tế để giải mã lấy flag.

### Tệp đính kèm

- `dr_mehtas_terminal.png`
- `encrypted_intake_records.txt`
- `patient_incident_report.md`

### Phân tích

- **Phân tích chuỗi ban đầu:**
  Khi xem nội dung file `encrypted_intake_records.txt`, chuỗi mã hóa thoạt nhìn rất giống định dạng Base64. Tuy nhiên, nếu trực tiếp dùng thao tác `From Base64` trong CyberChef, kết quả trả về chỉ là những ký tự vô nghĩa. Dựa vào hình ảnh từ `dr_mehtas_terminal.png`, ta đoán được tiến trình này trải qua nhiều lớp mã hóa được xếp chồng lên nhau.

- **Bóc tách các lớp mã hóa tĩnh:**
  Ta tiến hành thử nghiệm các lớp giải mã cơ bản. Thêm `ROT13` (Amount: 13), sau đó mới dùng `From Base64`. Kết quả xuất ra là một chuỗi Hex. Tiếp tục thêm thao tác `From Hex`, ta nhận được một chuỗi ký tự lạ lẫm, bắt đầu bằng: `'2+'?:6t45b6...`. Chú ý đến 6 byte Hex đầu tiên của chuỗi này: `27 32 2b 27 3f 3a`.

- **Tìm khóa XOR bằng Known-Plaintext Attack (KPA):**
  Dựa vào format flag của giải đấu, ta biết chắc chắn 6 ký tự đầu của plaintext là `psych{`. Chuyển chuỗi `psych{` sang Hex, ta được: `70 73 79 63 68 7b`. Dựa vào tính chất của phép toán XOR: `Key = Ciphertext ^ Plaintext`. Ta thử lấy bản mã XOR với bản rõ để tìm ra Key:
  
  - `0x27 ^ 0x70 ('p') = W`
  - `0x32 ^ 0x73 ('s') = A`
  - `0x2b ^ 0x79 ('y') = R`
  - `0x27 ^ 0x63 ('c') = D`
  - `0x3f ^ 0x68 ('h') = W`
  - `0x3a ^ 0x7b ('{') = A`
  
  Kết quả trả về chuỗi `WARDWA...` lặp đi lặp lại. Nghĩa là khóa XOR chính là chữ `WARD`! Nhớ lại đoạn mở đầu trong file `patient_incident_report.md` có ghi: *"Incident Report, Ward C"*. Rõ ràng bác sĩ đã lấy hồ sơ bệnh án rồi XOR với mã phân khu của bệnh viện (Ward).

### Lời giải

Sử dụng công cụ CyberChef, thiết lập Recipe với đúng 4 thao tác để đảo ngược hoàn toàn quá trình mã hóa của bác sĩ:

1. `ROT13` (Amount: 13)
2. `From Base64`
3. `From Hex`
4. `XOR` với:
   - Key: `WARD`
   - Scheme: `UTF8` (hoặc Standard)

Kết quả sẽ hiện ra flag nguyên vẹn.

### Flag

`psych{d0ct0r_kn0ws_y0ur_s3cr3ts}`
