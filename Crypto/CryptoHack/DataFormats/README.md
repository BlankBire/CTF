### DataFormats (CryptoHack) — Tổng hợp cách giải 3 bài

Ba bài `CERTainlyNot`, `PrivacyEnhancedMail` và `SshKeys` trong thư mục này đều xoay quanh việc đọc/parse các định dạng chứa khóa RSA khác nhau và trích xuất tham số quan trọng (như modulus n hoặc private exponent d). Dù file đầu vào khác định dạng, cách tiếp cận thực chất giống nhau: dùng PyCryptodome để `import_key` rồi đọc thuộc tính từ đối tượng khóa.

### Yêu cầu

- Python 3
- Thư viện PyCryptodome

```bash
pip install pycryptodome
```

### Cách làm chung

1. Đọc toàn bộ nội dung file khóa/chứng chỉ (ở dạng nhị phân là an toàn nhất).
2. Dùng `Crypto.PublicKey.RSA.import_key(data)` để parse dữ liệu.
3. Truy cập thuộc tính cần lấy:
   - `key.n`: modulus (dùng cho khóa công khai/lấy từ cert/SSH pubkey)
   - `key.e`: public exponent
   - `key.d`: private exponent (nếu là khóa riêng hoặc PEM có chứa private key)
4. In ra giá trị theo yêu cầu.

Lưu ý: Các định dạng khác nhau (DER, PEM, SSH public key) được PyCryptodome tự nhận diện trong `import_key`, nên không cần tự tay decode base64/ASN.1.

### Các bài cụ thể

- CERTainlyNot (DER X.509 certificate)

  - Đầu vào: file `.der` (chứng chỉ X.509 nhị phân) chứa public key RSA.
  - Mục tiêu: trích xuất `n` (modulus) của khóa RSA trong chứng chỉ.
  - Chạy:
    ```bash
    cd CERTainlyNot
    python main.py
    ```
  - Kết quả: in ra số `n` (số nguyên lớn).

- PrivacyEnhancedMail (PEM)

  - Đầu vào: file `.pem` (Privacy-Enhanced Mail). Có thể chứa public hoặc private key; ở bài này là private key nên có `d`.
  - Mục tiêu: trích xuất `d` (private exponent) từ khóa RSA.
  - Chạy:
    ```bash
    cd PrivacyEnhancedMail
    python main.py
    ```
  - Kết quả: in ra `d`.

- SshKeys (OpenSSH public key)
  - Đầu vào: file `.pub` (OpenSSH public key) chứa khóa công khai RSA ở dạng SSH.
  - Mục tiêu: trích xuất `n` (modulus) của khóa công khai.
  - Chạy:
    ```bash
    cd SshKeys
    python main.py
    ```
  - Kết quả: in ra số `n`.

### Gợi ý kiểm tra/chuyển đổi (nếu cần)

- DER ↔ PEM: có thể dùng `openssl x509 -in cert.der -inform DER -out cert.pem -outform PEM` để tham khảo cấu trúc, nhưng không bắt buộc vì `import_key` đọc trực tiếp được.
- Với SSH public key, `import_key` xử lý được chuỗi `ssh-rsa ...` mà không cần chuyển đổi thủ công.

### Tóm tắt

- Dù định dạng khác nhau, điểm chung là: đọc file → `RSA.import_key(data)` → lấy thuộc tính (`n`, `e`, `d`) → in kết quả theo đề.
