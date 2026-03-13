from __future__ import annotations

from typing import List, Tuple

LEAK_PATH = "keystream_leak.txt"
CIPHER_PATH = "cipher.txt"


def load_states() -> List[int]:
    states: List[int] = []
    with open(LEAK_PATH, "r", encoding="ascii") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            states.append(int(line))
    return states


def gaussian_solve(coeffs: List[int], rhs: List[int], num_vars: int) -> int:
    rows = coeffs[:]
    res = rhs[:]
    pivot_row_for_col = [-1] * num_vars
    row = 0
    total_rows = len(rows)

    for col in range(num_vars):
        pivot = None
        for r in range(row, total_rows):
            if (rows[r] >> col) & 1:
                pivot = r
                break
        if pivot is None:
            continue
        rows[row], rows[pivot] = rows[pivot], rows[row]
        res[row], res[pivot] = res[pivot], res[row]
        pivot_row_for_col[col] = row
        for r in range(total_rows):
            if r != row and ((rows[r] >> col) & 1):
                rows[r] ^= rows[row]
                res[r] ^= res[row]
        row += 1
        if row == total_rows:
            break

    solution = 0
    for col in range(num_vars - 1, -1, -1):
        pivot_row = pivot_row_for_col[col]
        if pivot_row == -1:
            continue
        value = res[pivot_row]
        row_bits = rows[pivot_row] & ~(1 << col)
        temp = row_bits
        while temp:
            lsb = temp & -temp
            bit_index = (lsb.bit_length() - 1)
            if (solution >> bit_index) & 1:
                value ^= 1
            temp ^= lsb
        if value & 1:
            solution |= (1 << col)
    return solution


def reconstruct_matrix(states: List[int]) -> Tuple[List[int], int]:
    prev_states = states[:-1]
    next_states = states[1:]
    coeff_rows = [s | (1 << 32) for s in prev_states]
    A_rows: List[int] = []
    b_bits: List[int] = []

    for bit in range(32):
        rhs = [ (nxt >> bit) & 1 for nxt in next_states ]
        row_solution = gaussian_solve(coeff_rows, rhs, 33)
        A_rows.append(row_solution & 0xFFFFFFFF)
        b_bits.append((row_solution >> 32) & 1)

    B = sum(bit << idx for idx, bit in enumerate(b_bits))
    return A_rows, B


def parity(x: int) -> int:
    return x.bit_count() & 1


def step(state: int, A_rows: List[int], B: int) -> int:
    result = 0
    for bit, row in enumerate(A_rows):
        bit_value = parity(row & state) ^ ((B >> bit) & 1)
        result |= bit_value << bit
    return result


def verify(states: List[int], A_rows: List[int], B: int) -> None:
    current = states[0]
    for idx, expected in enumerate(states[1:], start=1):
        current = step(current, A_rows, B)
        if current != expected:
            raise ValueError(f"Mismatch at index {idx}: expected {expected}, got {current}")


def decrypt(cipher_bytes: bytes, start_state: int, A_rows: List[int], B: int) -> bytes:
    state = start_state
    keystream = bytearray()
    plaintext = bytearray()

    for idx, c in enumerate(cipher_bytes):
        keystream_byte = state & 0xFF
        keystream.append(keystream_byte)
        plaintext.append(c ^ keystream_byte)
        state = step(state, A_rows, B)
    return bytes(plaintext)


if __name__ == "__main__":
    leak_states = load_states()
    if len(leak_states) < 2:
        raise SystemExit("Need at least two leaked states")

    A_rows, B = reconstruct_matrix(leak_states)
    verify(leak_states, A_rows, B)

    with open(CIPHER_PATH, "rb") as f:
        cipher_data = f.read()

    plain = decrypt(cipher_data, leak_states[0], A_rows, B)

    print("Plaintext:", plain)