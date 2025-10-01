# Challenge
For the next few challenges, you'll use what you've just learned to solve some more XOR puzzles.
I've hidden some data using XOR with a single byte, but that byte is a secret. Don't forget to decode from hex first.
`73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d`

# Description
We are given the hex string.
This string has been encoded by XORing each byte with a secret byte value (0-255). Decode to obtain the original text (flag).

# Requirement
`pip install pwntools`

# Solution
A short Python approach: Brute-force each key and check for printable ASCII output.
When we run the brute-force, one key produces a clearly readable plaintext that matches the `crypto{...}` pattern.
- Decode the hex string to raw bytes (`bytes.fromhex(...)`).
- For each possible single-byte key `k` from `0` to `255`, XOR every byte of the data with `k`.
- Attempt to interpret the result as ASCII text and filter for printable output.
- The result that looks like a normal readable string (and fits the `crypto{...}` format) is the flag.

# Flag
`crypto{0x10_15_my_f4v0ur173_by7e}`