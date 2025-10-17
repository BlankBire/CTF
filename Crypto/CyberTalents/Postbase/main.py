import base64
# fullcode = R[corrupted]BR3tCNDUzXzYxWDdZXzRSfQ==
code = "R3tCNDUzXzYxWDdZXzRSfQ==" # remove R[corrupted]B
decode = base64.b64decode(code)
print(decode)