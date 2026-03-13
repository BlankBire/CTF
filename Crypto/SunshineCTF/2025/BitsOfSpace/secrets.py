from pwn import *
data = open("voyager.bin", "rb").read()
# change iv from 0x13371337 to 0xdeadbabe
iv = bytearray(data[:16])
body = data[16:]
old = struct.pack("<I", 0x13371337)
new = struct.pack("<I", 0xdeadbabe)
for i in range(4):
    iv[i] ^= old[i] ^ new[i]
print(old, new)
p = remote("sunshinectf.games", 25401)
p.send(iv + body)
p.interactive()