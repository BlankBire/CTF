
import socket
import random
import re

HOST = 'challenge.cnsc.com.vn'
PORT = 31454
SEED = "Wanna Win?"
N = 128

def encrypt(A, x):
    b = [0] * N
    for i in range(N):
        for j in range(N):
            val = A[i][j] + x[j]
            if val > b[i]:
                b[i] = val
    return b

def solve():
    random.seed(SEED)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    
    f = s.makefile('rw', buffering=1)
    
    try:
        for r in range(64):
            line = f.readline()
            while "Round" not in line:
                if not line: break
                line = f.readline()
            print(f"Server: {line.strip()}")
            A = [random.randbytes(N) for _ in range(N)]
            b_line = f.readline().strip()
            if "b =" not in b_line:
                print(f"Unexpected line: {b_line}")
                return
            
            # Extract the list part
            b_str = b_line.split("=", 1)[1].strip()
            b = eval(b_str) # Safe here as we control context and input is numeric list
            
            # Solve for x
            # x_j = min_i (b_i - A_ij)
            x_candidate = []
            for j in range(N):
                min_diff = float('inf')
                for i in range(N):
                    # A[i] is bytes, so A[i][j] is an int
                    diff = b[i] - A[i][j]
                    if diff < min_diff:
                        min_diff = diff
                
                # Constrain to byte range [0, 255]
                # If equation allows > 255, we clamp to 255 because inputs must be bytes
                if min_diff > 255:
                    min_diff = 255
                if min_diff < 0:
                    min_diff = 0
                x_candidate.append(int(min_diff))
            
            # Send solution
            sol_bytes = bytes(x_candidate)
            sol_hex = sol_bytes.hex()
            f.write(sol_hex + "\n")
            f.flush()
            print(f"Sent solution for round {r+1}")
            
        # After 64 rounds
        final_response = f.read()
        print("Final Output:")
        print(final_response)
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        s.close()

if __name__ == "__main__":
    solve()