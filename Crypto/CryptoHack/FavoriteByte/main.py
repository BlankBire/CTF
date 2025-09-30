from pwn import xor
keyString = "73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d"
data = bytes.fromhex(keyString)
for k in range(256):
    result = xor(data, k)
    try:
        decoded = result.decode('ascii')
        if all(32 <= ord(c) <= 126 for c in decoded):
            print(decoded)
    except UnicodeDecodeError:
        continue