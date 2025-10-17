from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto import Random
with open("key.pem", "rb") as f:
    key = RSA.import_key(f.read())
with open("cipher", "rb") as f:
    ciphertext = f.read()
cipher_rsa = PKCS1_v1_5.new(key)
sentinel = Random.new().read(16)
plaintext = cipher_rsa.decrypt(ciphertext, sentinel)
print(plaintext.decode(errors="ignore"))