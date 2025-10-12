from pwn import xor

# The flag format: crypto{ -> format_bytes = b"crypto{"
# XOR the encrypted_bytes with the format_bytes -> b'myXORke+y_Q\x0bHOMe$~seG8bGURN\x04DFWg)a|\x1dTM!an\x7f'
# XOR the encrypted_bytes with the format_bytes = "myXORkey" -> real flag

encrypted_bytes = bytes.fromhex("0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104")
format_bytes = b"myXORkey"
flag = xor(encrypted_bytes, format_bytes)
print(flag)