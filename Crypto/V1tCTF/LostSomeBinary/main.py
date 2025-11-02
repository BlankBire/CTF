with open("Lost_Some_Binary.txt", "r") as f:
    data = f.read().strip()
binary_list = data.split()
lsb_bits = ''.join(b[-1] for b in binary_list)
print("LSB bits:", lsb_bits)
lsb_message = ''
for i in range(0, len(lsb_bits), 8):
    if i+8 <= len(lsb_bits):
        byte = lsb_bits[i:i+8]
        lsb_message += chr(int(byte, 2))
print("LSB message:", lsb_message)