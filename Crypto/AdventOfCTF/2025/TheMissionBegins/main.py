import base64
with open("start.txt", "r") as f:
    data = f.read()
data_ascii = ''.join(chr(int(b, 2)) for b in data.split())
print(data_ascii)
data_hex = bytes.fromhex(data_ascii)
print(data_hex)
flag = base64.b64decode(data_hex).decode()
print(flag)