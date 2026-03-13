## BabySharingan — Writeup (H7CTF)

### Mô tả
Bạn nhận được hai chuỗi hex và một vài gợi ý liên quan đến "Chakra" và các bản cuộn (scroll) của Làng Lá/ANBU. Nhiệm vụ là khôi phục nội dung thực và trích xuất chữ ký chakra để lấy flag.

Tệp kèm theo:
- `main.py`: mã in ra các chuỗi hex ở nhiều dạng.
- `Scroll.txt`: cùng nội dung ở dạng có nhãn.

Các trường dữ liệu (dạng hex):
- EncodedLeafScroll
- EncodedANBUReport
- DecodedLeafScroll (text)
- DecodedANBUReport (text)
- ChakraSignatureLeafScroll
- ChakraSignatureANBUReport

### Hints
- "Decoded ... (text)" vẫn còn ở dạng hex của ASCII, cần `bytes.fromhex(...).decode()` để ra chữ.
- "Chakra Signature" cũng là hex ASCII; khi giải sẽ lộ format flag dạng `H7tex{...}`.
- Hai phần "Chakra Signature" có vẻ là cùng một chữ ký, trong đó bản ANBU dài hơn chứa phần đuôi `...r3ts}H7tex`.

### Cách giải
1) Chạy `main.py` hoặc tự giải bằng Python:

```python
print(bytes.fromhex(DecodedLeafScroll).decode())
print(bytes.fromhex(DecodedANBUReport).decode())
print(bytes.fromhex(ChakraSignatureLeafScroll).decode())
print(bytes.fromhex(ChakraSignatureANBUReport).decode())
```

2) Kết quả mong đợi:
- Decoded Leaf Scroll: "KAKASHI COPIES EVERY JUTSU HE SEES."
- Decoded ANBU Report: "THE COPY NINJA STRIKES WITH SILENT PRECISION."
- Chakra Signature (Leaf): `H7tex{th3_sh4r1ng4n_r3v34ls_4ll_s3c`
- Chakra Signature (ANBU): `H7tex{th3_sh4r1ng4n_r3v34ls_4ll_s3cr3ts}H7tex`

### Flag
`H7tex{th3_sh4r1ng4n_r3v34ls_4ll_s3cr3ts}`