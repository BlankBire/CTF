from pwn import xor
given = 'label'
res = b''
for c in given:
    char = xor(ord(c), 13)
    res += char
print(res)