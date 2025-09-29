from pwn import * # pip install pwntools
import json
from Crypto.Util.number import *
import codecs
import base64

r = remote('socket.cryptohack.org', 13377, level = 'debug')
for i in range(101):
    def json_recv():
        line = r.recvline()
        return json.loads(line.decode())

    def json_send(hsh):
        request = json.dumps(hsh).encode()
        r.sendline(request)


    received = json_recv()

    print("Received type: ")
    print(received["type"])
    print("Received encoded value: ")
    print(received["encoded"])

    ######################################################
    if received["type"] == "base64":
        decoded = base64.b64decode(received["encoded"]).decode()
        print(decoded)
    elif received["type"] == "bigint":
        decoded = bytes.fromhex(received["encoded"][2:]).decode()
        print(decoded)
    elif received["type"] == "hex":
        decoded = bytes.fromhex(received["encoded"]).decode()
        print(decoded)
    elif received["type"] == "rot13":
        decoded = codecs.decode(received["encoded"], "rot_13")
        print(decoded)
    elif received["type"] == "utf-8":
        decoded = "" 
        for c in received["encoded"]:
            decoded += chr(c)
        print(decoded)
    #######################################################

    to_send = {
        "type": received["type"],
        "decoded": decoded
    }

    json_send(to_send)

    # json_recv()
