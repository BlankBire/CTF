from Crypto.Util.number import *
from hashlib import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import *
part_1 = "s0me_r4nd0m_str1ng".encode()

class LCG():
    
    def __init__(self, seed, a, c, m):
        self.seed = seed
        self.a = a
        self.c = c
        self.m = m
        self.state = seed
        
    def next(self):
        
        self.seed = (self.a * self.seed ** 65537 + self.c) % m
        return self.seed >> 20
    
a = getPrime(50)
c = getPrime(50)
m = getPrime(100)
seed = getRandomInteger(50)

lcg = LCG(seed, a, c, m)

key = sha256(long_to_bytes(seed)).digest()
enc = AES.new(key, AES.MODE_ECB).encrypt(pad(part_1, 16))


print(f"{enc = }")
print(f"{a = }")
print(f"{c = }")
print(f"{m = }")
print(f"{lcg.next() = }")
'''
enc = b'\xe6\x97\x9f\xb9\xc9>\xde\x1e\x85\xbb\xebQ"Ii\xda\'\x1f\xae\x19\x05M\x01\xe1kzS\x8fi\xf4\x8cz'
a = 958181900694223
c = 1044984108221161
m = 675709840048419795804542182249
lcg.next() = 176787694147066159797379
'''