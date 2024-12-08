# Constants
ROUNDS = 8  # Number of rounds
ROOT = 0x1f5  # Generator of GF(2^8)
C_X = [0x02, 0x03, 0x01, 0x01]  # Polynomial coefficients for µ
INV_C_X = [0x0E, 0x09, 0x0D, 0x0B]  # Polynomial coefficients for µ⁻¹
ROUND_CONSTANTS = [1 << i for i in range(ROUNDS)]  # Round constants

sbox = [
    0xc6, 0x37, 0x87, 0x47, 0xdf, 0x46, 0x06, 0xac, 0xf3, 0xe0, 0x86, 0x42, 0x1f, 0x8d, 0x4a, 0x97,
    0x5c, 0xd8, 0x6c, 0x27, 0x5f, 0x65, 0x84, 0xff, 0x2a, 0xbd, 0xda, 0x0a, 0x39, 0xba, 0xd7, 0xfc,
    0x8b, 0x2f, 0xc9, 0x92, 0x93, 0x03, 0x8f, 0x3c, 0xb3, 0xaa, 0xae, 0xef, 0xe7, 0x7d, 0xe3, 0xa1,
    0xb0, 0x8c, 0xc2, 0xcc, 0x71, 0x99, 0xa0, 0x59, 0x80, 0xd1, 0xf8, 0xde, 0x4e, 0x82, 0xdb, 0xa7,
    0x60, 0xc8, 0x32, 0x51, 0x41, 0x16, 0x55, 0xfa, 0xd5, 0x43, 0x9d, 0xcb, 0x62, 0xce, 0x02, 0xb8,
    0xc5, 0xed, 0xf0, 0x2e, 0xf2, 0x3f, 0xeb, 0x45, 0x56, 0x4c, 0x1b, 0x63, 0x54, 0x34, 0x75, 0x0c,
    0xfd, 0x0e, 0x5a, 0x4f, 0xc4, 0x24, 0xc3, 0xa8, 0xa4, 0x6f, 0xd0, 0x07, 0xf5, 0x33, 0x09, 0x7a,
    0xe5, 0xca, 0xf4, 0x08, 0xd9, 0x29, 0x73, 0xaf, 0x3b, 0x9b, 0x5d, 0xe2, 0xf1, 0x0f, 0xcf, 0xdd,
    0x2c, 0x30, 0xc1, 0x3e, 0x05, 0x89, 0xb4, 0x81, 0xbc, 0x8a, 0x17, 0x23, 0xb6, 0x25, 0x61, 0xc7,
    0xf6, 0xe8, 0x04, 0x3d, 0xd2, 0x52, 0xf9, 0x78, 0x94, 0x1e, 0x7b, 0xb1, 0x1d, 0x15, 0x40, 0x4d,
    0xfe, 0xd3, 0x53, 0x50, 0x64, 0x90, 0xb2, 0x35, 0xdc, 0xcd, 0x3a, 0xd6, 0xe9, 0xa9, 0xbe, 0x67,
    0x8e, 0x7c, 0x83, 0x26, 0x28, 0xad, 0x14, 0x6a, 0x36, 0x95, 0xbf, 0x5e, 0xa6, 0x57, 0x1a, 0x70,
    0x5b, 0x77, 0xa2, 0x12, 0x31, 0x9a, 0xbb, 0x9c, 0x7e, 0x2d, 0xb7, 0x01, 0x44, 0x2b, 0x48, 0x58,
    0xf7, 0x13, 0xab, 0x96, 0x74, 0xc0, 0x9f, 0x10, 0xe6, 0xa3, 0x85, 0x6b, 0x98, 0xec, 0x21, 0x19,
    0xee, 0x7f, 0x79, 0xe1, 0x66, 0x6d, 0x18, 0xb9, 0x49, 0x11, 0x88, 0x6e, 0x1c, 0xa5, 0x72, 0x0d,
    0x38, 0xea, 0x68, 0x20, 0x0b, 0x9e, 0xd4, 0x76, 0xe4, 0x69, 0x22, 0x00, 0xfb, 0xb5, 0x4b, 0x91
]

inv_sbox = [
    0xFB, 0xCB, 0x4E, 0x25, 0x92, 0x84, 0x06, 0x6B, 0x73, 0x6E, 0x1B, 0xF4, 0x5F, 0xEF, 0x61, 0x7D,
    0xD7, 0xE9, 0xC3, 0xD1, 0xB6, 0x9D, 0x45, 0x8A, 0xE6, 0xDF, 0xBE, 0x5A, 0xEC, 0x9C, 0x99, 0x0C,
    0xF3, 0xDE, 0xFA, 0x8B, 0x65, 0x8D, 0xB3, 0x13, 0xB4, 0x75, 0x18, 0xCD, 0x80, 0xC9, 0x53, 0x21,
    0x81, 0xC4, 0x42, 0x6D, 0x5D, 0xA7, 0xB8, 0x01, 0xF0, 0x1C, 0xAA, 0x78, 0x27, 0x93, 0x83, 0x55,
    0x9E, 0x44, 0x0B, 0x49, 0xCC, 0x57, 0x05, 0x03, 0xCE, 0xE8, 0x0E, 0xFE, 0x59, 0x9F, 0x3C, 0x63,
    0xA3, 0x43, 0x95, 0xA2, 0x5C, 0x46, 0x58, 0xBD, 0xCF, 0x37, 0x62, 0xC0, 0x10, 0x7A, 0xBB, 0x14,
    0x40, 0x8E, 0x4C, 0x5B, 0xA4, 0x15, 0xE4, 0xAF, 0xF2, 0xF9, 0xB7, 0xDB, 0x12, 0xE5, 0xEB, 0x69,
    0xBF, 0x34, 0xEE, 0x76, 0xD4, 0x5E, 0xF7, 0xC1, 0x97, 0xE2, 0x6F, 0x9A, 0xB1, 0x2D, 0xC8, 0xE1,
    0x38, 0x87, 0x3D, 0xB2, 0x16, 0xDA, 0x0A, 0x02, 0xEA, 0x85, 0x89, 0x20, 0x31, 0x0D, 0xB0, 0x26,
    0xA5, 0xFF, 0x23, 0x24, 0x98, 0xB9, 0xD3, 0x0F, 0xDC, 0x35, 0xC5, 0x79, 0xC7, 0x4A, 0xF5, 0xD6,
    0x36, 0x2F, 0xC2, 0xD9, 0x68, 0xED, 0xBC, 0x3F, 0x67, 0xAD, 0x29, 0xD2, 0x07, 0xB5, 0x2A, 0x77,
    0x30, 0x9B, 0xA6, 0x28, 0x86, 0xFD, 0x8C, 0xCA, 0x4F, 0xE7, 0x1D, 0xC6, 0x88, 0x19, 0xAE, 0xBA,
    0xD5, 0x82, 0x32, 0x66, 0x64, 0x50, 0x00, 0x8F, 0x41, 0x22, 0x71, 0x4B, 0x33, 0xA9, 0x4D, 0x7E,
    0x6A, 0x39, 0x94, 0xA1, 0xF6, 0x48, 0xAB, 0x1E, 0x11, 0x74, 0x1A, 0x3E, 0xA8, 0x7F, 0x3B, 0x04,
    0x09, 0xE3, 0x7B, 0x2E, 0xF8, 0x70, 0xD8, 0x2C, 0x91, 0xAC, 0xF1, 0x56, 0xDD, 0x51, 0xE0, 0x2B,
    0x52, 0x7C, 0x54, 0x08, 0x72, 0x6C, 0x90, 0xD0, 0x3A, 0x96, 0x47, 0xFC, 0x1F, 0x60, 0xA0, 0x17]

def gf_mult(a, b):
    """Multiply two elements in GF(2^8)."""
    result = 0
    for _ in range(8):
        if b & 1:
            result ^= a
        high_bit = a & 0x80
        a = (a << 1) & 0xFF
        if high_bit:
            a ^= ROOT
        b >>= 1
    return result

def matrix_mult(state, coefficients):
    """Helper function for µ and µ⁻¹: Multiply state rows with coefficients in GF(2^8)."""
    new_state = [[0] * 4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            new_state[i][j] = sum(
                gf_mult(coefficients[k], state[i][(j - k) % 4]) for k in range(4)
            ) % 256
    return new_state

def theta(state):
    """Apply the µ transformation to the state."""
    return matrix_mult(state, C_X)

def inv_theta(state):
    """Apply the µ⁻¹ transformation to the state."""
    return matrix_mult(state, INV_C_X)

def gamma(state):
    """Apply the S-box substitution (γ)."""
    return [[sbox[byte] for byte in row] for row in state]

def inv_gamma(state):
    """Apply the inverse S-box substitution (γ⁻¹)."""
    return [[inv_sbox[byte] for byte in row] for row in state]

def pi(state):
    """Transpose the state (π)."""
    return [list(row) for row in zip(*state)]

def sigma(state, round_key):
    """XOR the state with the round key (σ)."""
    return [[state[i][j] ^ round_key[i][j] for j in range(4)] for i in range(4)]

def left_rotate(row):
    """Perform a left byte rotation (rotl) on a 4-byte row."""
    return row[1:] + row[:1]

def right_rotate(row):
    """Perform a right byte rotation (rotr) on a 4-byte row."""
    return row[-1:] + row[:-1]

def key_schedule(key, round_num):
    """
    Generate the next round key based on the current key and round number.

    Parameters:
    key (list of list): The current 4x4 key matrix.
    round_num (int): The round number.

    Returns:
    list of list: The next round key as a 4x4 matrix.
    """
    # Initialize next key
    next_key = [[0] * 4 for _ in range(4)]

    # Handle round constant safely
    if round_num == 0:
        round_constant = 0  # No round constant for the initial round
    else:
        round_constant = (1 << (round_num - 1)) % 256

    # Compute the next round key rows
    next_key[0] = [
        key[0][j] ^ left_rotate(key[3])[j] ^ (round_constant if j == 0 else 0)
        for j in range(4)
    ]
    next_key[1] = [key[1][j] ^ next_key[0][j] for j in range(4)]
    next_key[2] = [key[2][j] ^ next_key[1][j] for j in range(4)]
    next_key[3] = [key[3][j] ^ next_key[2][j] for j in range(4)]

    return next_key


def check_properties(state):
    """Check all properties (Balanced, Constant, All) for the matrix."""
    print(f"State matrix: {state}")  # Debugging: Print the state matrix before checking properties
    balanced = []
    constant = []
    all = []

    # Ensure state is 4x4 matrix
    if len(state) != 4 or len(state[0]) != 4:
        raise ValueError("State must be a 4x4 matrix.")
        
    for j in range(4):
        for k in range(4):
            if isBalanced(state, j, k):
                balanced.append((j, k))
            if isConstant(state, j, k):
                constant.append((j, k))
            if isAll(state, j, k):
                all.append((j, k))

    return balanced, constant, all


def isBalanced(state, j, k):
    """Check if the difference pattern in the (j,k) element is balanced."""
    x = 0
    # Generate multiple states to check for balance
    for i in range(256):
        # Simulate how the state might change with different inputs
        test_state = [[(elem + i) % 256 for elem in row] for row in state]
        x ^= test_state[j][k]
    return x == 0


def isConstant(state, j, k):
    """Check if the (j,k) element is constant across all states."""
    base_value = state[j][k]
    # Generate multiple states to check for constancy
    for i in range(256):
        test_state = [[(elem + i) % 256 for elem in row] for row in state]
        if test_state[j][k] != base_value:
            return False
    return True


def isAll(state, j, k):
    """Check if the (j,k) element contains all values from 0 to 255."""
    # Generate multiple states to check for range
    values = set()
    for i in range(256):
        test_state = [[(elem + i) % 256 for elem in row] for row in state]
        values.add(test_state[j][k])
    return len(values) == 256



def round_function(state, round_key):
    """Perform one round of the cipher with cryptanalysis checks."""
    state = gamma(state)
    print("\nAfter Gamma:")
    balanced, constant, all = check_properties(state)
    print(f"Balanced properties: {balanced}")
    print(f"Constant properties: {constant}")
    print(f"All properties: {all}")

    state = pi(state)
    print("\nAfter Pi:")
    balanced, constant, all = check_properties(state)
    print(f"Balanced properties: {balanced}")
    print(f"Constant properties: {constant}")
    print(f"All properties: {all}")

    state = theta(state)
    print("\nAfter Theta:")
    balanced, constant, all = check_properties(state)
    print(f"Balanced properties: {balanced}")
    print(f"Constant properties: {constant}")
    print(f"All properties: {all}")

    state = sigma(state, round_key)
    print("\nAfter Sigma:")
    balanced, constant, all = check_properties(state)
    print(f"Balanced properties: {balanced}")
    print(f"Constant properties: {constant}")
    print(f"All properties: {all}")

    return state


def inv_round_function(state, round_key):
    """Perform one round of the inverse cipher with cryptanalysis checks."""
    state = sigma(state, round_key)
    print("\nAfter Sigma:")
    balanced, constant, all = check_properties(state)
    print(f"Balanced properties: {balanced}")
    print(f"Constant properties: {constant}")
    print(f"All properties: {all}")

    state = inv_theta(state)
    print("\nAfter Inverse Theta:")
    balanced, constant, all = check_properties(state)
    print(f"Balanced properties: {balanced}")
    print(f"Constant properties: {constant}")
    print(f"All properties: {all}")

    state = pi(state)
    print("\nAfter Pi:")
    balanced, constant, all = check_properties(state)
    print(f"Balanced properties: {balanced}")
    print(f"Constant properties: {constant}")
    print(f"All properties: {all}")

    state = inv_gamma(state)
    print("\nAfter Inverse Gamma:")
    balanced, constant, all = check_properties(state)
    print(f"Balanced properties: {balanced}")
    print(f"Constant properties: {constant}")
    print(f"All properties: {all}")

    return state


def to_matrix(data):
    """Convert a 16-byte string into a 4x4 matrix."""
    assert len(data) == 16, "Data must be exactly 16 bytes."
    return [[data[i * 4 + j] for j in range(4)] for i in range(4)]


def to_bytes(matrix):
    """Convert a 4x4 matrix back into a 16-byte string."""
    return bytes(matrix[i][j] for i in range(4) for j in range(4))




def encrypt(plaintext, key):
    """Encrypt the plaintext with cryptanalysis checks."""
    plaintext = to_matrix(plaintext)
    key = to_matrix(key)
    round_keys = [key] + [key_schedule(key, i) for i in range(ROUNDS)]

    # Initial key addition
    state = sigma(plaintext, round_keys[0])
    print("\nAfter Initial Sigma:")
    balanced, constant, all = check_properties(state)
    print(f"Balanced properties: {balanced}")
    print(f"Constant properties: {constant}")
    print(f"All properties: {all}")

    # Rounds
    for i in range(1, ROUNDS + 1):
        state = round_function(state, round_keys[i])

    return to_bytes(state)


def decrypt(ciphertext, key):
    """Decrypt the ciphertext with cryptanalysis checks."""
    ciphertext = to_matrix(ciphertext)
    key = to_matrix(key)
    round_keys = [key] + [key_schedule(key, i) for i in range(ROUNDS)]

    # Reverse rounds
    state = ciphertext
    for i in range(ROUNDS, 0, -1):
        state = inv_round_function(state, round_keys[i])

    # Final inverse key addition
    state = sigma(state, round_keys[0])

    return to_bytes(state)


# Example usage
plaintext = b"\x01" + b"\x00" * 15  # 16 bytes of plaintext data
key = b"\x2b\x28\xab\x09\x7e\xae\xf7\xcf\x15\xd2\x15\x4f\x16\xa6\x88\x3c"  # 16 bytes key

print("Plaintext:", plaintext.hex())
print("Key:", key.hex())

ciphertext = encrypt(plaintext, key)
print("Ciphertext:", ciphertext.hex())

decrypted = decrypt(ciphertext, key)
print("Decrypted:", decrypted.hex())
