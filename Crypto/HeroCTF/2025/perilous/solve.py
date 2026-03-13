from cryptography.hazmat.decrepit.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import Cipher

key_hex = "00112233445566778899AABBCCDDEEFF"      # khóa lúc hỏi flag
ct_hex = "eec7a3f72ac40a1f8bee600fbdb23cb3"      # ciphertext flag nhận được

cipher = Cipher(algorithms.ARC4(bytes.fromhex(key_hex)), mode=None)
flag = cipher.decryptor().update(bytes.fromhex(ct_hex))
print(flag)