# Challenge
Modern cryptography involves code, and code involves coding. CryptoHack provides a good opportunity to sharpen your skills.
Of all modern programming languages, Python 3 stands out as ideal for quickly writing cryptographic scripts and attacks. For more information about why we think Python is so great for this, please see the FAQ.
Run the attached Python script and it will output your flag.
Challenge files:
  - great_snakes.py
Resources:
  - Downloading Python

# Description
We are given a list of integers that represent an encoded flag.  
The encoding method is simple: each character of the original flag was XOR-ed with `0x32`.  
Our task is to recover the flag.

# Solution
We decode the flag by XOR-ing each number with `0x32`.
```
ords = [81, 64, 75, 66, 70, 93, 73, 72, 1, 92, 109, 2, 84, 109, 66, 75, 70, 90, 2, 92, 79]
print("Here is your flag:")
print("".join(chr(o ^ 0x32) for o in ords))
```

# Flag
`crypto{z3n_0f_pyth0n}`