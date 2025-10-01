# Challenge
ASCII is a 7-bit encoding standard which allows the representation of text using the integers 0-127.
Using the below integer array, convert the numbers to their corresponding ASCII characters to obtain a flag.
`[99, 114, 121, 112, 116, 111, 123, 65, 83, 67, 73, 73, 95, 112, 114, 49, 110, 116, 52, 98, 108, 51, 125]`
In Python, the `chr()` function can be used to convert an ASCII ordinal number to a character (the `ord()` function does the opposite).

# Description
We are given a list of integers. Each integer is an ASCII code for a character in the flag. We have to convert each number to its corresponding character with `chr()` and joins them to form the flag.

# Solution
Convert each integer in the array to its ASCII character using `chr()` and join them. Running the script will print the flag.
```
arr = [99, 114, 121, 112, 116, 111, 123, 65, 83, 67, 73, 73, 95, 112, 114, 49, 110, 116, 52, 98, 108, 51, 125]
print("".join(chr(i) for i in arr))
```

# Flag
`crypto{ASCII_pr1nt4bl3}`