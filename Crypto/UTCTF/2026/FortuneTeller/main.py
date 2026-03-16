x1 = 4176616824
x2 = 2681459949
x3 = 1541137174
x4 = 3272915523

m = 4294967296
ciphertext_hex = "3cff226828ec3f743bb820352aff1b7021b81b623cff31767ad428672ef6"
ciphertext = bytes.fromhex(ciphertext_hex)

a = (x2 - x3) * pow((x1 - x2), -1, m) % m
c = (x2 - a * x1) % m

x5 = (a * x4 + c) % m
x5_bytes = x5.to_bytes(4, 'big')

flag = bytes(ciphertext[i] ^ x5_bytes[i % 4] for i in range(len(ciphertext)))
print(flag.decode())