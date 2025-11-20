from sympy import factorint
from sympy import mod_inverse
from Cryptodome.Util.number import long_to_bytes
n = 31698460634924412577399959706905435239651
p = 101
q = 313846144900241708687128313929756784551
e = 65537
c = 23648999580642514140599125257944114844209
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)
m = pow(c, d, n)

for k in range(5):
    candidate = long_to_bytes(m + k * n)
    print(candidate)