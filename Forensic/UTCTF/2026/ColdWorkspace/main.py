import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

encd_b64 = "S4wX8ml7/f9C2ffc8vENqtWw8Bko1RAhCwLLG4vvjeT2iJ26nfeMzWEyx/HlK1KmOhIrSMoWtmgu2OKMtTtUXddZDQ87FTEXIqghzCL6ErnC1+GwpSfzCDr9woKXj5IzcU2C/Ft5u705bY3b6/Z/Q/N6MPLXV55pLzIDnO1nvtja123WWwH54O4mnyWNspt5"
enck_b64 = "Ddf4BCsshqFHJxXPr5X6MLPOGtITAmXK3drAqeZoFBU="
encv_b64 = "xXpGwuoqihg/QHFTM2yMxA=="

ciphertext = base64.b64decode(encd_b64)
key = base64.b64decode(enck_b64)
iv = base64.b64decode(encv_b64)

cipher = AES.new(key, AES.MODE_CBC, iv)

try:
    # Giải mã và loại bỏ padding
    decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
    print("Decrypted Text:", decrypted_data.decode('utf-8', errors='ignore'))
    with open("recovered_flag.bin", "wb") as f:
        f.write(decrypted_data)
except Exception as e:
    print("Error:", e)
