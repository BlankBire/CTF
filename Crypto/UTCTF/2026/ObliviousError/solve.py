import re
import socket
import time
from Crypto.Util.number import long_to_bytes

s = socket.socket()
s.connect(("challenge.utctf.live", 8379))
s.settimeout(3.0)

# Nhận các thông số ban đầu
data = b""
try:
    while b"k." not in data:
        chunk = s.recv(4096)
        if not chunk: break
        data += chunk
except: pass

data_str = data.decode()
N = int(re.search(r'N = (\d+)', data_str).group(1))
e = int(re.search(r'e = (\d+)', data_str).group(1))
x0 = int(re.search(r'x0: (\d+)', data_str).group(1))
x1 = int(re.search(r'x1: (\d+)', data_str).group(1))

# Thiết lập k sao cho k1 = 0
# Hệ thức: (x0 + (k ^ e)) - x1 = 0 mod N
k = ((x1 - x0) % N) ^ e

# Gửi k
s.send(str(k).encode() + b"\n")
time.sleep(1)

# Đọc phần còn lại
data2 = b""
try:
    while b"Message 2:" not in data2:
        chunk = s.recv(4096)
        if not chunk: break
        data2 += chunk
except: pass

data2_str = data2.decode()

# Trích xuất và giải mã Message 2 (chứa flag)
match = re.search(r'Message 2:\s+(\d+)', data2_str)
if match:
    m2 = int(match.group(1))
    print(long_to_bytes(m2).decode())
else:
    print(data2_str)
s.close()