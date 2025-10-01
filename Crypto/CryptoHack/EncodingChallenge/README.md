# Challenge
Now you've got the hang of the various encodings you'll be encountering, let's have a look at automating it.
Can you pass all 100 levels to get the flag?
The `13377.py` file attached below is the source code for what's running on the server. The `pwntools_example.py` file provides the start of a solution.
For more information about connecting to interactive challenges, see the FAQ. Feel free to skip ahead to the cryptography if you aren't in the mood for a coding challenge!
If you want to run and test the challenge locally, then check the FAQ to download the `utils.listener` module.
Connect at `socket.cryptohack.org 13377`
Challenge files:
  - 13377.py
  - pwntools_example.py

# Description
The server runs 100 levels. On each level it sends a JSON object describing the encoding type and the encoded value. Your client must return a JSON object containing the decoded plaintext in the `decoded` field. When you have answered 100 levels correctly the server returns the flag.
Possible encodings (from `13377.py`):
- `base64` - value is a Base64-encoded string (standard `base64.b64encode`/`b64decode`).
- `hex` - value is a hex string produced by `.encode().hex()` (decode with `bytes.fromhex()`).
- `rot13` - value is a ROT13 transformation of the plaintext (use `codecs.encode(..., 'rot_13')` / decode with same).
- `bigint` - value is a Python-style hex string representing the integer form of the message (the server uses `hex(bytes_to_long(msg))`). Example look: `"0x48656c6c6f5f776f726c64"`. To decode: strip the `0x`, convert hex → bytes → text.
- `utf-8` - value is a list of ordinal numbers for each character.
Server behaviour (summary from `13377.py`):
- On connect, server sends a JSON with `{"type": <encoding>, "encoded": <value>}`.
- We must reply with `{"decoded": "<original_text>"}` (the server also expects the type key in the example starter code; including it is fine).
- If correct, server sends the next level. After 100 correct answers the server replies with `{"flag": FLAG}`.
`pwntools_example.py` contains a skeleton that connects and receives JSON lines from the server and sends JSON replies. The script already handles connection and I/O; we have to decode the received value and send back the plaintext.
Minimal structure in the starter:
```
from pwn import *
import json
# ...
r = remote('socket.cryptohack.org', 13377, level='debug')

for i in range(101):
    def json_recv():
        line = r.recvline()
        return json.loads(line.decode())

    def json_send(hsh):
        request = json.dumps(hsh).encode()
        r.sendline(request)

    received = json_recv()
    # --- decode received["encoded"] based on received["type"] ---
    # json_send(to_send)
    json_recv()
```

# Requirement
`pip install pwntools pycryptodome`

# Solution
We need to detect received["type"] and decode accordingly, then send back the decoded string in JSON. Below is a working decoding block we can drop into the starter script:
```
import base64
import codecs

if received["type"] == "base64":
    decoded = base64.b64decode(received["encoded"]).decode()
elif received["type"] == "bigint":
    # received["encoded"] is like "0x..." — strip "0x", convert hex to bytes, decode
    decoded = bytes.fromhex(received["encoded"][2:]).decode()
elif received["type"] == "hex":
    decoded = bytes.fromhex(received["encoded"]).decode()
elif received["type"] == "rot13":
    decoded = codecs.decode(received["encoded"], "rot_13")
elif received["type"] == "utf-8":
    decoded = "".join(chr(c) for c in received["encoded"])

to_send = {
    "type": received["type"],
    "decoded": decoded
}
json_send(to_send)
```
Notes and tips:
- `base64.b64decode()` returns bytes; call `.decode()` to get a Python `str`.
- `bytes.fromhex()` converts hex string → bytes.
- For `bigint`, the server used `hex(bytes_to_long(msg))`, so we will receive a hex string prefixed with `0x`.
- The `utf-8` case is a list of integers - convert with `chr()`.
Run `pwntools_example.py`.

# Flag
`crypto{3nc0d3_d3c0d3_3nc0d3}`