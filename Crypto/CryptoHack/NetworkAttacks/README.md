# Challenge
Several of the challenges are dynamic and require you to talk to our challenge servers over the network. This allows you to perform man-in-the-middle attacks on people trying to communicate, or directly attack a vulnerable service. To keep things consistent, our interactive servers always send and receive JSON objects.
Such network communication can be made easy in Python with the `pwntools` module. This is not part of the Python standard library, so needs to be installed with pip using the command line `pip install pwntools`.
For this challenge, connect to `socket.cryptohack.org` on port `11112`. Send a JSON object with the key `buy` and value `flag`.
The example script below contains the beginnings of a solution for you to modify, and you can reuse it for later challenges.
Connect at `socket.cryptohack.org 11112`
Challenge files:
  - pwntools_example.py

# Description
The script connects to `socket.cryptohack.org` on port `11112` and communicates with the service using JSON. The server expects a JSON object with a `buy` field describing what the client wants to purchase. If the client asks for something the shop doesn't sell, the server returns an error; if the client asks for the special item `flag`, the server responds with the flag.
Provided original script:
```
request = {
    "buy": "clothes"
}
json_send(request)

response = json_recv()
print(response)
```
If you send `"buy": "clothes"` you receive:
```
{'error': 'Sorry! All we have to sell are flags.'}
```

# Requirement
- `pip install pwntools`

# Solution
The server only sells flags. Modify the `buy` value to `"flag"` (or send a JSON object with `{"buy": "flag"}`) and run the script. The script will print the returned JSON which contains the flag.

Change the request in the script to:
```
request = {
    "buy": "flag"
}
json_send(request)

response = json_recv()
print(response)
```

# Flag
`crypto{sh0pp1ng_f0r_fl4g5}`