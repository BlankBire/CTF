o = (
    (6, 0, 7),
    (8, 2, 1),
    (5, 4, 3),
)

# Build inverse lookup to map each base-9 digit back to the original (high, low) base-3 digits.
inverse = {}
for high, row in enumerate(o):
    for low, value in enumerate(row):
        inverse[value] = (high, low)

with open("encrypted", "rb") as f:
    data = f.read()

ss = int.from_bytes(data, byteorder="big")

if ss == 0:
    raise ValueError("Encrypted payload cannot be zero.")

# Recover the base-9 digit sequence produced during encryption.
digits_base9 = []
temp = ss
while temp:
    digits_base9.append(temp % 9)
    temp //= 9

digits_base9.reverse()

pairs = [inverse[d] for d in digits_base9]

total_digits = len(pairs) * 2
base3_digits = [0] * total_digits

for idx, (high, low) in enumerate(pairs):
    base3_digits[idx] = low
    base3_digits[total_digits - 1 - idx] = high

original = 0
for digit in reversed(base3_digits):
    original = original * 3 + digit

byte_length = (original.bit_length() + 7) // 8 or 1
flag_bytes = original.to_bytes(byte_length, byteorder="big")

print(flag_bytes)