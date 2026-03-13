
def main():
    flag = bytearray(b"th4t_y0u_h4ve_t0_f1nd")
    length = len(flag)

    for i in range(length):
        if i > 0:
            flag[i] ^= flag[i-1]

        v = flag[i] & 0xFF
        v ^= (v >> 4)
        v &= 0xFF
        v ^= (v >> 3)
        v &= 0xFF
        v ^= (v >> 2)
        v &= 0xFF
        v ^= (v >> 1)
        v &= 0xFF

        flag[i] = v
        print(f"{v:02x}", end="")

if __name__ == "__main__":
    main()

'''
6768107b1a357132741539783d6a661b5f3b
'''