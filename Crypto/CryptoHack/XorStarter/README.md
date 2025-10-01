# Challenge
XOR is a bitwise operator which returns 0 if the bits are the same, and 1 otherwise. In textbooks the XOR operator is denoted by ⊕, but in most challenges and programming languages you will see the caret ^ used instead.
![XOR](xor.png)
For longer binary numbers we XOR bit by bit: `0110 ^ 1010 = 1100`. We can XOR integers by first converting the integer from decimal to binary. We can XOR strings by first converting each character to the integer representing the Unicode character.
Given the string `label`, XOR each character with the integer `13`. Convert these integers back to a string and submit the flag as `crypto{new_string}`.

# Description
The XOR operator (`^`) compares bits pairwise and returns `1` when bits differ and `0` when they are the same. To XOR characters with an integer we convert each character to its byte/ordinal value, XOR that integer with 13, then convert back to a character.
We are given the plaintext string: `label`.

# Solution
Compute the XOR of each character's ASCII/ordinal value with `13` (decimal):
```
l : 01101100
a : 01100001
b : 01100010
e : 01100101
l : 01101100
13: 00001101

01101100 ^ 00001101 = 01100001 -> 'a'
01100001 ^ 00001101 = 01101100 -> 'l'
01100010 ^ 00001101 = 01101111 -> 'o'
01100101 ^ 00001101 = 01101000 -> 'h'
01101100 ^ 00001101 = 01100001 -> 'a'
```
# Flag
`crypto{aloha}`