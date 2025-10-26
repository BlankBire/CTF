## Structure of AES - Writeup (CryptoHack)

### Mô tả tổng quan

Một ma trận 4x4 được cung cấp. Làm phẳng nó trở lại thành một mảng 16 bytes.

### Ý tưởng

- Tạo một bytearray rỗng.
- Duyệt qua từng phần tử của ma trận và thêm vào bytearray.

### Cách giải

```python
def matrix2bytes(matrix):
    output = bytearray()
    for row in matrix:
        for item in row:
            output.append(item)
    return bytes(output)
```

### Flag

`crypto{inmatrix}`
