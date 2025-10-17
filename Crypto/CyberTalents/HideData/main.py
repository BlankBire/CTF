import codecs
with open("cipher.txt", "rb") as f:
    cipher = f.read()
plain = codecs.decode(cipher.decode(), "rot_13")
print(plain)