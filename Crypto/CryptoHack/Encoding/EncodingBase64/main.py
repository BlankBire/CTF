import base64
encoderHexText = "72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf"
decoderHexText = bytes.fromhex(encoderHexText)
b64 = base64.b64encode(decoderHexText)
print(b64)

# base64.b64encode(): bytes to base64
# base64.b64decode(): base64 to bytes