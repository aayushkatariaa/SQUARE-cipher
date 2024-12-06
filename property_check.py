ROOT = 0x1f5  # Generator of GF(2^8), maintains GF(2^8)

# Full S-box for block cipher square (you should include the entire SBOX here)
SBOX = [
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

def inverse_sbox():
    """Generates the inverse of the S-box."""
    inv_sbox = [0] * 256
    for i in range(256):
        inv_sbox[SBOX[i]] = i
    return inv_sbox

def gamma(matrix):
    """Gamma function substitutes bytes using S-box"""
    for i in range(16):
        matrix[i] = SBOX[matrix[i]]

def gamma_inverse(matrix):
    """Gamma function substitutes bytes using the inverse S-box"""
    inv_sbox = inverse_sbox()
    for i in range(16):
        matrix[i] = inv_sbox[matrix[i]]

def pi(matrix):
    """Pi function performs a simple transpose"""
    matrix[1], matrix[4] = matrix[4], matrix[1]
    matrix[2], matrix[8] = matrix[8], matrix[2]
    matrix[6], matrix[9] = matrix[9], matrix[6]
    matrix[3], matrix[0xC] = matrix[0xC], matrix[3]
    matrix[7], matrix[0xD] = matrix[0xD], matrix[7]
    matrix[0xB], matrix[0xE] = matrix[0xE], matrix[0xB]

def sigma(matrix, round_key):
    """Sigma function XORs the key with the matrix"""
    for i in range(16):
        matrix[i] ^= round_key[i]

def times2(n):
    """Used for multiplication by 2 in Galois Field"""
    n = n << 1
    if (n & 0x100) != 0:
        n ^= ROOT
    return n

def key_schedule(round_key, r):
    """Generates the round keys"""
    temp = round_key[0xC]
    round_key[0] ^= r
    round_key[0] ^= round_key[0xD]
    round_key[4] ^= round_key[0]
    round_key[8] ^= round_key[4]
    round_key[0xC] ^= round_key[8]
    round_key[1] ^= round_key[0xE]
    round_key[5] ^= round_key[1]
    round_key[9] ^= round_key[5]
    round_key[0xD] ^= round_key[9]
    round_key[2] ^= round_key[0xF]
    round_key[6] ^= round_key[2]
    round_key[0xA] ^= round_key[6]
    round_key[0xE] ^= round_key[0xA]
    round_key[3] ^= temp
    round_key[7] ^= round_key[3]
    round_key[0xB] ^= round_key[7]
    round_key[0xF] ^= round_key[0xB]
    r = times2(r)

def theta(matrix):
    """Theta function, similar to mix columns in AES, but for rows"""
    temp = [0] * 16
    for i in range(4):
        for j in range(4):
            temp[4 * i + j] = times2(matrix[4 * i + j])
            temp[4 * i + j] ^= matrix[4 * i + ((j + 1) % 4)]
            temp[4 * i + j] ^= times2(matrix[4 * i + ((j + 1) % 4)])
            temp[4 * i + j] ^= matrix[4 * i + ((j + 2) % 4)]
            temp[4 * i + j] ^= matrix[4 * i + ((j + 3) % 4)]
    for j in range(16):
        matrix[j] = temp[j]

def is_balanced(set_, j, k):
    """Check if the given indices follow the 'Balanced' property"""
    x = 0
    for i in range(256):
        x ^= set_[i][j * 4 + k]
    return x == 0

def is_constant(set_, j, k):
    """Check if the given indices follow the 'Constant' property"""
    for i in range(256):
        if set_[0][j * 4 + k] != set_[i][j * 4 + k]:
            return False
    return True

def is_all(set_, j, k):
    """Check if the given indices follow the 'All' property"""
    lane = []
    for i in range(256):
        lane.append(set_[i][j * 4 + k])
    for i in range(256):
        if lane.count(i) == 0:
            return False
    return True

def get_all_indices(set_):
    """Get all indices where the 'All' property holds"""
    indices = []
    for j in range(4):
        for k in range(4):
            if is_all(set_, j, k):
                indices.append([j, k])
    return indices

def get_constant_indices(set_):
    """Get all indices where the 'Constant' property holds"""
    indices = []
    for j in range(4):
        for k in range(4):
            if is_constant(set_, j, k):
                indices.append([j, k])
    return indices

def get_balanced_indices(set_):
    """Get all indices where the 'Balanced' property holds"""
    indices = []
    for j in range(4):
        for k in range(4):
            if is_balanced(set_, j, k):
                indices.append([j, k])
    return indices

def print_matrix(v):
    """Print matrix in a readable format."""
    print("-----------------")
    for i in range(0, len(v), 4):  # iterate over the matrix in chunks of 4 elements
        row = v[i:i+4]
        print("| " + " | ".join(map(str, row)) + " |")
        print("-----------------")

# Example usage:
matrix = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]  
round_key = [0] * 16  # Example round key
r = 0x2  # Example round key parameter

# Perform key scheduling, theta, gamma, etc.
key_schedule(round_key, r)
theta(matrix)
gamma(matrix)
pi(matrix)

# Print the matrix
print_matrix(matrix)
