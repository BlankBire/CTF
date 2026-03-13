import sympy as sp
from itertools import combinations

hex_shares = [
"ef73fe834623128e6f43cc923927b33350314b0d08eeb386", 
"2c17367ded0cd22e15220a2b2a6cede16e2ed64d1898bbad", 
"e05fd9646ff27414510dec2e46032469cd60d632606c8181", 
"0c4de736ced3f8412307729b8bea56cc6dc74abce06a0373", 
"afe15ff509b15eb48b0e9d72fc2285094f6233ec98914312", 
"cb1a439f208aa76e89236cb496abaf20723191c188e23f54"  
]
shares = [int(h,16) for h in hex_shares]
p = sp.nextprime(max(shares))

def lagrange_at_zero(xs, ys, p):
    out = 0
    k = len(xs)
    for i in range(k):
        xi, yi = xs[i], ys[i]
        num = 1
        den = 1
        for j in range(k):
            if j==i: continue
            xj = xs[j]
            num = (num * (-xj)) % p
            den = (den * (xi - xj)) % p
        out = (out + yi * num * pow(den, -1, p)) % p
    return out

for r in range(3,7):
    for combo in combinations(range(len(shares)), r):
        xs = [i+1 for i in combo]
        ys = [shares[i] for i in combo]
        secret_int = lagrange_at_zero(xs, ys, p)
        hexs = hex(secret_int)[2:].rjust(48,'0')  # đảm bảo 24 bytes
        secret = bytes.fromhex(hexs)
        frac = sum(1 for b in secret if 32 <= b <= 126) / len(secret)
        if frac > 0.6:
            print("combo", combo, "->", secret)
