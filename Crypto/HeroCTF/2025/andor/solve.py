#!/usr/bin/env python3
from telnetlib import Telnet
import binascii

HOST = "crypto.heroctf.fr"
PORT = 9000
ROUNDS = 300
STABLE = 8

def wait_for(prefix, tn):
    while True:
        line = tn.read_until(b"\n").strip()
        if line.startswith(prefix):
            return line.split(b"=",1)[1].strip()

with Telnet(HOST, PORT) as tn:
    front = None
    back  = None
    stable = 0

    for _ in range(ROUNDS):
        a_hex = wait_for(b"a =", tn)
        o_hex = wait_for(b"o =", tn)
        tn.read_until(b"> ")

        a = binascii.unhexlify(a_hex)
        o = binascii.unhexlify(o_hex)

        if front is None:
            front = bytearray(len(a))
            back  = bytearray(b"\xFF"*len(o))

        changed = False

        # front = OR of all AND results
        for i in range(len(a)):
            v = front[i] | a[i]
            if v != front[i]:
                front[i] = v
                changed = True

        # back = AND of all OR results
        for i in range(len(o)):
            v = back[i] & o[i]
            if v != back[i]:
                back[i] = v
                changed = True

        tn.write(b"0\n")

        if not changed:
            stable += 1
            if stable >= STABLE:
                break
        else:
            stable = 0

flag = bytes(front + back)
print(flag)