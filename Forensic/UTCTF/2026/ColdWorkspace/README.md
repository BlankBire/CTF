## Cold Workspace - Writeup (UTCTF)

### Mô tả

- Một thử thách yêu cầu khôi phục artifact file đã bị xóa khỏi hệ thống thông qua memory snapshot.

### Tệp đính kèm

- `cold-workspace.dmp`

### Phân tích

- **Tìm kiếm artifact khởi đầu:**
  Đầu tiên, chạy lệnh `strings` kết hợp với `grep` để tìm kiếm từ khóa "flag" trong memory dump. Ta tìm thấy dấu vết của một PowerShell script thực hiện việc mã hóa và xóa file:

  ```bash
  PS C:\Challenge> strings cold-workspace.dmp | grep "flag"
  cmdline(4608): powershell.exe -ExecutionPolicy Bypass -File C:\Users\analyst\Desktop\encrypt_flag.ps1
  %$bytes = [System.IO.File]::ReadAllBytes('C:\Users\analyst\Desktop\flag.jpg')
  Remove-Item C:\Users\analyst\Desktop\flag.jpg
  Set-Content C:\Users\analyst\Desktop\flag.enc $env:ENCD
  MFT: C:\Users\analyst\Desktop\flag.enc
  ```
  Script trên đọc mảng bytes từ file ảnh gốc `flag.jpg`, ghi đè ciphertext vào `flag.enc` thông qua biến môi trường `$env:ENCD` rồi tiến hành xóa file `flag.jpg` đi.

- **Mở rộng phạm vi tìm kiếm:**
  Biết được ciphertext nằm trong biến `ENCD`, ta tiếp tục `grep` để tìm giá trị của nó ở dạng UTF-16 little-endian (phổ biến với Windows command line):

  ```bash
  PS C:\Challenge> strings -el cold-workspace.dmp | grep -i "ENCD="
  ```
  Không tìm thấy kết quả. Do đó, ta quay lại tìm kiếm ASCII string và mở rộng phạm vi hiển thị quanh từ khoá `ENCD` (trước và sau 5 dòng):

  ```bash
  PS C:\Challenge> strings cold-workspace.dmp | grep -A 5 -B 5 "ENCD"
  %B*YN!
  %$bytes = [System.IO.File]::ReadAllBytes('C:\Users\analyst\Desktop\flag.jpg')
  $key = [byte[]](0..31)
  $iv = [byte[]](0..15)
  # actual key/iv allocated at runtime, serialized to env vars
  $env:ENCD = '<ciphertext b64>'
  $env:ENCK = '<key b64>'
  $env:ENCV = '<iv b64>'
  Remove-Item C:\Users\analyst\Desktop\flag.jpg
  Set-Content C:\Users\analyst\Desktop\flag.enc $env:ENCD
  ```
  Đoạn kết quả này cho thấy toàn bộ nội dung của script `encrypt_flag.ps1`. Các giá trị thực tế của Ciphertext (`ENCD`), Key (`ENCK`) và IV (`ENCV`) đang được truyền qua biến môi trường khi runtime. Script được chạy bởi tiến trình `powershell.exe` với PID là `4608` (đã lộ ở kết quả đầu tiên).

- **Trích xuất các biến môi trường:**
  Sử dụng plugin `windows.envars` của Volatility (hoặc tiếp tục grep vùng nhớ chứa ENV block) để xuất toàn bộ biến môi trường của tiến trình `powershell.exe` (PID 4608). Ta khôi phục được 3 chuỗi Base64 thực tế:

  ```text
  PID    Process         Variable   Value
  4608   powershell.exe  ENCD       S4wX8ml7/f9C2ffc8vENqtWw8Bko1RAhCwLLG4vvjeT2iJ26nfeMzWEyx/HlK1KmOhIrSMoWtmgu2OKMtTtUXddZDQ87FTEXIqghzCL6ErnC1+GwpSfzCDr9...<truncated>
  4608   powershell.exe  TEMP       C:\Users\analyst\AppData\Local\Temp
  ]CB=
  &<F?
  rVs1
  eCn 6
  --
  g jX#L
  %_)8K
  ol[A
  -@vHI
  c[P%
  4ENV_BLOCK_START::PID=4608::powershell.exe::ENCD=S4wX8ml7/f9C2ffc8vENqtWw8Bko1RAhCwLLG4vvjeT2iJ26nfeMzWEyx/HlK1KmOhIrSMoWtmgu2OKMtTtUXddZDQ87FTEXIqghzCL6ErnC1+GwpSfzCDr9woKXj5IzcU2C/Ft5u705bY3b6/Z/Q/N6MPLXV55pLzIDnO1nvtja123WWwH54O4mnyWNspt5
  ENCK=Ddf4BCsshqFHJxXPr5X6MLPOGtITAmXK3drAqeZoFBU=
  ENCV=xXpGwuoqihg/QHFTM2yMxA==
  SESSION=Console
  USERDOMAIN=WORKGROUP
  ENV_BLOCK_END
  ```

### Lời giải

Script `main.py` thực hiện các bước sau để giải mã:

1. Decode Base64 lấy lại Ciphertext (`ENCD`), Key (`ENCK`) và IV (`ENCV`).
2. Khởi tạo thuật toán mã hóa AES với mode CBC.
3. Giải mã, xóa padding và in ra màn hình nội dung chuỗi cất giấu flag.

```python
ciphertext = base64.b64decode(encd_b64)
key = base64.b64decode(enck_b64)
iv = base64.b64decode(encv_b64)

cipher = AES.new(key, AES.MODE_CBC, iv)

try:
    # Giải mã và loại bỏ padding
    decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
    print("Decrypted Text:", decrypted_data.decode('utf-8', errors='ignore'))
except Exception as e:
    print("Error:", e)
```

### Flag

`utflag{m3m0ry_r3t41ns_wh4t_d1sk_l053s}`
