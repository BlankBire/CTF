# Challenge
Another common encoding scheme is Base64, which allows us to represent binary data as an ASCII string using an alphabet of 64 characters. One character of a Base64 string encodes 6 binary digits (bits), and so 4 characters of Base64 encode three 8-bit bytes.
Base64 is most commonly used online, so binary data such as images can be easily included into HTML or CSS files.
Take the below hex string, decode it into bytes and then encode it into Base64.
`72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf`
In Python, after importing the base64 module with `import base64`, you can use the `base64.b64encode()` function. Remember to decode the hex first as the challenge description states.

# Description
We are given a hex string. The task is two-step:
- Decode the hex string into raw bytes (every two hex characters → one byte).
- Encode those bytes into Base64.
We implemented this in your script using `bytes.fromhex()` to decode the hex and `base64.b64encode()` to produce Base64.

# Solution
Decode the hex string with `bytes.fromhex()` and then Base64-encode the result with `base64.b64encode()`.
```
encoderHexText = "72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf"
decoderHexText = bytes.fromhex(encoderHexText)
b64 = base64.b64encode(decoderHexText)
```
# Flag
`crypto/Base+64+Encoding+is+Web+Safe/`