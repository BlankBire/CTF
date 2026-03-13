from Crypto.Cipher import AES
import itertools
import string

TARGET_HEX = "5aed095b21675ec4ceb770994289f72b"
PREFIX = "amateursCTF{"
SUFFIX = "}"
PLAIN_BLOCK = b"\x00" * 16

alphabet = string.ascii_letters + string.digits + "_{}!?$@#"  
for combo in itertools.product(alphabet, repeat=3):
    middle = "".join(combo)
    candidate = f"{PREFIX}{middle}{SUFFIX}"
    key_bytes = candidate.encode()
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    if cipher.encrypt(PLAIN_BLOCK).hex() == TARGET_HEX:
        print(candidate)
        break